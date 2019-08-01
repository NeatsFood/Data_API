import os
from flask import Flask
from flask import send_file
from flask_cors import CORS

from blueprints import (
    get_all_values,
    apply_to_device, 
    get_co2_details,
    get_current_stats, 
    get_temp_details, 
    get_user_devices, 
    get_recipe_by_uuid,
    register_device, 
    get_all_recipes, 
    get_device_types, 
    submit_recipe,
    delete_recipe,
    get_plant_types, 
    verify_user_session,
    user_authenticate, 
    upload_images, 
    get_user_info, 
    get_device_peripherals,
    get_device_images,
    submit_horticulture_measurements,
    save_user_profile_changes, 
    get_current_device_status,
    daily_horticulture_measurements, 
    get_horticulture_daily_logs,
    get_device_notifications, 
    ack_device_notification,
    view_image
)

app = Flask(__name__, 
        static_url_path='', # project root, the current directory 
        static_folder='doc/api-documentation/html') # doc root to serve

app.register_blueprint(get_all_values.get_all_values_bp)
app.register_blueprint(apply_to_device.apply_to_device_bp)
app.register_blueprint(get_co2_details.get_co2_details_bp)
app.register_blueprint(get_current_stats.get_current_stats_bp)
app.register_blueprint(get_temp_details.get_temp_details_bp)
app.register_blueprint(get_user_devices.get_user_devices_bp)
app.register_blueprint(register_device.register_bp)
app.register_blueprint(user_authenticate.user_authenticate)
app.register_blueprint(verify_user_session.verify_user_session_bp)
app.register_blueprint(get_device_peripherals.get_device_peripherals_bp)
app.register_blueprint(submit_recipe.submit_recipe_bp)
app.register_blueprint(delete_recipe.delete_recipe_bp)
app.register_blueprint(get_device_types.get_device_types_bp)
app.register_blueprint(get_plant_types.get_plant_types_bp)
app.register_blueprint(get_all_recipes.get_all_recipes_bp)
app.register_blueprint(get_recipe_by_uuid.get_recipe_by_uuid_bp)
app.register_blueprint(upload_images.upload_images_bp)
app.register_blueprint(get_user_info.get_user_info_bp)
app.register_blueprint(get_device_images.get_device_images_bp)
app.register_blueprint(save_user_profile_changes.save_user_profile_bp)
app.register_blueprint(get_current_device_status.get_current_device_status_bp)
app.register_blueprint(submit_horticulture_measurements.submit_horticulture_measurements_bp)
app.register_blueprint(daily_horticulture_measurements.daily_horticulture_measurements_bp)
app.register_blueprint(get_horticulture_daily_logs.get_horticulture_daily_logs_bp)
app.register_blueprint(view_image.viewimage_bp)
app.register_blueprint(get_device_notifications.get_device_notifications_bp)
app.register_blueprint(ack_device_notification.ack_device_notification_bp)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)


#------------------------------------------------------------------------------
# Serve our API documentation when a browser hits our URL.
@app.route('/')
def api_docs():
    return send_file(os.path.abspath('doc/api-documentation/html/index.html'))


#------------------------------------------------------------------------------
if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)



