#!/usr/bin/env python3
"""
Test script to verify the Gemini provider fixes.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent / 'backend'))

from services.llm_providers.gemini_provider import gemini_text_response, gemini_pro_text_gen, test_gemini_api_key

def test_gemini_text_response():
    """Test the basic text response function."""
    try:
        print("🧪 Testing Gemini text response...")
        
        # Test with a simple prompt
        prompt = "Hello, how are you today?"
        response = gemini_text_response(prompt, temperature=0.1, max_tokens=50)
        
        if response and len(response) > 0:
            print("✅ Gemini text response: PASSED")
            print(f"   - Response: {response[:100]}...")
            return True
        else:
            print("❌ Gemini text response: FAILED (Empty response)")
            return False
            
    except Exception as e:
        print(f"❌ Gemini text response: FAILED (Error: {e})")
        return False

def test_gemini_pro_text_gen():
    """Test the legacy text generation function."""
    try:
        print("🧪 Testing Gemini Pro text generation...")
        
        # Test with a simple prompt
        prompt = "What is the capital of France?"
        response = gemini_pro_text_gen(prompt, temperature=0.1, max_tokens=50)
        
        if response and len(response) > 0 and not response.startswith("Error"):
            print("✅ Gemini Pro text generation: PASSED")
            print(f"   - Response: {response[:100]}...")
            return True
        else:
            print(f"❌ Gemini Pro text generation: FAILED (Response: {response})")
            return False
            
    except Exception as e:
        print(f"❌ Gemini Pro text generation: FAILED (Error: {e})")
        return False

async def test_gemini_api_key_validation():
    """Test the API key validation function."""
    try:
        print("🧪 Testing Gemini API key validation...")
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ Gemini API key validation: FAILED (No API key found)")
            return False
        
        # Test the API key
        is_valid, message = await test_gemini_api_key(api_key)
        
        if is_valid:
            print("✅ Gemini API key validation: PASSED")
            print(f"   - Message: {message}")
            return True
        else:
            print(f"❌ Gemini API key validation: FAILED (Message: {message})")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API key validation: FAILED (Error: {e})")
        return False

async def main():
    """Run all Gemini tests."""
    print("🧪 Testing Gemini Provider Fixes")
    print("=" * 50)
    
    tests = [
        test_gemini_text_response,
        test_gemini_pro_text_gen,
        test_gemini_api_key_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test == test_gemini_api_key_validation:
            result = await test()
        else:
            result = test()
        
        if result:
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Gemini tests passed! The fixes are working correctly.")
        return 0
    else:
        print("⚠️ Some Gemini tests failed. Please check the API key and configuration.")
        return 1

if __name__ == "__main__":
    import asyncio
    sys.exit(asyncio.run(main())) 