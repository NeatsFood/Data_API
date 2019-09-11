// Reference: https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-nodejs
// Run Locally:
//    export GOOGLE_APPLICATION_CREDENTIALS="[PATH]/Data_API/config/service_account.json"
//    firebase serve

const functions = require('firebase-functions');
const { BigQuery } = require('@google-cloud/bigquery');
const { Storage } = require('@google-cloud/storage');
const fse = require('fs-extra');
const jsonexport = require('jsonexport');
var zipdir = require('zip-dir');

exports.helloWorld = functions.https.onRequest((request, response) => {
  response.send("Hello from Firebase!");
});

exports.createRecipeRunDataZip = functions.https.onRequest(async (request, response) => {
  console.log('Creating recipe run data zip');

  // Get parameters
  const deviceId = 'EDU-BA5E7012-f4-5e-ab-5b-4f-d2';
  const startTimestamp = '2019-08-06';
  const endTimestamp = '2019-08-20';

  // Validate parameters
  

  // Format directory name
  const filename = `${deviceId}_${startTimestamp}_to_${endTimestamp}`;
  const dirname = `/tmp/${filename}/${filename}`;
  const zipDirname = `/tmp/${filename}`;

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
  let csvData;
  console.log('Converting data to csv');
  await jsonexport(rows, { rowDelimiter: ',' }, (error, csv) => {

    // Verify json exported to csv
    if (error) { 
      return response.status(500).send('Unable to convert data to csv');
    }

    // Save csv data to file
    if (fse.pathExistsSync(zipDirname)) fse.removeSync(zipDirname);
    fse.ensureDirSync(dirname);
    fse.writeFileSync(`${dirname}/data.csv`, csv);
  });

  // Create zip file
  console.log('Zipping file');
  await zipdir(zipDirname, { saveTo: `${zipDirname}.zip` }, (error, buffer) => {
    if (error) {
      response.status(500).send('Unable to zip file');
    }
  });

  // Upload file to cloud storage
  console.log('Uploading to cloud storage');
  const storage = new Storage();
  const bucketName = 'openag-recipe-run-data-zips'
  await storage.bucket(bucketName).upload(`${zipDirname}.zip`, {
    gzip: true,
    metadata: {
      cacheControl: 'public, max-age=31536000',
    },
  });

  // Clean up created files
  fse.removeSync(zipDirname);

  // Return success
  response.send("Successfully created recipe run data zip");
});
