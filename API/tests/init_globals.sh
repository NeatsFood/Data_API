#!/bin/bash
../../scripts/test.sh tests/test_01_user_authenticate.py::test_login_works tests/test_02_get_user_devices.py::test_get_user_devices_works tests/$*
