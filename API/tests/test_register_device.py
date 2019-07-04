# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common

# test register_device blueprint

def test_register_device_works(client):
    data = {"user_token": global_vars.user_token,   # global, for user testman
            "device_name": "test",
            "device_reg_no": "test",
            "device_notes": "test",
            "device_type": "test",
            "testing": "True"}
    URL = '/api/register/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_register_device_fails(client):
    data = {} # no data so it should fail
    URL = '/api/register/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

