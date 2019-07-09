# http://flask.pocoo.org/docs/1.0/testing/

import json
import base64
from global_vars import global_vars # global vars used in tests
import common


# Translated from the UI JS code in 
# EDU_UI/react/src/js/components/device/device_images.js
# (used by getTwitterUri())
def getEncodedImagename(imageName):
    dataToSend = {"i":imageName,
                  "t": "Image from a PFC EDU taken on Thorsday"}
    json_str = json.dumps(dataToSend)
    json_bytes = json_str.encode('utf-8')
    json_b64 = base64.b64encode(json_bytes)
    json_b64_str = json_b64.decode('utf-8')
    return json_b64_str


#------------------------------------------------------------------------------
# test viewImage blueprint
def test_viewImage_works(client):
    # test image URL from my simulated mac (without the .png at the end)
    gizmo = 'https://storage.googleapis.com/openag-v1-images/EDU-39BD6A22-c4-b3-01-8d-9b-8c_2019-06-29-T00:19:17Z_Camera-Top'
    gizmo_URL = gizmo + '.png'
    imageData = getEncodedImagename(gizmo_URL) 
    URL = '/viewImage/' + imageData
    rv = common.do_get(client, URL)
    assert 200 == rv.status_code
    assert gizmo in rv.data.decode('utf-8')

def test_viewImage_fails(client):
    doesnt_exist = 'https://storage.googleapis.com/openag-v1-images/nope.png'
    imageData = getEncodedImagename(doesnt_exist) 
    URL = '/viewImage/' + imageData
    rv = common.do_get(client, URL)
    assert 500 == rv.status_code

