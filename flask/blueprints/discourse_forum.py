from flask import Blueprint, request
import json

from .utils.env_variables import datastore_client
from .utils.response import (success_response, error_response)
from .utils.auth import get_user_uuid_from_token
from .utils.common import is_expired
from . import utils
from google.cloud import datastore

forum_bp = Blueprint('forum_bp', __name__)

@forum_bp.route('/api/save_forum_api_key/', methods=['POST'])
def save_forum_api_key():
    """save a discourse forum key for a user.

    .. :quickref: Social; Associate a discourse forum key to a user

    :reqheader Accept: application/json
    :<json string user_token: User Token
    :<json string discourse_key: discourse_key
    :<json string api_username: api_username

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get('user_token')
    discourse_key = received_form_response.get('discourse_key')
    api_username = received_form_response.get('api_username')
    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message='Invalid User: Unauthorized.'
        )

    # Add the user to the users kind of entity
    key = datastore_client.key('DiscourseKeys')
    # Indexes every other column except the description
    discourse_key_task = datastore.Entity(key, exclude_from_indexes=[])

    discourse_key_task.update({
            'user_uuid': user_uuid,
            'discourse_key': discourse_key,
            'api_username': api_username
        })

    datastore_client.put(discourse_key_task)

    if discourse_key_task.key:
        return success_response(message="The given key now associated with your account.")

    else:
        return error_response(
            message="Sorry something failed. Womp womp!"
        )


@forum_bp.route('/api/get_forum_key_by_uuid/', methods=['GET', 'POST'])
def get_forum_key_by_uuid():
    print("Fetching all the user devices")
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", None)
    if user_token is None:
        print("get_user_devices: No user token in form response")
        return error_response(
            message="Please make sure you have added values for all the fields"
        )
    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message='Invalid User: Unauthorized.'
        )

    query = datastore_client.query(kind='DiscourseKeys')
    query.add_filter('user_uuid', '=', user_uuid)
    query_result = list(query.fetch())
    results = list(query_result)
    if len(results) == 0:
        return error_response(
            message="Sorry something failed. Womp womp!"
        )
    discourse_user = results[0]

    return success_response(
        discourse_key=discourse_user.get('discourse_key'),
        api_username=discourse_user.get('api_username')
    )
