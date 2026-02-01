import re
from email_validator import validate_email, EmailNotValidError

def validate_password(password):
    """
    Validate password strength
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None

def validate_email_address(email):
    """
    Validate email address format
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Validate and normalize
        valid = validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def validate_username(username):
    """
    Validate username
    
    Requirements:
    - 3-50 characters
    - Alphanumeric and underscores only
    - Must start with a letter
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(username) < 3 or len(username) > 50:
        return False, "Username must be between 3 and 50 characters"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Username must start with a letter and contain only letters, numbers, and underscores"
    
    return True, None

def validate_enum(value, allowed_values, field_name="Field"):
    """
    Validate enum value
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if value not in allowed_values:
        return False, f"{field_name} must be one of: {', '.join(allowed_values)}"
    
    return True, None

def sanitize_input(text, max_length=None):
    """
    Sanitize user input to prevent XSS
    
    Returns:
        Sanitized text
    """
    if not text:
        return text
    
    # Remove potentially dangerous characters
    sanitized = text.strip()
    
    # Limit length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized

def validate_phone(phone):
    """
    Validate phone number format
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Basic phone validation (international format)
    pattern = r'^\+?[1-9]\d{1,14}$'
    
    if not re.match(pattern, phone):
        return False, "Invalid phone number format"
    
    return True, None
