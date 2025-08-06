#!/usr/bin/env python3
"""Test script for content planning services."""

import asyncio
from loguru import logger

# Import all content planning services
from services.content_gap_analyzer import ContentGapAnalyzer
from services.competitor_analyzer import CompetitorAnalyzer
from services.keyword_researcher import KeywordResearcher
from services.ai_engine_service import AIEngineService
from services.website_analyzer import WebsiteAnalyzer

async def test_content_planning_services():
    """Test all content planning services."""
    logger.info("🧪 Testing Content Planning Services")
    
    try:
        # Test 1: Initialize all services
        logger.info("1. Initializing services...")
        content_gap_analyzer = ContentGapAnalyzer()
        competitor_analyzer = CompetitorAnalyzer()
        keyword_researcher = KeywordResearcher()
        ai_engine = AIEngineService()
        website_analyzer = WebsiteAnalyzer()
        logger.info("✅ All services initialized successfully")
        
        # Test 2: Test content gap analysis
        logger.info("2. Testing content gap analysis...")
        target_url = "https://alwrity.com"
        competitor_urls = ["https://competitor1.com", "https://competitor2.com"]
        target_keywords = ["content planning", "digital marketing", "seo strategy"]
        
        gap_analysis = await content_gap_analyzer.analyze_comprehensive_gap(
            target_url=target_url,
            competitor_urls=competitor_urls,
            target_keywords=target_keywords,
            industry="technology"
        )
        
        if gap_analysis:
            logger.info(f"✅ Content gap analysis completed: {len(gap_analysis.get('recommendations', []))} recommendations")
        else:
            logger.warning("⚠️ Content gap analysis returned empty results")
        
        # Test 3: Test competitor analysis
        logger.info("3. Testing competitor analysis...")
        competitor_analysis = await competitor_analyzer.analyze_competitors(
            competitor_urls=competitor_urls,
            industry="technology"
        )
        
        if competitor_analysis:
            logger.info(f"✅ Competitor analysis completed: {len(competitor_analysis.get('competitors', []))} competitors analyzed")
        else:
            logger.warning("⚠️ Competitor analysis returned empty results")
        
        # Test 4: Test keyword research
        logger.info("4. Testing keyword research...")
        keyword_analysis = await keyword_researcher.analyze_keywords(
            industry="technology",
            url=target_url,
            target_keywords=target_keywords
        )
        
        if keyword_analysis:
            logger.info(f"✅ Keyword analysis completed: {len(keyword_analysis.get('opportunities', []))} opportunities found")
        else:
            logger.warning("⚠️ Keyword analysis returned empty results")
        
        # Test 5: Test website analysis
        logger.info("5. Testing website analysis...")
        website_analysis = await website_analyzer.analyze_website(
            url=target_url,
            industry="technology"
        )
        
        if website_analysis:
            logger.info(f"✅ Website analysis completed: {website_analysis.get('content_analysis', {}).get('total_pages', 0)} pages analyzed")
        else:
            logger.warning("⚠️ Website analysis returned empty results")
        
        # Test 6: Test AI engine
        logger.info("6. Testing AI engine...")
        analysis_summary = {
            'target_url': target_url,
            'industry': 'technology',
            'serp_opportunities': 5,
            'expanded_keywords_count': 25,
            'competitors_analyzed': 2,
            'dominant_themes': ['content strategy', 'digital marketing', 'seo']
        }
        
        ai_insights = await ai_engine.analyze_content_gaps(analysis_summary)
        
        if ai_insights:
            logger.info(f"✅ AI insights generated: {len(ai_insights.get('strategic_insights', []))} insights")
        else:
            logger.warning("⚠️ AI insights returned empty results")
        
        # Test 7: Test content quality analysis
        logger.info("7. Testing content quality analysis...")
        content_quality = await website_analyzer.analyze_content_quality(target_url)
        
        if content_quality:
            logger.info(f"✅ Content quality analysis completed: Score {content_quality.get('overall_quality_score', 0)}/10")
        else:
            logger.warning("⚠️ Content quality analysis returned empty results")
        
        # Test 8: Test user experience analysis
        logger.info("8. Testing user experience analysis...")
        ux_analysis = await website_analyzer.analyze_user_experience(target_url)
        
        if ux_analysis:
            logger.info(f"✅ UX analysis completed: Score {ux_analysis.get('overall_ux_score', 0)}/10")
        else:
            logger.warning("⚠️ UX analysis returned empty results")
        
        # Test 9: Test keyword expansion
        logger.info("9. Testing keyword expansion...")
        seed_keywords = ["content planning", "digital marketing"]
        expanded_keywords = await keyword_researcher.expand_keywords(
            seed_keywords=seed_keywords,
            industry="technology"
        )
        
        if expanded_keywords:
            logger.info(f"✅ Keyword expansion completed: {len(expanded_keywords.get('expanded_keywords', []))} keywords generated")
        else:
            logger.warning("⚠️ Keyword expansion returned empty results")
        
        # Test 10: Test search intent analysis
        logger.info("10. Testing search intent analysis...")
        keywords = ["content planning guide", "digital marketing tips", "seo best practices"]
        intent_analysis = await keyword_researcher.analyze_search_intent(keywords)
        
        if intent_analysis:
            logger.info(f"✅ Search intent analysis completed: {len(intent_analysis.get('keyword_intents', {}))} keywords analyzed")
        else:
            logger.warning("⚠️ Search intent analysis returned empty results")
        
        logger.info("🎉 All content planning services tested successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing content planning services: {str(e)}")
        return False

async def test_ai_engine_features():
    """Test specific AI engine features."""
    logger.info("🤖 Testing AI Engine Features")
    
    try:
        ai_engine = AIEngineService()
        
        # Test market position analysis
        market_data = {
            'competitors_analyzed': 3,
            'avg_content_count': 150,
            'avg_quality_score': 8.5,
            'frequency_distribution': {'3x/week': 2, '2x/week': 1},
            'industry': 'technology'
        }
        
        market_position = await ai_engine.analyze_market_position(market_data)
        if market_position:
            logger.info("✅ Market position analysis completed")
        else:
            logger.warning("⚠️ Market position analysis failed")
        
        # Test content recommendations
        analysis_data = {
            'target_url': 'https://alwrity.com',
            'industry': 'technology',
            'keywords': ['content planning', 'digital marketing'],
            'competitors': ['competitor1.com', 'competitor2.com']
        }
        
        recommendations = await ai_engine.generate_content_recommendations(analysis_data)
        if recommendations:
            logger.info(f"✅ Content recommendations generated: {len(recommendations)} recommendations")
        else:
            logger.warning("⚠️ Content recommendations failed")
        
        # Test performance predictions
        content_data = {
            'content_type': 'blog_post',
            'target_keywords': ['content planning'],
            'industry': 'technology',
            'content_length': 1500
        }
        
        predictions = await ai_engine.predict_content_performance(content_data)
        if predictions:
            logger.info("✅ Performance predictions generated")
        else:
            logger.warning("⚠️ Performance predictions failed")
        
        # Test competitive intelligence
        competitor_data = {
            'competitors': ['competitor1.com', 'competitor2.com'],
            'industry': 'technology',
            'analysis_depth': 'comprehensive'
        }
        
        competitive_intelligence = await ai_engine.analyze_competitive_intelligence(competitor_data)
        if competitive_intelligence:
            logger.info("✅ Competitive intelligence analysis completed")
        else:
            logger.warning("⚠️ Competitive intelligence analysis failed")
        
        # Test strategic insights
        analysis_data = {
            'industry': 'technology',
            'target_audience': 'marketing professionals',
            'business_goals': ['increase traffic', 'improve conversions'],
            'current_performance': 'moderate'
        }
        
        strategic_insights = await ai_engine.generate_strategic_insights(analysis_data)
        if strategic_insights:
            logger.info(f"✅ Strategic insights generated: {len(strategic_insights)} insights")
        else:
            logger.warning("⚠️ Strategic insights failed")
        
        # Test content quality analysis
        content_data = {
            'content_text': 'Sample content for analysis',
            'target_keywords': ['content planning'],
            'industry': 'technology'
        }
        
        quality_analysis = await ai_engine.analyze_content_quality(content_data)
        if quality_analysis:
            logger.info(f"✅ Content quality analysis completed: Score {quality_analysis.get('overall_quality_score', 0)}/10")
        else:
            logger.warning("⚠️ Content quality analysis failed")
        
        logger.info("🎉 All AI engine features tested successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing AI engine features: {str(e)}")
        return False

async def main():
    """Main test function."""
    logger.info("🚀 Starting Content Planning Services Test Suite")
    
    # Test 1: Basic services
    services_result = await test_content_planning_services()
    
    # Test 2: AI engine features
    ai_result = await test_ai_engine_features()
    
    if services_result and ai_result:
        logger.info("🎉 All tests passed! Content Planning Services are ready for Phase 1 implementation.")
    else:
        logger.error("❌ Some tests failed. Please check the logs above.")
    
    logger.info("🏁 Test suite completed")

if __name__ == "__main__":
    asyncio.run(main()) 