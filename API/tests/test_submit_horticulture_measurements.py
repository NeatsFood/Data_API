# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test submit_horticulture_measurements blueprint
def test_submit_horticulture_measurements_works(client):
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.device_uuid,
            "leaves_count": "3",
            "plant_height": "9"}
    URL = '/api/submit_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_submit_horticulture_measurements_fails(client):
    data = {} # no data so it should fail
    URL = '/api/submit_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_submit_horticulture_measurements_fail1(client):
    data = {
            "device_uuid": global_vars.device_uuid,
            "leaves_count": "3",
            "plant_height": "9"}
    URL = '/api/submit_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_submit_horticulture_measurements_fail2(client):
    data = {"user_token": global_vars.user_token,
            
            "leaves_count": "3",
            "plant_height": "9"}
    URL = '/api/submit_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_submit_horticulture_measurements_fail3(client):
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.device_uuid,
            
            "plant_height": "9"}
    URL = '/api/submit_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_submit_horticulture_measurements_fail4(client):
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.device_uuid,
            "leaves_count": "3"
            }
    URL = '/api/submit_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

