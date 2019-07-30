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
    """Return the recipe. Used to build an editor to modify this recipe.  

    .. :quickref: Recipe; Recipe details 

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string recipe_uuid: Recipe UUID to look up

    **Example response**:

        .. sourcecode:: json

            "recipe": "recipe JSON string",
            "devices": "user devices",
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

    devices = get_devices_for_user(user_uuid)

    # Get queried recipe
    recipes_query = datastore.get_client().query(kind='Recipes')
    recipes_query.add_filter("recipe_uuid","=",recipe_uuid)
    recipes_query_results = list(recipes_query.fetch())
    if 0 < len(recipes_query_results):
        return success_response(
            recipe = recipes_query_results[0]["recipe"],
            devices = devices 
        )

    return error_response(
        message="No recipe with that UUID"
    )
