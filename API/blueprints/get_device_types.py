from flask import Blueprint

from cloud_common.cc.google import datastore
from .utils.response import success_response


get_device_types_bp = Blueprint('get_device_types_bp', __name__)

@get_device_types_bp.route('/api/get_device_types/', methods=['GET', 'POST'])
def get_device_types():
    """Get a JSON list of device types

    .. :quickref: Utility; Get a list of device types

    **Example Response**:

      .. sourcecode:: json

        {
          "results": [{
              "name": "EDU",
              "device_type_id": "SOME UUID?",
              "peripherals": ["UUID?", "UUID?", "UUID?"]
            }],
          "response_code": 200
        }

    """
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
