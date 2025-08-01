#!/usr/bin/env python3
"""
Production startup script for SmartMeetingAI
"""
import os
from app import app, db

if __name__ == '__main__':
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the application
    print("Starting SmartMeetingAI in production mode...")
    app.run(host='0.0.0.0', port=5001, debug=False) 