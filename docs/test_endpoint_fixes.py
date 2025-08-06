#!/usr/bin/env python3
"""
Test script to verify the endpoint fixes for 422 errors.
"""

import requests
import json
import sys

def test_strategies_endpoint():
    """Test the strategies endpoint that was causing 422 errors."""
    try:
        print("🧪 Testing strategies endpoint...")
        
        # Test without user_id (should now work)
        response = requests.get("http://localhost:8000/api/content-planning/strategies/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print("✅ Strategies endpoint: PASSED")
                print(f"   - Status: {response.status_code}")
                print(f"   - Found {len(data)} strategies")
                return True
            else:
                print(f"❌ Strategies endpoint: FAILED (Invalid response format: {data})")
                return False
        else:
            print(f"❌ Strategies endpoint: FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Strategies endpoint: FAILED (Error: {e})")
        return False

def test_gap_analysis_endpoint():
    """Test the gap analysis endpoint that was causing 422 errors."""
    try:
        print("🧪 Testing gap analysis endpoint...")
        
        # Test without user_id (should now work)
        response = requests.get("http://localhost:8000/api/content-planning/gap-analysis/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print("✅ Gap analysis endpoint: PASSED")
                print(f"   - Status: {response.status_code}")
                print(f"   - Found {len(data)} analyses")
                return True
            else:
                print(f"❌ Gap analysis endpoint: FAILED (Invalid response format: {data})")
                return False
        else:
            print(f"❌ Gap analysis endpoint: FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Gap analysis endpoint: FAILED (Error: {e})")
        return False

def test_ai_analytics_endpoint():
    """Test the AI analytics endpoint."""
    try:
        print("🧪 Testing AI analytics endpoint...")
        
        response = requests.get("http://localhost:8000/api/content-planning/ai-analytics/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "insights" in data and "recommendations" in data:
                print("✅ AI analytics endpoint: PASSED")
                print(f"   - Status: {response.status_code}")
                print(f"   - Found {len(data['insights'])} insights")
                print(f"   - Found {len(data['recommendations'])} recommendations")
                return True
            else:
                print(f"❌ AI analytics endpoint: FAILED (Missing expected fields)")
                return False
        else:
            print(f"❌ AI analytics endpoint: FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ AI analytics endpoint: FAILED (Error: {e})")
        return False

def main():
    """Run all endpoint tests."""
    print("🧪 Testing Endpoint Fixes")
    print("=" * 50)
    
    tests = [
        test_strategies_endpoint,
        test_gap_analysis_endpoint,
        test_ai_analytics_endpoint
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
        print("🎉 All endpoint tests passed! The 422 errors are fixed.")
        return 0
    else:
        print("⚠️ Some endpoint tests failed. Please check the backend.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 