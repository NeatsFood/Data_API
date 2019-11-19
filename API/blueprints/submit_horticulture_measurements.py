import json
from datetime import datetime

from flask import Blueprint, request

from cloud_common.cc.google import datastore
from google.cloud import datastore as gcds
from .utils.auth import get_user_uuid_from_token
from .utils.response import (success_response, error_response)


submit_horticulture_measurements_bp = Blueprint('submit_horticulture_measurements', __name__)

@submit_horticulture_measurements_bp.route('/api/submit_horticulture_measurements/', methods=['POST'])
def submit_horticulture_measurements():
    """Save horticulture measurements from a device.

    .. :quickref: Horticulture; Save horticulture measurements

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: Device UUID in which plant was measured
    :<json string leaves_count: Leaf count
    :<json string plant_height: Plant height in cm

    **Example response**:

        .. sourcecode:: json

          {
            "message": "Measurements saved.",
            "response_code": 200
          }
    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get('user_token')
    device_uuid = received_form_response.get('device_uuid')

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None or device_uuid is None:
        return error_response(
            message='Invalid User: Unauthorized.'
        )

    leaves_count = received_form_response.get("leaves_count")
    plant_height = received_form_response.get("plant_height")
    horticulture_notes = received_form_response.get("horticulture_notes")
    if leaves_count == None and plant_height == None and horticulture_notes == None:
        return error_response()

    # Add the user to the users kind of entity
    key = datastore.get_client().key('HorticultureMeasurements')

    # Indexes every other column except the description
    horitculture_reg_task = gcds.Entity(key, exclude_from_indexes=[])

    horitculture_reg_task.update({
        'device_uuid': device_uuid,
        'measurement': json.dumps({
            "leaves_count":leaves_count,
            "plant_height":plant_height,
            "horticulture_notes":horticulture_notes,
        }),
        "modified_at":datetime.now()
    })

    datastore.get_client().put(horitculture_reg_task)

    return success_response(
        message="Measurements saved."
    )


