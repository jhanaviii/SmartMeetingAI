#!/usr/bin/env python3
"""
Database initialization script for SmartMeetingAI
"""
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with tables and demo data"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully!")
            
            # Create demo user if none exists
            if not User.query.first():
                demo_user = User(
                    username='demo_user',
                    email='demo@example.com',
                    password_hash=generate_password_hash('demo123')
                )
                db.session.add(demo_user)
                db.session.commit()
                print("Demo user created: demo@example.com / demo123")
            else:
                print("Demo user already exists")
                
            print("Database initialization complete!")
            
        except Exception as e:
            print(f"Database initialization failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    init_database() 