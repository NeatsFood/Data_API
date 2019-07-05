# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common


#------------------------------------------------------------------------------
# test get_device_types blueprint
def test_get_device_types_works(client):
    data = {"user_token": global_vars.user_token}   # for user testman
    URL = '/api/get_device_types/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

# no failure case for this api
