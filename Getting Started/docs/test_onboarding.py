#!/usr/bin/env python3
"""
Test script to reset onboarding state and test the onboarding flow.
"""

import sys
import os
import sqlite3

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def reset_database():
    """Reset the onboarding database"""
    db_path = "backend/onboarding.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Database file removed")
    else:
        print("ℹ️  No database file found")

def check_onboarding_status():
    """Check the current onboarding status"""
    import requests
    try:
        response = requests.get("http://localhost:8000/api/check-onboarding")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Onboarding Status: {data}")
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error checking onboarding status: {e}")
        return None

def test_onboarding_flow():
    """Test the complete onboarding flow"""
    print("\n🧪 Testing Onboarding Flow...")
    
    # Step 1: Check initial status
    print("\n1️⃣ Checking initial onboarding status...")
    status = check_onboarding_status()
    
    if status and status.get('onboarding_required'):
        print("✅ Correctly shows onboarding required for first-time user")
    else:
        print("❌ Incorrectly shows onboarding complete")
    
    # Step 2: Start onboarding
    print("\n2️⃣ Starting onboarding session...")
    try:
        import requests
        response = requests.post("http://localhost:8000/api/onboarding/start")
        if response.status_code == 200:
            print("✅ Onboarding session started")
        else:
            print(f"❌ Error starting onboarding: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 3: Check status again
    print("\n3️⃣ Checking status after starting onboarding...")
    status = check_onboarding_status()
    
    if status and status.get('onboarding_required'):
        print("✅ Still shows onboarding required (correct)")
    else:
        print("❌ Incorrectly shows onboarding complete")

if __name__ == "__main__":
    print("🔄 Resetting onboarding state...")
    reset_database()
    
    print("\n⏳ Waiting for backend to restart...")
    import time
    time.sleep(3)
    
    test_onboarding_flow()
    
    print("\n🎯 Test complete! Check your frontend at http://localhost:3000") 