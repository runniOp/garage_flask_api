import logging
from utils.database import db
from models.task import Task

logger = logging.getLogger(__name__)

def get_all_tasks():
    """
    Retrieve all tasks.
    :return: list: A list of dictionaries containing information about all tasks.
    """
    try:
        tasks = Task.query.all()  # Retrieve all tasks from the database
        return [
            {
                "task_id": task.task_id,
                "created_at": task.created_at,
                "description": task.description,
                "employee_id": task.employee_id,
                "end_date": task.end_date,
                "start_date": task.start_date,
                "status": task.status,
                "work_id": task.work_id,
            }
            for task in tasks
        ]
    except Exception as e:
        logger.error(f"Error fetching all tasks: {e}")
        return {"error": "Internal Server Error"}

def get_task(task_id):
    """
    Retrieve a task by ID.
    :param task_id: The ID of the task to retrieve.
    :return: dict: A dictionary containing the task's information or an error message.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return None
        return {
            "task_id": task.task_id,
            "created_at": task.created_at,
            "description": task.description,
            "employee_id": task.employee_id,
            "end_date": task.end_date,
            "start_date": task.start_date,
            "status": task.status,
            "work_id": task.work_id,
        }
    except Exception as e:
        logger.error(f"Error fetching task {task_id}: {e}")
        return {"error": "Internal Server Error"}

def create_task(description, end_date, start_date, status):
    """
    Create a new task.
    :param description: The description of the task.
    :param end_date: The end_date of the task.
    :param start_date: The start_date of the task.
    :param status: The status of the task.
    :return: tuple: A dictionary containing the newly created task's information and the HTTP status code.
    """
    try:
        task = Task(description=description, end_date=end_date, start_date=start_date, status=status)
        db.session.add(task)  # Save the new task to the database
        db.session.commit() # Save the new task to the database
        return {
            "task_id": task.task_id,
            "created_at": task.created_at,
            "description": task.description,
            "employee_id": task.employee_id,
            "end_date": task.end_date,
            "start_date": task.start_date,
            "status": task.status,
            "work_id": task.work_id,
        }
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return {"error": "Internal Server Error"}


def update_task(task_id, description, employee_id, end_date, start_date, status, work_id):
    """
    Update an existing task.
    :param task_id: The ID of the task to update.
    :param description: The description of the task.
    :param employee_id: The ID of the employee to update.
    :param end_date: The end_date of the task.
    :param start_date: The start_date of the task.
    :param status: The status of the task.
    :param work_id: The ID of the work to update.
    :return: tuple: A dictionary containing the updated task's information or an error message and the HTTP status code.
    """
    try:
        # Find the task by ID
        task = Task.query.get(task_id)

        if not task:
            return None

        # Update the fields if new values are provided (they can be optional)
        task.description = description if description else task.description
        task.employee_id = employee_id if employee_id else task.employee_id
        task.end_date = end_date if end_date else task.end_date
        task.start_date = start_date if start_date else task.start_date
        task.status = status if status else task.status
        task.work_id = work_id if work_id else task.work_id

        # Commit the changes to the database
        db.session.commit()
        # Return updated task information
        return {
            "task_id": task.task_id,
            "created_at": task.created_at,
            "description": task.description,
            "employee_id": task.employee_id,
            "end_date": task.end_date,
            "start_date": task.start_date,
            "status": task.status,
            "work_id": task.work_id,
        }
    except Exception as e:
        # If an error occurs, rollback the transaction
        db.session.rollback()
        logger.error(f"Error updating task {task_id}: {e}")
        return {"error": "Internal Server Error"}
def delete_task(task_id):
    """
    Delete a task.
    :param task_id: The ID of the task to delete.
    :return: tuple: A message confirming deletion or an error message and the HTTP status code.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return None
        # Delete the task
        db.session.delete(task)
        # Commit the deletion
        db.session.commit()
        return task
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        return {"error": "Internal Server Error"}