import json
from flask import Blueprint, request, Response, stream_with_context
from .utils.auth import requires_auth
from cloud_common.cc.google import datastore
from .utils.response import (success_response, error_response, pre_serialize_device)
from .utils.common import is_expired
from .utils.auth import get_user_uuid_from_token
from cloud_common.cc import utils
from datetime import datetime
import time


get_user_cluster_bp = Blueprint('get_user_cluster_bp',__name__)


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds


def decode_url(image_entity):
    url = image_entity['URL']

    # In case the url is stored as a blob (represented in python by a
    # bytes object), decode it into a string.
    try:
        url = url.decode('utf-8')
    except AttributeError:
        pass

    return url

@get_user_cluster_bp.route('/api/get_user_cluster/', methods=['POST'])
def get_user_cluster():
    """Get all devices associated with a user account.

    .. :quickref: User; Get user's devices

    :reqheader Accept: multipart/form-data
    :<json string user_token: User Token returned from the /login API.

    **Example Response**:

      .. sourcecode:: json

        {
            "results": {
                "devices": [
                    {
                        "device_uuid": "EDU-9F2BEEEF-ac-de-48-00-11-22",
                        "device_notes": "",
                        "device_type": "EDU",
                        "device_reg_no": "9F2BEEEF",
                        "registration_date": "2019-04-29 20:09:10",
                        "user_uuid": "d2c7fe68-e857-4c4a-98b4-7e88154ddaa6",
                        "device_name": "Steve's Mac"
                    },
                    {
                        "device_uuid": "EDU-F3D9051D-b8-27-eb-0a-43-ee",
                        "device_notes": "",
                        "device_type": "EDU",
                        "device_reg_no": "F3D9051D",
                        "registration_date": "2019-04-08 13:18:58",
                        "user_uuid": "d2c7fe68-e857-4c4a-98b4-7e88154ddaa6",
                        "device_name": "Green-Frog-Bates"
                    }],
                "user_uuid": "d2c7fe68-e857-4c4a-98b4-7e88154ddaa6"
            },
            "response_code": 200
        }

    """
    print("Fetching all the users cluster")

    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", None)
    if user_token is None:
        print("get_user_devices: No user token in form response")
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        print("get_user_devices: No user uuid")
        return error_response(
            message="Invalid User: Unauthorized"
        )

    devices = get_cluster_devices_for_user(user_uuid)

    if not devices:
        print("get_user_devices: No devices for user")
        return error_response(
            message="No devices associated with user."
        )

    response = {
        "devices":devices,
        "user_uuid":user_uuid
    }
    return success_response(
        results=response
    )


def get_cluster_devices_for_user(user_uuid):
    # full_start_time = time.time()
    print("get_cluster: fetching devices")
    query = datastore.get_client().query(kind='Devices')
    query.add_filter('user_uuid', '=', user_uuid)
    query_results = list(query.fetch())

    # print("\t done {}".format(time.time() - full_start_time))

    devices = []

    print("get_cluster: feching device statuses")
    count_devs = len(query_results)
    i = 0
    for device in query_results:
        # dev_start_time = time.time()
        i += 1
        print("get_cluster: fetching {} of {}".format(i, count_devs))
        device_json = pre_serialize_device(device)
        device_id = device_json['device_uuid']  # Just for ease
        if device_id != "":
            # print("\t getting run info for device: {}".format(device_id))
            device_json["current_recipe"] = None
            device_json["recipe_start_date"] = None

            # get recipe info if running
            recipe_runs = datastore.get_device_data(datastore.DS_runs_KEY, device_id, count=1)
            if recipe_runs is not None \
                and len(recipe_runs) > 0 \
                and recipe_runs[0].get("end",None) is None:
                device_json["current_recipe"] = recipe_runs[0].get("recipe_name","")
                device_json["recipe_start_date"] = recipe_runs[0].get("start","")
            # print("\t ... done ({})".format(time.time() - dev_start_time))

            # Get device status
            # print("\t getting device data")
            #device_data = datastore.get_device_data_from_DS(device_id)
            device_data = datastore.get_all_recent_device_data_properties(device_id)
            # print(device_data)
            if device_data is not None:
                # print("\t calculating connected/disconnected")
                #timestamp = device_data.get("timestamp")  # .decode()
                status_json = json.loads(device_data.get("status"))
                timestamp = status_json["timestamp"]
                timestamp = utils.bytes_to_string(timestamp)
                timenow = str(datetime.utcnow())
                fmt1 = "%Y-%m-%d %H:%M:%S.%f"
                fmt2 = "%Y-%m-%dT%H:%M:%SZ"

                t1 = datetime.strptime(timenow, fmt1)
                t2 = datetime.strptime(timestamp, fmt2)

                time_hours, time_minutes, _ = convert_timedelta(t1 - t2)
                time_minutes += time_hours * 60
                if time_minutes > 5:
                    wifi_status = "Disconnected"
                else:
                    wifi_status = "Connected"
                # print("\t ... done ({})".format(time.time() - dev_start_time))
                # print("\t setting current values")
                if device_data.get(datastore.DS_temp_KEY):
                    device_json["current_temp"] = "%s C" % (
                        (device_data.get(datastore.DS_temp_KEY))
                    )  # .decode())

                if device_data.get(datastore.DS_rh_KEY):
                    device_json["current_rh"] = "%s %%" % (
                        (device_data.get(datastore.DS_rh_KEY))
                    )

                if device_data.get(datastore.DS_co2_KEY):
                    device_json["current_co2"] = "%s ppm" % (
                        (device_data.get(datastore.DS_co2_KEY))
                    )

                if device_data.get(datastore.DS_h20_ph_KEY):
                    device_json["current_h20_ph"] = "%s" % (
                        (device_data.get(datastore.DS_h20_ph_KEY))
                    )

                if device_data.get(datastore.DS_h20_ec_KEY):
                    device_json["current_h20_ec"] = "%s mS/cm" % (
                        (device_data.get(datastore.DS_temp_KEY))
                    )

                if device_data.get(datastore.DS_h20_temp_KEY):
                    device_json["current_h20_temp"] = "%s C" % (
                        (device_data.get(datastore.DS_h20_temp_KEY))
                    )

                if device_data.get(datastore.DS_light_spectrum_KEY):
                    device_json["current_led_spectrum"] = "%s" % (
                        (device_data.get(datastore.DS_light_spectrum_KEY))
                    )

                device_json["wifi_status"] = wifi_status
                device_json["status_timestamp"] = timestamp
                device_json["status_last_seen_mins"] = time_minutes
            # print("\t ... done ({})".format(time.time() - dev_start_time))
            # Get latest Image
            # print("\t getting latest image")
            image_query = datastore.get_client().query(kind="Images",
                                                       order=['-creation_date'])
            image_query.add_filter('device_uuid', '=', device_id)
            images = list(image_query.fetch(1))
            if images and len(images) > 0:
                image_url = decode_url(images[0])
                device_json["latest_image"] = image_url


            # print(device_json)
            # print("\t ... done ({})".format(time.time() - dev_start_time))
            devices.append(device_json)
    # print(" ... done ({})".format(time.time() - full_start_time))
    return devices


