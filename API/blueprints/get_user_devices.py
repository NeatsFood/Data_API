import json
from flask import Blueprint
from flask import Response
from flask import request

from cloud_common.cc.google import datastore
from .utils.response import (success_response, error_response, pre_serialize_device)
from .utils.common import is_expired
from .utils.auth import get_user_uuid_from_token


get_user_devices_bp = Blueprint('get_user_devices_bp',__name__)

@get_user_devices_bp.route('/api/get_user_devices/', methods=['POST'])
def get_user_devices():
    """Get all devices associated with a user account.

    .. :quickref: User; Get user's devices

    :reqheader Accept: multipart/form-data
    :<json string user_token: User Token returned from the /login API.

    **Example Response**:

      .. sourcecode:: json

        {
            "results": {
                "devices": [
                    {
                        "device_uuid": "EDU-9F2BEEEF-ac-de-48-00-11-22",
                        "device_notes": "",
                        "device_type": "EDU",
                        "device_reg_no": "9F2BEEEF",
                        "registration_date": "2019-04-29 20:09:10",
                        "user_uuid": "d2c7fe68-e857-4c4a-98b4-7e88154ddaa6",
                        "device_name": "Steve's Mac"
                    },
                    {
                        "device_uuid": "EDU-F3D9051D-b8-27-eb-0a-43-ee",
                        "device_notes": "",
                        "device_type": "EDU",
                        "device_reg_no": "F3D9051D",
                        "registration_date": "2019-04-08 13:18:58",
                        "user_uuid": "d2c7fe68-e857-4c4a-98b4-7e88154ddaa6",
                        "device_name": "Green-Frog-Bates"
                    }],
                "user_uuid": "d2c7fe68-e857-4c4a-98b4-7e88154ddaa6"
            },
            "response_code": 200
        }

    """
    print("Fetching all the user devices")

    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", None)
    if user_token is None:
        print("get_user_devices: No user token in form response")
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        print("get_user_devices: No user uuid")
        return error_response(
            message="Invalid User: Unauthorized"
        )

    devices = get_devices_for_user(user_uuid)

    if not devices:
        print("get_user_devices: No devices for user")
        return error_response(
            message="No devices associated with user."
        )

    response = {
        "devices":devices,
        "user_uuid":user_uuid
    }
    return success_response(
        results=response
    )


def get_devices_for_user(user_uuid):
    query = datastore.get_client().query(kind='Devices')
    query.add_filter('user_uuid', '=', user_uuid)
    query_results = list(query.fetch())

    devices = []
    for device in query_results:
        device_json = pre_serialize_device(device)
        print('    {}, {}, {}'.format(
            device_json['device_uuid'],
            device_json['device_reg_no'],
            device_json['device_name']
        ))
        devices.append(device_json)

    return devices


