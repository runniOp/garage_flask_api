from utils.database import db

# Model definition for the 'Work' table

class Work(db.Model):
    """
    Represents a work in the database.

    Attributes:
        work_id (int): The primary key for the work table.
        cost (float): The cost of the work. Cannot be null.
        created_at (datetime): Timestamp when the work was created. Defaults to the current time.
        description (text): The description of the work. Cannot be null.
        end_date (datetime): The end date of the work.
        start_date (datetime): The start date of the work
        status (text): The status of the work. Cannot be null.
        vehicle_id (int): The foreign key to the vehicle table.
    """

    # Define columns for the table
    work_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each work
    cost = db.Column(db.Float, nullable=False)  # Work cost    
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Auto-generated timestamp
    description = db.Column(db.Text, nullable=False)  # Work description
    end_date = db.Column(db.Date)  # Work end date
    start_date = db.Column(db.DateTime)  # Work start date
    status = db.Column(db.Text, nullable=False)  # Work status
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)  # Vehicle foreign key
    def __repr__(self):
        """
        String representation of the Work object.
        Useful for debugging and logging purposes.
        """
        return f"<Work {self.work_id}>"