import json
from flask import Blueprint
from flask import Response
from flask import request

from cloud_common.cc.google import datastore
from .utils.response import success_response, error_response


get_device_peripherals_bp = Blueprint('get_device_peripherals_bp',__name__)

@get_device_peripherals_bp.route('/api/get_device_peripherals/',methods=['POST'])
def get_device_peripherals():
    """Get peripherals. Used for recipe editor.

    .. :quickref: Recipe; Get peripherals

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string selected_peripherals: Comma separated list of peripheral UUIDs

    **Example Response**:

      .. sourcecode:: json

        {
          "results":[{
            "name": "Name",
            "sensor_name": "Sensor Name",
            "type": "Sensor Type",
            "color": "#FFAA00",
            "inputs": "inputs"
          }]
        }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token")
    peripherals_string = received_form_response.get("selected_peripherals")
    if user_token is None or peripherals_string is None:
        return error_response(
            message="Access denied."
        )

    peripheral_details = []
    peripherals_array = peripherals_string.split(",")

    for peripheral in peripherals_array:
        if len(peripheral) == 0:
            return error_response()

        query = datastore.get_client().query(kind='Peripherals')
        query.add_filter('uuid', '=', str(peripheral))
        peripheraldetails = list(query.fetch())

        if len(peripheraldetails) == 0:
            return error_response()

        peripheral_detail_json = {
            "name":peripheraldetails[0]["name"],
            "sensor_name":peripheraldetails[0]["sensor_name"],
            "type":peripheraldetails[0]["type"],
            "color":"#"+peripheraldetails[0]["color"],
            "inputs": peripheraldetails[0]["inputs"]
        }
        peripheral_details.append(peripheral_detail_json)

    return success_response(
        results=peripheral_details
    )
