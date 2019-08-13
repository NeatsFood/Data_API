import json
from datetime import datetime
from flask import Blueprint
from flask import Response
from flask import request

from googleapiclient import errors
from google.cloud import datastore as gcds

from cloud_common.cc.google import datastore
from cloud_common.cc.google import iot
from .utils.response import success_response, error_response
from .utils.auth import get_user_uuid_from_token


register_bp = Blueprint('register_bp',__name__)

# ------------------------------------------------------------------------------
@register_bp.route('/api/register/', methods=['POST'])
def register():
    """Register a Food Computer and associate it with a user account.

    .. :quickref: Device; Register device

    :reqheader Accept: application/json
    :<json string user_token: User Token, to associate this device with
    :<json string device_name: User specified name for the device ('mine!')
    :<json string device_reg_no: Key from the device registration process
    :<json string device_notes: User specified notes about the device ('blue')
    :<json string device_type: PFC_EDU, FS, etc.

    **Example response**:

        .. sourcecode:: json

          {
            "response_code": 200 
          }
    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    print('register API received_form_response={}'.format(received_form_response))

    user_token = received_form_response.get("user_token", None)
    device_name = received_form_response.get("device_name", None)
    device_reg_no = received_form_response.get("device_reg_no", None)
    device_notes = received_form_response.get("device_notes", None)
    device_type = received_form_response.get("device_type", None)
    testing = received_form_response.get("testing")
    time_stamp = datetime.now()

    if user_token is None or device_reg_no is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    if device_type is None:
        device_type = 'EDU'

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    if testing: # our pytest is hitting this API, so don't create the user
        return success_response()

    # Create a google IoT device registry entry for this device.
    # The method returns the device ID we need for IoT communications.
    try:
        device_uuid, device_software_version = \
                iot.create_iot_device_registry_entry(device_reg_no,
                                                 device_name,
                                                 device_notes,
                                                 device_type,
                                                 user_uuid)
    except ValueError as e:
        return error_response(
            message=str(e)
        )
    except errors.HttpError as e:
        return error_response(
            message=e._get_reason()
        )

    if device_uuid is None:
        return error_response(
            message="Could not register this IoT device."
        )

    # Add the device to the Devices datastore collection
    key = datastore.get_client().key('Devices')
    device_reg_task = gcds.Entity(key, exclude_from_indexes=[])

    device_reg_task.update({
        'device_uuid': device_uuid,
        'device_name': device_name,
        'device_reg_no': device_reg_no,
        'device_notes': device_notes,
        'user_uuid': user_uuid,
        'device_type': device_type,
        'registration_date': time_stamp,
        'device_software_version': device_software_version
    })

    datastore.get_client().put(device_reg_task)

    if device_reg_task.key:
        return success_response()

    else:
        return error_response(
            message="Sorry there was an error."
        )
