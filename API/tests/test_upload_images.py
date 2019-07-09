# http://flask.pocoo.org/docs/1.0/testing/

import io
from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test upload_images blueprint
def test_upload_images_works(client):
    fn = "tests/dude.jpg"
    data = {"user_token": global_vars.user_token,
            "file": (io.FileIO(fn), fn),
            "type": "user"}
    URL = '/api/upload_images/'
    rv = common.do_form_post(client, data, URL)
    assert 200 == rv['response_code']
    assert 'url' in rv
    assert 0 < len(rv['url'])

def test_upload_images_fails(client):
    data = {} # no data so it should fail
    URL = '/api/upload_images/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

