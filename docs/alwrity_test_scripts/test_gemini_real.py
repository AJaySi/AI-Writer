#!/usr/bin/env python3
"""
Test script to verify the Gemini provider is working with real API calls.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent / 'backend'))

from services.llm_providers.gemini_provider import gemini_text_response, gemini_pro_text_gen

def test_gemini_real_call():
    """Test a real Gemini API call."""
    try:
        print("🧪 Testing real Gemini API call...")
        
        # Test with a simple prompt
        prompt = "What is the capital of France? Answer in one sentence."
        response = gemini_text_response(prompt, temperature=0.1, max_tokens=50)
        
        if response and len(response) > 0:
            print("✅ Real Gemini API call: PASSED")
            print(f"   - Response: {response}")
            return True
        else:
            print("❌ Real Gemini API call: FAILED (Empty response)")
            return False
            
    except Exception as e:
        print(f"❌ Real Gemini API call: FAILED (Error: {e})")
        return False

def test_gemini_pro_real_call():
    """Test the legacy function with real API call."""
    try:
        print("🧪 Testing Gemini Pro real API call...")
        
        # Test with a simple prompt
        prompt = "What is 2 + 2? Answer in one word."
        response = gemini_pro_text_gen(prompt, temperature=0.1, max_tokens=10)
        
        if response and len(response) > 0 and not response.startswith("Error"):
            print("✅ Gemini Pro real API call: PASSED")
            print(f"   - Response: {response}")
            return True
        else:
            print(f"❌ Gemini Pro real API call: FAILED (Response: {response})")
            return False
            
    except Exception as e:
        print(f"❌ Gemini Pro real API call: FAILED (Error: {e})")
        return False

def main():
    """Run all real API tests."""
    print("🧪 Testing Gemini Provider Real API Calls")
    print("=" * 50)
    
    tests = [
        test_gemini_real_call,
        test_gemini_pro_real_call
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
        print("🎉 All real API tests passed! The Gemini provider is working correctly.")
        return 0
    else:
        print("⚠️ Some real API tests failed. Please check the API key and configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 