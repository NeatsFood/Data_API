import json
from flask import Blueprint
from flask import request

from cloud_common.cc.google import datastore
from .utils.auth import get_user_uuid_from_token
from .utils.response import success_response, error_response
from .get_user_devices import get_devices_for_user


get_recipe_by_uuid_bp = Blueprint('get_recipe_by_uuid_bp', __name__)

@get_recipe_by_uuid_bp.route('/api/get_recipe_by_uuid/', methods=['POST'])
def get_recipe_by_uuid():
    """Return all the details about this recipe and a users devices.  Used to build an editor to modify this recipe.  Not currently used.

    .. :quickref: Recipe; Recipe details 

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string recipe_uuid: Recipe UUID to look up

    **Example response**:

        .. sourcecode:: json

          {
            "lots and lots of data": "not described until we implement the new recipe editor",
            "response_code": 200
          }
    """
    received_form_response = request.get_json()
    user_token = received_form_response.get("user_token")
    recipe_uuid = received_form_response.get("recipe_uuid")
    if user_token is None or recipe_uuid is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    # Get all user devices
    devices = get_devices_for_user(user_uuid)

    # Get queried recipe
    recipes_query = datastore.get_client().query(kind='Recipes')
    recipes_query.add_filter("recipe_uuid","=",recipe_uuid)
    recipes_query_results = list(recipes_query.fetch())
    results_array = []
    for recipe in recipes_query_results:
        recipe_details_json = json.loads(recipe["recipe"])
        device_type = recipe['device_type']

        # Get Peripherals needed for this device type
        peripherals = []
        device_type_query = datastore.get_client().query(kind='DeviceType')
        device_type_results = list(device_type_query.fetch())
        for device_type_result in device_type_results:
            peripherals_string = device_type_result['peripherals']
            peripherals_array = peripherals_string.split(",")
            for peripheral in peripherals_array:

                peripherals_query = datastore.get_client().query(kind='Peripherals')
                peripherals_query.add_filter('uuid', '=', str(peripheral))
                peripheraldetails = list(peripherals_query.fetch())

                if len(peripheraldetails) > 0:
                    peripheral_detail_json = {
                        "name": peripheraldetails[0]["name"],
                        "sensor_name": peripheraldetails[0]["sensor_name"],
                        "type": peripheraldetails[0]["type"],
                        "color": "#" + peripheraldetails[0]["color"],
                        "inputs": peripheraldetails[0]["inputs"]
                    }
                    peripherals.append(peripheral_detail_json)

        recipe_json = {
            'name':recipe_details_json['name'],
            'image_url':recipe['image_url'],
            'description':recipe_details_json['description']['verbose'],
            'device_type':device_type,
            'plant_type':recipe_details_json['cultivars'][0]['name'],
            'peripherals':peripherals,
            'recipe_json':recipe_details_json
        }

        results_array.append(recipe_json)

    return success_response(
        results=results_array,
        devices=devices
    )
