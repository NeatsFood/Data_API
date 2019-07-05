# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_recipe_by_uuid blueprint
def test_get_recipe_by_uuid_works(client):
    data = {"user_token": global_vars.user_token,   # for user testman
            "recipe_uuid": global_vars.recipe_uuid}
    URL = '/api/get_recipe_by_uuid/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_get_recipe_by_uuid_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_recipe_by_uuid/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

