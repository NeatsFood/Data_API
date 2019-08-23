#!/bin/bash

# Run the python Flask API locally for development.

# Get the path to parent directory of this script.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
cd $DIR # Go to the project top level dir.

# Since we are running locally, we have to set our env. vars.
if [[ -z "${GOOGLE_APPLICATION_CREDENTIALS}" ]]; then
  # gcloud_env.bash has not been sourced, so do it now
  source $DIR/config/gcloud_env.bash
fi

# Deactivate any current python virtual environment we may be running.
if ! [ -z "${VIRTUAL_ENV}" ] ; then
    deactivate
fi

source $DIR/API/pyenv/bin/activate

cd $DIR/API
export PYTHONPATH=$DIR/API

python3 -c 'import sys
from cloud_common.cc.google import iot
device_uuid="EDU-4F882E84-c4-b3-01-8d-9b-8c"
cmd = [{"command": "START_RECIPE", "arg0": "{\"format\": \"openag-phased-environment-v1\", \"version\": \"1\", \"creation_timestamp_utc\": \"2019-07-18T10:14:41Z\", \"name\": \"Demo Rainbow\", \"uuid\": \"6ad1c2c7-c2ff-4af0-aa8f-5a163e652b26\", \"parent_recipe_uuid\": null, \"support_recipe_uuids\": null, \"description\": {\"brief\": \"Demo Recipe to cycle through different colors\", \"verbose\": \"Demo Recipe to cycle through different colors\"}, \"authors\": [{\"name\": \"Steve Moore\", \"email\": \"srmoore@openagfoundation.org\", \"uuid\": \"d2c7fe68-e857-4c4a-98b4-7e88154ddaa6\"}], \"cultivars\": [{\"name\": \"Genovese Basil\", \"uuid\": \"9dc80135-0c24-4a65-ae0b-95f1c5e53676\"}], \"cultivation_methods\": [{\"name\": \"Shallow Water Culture\", \"uuid\": \"30cbbded-07a7-4c49-a47b-e34fc99eefd0\"}], \"environments\": {\"sun\": {\"name\": \"Sun\", \"light_spectrum_nm_percent\": {\"380-399\": 2.03, \"400-499\": 20.3, \"500-599\": 23.27, \"600-700\": 31.09, \"701-780\": 23.31}, \"light_ppfd_umol_m2_s\": 300, \"light_illumination_distance_cm\": 15}, \"summer_sun\": {\"name\": \"Summer Sun\", \"light_spectrum_nm_percent\": {\"380-399\": 2.03, \"400-499\": 20.3, \"500-599\": 23.27, \"600-700\": 31.09, \"701-780\": 23.31}, \"light_ppfd_umol_m2_s\": 400, \"light_illumination_distance_cm\": 15}, \"red\": {\"name\": \"Red\", \"light_spectrum_nm_percent\": {\"380-399\": 0.0, \"400-499\": 0.0, \"500-599\": 0.0, \"600-700\": 100.0, \"701-780\": 0.0}, \"light_ppfd_umol_m2_s\": 300, \"light_illumination_distance_cm\": 15}, \"green\": {\"name\": \"Green\", \"light_spectrum_nm_percent\": {\"380-399\": 0.0, \"400-499\": 0.0, \"500-599\": 100.0, \"600-700\": 0.0, \"701-780\": 0.0}, \"light_ppfd_umol_m2_s\": 300, \"light_illumination_distance_cm\": 15}, \"blue\": {\"name\": \"Blue\", \"light_spectrum_nm_percent\": {\"380-399\": 0.0, \"400-499\": 100.0, \"500-599\": 0.0, \"600-700\": 0.0, \"701-780\": 0.0}, \"light_ppfd_umol_m2_s\": 300, \"light_illumination_distance_cm\": 15}, \"night\": {\"name\": \"Night\", \"light_spectrum_nm_percent\": {\"380-399\": 0.0, \"400-499\": 0.0, \"500-599\": 0.0, \"600-700\": 0.0, \"701-780\": 0.0}, \"light_ppfd_umol_m2_s\": 0, \"light_illumination_distance_cm\": 15}}, \"phases\": [{\"name\": \"Demo Lights\", \"repeat\": 35, \"cycles\": [{\"name\": \"Red\", \"environment\": \"red\", \"duration_hours\": 0.01}, {\"name\": \"Blue\", \"environment\": \"blue\", \"duration_hours\": 0.01}, {\"name\": \"Green\", \"environment\": \"green\", \"duration_hours\": 0.01}, {\"name\": \"Sun\", \"environment\": \"sun\", \"duration_hours\": 0.01}, {\"name\": \"Summer Sun\", \"environment\": \"summer_sun\", \"duration_hours\": 0.01}, {\"name\": \"Night\", \"environment\": \"night\", \"duration_hours\": 0.01}]}]}", "arg1": "0"}]
iot.send_recipe_to_device_via_IoT(device_uuid,cmd)
'



