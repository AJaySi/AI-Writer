#!/usr/bin/env python3
"""
Test script to verify all imports work correctly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports"""
    try:
        print("Testing imports...")
        
        # Test database imports
        print("Testing database imports...")
        from services.database import init_database, get_db_session
        print("✅ Database imports successful")
        
        # Test model imports
        print("Testing model imports...")
        from models.monitoring_models import StrategyMonitoringPlan, MonitoringTask
        from models.enhanced_strategy_models import EnhancedContentStrategy
        print("✅ Model imports successful")
        
        # Test service imports
        print("Testing service imports...")
        from services.strategy_service import StrategyService
        from services.monitoring_plan_generator import MonitoringPlanGenerator
        print("✅ Service imports successful")
        
        # Test LLM provider imports
        print("Testing LLM provider imports...")
        from services.llm_providers.anthropic_provider import anthropic_text_response
        print("✅ LLM provider imports successful")
        
        # Test API route imports
        print("Testing API route imports...")
        from api.content_planning.monitoring_routes import router as monitoring_router
        print("✅ API route imports successful")
        
        print("🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
