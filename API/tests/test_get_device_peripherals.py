# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


# Currently in the datastore there are no Peripheral entities, so this
# will always fail.  The UI no longer uses them, but may in the future.

#------------------------------------------------------------------------------
# test get_device_peripherals blueprint
def test_get_device_peripherals_should_fail(client):
    data = {"user_token": global_vars.user_token} 
    URL = '/api/get_device_peripherals/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_get_device_peripherals_no_peripherals(client):
    data = {} # no data 
    URL = '/api/get_device_peripherals/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_get_device_peripherals_fails(client):
    data = {"selected_peripherals": "bad_peripheral_uuid", # bad data 
            "user_token": global_vars.user_token}
    URL = '/api/get_device_peripherals/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

