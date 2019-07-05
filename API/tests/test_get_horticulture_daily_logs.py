# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_horticulture_daily_logs blueprint
def test_get_horticulture_daily_logs_works(client):
    data = {"device_uuid": global_vars.device_uuid}   
    URL = '/api/get_horticulture_daily_logs/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_get_horticulture_daily_logs_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_horticulture_daily_logs/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

