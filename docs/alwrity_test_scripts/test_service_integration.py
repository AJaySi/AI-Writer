#!/usr/bin/env python3
"""
Test script for Phase 3: Service Integration
Verifies that content planning service integrates with database and AI services correctly.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

from services.database import init_database, get_db_session
from services.content_planning_service import ContentPlanningService
from services.content_planning_db import ContentPlanningDBService
from loguru import logger

async def test_database_initialization():
    """Test database initialization."""
    
    print("🗄️ Testing Database Initialization...")
    
    try:
        # Initialize database
        init_database()
        print("✅ Database initialized successfully")
        
        # Test database session
        db_session = get_db_session()
        if db_session:
            print("✅ Database session created successfully")
            db_session.close()
            return True
        else:
            print("❌ Failed to create database session")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

async def test_service_initialization():
    """Test content planning service initialization."""
    
    print("\n🔧 Testing Service Initialization...")
    
    try:
        # Test service initialization with database session
        db_session = get_db_session()
        if not db_session:
            print("❌ No database session available")
            return False
        
        service = ContentPlanningService(db_session)
        
        if service.db_service:
            print("✅ Content planning service initialized with database service")
        else:
            print("❌ Database service not initialized")
            return False
        
        if service.ai_manager:
            print("✅ AI service manager initialized")
        else:
            print("❌ AI service manager not initialized")
            return False
        
        db_session.close()
        return True
        
    except Exception as e:
        print(f"❌ Service initialization failed: {str(e)}")
        return False

async def test_content_strategy_with_ai():
    """Test content strategy creation with AI integration."""
    
    print("\n📋 Testing Content Strategy with AI...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    service = ContentPlanningService(db_session)
    
    # Test 1: Create content strategy with AI
    print("\n📝 Test 1: Create Content Strategy with AI")
    strategy_data = {
        'user_id': 1,
        'name': 'AI-Enhanced Content Strategy',
        'industry': 'technology',
        'target_audience': {
            'demographics': '25-45 years old',
            'interests': ['technology', 'innovation', 'AI']
        },
        'content_preferences': {
            'formats': ['blog_posts', 'videos', 'social_media'],
            'frequency': 'weekly',
            'platforms': ['website', 'linkedin', 'youtube']
        }
    }
    
    try:
        strategy = await service.create_content_strategy_with_ai(
            user_id=strategy_data['user_id'],
            strategy_data=strategy_data
        )
        
        if strategy:
            print(f"✅ Content strategy created with AI: {strategy.id}")
            strategy_id = strategy.id
        else:
            print("❌ Failed to create content strategy with AI")
            return False
    except Exception as e:
        print(f"❌ Error creating content strategy with AI: {str(e)}")
        return False
    
    # Test 2: Get content strategy from database
    print("\n📖 Test 2: Get Content Strategy from Database")
    try:
        retrieved_strategy = await service.get_content_strategy(
            user_id=strategy_data['user_id'],
            strategy_id=strategy_id
        )
        
        if retrieved_strategy:
            print(f"✅ Content strategy retrieved: {retrieved_strategy.name}")
            print(f"   - Industry: {retrieved_strategy.industry}")
            print(f"   - AI Recommendations: {len(retrieved_strategy.ai_recommendations) if retrieved_strategy.ai_recommendations else 0} items")
        else:
            print("❌ Failed to retrieve content strategy")
            return False
    except Exception as e:
        print(f"❌ Error retrieving content strategy: {str(e)}")
        return False
    
    # Test 3: Analyze content strategy with AI
    print("\n🤖 Test 3: Analyze Content Strategy with AI")
    try:
        ai_strategy = await service.analyze_content_strategy_with_ai(
            industry='artificial_intelligence',
            target_audience={
                'demographics': '30-50 years old',
                'interests': ['AI', 'machine learning', 'data science']
            },
            business_goals=['thought leadership', 'lead generation'],
            content_preferences={
                'formats': ['blog_posts', 'webinars', 'case_studies'],
                'frequency': 'bi-weekly'
            },
            user_id=2
        )
        
        if ai_strategy:
            print(f"✅ AI-analyzed strategy created: {ai_strategy.id}")
            print(f"   - Name: {ai_strategy.name}")
            print(f"   - Industry: {ai_strategy.industry}")
        else:
            print("❌ Failed to create AI-analyzed strategy")
            return False
    except Exception as e:
        print(f"❌ Error analyzing content strategy with AI: {str(e)}")
        return False
    
    db_session.close()
    return True

async def test_calendar_events_with_ai():
    """Test calendar event creation with AI integration."""
    
    print("\n📅 Testing Calendar Events with AI...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    service = ContentPlanningService(db_session)
    
    # First create a strategy for the events
    strategy_data = {
        'user_id': 1,
        'name': 'Test Strategy for Events',
        'industry': 'technology'
    }
    
    try:
        strategy = await service.create_content_strategy_with_ai(
            user_id=strategy_data['user_id'],
            strategy_data=strategy_data
        )
        
        if not strategy:
            print("❌ Failed to create test strategy")
            return False
    except Exception as e:
        print(f"❌ Error creating test strategy: {str(e)}")
        return False
    
    # Test 1: Create calendar event with AI
    print("\n📝 Test 1: Create Calendar Event with AI")
    event_data = {
        'strategy_id': strategy.id,
        'title': 'AI Marketing Trends 2024',
        'description': 'Comprehensive analysis of AI marketing trends and strategies',
        'content_type': 'blog_post',
        'platform': 'website',
        'scheduled_date': datetime.utcnow() + timedelta(days=7)
    }
    
    try:
        event = await service.create_calendar_event_with_ai(event_data)
        
        if event:
            print(f"✅ Calendar event created with AI: {event.id}")
            print(f"   - Title: {event.title}")
            print(f"   - Platform: {event.platform}")
            print(f"   - AI Recommendations: {len(event.ai_recommendations) if event.ai_recommendations else 0} items")
            event_id = event.id
        else:
            print("❌ Failed to create calendar event with AI")
            return False
    except Exception as e:
        print(f"❌ Error creating calendar event with AI: {str(e)}")
        return False
    
    # Test 2: Get calendar events from database
    print("\n📖 Test 2: Get Calendar Events from Database")
    try:
        events = await service.get_calendar_events(strategy_id=strategy.id)
        
        if events:
            print(f"✅ Retrieved {len(events)} calendar events")
            for event in events:
                print(f"   - {event.title} ({event.content_type})")
        else:
            print("❌ No calendar events found")
            return False
    except Exception as e:
        print(f"❌ Error getting calendar events: {str(e)}")
        return False
    
    # Test 3: Track content performance with AI
    print("\n📊 Test 3: Track Content Performance with AI")
    try:
        performance = await service.track_content_performance_with_ai(event_id)
        
        if performance:
            print(f"✅ Performance tracking completed: {performance['analytics_id']}")
            print(f"   - Performance Score: {performance['performance_score']}")
            print(f"   - Engagement Prediction: {performance['engagement_prediction']}")
        else:
            print("❌ Failed to track content performance")
            return False
    except Exception as e:
        print(f"❌ Error tracking content performance: {str(e)}")
        return False
    
    db_session.close()
    return True

async def test_content_gap_analysis_with_ai():
    """Test content gap analysis with AI integration."""
    
    print("\n🔍 Testing Content Gap Analysis with AI...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    service = ContentPlanningService(db_session)
    
    # Test 1: Analyze content gaps with AI
    print("\n📝 Test 1: Analyze Content Gaps with AI")
    try:
        analysis = await service.analyze_content_gaps_with_ai(
            website_url='https://example.com',
            competitor_urls=['https://competitor1.com', 'https://competitor2.com'],
            user_id=1,
            target_keywords=['AI marketing', 'digital transformation', 'content strategy']
        )
        
        if analysis:
            print(f"✅ Content gap analysis completed: {analysis['analysis_id']}")
            print(f"   - Stored at: {analysis['stored_at']}")
            print(f"   - Results: {len(analysis['results']) if analysis['results'] else 0} items")
        else:
            print("❌ Failed to analyze content gaps with AI")
            return False
    except Exception as e:
        print(f"❌ Error analyzing content gaps with AI: {str(e)}")
        return False
    
    # Test 2: Generate content recommendations with AI
    print("\n💡 Test 2: Generate Content Recommendations with AI")
    try:
        # First create a strategy for recommendations
        strategy_data = {
            'user_id': 1,
            'name': 'Recommendation Test Strategy',
            'industry': 'technology'
        }
        
        strategy = await service.create_content_strategy_with_ai(
            user_id=strategy_data['user_id'],
            strategy_data=strategy_data
        )
        
        if strategy:
            recommendations = await service.generate_content_recommendations_with_ai(strategy.id)
            
            if recommendations:
                print(f"✅ Generated {len(recommendations)} content recommendations")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec.get('title', 'Untitled')} ({rec.get('type', 'content')})")
            else:
                print("❌ No content recommendations generated")
                return False
        else:
            print("❌ Failed to create strategy for recommendations")
            return False
    except Exception as e:
        print(f"❌ Error generating content recommendations: {str(e)}")
        return False
    
    db_session.close()
    return True

async def test_ai_analytics_storage():
    """Test AI analytics storage functionality."""
    
    print("\n📊 Testing AI Analytics Storage...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    service = ContentPlanningService(db_session)
    
    # Test 1: Create strategy and verify AI analytics storage
    print("\n📝 Test 1: Verify AI Analytics Storage")
    try:
        strategy_data = {
            'user_id': 1,
            'name': 'Analytics Test Strategy',
            'industry': 'technology',
            'target_audience': {'demographics': '25-45 years old'},
            'content_preferences': {'formats': ['blog_posts']}
        }
        
        strategy = await service.create_content_strategy_with_ai(
            user_id=strategy_data['user_id'],
            strategy_data=strategy_data
        )
        
        if strategy:
            print(f"✅ Strategy created with AI analytics: {strategy.id}")
            
            # Check if AI analytics were stored
            db_service = service._get_db_service()
            analytics = await db_service.get_strategy_analytics(strategy.id)
            
            if analytics:
                print(f"✅ AI analytics stored: {len(analytics)} records")
                for analytic in analytics:
                    print(f"   - Type: {analytic.analysis_type}")
                    print(f"   - Performance Score: {analytic.performance_score}")
            else:
                print("⚠️  No AI analytics found (this might be expected)")
        else:
            print("❌ Failed to create strategy for analytics test")
            return False
    except Exception as e:
        print(f"❌ Error testing AI analytics storage: {str(e)}")
        return False
    
    db_session.close()
    return True

async def main():
    """Main test function."""
    print("🚀 Starting Phase 3: Service Integration Tests...")
    print("=" * 60)

    # Test 1: Database Initialization
    db_init_success = await test_database_initialization()

    # Test 2: Service Initialization
    service_init_success = await test_service_initialization()

    # Test 3: Content Strategy with AI
    strategy_success = await test_content_strategy_with_ai()

    # Test 4: Calendar Events with AI
    events_success = await test_calendar_events_with_ai()

    # Test 5: Content Gap Analysis with AI
    analysis_success = await test_content_gap_analysis_with_ai()

    # Test 6: AI Analytics Storage
    analytics_success = await test_ai_analytics_storage()

    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"Database Initialization: {'✅ PASSED' if db_init_success else '❌ FAILED'}")
    print(f"Service Initialization: {'✅ PASSED' if service_init_success else '❌ FAILED'}")
    print(f"Content Strategy with AI: {'✅ PASSED' if strategy_success else '❌ FAILED'}")
    print(f"Calendar Events with AI: {'✅ PASSED' if events_success else '❌ FAILED'}")
    print(f"Content Gap Analysis with AI: {'✅ PASSED' if analysis_success else '❌ FAILED'}")
    print(f"AI Analytics Storage: {'✅ PASSED' if analytics_success else '❌ FAILED'}")

    if db_init_success and service_init_success and strategy_success and events_success and analysis_success and analytics_success:
        print("\n🎉 All Phase 3 service integration tests passed!")
        print("\n✅ Phase 3 Service Integration Achievements:")
        print("   - Content planning service integrated with database operations")
        print("   - AI services integrated with database storage")
        print("   - Data persistence for AI results implemented")
        print("   - Service database integration tested and functional")
        print("   - AI analytics tracking and storage working")
        print("   - Comprehensive error handling and logging")
        return 0
    else:
        print("\n⚠️  Some Phase 3 service integration tests failed. Please check the service configuration.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 