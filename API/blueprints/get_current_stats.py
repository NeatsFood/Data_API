import json

from flask import Blueprint
from flask import Response
from flask import request

from cloud_common.cc.google import env_vars
from cloud_common.cc.google import datastore
#debugrob:
#
#from .utils.env_variables import *
#from .utils.response import success_response, error_response
#from .utils.database import get_current_CO2_value, get_current_temp_value, get_current_RH_value, get_current_top_h2o_temp_value, get_current_middle_h2o_temp_value, get_current_bottom_h2o_temp_value

get_current_stats_bp = Blueprint('get_current_stats_bp',__name__)

#------------------------------------------------------------------------------
@get_current_stats_bp.route('/api/get_current_stats/', methods=['GET', 'POST'])
def get_current_stats():
    """Get current device status
    .. :quickref: Sensor Data; Get the current sensor readings

    :<json string selected_device_uuid: UUID of device

    **Example Response**:

        .. sourcecode:: json

          {
            "results": {
                "current_co2": 23,
                "current_temp": 27,
                "current_rh": 15,
                "top_h2o_temp": 26,
                "middle_h2o_temp": 26,
                "bottom_h2o_temp": 26
                },
            "response_code": 200
          }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    device_uuid = received_form_response.get("selected_device_uuid", None)

    if device_uuid is None:
        device_uuid = 'None'

    result_json = {}
    result_json["current_co2"] = get_current_CO2_value( device_uuid )
    result_json["current_temp"] = get_current_temp_value( device_uuid )
    result_json["current_rh"] = get_current_RH_value( device_uuid )
    result_json["top_h2o_temp"] = get_current_top_h2o_temp_value( device_uuid )
    result_json["middle_h2o_temp"] = get_current_middle_h2o_temp_value( device_uuid )
    result_json["bottom_h2o_temp"] = get_current_bottom_h2o_temp_value( device_uuid )

    return success_response(
        results=result_json
    )


