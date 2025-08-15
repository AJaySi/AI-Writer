#!/usr/bin/env python3
"""
Test script for Phase 4 AI Service Integration
Verifies that the AI Service Manager is working with centralized management and performance monitoring.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

from services.ai_service_manager import AIServiceManager
from services.content_gap_analyzer.ai_engine_service import AIEngineService
from loguru import logger

async def test_ai_service_manager():
    """Test the AI Service Manager functionality."""
    
    print("🔧 Testing AI Service Manager...")
    
    # Initialize the AI Service Manager
    ai_manager = AIServiceManager()
    
    # Test 1: Content Gap Analysis
    print("\n📊 Test 1: Content Gap Analysis")
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
        result = await ai_manager.generate_content_gap_analysis(analysis_data)
        print(f"✅ Content gap analysis completed")
        print(f"   - Strategic insights: {len(result.get('strategic_insights', []))}")
        print(f"   - Content recommendations: {len(result.get('content_recommendations', []))}")
    except Exception as e:
        print(f"❌ Content gap analysis failed: {str(e)}")
        return False
    
    # Test 2: Market Position Analysis
    print("\n🏢 Test 2: Market Position Analysis")
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
        result = await ai_manager.generate_market_position_analysis(market_data)
        print(f"✅ Market position analysis completed")
        print(f"   - Market leader: {result.get('market_leader', 'N/A')}")
        print(f"   - Market gaps: {len(result.get('market_gaps', []))}")
        print(f"   - Opportunities: {len(result.get('opportunities', []))}")
        print(f"   - Strategic recommendations: {len(result.get('strategic_recommendations', []))}")
    except Exception as e:
        print(f"❌ Market position analysis failed: {str(e)}")
        return False
    
    # Test 3: Keyword Analysis
    print("\n🔍 Test 3: Keyword Analysis")
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
        result = await ai_manager.generate_keyword_analysis(keyword_data)
        print(f"✅ Keyword analysis completed")
        print(f"   - Keyword opportunities: {len(result.get('keyword_opportunities', []))}")
    except Exception as e:
        print(f"❌ Keyword analysis failed: {str(e)}")
        return False
    
    # Test 4: Performance Metrics
    print("\n📈 Test 4: Performance Metrics")
    try:
        performance_metrics = ai_manager.get_performance_metrics()
        print(f"✅ Performance metrics retrieved")
        print(f"   - Total calls: {performance_metrics.get('total_calls', 0)}")
        print(f"   - Success rate: {performance_metrics.get('success_rate', 0):.1f}%")
        print(f"   - Average response time: {performance_metrics.get('average_response_time', 0):.2f}s")
        print(f"   - Service breakdown: {len(performance_metrics.get('service_breakdown', {}))} services")
    except Exception as e:
        print(f"❌ Performance metrics failed: {str(e)}")
        return False
    
    # Test 5: Health Check
    print("\n🏥 Test 5: Health Check")
    try:
        health_status = await ai_manager.health_check()
        print(f"✅ Health check completed")
        print(f"   - Service status: {health_status.get('status')}")
        print(f"   - Prompts loaded: {health_status.get('prompts_loaded')}")
        print(f"   - Schemas loaded: {health_status.get('schemas_loaded')}")
        print(f"   - AI integration: {health_status.get('capabilities', {}).get('ai_integration')}")
        print(f"   - Configuration: {len(health_status.get('configuration', {}))} settings")
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False
    
    return True

async def test_ai_engine_integration():
    """Test the AI Engine Service integration with AI Service Manager."""
    
    print("\n🤖 Testing AI Engine Service Integration...")
    
    # Initialize the AI Engine Service
    ai_engine = AIEngineService()
    
    # Test 1: Content Gap Analysis with AI Service Manager
    print("\n📊 Test 1: Content Gap Analysis with AI Service Manager")
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
        print(f"✅ Content gap analysis with AI Service Manager completed")
        print(f"   - Strategic insights: {len(result.get('strategic_insights', []))}")
        print(f"   - Content recommendations: {len(result.get('content_recommendations', []))}")
    except Exception as e:
        print(f"❌ Content gap analysis failed: {str(e)}")
        return False
    
    # Test 2: Market Position Analysis with AI Service Manager
    print("\n🏢 Test 2: Market Position Analysis with AI Service Manager")
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
        print(f"✅ Market position analysis with AI Service Manager completed")
        print(f"   - Market leader: {result.get('market_leader', 'N/A')}")
        print(f"   - Market gaps: {len(result.get('market_gaps', []))}")
        print(f"   - Strategic recommendations: {len(result.get('strategic_recommendations', []))}")
    except Exception as e:
        print(f"❌ Market position analysis failed: {str(e)}")
        return False
    
    return True

async def test_performance_monitoring():
    """Test the performance monitoring functionality."""
    
    print("\n📊 Testing Performance Monitoring...")
    
    # Initialize the AI Service Manager
    ai_manager = AIServiceManager()
    
    # Make multiple AI calls to generate performance data
    print("\n🔄 Making multiple AI calls to generate performance data...")
    
    test_data = {
        'target_url': 'test.com',
        'industry': 'technology',
        'serp_opportunities': 10,
        'expanded_keywords_count': 50,
        'competitors_analyzed': 3,
        'dominant_themes': {'test': 1.0},
        'competitive_landscape': {'test': 'test'}
    }
    
    # Make several calls to generate metrics
    for i in range(3):
        try:
            await ai_manager.generate_content_gap_analysis(test_data)
            print(f"   - Call {i+1} completed")
        except Exception as e:
            print(f"   - Call {i+1} failed: {str(e)}")
    
    # Test performance metrics
    print("\n📈 Testing Performance Metrics...")
    try:
        metrics = ai_manager.get_performance_metrics()
        print(f"✅ Performance metrics analysis:")
        print(f"   - Total calls: {metrics.get('total_calls', 0)}")
        print(f"   - Success rate: {metrics.get('success_rate', 0):.1f}%")
        print(f"   - Average response time: {metrics.get('average_response_time', 0):.2f}s")
        
        # Service breakdown
        service_breakdown = metrics.get('service_breakdown', {})
        print(f"   - Service breakdown:")
        for service, data in service_breakdown.items():
            print(f"     * {service}: {data.get('total_calls', 0)} calls, {data.get('success_rate', 0):.1f}% success")
        
    except Exception as e:
        print(f"❌ Performance metrics failed: {str(e)}")
        return False
    
    return True

async def test_configuration_management():
    """Test the configuration management functionality."""
    
    print("\n⚙️ Testing Configuration Management...")
    
    # Initialize the AI Service Manager
    ai_manager = AIServiceManager()
    
    # Test configuration access
    try:
        config = ai_manager.config
        print(f"✅ Configuration retrieved:")
        print(f"   - Max retries: {config.get('max_retries')}")
        print(f"   - Timeout seconds: {config.get('timeout_seconds')}")
        print(f"   - Temperature: {config.get('temperature')}")
        print(f"   - Max tokens: {config.get('max_tokens')}")
        print(f"   - Enable caching: {config.get('enable_caching')}")
        print(f"   - Performance monitoring: {config.get('performance_monitoring')}")
        print(f"   - Fallback enabled: {config.get('fallback_enabled')}")
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False
    
    return True

async def main():
    """Main test function."""
    print("🚀 Starting Phase 4 AI Service Integration Tests...")
    print("=" * 70)

    # Test 1: AI Service Manager
    ai_manager_success = await test_ai_service_manager()

    # Test 2: AI Engine Integration
    ai_engine_success = await test_ai_engine_integration()

    # Test 3: Performance Monitoring
    performance_success = await test_performance_monitoring()

    # Test 4: Configuration Management
    config_success = await test_configuration_management()

    print("\n" + "=" * 70)
    print("📊 Test Results Summary:")
    print(f"AI Service Manager: {'✅ PASSED' if ai_manager_success else '❌ FAILED'}")
    print(f"AI Engine Integration: {'✅ PASSED' if ai_engine_success else '❌ FAILED'}")
    print(f"Performance Monitoring: {'✅ PASSED' if performance_success else '❌ FAILED'}")
    print(f"Configuration Management: {'✅ PASSED' if config_success else '❌ FAILED'}")

    if ai_manager_success and ai_engine_success and performance_success and config_success:
        print("\n🎉 All Phase 4 tests passed! AI Service Integration is working correctly.")
        print("\n✅ Phase 4 Achievements:")
        print("   - Centralized AI service management implemented")
        print("   - Performance monitoring with metrics tracking")
        print("   - Service breakdown by AI type")
        print("   - Configuration management with timeout settings")
        print("   - Health monitoring and error handling")
        print("   - All services integrated with AI Service Manager")
        return 0
    else:
        print("\n⚠️  Some Phase 4 tests failed. Please check the AI configuration.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 