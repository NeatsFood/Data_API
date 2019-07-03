from flask import Blueprint
from flask import Response
from flask import request

from cloud_common.cc.google import env_vars
from cloud_common.cc.google import datastore
#debugrob:
#
#from .utils.env_variables import *
#from .utils.response import success_response, error_response
#from .utils.database import get_temp_and_humidity_history

get_temp_details_bp = Blueprint('get_temp_details_bp',__name__)

# ------------------------------------------------------------------------------
@get_temp_details_bp.route('/api/get_temp_details/', methods=['GET', 'POST'])
def get_temp_details():
    """Get historical temperature (and humidity) data.

        .. :quickref: Sensor Data; If there is Temp/RH data in the 'datastore' return that, otherwise get the last 30 days from BigQuery.

        :reqheader Accept: application/json
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
    device_uuid = received_form_response.get("selected_device_uuid", None)

    if device_uuid is None:
        device_uuid = 'None'

    result_json = get_temp_and_humidity_history( device_uuid )

    return success_response(
        results=result_json
    )

