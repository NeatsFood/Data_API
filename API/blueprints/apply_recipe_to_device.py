from flask import Blueprint
from flask import request
from google.cloud import datastore
import ast
from .utils.auth import get_user_uuid_from_token
from .utils.env_variables import *
from .utils.response import success_response, error_response
import uuid
from datetime import datetime, timedelta

apply_recipe_to_device_bp = Blueprint('apply_recipe_to_device', __name__)


# ------------------------------------------------------------------------------
# Handle Change to a recipe running on a device
@apply_recipe_to_device_bp.route('/api/apply_recipe_to_device/', methods=['GET', 'POST'])
def apply_recipe_to_device():
    """Runs a recipe on a device - possibly deprecated

    .. warning::
        Possible deprecated

    .. :quickref: Recipe; Apply a recipe to a device by UUID - DEPRECATED?

    :reqheader Accept: application/json
    :<json string user_token: User Token
    :<json string device_uuid: UUID of device to apply recipe to
    :<json string recipe_uuid: UUID of recipe to run
    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", "")
    device_uuid = received_form_response.get("device_uuid", "")
    recipe_uuid = received_form_response.get("recipe_uuid", "")
    recipe_dict = {}
    # Get user uuid associated with this sesssion token
    user_uuid = get_user_uuid_from_token(user_token)  # Add the user to the users kind of entity

    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    if device_uuid is None or recipe_uuid is None or user_token is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    # handle device SW version to recipe version here. can be None
    version = ''  # default of no version for older brains
    sw_ver = get_device_software_version(device_uuid)
    if sw_ver is not None and len(sw_ver) > 0:
        version = f'_v{sw_ver}'  # appended to recipe json property name

    #Get Recipe json
    recipe_details_query = datastore_client.query(kind='Recipes')
    recipe_details_query.add_filter('recipe_uuid','=',recipe_uuid)
    recipe_results = list(recipe_details_query.fetch())
    if len(recipe_results) > 0:
        # base recipe (unversioned or for all clients)
        recipe_dict = json.loads(recipe_results[0]['recipe'])

        # see if there is a client version specific json property
        recipe_property = f'recipe{version}'
        versioned_recipe_str = recipe_results[0].get(recipe_property, None)
        if versioned_recipe_str is not None:
            recipe_dict = json.loads(versioned_recipe_str)
    else:
        return error_response(
            message="This recipe can't be applied"
        )


    #TODO: Check the recipe format matches this device type

    key = datastore_client.key('DeviceHistory')
    # Indexes every other column except the description
    apply_to_device_task = datastore.Entity(key, exclude_from_indexes=['recipe_state'])
    date_applied = datetime.now()
    recipe_session_token = str(uuid.uuid4())
    apply_to_device_task.update({
        'recipe_session_token': recipe_session_token,
        # Used to track the recipe applied to the device and modifications made to it.
        'device_uuid': device_uuid,
        'recipe_uuid': recipe_uuid,
        'date_applied': date_applied,
        'date_expires': date_applied + timedelta(days=3000),
        'user_uuid': user_uuid,
        "recipe_state": str(recipe_dict)
    })


    datastore_client.put(apply_to_device_task)

    # convert the values in the dict into what the Jbrain expects
    commands_list = convert_UI_recipe_to_commands(recipe_uuid, recipe_dict)
    send_recipe_to_device_via_IoT(iot_client, device_uuid, commands_list)

    return success_response(
        message="Successfully applied"
    )
