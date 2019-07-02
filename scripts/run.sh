#!/bin/bash

# Run the python Flask API locally for development.

# Get the path to parent directory of this script.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
cd $DIR # Go to the project top level dir.

# deactivate any current python virtual environment we may be running
if ! [ -z "${VIRTUAL_ENV}" ] ; then
    deactivate
fi

source $DIR/API/pyenv/bin/activate

cd $DIR/API
export PYTHONPATH=$DIR/API
export FLASK_APP=main.py
export GOOGLE_APPLICATION_CREDENTIALS=$DIR/config/service_account.json
export FIREBASE_SERVICE_ACCOUNT=$DIR/config/fb_service_account.json
export GCLOUD_PROJECT=openag-v1
export GCLOUD_DEV_REG=device-registry
export GCLOUD_DEV_EVENTS=device-events
export GCLOUD_REGION=us-east1
export GCLOUD_ZONE=us-east1-b
export GCLOUD_NOTIFICATIONS_TOPIC_SUBS=notifications
export BQ_DATASET="openag_public_user_data"
export BQ_TABLE="vals"
export CS_BUCKET="openag-v1-images"
export CS_UPLOAD_BUCKET="openag-public-image-uploads"

python3 -m flask run
