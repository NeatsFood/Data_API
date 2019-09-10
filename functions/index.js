// Reference: https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-nodejs
// Run Locally:
//    export GOOGLE_APPLICATION_CREDENTIALS="[PATH]/Data_API/config/service_account.json"
//    firebase serve

const functions = require('firebase-functions');
const { BigQuery } = require('@google-cloud/bigquery');
const { Storage } = require('@google-cloud/storage');
const JSZip = require('jszip');
const fse = require('fs-extra');
const jsonexport = require('jsonexport');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

exports.helloWorld = functions.https.onRequest((request, response) => {
  response.send("Hello from Firebase!");
});

// exports.listFiles = functions.https.onRequest((request, response) => {
//   fs.readdir(__dirname, (error, files) => {
//     if (error) {
//       console.error(error);
//       response.sendStatus(500);
//     } else {
//       console.log('Files', files);
//       response.sendStatus(200);
//     }
//   });
// });

exports.createRecipeRunDataZip = functions.https.onRequest(async (request, response) => {
  console.log('Creating recipe run data zip');

  // Get parameters
  const deviceId = 'EDU-BA5E7012-f4-5e-ab-5b-4f-d2';
  const startTimestamp = '2019-08-06';
  const endTimestamp = '2019-08-20';

  // Format directory name
  const dirname = `/tmp/${deviceId}_${startTimestamp}_to_${endTimestamp}`;

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

  // Save data as csv
  console.log('Saving data as csv');
  await jsonexport(rows, { rowDelimiter: ',' }, (csv) => {
    if (fse.pathExistsSync(dirname)) fse.removeSync(dirname);
    fse.ensureDirSync(dirname);
    fse.writeFileSync(`${dirname}/data.csv`, csv);
  });

  // Create zip file
  console.log('Zipping file');
  const zip = new JSZip();
  const zipfile = zip.folder(dirname);
  fse.writeFileSync(`${dirname}.zip`, zipfile);

  // Return success
  response.send("Successfully created recipe run data zip");
});
