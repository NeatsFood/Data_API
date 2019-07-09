#!/bin/bash

# Build the API documentation.

DOC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DOC_DIR
source $DOC_DIR/pyenv/bin/activate
export PYTHONPATH=$DOC_DIR
if [[ -z "${GOOGLE_APPLICATION_CREDENTIALS}" ]]; then
  source $DOC_DIR/../../config/gcloud_env.bash
fi

cd $DOC_DIR
make clean html

# this is ugly!
#make clean markdown
