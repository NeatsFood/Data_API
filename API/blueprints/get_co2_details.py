import json
from flask import Blueprint
from flask import Response
from flask import request

from cloud_common.cc.google import datastore
from cloud_common.cc.google.database import get_co2_history
from .utils.response import success_response, error_response


get_co2_details_bp = Blueprint('get_co2_details_bp',__name__)

#------------------------------------------------------------------------------
@get_co2_details_bp.route('/api/get_co2_details/', methods=['POST'])
def get_co2_details():
    """Return a time series of historical co2 data.

    .. :quickref: Sensor Data; CO2 data

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string selected_device_uuid: Device UUID to get the CO2 data for

    **Example response**:

        .. sourcecode:: json

          {
            "results": [
                {"value": "33246.0", "time": "2019-05-08T16:44:39Z"},
                {"value": "33244.0", "time": "2019-05-08T16:39:39Z"}
            ],
            "response_code": 200
          }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token")
    device_uuid = received_form_response.get("selected_device_uuid", None)
    if device_uuid is None or user_token is None:
        return error_response(
            message="Access denied."
        )

    results = get_co2_history( device_uuid )

    return success_response(
        results=results
    )
