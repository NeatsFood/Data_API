# http://flask.pocoo.org/docs/1.0/testing/

import time
from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test submit_recipe blueprint
def test_submit_recipe_works(client):
    # must delay before submitting a recipe, since other tests also send and 
    # google iot will only let us send one "configuration" to a device per sec.
    time.sleep(1) 
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.device_uuid,
            "testing": "True"}
    URL = '/api/submit_recipe/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_submit_recipe_fails(client):
    data = {} # no data so it should fail
    URL = '/api/submit_recipe/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

