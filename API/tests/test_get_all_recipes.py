# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_all_recipes blueprint
def test_get_all_recipes_works(client):
    data = {"user_token": global_vars.user_token}   # for user testman
    URL = '/api/get_all_recipes/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert 'results' in rv
    assert 'devices' in rv

def test_get_all_recipes_fails(client):
    data = {} # no data so it should fail
    URL = '/api/get_all_recipes/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

