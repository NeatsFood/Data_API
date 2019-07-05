# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_device_notifications blueprint
def test_get_device_notifications_works(client):
    data = {"device_uuid": global_vars.device_uuid}   
    URL = '/api/get_device_notifications/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_get_device_notifications_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_device_notifications/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

