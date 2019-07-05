import json
from flask import Blueprint
from flask import request

from cloud_common.cc.google import env_vars
from cloud_common.cc.google import datastore
from cloud_common.cc.notifications.notification_data import NotificationData
from .utils.response import success_response, error_response


ack_device_notification_bp = Blueprint('ack_device_notification_bp',__name__)

#------------------------------------------------------------------------------
@ack_device_notification_bp.route('/api/ack_device_notification/', methods=['GET', 'POST'])
def ack_device_notification():
    """ACK a device notification

    .. :quickref: Device; Get current device notifications

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    device_uuid = received_form_response.get("device_uuid", None)
    ID = received_form_response.get("ID", None)
    if device_uuid is None or ID is None:
        return error_response()
    nd = NotificationData()
    nd.ack(device_uuid, ID)
    return success_response()

