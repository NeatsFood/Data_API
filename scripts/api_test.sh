#/bin/bash

HOST=localhost:5000

COOKIES=cookies.txt
#CURL_BIN="curl -s -c $COOKIES -b $COOKIES -e $LOGIN_URL"
CURL_BIN="curl -s  "

# Try to register a device
REST_URL=http://$HOST/api/register/
REST_METHOD=POST
POST_DATA='{"user_token": "b603826e-ac5b-4dae-a509-41c207222a9e", "device_name": "Test", "device_reg_no": "00000000", "device_notes": "Test", "device_type": "EDU"}'
echo "CALLING REST API: $REST_URL"
RET=`$CURL_BIN -X $REST_METHOD $REST_URL -H "Content-Type: application/json" -d "$POST_DATA" `
#RET=`$CURL_BIN -X $REST_METHOD $REST_URL -H "X-CSRFToken: $CSRF" -H "Content-Type: application/json" -d "$POST_DATA" --cookie "csrftoken=$CSRF"`
echo $RET
echo ''

