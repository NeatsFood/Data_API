import json
from datetime import datetime, timezone

# ------------------------------------------------------------------------------
def is_expired(expiration_date):
    """Returns whether something has expired

    Assumes that expiration_date is an 'aware' datetime object.
    """
    datenow = datetime.now(timezone.utc)
    return datenow > expiration_date


# ------------------------------------------------------------------------------
# Convert the UI display fields into a command set for the device.
# Returns a valid Jbrain recipe.
def convert_UI_recipe_to_commands(recipe_uuid, recipe_dict):
    try:
        # This "spectrum_key" is used to display the recipe.
        # We have to remove it from the recipe before we send it to
        # the device.   The brain doesn't know what to do with it (not part of
        # official recipe format).
        if "environments" in recipe_dict:
            for e in recipe_dict["environments"]:
                recipe_dict["environments"][e].pop('spectrum_key', None)

        recipe_json = json.dumps(recipe_dict)

        # Currently we can only send a start or stop command.
        return_list = []
        cmd = {}
        cmd['command'] = 'START_RECIPE'
        cmd['arg0'] = recipe_json
        cmd['arg1'] = '0'
        return_list = [cmd]

        return return_list
    except(Exception) as e:
        print(f'Exception in convert_UI_recipe_to_commands: {e}')


