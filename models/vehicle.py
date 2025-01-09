from utils.database import db

# Model definition for the 'Vehicle' table
class Vehicle(db.Model):
    """
    Represents a vehicle in the database.

    Attributes:
        vehicle_id (int): The primary key for the vehicle table.
        brand (TEXT): The brand of the vehicle.cannot be null.
        client_id (int): The ID of the client who owns the vehicle. Cannot be null.
        created_at (datetime): Timestamp when the vehicle was created. Defaults to the current time.
        license_plate (TEXT): The license plate of the vehicle. Cannot be null.
        model (TEXT): The model of the vehicle. Cannot be null.
        year (int): The year of the vehicle. Cannot be null.
    """

    # Define columns for the table
    vehicle_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each vehicle
    brand = db.Column(db.Text, nullable=False)  # Vehicle brand
    client_id = db.Column(db.Integer, db.ForeignKey('client'), nullable=False)  # Client ID who owns the vehicle
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Auto-generated timestamp
    license_plate = db.Column(db.Text, nullable=False)  # Vehicle license plate
    model = db.Column(db.Text, nullable=False)  # Vehicle model
    year = db.Column(db.Integer, nullable=False)  # Vehicle year
    def __repr__(self):
        """
        String representation of the Vehicle object.
        Useful for debugging and logging purposes.
        """
        return f"<Vehicle {self.vehicle_id} {self.brand} {self.year}>"