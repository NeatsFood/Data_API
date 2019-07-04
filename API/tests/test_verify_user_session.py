# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test verify_user_session blueprint
def test_verify_user_session_works(client):
    data = { "user_token": global_vars.user_token } # from an earlier test
    URL = '/api/verify_user_session/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    # since we just logged it, session better be valid
    assert False == rv['is_expired'] 
    assert 0 < len(rv['user_uuid'])


