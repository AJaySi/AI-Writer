#!/usr/bin/env python3
"""
Test script to verify the JSON compatibility fix.
"""

import os
import sys
import json
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent / 'backend'))

from llm_providers.gemini_provider import gemini_structured_json_response

def test_json_string_return():
    """Test that the function returns JSON string instead of dict."""
    try:
        print("🧪 Testing JSON string return...")
        
        # Simple schema for testing
        test_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "city": {"type": "string"}
            },
            "required": ["name", "age"]
        }
        
        # Test prompt
        prompt = "Create a person profile with name John, age 30, and city New York."
        
        response = gemini_structured_json_response(
            prompt=prompt,
            schema=test_schema,
            temperature=0.1,
            max_tokens=100
        )
        
        # Check that response is a JSON string
        if isinstance(response, str):
            # Try to parse it as JSON
            parsed = json.loads(response)
            if isinstance(parsed, dict) and "name" in parsed and "age" in parsed:
                print("✅ JSON string return: PASSED")
                print(f"   - Response type: {type(response)}")
                print(f"   - Parsed content: {parsed}")
                return True
            else:
                print(f"❌ JSON string return: FAILED (Invalid JSON content: {parsed})")
                return False
        else:
            print(f"❌ JSON string return: FAILED (Expected string, got {type(response)})")
            return False
            
    except Exception as e:
        print(f"❌ JSON string return: FAILED (Error: {e})")
        return False

def test_json_compatibility():
    """Test that the response can be parsed by calling code."""
    try:
        print("🧪 Testing JSON compatibility...")
        
        # Simple schema for testing
        test_schema = {
            "type": "object",
            "properties": {
                "result": {"type": "string"},
                "status": {"type": "string"}
            },
            "required": ["result", "status"]
        }
        
        # Test prompt
        prompt = "Return a simple result with status success."
        
        response = gemini_structured_json_response(
            prompt=prompt,
            schema=test_schema,
            temperature=0.1,
            max_tokens=50
        )
        
        # Simulate what calling code would do
        try:
            parsed_response = json.loads(response)
            if isinstance(parsed_response, dict):
                print("✅ JSON compatibility: PASSED")
                print(f"   - Successfully parsed by calling code")
                print(f"   - Parsed content: {parsed_response}")
                return True
            else:
                print(f"❌ JSON compatibility: FAILED (Parsed result not dict: {parsed_response})")
                return False
        except json.JSONDecodeError as e:
            print(f"❌ JSON compatibility: FAILED (JSON decode error: {e})")
            return False
            
    except Exception as e:
        print(f"❌ JSON compatibility: FAILED (Error: {e})")
        return False

def main():
    """Run all JSON compatibility tests."""
    print("🧪 Testing JSON Compatibility Fix")
    print("=" * 50)
    
    tests = [
        test_json_string_return,
        test_json_compatibility
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
        print("🎉 All JSON compatibility tests passed!")
        return 0
    else:
        print("⚠️ Some JSON compatibility tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 