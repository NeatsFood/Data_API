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
    :<json string shared: 'true' if this is a shared recipe.

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
    shared = received_form_response.get("shared", 'false')
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
    current_ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S:%f')[:-4] + 'Z'
    recipe_dict = json.loads(recipe_json)       # json > dict
    is_new = False
    if recipe_dict.get('uuid') is None:         # if no uuid, make one
        is_new = True
        new_uuid = str(uuid.uuid4())
        recipe_dict["uuid"] = new_uuid
        recipe_dict["creation_timestamp_utc"] = current_ts
        if 0 < len(recipe_dict["authors"]):
            recipe_dict["authors"][0]["uuid"] = user_uuid
    recipe_json = json.dumps(recipe_dict)       # dict > json

    # put a new recipe into the collection
    if is_new:
        entity = datastore.get_client().key('Recipes')
        recipe_reg_task = gcds.Entity(entity, exclude_from_indexes=["recipe"])

        recipe_reg_task.update({
            "recipe_uuid": recipe_dict.get("uuid"),
            "user_uuid": user_uuid,
            "recipe": recipe_json,
            "date_created": current_ts,
            "device_type": "PFC_EDU",
            "format": recipe_dict.get("format"),
            "version": recipe_dict.get("version"),
            "shared": shared 
        })
        datastore.get_client().put(recipe_reg_task)
    else: # recipe exists, so update it
        query = datastore.get_client().query(kind='Recipes')
        query.add_filter('recipe_uuid', '=', recipe_dict.get("uuid"))
        recipes = list(query.fetch(1))
        if 0 == len(recipes):
            return error_response(message="No matching recipe in collection")
        recipe = recipes[0]
        recipe["recipe"] = recipe_json
        recipe["date_created"] = current_ts
        recipe["shared"] = shared
        datastore.get_client().put(recipe)

    return success_response(
        message="Successfully saved.",
        modified=current_ts,
        recipe_uuid=recipe_dict.get("uuid")
    )
