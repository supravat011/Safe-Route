"""Main Flask application"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

from config import config
from database import Database
from utils.logger import setup_logger

# Import blueprints
from routes.auth import auth_bp
from routes.accidents import accidents_bp
from routes.alerts import alerts_bp
from routes.emergency import emergency_bp
from routes.awareness import awareness_bp
from routes.admin import admin_bp
from routes.export import export_bp
from routes.stats import stats_bp
from routes.backup import backup_bp

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Setup logging
    setup_logger(app)
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    jwt = JWTManager(app)
    
    # Rate limiting
    if app.config['RATE_LIMIT_ENABLED']:
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=[app.config['RATE_LIMIT_DEFAULT']]
        )
    
    # Initialize database connection pool
    try:
        Database.init_pool()
        app.logger.info("Database connection pool initialized")
    except Exception as e:
        app.logger.error(f"Failed to initialize database: {e}")
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(accidents_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(emergency_bp)
    app.register_blueprint(awareness_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(backup_bp)
    
    # Serve uploaded files
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Serve uploaded files"""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        db_status = Database.test_connection()
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database": "connected" if db_status else "disconnected"
        }, 200 if db_status else 503
    
    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint"""
        return {
            "message": "SAFE ROUTE API",
            "version": "1.0.0",
            "status": "running"
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"success": False, "message": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal error: {error}")
        return {"success": False, "message": "Internal server error"}, 500
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return {"success": False, "message": "Rate limit exceeded"}, 429
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'accidents'), exist_ok=True)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
