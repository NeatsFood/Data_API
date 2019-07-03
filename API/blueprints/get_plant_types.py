from flask import Blueprint

from cloud_common.cc.google import env_vars
from cloud_common.cc.google import datastore
#debugrob:
#
#from .utils.env_variables import *
#from .utils.response import success_response

get_plant_types_bp = Blueprint('get_plant_types_bp', __name__)


@get_plant_types_bp.route('/api/get_plant_types/', methods=['GET', 'POST'])
def get_plant_types():
    """Get plant types in datastore

    .. :quickref: Utility; Get known plant types from datastore

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
    query = datastore_client.query(kind='Plants')
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
