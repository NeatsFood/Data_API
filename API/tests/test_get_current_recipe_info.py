# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_current_recipe_info blueprint
def test_get_current_recipe_info_works(client):
    data = {"user_token": global_vars.user_token,
            "device_uuid": global_vars.device_uuid}
    URL = '/api/get_current_recipe_info/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_get_current_recipe_info_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_current_recipe_info/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

