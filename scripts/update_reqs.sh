#!/bin/bash

# Update up the python environment for local development.

# Get the path to parent directory of this script.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
cd $DIR # Go to the project top level dir.

cd $DIR/API
source pyenv/bin/activate
pip3 install --requirement $DIR/config/requirements.txt
pip3 install --requirement $DIR/API/cloud_common/config/requirements.txt 


