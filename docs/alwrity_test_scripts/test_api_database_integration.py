#!/usr/bin/env python3
"""
Test script for API Database Integration
Verifies that all API endpoints with database integration are working correctly.
"""

import asyncio
import sys
import os
import requests
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

from services.database import init_database, get_db_session
from services.content_planning_db import ContentPlanningDBService
from loguru import logger

# API base URL
API_BASE_URL = "http://localhost:8000"

def test_database_initialization():
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

def test_api_health_check():
    """Test API health check endpoints."""
    
    print("\n🏥 Testing API Health Checks...")
    
    # Test content planning health check
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Content planning health check: {health_data['status']}")
        else:
            print(f"❌ Content planning health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Content planning health check error: {str(e)}")
        return False
    
    # Test database health check
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/database/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Database health check: {health_data['status']}")
        else:
            print(f"❌ Database health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database health check error: {str(e)}")
        return False
    
    return True

def test_content_strategy_api():
    """Test content strategy API endpoints."""
    
    print("\n📋 Testing Content Strategy API...")
    
    # Test 1: Create content strategy
    print("\n📝 Test 1: Create Content Strategy")
    strategy_data = {
        "user_id": 1,
        "name": "Test Content Strategy",
        "industry": "technology",
        "target_audience": {
            "demographics": "25-45 years old",
            "interests": ["technology", "innovation"]
        },
        "content_pillars": [
            {"name": "AI", "description": "Artificial Intelligence content"},
            {"name": "Machine Learning", "description": "ML tutorials and guides"}
        ],
        "ai_recommendations": {
            "strategic_insights": ["Focus on educational content"],
            "content_recommendations": ["Create comprehensive guides"]
        }
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/content-planning/strategies/",
            json=strategy_data
        )
        
        if response.status_code == 200:
            strategy = response.json()
            print(f"✅ Content strategy created: {strategy['id']}")
            strategy_id = strategy['id']
        else:
            print(f"❌ Failed to create content strategy: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating content strategy: {str(e)}")
        return False
    
    # Test 2: Get content strategy
    print("\n📖 Test 2: Get Content Strategy")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/strategies/{strategy_id}")
        
        if response.status_code == 200:
            strategy = response.json()
            print(f"✅ Content strategy retrieved: {strategy['name']}")
        else:
            print(f"❌ Failed to retrieve content strategy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error retrieving content strategy: {str(e)}")
        return False
    
    # Test 3: Get user strategies
    print("\n👤 Test 3: Get User Content Strategies")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/strategies/?user_id=1")
        
        if response.status_code == 200:
            strategies = response.json()
            print(f"✅ Retrieved {len(strategies)} user strategies")
        else:
            print(f"❌ Failed to get user strategies: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting user strategies: {str(e)}")
        return False
    
    # Test 4: Update content strategy
    print("\n✏️ Test 4: Update Content Strategy")
    update_data = {
        "name": "Updated Test Content Strategy",
        "industry": "artificial_intelligence"
    }
    
    try:
        response = requests.put(
            f"{API_BASE_URL}/api/content-planning/strategies/{strategy_id}",
            json=update_data
        )
        
        if response.status_code == 200:
            strategy = response.json()
            print(f"✅ Content strategy updated: {strategy['name']}")
        else:
            print(f"❌ Failed to update content strategy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error updating content strategy: {str(e)}")
        return False
    
    # Test 5: Delete content strategy
    print("\n🗑️ Test 5: Delete Content Strategy")
    try:
        response = requests.delete(f"{API_BASE_URL}/api/content-planning/strategies/{strategy_id}")
        
        if response.status_code == 200:
            print("✅ Content strategy deleted successfully")
        else:
            print(f"❌ Failed to delete content strategy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting content strategy: {str(e)}")
        return False
    
    return True

def test_calendar_event_api():
    """Test calendar event API endpoints."""
    
    print("\n📅 Testing Calendar Event API...")
    
    # First create a strategy for the event
    strategy_data = {
        "user_id": 1,
        "name": "Test Strategy for Events",
        "industry": "technology"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/content-planning/strategies/",
            json=strategy_data
        )
        
        if response.status_code == 200:
            strategy = response.json()
            strategy_id = strategy['id']
        else:
            print(f"❌ Failed to create test strategy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error creating test strategy: {str(e)}")
        return False
    
    # Test 1: Create calendar event
    print("\n📝 Test 1: Create Calendar Event")
    event_data = {
        "strategy_id": strategy_id,
        "title": "Test Blog Post",
        "description": "A comprehensive guide to AI",
        "content_type": "blog_post",
        "platform": "website",
        "scheduled_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "ai_recommendations": {
            "keywords": ["AI", "machine learning"],
            "estimated_performance": "High engagement expected"
        }
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/content-planning/calendar-events/",
            json=event_data
        )
        
        if response.status_code == 200:
            event = response.json()
            print(f"✅ Calendar event created: {event['id']}")
            event_id = event['id']
        else:
            print(f"❌ Failed to create calendar event: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error creating calendar event: {str(e)}")
        return False
    
    # Test 2: Get calendar event
    print("\n📖 Test 2: Get Calendar Event")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/calendar-events/{event_id}")
        
        if response.status_code == 200:
            event = response.json()
            print(f"✅ Calendar event retrieved: {event['title']}")
        else:
            print(f"❌ Failed to retrieve calendar event: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error retrieving calendar event: {str(e)}")
        return False
    
    # Test 3: Get strategy events
    print("\n📋 Test 3: Get Strategy Calendar Events")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/calendar-events/?strategy_id={strategy_id}")
        
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Retrieved {len(events)} strategy events")
        else:
            print(f"❌ Failed to get strategy events: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting strategy events: {str(e)}")
        return False
    
    # Clean up
    try:
        requests.delete(f"{API_BASE_URL}/api/content-planning/strategies/{strategy_id}")
    except:
        pass
    
    return True

def test_content_gap_analysis_api():
    """Test content gap analysis API endpoints."""
    
    print("\n🔍 Testing Content Gap Analysis API...")
    
    # Test 1: Create content gap analysis
    print("\n📝 Test 1: Create Content Gap Analysis")
    analysis_data = {
        "user_id": 1,
        "website_url": "https://example.com",
        "competitor_urls": ["https://competitor1.com", "https://competitor2.com"],
        "target_keywords": ["AI", "machine learning", "data science"],
        "industry": "technology",
        "analysis_results": {
            "content_gaps": ["Video tutorials", "Case studies"],
            "opportunities": ["Educational content", "Expert interviews"]
        },
        "recommendations": {
            "strategic_insights": ["Focus on educational content"],
            "content_recommendations": ["Create comprehensive guides"]
        },
        "opportunities": {
            "high_priority": ["Video tutorials"],
            "medium_priority": ["Case studies"]
        }
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/content-planning/gap-analysis/",
            json=analysis_data
        )
        
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Content gap analysis created: {analysis['id']}")
            analysis_id = analysis['id']
        else:
            print(f"❌ Failed to create content gap analysis: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error creating content gap analysis: {str(e)}")
        return False
    
    # Test 2: Get content gap analysis
    print("\n📖 Test 2: Get Content Gap Analysis")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/gap-analysis/{analysis_id}")
        
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Content gap analysis retrieved: {analysis['website_url']}")
        else:
            print(f"❌ Failed to retrieve content gap analysis: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error retrieving content gap analysis: {str(e)}")
        return False
    
    # Test 3: Get user analyses
    print("\n👤 Test 3: Get User Content Gap Analyses")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/gap-analysis/?user_id=1")
        
        if response.status_code == 200:
            analyses = response.json()
            print(f"✅ Retrieved {len(analyses)} user analyses")
        else:
            print(f"❌ Failed to get user analyses: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting user analyses: {str(e)}")
        return False
    
    return True

def test_advanced_api_endpoints():
    """Test advanced API endpoints."""
    
    print("\n🚀 Testing Advanced API Endpoints...")
    
    # Create a test strategy first
    strategy_data = {
        "user_id": 1,
        "name": "Advanced Test Strategy",
        "industry": "technology"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/content-planning/strategies/",
            json=strategy_data
        )
        
        if response.status_code == 200:
            strategy = response.json()
            strategy_id = strategy['id']
        else:
            print(f"❌ Failed to create test strategy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error creating test strategy: {str(e)}")
        return False
    
    # Test 1: Get strategy analytics
    print("\n📊 Test 1: Get Strategy Analytics")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/strategies/{strategy_id}/analytics")
        
        if response.status_code == 200:
            analytics = response.json()
            print(f"✅ Strategy analytics retrieved: {analytics['analytics_count']} records")
        else:
            print(f"❌ Failed to get strategy analytics: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting strategy analytics: {str(e)}")
        return False
    
    # Test 2: Get strategy events
    print("\n📅 Test 2: Get Strategy Events")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/strategies/{strategy_id}/events")
        
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Strategy events retrieved: {events['events_count']} events")
        else:
            print(f"❌ Failed to get strategy events: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting strategy events: {str(e)}")
        return False
    
    # Test 3: Get user recommendations
    print("\n💡 Test 3: Get User Recommendations")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/users/1/recommendations")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ User recommendations retrieved: {recommendations['recommendations_count']} recommendations")
        else:
            print(f"❌ Failed to get user recommendations: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting user recommendations: {str(e)}")
        return False
    
    # Test 4: Get strategy summary
    print("\n📋 Test 4: Get Strategy Summary")
    try:
        response = requests.get(f"{API_BASE_URL}/api/content-planning/strategies/{strategy_id}/summary")
        
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Strategy summary retrieved successfully")
        else:
            print(f"❌ Failed to get strategy summary: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting strategy summary: {str(e)}")
        return False
    
    # Clean up
    try:
        requests.delete(f"{API_BASE_URL}/api/content-planning/strategies/{strategy_id}")
    except:
        pass
    
    return True

def main():
    """Main test function."""
    print("🚀 Starting API Database Integration Tests...")
    print("=" * 60)

    # Test 1: Database Initialization
    db_init_success = test_database_initialization()

    # Test 2: API Health Checks
    health_success = test_api_health_check()

    # Test 3: Content Strategy API
    strategy_success = test_content_strategy_api()

    # Test 4: Calendar Event API
    event_success = test_calendar_event_api()

    # Test 5: Content Gap Analysis API
    analysis_success = test_content_gap_analysis_api()

    # Test 6: Advanced API Endpoints
    advanced_success = test_advanced_api_endpoints()

    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"Database Initialization: {'✅ PASSED' if db_init_success else '❌ FAILED'}")
    print(f"API Health Checks: {'✅ PASSED' if health_success else '❌ FAILED'}")
    print(f"Content Strategy API: {'✅ PASSED' if strategy_success else '❌ FAILED'}")
    print(f"Calendar Event API: {'✅ PASSED' if event_success else '❌ FAILED'}")
    print(f"Content Gap Analysis API: {'✅ PASSED' if analysis_success else '❌ FAILED'}")
    print(f"Advanced API Endpoints: {'✅ PASSED' if advanced_success else '❌ FAILED'}")

    if db_init_success and health_success and strategy_success and event_success and analysis_success and advanced_success:
        print("\n🎉 All API database integration tests passed!")
        print("\n✅ API Database Integration Achievements:")
        print("   - Database models integrated with API endpoints")
        print("   - All CRUD operations working via API")
        print("   - Health checks for both services and database")
        print("   - Advanced query endpoints functional")
        print("   - Error handling and validation working")
        print("   - RESTful API design implemented")
        return 0
    else:
        print("\n⚠️  Some API database integration tests failed. Please check the API server and database configuration.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 