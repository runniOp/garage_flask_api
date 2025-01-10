import logging
from utils.database import db
from models.setting import Setting

logger = logging.getLogger(__name__)

def get_all_settings():
    """
    Retrieve all settings.
    :return: list: A list of dictionaries containing information about all settings.
    """
    try:
        settings = Setting.query.all()  # Retrieve all settings from the database
        return [
            {
                "setting_id": setting.setting_id,
                "key_name": setting.key_name,
                "updated_at": setting.updated_at,
                "value": setting.value,
            }
            for setting in settings
        ]
    except Exception as e:
        logger.error(f"Error fetching all settings: {e}")
        return {"error": "Internal Server Error"}

def get_setting(setting_id):
    """
    Retrieve a setting by ID.
    :param setting_id: The ID of the setting to retrieve.
    :return: dict: A dictionary containing the setting's information or an error message.
    """
    try:
        setting = Setting.query.get(setting_id)
        if not setting:
            return None
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "updated_at": setting.updated_at,
            "value": setting.value,
        }
    except Exception as e:
        logger.error(f"Error fetching setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}

def create_setting(key_name, value):
    """
    Create a new setting.
    :param key_name: The name of the setting.
    :param value: The value of the setting.
    :return: tuple: A dictionary containing the newly created setting's information and the HTTP status code.
    """
    try:
        setting = Setting(key_name=key_name, value=value)
        db.session.add(setting)  # Save the new setting to the database
        db.session.commit() # Save the new setting to the database
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "updated_at": setting.updated_at,
            "value": setting.value,
        }
    except Exception as e:
        logger.error(f"Error creating setting: {e}")
        return {"error": "Internal Server Error"}


def update_setting(setting_id, key_name, updated_at, value):
    """
    Update an existing setting.
    :param setting_id: The ID of the setting to update.
    :param key_name: The name of the setting.
    :param value: The value of the setting.
    :return: tuple: A dictionary containing the updated setting's information or an error message and the HTTP status code.
    """
    try:
        # Find the setting by ID
        setting = Setting.query.get(setting_id)

        if not setting:
            return None

        # Update the fields if new values are provided (they can be optional)
        setting.key_name = key_name if key_name else setting.key_name
        setting.value = value if value else setting.value

        # Commit the changes to the database
        db.session.commit()
        # Return updated setting information
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "updated_at": setting.updated_at,
            "value": setting.value,
        }
    except Exception as e:
        # If an error occurs, rollback the transaction
        db.session.rollback()
        logger.error(f"Error updating setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}
def delete_setting(setting_id):
    """
    Delete a setting.
    :param setting_id: The ID of the setting to delete.
    :return: tuple: A message confirming deletion or an error message and the HTTP status code.
    """
    try:
        setting = Setting.query.get(setting_id)
        if not setting:
            return None
        # Delete the setting
        db.session.delete(setting)
        # Commit the deletion
        db.session.commit()
        return setting
    except Exception as e:
        logger.error(f"Error deleting setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}