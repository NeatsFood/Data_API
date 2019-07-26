import ast
import uuid
import json
from datetime import datetime, timedelta
from flask import Blueprint
from flask import request

from google.cloud import datastore as gcds
from cloud_common.cc.google import datastore
from .utils.auth import get_user_uuid_from_token
from .utils.response import success_response, error_response


#------------------------------------------------------------------------------
# Save a recipe.
submit_recipe_bp = Blueprint('submit_recipe', __name__)
@submit_recipe_bp.route('/api/submit_recipe/', methods=['POST'])
def submit_recipe():
    """Save a recipe created or modified in the editor.

    .. :quickref: Recipe; Save recipe

    :reqheader Accept: application/json
    :<json string user_token: User's Token.
    :<json string recipe: JSON recipe.

    **Example response**:

        .. sourcecode:: json

          {
            "message": "success",
            "response_code": 200
          }
    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", "")
    recipe_json = received_form_response.get("recipe")
    testing = received_form_response.get("testing")

    if user_token is None or recipe_json is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    # Get user uuid associated with this sesssion token
    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    # if pytest is calling this, don't actually save a recipe
    if testing:
        return success_response(message="test worked")

    # Make sure this recipe has a UUID, it could be null meaning a new recipe.
    recipe_dict = json.loads(recipe_json)       # json > dict
    if recipe_dict.get('uuid') is None:         # if no uuid, make one
        recipe_dict["uuid"] = str(uuid.uuid4())
    recipe_json = json.dumps(recipe_dict)       # dict > json

    key = datastore.get_client().key('Recipes')
    recipe_reg_task = gcds.Entity(key, exclude_from_indexes=["recipe"])

    recipe_reg_task.update({
        "recipe_uuid": recipe_dict.get("uuid"),
        "user_uuid": user_uuid,
        "recipe": recipe_json,
        "date_created": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S:%f')[:-4] + 'Z',
        "device_type": "PFC_EDU",
        "format": recipe_dict.get("format"),
        "version": recipe_dict.get("version")
    })
    datastore.get_client().put(recipe_reg_task)

    # TODO: remove this when the rest of the EDU UI doesn't use DeviceHistory for running recipe state.   It should be using DeviceData.runs
    key = datastore.get_client().key('DeviceHistory')
    apply_to_device_task = gcds.Entity(key, exclude_from_indexes=[])

    date_applied = datetime.now()
    apply_to_device_task.update({
        # Used to track the recipe applied to the device and modifications made to it.
        'recipe_uuid': recipe_dict.get("uuid"),
        'date_applied': date_applied,
        'date_expires': date_applied + timedelta(days=3000),
        'user_uuid': user_uuid
    })
    datastore.get_client().put(apply_to_device_task)

    return success_response(
        message="Successfully saved."
    )
