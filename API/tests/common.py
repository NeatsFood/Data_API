"""
For these tests to all pass, we require:
    A UI user named "testman" with password "testman".
    The 'testman' user needs a device associated with their UI account.
    There needs to be one available recipe in the datastore Recipes collection.
"""
# This is a common function to do a POST to a Flask URL.
# Returns the result of the POST.
def do_post(client, post_data_dict, URL):
    rv = client.post(URL, json=post_data_dict, follow_redirects=True)
    print(f'{URL} POST result={rv.get_json()}')
    return rv.get_json()

def do_form_post(client, post_data_dict, URL):
    rv = client.post(URL, data=post_data_dict, follow_redirects=True,
            content_type='multipart/form-data')
    print(f'{URL} FORM POST result={rv.get_json()}')
    return rv.get_json()

def do_get(client, URL):
    rv = client.get(URL, follow_redirects=True)
    print(f'{URL} GET result={rv}')
    return rv


