"""Accident reporting routes"""
from flask import Blueprint, request
from models.accident import Accident
from models.alert import Alert
from utils.validators import validate_enum, sanitize_input
from utils.geolocation import validate_coordinates
from utils.file_handler import save_uploaded_file, get_file_url
from utils.response import success_response, error_response, paginated_response, get_pagination_params
from middleware.auth import token_required, role_required, get_current_user
from datetime import datetime

accidents_bp = Blueprint('accidents', __name__, url_prefix='/api/accidents')

@accidents_bp.route('/report', methods=['POST'])
@token_required
def report_accident():
    """Submit a new accident report"""
    try:
        user_id = get_current_user()
        
        # Get form data
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        accident_type = request.form.get('accident_type')
        severity = request.form.get('severity')
        description = request.form.get('description', '')
        
        # Validate required fields
        if not all([latitude, longitude, accident_type, severity]):
            return error_response("Missing required fields", 400)
        
        # Validate coordinates
        is_valid, error = validate_coordinates(latitude, longitude)
        if not is_valid:
            return error_response(error, 400)
        
        latitude = float(latitude)
        longitude = float(longitude)
        
        # Validate accident type
        valid_types = ['collision', 'fire', 'injury', 'pedestrian', 'vehicle_breakdown', 'other']
        is_valid, error = validate_enum(accident_type, valid_types, "Accident type")
        if not is_valid:
            return error_response(error, 400)
        
        # Validate severity
        valid_severities = ['low', 'medium', 'high']
        is_valid, error = validate_enum(severity, valid_severities, "Severity")
        if not is_valid:
            return error_response(error, 400)
        
        # Sanitize description
        description = sanitize_input(description, 1000)
        
        # Check for duplicate
        if Accident.check_duplicate(user_id, latitude, longitude):
            return error_response("Similar accident already reported recently", 400)
        
        # Handle image upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                success, result = save_uploaded_file(file, 'accidents')
                if success:
                    image_path = result
                else:
                    return error_response(f"Image upload failed: {result}", 400)
        
        # Create accident report
        accident_id = Accident.create(
            user_id, latitude, longitude,
            accident_type, severity, description, image_path
        )
        
        if not accident_id:
            return error_response("Failed to create accident report", 500)
        
        # Create alert for high severity accidents
        if severity == 'high':
            Alert.create(
                alert_type='accident',
                severity=severity,
                latitude=latitude,
                longitude=longitude,
                message=f"High severity {accident_type} reported in your area",
                radius=5.0,
                accident_id=accident_id,
                expires_hours=24
            )
        
        return success_response({
            "accident_id": accident_id,
            "image_url": get_file_url(image_path) if image_path else None
        }, "Accident reported successfully", 201)
        
    except Exception as e:
        return error_response(f"Failed to report accident: {str(e)}", 500)

@accidents_bp.route('/live', methods=['GET'])
def get_live_accidents():
    """Get live accident data with filters"""
    try:
        # Get pagination params
        page, page_size, offset = get_pagination_params(request)
        
        # Build filters
        filters = {}
        
        if request.args.get('severity'):
            severity = request.args.get('severity')
            if severity in ['low', 'medium', 'high']:
                filters['severity'] = severity
        
        if request.args.get('accident_type'):
            filters['accident_type'] = request.args.get('accident_type')
        
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        
        if request.args.get('start_date'):
            filters['start_date'] = request.args.get('start_date')
        
        if request.args.get('end_date'):
            filters['end_date'] = request.args.get('end_date')
        
        # Location filter
        if all(request.args.get(k) for k in ['latitude', 'longitude', 'radius']):
            try:
                filters['latitude'] = float(request.args.get('latitude'))
                filters['longitude'] = float(request.args.get('longitude'))
                filters['radius'] = float(request.args.get('radius'))
            except ValueError:
                return error_response("Invalid location parameters", 400)
        
        # Get accidents
        accidents = Accident.get_all(filters, limit=page_size, offset=offset)
        total_count = Accident.count(filters)
        
        # Add image URLs
        for accident in accidents:
            if accident.get('image_path'):
                accident['image_url'] = get_file_url(accident['image_path'])
        
        return paginated_response(
            accidents, page, page_size, total_count,
            "Accidents retrieved successfully"
        )
        
    except Exception as e:
        return error_response(f"Failed to get accidents: {str(e)}", 500)

@accidents_bp.route('/<int:accident_id>', methods=['GET'])
def get_accident(accident_id):
    """Get specific accident details"""
    try:
        accident = Accident.find_by_id(accident_id)
        
        if not accident:
            return error_response("Accident not found", 404)
        
        if accident.get('image_path'):
            accident['image_url'] = get_file_url(accident['image_path'])
        
        return success_response(accident, "Accident retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get accident: {str(e)}", 500)

@accidents_bp.route('/<int:accident_id>/status', methods=['PUT'])
@role_required('admin', 'authority')
def update_accident_status(accident_id):
    """Update accident status (admin/authority only)"""
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return error_response("Missing status field", 400)
        
        status = data['status']
        valid_statuses = ['reported', 'verified', 'resolved']
        
        if status not in valid_statuses:
            return error_response(f"Invalid status. Must be one of: {', '.join(valid_statuses)}", 400)
        
        success = Accident.update_status(accident_id, status)
        
        if not success:
            return error_response("Failed to update accident status", 500)
        
        return success_response(None, "Accident status updated successfully")
        
    except Exception as e:
        return error_response(f"Failed to update status: {str(e)}", 500)

@accidents_bp.route('/<int:accident_id>', methods=['DELETE'])
@role_required('admin')
def delete_accident(accident_id):
    """Delete an accident (admin only)"""
    try:
        success = Accident.delete(accident_id)
        
        if not success:
            return error_response("Failed to delete accident", 500)
        
        return success_response(None, "Accident deleted successfully")
        
    except Exception as e:
        return error_response(f"Failed to delete accident: {str(e)}", 500)
