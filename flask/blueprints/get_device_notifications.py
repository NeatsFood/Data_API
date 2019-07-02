from flask import Blueprint
from flask import request
from .utils.database import get_device_notifications_from_DS
from .utils.env_variables import *
from .utils.response import success_response, error_response
from datetime import timezone

get_device_notifications_bp = Blueprint('get_device_notifications_bp',__name__)

#------------------------------------------------------------------------------
@get_device_notifications_bp.route('/api/get_device_notifications/', methods=['GET', 'POST'])
def get_current_device_status():
    """Get device notifications

    .. :quickref: Device; Get current device notifications

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    device_uuid = received_form_response.get("device_uuid", None)

    if device_uuid is None:
        return error_response()

    notifications = get_device_notifications_from_DS(device_uuid)

    result_json = {
        "notifications": notifications
    }
    return success_response(
        results=result_json
    )

