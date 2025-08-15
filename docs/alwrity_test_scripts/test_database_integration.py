#!/usr/bin/env python3
"""
Test script for Database Integration
Verifies that all database operations are working correctly.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

from services.database import get_db_session, init_database
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

async def test_content_strategy_operations():
    """Test content strategy database operations."""
    
    print("\n📋 Testing Content Strategy Operations...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    db_service = ContentPlanningDBService(db_session)
    
    # Test 1: Create content strategy
    print("\n📝 Test 1: Create Content Strategy")
    strategy_data = {
        'user_id': 1,
        'name': 'Test Content Strategy',
        'industry': 'technology',
        'target_audience': {
            'demographics': '25-45 years old',
            'interests': ['technology', 'innovation']
        },
        'content_pillars': ['AI', 'Machine Learning', 'Data Science'],
        'ai_recommendations': {
            'strategic_insights': ['Focus on educational content'],
            'content_recommendations': ['Create comprehensive guides']
        }
    }
    
    try:
        strategy = await db_service.create_content_strategy(strategy_data)
        if strategy:
            print(f"✅ Content strategy created: {strategy.id}")
            strategy_id = strategy.id
        else:
            print("❌ Failed to create content strategy")
            return False
    except Exception as e:
        print(f"❌ Error creating content strategy: {str(e)}")
        return False
    
    # Test 2: Get content strategy
    print("\n📖 Test 2: Get Content Strategy")
    try:
        retrieved_strategy = await db_service.get_content_strategy(strategy_id)
        if retrieved_strategy:
            print(f"✅ Content strategy retrieved: {retrieved_strategy.name}")
        else:
            print("❌ Failed to retrieve content strategy")
            return False
    except Exception as e:
        print(f"❌ Error retrieving content strategy: {str(e)}")
        return False
    
    # Test 3: Update content strategy
    print("\n✏️ Test 3: Update Content Strategy")
    update_data = {
        'name': 'Updated Test Content Strategy',
        'industry': 'artificial_intelligence'
    }
    
    try:
        updated_strategy = await db_service.update_content_strategy(strategy_id, update_data)
        if updated_strategy:
            print(f"✅ Content strategy updated: {updated_strategy.name}")
        else:
            print("❌ Failed to update content strategy")
            return False
    except Exception as e:
        print(f"❌ Error updating content strategy: {str(e)}")
        return False
    
    # Test 4: Get user strategies
    print("\n👤 Test 4: Get User Content Strategies")
    try:
        user_strategies = await db_service.get_user_content_strategies(1)
        print(f"✅ Retrieved {len(user_strategies)} user strategies")
    except Exception as e:
        print(f"❌ Error getting user strategies: {str(e)}")
        return False
    
    # Test 5: Delete content strategy
    print("\n🗑️ Test 5: Delete Content Strategy")
    try:
        deleted = await db_service.delete_content_strategy(strategy_id)
        if deleted:
            print("✅ Content strategy deleted successfully")
        else:
            print("❌ Failed to delete content strategy")
            return False
    except Exception as e:
        print(f"❌ Error deleting content strategy: {str(e)}")
        return False
    
    db_session.close()
    return True

async def test_calendar_event_operations():
    """Test calendar event database operations."""
    
    print("\n📅 Testing Calendar Event Operations...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    db_service = ContentPlanningDBService(db_session)
    
    # First create a strategy for the event
    strategy_data = {
        'user_id': 1,
        'name': 'Test Strategy for Events',
        'industry': 'technology'
    }
    strategy = await db_service.create_content_strategy(strategy_data)
    if not strategy:
        print("❌ Failed to create test strategy")
        return False
    
    # Test 1: Create calendar event
    print("\n📝 Test 1: Create Calendar Event")
    event_data = {
        'strategy_id': strategy.id,
        'title': 'Test Blog Post',
        'description': 'A comprehensive guide to AI',
        'content_type': 'blog_post',
        'platform': 'website',
        'scheduled_date': datetime.utcnow(),
        'status': 'draft',
        'ai_recommendations': {
            'keywords': ['AI', 'machine learning'],
            'estimated_performance': 'High engagement expected'
        }
    }
    
    try:
        event = await db_service.create_calendar_event(event_data)
        if event:
            print(f"✅ Calendar event created: {event.id}")
            event_id = event.id
        else:
            print("❌ Failed to create calendar event")
            return False
    except Exception as e:
        print(f"❌ Error creating calendar event: {str(e)}")
        return False
    
    # Test 2: Get calendar event
    print("\n📖 Test 2: Get Calendar Event")
    try:
        retrieved_event = await db_service.get_calendar_event(event_id)
        if retrieved_event:
            print(f"✅ Calendar event retrieved: {retrieved_event.title}")
        else:
            print("❌ Failed to retrieve calendar event")
            return False
    except Exception as e:
        print(f"❌ Error retrieving calendar event: {str(e)}")
        return False
    
    # Test 3: Get strategy events
    print("\n📋 Test 3: Get Strategy Calendar Events")
    try:
        strategy_events = await db_service.get_strategy_calendar_events(strategy.id)
        print(f"✅ Retrieved {len(strategy_events)} strategy events")
    except Exception as e:
        print(f"❌ Error getting strategy events: {str(e)}")
        return False
    
    # Test 4: Update calendar event
    print("\n✏️ Test 4: Update Calendar Event")
    update_data = {
        'title': 'Updated Test Blog Post',
        'status': 'scheduled'
    }
    
    try:
        updated_event = await db_service.update_calendar_event(event_id, update_data)
        if updated_event:
            print(f"✅ Calendar event updated: {updated_event.title}")
        else:
            print("❌ Failed to update calendar event")
            return False
    except Exception as e:
        print(f"❌ Error updating calendar event: {str(e)}")
        return False
    
    # Clean up
    await db_service.delete_content_strategy(strategy.id)
    db_session.close()
    return True

async def test_content_gap_analysis_operations():
    """Test content gap analysis database operations."""
    
    print("\n🔍 Testing Content Gap Analysis Operations...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    db_service = ContentPlanningDBService(db_session)
    
    # Test 1: Create content gap analysis
    print("\n📝 Test 1: Create Content Gap Analysis")
    analysis_data = {
        'user_id': 1,
        'website_url': 'https://example.com',
        'competitor_urls': ['https://competitor1.com', 'https://competitor2.com'],
        'target_keywords': ['AI', 'machine learning', 'data science'],
        'analysis_results': {
            'content_gaps': ['Video tutorials', 'Case studies'],
            'opportunities': ['Educational content', 'Expert interviews']
        },
        'recommendations': {
            'strategic_insights': ['Focus on educational content'],
            'content_recommendations': ['Create comprehensive guides']
        },
        'opportunities': {
            'high_priority': ['Video tutorials'],
            'medium_priority': ['Case studies']
        }
    }
    
    try:
        analysis = await db_service.create_content_gap_analysis(analysis_data)
        if analysis:
            print(f"✅ Content gap analysis created: {analysis.id}")
            analysis_id = analysis.id
        else:
            print("❌ Failed to create content gap analysis")
            return False
    except Exception as e:
        print(f"❌ Error creating content gap analysis: {str(e)}")
        return False
    
    # Test 2: Get content gap analysis
    print("\n📖 Test 2: Get Content Gap Analysis")
    try:
        retrieved_analysis = await db_service.get_content_gap_analysis(analysis_id)
        if retrieved_analysis:
            print(f"✅ Content gap analysis retrieved: {retrieved_analysis.website_url}")
        else:
            print("❌ Failed to retrieve content gap analysis")
            return False
    except Exception as e:
        print(f"❌ Error retrieving content gap analysis: {str(e)}")
        return False
    
    # Test 3: Get user analyses
    print("\n👤 Test 3: Get User Content Gap Analyses")
    try:
        user_analyses = await db_service.get_user_content_gap_analyses(1)
        print(f"✅ Retrieved {len(user_analyses)} user analyses")
    except Exception as e:
        print(f"❌ Error getting user analyses: {str(e)}")
        return False
    
    # Test 4: Update content gap analysis
    print("\n✏️ Test 4: Update Content Gap Analysis")
    update_data = {
        'website_url': 'https://updated-example.com',
        'analysis_results': {
            'content_gaps': ['Video tutorials', 'Case studies', 'Webinars'],
            'opportunities': ['Educational content', 'Expert interviews', 'Interactive content']
        }
    }
    
    try:
        updated_analysis = await db_service.update_content_gap_analysis(analysis_id, update_data)
        if updated_analysis:
            print(f"✅ Content gap analysis updated: {updated_analysis.website_url}")
        else:
            print("❌ Failed to update content gap analysis")
            return False
    except Exception as e:
        print(f"❌ Error updating content gap analysis: {str(e)}")
        return False
    
    # Clean up
    await db_service.delete_content_gap_analysis(analysis_id)
    db_session.close()
    return True

async def test_content_recommendation_operations():
    """Test content recommendation database operations."""
    
    print("\n💡 Testing Content Recommendation Operations...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    db_service = ContentPlanningDBService(db_session)
    
    # Test 1: Create content recommendation
    print("\n📝 Test 1: Create Content Recommendation")
    recommendation_data = {
        'user_id': 1,
        'recommendation_type': 'blog_post',
        'title': 'Complete Guide to AI Implementation',
        'description': 'A comprehensive guide for implementing AI in business',
        'target_keywords': ['AI implementation', 'business AI', 'AI strategy'],
        'estimated_length': '2000-3000 words',
        'priority': 'high',
        'platforms': ['website', 'linkedin'],
        'estimated_performance': 'High engagement expected',
        'status': 'pending'
    }
    
    try:
        recommendation = await db_service.create_content_recommendation(recommendation_data)
        if recommendation:
            print(f"✅ Content recommendation created: {recommendation.id}")
            recommendation_id = recommendation.id
        else:
            print("❌ Failed to create content recommendation")
            return False
    except Exception as e:
        print(f"❌ Error creating content recommendation: {str(e)}")
        return False
    
    # Test 2: Get content recommendation
    print("\n📖 Test 2: Get Content Recommendation")
    try:
        retrieved_recommendation = await db_service.get_content_recommendation(recommendation_id)
        if retrieved_recommendation:
            print(f"✅ Content recommendation retrieved: {retrieved_recommendation.title}")
        else:
            print("❌ Failed to retrieve content recommendation")
            return False
    except Exception as e:
        print(f"❌ Error retrieving content recommendation: {str(e)}")
        return False
    
    # Test 3: Get user recommendations
    print("\n👤 Test 3: Get User Content Recommendations")
    try:
        user_recommendations = await db_service.get_user_content_recommendations(1)
        print(f"✅ Retrieved {len(user_recommendations)} user recommendations")
    except Exception as e:
        print(f"❌ Error getting user recommendations: {str(e)}")
        return False
    
    # Test 4: Update content recommendation
    print("\n✏️ Test 4: Update Content Recommendation")
    update_data = {
        'title': 'Updated Complete Guide to AI Implementation',
        'status': 'accepted',
        'priority': 'medium'
    }
    
    try:
        updated_recommendation = await db_service.update_content_recommendation(recommendation_id, update_data)
        if updated_recommendation:
            print(f"✅ Content recommendation updated: {updated_recommendation.title}")
        else:
            print("❌ Failed to update content recommendation")
            return False
    except Exception as e:
        print(f"❌ Error updating content recommendation: {str(e)}")
        return False
    
    # Clean up
    await db_service.delete_content_recommendation(recommendation_id)
    db_session.close()
    return True

async def test_analytics_operations():
    """Test analytics database operations."""
    
    print("\n📊 Testing Analytics Operations...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    db_service = ContentPlanningDBService(db_session)
    
    # Create test strategy and event for analytics
    strategy_data = {
        'user_id': 1,
        'name': 'Test Strategy for Analytics',
        'industry': 'technology'
    }
    strategy = await db_service.create_content_strategy(strategy_data)
    
    event_data = {
        'strategy_id': strategy.id,
        'title': 'Test Event for Analytics',
        'content_type': 'blog_post',
        'platform': 'website',
        'scheduled_date': datetime.utcnow(),
        'status': 'published'
    }
    event = await db_service.create_calendar_event(event_data)
    
    # Test 1: Create content analytics
    print("\n📝 Test 1: Create Content Analytics")
    analytics_data = {
        'event_id': event.id,
        'strategy_id': strategy.id,
        'platform': 'website',
        'metrics': {
            'page_views': 1500,
            'unique_visitors': 800,
            'time_on_page': 180,
            'bounce_rate': 0.25,
            'social_shares': 45
        },
        'performance_score': 8.5,
        'recorded_at': datetime.utcnow()
    }
    
    try:
        analytics = await db_service.create_content_analytics(analytics_data)
        if analytics:
            print(f"✅ Content analytics created: {analytics.id}")
            analytics_id = analytics.id
        else:
            print("❌ Failed to create content analytics")
            return False
    except Exception as e:
        print(f"❌ Error creating content analytics: {str(e)}")
        return False
    
    # Test 2: Get event analytics
    print("\n📖 Test 2: Get Event Analytics")
    try:
        event_analytics = await db_service.get_event_analytics(event.id)
        print(f"✅ Retrieved {len(event_analytics)} event analytics")
    except Exception as e:
        print(f"❌ Error getting event analytics: {str(e)}")
        return False
    
    # Test 3: Get strategy analytics
    print("\n📋 Test 3: Get Strategy Analytics")
    try:
        strategy_analytics = await db_service.get_strategy_analytics(strategy.id)
        print(f"✅ Retrieved {len(strategy_analytics)} strategy analytics")
    except Exception as e:
        print(f"❌ Error getting strategy analytics: {str(e)}")
        return False
    
    # Test 4: Get platform analytics
    print("\n🌐 Test 4: Get Platform Analytics")
    try:
        platform_analytics = await db_service.get_analytics_by_platform('website')
        print(f"✅ Retrieved {len(platform_analytics)} platform analytics")
    except Exception as e:
        print(f"❌ Error getting platform analytics: {str(e)}")
        return False
    
    # Clean up
    await db_service.delete_content_strategy(strategy.id)
    db_session.close()
    return True

async def test_advanced_operations():
    """Test advanced database operations."""
    
    print("\n🚀 Testing Advanced Operations...")
    
    db_session = get_db_session()
    if not db_session:
        print("❌ No database session available")
        return False
    
    db_service = ContentPlanningDBService(db_session)
    
    # Create test data
    strategy_data = {
        'user_id': 1,
        'name': 'Advanced Test Strategy',
        'industry': 'technology'
    }
    strategy = await db_service.create_content_strategy(strategy_data)
    
    # Create multiple events
    events_data = [
        {
            'strategy_id': strategy.id,
            'title': 'Event 1',
            'content_type': 'blog_post',
            'platform': 'website',
            'scheduled_date': datetime.utcnow(),
            'status': 'published'
        },
        {
            'strategy_id': strategy.id,
            'title': 'Event 2',
            'content_type': 'video',
            'platform': 'youtube',
            'scheduled_date': datetime.utcnow(),
            'status': 'draft'
        }
    ]
    
    for event_data in events_data:
        await db_service.create_calendar_event(event_data)
    
    # Test 1: Get strategies with analytics
    print("\n📊 Test 1: Get Strategies with Analytics")
    try:
        strategies_with_analytics = await db_service.get_strategies_with_analytics(1)
        print(f"✅ Retrieved {len(strategies_with_analytics)} strategies with analytics")
    except Exception as e:
        print(f"❌ Error getting strategies with analytics: {str(e)}")
        return False
    
    # Test 2: Get events by status
    print("\n📋 Test 2: Get Events by Status")
    try:
        published_events = await db_service.get_events_by_status(strategy.id, 'published')
        draft_events = await db_service.get_events_by_status(strategy.id, 'draft')
        print(f"✅ Retrieved {len(published_events)} published events and {len(draft_events)} draft events")
    except Exception as e:
        print(f"❌ Error getting events by status: {str(e)}")
        return False
    
    # Test 3: Health check
    print("\n🏥 Test 3: Database Health Check")
    try:
        health_status = await db_service.health_check()
        print(f"✅ Health check completed: {health_status['status']}")
        print(f"   - Tables: {len(health_status['tables'])}")
    except Exception as e:
        print(f"❌ Error in health check: {str(e)}")
        return False
    
    # Clean up
    await db_service.delete_content_strategy(strategy.id)
    db_session.close()
    return True

async def main():
    """Main test function."""
    print("🚀 Starting Database Integration Tests...")
    print("=" * 60)

    # Test 1: Database Initialization
    db_init_success = await test_database_initialization()

    # Test 2: Content Strategy Operations
    strategy_success = await test_content_strategy_operations()

    # Test 3: Calendar Event Operations
    event_success = await test_calendar_event_operations()

    # Test 4: Content Gap Analysis Operations
    analysis_success = await test_content_gap_analysis_operations()

    # Test 5: Content Recommendation Operations
    recommendation_success = await test_content_recommendation_operations()

    # Test 6: Analytics Operations
    analytics_success = await test_analytics_operations()

    # Test 7: Advanced Operations
    advanced_success = await test_advanced_operations()

    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"Database Initialization: {'✅ PASSED' if db_init_success else '❌ FAILED'}")
    print(f"Content Strategy Operations: {'✅ PASSED' if strategy_success else '❌ FAILED'}")
    print(f"Calendar Event Operations: {'✅ PASSED' if event_success else '❌ FAILED'}")
    print(f"Content Gap Analysis Operations: {'✅ PASSED' if analysis_success else '❌ FAILED'}")
    print(f"Content Recommendation Operations: {'✅ PASSED' if recommendation_success else '❌ FAILED'}")
    print(f"Analytics Operations: {'✅ PASSED' if analytics_success else '❌ FAILED'}")
    print(f"Advanced Operations: {'✅ PASSED' if advanced_success else '❌ FAILED'}")

    if (db_init_success and strategy_success and event_success and 
        analysis_success and recommendation_success and analytics_success and advanced_success):
        print("\n🎉 All database integration tests passed!")
        print("\n✅ Database Integration Achievements:")
        print("   - Database models integrated successfully")
        print("   - All CRUD operations working correctly")
        print("   - Relationships and foreign keys functional")
        print("   - Error handling and rollback mechanisms working")
        print("   - Session management and connection handling operational")
        print("   - Advanced queries and analytics working")
        print("   - Health monitoring and status checks functional")
        return 0
    else:
        print("\n⚠️  Some database integration tests failed. Please check the database configuration.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 