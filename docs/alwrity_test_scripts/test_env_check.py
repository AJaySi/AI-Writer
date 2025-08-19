#!/usr/bin/env python3
"""
Test script to check environment variables and API key loading.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

def test_environment_loading():
    """Test environment variable loading."""
    print("🔍 Testing environment variable loading...")
    
    # Check current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if .env file exists in various locations
    possible_env_paths = [
        Path('.env'),  # Current directory
        Path('../.env'),  # Parent directory
        Path('../../.env'),  # Grandparent directory
        Path('../../../.env'),  # Great-grandparent directory
        Path('backend/.env'),  # Backend directory
    ]
    
    print("\n📁 Checking for .env files:")
    for env_path in possible_env_paths:
        if env_path.exists():
            print(f"✅ Found .env file: {env_path.absolute()}")
        else:
            print(f"❌ No .env file: {env_path.absolute()}")
    
    # Try to load .env from different locations
    print("\n🔄 Attempting to load .env files:")
    for env_path in possible_env_paths:
        if env_path.exists():
            print(f"Loading .env from: {env_path.absolute()}")
            load_dotenv(env_path)
            break
    else:
        print("⚠️ No .env file found, trying to load from current directory")
        load_dotenv()
    
    # Check environment variables
    print("\n🔑 Checking environment variables:")
    env_vars_to_check = [
        'GEMINI_API_KEY',
        'GOOGLE_API_KEY',
        'OPENAI_API_KEY',
        'DATABASE_URL',
        'SECRET_KEY'
    ]
    
    for var in env_vars_to_check:
        value = os.getenv(var)
        if value:
            # Show first few characters for security
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"❌ {var}: Not set")
    
    # Test specific Gemini API key loading
    print("\n🤖 Testing Gemini API key loading:")
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print(f"✅ GEMINI_API_KEY found: {gemini_key[:8]}...")
        
        # Test if the key looks valid
        if len(gemini_key) > 20:
            print("✅ API key length looks valid")
        else:
            print("⚠️ API key seems too short")
    else:
        print("❌ GEMINI_API_KEY not found")
        
        # Check alternative names
        alternative_keys = ['GOOGLE_API_KEY', 'GEMINI_KEY', 'GOOGLE_AI_API_KEY']
        for alt_key in alternative_keys:
            alt_value = os.getenv(alt_key)
            if alt_value:
                print(f"⚠️ Found alternative key {alt_key}: {alt_value[:8]}...")
    
    return gemini_key is not None

def test_gemini_provider_import():
    """Test importing the Gemini provider."""
    print("\n🧪 Testing Gemini provider import...")
    
    try:
        from services.llm_providers.gemini_provider import gemini_structured_json_response
        print("✅ Successfully imported gemini_structured_json_response")
        return True
    except Exception as e:
        print(f"❌ Failed to import Gemini provider: {e}")
        return False

def test_ai_service_manager_import():
    """Test importing the AI service manager."""
    print("\n🧪 Testing AI service manager import...")
    
    try:
        from services.ai_service_manager import AIServiceManager
        print("✅ Successfully imported AIServiceManager")
        
        # Try to create an instance
        ai_manager = AIServiceManager()
        print("✅ Successfully created AIServiceManager instance")
        return True
    except Exception as e:
        print(f"❌ Failed to import/create AI service manager: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting environment and API key validation tests")
    print("=" * 60)
    
    # Test environment loading
    env_ok = test_environment_loading()
    
    # Test imports
    gemini_import_ok = test_gemini_provider_import()
    ai_manager_ok = test_ai_service_manager_import()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"Environment loading: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Gemini provider import: {'✅ PASS' if gemini_import_ok else '❌ FAIL'}")
    print(f"AI service manager: {'✅ PASS' if ai_manager_ok else '❌ FAIL'}")
    
    if not env_ok:
        print("\n💡 To fix environment issues:")
        print("1. Create a .env file in the backend directory")
        print("2. Add your GEMINI_API_KEY to the .env file")
        print("3. Example: GEMINI_API_KEY=your_actual_api_key_here")
    
    print("\n" + "=" * 60) 