# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test save_user_profile_changes blueprint
def test_save_user_profile_changes_works(client):
    # set, then reset these user properties
    test_email_address = "joe@schmo.abc"
    test_username = "joe.schmo"
    test_organization = "my org"
    data = {"user_token":    global_vars.user_token,
            "email_address": test_email_address,
            "username":      test_username,
            "organization":  test_organization}
    URL = '/api/save_user_profile_changes/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    # now get the user info to verify they were set
    data = {"user_token": global_vars.user_token}
    URL = '/api/get_user_info/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    assert test_email_address == rv['email_address']
    assert test_username == rv['username']
    assert test_organization == rv['organization']
    # now set the user info back to the saved global_vars
    data = {"user_token":    global_vars.user_token,
            "email_address": global_vars.user_email_address,
            "username":      global_vars.user_username,
            "organization":  global_vars.user_organization}
    URL = '/api/save_user_profile_changes/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_save_user_profile_changes_fails(client):
    data = {}
    URL = '/api/save_user_profile_changes/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']


