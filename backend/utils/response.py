from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """
    Create a standardized success response
    
    Args:
        data: Response data (dict, list, or None)
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Flask response object
    """
    response = {
        "success": True,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        errors: Additional error details (dict or list)
        
    Returns:
        Flask response object
    """
    response = {
        "success": False,
        "message": message
    }
    
    if errors:
        response["errors"] = errors
    
    return jsonify(response), status_code

def paginated_response(items, page, page_size, total_count, message="Success"):
    """
    Create a paginated response
    
    Args:
        items: List of items for current page
        page: Current page number
        page_size: Items per page
        total_count: Total number of items
        message: Success message
        
    Returns:
        Flask response object
    """
    total_pages = (total_count + page_size - 1) // page_size
    
    response = {
        "success": True,
        "message": message,
        "data": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
    
    return jsonify(response), 200

def get_pagination_params(request, default_page=1, default_size=20, max_size=100):
    """
    Extract and validate pagination parameters from request
    
    Args:
        request: Flask request object
        default_page: Default page number
        default_size: Default page size
        max_size: Maximum allowed page size
        
    Returns:
        Tuple of (page, page_size, offset)
    """
    try:
        page = int(request.args.get('page', default_page))
        page_size = int(request.args.get('page_size', default_size))
        
        # Validate
        page = max(1, page)
        page_size = min(max(1, page_size), max_size)
        
        offset = (page - 1) * page_size
        
        return page, page_size, offset
        
    except (ValueError, TypeError):
        return default_page, default_size, 0
