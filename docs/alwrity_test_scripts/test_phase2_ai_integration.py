#!/usr/bin/env python3
"""
Test script for Phase 2 AI Integration
Verifies that the Keyword Researcher and Competitor Analyzer are working with real AI calls.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

from services.content_gap_analyzer.keyword_researcher import KeywordResearcher
from services.content_gap_analyzer.competitor_analyzer import CompetitorAnalyzer
from loguru import logger

async def test_keyword_researcher_ai():
    """Test the Keyword Researcher AI integration."""
    
    print("🔍 Testing Keyword Researcher AI Integration...")
    
    # Initialize the Keyword Researcher
    keyword_researcher = KeywordResearcher()
    
    # Test data
    test_industry = "Technology"
    test_url = "https://example.com"
    test_keywords = ["artificial intelligence", "machine learning", "data science"]
    
    try:
        print("\n1. Testing Keyword Analysis...")
        keyword_analysis = await keyword_researcher.analyze_keywords(test_industry, test_url, test_keywords)
        print(f"✅ Keyword Analysis completed: {len(keyword_analysis.get('insights', []))} insights generated")
        
        print("\n2. Testing Keyword Expansion...")
        keyword_expansion = await keyword_researcher.expand_keywords(test_keywords, test_industry)
        print(f"✅ Keyword Expansion completed: {len(keyword_expansion.get('expanded_keywords', []))} keywords expanded")
        
        print("\n3. Testing Search Intent Analysis...")
        intent_analysis = await keyword_researcher.analyze_search_intent(test_keywords)
        print(f"✅ Search Intent Analysis completed: {len(intent_analysis.get('intent_categories', {}))} intent categories")
        
        print("\n4. Testing Content Format Suggestions...")
        # Create mock AI insights for testing
        mock_ai_insights = {
            'keywords': test_keywords,
            'industry': test_industry,
            'trends': {'ai': 'rising', 'ml': 'stable'}
        }
        content_formats = await keyword_researcher._suggest_content_formats(mock_ai_insights)
        print(f"✅ Content Format Suggestions completed: {len(content_formats)} formats suggested")
        
        print("\n5. Testing Topic Clustering...")
        topic_clusters = await keyword_researcher._create_topic_clusters(mock_ai_insights)
        print(f"✅ Topic Clustering completed: {len(topic_clusters.get('topic_clusters', []))} clusters created")
        
        print("\n🎉 All Keyword Researcher AI Tests Passed!")
        return True
        
    except Exception as e:
        print(f"❌ Keyword Researcher AI Test Failed: {str(e)}")
        logger.error(f"Keyword Researcher AI test failed: {str(e)}")
        return False

async def test_competitor_analyzer_ai():
    """Test the Competitor Analyzer AI integration."""
    
    print("\n🏢 Testing Competitor Analyzer AI Integration...")
    
    # Initialize the Competitor Analyzer
    competitor_analyzer = CompetitorAnalyzer()
    
    # Test data
    test_competitor_urls = [
        "https://competitor1.com",
        "https://competitor2.com",
        "https://competitor3.com"
    ]
    test_industry = "Technology"
    
    try:
        print("\n1. Testing Competitor Analysis...")
        competitor_analysis = await competitor_analyzer.analyze_competitors(test_competitor_urls, test_industry)
        print(f"✅ Competitor Analysis completed: {len(competitor_analysis.get('competitors', []))} competitors analyzed")
        
        print("\n2. Testing Market Position Evaluation...")
        # Create mock competitor data for testing
        mock_competitors = [
            {
                'url': 'competitor1.com',
                'analysis': {
                    'content_count': 150,
                    'avg_quality_score': 8.5,
                    'top_keywords': ['AI', 'ML', 'Data Science']
                }
            },
            {
                'url': 'competitor2.com',
                'analysis': {
                    'content_count': 200,
                    'avg_quality_score': 7.8,
                    'top_keywords': ['Automation', 'Innovation', 'Tech']
                }
            }
        ]
        market_position = await competitor_analyzer._evaluate_market_position(mock_competitors, test_industry)
        print(f"✅ Market Position Evaluation completed: {len(market_position.get('strategic_recommendations', []))} recommendations")
        
        print("\n3. Testing Content Gap Identification...")
        content_gaps = await competitor_analyzer._identify_content_gaps(mock_competitors)
        print(f"✅ Content Gap Identification completed: {len(content_gaps)} gaps identified")
        
        print("\n4. Testing Competitive Insights Generation...")
        # Create mock analysis results for testing
        mock_analysis_results = {
            'competitors': mock_competitors,
            'market_position': market_position,
            'content_gaps': content_gaps,
            'industry': test_industry
        }
        competitive_insights = await competitor_analyzer._generate_competitive_insights(mock_analysis_results)
        print(f"✅ Competitive Insights Generation completed: {len(competitive_insights)} insights generated")
        
        print("\n🎉 All Competitor Analyzer AI Tests Passed!")
        return True
        
    except Exception as e:
        print(f"❌ Competitor Analyzer AI Test Failed: {str(e)}")
        logger.error(f"Competitor Analyzer AI test failed: {str(e)}")
        return False

async def test_ai_fallback_functionality():
    """Test the fallback functionality when AI fails."""
    
    print("\n🔄 Testing AI Fallback Functionality...")
    
    # Initialize services
    keyword_researcher = KeywordResearcher()
    competitor_analyzer = CompetitorAnalyzer()
    
    # Test with minimal data to trigger fallback
    minimal_data = {'test': 'data'}
    
    try:
        print("Testing Keyword Researcher fallback...")
        keyword_result = await keyword_researcher._analyze_keyword_trends("test", [])
        
        if keyword_result and 'trends' in keyword_result:
            print("✅ Keyword Researcher fallback working correctly")
        else:
            print("❌ Keyword Researcher fallback failed")
            return False
        
        print("Testing Competitor Analyzer fallback...")
        competitor_result = await competitor_analyzer._evaluate_market_position([], "test")
        
        if competitor_result and 'market_leader' in competitor_result:
            print("✅ Competitor Analyzer fallback working correctly")
        else:
            print("❌ Competitor Analyzer fallback failed")
            return False
        
        print("✅ All fallback functionality working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {str(e)}")
        return False

async def main():
    """Main test function."""
    print("🚀 Starting Phase 2 AI Integration Tests...")
    print("=" * 60)
    
    # Test 1: Keyword Researcher AI Integration
    keyword_success = await test_keyword_researcher_ai()
    
    # Test 2: Competitor Analyzer AI Integration
    competitor_success = await test_competitor_analyzer_ai()
    
    # Test 3: Fallback Functionality
    fallback_success = await test_ai_fallback_functionality()
    
    print("\n" + "=" * 60)
    print("📊 Phase 2 Test Results Summary:")
    print(f"Keyword Researcher AI: {'✅ PASSED' if keyword_success else '❌ FAILED'}")
    print(f"Competitor Analyzer AI: {'✅ PASSED' if competitor_success else '❌ FAILED'}")
    print(f"Fallback Functionality: {'✅ PASSED' if fallback_success else '❌ FAILED'}")
    
    if keyword_success and competitor_success and fallback_success:
        print("\n🎉 All Phase 2 tests passed! AI Integration is working correctly.")
        print("✅ Phase 2: Advanced AI Features COMPLETED")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the AI configuration.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 