import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.setting_service import (
    get_all_settings,
    get_setting,
    create_setting,
    update_setting,
    delete_setting
)
from utils.utils import generate_swagger_model
from models.setting import Setting


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing settings
settings_ns = Namespace('setting', description='CRUD operations for managing settings')

# Generate the Swagger model for the setting resource
setting_model = generate_swagger_model(
    api=settings_ns,        # Namespace to associate with the model
    model=Setting,          # SQLAlchemy model representing the setting resource
    exclude_fields=[],     # No excluded fields in this model
    readonly_fields=['setting_id']  # Fields that cannot be modified
)


@settings_ns.route('/')
class SettingList(Resource):
    """
    Handles operations on the collection of settings.
    Supports retrieving all settings (GET) and creating new settings (POST).
    """

    @settings_ns.doc('get_all_settings')
    @settings_ns.marshal_list_with(setting_model)
    def get(self):
        """
        Retrieve all settings.
        :return: List of all settings
        """
        try:
            # Fetch all settings from the service layer
            return get_all_settings()
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving settings: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving settings: {e}")
            settings_ns.abort(500, "An error occurred while retrieving the settings.")

    @settings_ns.doc('create_setting')
    @settings_ns.expect(setting_model, validate=True)
    @settings_ns.marshal_with(setting_model, code=201)
    def post(self):
        """
        Create a new setting.
        :return: The created setting with HTTP status code 201
        """
        data = settings_ns.payload  # Extract JSON payload
        try:
            # Call the service to create a new setting
            return create_setting(data["key_name"],data["value"]), 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating setting: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error creating setting: {e}")
            settings_ns.abort(500, "An error occurred while creating the setting.")


@settings_ns.route('/<int:setting_id>')
@settings_ns.param('setting_id', 'The ID of the setting')
class Setting(Resource):
    """
    Handles operations on a single setting.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) a setting.
    """

    @settings_ns.doc('get_setting')
    @settings_ns.marshal_with(setting_model)
    def get(self, setting_id):
        """
        Retrieve a setting by ID.
        :param setting_id: The ID of the setting
        :return: The setting details or 404 if not found
        """
        try:
            # Fetch setting by ID
            setting = get_setting(setting_id)
            if not setting:
                # Return a 404 error if setting does not exist
                settings_ns.abort(404, f"setting with ID {setting_id} not found.")
            return setting
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving setting with ID {setting_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving setting with ID {setting_id}: {e}")
            settings_ns.abort(500, "An error occurred while retrieving the setting.")

    @settings_ns.doc('update_setting')
    @settings_ns.expect(setting_model, validate=True)
    @settings_ns.marshal_with(setting_model)
    def put(self, setting_id):
        """
        Update a setting by ID.
        :param setting_id: The ID of the setting
        :return: The updated setting details or 404 if not found
        """
        data = settings_ns.payload  # Extract JSON payload
        try:
            # Call the service to update the setting
            setting = update_setting(setting_id, data["key_name"],data["value"])
            if not setting:
                # Return a 404 error if setting does not exist
                settings_ns.abort(404, f"setting with ID {setting_id} not found.")
            return setting
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating setting with ID {setting_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error updating setting with ID {setting_id}: {e}")
            settings_ns.abort(500, "An error occurred while updating the setting.")

    @settings_ns.doc('delete_setting')
    @settings_ns.response(204, 'setting successfully deleted')
    def delete(self, setting_id):
        """
        Delete a setting by ID.
        :param setting_id: The ID of the setting
        :return: HTTP 204 status code if deleted successfully or 404 if not found
        """
        try:
            # Call the service to delete the setting
            setting = delete_setting(setting_id)
            if not setting:
                # Return a 404 error if setting does not exist
                settings_ns.abort(404, f"setting with ID {setting_id} not found.")
            return '', 204  # Return no content with status code 204
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting setting with ID {setting_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error deleting setting with ID {setting_id}: {e}")
            settings_ns.abort(500, "An error occurred while deleting the setting.")