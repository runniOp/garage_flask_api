import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.work_service import (
    get_all_works,
    get_work,
    create_work,
    update_work,
    delete_work
)
from utils.utils import generate_swagger_model
from models.work import Work

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing works
works_ns = Namespace('work', description='CRUD operations for managing works')

# Generate the Swagger model for the work resource
work_model = generate_swagger_model(
    api=works_ns,        # Namespace to associate with the model
    model=Work,          # SQLAlchemy model representing the work resource
    exclude_fields=[],   # No excluded fields in this model
    readonly_fields=['work_id']  # Fields that cannot be modified
)

@works_ns.route('/')
class WorkList(Resource):
    """
    Handles operations on the collection of works.
    Supports retrieving all works (GET) and creating new works (POST).
    """

    @works_ns.doc('get_all_works')
    @works_ns.marshal_list_with(work_model)
    def get(self):
        """
        Retrieve all works.
        :return: List of all works
        """
        try:
            # Fetch all works from the service layer
            return get_all_works()
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving works: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving works: {e}")
            works_ns.abort(500, "An error occurred while retrieving the works.")

    @works_ns.doc('create_work')
    @works_ns.expect(work_model, validate=True)
    @works_ns.marshal_with(work_model, code=201)
    def post(self):
        """
        Create a new work.
        :return: The created work
        """
        try:
            # Parse the input data
            data = works_ns.payload
            # Create a new work using the service layer
            new_work = create_work(data)
            return new_work, 201
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while creating work: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error creating work: {e}")
            works_ns.abort(500, "An error occurred while creating the work.")

@works_ns.route('/<int:work_id>')
@works_ns.param('work_id', 'The ID of the work')
class Work(Resource):
    """
    Handles operations on a single work.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) a work.
    """

    @works_ns.doc('get_work')
    @works_ns.marshal_with(work_model)
    def get(self, work_id):
        """
        Retrieve a work by ID.
        :param work_id: The ID of the work to retrieve.
        :return: The work with the specified ID
        """
        try:
            # Fetch the work by ID from the service layer
            work = get_work(work_id)
            if not work:
                # Return a 404 status code if the work is not found
                works_ns.abort(404, f"Work {work_id} not found.")
            return work
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving work {work_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving work {work_id}: {e}")
            works_ns.abort(500, "An error occurred while retrieving the work.")

    @works_ns.doc('update_work')
    @works_ns.expect(work_model, validate=True)
    @works_ns.marshal_with(work_model)
    def put(self, work_id):
        """
        Update a work by ID.
        :param work_id: The ID of the work to update.
        :return: The updated work
        """
        try:
            # Extract the request body
            data = works_ns.payload
            # Update the work using the service layer
            return update_work(
                work_id=work_id,
                cost=data['cost'],
                description=data['description'],
                status=data['status'],
                vehicle_id=data['vehicle_id'],
                start_date=data.get('start_date'),
                end_date=data.get('end_date')
            )
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while updating work {work_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error updating work {work_id}: {e}")
            works_ns.abort(500, "An error occurred while updating the work.")

    @works_ns.doc('delete_work')
    @works_ns.response(204, 'Work successfully deleted')
    def delete(self, work_id):
        """
        Delete a work by ID.
        :param work_id: The ID of the work to delete.
        :return: HTTP 204 status code if deleted successfully
        """
        try:
            # Delete the work using the service layer
            delete_work(work_id)
            return '', 204
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while deleting work {work_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error deleting work {work_id}: {e}")
            works_ns.abort(500, "An error occurred while deleting the work.")