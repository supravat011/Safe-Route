import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    """
    Configure application logging
    
    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set logging level
    app.logger.setLevel(logging.INFO)
    
    # File handler for general logs
    file_handler = RotatingFileHandler(
        'logs/safe_route.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(file_formatter)
    
    # File handler for errors
    error_handler = RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10240000,
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(console_handler)
    
    app.logger.info('SAFE ROUTE backend startup')

def get_logger(name):
    """
    Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
