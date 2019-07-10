import json
from flask import Blueprint
from flask import request

from cloud_common.cc.google import env_vars
from cloud_common.cc.google import datastore
from cloud_common.cc.notifications.notification_data import NotificationData
from .utils.response import success_response, error_response


get_device_notifications_bp = Blueprint('get_device_notifications_bp',__name__)

#------------------------------------------------------------------------------
@get_device_notifications_bp.route('/api/get_device_notifications/', methods=['POST'])
def get_current_device_status():
    """Get the list un-acknowledged notifications for this device.

    .. :quickref: Device; Device notifications

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: UUID of device to apply recipe to

    **Example response**:

        .. sourcecode:: json

          {
            "results": {
                "notifications": [
                        {
                            "ID": "UUID",
                            "type": "Done",
                            "message": "Time to water your plant.",
                            "created": "date created",
                            "acknowledged": "date ackd",
                            "URL": "URL to video notification",
                        },
                    ]
                }
            "response_code": 200 
          }
    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token")
    device_uuid = received_form_response.get("device_uuid", None)
    if user_token is None or device_uuid is None:
        return error_response(
            message="Access denied."
        )

    nd = NotificationData()
    notifications = nd.get_unacknowledged(device_uuid)

    result_json = {
        "notifications": notifications
    }
    return success_response(
        results=result_json
    )

