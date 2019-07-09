import uuid
import json
from datetime import timedelta, datetime
from flask import Blueprint
from flask import Response
from flask import request

from google.cloud import datastore as gcds
from cloud_common.cc.google import datastore
from cloud_common.cc.google import iot
from .utils.response import success_response, error_response
from .utils.auth import get_user_uuid_from_token
from .utils.common import convert_UI_recipe_to_commands


apply_to_device_bp = Blueprint('apply_to_device_bp',__name__)

# ------------------------------------------------------------------------------
# Send a recipe to a device, and save the recipe state.
@apply_to_device_bp.route('/api/apply_to_device/', methods=['GET', 'POST'])
def apply_to_device():
    """Runs a recipe on a device.

    .. :quickref: Recipe; Apply a recipe to a device by UUID

    :reqheader Accept: application/json
    :<json string user_token: User Token
    :<json string device_uuid: UUID of device to apply recipe to
    :<json string recipe_uuid: UUID of recipe to run
    """
    try:
        received_form_response = json.loads(request.data.decode('utf-8'))

        device_uuid = received_form_response.get("device_uuid", None)
        recipe_uuid = received_form_response.get("recipe_uuid", None)
        user_token = received_form_response.get("user_token", None)

        # Using the session token get the user_uuid associated with it
        user_uuid = get_user_uuid_from_token(user_token)
        if user_uuid is None or device_uuid is None or recipe_uuid is None:
            return error_response(message="Missing fields")

        # handle device SW version to recipe version here. can be None
        version = ''  # default of no version for older brains
        sw_ver = datastore.get_device_software_version(device_uuid)
        if sw_ver is not None and len(sw_ver) > 0:
            version = f'_v{sw_ver}'  # appended to recipe json property name

        recipe_dict = {}
        query = datastore.get_client().query(kind='Recipes')
        query.add_filter("recipe_uuid", "=", recipe_uuid)
        results = list(query.fetch())
        if len(results) > 0:
            # base recipe (unversioned or for all clients)
            recipe_dict = json.loads(results[0]['recipe'])

            # see if there is a client version specific json property
            recipe_property = f'recipe{version}'
            versioned_recipe_str = results[0].get(recipe_property, None)
            if versioned_recipe_str is not None:
                recipe_dict = json.loads(versioned_recipe_str)
        else:
            return error_response(message="Nope!")

        # send the recipe to the device
        commands_list = convert_UI_recipe_to_commands(recipe_uuid, recipe_dict)
        iot.send_recipe_to_device_via_IoT(device_uuid, commands_list)

        # TODO: should get this from the new DeviceData.runs list.

        # Save the current state of the recipe that was started.
        key = datastore.get_client().key('DeviceHistory')
        apply_to_device_task = gcds.Entity(key, 
                exclude_from_indexes=['recipe_state'])
        recipe_session_token = str(uuid.uuid4())
        date_applied = datetime.now()
        apply_to_device_task.update({
            'recipe_session_token': recipe_session_token,
            'device_uuid': device_uuid,
            'recipe_uuid': recipe_uuid,
            'date_applied': date_applied,
            'date_expires': date_applied + timedelta(days=100),
            'user_uuid': user_uuid,
            'recipe_state':str(recipe_dict)
        })
        datastore.get_client().put(apply_to_device_task)

        return success_response()
    except(Exception) as e:
        print(f'Error in apply_to_device {e}')
        return error_response(message='Fail')



