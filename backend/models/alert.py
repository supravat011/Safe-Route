"""Alert model"""
from database import Database
from utils.geolocation import get_bounding_box
from datetime import datetime, timedelta

class Alert:
    """Alert model for notifications"""
    
    @staticmethod
    def create(alert_type, severity, latitude, longitude, message, radius=5.0, accident_id=None, expires_hours=24):
        """
        Create a new alert
        
        Args:
            alert_type: Type of alert (accident, zone_warning, custom)
            severity: Severity level
            latitude: Alert latitude
            longitude: Alert longitude
            message: Alert message
            radius: Alert radius in km
            accident_id: Optional related accident ID
            expires_hours: Hours until alert expires
            
        Returns:
            Alert ID if successful, None otherwise
        """
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        query = """
            INSERT INTO alerts 
            (accident_id, alert_type, severity, latitude, longitude, radius, message, expires_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            alert_id = Database.execute_query(
                query,
                (accident_id, alert_type, severity, latitude, longitude, radius, message, expires_at),
                commit=True
            )
            return alert_id
        except Exception as e:
            print(f"Error creating alert: {e}")
            return None
    
    @staticmethod
    def get_active_alerts(latitude=None, longitude=None, radius=None):
        """
        Get active alerts, optionally filtered by location
        
        Args:
            latitude: User latitude
            longitude: User longitude
            radius: Search radius in km
            
        Returns:
            List of active alerts
        """
        query = """
            SELECT * FROM alerts
            WHERE is_active = TRUE
            AND (expires_at IS NULL OR expires_at > NOW())
        """
        params = []
        
        if all(v is not None for v in [latitude, longitude, radius]):
            min_lat, max_lat, min_lon, max_lon = get_bounding_box(latitude, longitude, radius)
            query += """ AND latitude BETWEEN %s AND %s 
                        AND longitude BETWEEN %s AND %s"""
            params.extend([min_lat, max_lat, min_lon, max_lon])
        
        query += " ORDER BY created_at DESC"
        
        return Database.execute_query(query, tuple(params), fetch_all=True) or []
    
    @staticmethod
    def get_by_id(alert_id):
        """Get alert by ID"""
        query = "SELECT * FROM alerts WHERE id = %s"
        return Database.execute_query(query, (alert_id,), fetch_one=True)
    
    @staticmethod
    def deactivate(alert_id):
        """Deactivate an alert"""
        query = "UPDATE alerts SET is_active = FALSE WHERE id = %s"
        try:
            Database.execute_query(query, (alert_id,), commit=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def cleanup_expired():
        """Deactivate expired alerts"""
        query = """
            UPDATE alerts 
            SET is_active = FALSE 
            WHERE expires_at IS NOT NULL 
            AND expires_at < NOW() 
            AND is_active = TRUE
        """
        try:
            Database.execute_query(query, commit=True)
            return True
        except Exception:
            return False
