import json
from flask import Response
from flask import request
from flask import Blueprint
from flask import g
from flask_cors import cross_origin
from pyisemail import is_email

from FCClass.user import User
from FCClass.user_session import UserSession

from blueprints.utils.auth import requires_auth0_auth
from .utils.response import success_response, error_response
from cloud_common.cc.google import datastore

user_authenticate = Blueprint('user_authenticate', __name__)


@user_authenticate.route('/api/signup/', methods=['POST'])
def signup():
    """Create a user account.

    .. :quickref: Authentication; Create account

    :reqheader Accept: application/json
    :<json string username: Users login name
    :<json string email_address: Users email address
    :<json string password: Users password
    :<json string organization: Users organization (self chosen)

    **Example response**:

        .. sourcecode:: json

          {
            "response_code": 200
          }
    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    username = received_form_response.get("username")
    email_address = received_form_response.get("email_address")
    password = received_form_response.get("password")
    organization = received_form_response.get("organization")
    testing = received_form_response.get("testing")

    if not (username and email_address and password):
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    if not is_email(email_address, check_dns=True):
        return error_response(
            message="Invalid email."
        )

    if testing:  # our pytest is hitting this API, so don't create the user
        return success_response()

    user_uuid = User(username=username, password=password,
                     email_address=email_address,
                     organization=organization).insert_into_db(datastore.get_client())

    if user_uuid:
        return success_response()
    else:
        return error_response(
            message="User creation failed."
        )


def signup_user_oauth():
    """Create a user account from oidc user info.

    .. :quickref: Authentication; Create account

    :reqheader Accept: application/json
    :<json string username: Users login name
    :<json string email_address: Users email address
    :<json string password: Users password
    :<json string organization: Users organization (self chosen)

    **Example response**:

        .. sourcecode:: json

          {
            "response_code": 200
          }
    """
    print(g.user_info)
    print(g.current_user)
    username = g.user_info["sub"]
    email_address = g.user_info["email"]
    password = None # received_form_response.get("password")
    organization = None #received_form_response.get("organization")
    testing = False # received_form_response.get("testing")

    if not (username and email_address):
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    if not is_email(email_address, check_dns=True):
        return error_response(
            message="Invalid email."
        )

    if testing:  # our pytest is hitting this API, so don't create the user
        return success_response()

    new_user = User(username=username, password=password,
                     email_address=email_address,
                     organization=organization)
    user_uuid = new_user.insert_into_db(datastore.get_client())
    return new_user


@user_authenticate.route('/login/', methods=['POST'])
def login():
    """Log a user into this API, returns a session token.

    .. :quickref: Authentication; Log in

    :reqheader Accept: application/json
    :<json string username: Users username (from the /api/signup API call)
    :<json string password: Users password (from the /api/signup API call)

    **Example response**:

        .. sourcecode:: json

          {
            "user_uuid": "Users UUID from the registration process",
            "user_token": "token string",
            "is_admin": False
            "message": "Login Successful"
            "response_code": 200
          }
    """
    received_form_response = json.loads(request.data.decode('utf-8'))

    username = received_form_response.get("username")
    password = received_form_response.get("password")

    if not (username and password):
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user = User(username=username, password=password)
    user_uuid, is_admin = user.login_user(client=datastore.get_client())
    if user_uuid is None:
        return error_response(
            message="Login failed. Please check your credentials."
        )

    session_token = UserSession(user_uuid=user_uuid).insert_into_db(
        client=datastore.get_client())
    return success_response(
        user_uuid=user_uuid,
        user_token=session_token,
        is_admin=is_admin,
        message="Login Successful"
    )

# TODO: Make a test for this route. Might need an Auth0 OAuth token
@user_authenticate.route("/oauth_login/", methods=['POST'])
@cross_origin(headers=['Content-Type','Authorization'])
@requires_auth0_auth
def oauth_login():
    client = datastore.get_client()
    query = client.query(kind='Users')
    query.add_filter('email_address', '=', g.user_info['email'])
    query_result = list(query.fetch(1))
    if not query_result:
        user = signup_user_oauth()
    else:
        user = query_result[0]

    user_uuid = user.get('user_uuid')
    is_admin = user.get('is_admin', False)
    if user_uuid is None:
        return error_response(
            message="Login failed. Please check your credentials."
        )
    session_token = UserSession(user_uuid=user_uuid).insert_into_db(
        client=datastore.get_client())
    return success_response(
        user_uuid=user_uuid,
        user_token=session_token,
        is_admin=is_admin,
        message="Login Successful"
    )
