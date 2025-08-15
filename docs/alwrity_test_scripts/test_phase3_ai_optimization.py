#!/usr/bin/env python3
"""
Test script for Phase 3 AI Prompt Optimization
Verifies that the AI Prompt Optimizer is working with advanced prompts and schemas.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

from services.ai_prompt_optimizer import AIPromptOptimizer
from services.content_gap_analyzer.ai_engine_service import AIEngineService
from loguru import logger

async def test_ai_prompt_optimizer():
    """Test the AI Prompt Optimizer functionality."""
    
    print("🔧 Testing AI Prompt Optimizer...")
    
    # Initialize the AI Prompt Optimizer
    ai_optimizer = AIPromptOptimizer()
    
    # Test 1: Strategic Content Gap Analysis
    print("\n📊 Test 1: Strategic Content Gap Analysis")
    analysis_data = {
        'target_url': 'example.com',
        'industry': 'technology',
        'serp_opportunities': 25,
        'expanded_keywords_count': 150,
        'competitors_analyzed': 5,
        'content_quality_score': 8.5,
        'competition_level': 'high',
        'dominant_themes': {
            'artificial_intelligence': 0.3,
            'machine_learning': 0.25,
            'data_science': 0.2,
            'automation': 0.15,
            'innovation': 0.1
        },
        'competitive_landscape': {
            'market_leader': 'competitor1.com',
            'content_leader': 'competitor2.com',
            'quality_leader': 'competitor3.com'
        }
    }
    
    try:
        result = await ai_optimizer.generate_strategic_content_gap_analysis(analysis_data)
        print(f"✅ Strategic content gap analysis completed")
        print(f"   - Strategic insights: {len(result.get('strategic_insights', []))}")
        print(f"   - Content recommendations: {len(result.get('content_recommendations', []))}")
        print(f"   - Keyword strategy: {bool(result.get('keyword_strategy'))}")
    except Exception as e:
        print(f"❌ Strategic content gap analysis failed: {str(e)}")
        return False
    
    # Test 2: Advanced Market Position Analysis
    print("\n🏢 Test 2: Advanced Market Position Analysis")
    market_data = {
        'industry': 'technology',
        'competitors': [
            {
                'url': 'competitor1.com',
                'content_score': 8.5,
                'quality_score': 9.0,
                'frequency': 'high'
            },
            {
                'url': 'competitor2.com',
                'content_score': 7.8,
                'quality_score': 8.2,
                'frequency': 'medium'
            }
        ],
        'market_size': 'Large',
        'growth_rate': '15%',
        'key_trends': ['AI adoption', 'Cloud migration', 'Digital transformation']
    }
    
    try:
        result = await ai_optimizer.generate_advanced_market_position_analysis(market_data)
        print(f"✅ Advanced market position analysis completed")
        print(f"   - Market leader: {result.get('market_leader', 'N/A')}")
        print(f"   - Market gaps: {len(result.get('market_gaps', []))}")
        print(f"   - Opportunities: {len(result.get('opportunities', []))}")
        print(f"   - Strategic recommendations: {len(result.get('strategic_recommendations', []))}")
    except Exception as e:
        print(f"❌ Advanced market position analysis failed: {str(e)}")
        return False
    
    # Test 3: Advanced Keyword Analysis
    print("\n🔍 Test 3: Advanced Keyword Analysis")
    keyword_data = {
        'industry': 'technology',
        'target_keywords': ['artificial intelligence', 'machine learning', 'data science'],
        'search_volume_data': {
            'artificial intelligence': 50000,
            'machine learning': 35000,
            'data science': 25000
        },
        'competition_analysis': {
            'artificial intelligence': 'high',
            'machine learning': 'medium',
            'data science': 'low'
        },
        'trend_analysis': {
            'artificial intelligence': 'rising',
            'machine learning': 'stable',
            'data science': 'rising'
        }
    }
    
    try:
        result = await ai_optimizer.generate_advanced_keyword_analysis(keyword_data)
        print(f"✅ Advanced keyword analysis completed")
        print(f"   - Keyword opportunities: {len(result.get('keyword_opportunities', []))}")
        print(f"   - Keyword clusters: {len(result.get('keyword_clusters', []))}")
    except Exception as e:
        print(f"❌ Advanced keyword analysis failed: {str(e)}")
        return False
    
    # Test 4: Health Check
    print("\n🏥 Test 4: Health Check")
    try:
        health_status = await ai_optimizer.health_check()
        print(f"✅ Health check completed")
        print(f"   - Service status: {health_status.get('status')}")
        print(f"   - Prompts loaded: {health_status.get('prompts_loaded')}")
        print(f"   - Schemas loaded: {health_status.get('schemas_loaded')}")
        print(f"   - AI integration: {health_status.get('capabilities', {}).get('ai_integration')}")
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False
    
    return True

async def test_ai_engine_integration():
    """Test the AI Engine Service integration with prompt optimizer."""
    
    print("\n🤖 Testing AI Engine Service Integration...")
    
    # Initialize the AI Engine Service
    ai_engine = AIEngineService()
    
    # Test 1: Content Gap Analysis with Advanced Prompts
    print("\n📊 Test 1: Content Gap Analysis with Advanced Prompts")
    analysis_summary = {
        'target_url': 'example.com',
        'industry': 'technology',
        'serp_opportunities': 25,
        'expanded_keywords_count': 150,
        'competitors_analyzed': 5,
        'dominant_themes': {
            'artificial_intelligence': 0.3,
            'machine_learning': 0.25,
            'data_science': 0.2
        }
    }
    
    try:
        result = await ai_engine.analyze_content_gaps(analysis_summary)
        print(f"✅ Content gap analysis with advanced prompts completed")
        print(f"   - Strategic insights: {len(result.get('strategic_insights', []))}")
        print(f"   - Content recommendations: {len(result.get('content_recommendations', []))}")
    except Exception as e:
        print(f"❌ Content gap analysis failed: {str(e)}")
        return False
    
    # Test 2: Market Position Analysis with Advanced Prompts
    print("\n🏢 Test 2: Market Position Analysis with Advanced Prompts")
    market_data = {
        'industry': 'technology',
        'competitors': [
            {
                'url': 'competitor1.com',
                'content_score': 8.5,
                'quality_score': 9.0
            },
            {
                'url': 'competitor2.com',
                'content_score': 7.8,
                'quality_score': 8.2
            }
        ]
    }
    
    try:
        result = await ai_engine.analyze_market_position(market_data)
        print(f"✅ Market position analysis with advanced prompts completed")
        print(f"   - Market leader: {result.get('market_leader', 'N/A')}")
        print(f"   - Market gaps: {len(result.get('market_gaps', []))}")
        print(f"   - Strategic recommendations: {len(result.get('strategic_recommendations', []))}")
    except Exception as e:
        print(f"❌ Market position analysis failed: {str(e)}")
        return False
    
    return True

async def test_ai_fallback_functionality():
    """Test the fallback functionality when AI fails."""
    
    print("\n🛡️ Testing AI Fallback Functionality...")
    
    # Initialize the AI Prompt Optimizer
    ai_optimizer = AIPromptOptimizer()
    
    # Test with invalid data to trigger fallback
    print("\n📊 Test: Fallback for Strategic Content Gap Analysis")
    invalid_data = {
        'invalid_field': 'invalid_value'
    }
    
    try:
        result = await ai_optimizer.generate_strategic_content_gap_analysis(invalid_data)
        print(f"✅ Fallback functionality working")
        print(f"   - Strategic insights: {len(result.get('strategic_insights', []))}")
        print(f"   - Content recommendations: {len(result.get('content_recommendations', []))}")
    except Exception as e:
        print(f"❌ Fallback functionality failed: {str(e)}")
        return False
    
    return True

async def main():
    """Main test function."""
    print("🚀 Starting Phase 3 AI Prompt Optimization Tests...")
    print("=" * 60)

    # Test 1: AI Prompt Optimizer
    ai_optimizer_success = await test_ai_prompt_optimizer()

    # Test 2: AI Engine Integration
    ai_engine_success = await test_ai_engine_integration()

    # Test 3: Fallback Functionality
    fallback_success = await test_ai_fallback_functionality()

    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"AI Prompt Optimizer: {'✅ PASSED' if ai_optimizer_success else '❌ FAILED'}")
    print(f"AI Engine Integration: {'✅ PASSED' if ai_engine_success else '❌ FAILED'}")
    print(f"Fallback Functionality: {'✅ PASSED' if fallback_success else '❌ FAILED'}")

    if ai_optimizer_success and ai_engine_success and fallback_success:
        print("\n🎉 All Phase 3 tests passed! AI Prompt Optimization is working correctly.")
        print("\n✅ Phase 3 Achievements:")
        print("   - Advanced AI prompts implemented")
        print("   - Comprehensive JSON schemas created")
        print("   - Expert-level AI instructions optimized")
        print("   - Robust error handling and fallbacks")
        print("   - AI engine service integration completed")
        return 0
    else:
        print("\n⚠️  Some Phase 3 tests failed. Please check the AI configuration.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 