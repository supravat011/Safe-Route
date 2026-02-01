"""Accident model"""
from database import Database
from utils.geolocation import get_bounding_box
from datetime import datetime

class Accident:
    """Accident report model"""
    
    @staticmethod
    def create(user_id, latitude, longitude, accident_type, severity, description=None, image_path=None):
        """
        Create a new accident report
        
        Args:
            user_id: ID of user reporting the accident
            latitude: Accident latitude
            longitude: Accident longitude
            accident_type: Type of accident
            severity: Severity level
            description: Optional description
            image_path: Optional image path
            
        Returns:
            Accident ID if successful, None otherwise
        """
        query = """
            INSERT INTO accidents 
            (user_id, latitude, longitude, accident_type, severity, description, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            accident_id = Database.execute_query(
                query,
                (user_id, latitude, longitude, accident_type, severity, description, image_path),
                commit=True
            )
            return accident_id
        except Exception as e:
            print(f"Error creating accident: {e}")
            return None
    
    @staticmethod
    def find_by_id(accident_id):
        """Find accident by ID"""
        query = """
            SELECT a.*, u.username, u.email
            FROM accidents a
            JOIN users u ON a.user_id = u.id
            WHERE a.id = %s
        """
        return Database.execute_query(query, (accident_id,), fetch_one=True)
    
    @staticmethod
    def get_all(filters=None, limit=100, offset=0):
        """
        Get all accidents with optional filters
        
        Args:
            filters: Dict with optional keys: severity, accident_type, status, 
                    start_date, end_date, latitude, longitude, radius
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of accidents
        """
        query = """
            SELECT a.*, u.username
            FROM accidents a
            JOIN users u ON a.user_id = u.id
            WHERE 1=1
        """
        params = []
        
        if filters:
            # Severity filter
            if 'severity' in filters:
                query += " AND a.severity = %s"
                params.append(filters['severity'])
            
            # Type filter
            if 'accident_type' in filters:
                query += " AND a.accident_type = %s"
                params.append(filters['accident_type'])
            
            # Status filter
            if 'status' in filters:
                query += " AND a.status = %s"
                params.append(filters['status'])
            
            # Date range filter
            if 'start_date' in filters:
                query += " AND a.timestamp >= %s"
                params.append(filters['start_date'])
            
            if 'end_date' in filters:
                query += " AND a.timestamp <= %s"
                params.append(filters['end_date'])
            
            # Location filter (bounding box for efficiency)
            if all(k in filters for k in ['latitude', 'longitude', 'radius']):
                min_lat, max_lat, min_lon, max_lon = get_bounding_box(
                    filters['latitude'],
                    filters['longitude'],
                    filters['radius']
                )
                query += """ AND a.latitude BETWEEN %s AND %s 
                            AND a.longitude BETWEEN %s AND %s"""
                params.extend([min_lat, max_lat, min_lon, max_lon])
        
        query += " ORDER BY a.timestamp DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        return Database.execute_query(query, tuple(params), fetch_all=True) or []
    
    @staticmethod
    def count(filters=None):
        """Count accidents with optional filters"""
        query = "SELECT COUNT(*) as count FROM accidents WHERE 1=1"
        params = []
        
        if filters:
            if 'severity' in filters:
                query += " AND severity = %s"
                params.append(filters['severity'])
            
            if 'accident_type' in filters:
                query += " AND accident_type = %s"
                params.append(filters['accident_type'])
            
            if 'status' in filters:
                query += " AND status = %s"
                params.append(filters['status'])
            
            if 'start_date' in filters:
                query += " AND timestamp >= %s"
                params.append(filters['start_date'])
            
            if 'end_date' in filters:
                query += " AND timestamp <= %s"
                params.append(filters['end_date'])
        
        result = Database.execute_query(query, tuple(params), fetch_one=True)
        return result['count'] if result else 0
    
    @staticmethod
    def update_status(accident_id, status):
        """Update accident status"""
        query = "UPDATE accidents SET status = %s WHERE id = %s"
        try:
            Database.execute_query(query, (status, accident_id), commit=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete(accident_id):
        """Delete an accident"""
        query = "DELETE FROM accidents WHERE id = %s"
        try:
            Database.execute_query(query, (accident_id,), commit=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def check_duplicate(user_id, latitude, longitude, time_window_minutes=30):
        """
        Check for duplicate accident reports
        
        Args:
            user_id: User ID
            latitude: Accident latitude
            longitude: Accident longitude
            time_window_minutes: Time window to check for duplicates
            
        Returns:
            True if duplicate found, False otherwise
        """
        query = """
            SELECT COUNT(*) as count
            FROM accidents
            WHERE user_id = %s
            AND latitude BETWEEN %s AND %s
            AND longitude BETWEEN %s AND %s
            AND timestamp >= DATE_SUB(NOW(), INTERVAL %s MINUTE)
        """
        
        # Small bounding box (0.01 degrees ~ 1km)
        lat_offset = 0.01
        lon_offset = 0.01
        
        result = Database.execute_query(
            query,
            (user_id, 
             latitude - lat_offset, latitude + lat_offset,
             longitude - lon_offset, longitude + lon_offset,
             time_window_minutes),
            fetch_one=True
        )
        
        return result['count'] > 0 if result else False
