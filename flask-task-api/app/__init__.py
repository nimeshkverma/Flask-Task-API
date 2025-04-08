"""
Application initialization module for the Flask Task Management API.

This module contains the core application setup, including Flask extensions,
configuration loading, and blueprint registration.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from config import config

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
cors = CORS()

def create_app(config_name='default'):
    """
    Create and configure the Flask application.

    Args:
        config_name (str): Configuration name to use. Defaults to 'default'.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app, config={
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300
    })
    cors.init_app(app)
    
    # Import models
    from .models import user, task
    
    # Setup logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.task_routes import task_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(task_bp, url_prefix='/api/v1')

    return app