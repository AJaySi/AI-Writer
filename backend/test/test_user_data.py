#!/usr/bin/env python3
"""
Test script for user data service
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.database import init_database, get_db_session
from services.user_data_service import UserDataService
from loguru import logger

def test_user_data():
    """Test the user data service functionality."""
    
    print("👤 Testing User Data Service")
    print("=" * 50)
    
    try:
        # Initialize database
        print("📊 Initializing database...")
        init_database()
        print("✅ Database initialized successfully")
        
        # Test fetching user website URL
        print("\n🌐 Testing website URL fetching...")
        db_session = get_db_session()
        if db_session:
            try:
                user_data_service = UserDataService(db_session)
                website_url = user_data_service.get_user_website_url()
                
                if website_url:
                    print(f"✅ Found website URL: {website_url}")
                else:
                    print("⚠️ No website URL found in database")
                    print("   This is expected if no onboarding has been completed yet")
                
                # Test getting full onboarding data
                print("\n📋 Testing full onboarding data...")
                onboarding_data = user_data_service.get_user_onboarding_data()
                
                if onboarding_data:
                    print("✅ Found onboarding data:")
                    print(f"   Session ID: {onboarding_data['session']['id']}")
                    print(f"   Current Step: {onboarding_data['session']['current_step']}")
                    print(f"   Progress: {onboarding_data['session']['progress']}")
                    
                    if onboarding_data['website_analysis']:
                        print(f"   Website URL: {onboarding_data['website_analysis']['website_url']}")
                        print(f"   Analysis Status: {onboarding_data['website_analysis']['status']}")
                    else:
                        print("   No website analysis found")
                    
                    print(f"   API Keys: {len(onboarding_data['api_keys'])} configured")
                    
                    if onboarding_data['research_preferences']:
                        print("   Research preferences configured")
                    else:
                        print("   No research preferences found")
                else:
                    print("⚠️ No onboarding data found")
                    print("   This is expected if no onboarding has been completed yet")
                    
            except Exception as e:
                print(f"❌ Database error: {str(e)}")
            finally:
                db_session.close()
        else:
            print("❌ Failed to get database session")
        
        print("\n🎉 User Data Service Test Completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        logger.error(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_user_data() 