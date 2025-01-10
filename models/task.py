from utils.database import db
from datetime import datetime

# Model definition for the 'Task' table
class Task(db.Model):
    """
    Represents a task in the database.

    Attributes:
        task_id (int): The primary key for the task table.
        created_at (datetime): Timestamp when the task was created. Defaults to the current time.
        description (str): The name of the task. Cannot be null.
        employee_id (int): Must be unique and cannot be null.
        end_date (date): The end date of the task.
        start_date (date): The start date of the task. Cannot be null.
        status (str): The status of the task.
        work_id (int): Must be unique and cannot be null.
    """

    # Define columns for the table
    task_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each task
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Auto-generated timestamp
    description = db.Column(db.String(255), nullable=False)  # task description
    employee_id = db.Column(db.Integer, nullable=False)  # identifier of employee table
    end_date = db.Column(db.DateTime, nullable=True)  # task end date
    start_date = db.Column(db.DateTime, nullable=False)  # task start date, cannot be null
    status = db.Column(db.String(50), nullable=False)  # task status
    work_id = db.Column(db.Integer, nullable=False)  # identifier of work table
    
    def __repr__(self):
        """
        String representation of the task object.
        Useful for debugging and logging purposes.
        """
        return f"<task {self.task_id}>"