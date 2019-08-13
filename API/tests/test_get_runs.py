# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common

# one of Steve's test machines
device_uuid = 'EDU-962B82D7-b8-27-eb-bf-8b-94'

#------------------------------------------------------------------------------
# test get_recipe_by_uuid blueprint
def test_get_runs_works(client):
    data = {"user_token": global_vars.user_token,   # for user testman
            "device_uuid": device_uuid}
    URL = '/api/get_runs/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_get_runs_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_runs/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

