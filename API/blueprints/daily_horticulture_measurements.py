import uuid, json
from datetime import datetime
from flask import Blueprint
from flask import Response
from flask import request

from google.cloud import datastore as gcds
from cloud_common.cc.google import datastore
from .utils.response import success_response, error_response
from .utils.auth import get_user_uuid_from_token


daily_horticulture_measurements_bp = Blueprint('daily_horticulture_measurements_bp', __name__)

@daily_horticulture_measurements_bp.route('/api/daily_horticulture_measurements/', methods=['POST'])
def save_horticulture_measurements():
    """Save horitculture measurements for a device.

    .. :quickref: Horticulture; Save horitculture measurements

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: Device UUID
    :<json string plant_height: plant_height
    :<json string leaf_count: leaf_count
    :<json string leaf_colors: leaf_colors
    :<json string leaf_withering: leaf_withering
    :<json string flavors: flavors
    :<json string root_colors: root_colors
    :<json string horticulture_notes: horticulture_notes
    :<json string submission_name: submission_name

    **Example response**:

        .. sourcecode:: json

          {
            "response_code": 200
          }

    """
    received_form_json = json.loads(request.data.decode('utf-8'))
    user_token = received_form_json.get("user_token")
    device_uuid = received_form_json.get("device_uuid")
    plant_height = received_form_json.get("plant_height", "")
    leaf_count = received_form_json.get("leaf_count", "")
    leaf_colors = received_form_json.get("leaf_colors", "")
    leaf_withering = received_form_json.get("leaf_withering", "")
    flavors = received_form_json.get("flavors", "")
    root_colors = received_form_json.get("root_colors", "")
    horticulture_notes = received_form_json.get("horticulture_notes", "")
    submission_name = received_form_json.get("submission_name", "")
    #print(received_form_json)
    if device_uuid is None:
        return error_response(
            message="Access denied."
        )

    # Add the user to the users kind of entity
    key = datastore.get_client().key('DailyHorticultureLog')
    # Indexes every other column except the description
    horticulture_task = gcds.Entity(key, exclude_from_indexes=[])

    horticulture_task.update({
        "device_uuid": device_uuid,
        "plant_height":str(plant_height),
        "leaf_count": str(leaf_count),
        "leaf_colors": ",".join(x for x in leaf_colors),
        "leaf_withering":  ",".join(x for x in leaf_withering),
        "flavors": ",".join(x for x in flavors),
        "root_colors": ",".join(x for x in root_colors),
        "horticulture_notes": str(horticulture_notes),
        "submission_name": str(submission_name),
        "submitted_at": datetime.now(),
    })

    datastore.get_client().put(horticulture_task)

    if horticulture_task.key:
        return success_response()
    else:
        return error_response()
