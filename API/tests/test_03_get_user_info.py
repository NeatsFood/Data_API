# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_user_info blueprint
def test_get_user_info_works(client):
    # send user_token that we cached globally from an earlier test
    data = {"user_token": global_vars.user_token}
    URL = '/api/get_user_info/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    # save for the user profile test
    global_vars.user_email_address = rv['email_address']
    global_vars.user_username = rv['username']
    global_vars.user_organization = rv['organization']
    assert 0 < len(global_vars.user_email_address)
    assert 0 < len(global_vars.user_username)
    assert 0 < len(global_vars.user_organization)

def test_get_user_info_fails(client):
    data = {} # no user_token so it should fail
    URL = '/api/get_user_info/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']


