# http://flask.pocoo.org/docs/1.0/testing/

import pytest
import json
import main # our main flask app

# global cached values, so we don't have to keep logging in
user_token = None


# This pytest fixture runs for every test, it sets up the flask environment.
@pytest.fixture
def client():
    # do config
    main.app.config['TESTING'] = True
    client = main.app.test_client()
    #print(f'{__name__} client fixture')
    """
    with main.app.app_context():
        # do more setup with the context?
        main.init_db()
    """
    yield client

#debugrob: don't think we need GET  rv = client.get('/login/', follow_redirects=True)

# This is a common function to do a POST to a Flask URL.
# Returns the result of the POST.
def do_post(client, post_data_dict, URL):
    rv = client.post(URL, json=post_data_dict, follow_redirects=True)
    print(f'{URL} result={rv.get_json()}')
    return rv.get_json()


#------------------------------------------------------------------------------
# test user_authenticate blueprint
def test_login_works(client):
    data = { "username": "testman",
             "password": "testman" }
    URL = '/login/'
    rv = do_post(client, data, URL)
    assert 200 == rv['response_code']
    # global token used by all other tests that require it
    global user_token 
    user_token = rv['user_token'] 

def test_login_no_username(client):
    data = { "username": "",
             "password": "fail" }
    URL = '/login/'
    rv = do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_login_no_password(client):
    data = { "username": "fail",
             "password": "" }
    URL = '/login/'
    rv = do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_signup_works(client):
    data = { "username": "test",
             "password": "test",
             "email_address": "test@gmail.com",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_signup_no_username(client):
    data = { "username": "",
             "password": "test",
             "email_address": "test@gmail.com",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_signup_no_password(client):
    data = { "username": "fail",
             "password": "",
             "email_address": "test@gmail.com",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_signup_no_email(client):
    data = { "username": "fail",
             "password": "asfd",
             "email_address": "",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_signup_bad_email(client):
    data = { "username": "fail",
             "password": "asfd",
             "email_address": "fail@no_domain",
             "organization": "OpenAg",
             "testing": "True" }
    URL = '/api/signup/'
    rv = do_post(client, data, URL)
    assert 500 == rv['response_code']


#------------------------------------------------------------------------------
# test get_user_info blueprint
def test_get_user_info_works(client):
    # send user_token that we cached globally from an earlier test
    data = { "user_token": user_token }
    URL = '/api/get_user_info/'
    rv = do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_get_user_info_fails(client):
    # send user_token that we cached globally from an earlier test
    data = {}
    URL = '/api/get_user_info/'
    rv = do_post(client, data, URL)
    assert 500 == rv['response_code']



# datastore.get_client()

""" debugrob: test all endpoints in these

    apply_to_device, 
    apply_recipe_to_device,
    get_current_recipe, 
    get_co2_details,
    get_current_stats, 
    get_temp_details, 
    get_user_devices, 
    get_recipe_by_uuid,
    register_device, 
    get_all_recipes, 
    get_device_types, 
    submit_recipe,
    get_plant_types, 
    submit_recipe_change, 
    verify_user_session,
    upload_images, 
    get_device_peripherals,
    get_device_images,
    submit_horticulture_measurements,
    get_current_recipe_info, 
    save_user_profile_changes, 
    get_current_device_status,
    daily_horticulture_measurements, 
    get_horticulture_daily_logs,
    get_device_notifications, 
    ack_device_notification,
    view_image
"""
