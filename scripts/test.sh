#!/bin/bash

# TEST the python Flask API.

# You can pass in tests you want on the command line in this format:
# tests/test_API.py::test_<name>
#
# e.g. this is how you run the test_verify_user_session_works test,
# which requires a valid session token, so you run the test_login_works first:
#
# ./scripts/test.sh tests/test_API.py::test_login_works tests/test_API.py::test_verify_user_session_works


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

# tests are in the API/tests dir
py.test -v --capture=no --disable-pytest-warnings $*

