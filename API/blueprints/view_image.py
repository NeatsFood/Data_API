import base64
import json, os
from urllib.parse import unquote
from flask import Blueprint, render_template, Request, Response

from cloud_common.cc.google import storage
from cloud_common.cc.google import env_vars
from .utils.response import error_response


MEDIUM_FILE_SUFFIX = "_medium"

viewimage_bp = Blueprint('viewimage_bp', __name__)

@viewimage_bp.route("/viewImage/<imageData>", methods=['GET'])
def viewimage(imageData):
    """Generate a small image page for tweeting.  Returns HTML.

    .. :quickref: Utility; Generate tweet

    :reqheader Accept: application/json
    :<json string i: Image URL to show in the tweet.
    :<json string t: Text to display in the tweet.
    """
    imageDataString = base64.b64decode(imageData)
    imageObject = json.loads(imageDataString.decode('utf-8'))
    imageString = imageObject['i']
    imageString = unquote(imageString)
    filename = imageString.split('/')[-1]

    # Find files with the filename - .png as a prefix
    file_prefix = filename.split('.')[0]
    bucket = storage.storage_client.get_bucket(env_vars.cs_bucket)
    blob_list = list(bucket.list_blobs(prefix=file_prefix))

    # Now look for the _medium version... 
    # if it exists then pass that to the view.
    found = False
    print("Blobs:")
    for blob in blob_list:
        if MEDIUM_FILE_SUFFIX in blob.name:
            imageString = imageString.replace(filename, blob.name)
            found = True
            break
        if file_prefix in blob.name:
            found = True

    if not found:
        return error_response(message='Invalid URL.')

    # file is in API/templates/
    return render_template('viewImage.html', imageFile=imageString,
            imageText=imageObject['t'])


