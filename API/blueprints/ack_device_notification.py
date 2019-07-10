import json
from flask import Blueprint
from flask import request

from cloud_common.cc.google import env_vars
from cloud_common.cc.google import datastore
from cloud_common.cc.notifications.notification_data import NotificationData
from .utils.response import success_response, error_response


ack_device_notification_bp = Blueprint('ack_device_notification_bp',__name__)

#------------------------------------------------------------------------------
@ack_device_notification_bp.route('/api/ack_device_notification/', methods=['POST'])
def ack_device_notification():
    """Acknowledge a device notification.

    .. :quickref: Device; ACK a notification

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: UUID of device to apply recipe to
    :<json string ID: Notification ID to acknowledge

    **Example response**:

        .. sourcecode:: json

          {
            "response_code": 200
          }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token")
    device_uuid = received_form_response.get("device_uuid", None)
    ID = received_form_response.get("ID", None)
    if device_uuid is None or ID is None or user_token is None:
        return error_response(
            message="Access denied."
        )
    nd = NotificationData()
    nd.ack(device_uuid, ID)
    return success_response()

