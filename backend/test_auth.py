#!/usr/bin/env python3
"""
Test script to verify authentication functionality
"""
import requests
import json

def test_auth():
    base_url = "http://127.0.0.1:5000"
    
    # Test registration
    print("Testing registration...")
    register_data = {
        "action": "register",
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth", json=register_data)
        print(f"Registration response: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Registration result: {result}")
        else:
            print("Registration failed!")
            
    except Exception as e:
        print(f"Registration error: {e}")
    
    # Test login
    print("\nTesting login...")
    login_data = {
        "action": "login",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth", json=login_data)
        print(f"Login response: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Login result: {result}")
        else:
            print("Login failed!")
            
    except Exception as e:
        print(f"Login error: {e}")

if __name__ == "__main__":
    test_auth() 