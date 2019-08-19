from cloud_common.cc.google import datastore

# For creating decorator functions
from functools import wraps

# For getting information from Auth0
from six.moves.urllib.request import urlopen
from six.moves.urllib.request import Request
import json
from jose import jwt

from flask import request, g
from openag_cache import cache


# Auth0 Config TODO: MOVE SOMEWHERE ELSE
### Auth0 config
AUTH0_DOMAIN = 'dev-rblr1pjr.auth0.com'
# AUDIENCE is more of an identifier, but eventually should be the actual URL we're using.
API_AUDIENCE = 'https://data_api.openagfoundation.org'
ALGORITHMS = ["RS256"]

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_user_uuid_from_token(user_token):
    """Verifies session and returns user uuid"""

    session = datastore.get_one_from_DS(
        kind="UserSession", key="session_token", value=user_token
    )
    if not session:
        return None

    uuid = session.get("user_uuid")
    return uuid


@cache.cached(key_prefix='get_user_info_auth0')
def get_user_info_auth0(token):
    url = "https://"+AUTH0_DOMAIN+"/userinfo"
    headers = {'Authorization': 'Bearer ' + token}
    req = Request(url, headers=headers)
    response = urlopen(req)
    ui = json.loads(response.read())
    return ui


def get_token_auth_header():
    """Obtains the access token from the authorization header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code":"authorization_header_missing",
                         "description":"Authorization header is expected"},
                        401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code":"invalid_header",
                         "description": "Authorization header must start with Bearer"},
                        401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)

    token = parts[1]
    return token

# TODO: Make all the APIs use this
def requires_auth0_auth(f):
    """Decorator to require authentication
    Currently using old user_token version"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        #TODO: Cache the jwks, since it shouldn't change very much
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expied"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code":"invalid_claims",
                                 "description": "incorrect claims, please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                     "Unable to parse authentication"
                                     " token."}, 401)

            g.user_info = get_user_info_auth0(token)
            # user_token = get_user_token_from_auth0_info(user_info)
            g.current_user = payload

            return f(*args, **kwargs)
        raise AuthError({"code":"invalid_header",
                         "description":"Unable to find appropriate key"}, 401)
    return decorated


# TODO: Remove this-- as I don't think we'll ever move the old auth over to using a decorator
def requires_auth(f):
    """Decorator to require authentication
    Currently using old user_token version"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        received_form_response = request.get_json()
        user_token = received_form_response.get("user_token")
        if user_token is None:
            raise AuthError("Please Make Sure You have added values for all the fields", 401)

        user_uuid = get_user_uuid_from_token(user_token)
        if user_uuid is None:
            raise AuthError("Invalid User: Unauthorized")

        g.user_token = user_token
        g.user_uuid = user_uuid