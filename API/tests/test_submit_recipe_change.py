# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


"""
#------------------------------------------------------------------------------
# test debugrob blueprint
def test_debugrob_works(client):
    data = {"user_token": global_vars.user_token}   # for user testman
    URL = '/api/debugrob/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_debugrob_fails(client):
    data = {} # no data so it should fail
    URL = '/api/debugrob/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

"""
