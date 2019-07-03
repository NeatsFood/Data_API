import uuid
from datetime import timedelta
from flask import Blueprint
from flask import Response
from flask import request

from cloud_common.cc.google import env_vars
from cloud_common.cc.google import datastore
#debugrob: fix
#from google.cloud import datastore
#from .utils.env_variables import *
#from .utils.response import success_response, error_response
#from .utils.auth import get_user_uuid_from_token

apply_to_device_bp = Blueprint('apply_to_device_bp',__name__)

# ------------------------------------------------------------------------------
# Save the device history.
@apply_to_device_bp.route('/api/apply_to_device/', methods=['GET', 'POST'])
def apply_to_device():
    """Runs a recipe on a device.

    .. :quickref: Recipe; Apply a recipe to a device by UUID

    :reqheader Accept: application/json
    :<json string user_token: User Token
    :<json string device_uuid: UUID of device to apply recipe to
    :<json string recipe_uuid: UUID of recipe to run
    """
    received_form_response = json.loads(request.data.decode('utf-8'))

    device_uuid = received_form_response.get("device_uuid", None)
    recipe_uuid = received_form_response.get("recipe_uuid", None)
    user_token = received_form_response.get("user_token", None)
    date_applied = datetime.now()

    # Using the session token get the user_uuid associated with it
    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    # handle device SW version to recipe version here. can be None
    version = ''  # default of no version for older brains
    sw_ver = get_device_software_version(device_uuid)
    if sw_ver is not None and len(sw_ver) > 0:
        version = f'_v{sw_ver}'  # appended to recipe json property name

    recipe_dict = {}
    query = datastore_client.query(kind='Recipes')
    query.add_filter("recipe_uuid", "=", recipe_uuid)
    results = list(query.fetch())
    if len(results) > 0:
        # base recipe (unversioned or for all clients)
        recipe_dict = json.loads(recipe_results[0]['recipe'])

        # see if there is a client version specific json property
        recipe_property = f'recipe{version}'
        versioned_recipe_str = recipe_results[0].get(recipe_property, None)
        if versioned_recipe_str is not None:
            recipe_dict = json.loads(versioned_recipe_str)

    # send the recipe to the device
    commands_list = convert_UI_recipe_to_commands(recipe_uuid, recipe_dict)
    send_recipe_to_device_via_IoT(iot_client, device_uuid, commands_list)

    # Add the user to the users kind of entity
    key = datastore_client.key('DeviceHistory')

    # Indexes every other column except the description
    apply_to_device_task = datastore.Entity(key, exclude_from_indexes=[])

    if device_uuid is None or recipe_uuid is None or user_token is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    recipe_session_token = str(uuid.uuid4())
    apply_to_device_task.update({
        'recipe_session_token': recipe_session_token,
    # Used to track the recipe applied to the device and modifications made to it.
        'device_uuid': device_uuid,
        'recipe_uuid': recipe_uuid,
        'date_applied': date_applied,
        'date_expires': date_applied + timedelta(days=3000),
        'user_uuid': user_uuid,
        'recipe_state':str(recipe_dict)
    })



    datastore_client.put(apply_to_device_task)
    if apply_to_device_task.key:
        return success_response()

    else:
        return error_response(
            message="Sorry something failed. Womp womp!"
        )
