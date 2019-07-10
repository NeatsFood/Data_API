# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_temp_details blueprint
def test_get_temp_details_works(client):
    data = {"selected_device_uuid": global_vars.ACE4_device_uuid,
            "user_token": global_vars.user_token}
    URL = '/api/get_temp_details/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert 'results' in rv
    assert 'RH' in rv['results']
    assert 0 < len(rv['results']['RH'])
    assert 'temp' in rv['results']
    assert 0 < len(rv['results']['temp'])

def test_get_temp_details_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_temp_details/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

