# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test apply_to_device blueprint
def test_apply_to_device_works(client):
    data = {"user_token": global_vars.user_token,   # for user testman
            "device_uuid": global_vars.device_uuid, # for testman's device
            "recipe_uuid": global_vars.recipe_uuid} # get growing basil
    URL = '/api/apply_to_device/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_apply_to_device_fails(client):
    data = {} # no data so it should fail
    URL = '/api/apply_to_device/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_apply_to_device_no_token(client):
    data = { "user_token": None,        # wrong
             "device_uuid": global_vars.device_uuid, 
             "recipe_uuid": global_vars.recipe_uuid}
    URL = '/api/apply_to_device/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_apply_to_device_no_device(client):
    data = { "user_token": global_vars.user_token,   
             "device_uuid": None, # wrong
             "recipe_uuid": global_vars.recipe_uuid}
    URL = '/api/apply_to_device/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_apply_to_device_no_recipe(client):
    data = { "user_token": global_vars.user_token,   
             "device_uuid": global_vars.device_uuid,
             "recipe_uuid": None} # wrong
    URL = '/api/apply_to_device/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']


