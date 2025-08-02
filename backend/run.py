#!/usr/bin/env python3
"""
SmartMeetingAI Backend Startup Script
"""
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, db

if __name__ == '__main__':
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the application
    print("Starting SmartMeetingAI in production mode...")
    print("Access the application at: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False) 