import json
import ast
from flask import Blueprint
from flask import request

from cloud_common.cc.google import datastore
from .utils.auth import get_user_uuid_from_token
from .utils.response import success_response, error_response


get_current_recipe_bp = Blueprint('get_current_recipe', __name__)

@get_current_recipe_bp.route('/api/get_current_recipe/', methods=['POST'])
def get_current_recipe():
    """Get current recipe running on device.

        .. :quickref: Recipe; Get current recipe

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string selected_device_uuid: UUID of device

    **Example Response**:

      .. sourcecode:: json

          {"results": {
            "format": "openag-phased-environment-v1",
            "version": "0.1.2",
            "creation_timestamp_utc":
            "2018-07-19T16:54:24:44Z",
            "name": "Get Growing - Basil Recipe",
            "uuid": "e6085be7-d496-43cc-8bd3-3a40a79e854e",
            "parent_recipe_uuid": "37dc0177-076a-4903-8557-c7586e42e90e",
            "support_recipe_uuids": null,
            "description": {
                "brief": "Grows basil.",
                "verbose": "Grows basil."
            },
            "authors": [{"name": "OpenAgTest", "uuid": "1e91ef7d-e9c2-4b0d-8904-f262a9eda70d", "email": "rp492@cornell.edu"}],
            "cultivars": [{"name": "Basil/Sweet Basil", "uuid": "02b0328f-ff19-44a8-a8b8-cd13cf6b80af"}],
            "cultivation_methods": [{"name": "Shallow Water Culture", "uuid": "45fa509b-2008-4109-a39e-e5682c421925"}],
            "environments": {"standard_day": {
                                "name": "Standard Day",
                                "spectrum_key": "flat",
                                "light_spectrum_nm_percent": {"380-399": 2.03, "400-499": 20.3, "500-599": 23.27, "600-700": 31.09, "701-780": 23.31},
                                "light_ppfd_umol_m2_s": 300,
                                "light_illumination_distance_cm": 10,
                                "air_temperature_celcius": 22
                            },
                            "standard_night": {
                                "name": "Standard Night",
                                "spectrum_key": "off",
                                "light_spectrum_nm_percent": {"380-399": 0.0, "400-499": 0.0, "500-599": 0.0, "600-700": 0.0, "701-780": 0.0},
                                "light_ppfd_umol_m2_s": 0,
                                "light_illumination_distance_cm": 10,
                                "air_temperature_celcius": 22
                            },
                            "cold_day": {"name": "Cold Day", "spectrum_key": "flat", "light_spectrum_nm_percent": {"380-399": 0.0, "400-499": 28.01, "500-599": 26.9, "600-700": 41.13, "701-780": 3.96}, "light_ppfd_umol_m2_s": 300, "light_illumination_distance_cm": 10, "air_temperature_celcius": 10},
                            "frost_night": {"name": "Frost Night", "spectrum_key": "off", "light_spectrum_nm_percent": {"380-399": 0.0, "400-499": 0.0, "500-599": 0.0, "600-700": 0.0, "701-780": 0.0}, "light_ppfd_umol_m2_s": 0, "light_illumination_distance_cm": 10, "air_temperature_celcius": 2}
                        },
                        "phases": [{"name": "Standard Growth",
                                    "repeat": 29,
                                    "cycles": [{"name": "Day", "environment": "standard_day", "duration_hours": 18},
                                                {"name": "Night", "environment": "standard_night", "duration_hours": 6}]
                                    },
                                    {"name": "Frosty Growth",
                                    "repeat": 1,
                                    "cycles": [{"name": "Day", "environment": "cold_day", "duration_hours": 18},
                                                {"name": "Night", "environment": "frost_night", "duration_hours": 6}]
                                    }]
                        },
          "response_code": 200}

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token")
    device_uuid = received_form_response.get("selected_device_uuid", None)
    if user_token is None or device_uuid is None:
        return error_response(
            message="Access denied."
        )

    # TODO: should get this from the new DeviceData.runs list.
    query = datastore.get_client().query(kind='DeviceHistory',
                                   order=['-date_applied'])
    query.add_filter('device_uuid', '=', device_uuid)
    query_result = list(query.fetch(1))
    if not query_result:
        return error_response(
            message='No recipe running on your device.'
        )

    recipe_state = {}
    if len(query_result) > 0:
        recipe_state = ast.literal_eval(query_result[0]['recipe_state'])

    return success_response(
        results=recipe_state
    )
