# http://flask.pocoo.org/docs/1.0/testing/

import time
from global_vars import global_vars # global vars used in tests
import common

# test get_user_devices blueprint

def test_get_user_devices_works(client):
    data = {"user_token": global_vars.user_token} 
    URL = '/api/get_user_devices/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert 'results' in rv
    assert 0 < len(rv['results']['devices'])
    global_vars.device_uuid = rv['results']['devices'][0]['device_uuid']
    assert 0 < len(global_vars.device_uuid)
    # For some wacky reason, have to delay to make sure global is set.
    # Probably caused by pytest starting the next tests before this global is
    # written.
    time.sleep(0.5) 


