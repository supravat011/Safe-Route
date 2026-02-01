"""Emergency services model"""
from database import Database
from utils.geolocation import get_bounding_box, haversine_distance

class EmergencyService:
    """Emergency services model (hospitals, police, ambulance)"""
    
    @staticmethod
    def create(name, service_type, latitude, longitude, address=None, phone=None):
        """Create a new emergency service"""
        query = """
            INSERT INTO emergency_services 
            (name, type, latitude, longitude, address, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            service_id = Database.execute_query(
                query,
                (name, service_type, latitude, longitude, address, phone),
                commit=True
            )
            return service_id
        except Exception as e:
            print(f"Error creating emergency service: {e}")
            return None
    
    @staticmethod
    def find_nearby(latitude, longitude, radius_km=10, service_type=None):
        """
        Find nearby emergency services
        
        Args:
            latitude: User latitude
            longitude: User longitude
            radius_km: Search radius in kilometers
            service_type: Optional filter by type (hospital, police, ambulance)
            
        Returns:
            List of nearby services with distances
        """
        # Use bounding box for initial filtering
        min_lat, max_lat, min_lon, max_lon = get_bounding_box(latitude, longitude, radius_km)
        
        query = """
            SELECT * FROM emergency_services
            WHERE is_active = TRUE
            AND latitude BETWEEN %s AND %s
            AND longitude BETWEEN %s AND %s
        """
        params = [min_lat, max_lat, min_lon, max_lon]
        
        if service_type:
            query += " AND type = %s"
            params.append(service_type)
        
        services = Database.execute_query(query, tuple(params), fetch_all=True) or []
        
        # Calculate exact distances and filter by radius
        results = []
        for service in services:
            distance = haversine_distance(
                latitude, longitude,
                float(service['latitude']), float(service['longitude'])
            )
            
            if distance <= radius_km:
                service['distance_km'] = round(distance, 2)
                results.append(service)
        
        # Sort by distance
        results.sort(key=lambda x: x['distance_km'])
        
        return results
    
    @staticmethod
    def get_all(service_type=None):
        """Get all emergency services"""
        if service_type:
            query = "SELECT * FROM emergency_services WHERE type = %s AND is_active = TRUE"
            return Database.execute_query(query, (service_type,), fetch_all=True) or []
        else:
            query = "SELECT * FROM emergency_services WHERE is_active = TRUE"
            return Database.execute_query(query, fetch_all=True) or []
    
    @staticmethod
    def update(service_id, **kwargs):
        """Update emergency service"""
        allowed_fields = ['name', 'type', 'latitude', 'longitude', 'address', 'phone', 'is_active']
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(service_id)
        query = f"UPDATE emergency_services SET {', '.join(updates)} WHERE id = %s"
        
        try:
            Database.execute_query(query, tuple(values), commit=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete(service_id):
        """Delete emergency service"""
        query = "DELETE FROM emergency_services WHERE id = %s"
        try:
            Database.execute_query(query, (service_id,), commit=True)
            return True
        except Exception:
            return False
