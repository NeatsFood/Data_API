#!/bin/bash

# Set up the python environment for local development.

# Get the path to parent directory of this script.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
cd $DIR # Go to the project top level dir.

# deactivate any current python virtual environment we may be running
if ! [ -z "${VIRTUAL_ENV}" ] ; then
    deactivate
fi

cd $DIR/flask
rm -fr pyenv __pycache__  
python3.6 -m venv pyenv
source pyenv/bin/activate
pip3 install --requirement $DIR/config/requirements.txt
pip3 install --requirement $DIR/flask/cloud_common/config/requirements.txt 

deactivate

