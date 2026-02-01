"""User model"""
from database import Database
from utils.security import hash_password, verify_password
from datetime import datetime

class User:
    """User model for authentication and authorization"""
    
    @staticmethod
    def create(username, email, password, role='citizen'):
        """
        Create a new user
        
        Args:
            username: Unique username
            email: User email
            password: Plain text password (will be hashed)
            role: User role (citizen, admin, authority)
            
        Returns:
            User ID if successful, None otherwise
        """
        password_hash = hash_password(password)
        
        query = """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            user_id = Database.execute_query(
                query,
                (username, email, password_hash, role),
                commit=True
            )
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        return Database.execute_query(query, (email,), fetch_one=True)
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        return Database.execute_query(query, (username,), fetch_one=True)
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        query = "SELECT id, username, email, role, created_at FROM users WHERE id = %s"
        return Database.execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def authenticate(email, password):
        """
        Authenticate user with email and password
        
        Returns:
            User dict if successful, None otherwise
        """
        user = User.find_by_email(email)
        
        if user and verify_password(password, user['password_hash']):
            # Remove password hash from returned user
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'created_at': user['created_at']
            }
            return user_data
        
        return None
    
    @staticmethod
    def update(user_id, **kwargs):
        """
        Update user fields
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
        """
        allowed_fields = ['username', 'email', 'role']
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        
        try:
            Database.execute_query(query, tuple(values), commit=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_all(role=None):
        """Get all users, optionally filtered by role"""
        if role:
            query = "SELECT id, username, email, role, created_at FROM users WHERE role = %s"
            return Database.execute_query(query, (role,), fetch_all=True)
        else:
            query = "SELECT id, username, email, role, created_at FROM users"
            return Database.execute_query(query, fetch_all=True)
