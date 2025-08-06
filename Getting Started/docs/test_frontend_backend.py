#!/usr/bin/env python3
"""
Test script to verify frontend-backend communication.
"""

import requests
import time

def test_backend_endpoints():
    """Test all backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Backend Endpoints...")
    
    # Test health endpoint
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test onboarding check
    print("\n2️⃣ Testing onboarding check...")
    try:
        response = requests.get(f"{base_url}/api/check-onboarding")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Onboarding check working: {data}")
        else:
            print(f"❌ Onboarding check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Onboarding check error: {e}")
    
    # Test onboarding start
    print("\n3️⃣ Testing onboarding start...")
    try:
        response = requests.post(f"{base_url}/api/onboarding/start")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Onboarding start working: {data}")
        else:
            print(f"❌ Onboarding start failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Onboarding start error: {e}")
    
    # Test onboarding step
    print("\n4️⃣ Testing onboarding step...")
    try:
        response = requests.get(f"{base_url}/api/onboarding/step")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Onboarding step working: {data}")
        else:
            print(f"❌ Onboarding step failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Onboarding step error: {e}")

def test_frontend_communication():
    """Test if frontend can reach backend"""
    print("\n🌐 Testing Frontend-Backend Communication...")
    
    # Simulate frontend API calls
    base_url = "http://localhost:8000"
    
    # Test the exact endpoints the frontend uses
    endpoints = [
        ("GET", "/api/check-onboarding"),
        ("POST", "/api/onboarding/start"),
        ("GET", "/api/onboarding/step"),
        ("GET", "/api/onboarding/api-keys"),
        ("POST", "/api/onboarding/api-keys"),
        ("GET", "/api/onboarding/progress"),
    ]
    
    for method, endpoint in endpoints:
        print(f"\nTesting {method} {endpoint}...")
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}")
            elif method == "POST":
                response = requests.post(f"{base_url}{endpoint}")
            
            if response.status_code in [200, 404]:  # 404 is expected for some endpoints without data
                print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            else:
                print(f"❌ {method} {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Frontend-Backend Communication Test...")
    
    # Wait a moment for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(2)
    
    test_backend_endpoints()
    test_frontend_communication()
    
    print("\n🎯 Test complete!")
    print("📝 If all tests pass, the frontend should work correctly.")
    print("🌐 Visit http://localhost:3000 to test the onboarding flow.") 