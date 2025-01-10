import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.invoice_service import (
    get_all_invoices,
    get_invoice,
    create_invoice,
    update_invoice,
    delete_invoice
)
from utils.utils import generate_swagger_model
from models.invoice import Invoice


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing invoices
invoices_ns = Namespace('invoice', description='CRUD operations for managing invoices')

# Generate the Swagger model for the invoice resource
invoice_model = generate_swagger_model(
    api=invoices_ns,
    model=Invoice,
    exclude_fields=[],
    readonly_fields=['invoice_id']
)


@invoices_ns.route('/')
class InvoiceList(Resource):
    """
    Handles operations on the collection of invoices.
    Supports retrieving all invoices (GET) and creating new invoices (POST).
    """

    @invoices_ns.doc('get_all_invoices')
    @invoices_ns.marshal_list_with(invoice_model)
    def get(self):
        """
        Retrieve all invoices.
        :return: List of all invoices
        """
        try:
            return get_all_invoices()
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving invoices: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving invoices: {e}")
            invoices_ns.abort(500, "An error occurred while retrieving the invoices.")

    @invoices_ns.doc('create_invoice')
    @invoices_ns.expect(invoice_model, validate=True)
    @invoices_ns.marshal_with(invoice_model, code=201)
    def post(self):
        """
        Create a new invoice.
        :return: The created invoice with HTTP status code 201
        """
        data = invoices_ns.payload
        try:
            return create_invoice(data["client_id"], data["issued_at"], data["iva"], data["total"], data["total_with_iva"]), 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating invoice: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            invoices_ns.abort(500, "An error occurred while creating the invoice.")


@invoices_ns.route('/<int:invoice_id>')
@invoices_ns.param('invoice_id', 'The ID of the invoice')
class Invoice(Resource):
    """
    Handles operations on a single invoice.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) an invoice.
    """

    @invoices_ns.doc('get_invoice')
    @invoices_ns.marshal_with(invoice_model)
    def get(self, invoice_id):
        """
        Retrieve an invoice by ID.
        :param invoice_id: The ID of the invoice
        :return: The invoice details or 404 if not found
        """
        try:
            invoice = get_invoice(invoice_id)
            if not invoice:
                invoices_ns.abort(404, f"Invoice with ID {invoice_id} not found.")
            return invoice
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving invoice with ID {invoice_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving invoice with ID {invoice_id}: {e}")
            invoices_ns.abort(500, "An error occurred while retrieving the invoice.")

    @invoices_ns.doc('update_invoice')
    @invoices_ns.expect(invoice_model, validate=True)
    @invoices_ns.marshal_with(invoice_model)
    def put(self, invoice_id):
        """
        Update an invoice by ID.
        :param invoice_id: The ID of the invoice
        :return: The updated invoice details or 404 if not found
        """
        data = invoices_ns.payload
        try:
            invoice = update_invoice(invoice_id, data["client_id"], data["issued_at"], data["iva"], data["total"], data["total_with_iva"])
            if not invoice:
                invoices_ns.abort(404, f"Invoice with ID {invoice_id} not found.")
            return invoice
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating invoice with ID {invoice_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error updating invoice with ID {invoice_id}: {e}")
            invoices_ns.abort(500, "An error occurred while updating the invoice.")

    @invoices_ns.doc('delete_invoice')
    @invoices_ns.response(204, 'Invoice successfully deleted')
    def delete(self, invoice_id):
        """
        Delete an invoice by ID.
        :param invoice_id: The ID of the invoice
        :return: HTTP 204 status code if deleted successfully or 404 if not found
        """
        try:
            invoice = delete_invoice(invoice_id)
            if not invoice:
                invoices_ns.abort(404, f"Invoice with ID {invoice_id} not found.")
            return '', 204
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting invoice with ID {invoice_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error deleting invoice with ID {invoice_id}: {e}")
            invoices_ns.abort(500, "An error occurred while deleting the invoice.")
