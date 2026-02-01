"""Authentication routes"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from models.user import User
from utils.validators import validate_email_address, validate_password, validate_username, sanitize_input
from utils.response import success_response, error_response
from middleware.auth import token_required, get_current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['username', 'email', 'password']):
            return error_response("Missing required fields", 400)
        
        username = sanitize_input(data['username'], 50)
        email = sanitize_input(data['email'], 100)
        password = data['password']
        role = data.get('role', 'citizen')
        
        # Validate username
        is_valid, error = validate_username(username)
        if not is_valid:
            return error_response(error, 400)
        
        # Validate email
        is_valid, error = validate_email_address(email)
        if not is_valid:
            return error_response(error, 400)
        
        # Validate password
        is_valid, error = validate_password(password)
        if not is_valid:
            return error_response(error, 400)
        
        # Validate role
        if role not in ['citizen', 'admin', 'authority']:
            return error_response("Invalid role", 400)
        
        # Check if user already exists
        if User.find_by_email(email):
            return error_response("Email already registered", 400)
        
        if User.find_by_username(username):
            return error_response("Username already taken", 400)
        
        # Create user
        user_id = User.create(username, email, password, role)
        
        if not user_id:
            return error_response("Failed to create user", 500)
        
        return success_response(
            {"user_id": user_id, "username": username, "email": email, "role": role},
            "User registered successfully",
            201
        )
        
    except Exception as e:
        return error_response(f"Registration failed: {str(e)}", 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['email', 'password']):
            return error_response("Missing email or password", 400)
        
        email = sanitize_input(data['email'], 100)
        password = data['password']
        
        # Authenticate user
        user = User.authenticate(email, password)
        
        if not user:
            return error_response("Invalid email or password", 401)
        
        # Create JWT token with user info
        additional_claims = {
            "role": user['role'],
            "username": user['username']
        }
        
        access_token = create_access_token(
            identity=user['id'],
            additional_claims=additional_claims
        )
        
        return success_response({
            "access_token": access_token,
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role']
            }
        }, "Login successful")
        
    except Exception as e:
        return error_response(f"Login failed: {str(e)}", 500)

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_current_user()
        user = User.find_by_id(user_id)
        
        if not user:
            return error_response("User not found", 404)
        
        return success_response(user, "Profile retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get profile: {str(e)}", 500)
