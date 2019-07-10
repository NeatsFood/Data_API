import json
from datetime import datetime, timezone
from flask import Blueprint
from flask import Response
from flask import request

from cloud_common.cc.google import datastore
from .utils.response import success_response, error_response
from .utils.common import is_expired


verify_user_session_bp = Blueprint('verify_user_session_bp',__name__)

@verify_user_session_bp.route('/api/verify_user_session/', methods=['POST'])
def verify_user_session():
    """Verify the user's session token is still valid.
    .. :quickref: Authentication; Verify user's session

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.

    **Example response**:

        .. sourcecode:: json

          {
            "message": "Successful",
            "is_expired": "True",
            "response_code": 200
          }
    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", None)
    query_session = datastore.get_client().query(kind="UserSession")
    query_session.add_filter('session_token', '=', user_token)
    query_session_result = list(query_session.fetch())
    expired = True
    user_uuid = None
    if len(query_session_result) > 0:
        user_uuid = query_session_result[0].get("user_uuid", None)
        session_expiration = query_session_result[0].get("expiration_date")
        if session_expiration is not None:
            expired = is_expired(session_expiration)

    return success_response(
        message="Successful",
        is_expired=expired,
        user_uuid=user_uuid
    )
