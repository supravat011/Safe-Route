import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def is_within_radius(lat1, lon1, lat2, lon2, radius_km):
    """
    Check if two coordinates are within a given radius
    
    Args:
        lat1, lon1: First coordinate
        lat2, lon2: Second coordinate
        radius_km: Radius in kilometers
        
    Returns:
        Boolean indicating if points are within radius
    """
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return distance <= radius_km

def validate_coordinates(latitude, longitude):
    """
    Validate latitude and longitude values
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if lat < -90 or lat > 90:
            return False, "Latitude must be between -90 and 90"
        
        if lon < -180 or lon > 180:
            return False, "Longitude must be between -180 and 180"
        
        return True, None
        
    except (ValueError, TypeError):
        return False, "Invalid coordinate format"

def get_bounding_box(latitude, longitude, radius_km):
    """
    Calculate bounding box for a given point and radius
    Useful for optimizing database queries
    
    Returns:
        Tuple of (min_lat, max_lat, min_lon, max_lon)
    """
    # Approximate degrees per kilometer
    lat_degree_km = 111.0
    lon_degree_km = 111.0 * math.cos(math.radians(latitude))
    
    lat_offset = radius_km / lat_degree_km
    lon_offset = radius_km / lon_degree_km
    
    return (
        latitude - lat_offset,   # min_lat
        latitude + lat_offset,   # max_lat
        longitude - lon_offset,  # min_lon
        longitude + lon_offset   # max_lon
    )

def format_distance(distance_km):
    """
    Format distance for display
    
    Returns:
        String with formatted distance
    """
    if distance_km < 1:
        return f"{int(distance_km * 1000)} meters"
    else:
        return f"{distance_km:.2f} km"
