import json
from datetime import datetime
from flask import Response
from flask import request
from flask import Blueprint, request

from cloud_common.cc.google import datastore
from .utils.response import success_response, error_response


get_horticulture_daily_logs_bp = Blueprint('get_horticulture_daily_logs_bp',__name__)

#------------------------------------------------------------------------------
@get_horticulture_daily_logs_bp.route('/api/get_horticulture_daily_logs/', methods=['POST'])
def get_horticulture_daily_logs():
    """Get horitculture measurements for a device.

    .. :quickref: Horticulture; Get horitculture measurements

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: Device UUID

    **Example response**:

        .. sourcecode:: json

          {
            "leaf_count_results": [
                    {"value":3,"time":"2019-04-08 13:18:58"},
                    {},
                    {}
                ],
            "plant_height_results": [
                    {"value":2.5,"time":"2019-04-08 13:18:58"},
                    {},
                    {}
                ],
            "response_code": 200
          }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token")
    device_uuid = received_form_response.get("device_uuid")
    if user_token is None or device_uuid is None:
        return error_response(
            message="Access denied."
        )

    query = datastore.get_client().query(kind='DailyHorticultureLog')
    query.add_filter('device_uuid', '=', device_uuid)
    query_result = list(query.fetch())
    if len(query_result) == 0:
        return success_response(
            expired=True
        )
    leaf_count_results = []
    plant_height_results = []
    horticulture_notes_results = []
    for result in query_result:
        leaf_count_results.append({"value":result["leaf_count"],"time":str(result["submitted_at"])})
        plant_height_results.append({"value": result["plant_height"], "time": str(result["submitted_at"])})
        horticulture_notes_results.append({"value": result["horticulture_notes"], "time": str(result["submitted_at"])})
    return success_response(
        leaf_count_results=leaf_count_results,
        plant_height_results=plant_height_results,
        horticulture_notes_results=horticulture_notes_results,
    )
