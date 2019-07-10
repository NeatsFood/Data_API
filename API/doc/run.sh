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

echo ""
echo "After you are happy with how the HTML docs look, please use your browser to save them to a PDF file and check it into the top level docs directory."
echo "Then update the top level README.md to reference the latest PDF."
