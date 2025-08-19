#!/usr/bin/env python3
"""
Test script to verify the schema validation fixes.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent / 'backend'))

from services.llm_providers.gemini_provider import _clean_schema_for_gemini, _validate_and_fix_schema

def test_empty_object_fix():
    """Test fixing empty object properties."""
    try:
        print("🧪 Testing empty object property fix...")
        
        # Test schema with empty object properties (like the one causing errors)
        test_schema = {
            "type": "object",
            "properties": {
                "trends": {
                    "type": "object",
                    "properties": {}  # This causes the error
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "score": {"type": "number"}
                    }
                }
            }
        }
        
        # Clean the schema
        cleaned_schema = _clean_schema_for_gemini(test_schema)
        fixed_schema = _validate_and_fix_schema(cleaned_schema)
        
        # Check that empty object properties are converted to strings
        assert fixed_schema["properties"]["trends"]["type"] == "string"
        assert fixed_schema["properties"]["analysis"]["type"] == "object"
        assert "score" in fixed_schema["properties"]["analysis"]["properties"]
        
        print("✅ Empty object property fix: PASSED")
        print(f"   - Trends type: {fixed_schema['properties']['trends']['type']}")
        print(f"   - Analysis type: {fixed_schema['properties']['analysis']['type']}")
        return True
        
    except Exception as e:
        print(f"❌ Empty object property fix: FAILED (Error: {e})")
        return False

def test_complex_schema_validation():
    """Test complex schema validation."""
    try:
        print("🧪 Testing complex schema validation...")
        
        # Test schema with nested empty objects
        test_schema = {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "metrics": {
                            "type": "object",
                            "properties": {}  # Empty properties
                        },
                        "summary": {
                            "type": "object",
                            "properties": {
                                "total": {"type": "integer"},
                                "average": {"type": "number"}
                            }
                        }
                    }
                }
            }
        }
        
        # Clean and validate the schema
        cleaned_schema = _clean_schema_for_gemini(test_schema)
        fixed_schema = _validate_and_fix_schema(cleaned_schema)
        
        # Check that empty nested objects are fixed
        assert fixed_schema["properties"]["data"]["properties"]["metrics"]["type"] == "string"
        assert fixed_schema["properties"]["data"]["properties"]["summary"]["type"] == "object"
        assert "total" in fixed_schema["properties"]["data"]["properties"]["summary"]["properties"]
        
        print("✅ Complex schema validation: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Complex schema validation: FAILED (Error: {e})")
        return False

def test_unsupported_properties_removal():
    """Test removal of unsupported properties."""
    try:
        print("🧪 Testing unsupported properties removal...")
        
        # Test schema with unsupported properties
        test_schema = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 100,
                    "pattern": "^[a-zA-Z0-9 ]+$"
                },
                "content": {
                    "type": "string",
                    "format": "text"
                }
            },
            "additionalProperties": False
        }
        
        # Clean the schema
        cleaned_schema = _clean_schema_for_gemini(test_schema)
        
        # Check that unsupported properties are removed
        assert "additionalProperties" not in cleaned_schema
        assert "minLength" not in cleaned_schema["properties"]["title"]
        assert "maxLength" not in cleaned_schema["properties"]["title"]
        assert "pattern" not in cleaned_schema["properties"]["title"]
        assert "format" not in cleaned_schema["properties"]["content"]
        
        # Check that supported properties remain
        assert "type" in cleaned_schema
        assert "properties" in cleaned_schema
        
        print("✅ Unsupported properties removal: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Unsupported properties removal: FAILED (Error: {e})")
        return False

def main():
    """Run all schema validation tests."""
    print("🧪 Testing Schema Validation Fixes")
    print("=" * 50)
    
    tests = [
        test_empty_object_fix,
        test_complex_schema_validation,
        test_unsupported_properties_removal
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
        print("🎉 All schema validation tests passed!")
        return 0
    else:
        print("⚠️ Some schema validation tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 