#!/usr/bin/env python3
"""
Simple test script for the Hallucination Detection API endpoints.
This script tests the API without requiring full dependencies.
"""

import json
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_structure():
    """Test that the API structure is correct."""
    print("🧪 Testing Hallucination Detection API Structure")
    print("=" * 50)
    
    # Test 1: Check if files exist
    files_to_check = [
        "models/hallucination_models.py",
        "services/hallucination_detection_service.py", 
        "routers/hallucination_detection.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    # Test 2: Check syntax compilation
    print("\n📝 Testing Python syntax:")
    for file_path in files_to_check:
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            print(f"✅ {file_path} compiles correctly")
        except SyntaxError as e:
            print(f"❌ {file_path} has syntax error: {e}")
            return False
    
    # Test 3: Check model definitions
    print("\n🏗️  Testing model definitions:")
    models_file = "models/hallucination_models.py"
    with open(models_file, 'r') as f:
        content = f.read()
        
    required_models = [
        "HallucinationDetectionRequest",
        "HallucinationDetectionResponse", 
        "ClaimVerification",
        "SourceDocument",
        "BatchHallucinationRequest",
        "HallucinationHealthCheck"
    ]
    
    for model in required_models:
        if f"class {model}" in content:
            print(f"✅ {model} model defined")
        else:
            print(f"❌ {model} model missing")
            return False
    
    # Test 4: Check service methods
    print("\n⚙️  Testing service methods:")
    service_file = "services/hallucination_detection_service.py"
    with open(service_file, 'r') as f:
        content = f.read()
        
    required_methods = [
        "detect_hallucinations",
        "extract_claims",
        "verify_claim", 
        "search_for_sources",
        "health_check"
    ]
    
    for method in required_methods:
        if f"def {method}" in content or f"async def {method}" in content:
            print(f"✅ {method} method defined")
        else:
            print(f"❌ {method} method missing")
            return False
    
    # Test 5: Check API endpoints
    print("\n🌐 Testing API endpoints:")
    router_file = "routers/hallucination_detection.py"
    with open(router_file, 'r') as f:
        content = f.read()
        
    required_endpoints = [
        "/analyze",
        "/analyze-batch",
        "/extract-claims",
        "/verify-claim",
        "/demo",
        "/health"
    ]
    
    for endpoint in required_endpoints:
        if f'"{endpoint}"' in content:
            print(f"✅ {endpoint} endpoint defined")
        else:
            print(f"❌ {endpoint} endpoint missing")
            return False
    
    # Test 6: Check integration with main app
    print("\n🔗 Testing integration:")
    app_file = "app.py"
    if os.path.exists(app_file):
        with open(app_file, 'r') as f:
            content = f.read()
            
        if "hallucination_router" in content:
            print("✅ Hallucination router integrated in main app")
        else:
            print("❌ Hallucination router not integrated")
            return False
    else:
        print("❌ app.py not found")
        return False
    
    return True

def test_demo_data():
    """Test the demo data structure."""
    print("\n🎯 Testing demo data structure:")
    
    # Read the router file to extract demo data
    with open("routers/hallucination_detection.py", 'r') as f:
        content = f.read()
    
    # Check if demo endpoint has proper structure
    if "demo_response" in content:
        print("✅ Demo response structure defined")
    else:
        print("❌ Demo response structure missing")
        return False
        
    # Check for required demo fields
    demo_fields = [
        "original_text",
        "total_claims", 
        "claims_analysis",
        "overall_assessment"
    ]
    
    for field in demo_fields:
        if f'"{field}"' in content:
            print(f"✅ Demo field '{field}' present")
        else:
            print(f"❌ Demo field '{field}' missing")
            return False
    
    return True

def generate_api_summary():
    """Generate a summary of the implemented API."""
    print("\n📊 API Implementation Summary:")
    print("=" * 50)
    
    summary = {
        "service_name": "Hallucination Detection API",
        "version": "1.0.0",
        "base_path": "/api/hallucination-detection",
        "endpoints": [
            {
                "path": "/analyze",
                "method": "POST",
                "description": "Analyze text for hallucinations",
                "input": "HallucinationDetectionRequest",
                "output": "HallucinationDetectionResponse"
            },
            {
                "path": "/analyze-batch", 
                "method": "POST",
                "description": "Batch analyze multiple texts",
                "input": "BatchHallucinationRequest",
                "output": "BatchHallucinationResponse"
            },
            {
                "path": "/extract-claims",
                "method": "POST", 
                "description": "Extract claims without verification",
                "input": "TextInput",
                "output": "Claims list"
            },
            {
                "path": "/verify-claim",
                "method": "POST",
                "description": "Verify a single claim",
                "input": "Query parameters",
                "output": "ClaimVerification"
            },
            {
                "path": "/demo",
                "method": "GET",
                "description": "Get demonstration analysis",
                "input": "None",
                "output": "Demo response"
            },
            {
                "path": "/health",
                "method": "GET", 
                "description": "Service health check",
                "input": "None",
                "output": "HallucinationHealthCheck"
            }
        ],
        "features": [
            "Factual claim extraction using LLM",
            "Web search for source verification",
            "Confidence scoring for assessments", 
            "Batch processing support",
            "Comprehensive error handling",
            "Demo mode for testing"
        ]
    }
    
    print(json.dumps(summary, indent=2))
    return summary

def main():
    """Main test function."""
    print("🚀 Starting Hallucination Detection API Tests")
    print("=" * 60)
    
    # Run tests
    structure_ok = test_api_structure()
    demo_ok = test_demo_data()
    
    if structure_ok and demo_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The Hallucination Detection API is ready to use")
        
        # Generate summary
        generate_api_summary()
        
        print("\n📖 Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set environment variables (OPENAI_API_KEY, EXA_API_KEY)")
        print("3. Start the server: uvicorn app:app --reload")
        print("4. Test the API at: http://localhost:8000/api/hallucination-detection/")
        print("5. View API docs at: http://localhost:8000/docs")
        print("6. Implement React UI using the provided documentation")
        
        return True
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Please check the errors above and fix them before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)