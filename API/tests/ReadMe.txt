In this directory are pytest files (file names starting with test_).

In each test_* file there are functions that start with "test_" which will be run by pytest.

Some of the files of tests have a number in them, e.g. "01", that is to make
sure those tests run before the other tests because they save something into
the global_vars class.  Such as a user token, so we don't have to login before
every API call.

There is a script in Data_API/scripts/test.sh that runs pytest and it discovers all test files and functions that begin with "test_".

This page is helpful understanding how to test a Flask REST API with pytest:
http://flask.pocoo.org/docs/1.0/testing/
