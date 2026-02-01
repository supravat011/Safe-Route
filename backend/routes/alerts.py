"""Alert routes"""
from flask import Blueprint, request
from models.alert import Alert
from utils.response import success_response, error_response
from middleware.auth import token_required, role_required

alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@alerts_bp.route('', methods=['GET'])
def get_alerts():
    """Get active alerts"""
    try:
        # Optional location filtering
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius', 10)
        
        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                radius = float(radius)
                alerts = Alert.get_active_alerts(latitude, longitude, radius)
            except ValueError:
                return error_response("Invalid location parameters", 400)
        else:
            alerts = Alert.get_active_alerts()
        
        return success_response(alerts, "Alerts retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get alerts: {str(e)}", 500)

@alerts_bp.route('/nearby', methods=['GET'])
def get_nearby_alerts():
    """Get alerts near a specific location"""
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius', 5)
        
        if not latitude or not longitude:
            return error_response("Missing latitude or longitude", 400)
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
        except ValueError:
            return error_response("Invalid location parameters", 400)
        
        alerts = Alert.get_active_alerts(latitude, longitude, radius)
        
        return success_response(alerts, f"Found {len(alerts)} alerts nearby")
        
    except Exception as e:
        return error_response(f"Failed to get nearby alerts: {str(e)}", 500)

@alerts_bp.route('/create', methods=['POST'])
@role_required('admin', 'authority')
def create_alert():
    """Create a custom alert (admin/authority only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['alert_type', 'severity', 'latitude', 'longitude', 'message']
        if not all(k in data for k in required):
            return error_response("Missing required fields", 400)
        
        alert_id = Alert.create(
            alert_type=data['alert_type'],
            severity=data['severity'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            message=data['message'],
            radius=float(data.get('radius', 5.0)),
            expires_hours=int(data.get('expires_hours', 24))
        )
        
        if not alert_id:
            return error_response("Failed to create alert", 500)
        
        return success_response(
            {"alert_id": alert_id},
            "Alert created successfully",
            201
        )
        
    except Exception as e:
        return error_response(f"Failed to create alert: {str(e)}", 500)

@alerts_bp.route('/<int:alert_id>/dismiss', methods=['PUT'])
@role_required('admin', 'authority')
def dismiss_alert(alert_id):
    """Dismiss/deactivate an alert (admin/authority only)"""
    try:
        success = Alert.deactivate(alert_id)
        
        if not success:
            return error_response("Failed to dismiss alert", 500)
        
        return success_response(None, "Alert dismissed successfully")
        
    except Exception as e:
        return error_response(f"Failed to dismiss alert: {str(e)}", 500)
