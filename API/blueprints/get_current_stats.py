import json

from flask import Blueprint
from flask import Response
from flask import request

from cloud_common.cc.google import database
from .utils.response import success_response, error_response


get_current_stats_bp = Blueprint('get_current_stats_bp',__name__)

#------------------------------------------------------------------------------
@get_current_stats_bp.route('/api/get_current_stats/', methods=['POST'])
def get_current_stats():
    """Get the current sensor readings.

    .. :quickref: Sensor Data; Current readings

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string selected_device_uuid: UUID of device

    **Example Response**:

        .. sourcecode:: json

          {
            "results": {
                "current_co2": "23",
                "current_temp": "27",
                "current_rh": "50.1",
                "current_h20_ec": "4.4",
                "current_h20_ph": "7.1",
                "current_h20_temp": "25.0"
                },
            "response_code": 200
          }

    """
    print("Getting current stats")
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token")
    device_uuid = received_form_response.get("selected_device_uuid", None)
    if user_token is None or device_uuid is None:
        return error_response(
            message="Access denied."
        )

    result_json = {}
    result_json["current_co2"] = database.get_current_CO2_value(device_uuid)
    result_json["current_temp"] = database.get_current_temp_value(device_uuid)
    result_json["current_rh"] = database.get_current_RH_value(device_uuid)
    result_json["current_h20_ec"] = database.get_current_EC_value(device_uuid)
    result_json["current_h20_ph"] = database.get_current_pH_value(device_uuid)
    result_json["current_h20_temp"] = database.get_current_h2o_temp_value(device_uuid)

    return success_response(
        results=result_json
    )


