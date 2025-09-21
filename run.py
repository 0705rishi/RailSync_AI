#!/usr/bin/env python3
"""
RailSync AI - Railway Traffic Control System
SIH 2025 Entry Point

Run this file to start the application
"""

import os
from app import app
from config import config

if __name__ == '__main__':
    # Load configuration
    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Run application
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', True)
    )