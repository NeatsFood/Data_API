from flask import Blueprint
from flask import request

from cloud_common.cc.google import datastore
from .utils.response import success_response, error_response


get_device_types_bp = Blueprint('get_device_types_bp', __name__)

@get_device_types_bp.route('/api/get_device_types/', methods=['POST'])
def get_device_types():
    """Get a list of all device types.

    .. :quickref: Utility; Device types

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.

    **Example Response**:

      .. sourcecode:: json

        {
          "results": [{
              "name": "EDU",
              "device_type_id": "Type-UUID",
              "peripherals": ["P1-UUID", "P2-UUID", "P3-UUID"]
            }],
          "response_code": 200
        }

    """
    received_form_response = request.get_json()
    user_token = received_form_response.get("user_token")
    if user_token is None:
        return error_response(
            message="Access denied."
        )

    query = datastore.get_client().query(kind='DeviceType')
    query_result = list(query.fetch())
    results = list(query_result)

    results_array = []
    for result in results:
        device_type_json = {
            'peripherals':result['peripherals'],
            'device_type_id':result['id'],
            'name':result['name']
        }
        results_array.append(device_type_json)

    return success_response(
        results=results_array
    )
