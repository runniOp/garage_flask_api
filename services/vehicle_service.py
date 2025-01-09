import logging
from utils.database import db
from models.vehicle import Vehicle

logger = logging.getLogger(__name__)

def get_all_vehicles():
    """
    Retrieve all vehicles.
    :return: list: A list of dictionaries containing information about all vehicles.
    """
    try:
        vehicles = Vehicle.query.all()  # Retrieve all vehicles from the database
        return [
            {
                "vehicle_id": vehicle.vehicle_id,
                "brand": vehicle.brand,
                "client_id": vehicle.client_id,
                "created_at": vehicle.created_at,
                "license_plate": vehicle.license_plate,
                "model": vehicle.model,
                "year": vehicle.year,
            }
            for vehicle in vehicles
        ]
    except Exception as e:
        logger.error(f"Error fetching all vehicles: {e}")
        return {"error": "Internal Server Error"}
    

def get_vehicle(vehicle_id):
    """
    Retrieve a vehicle by ID.
    :param vehicle_id: The ID of the vehicle to retrieve.
    :return: dict: A dictionary containing the vehicle's information or an error message.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None
        return {
            "vehicle_id": vehicle.vehicle_id,
            "brand": vehicle.brand,
            "client_id": vehicle.client_id,
            "created_at": vehicle.created_at,
            "license_plate": vehicle.license_plate,
            "model": vehicle.model,
            "year": vehicle.year,
        }
    except Exception as e:
        logger.error(f"Error fetching vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}
    
def create_vehicle(brand, client_id, license_plate, model, year):
    """
    Create a new vehicle.
    :param brand: The brand of the vehicle.
    :param client_id: The ID of the client who owns the vehicle.
    :param license_plate: The license plate of the vehicle.
    :param model: The model of the vehicle.
    :param year: The year of the vehicle.
    :return: tuple: A dictionary containing the newly created vehicle's information and the HTTP status code.
    """
    try:
        vehicle = Vehicle(brand=brand, client_id=client_id, license_plate=license_plate, model=model, year=year)
        db.session.add(vehicle)
        db.session.commit()
        return {
            "vehicle_id": vehicle.vehicle_id,
            "brand": vehicle.brand,
            "client_id": vehicle.client_id,
            "created_at": vehicle.created_at,
            "license_plate": vehicle.license_plate,
            "model": vehicle.model,
            "year": vehicle.year,
        }, 201
    except Exception as e:
        logger.error(f"Error creating vehicle: {e}")
        return {"error": "Internal Server Error"}
    
def update_vehicle(vehicle_id, brand, client_id, license_plate, model, year):
    """
    Update a vehicle.
    :param vehicle_id: The ID of the vehicle to update.
    :param brand: The brand of the vehicle.
    :param client_id: The ID of the client who owns the vehicle.
    :param license_plate: The license plate of the vehicle.
    :param model: The model of the vehicle.
    :param year: The year of the vehicle.
    :return: dict: A dictionary containing the updated vehicle's information or an error message.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None
        vehicle.brand = brand
        vehicle.client_id = client_id
        vehicle.license_plate = license_plate
        vehicle.model = model
        vehicle.year = year
        db.session.commit()
        return {
            "vehicle_id": vehicle.vehicle_id,
            "brand": vehicle.brand,
            "client_id": vehicle.client_id,
            "created_at": vehicle.created_at,
            "license_plate": vehicle.license_plate,
            "model": vehicle.model,
            "year": vehicle.year,
        }
    except Exception as e:
        logger.error(f"Error updating vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_vehicle(vehicle_id):
    """
    Delete a vehicle.
    :param vehicle_id: The ID of the vehicle to delete.
    :return: dict: A message indicating success or an error message.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None
        db.session.delete(vehicle)
        db.session.commit()
        return {"message": "Vehicle deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}
    
