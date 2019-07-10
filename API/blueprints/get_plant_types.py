from flask import Blueprint
from flask import request

from cloud_common.cc.google import datastore
from .utils.response import success_response, error_response


get_plant_types_bp = Blueprint('get_plant_types_bp', __name__)


@get_plant_types_bp.route('/api/get_plant_types/', methods=['POST'])
def get_plant_types():
    """Get known plant types.  For the recipe editor.

    .. :quickref: Utility; Plant types 

    **Example Response**:

      .. sourcecode:: json

        {
          "results": [
                        {
                          "name": "Basil",
                          "variants": "Sweet Basil, Purple Basil"
                        },
                        {
                          "name": "Lettuce",
                          "variants": "Iceberg, Butterhead, Rocket, Mizuna, Romaine"
                        }
                    ],
          "response_code": 200
        }

    """
    received_form_response = request.get_json()
    user_token = received_form_response.get("user_token")
    if user_token is None:
        return error_response(
            message="Access denied."
        )

    query = datastore.get_client().query(kind='Plants')
    query_result = list(query.fetch())
    results = list(query_result)

    results_array = []
    for result in results:
        plant_type_json = {
            'name':result['name'],
            'variants':result['variants']
        }
        results_array.append(plant_type_json)

    return success_response(
        results=results_array
    )
