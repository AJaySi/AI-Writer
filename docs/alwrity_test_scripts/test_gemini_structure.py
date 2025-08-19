#!/usr/bin/env python3
"""
Test script to verify the Gemini provider structure is correct.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent / 'backend'))

def test_gemini_import():
    """Test that the Gemini provider can be imported without errors."""
    try:
        print("🧪 Testing Gemini provider import...")
        
        # Test import
        from services.llm_providers.gemini_provider import (
            gemini_text_response, 
            gemini_pro_text_gen, 
            test_gemini_api_key,
            gemini_structured_json_response
        )
        
        print("✅ Gemini provider import: PASSED")
        print("   - All functions imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Gemini provider import: FAILED (Error: {e})")
        return False

def test_gemini_function_signatures():
    """Test that the function signatures are correct."""
    try:
        print("🧪 Testing Gemini function signatures...")
        
        from services.llm_providers.gemini_provider import (
            gemini_text_response, 
            gemini_pro_text_gen, 
            test_gemini_api_key,
            gemini_structured_json_response
        )
        
        # Test function signatures
        import inspect
        
        # Check gemini_text_response
        sig = inspect.signature(gemini_text_response)
        expected_params = ['prompt', 'temperature', 'top_p', 'n', 'max_tokens', 'system_prompt']
        actual_params = list(sig.parameters.keys())
        
        if all(param in actual_params for param in expected_params):
            print("✅ gemini_text_response signature: PASSED")
        else:
            print(f"❌ gemini_text_response signature: FAILED")
            print(f"   - Expected: {expected_params}")
            print(f"   - Actual: {actual_params}")
            return False
        
        # Check gemini_pro_text_gen
        sig = inspect.signature(gemini_pro_text_gen)
        expected_params = ['prompt', 'temperature', 'top_p', 'top_k', 'max_tokens']
        actual_params = list(sig.parameters.keys())
        
        if all(param in actual_params for param in expected_params):
            print("✅ gemini_pro_text_gen signature: PASSED")
        else:
            print(f"❌ gemini_pro_text_gen signature: FAILED")
            print(f"   - Expected: {expected_params}")
            print(f"   - Actual: {actual_params}")
            return False
        
        # Check gemini_structured_json_response
        sig = inspect.signature(gemini_structured_json_response)
        expected_params = ['prompt', 'schema', 'temperature', 'top_p', 'top_k', 'max_tokens', 'system_prompt']
        actual_params = list(sig.parameters.keys())
        
        if all(param in actual_params for param in expected_params):
            print("✅ gemini_structured_json_response signature: PASSED")
        else:
            print(f"❌ gemini_structured_json_response signature: FAILED")
            print(f"   - Expected: {expected_params}")
            print(f"   - Actual: {actual_params}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini function signatures: FAILED (Error: {e})")
        return False

def test_gemini_api_key_handling():
    """Test that the API key handling is correct."""
    try:
        print("🧪 Testing Gemini API key handling...")
        
        from services.llm_providers.gemini_provider import gemini_text_response
        
        # Test with no API key (should raise ValueError)
        original_key = os.environ.get('GEMINI_API_KEY')
        if 'GEMINI_API_KEY' in os.environ:
            del os.environ['GEMINI_API_KEY']
        
        try:
            gemini_text_response("test", max_tokens=10)
            print("❌ API key handling: FAILED (Should have raised ValueError)")
            return False
        except ValueError as e:
            if "Gemini API key not found" in str(e):
                print("✅ API key handling: PASSED")
                print("   - Correctly raises ValueError when API key is missing")
            else:
                print(f"❌ API key handling: FAILED (Unexpected error: {e})")
                return False
        finally:
            # Restore original key if it existed
            if original_key:
                os.environ['GEMINI_API_KEY'] = original_key
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini API key handling: FAILED (Error: {e})")
        return False

def main():
    """Run all structure tests."""
    print("🧪 Testing Gemini Provider Structure")
    print("=" * 50)
    
    tests = [
        test_gemini_import,
        test_gemini_function_signatures,
        test_gemini_api_key_handling
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
        print("🎉 All structure tests passed! The Gemini provider is correctly structured.")
        print("💡 To test with real API calls, set the GEMINI_API_KEY environment variable.")
        return 0
    else:
        print("⚠️ Some structure tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 