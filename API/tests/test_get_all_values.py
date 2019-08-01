# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
def test_get_all_values_no_date_range_works(client):
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.ACE4_device_uuid,
            "start_ts": None,
            "end_ts": None}
    URL = '/api/get_all_values/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert "RH" in rv
    assert "temp" in rv
    assert "co2" in rv
    assert "leaf_count" in rv
    assert "plant_height" in rv

def test_get_all_values_date_range_works(client):
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.ACE4_device_uuid,
            "start_ts": '2019-07-17T10:01:36Z',
            "end_ts": '2019-07-17T10:26:40Z'}
    URL = '/api/get_all_values/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert "RH" in rv
    assert "temp" in rv
    assert "co2" in rv
    assert "leaf_count" in rv
    assert "plant_height" in rv

def test_get_all_values_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_all_values/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_get_all_values_as_csv_works(client):
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.ACE4_device_uuid,
            "start_ts": '2019-07-17T10:01:36Z',
            "end_ts": '2019-07-17T10:26:40Z'}
    URL = '/api/get_all_values_as_csv/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert "CSV" in rv

















