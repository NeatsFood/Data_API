import json
from flask import Blueprint, request

from FCClass.user import User
from cloud_common.cc.google import env_vars
from cloud_common.cc.google import datastore
from .utils.response import success_response, error_response
from .utils.auth import get_user_uuid_from_token


save_user_profile_bp = Blueprint('save_user_profile_bp', __name__)

@save_user_profile_bp.route('/api/save_user_profile_changes/', methods=['POST'])
def save_user_profile_changes():
    """Update the users' profile information.

    .. :quickref: User; Update profile 

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string email_address: Users email address
    :<json string username: Users username (and login name)
    :<json string organization: The organizaion the user is associated with

    **Example response**:

        .. sourcecode:: json

          {
            "profile_image": "previously saved profile image",
            "username": "saved name",
            "email_address": "saved email address",
            "organization": "saved organization",
            "response_code": 200
          }
    """
    received_form_response = request.get_json()

    user_token = received_form_response.get("user_token")
    if user_token is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    query = datastore.get_client().query(kind='Users')
    query.add_filter('user_uuid', '=', user_uuid)
    user = list(query.fetch(1))[0]

    # This checks if inputs are empty strings as well.
    email_address = get_non_empty(received_form_response,
                                  'email_address',
                                  user['email_address'])
    username = get_non_empty(received_form_response,
                             'username',
                             user['username'])
    org = get_non_empty(received_form_response,
                        'organization',
                        user['organization'])

    if not datastore.update_user(user_uuid, username, email_address, org):
        return error_response("nope")

    return success_response(
        profile_image=user.get('profile_image'),
        username=user.get('username'),
        email_address=user.get('email_address'),
        organization=user.get('organization')
    )

def get_non_empty(form_input, key, default):
    """dict.get that replaces empty strings with the default value as well"""
    value = form_input.get(key, default)
    if not value:
        value = default
    return value
