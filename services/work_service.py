import logging
from utils.database import db
from models.work import Work 
from datetime import datetime

logger = logging.getLogger(__name__)

def get_all_works():
    """
    Retrieve all works.
    :return: list: A list of dictionaries containing information about all works.
    """
    try:
        works = Work.query.all()  # Retrieve all works from the database
        return [
            {
                "work_id": work.work_id,
                "cost": work.cost,
                "created_at": work.created_at,
                "description": work.description,
                "end_date": work.end_date,
                "start_date": work.start_date,
                "status": work.status,
                "vehicle_id": work.vehicle_id
            }
            for work in works
        ]
    except Exception as e:
        logger.error(f"Error fetching all works: {e}")
        return {"error": "Internal Server Error"}

def get_work(work_id):
    """
    Retrieve a work by ID.
    :param work_id: The ID of the work to retrieve.
    :return: dict: A dictionary containing the work's information or an error message.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None
        return {
            "work_id": work.work_id,
            "cost": work.cost,
            "created_at": work.created_at,
            "description": work.description,
            "end_date": work.end_date,
            "start_date": work.start_date,
            "status": work.status,
            "vehicle_id": work.vehicle_id
        }
    except Exception as e:
        logger.error(f"Error fetching work {work_id}: {e}")
        return {"error": "Internal Server Error"}

def create_work(cost, description, status, vehicle_id, start_date=None, end_date=None):
    """
    Create a new work.
    :param cost: The cost of the work.
    :param description: The description of the work.
    :param status: The status of the work.
    :param vehicle_id: The ID of the vehicle associated with the work.
    :param start_date: The start date of the work (optional).
    :param end_date: The end date of the work (optional).
    :return: dict: A dictionary containing the newly created work's information.
    """
    try:
        work = Work(cost=cost, description=description, status=status, vehicle_id=vehicle_id, start_date=start_date, end_date=end_date)
        db.session.add(work)  # Save the new work to the database
        db.session.commit()
        return {
            "work_id": work.work_id,
            "cost": work.cost,
            "created_at": work.created_at,
            "description": work.description,
            "end_date": work.end_date,
            "start_date": work.start_date,
            "status": work.status,
            "vehicle_id": work.vehicle_id
        }
    except Exception as e:
        logger.error(f"Error creating work: {e}")
        return {"error": "Internal Server Error"}

from datetime import datetime    

def update_work(work_id, cost, description, status, vehicle_id, start_date=None, end_date=None):
    """
    Update an existing work.
    :param work_id: The ID of the work to update.
    :param cost: The cost of the work.
    :param description: The description of the work.
    :param status: The status of the work.
    :param vehicle_id: The ID of the vehicle associated with the work.
    :param start_date: The start date of the work (optional).
    :param end_date: The end date of the work (optional).
    :return: dict: A dictionary containing the updated work's information.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None
        work.cost = cost
        work.description = description
        work.status = status
        work.vehicle_id = vehicle_id
        work.start_date = start_date
        work.end_date = end_date
        db.session.commit()
        return {
            "work_id": work.work_id,
            "cost": work.cost,
            "created_at": work.created_at,
            "description": work.description,
            "end_date": work.end_date,
            "start_date": work.start_date,
            "status": work.status,
            "vehicle_id": work.vehicle_id
        }
    except Exception as e:
        logger.error(f"Error updating work {work_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_work(work_id):
    """
    Delete a work by ID.
    :param work_id: The ID of the work to delete.
    :return: dict: A dictionary containing the status of the deletion operation.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None
        db.session.delete(work)
        db.session.commit()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error deleting work {work_id}: {e}")
        return {"error": "Internal Server Error"}