# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_device_images blueprint
def test_get_device_images_works(client):
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.ACE4_device_uuid}
    URL = '/api/get_device_images/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert 0 < len(rv['image_urls'])

def test_get_device_images_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_device_images/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

