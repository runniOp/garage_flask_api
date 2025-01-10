from utils.database import db


# Model definition for the 'Setting' table
class Setting(db.Model):
    """
    Represents a setting in the database.

    Attributes:
        setting_id (int): The primary key for the setting table.
        key_name (str): The name of the setting. Must be unique and cannot be null.
        updated_at (datetime): Timestamp when the setting was created. Defaults to the current time.
        value (str): The value of the setting. Cannot be null.
    """

    # Define columns for the table
    setting_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each setting
    key_name = db.Column(db.String(80), unique=True, nullable=False)  # setting name, must be unique
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())  # Auto-generated timestamp
    value = db.Column(db.String(200), nullable=False)  # setting value
    
    def __repr__(self):
        """
        String representation of the setting object.
        Useful for debugging and logging purposes.
        """
        return f"<setting {self.key_name}>"