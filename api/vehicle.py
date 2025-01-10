import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.vehicle_service import (
    get_all_vehicles,
    get_vehicle,
    create_vehicle,
    update_vehicle,
    delete_vehicle
)
from utils.utils import generate_swagger_model
from models.vehicle import Vehicle

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing vehicles
vehicles_ns = Namespace('vehicle', description='CRUD operations for managing vehicles')

# Generate the Swagger model for the vehicle resource
vehicle_model = generate_swagger_model(
    api=vehicles_ns,        # Namespace to associate with the model
    model=Vehicle,          # SQLAlchemy model representing the vehicle resource
    exclude_fields=[],     # No excluded fields in this model
    readonly_fields=['vehicle_id']  # Fields that cannot be modified
)

@vehicles_ns.route('/')
class VehicleList(Resource):
    """
    Handles operations on the collection of vehicles.
    Supports retrieving all vehicles (GET) and creating new vehicles (POST).
    """

    @vehicles_ns.doc('get_all_vehicles')
    @vehicles_ns.marshal_list_with(vehicle_model)
    def get(self):
        """
        Retrieve all vehicles.
        :return: List of all vehicles
        """
        try:
            # Fetch all vehicles from the service layer
            return get_all_vehicles()
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving vehicles: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving vehicles: {e}")
            vehicles_ns.abort(500, "An error occurred while retrieving the vehicles.")

    @vehicles_ns.doc('create_vehicle')
    @vehicles_ns.expect(vehicle_model, validate=True)
    @vehicles_ns.marshal_with(vehicle_model, code=201)
    def post(self):
        """
        Create a new vehicle.
        :return: The newly created vehicle
        """
        try:
            # Parse the request payload and create a new vehicle
            payload = vehicles_ns.payload
            brand = payload.get('brand')
            client_id = payload.get('client_id')
            license_plate = payload.get('license_plate')
            model = payload.get('model')
            year = payload.get('year')
            return create_vehicle(brand, client_id, license_plate, model, year), 201
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while creating a vehicle: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error creating a vehicle: {e}")
            vehicles_ns.abort(500, "An error occurred while creating the vehicle.")

@vehicles_ns.route('/<int:vehicle_id>')
@vehicles_ns.param('vehicle_id', 'The ID of the vehicle')
class Vehicle(Resource):
    """
    Handles operations on a single vehicle.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) a vehicle.
    """

    @vehicles_ns.doc('get_vehicle')
    @vehicles_ns.marshal_with(vehicle_model)
    def get(self, vehicle_id):
        """
        Retrieve a vehicle by ID.
        :param vehicle_id: The ID of the vehicle to retrieve.
        :return: The vehicle with the specified ID
        """
        try:
            # Fetch the vehicle with the specified ID
            vehicle = get_vehicle(vehicle_id)
            if vehicle is None:
                vehicles_ns.abort(404, f"Vehicle with ID {vehicle_id} not found")
            return vehicle
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving vehicle {vehicle_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving vehicle {vehicle_id}: {e}")
            vehicles_ns.abort(500, "An error occurred while retrieving the vehicle.")

    @vehicles_ns.doc('update_vehicle')
    @vehicles_ns.expect(vehicle_model, validate=True)
    @vehicles_ns.marshal_with(vehicle_model)
    def put(self, vehicle_id):
        """
        Update a vehicle by ID.
        :param vehicle_id: The ID of the vehicle to update.
        :return: The updated vehicle
        """
        try:
            # Parse the request payload and update the vehicle
            payload = vehicles_ns.payload
            brand = payload.get('brand')
            client_id = payload.get('client_id')
            license_plate = payload.get('license_plate')
            model = payload.get('model')
            year = payload.get('year')
            return update_vehicle(vehicle_id, brand, client_id, license_plate, model, year)
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while updating vehicle {vehicle_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error updating vehicle {vehicle_id}: {e}")
            vehicles_ns.abort(500, "An error occurred while updating the vehicle.")
    @vehicles_ns.doc('delete_vehicle')
    @vehicles_ns.response(204, 'Vehicle deleted successfully')
    def delete(self, vehicle_id):
        """
        Delete a vehicle by ID.
        :param vehicle_id: The ID of the vehicle to delete.
        :return: 204 No Content
        """
        try:
            # Delete the vehicle with the specified ID
            delete_vehicle(vehicle_id)
            return '', 204
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while deleting vehicle {vehicle_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error deleting vehicle {vehicle_id}: {e}")
            vehicles_ns.abort(500, "An error occurred while deleting the vehicle.")