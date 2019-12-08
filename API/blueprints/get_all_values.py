import json
from flask import Blueprint
from flask import request
import pandas as pd

from cloud_common.cc.google import datastore
from cloud_common.cc.google import database
from .utils.response import success_response, error_response
from .utils.auth import get_user_uuid_from_token


get_all_values_bp = Blueprint('get_all_values', __name__)

@get_all_values_bp.route('/api/get_all_values/', methods=['POST'])
def get_all_values():
    """Retrieve all sensor and horticulture values for a device.

    .. :quickref: Device; Get all values 

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: Device to get data for.
    :<json string start_ts: UTC timestamp of stating date.
    :<json string end_ts: UTC timestamp of ending date.

    **Example response**:

        .. sourcecode:: json

          {
              "RH": [
                  {"value": "28.0", "time": "2019-05-08T18:39:53Z"},
                  {"value": "29.0", "time": "2019-05-08T18:29:52Z"}],
              "temp": [
                  {"value": "25.0", "time": "2019-05-08T18:29:52Z"},
                  {"value": "24.0", "time": "2019-05-08T18:24:52Z"}],
              "co2": [
                  {"value": "33246.0", "time": "2019-05-08T16:44:39Z"},
                  {"value": "33244.0", "time": "2019-05-08T16:39:39Z"}],
              "leaf_count": [
                  {"value": 3, "time": "2019-04-08T13:18:58Z"}],
                  {"value": 8, "time": "2019-04-09T03:10:08Z"}],
              "plant_height": [
                  {"value": 2.5, "time": "2019-04-08T13:18:58Z"}],
                  {"value": 2.9, "time": "2019-04-09T03:08:08Z"}],
              "response-code": 200
          }

    """
    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", None)
    device_uuid = received_form_response.get("device_uuid", None)
    start_ts = received_form_response.get("start_ts", None)
    end_ts = received_form_response.get("end_ts", None)
    if user_token is None or device_uuid is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    # Get 5 lists of dicts of all the data in the date range
    temp, RH, co2, leaf_count, plant_height, horticulture_notes = \
        database.get_all_historical_values(device_uuid, start_ts, end_ts)

    return success_response(
        temp=temp,
        RH=RH,
        co2=co2,
        leaf_count=leaf_count,
        plant_height=plant_height,
        horticulture_notes=horticulture_notes,
    )


#------------------------------------------------------------------------------
@get_all_values_bp.route('/api/get_all_values_as_csv/', methods=['POST'])
def get_all_values_as_csv():
    """Retrieve a CSV of all sensor and horticulture values for a device, suitable for downloading as a file.

    .. :quickref: Device; Get all values as CSV

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.
    :<json string device_uuid: Device to get data for.
    :<json string start_ts: UTC timestamp of stating date.
    :<json string end_ts: UTC timestamp of ending date.

    **Example response**:

        .. sourcecode:: json

          {
              "CSV": "one giant string of: time, temp, RH, co2, leaf_count, plant_height"
              "response-code": 200
          }

    """

    received_form_response = json.loads(request.data.decode('utf-8'))
    user_token = received_form_response.get("user_token", None)
    device_uuid = received_form_response.get("device_uuid", None)
    start_ts = received_form_response.get("start_ts", None)
    end_ts = received_form_response.get("end_ts", None)
    if user_token is None or device_uuid is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    # Get 5 lists of dicts of all the data in the date range
    temp, RH, co2, leaf_count, plant_height = \
        database.get_all_historical_values(device_uuid, start_ts, end_ts)

    # Make dataframes from the list of dicts and merge them into one frame
    result = pd.DataFrame()
    temp_df = pd.DataFrame(temp)
    if 0 < len(temp):
        temp_df.columns=['timestamp', 'air_temp_C']

    RH_df = pd.DataFrame(RH)
    if 0 < len(RH):
        RH_df.columns=['timestamp', 'RH']

    if 0 < len(temp) and 0 < len(RH):
        result = pd.merge(temp_df, RH_df, on='timestamp', how='outer', sort=True)

    co2_df = pd.DataFrame(co2)
    if 0 < len(co2):
        co2_df.columns=['timestamp', 'CO2']
        result = pd.merge(result, co2_df, on='timestamp', how='outer', sort=True)

    leaf_count_df = pd.DataFrame(leaf_count)
    if 0 < len(leaf_count):
        leaf_count_df.columns=['timestamp', 'leaf_count']
        result = pd.merge(result, leaf_count_df, on='timestamp', how='outer', sort=True)

    plant_height_df = pd.DataFrame(plant_height)
    if 0 < len(plant_height):
        plant_height_df.columns=['timestamp', 'plant_height']
        result = pd.merge(result, plant_height_df, on='timestamp', how='outer', sort=True)

    return success_response(
        CSV=result.to_csv()
    )



