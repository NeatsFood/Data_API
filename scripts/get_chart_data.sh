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

source $DIR/API/pyenv/bin/activate
cd $DIR/API
export PYTHONPATH=$DIR/API

python3 -c 'import sys, logging
from cloud_common.cc.google import datastore
from cloud_common.cc.google import database
from FCClass.user import User
from FCClass.user_session import UserSession

logging.basicConfig(level=logging.DEBUG) 

device_uuid="EDU-F489B205-b8-27-eb-bf-8b-94" # PFC-aged-snowflake

temp, RH, co2, leaf_count, plant_height = \
    database.get_all_historical_values(device_uuid, None, None)
print(temp, RH, co2, leaf_count, plant_height)

#Not needed now
#username="training"
#password="OpenAg12"
#user = User(username=username, password=password)
#user_uuid, is_admin = user.login_user(client=datastore.get_client())
#if user_uuid is None:
#    print("Login failed. Please check your credentials.")
#    return
#user_token = UserSession(user_uuid=user_uuid).insert_into_db(
#        client=datastore.get_client())

'



