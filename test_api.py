#!/usr/bin/env python3
"""
Simple script to test the API endpoints
Run this after starting the server with: python -m backend.main
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    return response.json() if response.status_code < 400 else None

def main():
    print("🚀 Testing Fanbase Builder API")
    print(f"Base URL: {BASE_URL}\n")
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    health_data = print_response(response, "Health Check")
    
    if not health_data or health_data.get("status") != "healthy":
        print("❌ Server is not healthy. Make sure it's running!")
        return
    
    # Test 2: Root endpoint
    print("\n2️⃣ Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root Endpoint")
    
    # Test 3: Sign Up
    print("\n3️⃣ Testing User Signup...")
    signup_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "artist_name": "Test Artist"
    }
    response = requests.post(
        f"{BASE_URL}/api/auth/signup",
        json=signup_data
    )
    signup_result = print_response(response, "Signup")
    
    if response.status_code == 400 and "already exists" in response.text.lower():
        print("ℹ️  User already exists, continuing with login...")
        signup_result = None
    
    # Test 4: Login
    print("\n4️⃣ Testing Login...")
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    login_result = print_response(response, "Login")
    
    if not login_result or "access_token" not in login_result:
        print("❌ Login failed. Cannot continue with protected routes.")
        return
    
    access_token = login_result["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test 5: Get Current User
    print("\n5️⃣ Testing Get Current User (Protected Route)...")
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print_response(response, "Current User")
    
    # Test 6: Get Metrics Overview
    print("\n6️⃣ Testing Metrics Overview...")
    response = requests.get(f"{BASE_URL}/api/metrics/overview", headers=headers)
    print_response(response, "Metrics Overview")
    
    # Test 7: Get Connections
    print("\n7️⃣ Testing Get Connections...")
    response = requests.get(f"{BASE_URL}/api/connections", headers=headers)
    print_response(response, "Connections")
    
    # Test 8: Get Content Posts
    print("\n8️⃣ Testing Get Content Posts...")
    response = requests.get(f"{BASE_URL}/api/content", headers=headers)
    print_response(response, "Content Posts")
    
    # Test 9: Create a Content Post
    print("\n9️⃣ Testing Create Content Post...")
    post_data = {
        "platform": "instagram",
        "content_type": "photo",
        "caption": "Test post from API",
        "scheduled_for": None  # Post immediately
    }
    response = requests.post(
        f"{BASE_URL}/api/content",
        json=post_data,
        headers=headers
    )
    print_response(response, "Create Content Post")
    
    print("\n" + "="*60)
    print("✅ Testing Complete!")
    print("="*60)
    print("\n💡 Tips:")
    print("   - Visit http://localhost:8000/docs for interactive API docs")
    print("   - Visit http://localhost:8000/redoc for alternative docs")
    print("   - Use the access_token above to test other endpoints")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server!")
        print("   Make sure the server is running:")
        print("   python -m backend.main")
    except Exception as e:
        print(f"❌ Error: {e}")

