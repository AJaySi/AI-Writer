#!/usr/bin/env python3
"""
Test script to verify the structured output functionality.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent / 'backend'))

from llm_providers.gemini_provider import gemini_structured_json_response, _clean_schema_for_gemini

def test_schema_cleaning():
    """Test the schema cleaning function."""
    try:
        print("🧪 Testing schema cleaning...")
        
        # Test schema with unsupported properties
        test_schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string", "minLength": 1, "maxLength": 100},
                "description": {"type": "string", "pattern": "^[a-zA-Z0-9 ]+$"},
                "tags": {"type": "array", "items": {"type": "string"}}
            },
            "additionalProperties": False,
            "required": ["title"]
        }
        
        cleaned_schema = _clean_schema_for_gemini(test_schema)
        
        # Check that unsupported properties are removed
        assert "additionalProperties" not in cleaned_schema
        assert "minLength" not in cleaned_schema["properties"]["title"]
        assert "maxLength" not in cleaned_schema["properties"]["title"]
        assert "pattern" not in cleaned_schema["properties"]["description"]
        
        # Check that supported properties remain
        assert "type" in cleaned_schema
        assert "properties" in cleaned_schema
        assert "required" in cleaned_schema
        
        print("✅ Schema cleaning: PASSED")
        print(f"   - Original schema keys: {list(test_schema.keys())}")
        print(f"   - Cleaned schema keys: {list(cleaned_schema.keys())}")
        return True
        
    except Exception as e:
        print(f"❌ Schema cleaning: FAILED (Error: {e})")
        return False

def test_structured_output():
    """Test structured JSON output."""
    try:
        print("🧪 Testing structured JSON output...")
        
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
        
        if isinstance(response, dict) and "name" in response and "age" in response:
            print("✅ Structured JSON output: PASSED")
            print(f"   - Response: {response}")
            return True
        else:
            print(f"❌ Structured JSON output: FAILED (Response: {response})")
            return False
            
    except Exception as e:
        print(f"❌ Structured JSON output: FAILED (Error: {e})")
        return False

def main():
    """Run all structured output tests."""
    print("🧪 Testing Structured Output Functionality")
    print("=" * 50)
    
    tests = [
        test_schema_cleaning,
        test_structured_output
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
        print("🎉 All structured output tests passed!")
        return 0
    else:
        print("⚠️ Some structured output tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 