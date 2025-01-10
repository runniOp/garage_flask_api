import logging
from utils.database import db
from models.invoice import Invoice

logger = logging.getLogger(__name__)

def get_all_invoices():
    """
    Retrieve all invoices.
    :return: list: A list of dictionaries containing information about all invoices.
    """
    try:
        invoices = Invoice.query.all()
        return [
            {
                "invoice_id": invoice.invoice_id,
                "client_id": invoice.client_id,
                "issued_at": invoice.issued_at,
                "iva": invoice.iva,
                "total": invoice.total,
                "total_with_iva": invoice.total_with_iva,
            }
            for invoice in invoices
        ]
    except Exception as e:
        logger.error(f"Error fetching all invoices: {e}")
        return {"error": "Internal Server Error"}

def get_invoice(invoice_id):
    """
    Retrieve an invoice by ID.
    :param invoice_id: The ID of the invoice to retrieve.
    :return: dict: A dictionary containing the invoice information or None if not found.
    """
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return None
        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "iva": invoice.iva,
            "total": invoice.total,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        logger.error(f"Error fetching invoice {invoice_id}: {e}")
        return {"error": "Internal Server Error"}

def create_invoice(client_id, issued_at, iva, total, total_with_iva):
    """
    Create a new invoice.
    :param client_id: The client associated with the invoice.
    :param issued_at: The issue date of the invoice.
    :param iva: The IVA applied.
    :param total: The total amount before IVA.
    :param total_with_iva: The total amount including IVA.
    :return: dict: A dictionary containing the newly created invoice's information.
    """
    try:
        invoice = Invoice(client_id=client_id, issued_at=issued_at, iva=iva, total=total, total_with_iva=total_with_iva)
        db.session.add(invoice)
        db.session.commit()
        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "iva": invoice.iva,
            "total": invoice.total,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        logger.error(f"Error creating invoice: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}

def update_invoice(invoice_id, client_id, issued_at, iva, total, total_with_iva):
    """
    Update an existing invoice.
    :param invoice_id: The ID of the invoice to update.
    :return: dict: A dictionary containing the updated invoice's information or None if not found.
    """
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return None
        invoice.client_id = client_id if client_id else invoice.client_id
        invoice.issued_at = issued_at if issued_at else invoice.issued_at
        invoice.iva = iva if iva else invoice.iva
        invoice.total = total if total else invoice.total
        invoice.total_with_iva = total_with_iva if total_with_iva else invoice.total_with_iva

        db.session.commit()
        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "iva": invoice.iva,
            "total": invoice.total,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        logger.error(f"Error updating invoice {invoice_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}

def delete_invoice(invoice_id):
    """
    Delete an invoice.
    :param invoice_id: The ID of the invoice to delete.
    :return: dict: The deleted invoice's information or None if not found.
    """
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return None
        db.session.delete(invoice)
        db.session.commit()
        return invoice
    except Exception as e:
        logger.error(f"Error deleting invoice {invoice_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}
