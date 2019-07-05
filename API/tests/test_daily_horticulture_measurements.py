# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test daily_horticulture_measurements blueprint
def test_daily_horticulture_measurements_works_empty(client):
    data = {"device_uuid": global_vars.device_uuid} 
    URL = '/api/daily_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_daily_horticulture_measurements_works_with_data(client):
    data = {"device_uuid": global_vars.device_uuid,
            "plant_height": "test",
            "leaf_count": "test",
            "leaf_colors": "test",
            "leaf_withering": "test",
            "flavors": "test",
            "root_colors": "test",
            "horticulture_notes": "test",
            "submission_name": "test"}
    URL = '/api/daily_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_daily_horticulture_measurements_fails(client):
    data = {} # no data so it should fail
    URL = '/api/daily_horticulture_measurements/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

