import json
from flask import Blueprint
from flask import request

from cloud_common.cc.runs.runs_data import RunsData
from .utils.response import success_response, error_response
from .utils.auth import get_user_uuid_from_token


get_runs_bp = Blueprint('get_runs', __name__)


@get_runs_bp.route('/api/get_runs/', methods=['POST'])
def get_runs():
    """Retrieve all recipe start, end times for a device.

    .. :quickref: Recipe; Get all recipe run times 

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: Device UUID to get the runs from.

    **Example response**:

        .. sourcecode:: json

          {
              "runs": [
                  {"recipe_name":"Demo Rainbow",
                   "start":"2019-08-09T16:52:46Z",
                   "end":"2019-08-09T16:53:29Z"}
              ],
              "response-code": 200
          }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", None)
    device_uuid = received_form_response.get("device_uuid", None)
    if device_uuid is None or user_token is None:
        return error_response(
            message="Access denied."
        )

    rd = RunsData()
    runs = rd.get_runs(device_uuid)

    return success_response(
        runs=runs
    )
