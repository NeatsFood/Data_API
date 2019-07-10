import json
import time
from flask import Blueprint, request

from cloud_common.cc.google import datastore
from cloud_common.cc.google import storage
from .utils.response import success_response, error_response
from .utils.auth import get_user_uuid_from_token


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
def is_allowed(filename):
    if not '.' in filename:
        return False
    else:
        extension = filename.rsplit('.', 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS

upload_images_bp = Blueprint('upload_images_bp', __name__)

GOOGLE_CLOUD_STORAGE_BUCKETS = {
    'user': 'openag-user-images',
    'recipe': 'openag-recipe-images'
}
@upload_images_bp.route('/api/upload_images/', methods=['POST'])
def upload_images():
    """Upload an image for use in the user profile and recipe.

    .. :quickref: Utility; Upload an image

    :reqheader Accept: multipart/form-data
    :<json string file: Form posted base64 encoded binary file
    :<json string type: 'user' or 'recipe'
    :<json string user_token: User Token returned from the /login API.

    **Example response**:

        .. sourcecode:: json

          {
            "url": "public URL of the uploaded image",
            "message": "done",
            "response_code": 200
          }
    """
    image = request.files.get('file')
    if not image:
        return error_response(
            message='No file uploaded.'
        )

    if not is_allowed(image.filename):
        return error_response(
            message='File type not allowed.'
        )

    upload_type = request.form.get('type')
    if upload_type not in GOOGLE_CLOUD_STORAGE_BUCKETS:
        return error_response(
            message="Type must be one of {}"
                .format(list(GOOGLE_CLOUD_STORAGE_BUCKETS.keys()))
        )

    user_token = request.form.get('user_token')
    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message='Invalid User: Unauthorized'
        )

    bucket = GOOGLE_CLOUD_STORAGE_BUCKETS[upload_type]
    filename = "{}-{}".format(user_uuid, str(int(time.time())))
    url = upload_file(image.read(), filename, image.content_type, bucket)

    if upload_type == 'user':
        set_profile_picture(user_uuid, url)

    return success_response(
        message='File saved.',
        url=url
    )

def upload_file(file_stream, filename, content_type, bucket):
    bucket = storage.storage_client.bucket(bucket)
    blob = bucket.blob(filename)
    blob.upload_from_string(file_stream, content_type=content_type)
    blob.make_public()
    return blob.public_url

def set_profile_picture(user_uuid, picture_url):
    query = datastore.get_client().query(kind='Users')
    query.add_filter('user_uuid', '=', user_uuid)
    user = list(query.fetch(1))[0]

    user['profile_image'] = picture_url
    datastore.get_client().put(user)



