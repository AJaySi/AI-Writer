#!/usr/bin/env python3
"""
Test script for AI Integration
Verifies that the AI Engine Service is working with real AI calls.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

from services.content_gap_analyzer.ai_engine_service import AIEngineService
from loguru import logger

async def test_ai_integration():
    """Test the AI integration functionality."""
    
    print("🤖 Testing AI Integration...")
    
    # Initialize the AI Engine Service
    ai_service = AIEngineService()
    
    # Test data
    test_analysis_summary = {
        'target_url': 'https://example.com',
        'industry': 'Technology',
        'serp_opportunities': 15,
        'expanded_keywords_count': 50,
        'competitors_analyzed': 5,
        'dominant_themes': {
            'artificial_intelligence': 0.3,
            'machine_learning': 0.25,
            'data_science': 0.2,
            'automation': 0.15,
            'innovation': 0.1
        }
    }
    
    test_market_data = {
        'industry': 'Technology',
        'competitors': [
            {
                'url': 'competitor1.com',
                'content_count': 150,
                'avg_quality_score': 8.5,
                'top_keywords': ['AI', 'ML', 'Data Science']
            },
            {
                'url': 'competitor2.com',
                'content_count': 200,
                'avg_quality_score': 7.8,
                'top_keywords': ['Automation', 'Innovation', 'Tech']
            }
        ]
    }
    
    try:
        print("\n1. Testing Content Gap Analysis...")
        content_gaps = await ai_service.analyze_content_gaps(test_analysis_summary)
        print(f"✅ Content Gap Analysis completed: {len(content_gaps.get('strategic_insights', []))} insights generated")
        
        print("\n2. Testing Market Position Analysis...")
        market_position = await ai_service.analyze_market_position(test_market_data)
        print(f"✅ Market Position Analysis completed: {len(market_position.get('strategic_recommendations', []))} recommendations generated")
        
        print("\n3. Testing Content Recommendations...")
        recommendations = await ai_service.generate_content_recommendations(test_analysis_summary)
        print(f"✅ Content Recommendations completed: {len(recommendations)} recommendations generated")
        
        print("\n4. Testing Performance Predictions...")
        predictions = await ai_service.predict_content_performance(test_analysis_summary)
        print(f"✅ Performance Predictions completed: {predictions.get('traffic_predictions', {}).get('confidence_level', 'N/A')} confidence")
        
        print("\n5. Testing Strategic Insights...")
        insights = await ai_service.generate_strategic_insights(test_analysis_summary)
        print(f"✅ Strategic Insights completed: {len(insights)} insights generated")
        
        print("\n6. Testing Health Check...")
        health = await ai_service.health_check()
        print(f"✅ Health Check completed: {health.get('status', 'unknown')} status")
        print(f"   AI Integration Status: {health.get('capabilities', {}).get('ai_integration', 'unknown')}")
        
        print("\n🎉 All AI Integration Tests Passed!")
        return True
        
    except Exception as e:
        print(f"❌ AI Integration Test Failed: {str(e)}")
        logger.error(f"AI Integration test failed: {str(e)}")
        return False

async def test_ai_fallback():
    """Test the fallback functionality when AI fails."""
    
    print("\n🔄 Testing AI Fallback Functionality...")
    
    # Initialize the AI Engine Service
    ai_service = AIEngineService()
    
    # Test with minimal data to trigger fallback
    minimal_data = {'test': 'data'}
    
    try:
        print("Testing fallback with minimal data...")
        result = await ai_service.analyze_content_gaps(minimal_data)
        
        if result and 'strategic_insights' in result:
            print("✅ Fallback functionality working correctly")
            return True
        else:
            print("❌ Fallback functionality failed")
            return False
            
    except Exception as e:
        print(f"❌ Fallback test failed: {str(e)}")
        return False

async def main():
    """Main test function."""
    print("🚀 Starting AI Integration Tests...")
    print("=" * 50)
    
    # Test 1: AI Integration
    ai_success = await test_ai_integration()
    
    # Test 2: Fallback Functionality
    fallback_success = await test_ai_fallback()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"AI Integration: {'✅ PASSED' if ai_success else '❌ FAILED'}")
    print(f"Fallback Functionality: {'✅ PASSED' if fallback_success else '❌ FAILED'}")
    
    if ai_success and fallback_success:
        print("\n🎉 All tests passed! AI Integration is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the AI configuration.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 