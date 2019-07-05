# http://flask.pocoo.org/docs/1.0/testing/

from global_vars import global_vars # global vars used in tests
import common
from cloud_common.cc.notifications.notification_data import NotificationData


#------------------------------------------------------------------------------
# test ack_device_notification blueprint
def test_ack_device_notification_works(client):

    # first create a notification
    nd = NotificationData()
    ID = nd.add(global_vars.device_uuid, "running pytest")
    
    data = {"device_uuid": global_vars.device_uuid,
            "ID": ID} # the ID of the notification we just created
    URL = '/api/ack_device_notification/'
    rv = common.do_post(client, data, URL)
    assert 200 == rv['response_code']

def test_ack_device_notification_fails(client):
    data = {} # no data so it should fail
    URL = '/api/ack_device_notification/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_ack_device_notification_no_deviceid(client):
    data = {"ID": "blarg"} 
    URL = '/api/ack_device_notification/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

def test_ack_device_notification_no_notificationid(client):
    data = {"device_uuid": global_vars.device_uuid}
    URL = '/api/ack_device_notification/'
    rv = common.do_post(client, data, URL)
    assert 500 == rv['response_code']

