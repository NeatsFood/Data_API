# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_current_device_status blueprint
def test_get_current_device_status_works(client):
    data = {"device_uuid": global_vars.device_uuid}  
    URL = '/api/get_current_device_status/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert 'results' in rv
    assert 'progress' in rv['results']
    assert 'age_in_days' in rv['results']
    assert 'wifi_status' in rv['results']
    assert 'current_temp' in rv['results']
    assert 'runtime' in rv['results']

def test_get_current_device_status_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_current_device_status/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

