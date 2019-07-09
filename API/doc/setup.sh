#!/bin/bash

# Set up the python environment for local development.

# Get the path to the directory of this script.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR # Go to this dir.

rm -fr pyenv __pycache__  
python3.6 -m venv pyenv
source pyenv/bin/activate
pip3 install --requirement $DIR/requirements.txt
pip3 install --requirement $DIR/../../config/requirements.txt
pip3 install --requirement $DIR/../cloud_common/config/requirements.txt

deactivate

