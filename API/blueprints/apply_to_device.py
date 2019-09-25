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


apply_to_device_bp = Blueprint("apply_to_device_bp", __name__)

# ------------------------------------------------------------------------------
# Send a recipe to a device, and save the recipe state.
@apply_to_device_bp.route("/api/apply_to_device/", methods=["POST"])
def apply_to_device():
    """Run a recipe on a device.

    .. :quickref: Recipe; Run recipe, run

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: UUID of device to apply recipe to
    :<json string recipe_uuid: UUID of recipe to run

    **Example response**:

        .. sourcecode:: json

          {
            "response_code": 200
          }

    """

    # Get request parameters
    request_json = json.loads(request.data.decode("utf-8"))
    device_uuid = request_json.get("device_uuid", None)
    recipe_uuid = request_json.get("recipe_uuid", None)
    user_token = request_json.get("user_token", None)

    # Validate parameters
    if device_uuid is None:
        return Response(json.dumps({"message": "Device UUID is required"}), 400)
    if recipe_uuid is None:
        return Response(json.dumps({"message": "Recipe UUID is required"}), 400)
    if user_token is None:
        return Response(json.dumps({"message": "User token is required"}), 400)

    # Get user from token
    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return Response(json.dumps({"message": "User token is invalid"}), 400)

    # Get recipe entry from datastore
    recipe_dict = {}
    query = datastore.get_client().query(kind="Recipes")
    query.add_filter("recipe_uuid", "=", recipe_uuid)
    results = list(query.fetch())

    # Verify recipe entry exists
    if len(results) < 0:
        return Response(json.dumps({"message": "Recipe uuid is invalid"}), 400)

    # Get recipe versions
    # NOTE: Versioning should not be done like this...
    device_software_version = datastore.get_device_software_version(device_uuid)
    versioned_recipe = results[0].get(f"recipe_v{device_software_version}")
    unversioned_recipe = results[0].get("recipe")

    # Get recipe dict
    if versioned_recipe is not None:
        recipe_dict = json.loads(versioned_recipe)
    else:
        recipe_dict = json.loads(unversioned_recipe)

    # Send recipe to device
    try:
        iot.send_start_recipe_command(device_uuid, recipe_uuid, recipe_dict)
        return Response(json.dumps({"message": "Sent recipe to device"}), 200)
    except iot.SendCommandError as e:
        print(f"Unable to send recipe to device: {e.message}")
        return Response(json.dumps({"message": e.message}), 503)
