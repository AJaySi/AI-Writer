#!/usr/bin/env python3
"""
Test script to verify the fixes for the Content Planning Dashboard.
"""

import requests
import json
import sys

def test_backend_health():
    """Test if the backend is responding."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check: PASSED")
            return True
        else:
            print(f"❌ Backend health check: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Backend health check: FAILED (Error: {e})")
        return False

def test_ai_analytics_endpoint():
    """Test if the AI analytics endpoint is working."""
    try:
        response = requests.get("http://localhost:8000/api/content-planning/ai-analytics/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'insights' in data and 'recommendations' in data:
                print("✅ AI Analytics endpoint: PASSED")
                print(f"   - Found {len(data['insights'])} insights")
                print(f"   - Found {len(data['recommendations'])} recommendations")
                return True
            else:
                print("❌ AI Analytics endpoint: FAILED (Missing expected fields)")
                return False
        else:
            print(f"❌ AI Analytics endpoint: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ AI Analytics endpoint: FAILED (Error: {e})")
        return False

def test_content_planning_health():
    """Test if the content planning health endpoint is working."""
    try:
        response = requests.get("http://localhost:8000/api/content-planning/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'status' in data:
                print("✅ Content Planning health check: PASSED")
                print(f"   - Status: {data['status']}")
                return True
            else:
                print("❌ Content Planning health check: FAILED (Missing status field)")
                return False
        else:
            print(f"❌ Content Planning health check: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Content Planning health check: FAILED (Error: {e})")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Content Planning Dashboard Fixes")
    print("=" * 50)
    
    tests = [
        test_backend_health,
        test_ai_analytics_endpoint,
        test_content_planning_health
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The fixes are working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the backend logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 