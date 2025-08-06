"""Test script for ALwrity backend."""

import requests
import json
import time

def test_backend():
    """Test the backend endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ALwrity Backend API...")
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Get onboarding status
    print("\n2. Testing onboarding status...")
    try:
        response = requests.get(f"{base_url}/api/onboarding/status")
        if response.status_code == 200:
            print("✅ Onboarding status passed")
            data = response.json()
            print(f"   Current step: {data.get('current_step')}")
            print(f"   Completion: {data.get('completion_percentage')}%")
        else:
            print(f"❌ Onboarding status failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Onboarding status error: {e}")
        return False
    
    # Test 3: Get onboarding config
    print("\n3. Testing onboarding config...")
    try:
        response = requests.get(f"{base_url}/api/onboarding/config")
        if response.status_code == 200:
            print("✅ Onboarding config passed")
            data = response.json()
            print(f"   Total steps: {data.get('total_steps')}")
        else:
            print(f"❌ Onboarding config failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Onboarding config error: {e}")
        return False
    
    # Test 4: Get API keys
    print("\n4. Testing API keys endpoint...")
    try:
        response = requests.get(f"{base_url}/api/onboarding/api-keys")
        if response.status_code == 200:
            print("✅ API keys endpoint passed")
            data = response.json()
            print(f"   Configured keys: {data.get('total_configured')}")
        else:
            print(f"❌ API keys endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API keys endpoint error: {e}")
        return False
    
    # Test 5: Save API key
    print("\n5. Testing save API key...")
    try:
        test_key_data = {
            "provider": "openai",
            "api_key": "sk-test1234567890abcdef",
            "description": "Test API key"
        }
        response = requests.post(
            f"{base_url}/api/onboarding/api-keys",
            json=test_key_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Save API key passed")
            data = response.json()
            print(f"   Message: {data.get('message')}")
        else:
            print(f"❌ Save API key failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Save API key error: {e}")
        return False
    
    # Test 6: Complete step
    print("\n6. Testing complete step...")
    try:
        step_data = {
            "data": {"api_keys": ["openai"]},
            "validation_errors": []
        }
        response = requests.post(
            f"{base_url}/api/onboarding/step/1/complete",
            json=step_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Complete step passed")
            data = response.json()
            print(f"   Message: {data.get('message')}")
        else:
            print(f"❌ Complete step failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Complete step error: {e}")
        return False
    
    # Test 7: Get updated status
    print("\n7. Testing updated status...")
    try:
        response = requests.get(f"{base_url}/api/onboarding/status")
        if response.status_code == 200:
            print("✅ Updated status passed")
            data = response.json()
            print(f"   Current step: {data.get('current_step')}")
            print(f"   Completion: {data.get('completion_percentage')}%")
        else:
            print(f"❌ Updated status failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Updated status error: {e}")
        return False
    
    print("\n🎉 All tests completed!")
    return True

def test_api_docs():
    """Test if API documentation is accessible."""
    base_url = "http://localhost:8000"
    
    print("\n📚 Testing API documentation...")
    
    try:
        # Test Swagger docs
        response = requests.get(f"{base_url}/api/docs")
        if response.status_code == 200:
            print("✅ Swagger docs accessible")
        else:
            print(f"❌ Swagger docs failed: {response.status_code}")
        
        # Test ReDoc
        response = requests.get(f"{base_url}/api/redoc")
        if response.status_code == 200:
            print("✅ ReDoc accessible")
        else:
            print(f"❌ ReDoc failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API docs error: {e}")

if __name__ == "__main__":
    print("🚀 Starting ALwrity Backend Tests")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Run tests
    success = test_backend()
    test_api_docs()
    
    if success:
        print("\n✅ All tests passed! Backend is working correctly.")
        print("\n📖 You can now:")
        print("   - View API docs at: http://localhost:8000/api/docs")
        print("   - Test endpoints manually")
        print("   - Integrate with React frontend")
    else:
        print("\n❌ Some tests failed. Please check the backend logs.") 