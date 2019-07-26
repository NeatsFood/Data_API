import json
from flask import Blueprint
from flask import request

from cloud_common.cc.google import datastore
from .utils.response import success_response, error_response
from .utils.auth import get_user_uuid_from_token


get_all_recipes_bp = Blueprint('get_all_recipes', __name__)


@get_all_recipes_bp.route('/api/get_all_recipes/', methods=['POST'])
def get_all_recipes():
    """Retrieve all recipes for a user account.

    .. :quickref: Recipe; Get all recipes 

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.

    **Example response**:

        .. sourcecode:: json

          {
              "results": ["recipe", "recipe"],
              "devices": ["device", "device"],
              "user_uuid": "UUID-For-User",
              "response-code": 200
          }

    **Example Recipe**:

        .. sourcecode:: json

          {
            "name": "Get Growing - Basil Recipe",
            "description": "Grows basil.",
            "recipe_uuid": "e6085be7-d496-43cc-8bd3-3a40a79e854e",
            "recipe_json": {"Recipe in": "JSON format"},
            "user_uuid": "1e91ef7d-e9c2-4b0d-8904-f262a9eda70d",
            "image_url": "http://via.placeholder.com/200x200",
            "saved": true
          }

    **Example Device**:

        .. sourcecode:: json

          {
            "device_name": "Green-Frog-Bates",
            "device_notes": "",
            "device_reg_no": "F3D9051D",
            "device_type": "EDU",
            "device_uuid": "EDU-F3D9051D-b8-27-eb-0a-43-ee",
            "registration_date": "2019-04-08 13:18:58",
            "user_uuid": "d2c7fe68-e857-4c4a-98b4-7e88154ddaa6"
          }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", None)
    if user_token is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    #Get all user devices
    query = datastore.get_client().query(kind='Devices')
    query.add_filter('user_uuid', '=', user_uuid)
    query_result = list(query.fetch())
    results = list(query_result)
    devices_array = []
    if len(results) > 0:
        for result_row in results:
            device_id = result_row.get("device_uuid", "")
            device_reg_no = result_row.get("device_reg_no", "")
            device_name = result_row.get("device_name", "")
            print('  {}, {}, {}'.format(
                device_id, device_reg_no, device_name))
            result_json = {
                'device_uuid': device_id,
                'device_notes': result_row.get("device_notes", ""),
                'device_type': result_row.get("device_type", ""),
                'device_reg_no': device_reg_no,
                'registration_date': result_row.get("registration_date", "").strftime("%Y-%m-%d %H:%M:%S"),
                'user_uuid': result_row.get("user_uuid", ""),
                'device_name': device_name
            }
            devices_array.append(result_json)


    recipe_query = datastore.get_client().query(kind='Recipes')
    query_result = list(recipe_query.fetch())
    results = list(query_result)

    user = datastore.get_one_from_DS(
        kind='Users', key='user_uuid', value=user_uuid
    )
    saved_recipes = user.get('saved_recipes', [])

    results_array = []
    for result in results:
        recipe_json = json.loads(result["recipe"])
        results_array.append({
            'name': recipe_json['name'],
            'description': recipe_json['description']['brief'],
            'recipe_uuid': result.get("recipe_uuid", ""),
            "recipe_json": recipe_json,
            "user_uuid": result.get('user_uuid', ""),
            "image_url": result.get("image_url", ""),
            'saved': result.get('recipe_uuid') in saved_recipes
        })

    return success_response(
        results=results_array,
        devices=devices_array,
        user_uuid=user_uuid
    )
