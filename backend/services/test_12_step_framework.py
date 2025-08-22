"""
Test Script for 12-Step Prompt Chaining Framework

This script tests the basic functionality of the 12-step prompt chaining framework.
"""

import asyncio
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calendar_generation_datasource_framework.prompt_chaining import PromptChainOrchestrator


async def test_12_step_framework():
    """Test the 12-step prompt chaining framework."""
    print("🚀 Testing 12-Step Prompt Chaining Framework")
    print("=" * 50)
    
    try:
        # Initialize the orchestrator
        print("📋 Initializing Prompt Chain Orchestrator...")
        orchestrator = PromptChainOrchestrator()
        
        # Test health status
        print("\n🏥 Testing Health Status...")
        health_status = await orchestrator.get_health_status()
        print(f"✅ Health Status: {health_status}")
        
        # Test calendar generation
        print("\n🎯 Testing Calendar Generation...")
        result = await orchestrator.generate_calendar(
            user_id=1,
            strategy_id=123,
            calendar_type="monthly",
            industry="technology",
            business_size="sme"
        )
        
        print(f"✅ Calendar Generation Result:")
        print(f"   - Status: {result.get('status')}")
        print(f"   - Processing Time: {result.get('processing_time', 0):.2f}s")
        print(f"   - Quality Score: {result.get('quality_score', 0):.2f}")
        print(f"   - Framework Version: {result.get('framework_version')}")
        
        # Test progress tracking
        print("\n📊 Testing Progress Tracking...")
        progress = await orchestrator.get_progress()
        print(f"✅ Progress: {progress.get('completed_steps')}/{progress.get('total_steps')} steps completed")
        print(f"   - Progress Percentage: {progress.get('progress_percentage', 0):.1f}%")
        print(f"   - Current Phase: {progress.get('current_phase')}")
        print(f"   - Overall Quality Score: {progress.get('overall_quality_score', 0):.2f}")
        
        # Test step details
        print("\n🔍 Testing Step Details...")
        step_details = progress.get('step_details', {})
        for step_name, step_data in step_details.items():
            print(f"   - {step_name}: {step_data.get('status')} (Quality: {step_data.get('quality_score', 0):.2f})")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_individual_components():
    """Test individual components of the framework."""
    print("\n🔧 Testing Individual Components")
    print("=" * 50)
    
    try:
        from calendar_generation_datasource_framework.prompt_chaining import (
            StepManager, ContextManager, ProgressTracker, ErrorHandler
        )
        
        # Test Step Manager
        print("\n🎯 Testing Step Manager...")
        step_manager = StepManager()
        health_status = step_manager.get_health_status()
        print(f"✅ Step Manager Health: {health_status}")
        
        # Test Context Manager
        print("\n📋 Testing Context Manager...")
        context_manager = ContextManager()
        health_status = context_manager.get_health_status()
        print(f"✅ Context Manager Health: {health_status}")
        
        # Test Progress Tracker
        print("\n📊 Testing Progress Tracker...")
        progress_tracker = ProgressTracker()
        health_status = progress_tracker.get_health_status()
        print(f"✅ Progress Tracker Health: {health_status}")
        
        # Test Error Handler
        print("\n🛡️ Testing Error Handler...")
        error_handler = ErrorHandler()
        health_status = error_handler.get_health_status()
        print(f"✅ Error Handler Health: {health_status}")
        
        print("\n✅ All component tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Component test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    print("🧪 12-Step Prompt Chaining Framework Test Suite")
    print("=" * 60)
    
    # Test individual components
    component_success = await test_individual_components()
    
    # Test full framework
    framework_success = await test_12_step_framework()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 30)
    print(f"✅ Individual Components: {'PASSED' if component_success else 'FAILED'}")
    print(f"✅ Full Framework: {'PASSED' if framework_success else 'FAILED'}")
    
    if component_success and framework_success:
        print("\n🎉 All tests passed! The 12-step framework is ready for implementation.")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")


if __name__ == "__main__":
    asyncio.run(main())
