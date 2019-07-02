import base64
import json, os
from .utils.env_variables import storage_client
from flask import Blueprint, render_template, Request, Response


GOOGLE_CLOUD_STORAGE = "openag-v1-images"
MEDIUM_FILE_SUFFIX = "_medium"

viewimage_bp = Blueprint('viewimage_bp', __name__)

@viewimage_bp.route("/viewImage/<imageData>")
def viewimage(imageData):
    imageDataString = base64.b64decode(imageData)
    imageObject = json.loads(imageDataString.decode('utf-8'))
    filename = imageObject['i'].split('/')[-1]
    # Find files with the filename - .png as a prefix
    file_prefix = filename.split('.')[0]
    blob_list = storage_client.get_bucket(GOOGLE_CLOUD_STORAGE).list_blobs(prefix=file_prefix)
    # Now look for the _medium version... if it exists then pass that to the view.
    for blob in blob_list:
        if MEDIUM_FILE_SUFFIX in blob.name:
            imageObject['i'] = imageObject['i'].replace(filename, blob.name)
            break

    return render_template('viewImage.html', imageFile=imageObject['i'], imageText=imageObject['t'])