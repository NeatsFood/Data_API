# http://flask.pocoo.org/docs/1.0/testing/

import pytest
import main # our main flask app

"""
For these tests to all pass, we require:
    A UI user named "testman" with password "testman".
    The 'testman' user needs a device associated with their UI account.
    There needs to be one available recipe in the datastore Recipes collection.
"""

# This pytest fixture runs for every test, it sets up the flask environment.
@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    client = main.app.test_client()
    """
    print(f'{__name__} client fixture')
    with main.app.app_context():
        # do more setup with the context?
        #main.init_db()
    """
    yield client

