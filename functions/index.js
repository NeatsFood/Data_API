/**
 * Google Cloud Functions
 * 
 * Bigquery Reference:
 *  - https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-nodejs
 *
 * Run locally:
 *  - export GOOGLE_APPLICATION_CREDENTIALS="[PATH]/Data_API/config/service_account.json"
 *  - firebase serve
 */

const functions = require('firebase-functions');
const { BigQuery } = require('@google-cloud/bigquery');
const { Storage } = require('@google-cloud/storage');
const os = require('os');
const fse = require('fs-extra');
const jsonexport = require('jsonexport');
var zipdir = require('zip-dir');

/**
 * Create Recipe Run Data Zip
 * 
 * When the mqtt service receives a stop recipe event, it calls this function to 
 * package up the data collected over the recipe duration and uploads it as a 
 * single zip file to the gcloud storage bucket: 'openag-recipe-run-data-zips'
 * 
 * This function is a bit of a one-off and is expected to be deprecated by
 * a future function to 'get crop data' once the data infrastructure matures.
 * 
 * Args:
 *  - deviceId (string): The unique device identifier
 *  - startTimestamp (string): The timestamp string from when the recipe started
 *  - endTimestamp (string): The timestamp string from then the recipe ended
 * 
 * Example request:
 *  - curl -d '{"deviceId":"EDU-BA5E7012-f4-5e-ab-5b-4f-d2", "startTimestamp":"2019-08-06", "endTimestamp":"2019-08-20"}' -H "Content-Type: application/json" -X POST https://us-central1-openag-v1.cloudfunctions.net/createRecipeRunDataZip
 * 
 * Public zip file access:
 *  - Note: Requires any google account to view (doesn't have to be an OpenAg account)
 *  - https://console.cloud.google.com/storage/browser/openag-recipe-run-data-zips
 *  
 */
exports.createRecipeRunDataZip = functions.https.onRequest(async (request, response) => {
  console.log('Creating recipe run data zip');

  // Validate request format
  const contentType = request.get('content-type');
  if (contentType !== 'application/json') {
    return response.status(400).send('Content type must be application/json');
  }

  // Get parameters
  const { deviceId, startTimestamp, endTimestamp } = request.body;
  console.log('deviceId:', deviceId);
  console.log('startTimestamp:', startTimestamp);
  console.log('endTimestamp:', endTimestamp);

  // Validate parameters
  if (!deviceId) return response.status(400).send('deviceId is required');
  if (!startTimestamp) return response.status(400).send('startTimestamp is required');
  if (!endTimestamp) return response.status(400).send('endTimestamp is required');

  // Format directory name
  // Note: Need nested structure so zip file exports a folder instead of an individual file
  const tmpdir = os.tmpdir();
  const filename = `${deviceId}_${startTimestamp}_to_${endTimestamp}`;
  const dirname = `${tmpdir}/${filename}/${filename}`;
  const zipDirname = `${tmpdir}/${filename}`;

  // Initialize big query
  const bigquery = new BigQuery();

  // Initialize query
  const query = `#standardsql

  # The regex function indexes fields starting at zero!
  # 0: Key
  # 1: var name
  # 2: timestamp
  # 3: device ID
  
  SELECT
    REGEXP_EXTRACT(id, r'(?:[^~]*~){3}([^~]*)') as device,
    TIMESTAMP( REGEXP_EXTRACT(id, r'(?:[^~]*~){2}([^~]*)')) as report_time,
    REGEXP_EXTRACT(id, r'(?:[^~]*~){1}([^~]*)') as var,
    JSON_EXTRACT_SCALAR(values, "$.values[0].name") as name,
    JSON_EXTRACT_SCALAR(values, "$.values[0].value") as value
    , values
    
    FROM openag_public_user_data.vals
  
  WHERE '${deviceId}' = REGEXP_EXTRACT(id, r'(?:[^~]*~){3}([^~]*)')
  
    AND 'boot' != REGEXP_EXTRACT(id, r'(?:[^~]*~){1}([^~]*)')
    AND 'status' != REGEXP_EXTRACT(id, r'(?:[^~]*~){1}([^~]*)')
  
  # eliminate empty values
    AND FALSE = REGEXP_CONTAINS(values, "'value':'None'")
  
  # date range, oldest to newest
   AND TIMESTAMP( REGEXP_EXTRACT(id, r'(?:[^~]*~){2}([^~]*)')) <= TIMESTAMP('${endTimestamp}') AND TIMESTAMP( REGEXP_EXTRACT(id, r'(?:[^~]*~){2}([^~]*)')) >= TIMESTAMP('${startTimestamp}') 
  
  # order by timestamp  
    ORDER BY REGEXP_EXTRACT(id, r'(?:[^~]*~){2}([^~]*)') DESC`

  const options = {
    query: query,
    location: 'US',
  };

  // Run the query
  console.log('Running query');
  const [job] = await bigquery.createQueryJob(options);
  const [rows] = await job.getQueryResults();

  // Export data as csv
  console.log('Converting data to csv');
  await jsonexport(rows, { rowDelimiter: ',' }, (error, csv) => {

    // Verify json exported to csv
    if (error) {
      return response.status(500).send('Unable to convert data to csv');
    }

    // Save csv data to file
    if (fse.pathExistsSync(zipDirname)) fse.removeSync(zipDirname);
    fse.ensureDirSync(dirname);
    return fse.writeFileSync(`${dirname}/data.csv`, csv);
  });

  // Export data as zip file
  console.log('Zipping file');
  return zipdir(zipDirname, { saveTo: `${zipDirname}.zip` }, async (error, buffer) => {

    // Verify data exported to zip
    if (error) {
      return response.status(500).send('Unable to zip file');
    }

    // Upload zip file to cloud storage
    console.log('Uploading zip file to cloud storage');
    const storage = new Storage();
    const bucketName = 'openag-recipe-run-data-zips'
    await storage.bucket(bucketName).upload(`${zipDirname}.zip`, {
      gzip: true,
      metadata: {
        cacheControl: 'public, max-age=31536000',
      },
    });

    // Clean up files
    console.log('Cleaning up files');
    fse.removeSync(zipDirname);

    // Return success
    console.log('Successfully created recipe run data zip');
    return response.send("Successfully created recipe run data zip");
  });
});
