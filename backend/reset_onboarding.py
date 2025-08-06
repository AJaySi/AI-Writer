#!/usr/bin/env python3
"""Reset onboarding progress for testing."""

import os
import json
from pathlib import Path

def reset_onboarding_progress():
    """Reset the onboarding progress by deleting the progress file."""
    
    # Progress file path
    progress_file = ".onboarding_progress.json"
    
    print("🔄 Resetting onboarding progress...")
    
    # Check if progress file exists
    if os.path.exists(progress_file):
        try:
            # Read current progress for backup
            with open(progress_file, 'r') as f:
                current_progress = json.load(f)
            
            print(f"   📊 Current progress:")
            print(f"      - Current step: {current_progress.get('current_step', 'N/A')}")
            print(f"      - Completion: {current_progress.get('is_completed', False)}")
            print(f"      - Started: {current_progress.get('started_at', 'N/A')}")
            
            # Delete the progress file
            os.remove(progress_file)
            print("   ✅ Progress file deleted successfully")
            
        except Exception as e:
            print(f"   ❌ Error reading/deleting progress file: {e}")
            return False
    else:
        print("   ℹ️  No progress file found (already reset)")
    
    # Also reset .env file if it exists (optional)
    env_file = ".env"
    if os.path.exists(env_file):
        try:
            # Create backup
            backup_file = ".env.backup"
            with open(env_file, 'r') as f:
                env_content = f.read()
            
            with open(backup_file, 'w') as f:
                f.write(env_content)
            
            # Clear API keys from .env
            lines = env_content.split('\n')
            cleared_lines = []
            for line in lines:
                if not any(key in line.upper() for key in ['API_KEY', 'OPENAI', 'GEMINI', 'ANTHROPIC', 'MISTRAL']):
                    cleared_lines.append(line)
            
            with open(env_file, 'w') as f:
                f.write('\n'.join(cleared_lines))
            
            print("   ✅ API keys cleared from .env file")
            print(f"   💾 Backup saved as {backup_file}")
            
        except Exception as e:
            print(f"   ⚠️  Warning: Could not reset .env file: {e}")
    
    print("\n✅ Onboarding progress reset complete!")
    print("\n📋 Next steps:")
    print("   1. Start the backend: python start.py")
    print("   2. Test the onboarding flow")
    print("   3. Check API endpoints at: http://localhost:8000/api/docs")
    
    return True

def show_test_instructions():
    """Show instructions for testing the onboarding flow."""
    
    print("\n🧪 Testing Instructions:")
    print("=" * 50)
    
    print("\n1. Start the backend:")
    print("   cd backend")
    print("   python start.py")
    
    print("\n2. Test the onboarding flow:")
    print("   - Open: http://localhost:8000/api/docs")
    print("   - Or use curl commands:")
    
    print("\n   # Check initial status")
    print("   curl http://localhost:8000/api/onboarding/status")
    
    print("\n   # Start onboarding")
    print("   curl -X POST http://localhost:8000/api/onboarding/start")
    
    print("\n   # Complete step 1 (AI LLM Providers)")
    print("   curl -X POST http://localhost:8000/api/onboarding/step/1/complete \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"data\": {\"api_keys\": [\"openai\"]}}'")
    
    print("\n   # Save an API key")
    print("   curl -X POST http://localhost:8000/api/onboarding/api-keys \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"provider\": \"openai\", \"api_key\": \"sk-test1234567890abcdef\"}'")
    
    print("\n   # Check progress")
    print("   curl http://localhost:8000/api/onboarding/progress")
    
    print("\n   # Complete final step")
    print("   curl -X POST http://localhost:8000/api/onboarding/step/6/complete \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"data\": {\"finalized\": true}}'")
    
    print("\n3. Run automated tests:")
    print("   python test_backend.py")

if __name__ == "__main__":
    print("🎯 ALwrity Onboarding Reset Tool")
    print("=" * 40)
    
    # Reset the progress
    success = reset_onboarding_progress()
    
    if success:
        # Show testing instructions
        show_test_instructions()
    else:
        print("\n❌ Failed to reset onboarding progress") 