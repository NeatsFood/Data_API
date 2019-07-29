import ast
import uuid
import json
from datetime import datetime, timedelta
from flask import Blueprint
from flask import request

from cloud_common.cc.google import datastore
from .utils.auth import get_user_uuid_from_token
from .utils.response import success_response, error_response


#------------------------------------------------------------------------------
# Delete a recipe.
delete_recipe_bp = Blueprint('delete_recipe', __name__)
@delete_recipe_bp.route('/api/delete_recipe/', methods=['POST'])
def delete_recipe():
    """Delete a users recipe.

    .. :quickref: Recipe; Delete recipe

    :reqheader Accept: application/json
    :<json string user_token: User's Token.
    :<json string recipe_uuid: Recipe UUID.

    **Example response**:

        .. sourcecode:: json

          {
            "message": "success",
            "response_code": 200
          }
    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", "")
    recipe_uuid = received_form_response.get("recipe_uuid")
    testing = received_form_response.get("testing")

    if user_token is None or recipe_uuid is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    # Get user uuid associated with this sesssion token
    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(message="Invalid User: Unauthorized")

    # If pytest is calling this, don't actually save a recipe
    if testing:
        return success_response(message="test worked")

    # Get the recipe
    recipe = datastore.get_one_from_DS('Recipes', 'recipe_uuid', recipe_uuid)
    if recipe is None:
        return error_response(message="Invalid recipe uuid.")

    # Only delete the recipe if it has the users user_uuid
    if recipe.get('user_uuid') != user_uuid:
        return error_response(message="User does not own this recipe.")

    # Delete it.
    datastore.get_client().delete(key=recipe.key)

    return success_response(
        message="Successfully saved."
    )
