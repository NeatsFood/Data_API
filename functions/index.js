// Reference: https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-nodejs
// Run Locally:
//    export GOOGLE_APPLICATION_CREDENTIALS="[PATH]/Data_API/config/service_account.json"
//    firebase serve

const functions = require('firebase-functions');
const { BigQuery } = require('@google-cloud/bigquery');

exports.helloWorld = functions.https.onRequest((request, response) => {
  response.send("Hello from Firebase!");
});

exports.createRecipeRunDataZip = functions.https.onRequest(async (request, response) => {
  console.log('Creating recipe run data zip');

  // Get parameters
  const deviceId = 'EDU-BA5E7012-f4-5e-ab-5b-4f-d2';
  const startTimestamp = '2019-08-06';
  const endTimestamp = '2019-09-10';

  // Initialize big query
  const bigquery = new BigQuery();

  // Get data from bigquery
  const query = `#standardsql

  # The regex function indexes fields starting at zero!
  # 0: Key
  # 1: var name
  # 2: timestamp
  # 3: device ID
  
  SELECT
    REGEXP_EXTRACT(id, r'(?:[^\~]*\~){3}([^~]*)') as device,
    TIMESTAMP( REGEXP_EXTRACT(id, r'(?:[^\~]*\~){2}([^~]*)')) as report_time,
    REGEXP_EXTRACT(id, r'(?:[^\~]*\~){1}([^~]*)') as var,
    JSON_EXTRACT_SCALAR(values, "$.values[0].name") as name,
    JSON_EXTRACT_SCALAR(values, "$.values[0].value") as value
    , values
    
    FROM openag_public_user_data.vals
  
  WHERE '${deviceId}' = REGEXP_EXTRACT(id, r'(?:[^\~]*\~){3}([^~]*)')
  
    AND 'boot' != REGEXP_EXTRACT(id, r'(?:[^\~]*\~){1}([^~]*)')
    AND 'status' != REGEXP_EXTRACT(id, r'(?:[^\~]*\~){1}([^~]*)')
  
  # eliminate empty values
    AND FALSE = REGEXP_CONTAINS(values, "'value':'None'")
  
  # date range, oldest to newest
   AND TIMESTAMP( REGEXP_EXTRACT(id, r'(?:[^\~]*\~){2}([^~]*)')) <= TIMESTAMP('${endTimestamp}') AND TIMESTAMP( REGEXP_EXTRACT(id, r'(?:[^\~]*\~){2}([^~]*)')) >= TIMESTAMP('${startTimestamp}') 
  
  # order by timestamp  
    ORDER BY REGEXP_EXTRACT(id, r'(?:[^\~]*\~){2}([^~]*)') DESC`

  const options = {
    query: query,
    location: 'US',
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);
  console.log(`Job ${job.id} started.`);

  // Wait for the query to finish
  const [rows] = await job.getQueryResults();

  // Print the results
  console.log('Rows:');
  rows.forEach(row => {
    const { device, report_time, name, value, values } = row;
    const variable = row.var;
    console.log(device, report_time, variable, name, value, values);
  });

  // Return success
  response.send("Successfully created recipe run data zip");
});
