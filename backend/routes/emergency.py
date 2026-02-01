"""Emergency services routes"""
from flask import Blueprint, request
from models.emergency_service import EmergencyService
from utils.response import success_response, error_response
from middleware.auth import role_required

emergency_bp = Blueprint('emergency', __name__, url_prefix='/api/emergency')

@emergency_bp.route('/nearby', methods=['GET'])
def get_nearby_services():
    """Get all nearby emergency services"""
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius', 10)
        
        if not latitude or not longitude:
            return error_response("Missing latitude or longitude", 400)
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
        except ValueError:
            return error_response("Invalid location parameters", 400)
        
        services = EmergencyService.find_nearby(latitude, longitude, radius)
        
        return success_response(services, f"Found {len(services)} emergency services nearby")
        
    except Exception as e:
        return error_response(f"Failed to get emergency services: {str(e)}", 500)

@emergency_bp.route('/hospitals', methods=['GET'])
def get_nearby_hospitals():
    """Get nearby hospitals"""
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius', 10)
        
        if not latitude or not longitude:
            return error_response("Missing latitude or longitude", 400)
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
        except ValueError:
            return error_response("Invalid location parameters", 400)
        
        hospitals = EmergencyService.find_nearby(latitude, longitude, radius, 'hospital')
        
        return success_response(hospitals, f"Found {len(hospitals)} hospitals nearby")
        
    except Exception as e:
        return error_response(f"Failed to get hospitals: {str(e)}", 500)

@emergency_bp.route('/police', methods=['GET'])
def get_nearby_police():
    """Get nearby police stations"""
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius', 10)
        
        if not latitude or not longitude:
            return error_response("Missing latitude or longitude", 400)
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
        except ValueError:
            return error_response("Invalid location parameters", 400)
        
        police = EmergencyService.find_nearby(latitude, longitude, radius, 'police')
        
        return success_response(police, f"Found {len(police)} police stations nearby")
        
    except Exception as e:
        return error_response(f"Failed to get police stations: {str(e)}", 500)

@emergency_bp.route('/ambulance', methods=['GET'])
def get_ambulance_services():
    """Get ambulance services"""
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius', 10)
        
        if not latitude or not longitude:
            return error_response("Missing latitude or longitude", 400)
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
        except ValueError:
            return error_response("Invalid location parameters", 400)
        
        ambulances = EmergencyService.find_nearby(latitude, longitude, radius, 'ambulance')
        
        return success_response(ambulances, f"Found {len(ambulances)} ambulance services nearby")
        
    except Exception as e:
        return error_response(f"Failed to get ambulance services: {str(e)}", 500)

@emergency_bp.route('/add', methods=['POST'])
@role_required('admin')
def add_emergency_service():
    """Add a new emergency service (admin only)"""
    try:
        data = request.get_json()
        
        required = ['name', 'type', 'latitude', 'longitude']
        if not all(k in data for k in required):
            return error_response("Missing required fields", 400)
        
        service_id = EmergencyService.create(
            name=data['name'],
            service_type=data['type'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            address=data.get('address'),
            phone=data.get('phone')
        )
        
        if not service_id:
            return error_response("Failed to add emergency service", 500)
        
        return success_response(
            {"service_id": service_id},
            "Emergency service added successfully",
            201
        )
        
    except Exception as e:
        return error_response(f"Failed to add emergency service: {str(e)}", 500)
