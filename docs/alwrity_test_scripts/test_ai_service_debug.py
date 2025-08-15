#!/usr/bin/env python3
"""
Test script to debug AI analytics service issues.
"""

import asyncio
import sys
import traceback
from datetime import datetime

# Add backend to path
sys.path.append('backend')

async def test_ai_analytics_service():
    """Test the AI analytics service directly."""
    try:
        print("🧪 Testing AI Analytics Service Directly")
        print("=" * 50)
        
        # Import the service
        from services.ai_analytics_service import AIAnalyticsService
        
        print("✅ AI Analytics Service imported successfully")
        
        # Create service instance
        ai_service = AIAnalyticsService()
        print("✅ AI Analytics Service instantiated")
        
        # Test performance trends analysis
        print("\n🧪 Testing performance trends analysis...")
        try:
            performance_analysis = await ai_service.analyze_performance_trends(
                strategy_id=1,
                metrics=['engagement_rate', 'reach', 'conversion_rate']
            )
            print(f"✅ Performance analysis completed: {len(performance_analysis)} keys")
            print(f"   - Keys: {list(performance_analysis.keys())}")
            
            if 'trend_analysis' in performance_analysis:
                print(f"   - Trend analysis: {len(performance_analysis['trend_analysis'])} metrics")
            else:
                print("   - No trend_analysis found")
                
        except Exception as e:
            print(f"❌ Performance analysis failed: {e}")
            print(f"   - Error type: {type(e).__name__}")
            traceback.print_exc()
        
        # Test strategic intelligence
        print("\n🧪 Testing strategic intelligence...")
        try:
            strategic_intelligence = await ai_service.generate_strategic_intelligence(
                strategy_id=1
            )
            print(f"✅ Strategic intelligence completed: {len(strategic_intelligence)} keys")
            print(f"   - Keys: {list(strategic_intelligence.keys())}")
            
        except Exception as e:
            print(f"❌ Strategic intelligence failed: {e}")
            print(f"   - Error type: {type(e).__name__}")
            traceback.print_exc()
        
        # Test content evolution
        print("\n🧪 Testing content evolution...")
        try:
            evolution_analysis = await ai_service.analyze_content_evolution(
                strategy_id=1,
                time_period="30d"
            )
            print(f"✅ Content evolution completed: {len(evolution_analysis)} keys")
            print(f"   - Keys: {list(evolution_analysis.keys())}")
            
        except Exception as e:
            print(f"❌ Content evolution failed: {e}")
            print(f"   - Error type: {type(e).__name__}")
            traceback.print_exc()
        
        print("\n" + "=" * 50)
        print("📊 AI Service Debug Complete")
        
    except Exception as e:
        print(f"❌ AI service test failed: {e}")
        traceback.print_exc()

async def test_ai_engine_service():
    """Test the AI engine service that AI analytics depends on."""
    try:
        print("\n🧪 Testing AI Engine Service")
        print("=" * 30)
        
        from services.content_gap_analyzer.ai_engine_service import AIEngineService
        
        print("✅ AI Engine Service imported successfully")
        
        # Create service instance
        ai_engine = AIEngineService()
        print("✅ AI Engine Service instantiated")
        
        # Test a simple AI call
        print("\n🧪 Testing simple AI call...")
        try:
            # Test with a simple prompt
            result = await ai_engine.generate_recommendations(
                website_analysis={"content_types": ["blog", "video"]},
                competitor_analysis={"top_performers": ["competitor1.com"]},
                gap_analysis={"content_gaps": ["AI content"]},
                keyword_analysis={"high_value_keywords": ["AI marketing"]}
            )
            print(f"✅ AI engine call completed: {type(result)}")
            print(f"   - Result: {result}")
            
        except Exception as e:
            print(f"❌ AI engine call failed: {e}")
            print(f"   - Error type: {type(e).__name__}")
            traceback.print_exc()
        
    except Exception as e:
        print(f"❌ AI engine test failed: {e}")
        traceback.print_exc()

async def main():
    """Run all AI service tests."""
    await test_ai_analytics_service()
    await test_ai_engine_service()

if __name__ == "__main__":
    asyncio.run(main()) 