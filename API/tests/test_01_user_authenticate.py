# http://flask.pocoo.org/docs/1.0/testing/

import time
from global_vars import global_vars # global vars used in tests
import common

# Test user_authenticate blueprint

def test_login_works(client):
    data = { "username": "testman",
             "password": "testman" }
    URL = '/login/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']
    # global token used by all other tests that require it
    global_vars.user_token = rv['user_token'] 
    # For some wacky reason, have to delay to make sure global is set.
    # Probably caused by pytest starting the next tests before this global is
    # written.
    time.sleep(0.5) 

def test_login_no_username(client):
    data = { "username": "",
             "password": "fail" }
    URL = '/login/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_login_no_password(client):
    data = { "username": "fail",
             "password": "" }
    URL = '/login/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_signup_works(client):
    data = { "username": "test",
             "password": "test",
             "email_address": "test@gmail.com",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_signup_no_username(client):
    data = { "username": "",
             "password": "test",
             "email_address": "test@gmail.com",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_signup_no_password(client):
    data = { "username": "fail",
             "password": "",
             "email_address": "test@gmail.com",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_signup_no_email(client):
    data = { "username": "fail",
             "password": "asfd",
             "email_address": "",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_signup_bad_email(client):
    data = { "username": "fail",
             "password": "asfd",
             "email_address": "fail@no_domain",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']


