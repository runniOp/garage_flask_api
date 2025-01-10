import logging
from utils.database import db
from models.invoice_item import InvoiceItem

logger = logging.getLogger(__name__)

def get_all_invoice_items():
    """
    Retrieve all invoice items.
    :return: list: A list of dictionaries containing information about all invoice items.
    """
    try:
        items = InvoiceItem.query.all()
        return [
            {
                "item_id": item.item_id,
                "description": item.description,
                "cost": item.cost,
                "invoice_id": item.invoice_id,
                "task_id": item.task_id,
            }
            for item in items
        ]
    except Exception as e:
        logger.error(f"Error fetching all invoice items: {e}")
        return {"error": "Internal Server Error"}

def get_invoice_item(item_id):
    """
    Retrieve an invoice item by ID.
    :param item_id: The ID of the invoice item to retrieve.
    :return: dict: A dictionary containing the invoice item's information or None if not found.
    """
    try:
        item = InvoiceItem.query.get(item_id)
        if not item:
            return None
        return {
            "item_id": item.item_id,
            "description": item.description,
            "cost": item.cost,
            "invoice_id": item.invoice_id,
            "task_id": item.task_id,
        }
    except Exception as e:
        logger.error(f"Error fetching invoice item {item_id}: {e}")
        return {"error": "Internal Server Error"}

def create_invoice_item(description, cost, invoice_id, task_id):
    """
    Create a new invoice item.
    :return: dict: A dictionary containing the newly created invoice item's information.
    """
    try:
        item = InvoiceItem(description=description, cost=cost, invoice_id=invoice_id, task_id=task_id)
        db.session.add(item)
        db.session.commit()
        return {
            "item_id": item.item_id,
            "description": item.description,
            "cost": item.cost,
            "invoice_id": item.invoice_id,
            "task_id": item.task_id,
        }
    except Exception as e:
        logger.error(f"Error creating invoice item: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}

def update_invoice_item(item_id, description, cost, invoice_id, task_id):
    """
    Update an existing invoice item.
    :return: dict: The updated invoice item's information or None if not found.
    """
    try:
        item = InvoiceItem.query.get(item_id)
        if not item:
            return None
        item.description = description if description else item.description
        item.cost = cost if cost else item.cost
        item.invoice_id = invoice_id if invoice_id else item.invoice_id
        item.task_id = task_id if task_id else item.task_id

        db.session.commit()
        return {
            "item_id": item.item_id,
            "description": item.description,
            "cost": item.cost,
            "invoice_id": item.invoice_id,
            "task_id": item.task_id,
        }
    except Exception as e:
        logger.error(f"Error updating invoice item {item_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}

def delete_invoice_item(item_id):
    """
    Delete an invoice item.
    :return: dict: The deleted invoice item's information or None if not found.
    """
    try:
        item = InvoiceItem.query.get(item_id)
        if not item:
            return None
        db.session.delete(item)
        db.session.commit()
        return item
    except Exception as e:
        logger.error(f"Error deleting invoice item {item_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}
