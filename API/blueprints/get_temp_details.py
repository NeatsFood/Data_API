import json
from flask import Blueprint
from flask import Response
from flask import request

from .utils.response import success_response, error_response
from cloud_common.cc.google.database import get_temp_and_humidity_history


get_temp_details_bp = Blueprint('get_temp_details_bp',__name__)

# ------------------------------------------------------------------------------
@get_temp_details_bp.route('/api/get_temp_details/', methods=['POST'])
def get_temp_details():
    """Get historical temperature (and humidity) time series data.

        .. :quickref: Sensor Data; Temp/RH data

        :reqheader Accept: application/json
        :<json string user_token: User Token returned from the /login API.
        :<json string selected_device_uuid: Device UUID to get the Temp/RH data for

        **Example response**:

            .. sourcecode:: json

              {
                "results": {
                    "RH": [
                        {"value": "28.0", "time": "2019-05-08T18:39:53Z"},
                        {"value": "29.0", "time": "2019-05-08T18:29:52Z"}],
                    "temp": [
                        {"value": "25.0", "time": "2019-05-08T18:29:52Z"},
                        {"value": "24.0", "time": "2019-05-08T18:24:52Z"}]
                },
                "response_code": 200
              }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token")
    device_uuid = received_form_response.get("selected_device_uuid", None)
    if user_token is None or device_uuid is None:
        return error_response(
            message="Access denied."
        )

    result_json = get_temp_and_humidity_history(device_uuid)
    return success_response(
        results=result_json
    )

