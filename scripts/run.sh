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
export FLASK_APP=main.py

python3 -m flask run
#gunicorn -b :5000 main:app
