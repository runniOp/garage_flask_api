import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.task_service import (
    get_all_tasks,
    get_task,
    create_task,
    update_task,
    delete_task
)
from utils.utils import generate_swagger_model
from models.task import Task


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing tasks
tasks_ns = Namespace('task', description='CRUD operations for managing tasks')

# Generate the Swagger model for the task resource
task_model = generate_swagger_model(
    api=tasks_ns,        # Namespace to associate with the model
    model=Task,          # SQLAlchemy model representing the task resource
    exclude_fields=[],     # No excluded fields in this model
    readonly_fields=['task_id']  # Fields that cannot be modified
)


@tasks_ns.route('/')
class TaskList(Resource):
    """
    Handles operations on the collection of tasks.
    Supports retrieving all tasks (GET) and creating new tasks (POST).
    """

    @tasks_ns.doc('get_all_tasks')
    @tasks_ns.marshal_list_with(task_model)
    def get(self):
        """
        Retrieve all tasks.
        :return: List of all tasks
        """
        try:
            # Fetch all tasks from the service layer
            return get_all_tasks()
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving tasks: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving tasks: {e}")
            tasks_ns.abort(500, "An error occurred while retrieving the tasks.")

    @tasks_ns.doc('create_task')
    @tasks_ns.expect(task_model, validate=True)
    @tasks_ns.marshal_with(task_model, code=201)
    def post(self):
        """
        Create a new task.
        :return: The created task with HTTP status code 201
        """
        data = tasks_ns.payload  # Extract JSON payload
        try:
            # Call the service to create a new task
            return create_task(data["description"],data["end_date"],data["start_date"],data["status"]), 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating task: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error creating task: {e}")
            tasks_ns.abort(500, "An error occurred while creating the task.")


@tasks_ns.route('/<int:task_id>')
@tasks_ns.param('task_id', 'The ID of the task')
class Task(Resource):
    """
    Handles operations on a single task.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) a task.
    """

    @tasks_ns.doc('get_task')
    @tasks_ns.marshal_with(task_model)
    def get(self, task_id):
        """
        Retrieve a task by ID.
        :param task_id: The ID of the task
        :return: The task details or 404 if not found
        """
        try:
            # Fetch task by ID
            task = get_task(task_id)
            if not task:
                # Return a 404 error if task does not exist
                tasks_ns.abort(404, f"task with ID {task_id} not found.")
            return task
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving task with ID {task_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving task with ID {task_id}: {e}")
            tasks_ns.abort(500, "An error occurred while retrieving the task.")

    @tasks_ns.doc('update_task')
    @tasks_ns.expect(task_model, validate=True)
    @tasks_ns.marshal_with(task_model)
    def put(self, task_id):
        """
        Update a task by ID.
        :param task_id: The ID of the task
        :return: The updated task details or 404 if not found
        """
        data = tasks_ns.payload  # Extract JSON payload
        try:
            # Call the service to update the task
            task = update_task(task_id, data["description"],data["end_date"],data["start_date"],data["status"])
            if not task:
                # Return a 404 error if task does not exist
                tasks_ns.abort(404, f"task with ID {task_id} not found.")
            return task
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating task with ID {task_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error updating task with ID {task_id}: {e}")
            tasks_ns.abort(500, "An error occurred while updating the task.")

    @tasks_ns.doc('delete_task')
    @tasks_ns.response(204, 'task successfully deleted')
    def delete(self, task_id):
        """
        Delete a task by ID.
        :param task_id: The ID of the task
        :return: HTTP 204 status code if deleted successfully or 404 if not found
        """
        try:
            # Call the service to delete the task
            task = delete_task(task_id)
            if not task:
                # Return a 404 error if task does not exist
                tasks_ns.abort(404, f"task with ID {task_id} not found.")
            return '', 204  # Return no content with status code 204
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting task with ID {task_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error deleting task with ID {task_id}: {e}")
            tasks_ns.abort(500, "An error occurred while deleting the task.")