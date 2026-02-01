"""Authentication middleware"""
from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from utils.response import error_response

def token_required(fn):
    """
    Decorator to require valid JWT token
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return error_response("Invalid or missing token", 401)
    
    return wrapper

def role_required(*allowed_roles):
    """
    Decorator to require specific user role(s)
    
    Usage:
        @role_required('admin')
        @role_required('admin', 'authority')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_role = claims.get('role', 'citizen')
                
                if user_role not in allowed_roles:
                    return error_response(
                        "Insufficient permissions",
                        403
                    )
                
                return fn(*args, **kwargs)
            except Exception as e:
                return error_response("Invalid or missing token", 401)
        
        return wrapper
    return decorator

def get_current_user():
    """
    Get current user ID from JWT token
    
    Returns:
        User ID or None
    """
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception:
        return None

def get_current_user_role():
    """
    Get current user role from JWT token
    
    Returns:
        User role or None
    """
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        return claims.get('role', 'citizen')
    except Exception:
        return None
