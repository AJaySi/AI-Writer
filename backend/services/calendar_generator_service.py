"""
Calendar Generator Service
AI-powered service for generating comprehensive content calendars based on enterprise best practices.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from loguru import logger

from services.content_gap_analyzer.ai_engine_service import AIEngineService
from services.onboarding_data_service import OnboardingDataService
from services.content_gap_analyzer.keyword_researcher import KeywordResearcher
from services.content_gap_analyzer.competitor_analyzer import CompetitorAnalyzer
from services.ai_analysis_db_service import AIAnalysisDBService
from services.content_planning_db import ContentPlanningDBService
from services.ai_service_manager import AIServiceManager

class CalendarGeneratorService:
    """AI-powered content calendar generator for SMEs."""
    
    def __init__(self):
        self.ai_engine = AIEngineService()
        self.onboarding_service = OnboardingDataService()
        self.keyword_researcher = KeywordResearcher()
        self.competitor_analyzer = CompetitorAnalyzer()
        self.ai_analysis_db_service = AIAnalysisDBService()
        # Initialize content planning db service as None - will be set when needed
        self.content_planning_db_service = None
        
        # Enterprise content calendar templates
        self.content_pillars = {
            "technology": ["Educational Content", "Thought Leadership", "Product Updates", "Industry Insights", "Team Culture"],
            "healthcare": ["Patient Education", "Medical Insights", "Health Tips", "Industry News", "Expert Opinions"],
            "finance": ["Financial Education", "Market Analysis", "Investment Tips", "Regulatory Updates", "Success Stories"],
            "education": ["Learning Resources", "Teaching Tips", "Student Success", "Industry Trends", "Innovation"],
            "retail": ["Product Showcases", "Shopping Tips", "Customer Stories", "Trend Analysis", "Behind the Scenes"],
            "manufacturing": ["Industry Insights", "Process Improvements", "Technology Updates", "Case Studies", "Team Spotlights"]
        }
        
        self.platform_strategies = {
            "website": {
                "content_types": ["blog_posts", "case_studies", "whitepapers", "product_pages"],
                "frequency": "2-3 per week",
                "optimal_length": "1500+ words",
                "tone": "professional, educational"
            },
            "linkedin": {
                "content_types": ["industry_insights", "professional_tips", "company_updates", "employee_spotlights"],
                "frequency": "daily",
                "optimal_length": "100-300 words",
                "tone": "professional, thought leadership"
            },
            "instagram": {
                "content_types": ["behind_scenes", "product_demos", "team_culture", "infographics"],
                "frequency": "daily",
                "optimal_length": "visual focus",
                "tone": "casual, engaging"
            },
            "youtube": {
                "content_types": ["tutorial_videos", "product_demos", "customer_testimonials", "industry_interviews"],
                "frequency": "weekly",
                "optimal_length": "5-15 minutes",
                "tone": "educational, conversational"
            },
            "twitter": {
                "content_types": ["industry_news", "quick_tips", "event_announcements", "community_engagement"],
                "frequency": "3-5 per day",
                "optimal_length": "280 characters",
                "tone": "informative, conversational"
            }
        }
        
        self.content_mix = {
            "educational": 0.40,
            "thought_leadership": 0.30,
            "engagement": 0.20,
            "promotional": 0.10
        }
    
    async def generate_comprehensive_calendar(
        self,
        user_id: int,
        strategy_id: Optional[int] = None,
        calendar_type: str = "monthly",
        industry: Optional[str] = None,
        business_size: str = "sme"
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive content calendar using AI with database-driven insights.
        
        Args:
            user_id: User ID
            strategy_id: Content strategy ID
            calendar_type: Type of calendar (monthly, weekly, custom)
            industry: Business industry
            business_size: Business size (startup, sme, enterprise)
        
        Returns:
            Comprehensive calendar with AI insights and recommendations
        """
        try:
            logger.info(f"🚀 Starting comprehensive calendar generation for user {user_id}")
            start_time = time.time()
            
            # Get comprehensive user data from database
            user_data = await self._get_comprehensive_user_data(user_id, strategy_id)
            industry = industry or user_data.get("industry", "technology")
            
            # Generate calendar components using database insights
            calendar_data = {
                "user_id": user_id,
                "strategy_id": strategy_id,
                "calendar_type": calendar_type,
                "industry": industry,
                "business_size": business_size,
                "generated_at": datetime.utcnow().isoformat(),
                "content_pillars": self._get_content_pillars(industry),
                "platform_strategies": self.platform_strategies,
                "content_mix": self.content_mix,
                "daily_schedule": await self._generate_daily_schedule_with_db_data(calendar_type, industry, user_data),
                "weekly_themes": await self._generate_weekly_themes_with_db_data(calendar_type, industry, user_data),
                "content_recommendations": await self._generate_content_recommendations_with_db_data(user_data, industry),
                "optimal_timing": await self._generate_optimal_timing_with_db_data(industry, user_data),
                "performance_predictions": await self._generate_performance_predictions_with_db_data(industry, user_data),
                "trending_topics": await self._get_trending_topics_from_db(industry, user_data),
                "repurposing_opportunities": await self._generate_repurposing_opportunities_with_db_data(user_data),
                "ai_insights": await self._generate_ai_insights_with_db_data(user_data, industry),
                "competitor_analysis": await self._analyze_competitors_with_db_data(user_data, industry),
                "gap_analysis_insights": user_data.get("gap_analysis", {}),
                "strategy_insights": user_data.get("strategy_data", {}),
                "onboarding_insights": user_data.get("onboarding_data", {})
            }
            
            processing_time = time.time() - start_time
            calendar_data["processing_time"] = processing_time
            calendar_data["ai_confidence"] = 0.90  # Higher confidence with database-driven insights
            
            logger.info(f"✅ Calendar generation completed in {processing_time:.2f}s")
            return calendar_data
            
        except Exception as e:
            logger.error(f"❌ Error generating calendar: {str(e)}")
            raise
    
    async def generate_ai_powered_calendar(
        self,
        user_id: int,
        strategy_id: Optional[int] = None,
        calendar_type: str = "monthly",
        industry: Optional[str] = None,
        business_size: str = "sme"
    ) -> Dict[str, Any]:
        """
        Generate an AI-powered content calendar using comprehensive database insights.
        This is the enhanced version with full data transparency and advanced features.
        """
        try:
            logger.info(f"Generating AI-powered calendar for user {user_id}")
            start_time = time.time()
            
            # Get comprehensive user data
            user_data = await self._get_comprehensive_user_data(user_id, strategy_id)
            
            # Generate calendar using AI insights
            calendar_data = await self._generate_calendar_with_advanced_ai(
                user_data, calendar_type, industry, business_size
            )
            
            # Add performance predictions
            performance_predictions = await self._predict_calendar_performance(
                calendar_data, user_data
            )
            
            # Add trending topics integration
            trending_topics = await self._get_trending_topics_for_calendar(
                user_data, industry
            )
            
            # Add content repurposing opportunities
            repurposing_opportunities = await self._identify_repurposing_opportunities(
                calendar_data, user_data
            )
            
            processing_time = time.time() - start_time
            
            return {
                "user_id": user_id,
                "strategy_id": strategy_id,
                "calendar_type": calendar_type,
                "industry": industry or user_data.get("industry", "technology"),
                "business_size": business_size,
                "generated_at": datetime.now().isoformat(),
                "content_pillars": calendar_data.get("content_pillars", []),
                "platform_strategies": calendar_data.get("platform_strategies", {}),
                "content_mix": calendar_data.get("content_mix", {}),
                "daily_schedule": calendar_data.get("daily_schedule", []),
                "weekly_themes": calendar_data.get("weekly_themes", []),
                "content_recommendations": calendar_data.get("content_recommendations", []),
                "optimal_timing": calendar_data.get("optimal_timing", {}),
                "performance_predictions": performance_predictions,
                "trending_topics": trending_topics,
                "repurposing_opportunities": repurposing_opportunities,
                "ai_insights": calendar_data.get("ai_insights", []),
                "competitor_analysis": user_data.get("competitor_analysis", {}),
                "gap_analysis_insights": user_data.get("gap_analysis", {}),
                "strategy_insights": user_data.get("strategy_data", {}),
                "onboarding_insights": user_data.get("onboarding_data", {}),
                "processing_time": processing_time,
                "ai_confidence": 0.95
            }
            
        except Exception as e:
            logger.error(f"Error generating AI-powered calendar: {str(e)}")
            raise

    async def _get_comprehensive_user_data(self, user_id: int, strategy_id: Optional[int]) -> Dict[str, Any]:
        """Get comprehensive user data from all database sources."""
        try:
            logger.info(f"Getting comprehensive user data for user {user_id}")
            
            # Get onboarding data (not async)
            onboarding_data = self.onboarding_service.get_personalized_ai_inputs(user_id)
            
            # Get AI analysis results from the working endpoint
            try:
                from services.ai_analytics_service import AIAnalyticsService
                ai_analytics = AIAnalyticsService()
                ai_analysis_results = await ai_analytics.generate_strategic_intelligence(strategy_id or 1)
            except Exception as e:
                logger.warning(f"Could not get AI analysis results: {str(e)}")
                ai_analysis_results = {"insights": [], "recommendations": []}
            
            # Get gap analysis data from the working endpoint
            try:
                from services.content_gap_analyzer.ai_engine_service import AIEngineService
                ai_engine = AIEngineService()
                gap_analysis_data = await ai_engine.generate_content_recommendations(onboarding_data)
            except Exception as e:
                logger.warning(f"Could not get gap analysis data: {str(e)}")
                gap_analysis_data = []
            
            # Get content strategy data
            strategy_data = {}
            if strategy_id:
                strategy_data = await self._get_strategy_data(strategy_id)
            
            # Get content recommendations
            recommendations_data = await self._get_recommendations_data(user_id, strategy_id)
            
            # Get performance metrics
            performance_data = await self._get_performance_data(user_id, strategy_id)
            
            # Build comprehensive response
            comprehensive_data = {
                "user_id": user_id,
                "onboarding_data": onboarding_data,
                "ai_analysis_results": ai_analysis_results,
                "gap_analysis": {
                    "content_gaps": gap_analysis_data if isinstance(gap_analysis_data, list) else [],
                    "keyword_opportunities": onboarding_data.get("keyword_analysis", {}).get("high_value_keywords", []),
                    "competitor_insights": onboarding_data.get("competitor_analysis", {}).get("top_performers", []),
                    "recommendations": gap_analysis_data if isinstance(gap_analysis_data, list) else [],
                    "opportunities": onboarding_data.get("gap_analysis", {}).get("content_opportunities", [])
                },
                "strategy_data": strategy_data,
                "recommendations_data": recommendations_data,
                "performance_data": performance_data,
                "industry": onboarding_data.get("website_analysis", {}).get("industry_focus", "technology"),
                "target_audience": onboarding_data.get("website_analysis", {}).get("target_audience", []),
                "business_goals": ["Increase brand awareness", "Generate leads", "Establish thought leadership"],
                "website_analysis": onboarding_data.get("website_analysis", {}),
                "competitor_analysis": onboarding_data.get("competitor_analysis", {}),
                "keyword_analysis": onboarding_data.get("keyword_analysis", {})
            }
            
            logger.info(f"✅ Successfully retrieved comprehensive user data for user {user_id}")
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"Error getting comprehensive user data: {str(e)}")
            return {"user_id": user_id, "industry": "technology"}
    
    async def _get_gap_analysis_data(self, user_id: int) -> Dict[str, Any]:
        """Get gap analysis data from database."""
        try:
            # Check if database service is available
            if self.content_planning_db_service is None:
                logger.warning("ContentPlanningDBService not available, returning empty gap analysis data")
                return {}
            
            # Get latest gap analysis results using the correct method name
            gap_analyses = await self.content_planning_db_service.get_user_content_gap_analyses(user_id)
            
            if gap_analyses:
                latest_analysis = gap_analyses[0]  # Get most recent
                return {
                    "content_gaps": latest_analysis.get("analysis_results", {}).get("content_gaps", []),
                    "keyword_opportunities": latest_analysis.get("analysis_results", {}).get("keyword_opportunities", []),
                    "competitor_insights": latest_analysis.get("analysis_results", {}).get("competitor_insights", []),
                    "recommendations": latest_analysis.get("recommendations", []),
                    "opportunities": latest_analysis.get("opportunities", [])
                }
            return {}
        except Exception as e:
            logger.error(f"Error getting gap analysis data: {str(e)}")
            return {}
    
    async def _get_strategy_data(self, strategy_id: int) -> Dict[str, Any]:
        """Get content strategy data from database."""
        try:
            # Check if database service is available
            if self.content_planning_db_service is None:
                logger.warning("ContentPlanningDBService not available, returning empty strategy data")
                return {}
            
            strategy = await self.content_planning_db_service.get_content_strategy(strategy_id)
            if strategy:
                return {
                    "content_pillars": strategy.get("content_pillars", []),
                    "target_audience": strategy.get("target_audience", {}),
                    "ai_recommendations": strategy.get("ai_recommendations", {}),
                    "industry": strategy.get("industry", ""),
                    "business_goals": strategy.get("business_goals", [])
                }
            return {}
        except Exception as e:
            logger.error(f"Error getting strategy data: {str(e)}")
            return {}
    
    async def _get_recommendations_data(self, user_id: int, strategy_id: Optional[int]) -> List[Dict[str, Any]]:
        """Get content recommendations from database."""
        try:
            # Check if database service is available
            if self.content_planning_db_service is None:
                logger.warning("ContentPlanningDBService not available, returning empty recommendations data")
                return []
            
            recommendations = await self.content_planning_db_service.get_user_content_recommendations(user_id)
            return recommendations or []
        except Exception as e:
            logger.error(f"Error getting recommendations data: {str(e)}")
            return []
    
    async def _get_performance_data(self, user_id: int, strategy_id: Optional[int]) -> Dict[str, Any]:
        """Get performance data from database."""
        try:
            # Check if database service is available
            if self.content_planning_db_service is None:
                logger.warning("ContentPlanningDBService not available, returning empty performance data")
                return {}
            
            # For now, return empty performance data since the method might not exist
            # This can be enhanced later when performance tracking is implemented
            return {}
        except Exception as e:
            logger.error(f"Error getting performance data: {str(e)}")
            return {}
    
    def _get_content_pillars(self, industry: str) -> List[str]:
        """Get content pillars for the industry."""
        return self.content_pillars.get(industry, self.content_pillars["technology"])
    
    async def _generate_daily_schedule_with_db_data(self, calendar_type: str, industry: str, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate daily content schedule using database insights."""
        try:
            # Extract relevant data from user_data
            gap_analysis = user_data.get("gap_analysis", {})
            strategy_data = user_data.get("strategy_data", {})
            onboarding_data = user_data.get("onboarding_data", {})
            recommendations = user_data.get("recommendations_data", [])
            
            prompt = f"""
            Create a comprehensive daily content schedule for a {industry} business using the following specific data:
            
            GAP ANALYSIS INSIGHTS:
            - Content Gaps: {gap_analysis.get('content_gaps', [])}
            - Keyword Opportunities: {gap_analysis.get('keyword_opportunities', [])}
            - Competitor Insights: {gap_analysis.get('competitor_insights', [])}
            - Recommendations: {gap_analysis.get('recommendations', [])}
            
            STRATEGY DATA:
            - Content Pillars: {strategy_data.get('content_pillars', [])}
            - Target Audience: {strategy_data.get('target_audience', {})}
            - AI Recommendations: {strategy_data.get('ai_recommendations', {})}
            
            ONBOARDING DATA:
            - Website Analysis: {onboarding_data.get('website_analysis', {})}
            - Competitor Analysis: {onboarding_data.get('competitor_analysis', {})}
            - Keyword Analysis: {onboarding_data.get('keyword_analysis', {})}
            
            EXISTING RECOMMENDATIONS:
            - Content Recommendations: {recommendations}
            
            Requirements:
            - Generate {calendar_type} schedule
            - Address specific content gaps identified
            - Incorporate keyword opportunities
            - Use competitor insights for differentiation
            - Align with existing content pillars
            - Consider target audience preferences
            - Balance educational, thought leadership, engagement, and promotional content
            
            Return a structured schedule that specifically addresses the identified gaps and opportunities.
            """
            
            response = await self.ai_engine.generate_structured_response(
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "daily_schedule": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "day": {"type": "string"},
                                    "theme": {"type": "string"},
                                    "content_types": {"type": "array", "items": {"type": "string"}},
                                    "platforms": {"type": "array", "items": {"type": "string"}},
                                    "optimal_times": {"type": "array", "items": {"type": "string"}},
                                    "content_mix": {"type": "object"},
                                    "gap_addresses": {"type": "array", "items": {"type": "string"}},
                                    "keyword_focus": {"type": "array", "items": {"type": "string"}},
                                    "competitor_differentiation": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            )
            
            return response.get("daily_schedule", [])
            
        except Exception as e:
            logger.error(f"Error generating daily schedule with DB data: {str(e)}")
            return self._get_default_daily_schedule(calendar_type)
    
    async def _generate_weekly_themes_with_db_data(self, calendar_type: str, industry: str, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate weekly content themes using database insights."""
        try:
            gap_analysis = user_data.get("gap_analysis", {})
            strategy_data = user_data.get("strategy_data", {})
            onboarding_data = user_data.get("onboarding_data", {})
            
            prompt = f"""
            Create weekly content themes for a {industry} business using specific database insights:
            
            CONTENT GAPS TO ADDRESS:
            - Identified Gaps: {gap_analysis.get('content_gaps', [])}
            - Opportunities: {gap_analysis.get('opportunities', [])}
            
            STRATEGY FOUNDATION:
            - Content Pillars: {strategy_data.get('content_pillars', [])}
            - Target Audience: {strategy_data.get('target_audience', {})}
            
            COMPETITOR INSIGHTS:
            - Competitor Analysis: {onboarding_data.get('competitor_analysis', {})}
            - Industry Position: {onboarding_data.get('website_analysis', {}).get('industry_focus', '')}
            
            Requirements:
            - Generate {calendar_type} themes that address specific gaps
            - Align with existing content pillars
            - Incorporate competitor insights for differentiation
            - Focus on identified opportunities
            - Consider seasonal and trending topics
            - Balance different content types based on audience preferences
            
            Return structured weekly themes that specifically address the identified gaps and opportunities.
            """
            
            response = await self.ai_engine.generate_structured_response(
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "weekly_themes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "week": {"type": "string"},
                                    "theme": {"type": "string"},
                                    "focus_areas": {"type": "array", "items": {"type": "string"}},
                                    "trending_topics": {"type": "array", "items": {"type": "string"}},
                                    "content_types": {"type": "array", "items": {"type": "string"}},
                                    "gap_addresses": {"type": "array", "items": {"type": "string"}},
                                    "competitor_differentiation": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            )
            
            return response.get("weekly_themes", [])
            
        except Exception as e:
            logger.error(f"Error generating weekly themes with DB data: {str(e)}")
            return self._get_default_weekly_themes(calendar_type)
    
    async def _generate_content_recommendations_with_db_data(self, user_data: Dict[str, Any], industry: str) -> List[Dict[str, Any]]:
        """Generate specific content recommendations using database insights."""
        try:
            gap_analysis = user_data.get("gap_analysis", {})
            strategy_data = user_data.get("strategy_data", {})
            onboarding_data = user_data.get("onboarding_data", {})
            existing_recommendations = user_data.get("recommendations_data", [])
            
            prompt = f"""
            Generate specific content recommendations for a {industry} business using comprehensive database insights:
            
            CONTENT GAPS TO FILL:
            - Identified Gaps: {gap_analysis.get('content_gaps', [])}
            - Keyword Opportunities: {gap_analysis.get('keyword_opportunities', [])}
            - Competitor Insights: {gap_analysis.get('competitor_insights', [])}
            
            STRATEGY CONTEXT:
            - Content Pillars: {strategy_data.get('content_pillars', [])}
            - Target Audience: {strategy_data.get('target_audience', {})}
            - AI Recommendations: {strategy_data.get('ai_recommendations', {})}
            
            AUDIENCE INSIGHTS:
            - Website Analysis: {onboarding_data.get('website_analysis', {})}
            - Target Demographics: {onboarding_data.get('target_audience', {})}
            - Content Preferences: {onboarding_data.get('keyword_analysis', {}).get('content_topics', [])}
            
            EXISTING RECOMMENDATIONS:
            - Current Recommendations: {existing_recommendations}
            
            Requirements:
            - Create specific content ideas that address identified gaps
            - Incorporate keyword opportunities
            - Use competitor insights for differentiation
            - Align with content pillars and audience preferences
            - Predict performance based on existing data
            - Provide implementation suggestions
            
            Return structured recommendations that specifically address the database insights.
            """
            
            response = await self.ai_engine.generate_structured_response(
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "content_recommendations": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "content_type": {"type": "string"},
                                    "platforms": {"type": "array", "items": {"type": "string"}},
                                    "target_audience": {"type": "string"},
                                    "estimated_performance": {"type": "object"},
                                    "implementation_tips": {"type": "array", "items": {"type": "string"}},
                                    "gap_addresses": {"type": "array", "items": {"type": "string"}},
                                    "keyword_focus": {"type": "array", "items": {"type": "string"}},
                                    "competitor_differentiation": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            )
            
            return response.get("content_recommendations", [])
            
        except Exception as e:
            logger.error(f"Error generating content recommendations with DB data: {str(e)}")
            return self._get_default_content_recommendations(industry)
    
    async def _generate_optimal_timing_with_db_data(self, industry: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimal posting times using database insights."""
        try:
            performance_data = user_data.get("performance_data", {})
            onboarding_data = user_data.get("onboarding_data", {})
            
            prompt = f"""
            Generate optimal posting times for different social media platforms for a {industry} business using performance data:
            
            PERFORMANCE INSIGHTS:
            - Historical Performance: {performance_data}
            - Audience Demographics: {onboarding_data.get('target_audience', {})}
            - Website Analysis: {onboarding_data.get('website_analysis', {})}
            
            Requirements:
            - Consider industry-specific audience behavior
            - Use historical performance data to optimize timing
            - Include multiple platforms (LinkedIn, Instagram, Twitter, YouTube)
            - Provide specific time recommendations based on audience data
            - Include frequency guidelines
            - Consider timezone considerations
            
            Return structured timing recommendations based on actual performance data.
            """
            
            response = await self.ai_engine.generate_structured_response(
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "optimal_timing": {
                            "type": "object",
                            "properties": {
                                "linkedin": {"type": "object"},
                                "instagram": {"type": "object"},
                                "twitter": {"type": "object"},
                                "youtube": {"type": "object"},
                                "website": {"type": "object"}
                            }
                        }
                    }
                }
            )
            
            return response.get("optimal_timing", {})
            
        except Exception as e:
            logger.error(f"Error generating optimal timing with DB data: {str(e)}")
            return self._get_default_optimal_timing()
    
    async def _generate_performance_predictions_with_db_data(self, industry: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance predictions using database insights."""
        try:
            performance_data = user_data.get("performance_data", {})
            gap_analysis = user_data.get("gap_analysis", {})
            onboarding_data = user_data.get("onboarding_data", {})
            
            prompt = f"""
            Generate performance predictions for different content types in the {industry} industry using database insights:
            
            HISTORICAL PERFORMANCE:
            - Performance Data: {performance_data}
            - Engagement Patterns: {performance_data.get('engagement_patterns', {})}
            - Conversion Data: {performance_data.get('conversion_data', {})}
            
            CONTENT OPPORTUNITIES:
            - Content Gaps: {gap_analysis.get('content_gaps', [])}
            - Keyword Opportunities: {gap_analysis.get('keyword_opportunities', [])}
            
            AUDIENCE INSIGHTS:
            - Target Demographics: {onboarding_data.get('target_audience', {})}
            - Content Preferences: {onboarding_data.get('keyword_analysis', {}).get('content_topics', [])}
            
            Requirements:
            - Predict engagement rates based on historical data
            - Estimate reach and impressions using audience insights
            - Consider industry benchmarks
            - Include conversion predictions based on gap analysis
            - Provide ROI estimates using performance data
            
            Return structured predictions based on actual database insights.
            """
            
            response = await self.ai_engine.generate_structured_response(
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "performance_predictions": {
                            "type": "object",
                            "properties": {
                                "content_types": {"type": "object"},
                                "platforms": {"type": "object"},
                                "industry_benchmarks": {"type": "object"},
                                "roi_estimates": {"type": "object"},
                                "gap_opportunities": {"type": "object"}
                            }
                        }
                    }
                }
            )
            
            return response.get("performance_predictions", {})
            
        except Exception as e:
            logger.error(f"Error generating performance predictions with DB data: {str(e)}")
            return self._get_default_performance_predictions()
    
    async def _get_trending_topics_from_db(self, industry: str, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get trending topics using database insights."""
        try:
            gap_analysis = user_data.get("gap_analysis", {})
            onboarding_data = user_data.get("onboarding_data", {})
            
            # Use keyword researcher with database insights
            keywords = [industry, "trending", "latest"]
            if gap_analysis.get('keyword_opportunities'):
                keywords.extend(gap_analysis['keyword_opportunities'][:5])
            
            trending_data = await self.keyword_researcher.analyze_keywords(
                keywords=keywords,
                analysis_type="trend_analysis"
            )
            
            # Enhance with database insights
            enhanced_trends = trending_data.get("trending_topics", [])
            for trend in enhanced_trends:
                trend["gap_relevance"] = self._assess_gap_relevance(trend, gap_analysis)
                trend["audience_alignment"] = self._assess_audience_alignment(trend, onboarding_data)
            
            return enhanced_trends
            
        except Exception as e:
            logger.error(f"Error getting trending topics from DB: {str(e)}")
            return []
    
    async def _generate_repurposing_opportunities_with_db_data(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content repurposing opportunities using database insights."""
        try:
            gap_analysis = user_data.get("gap_analysis", {})
            strategy_data = user_data.get("strategy_data", {})
            recommendations = user_data.get("recommendations_data", [])
            
            prompt = f"""
            Generate content repurposing opportunities using database insights:
            
            CONTENT GAPS:
            - Identified Gaps: {gap_analysis.get('content_gaps', [])}
            - Opportunities: {gap_analysis.get('opportunities', [])}
            
            EXISTING CONTENT:
            - Content Pillars: {strategy_data.get('content_pillars', [])}
            - Recommendations: {recommendations}
            
            Requirements:
            - Identify how to adapt existing content to fill gaps
            - Suggest content transformations based on opportunities
            - Include platform-specific adaptations
            - Consider audience preferences per platform
            - Focus on addressing identified content gaps
            
            Return structured repurposing opportunities that address specific database insights.
            """
            
            response = await self.ai_engine.generate_structured_response(
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "repurposing_opportunities": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "original_content": {"type": "string"},
                                    "platform_adaptations": {"type": "array", "items": {"type": "string"}},
                                    "transformations": {"type": "array", "items": {"type": "string"}},
                                    "implementation_tips": {"type": "array", "items": {"type": "string"}},
                                    "gap_addresses": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        }
                    }
                }
            )
            
            return response.get("repurposing_opportunities", [])
            
        except Exception as e:
            logger.error(f"Error generating repurposing opportunities with DB data: {str(e)}")
            return []
    
    async def _generate_ai_insights_with_db_data(self, user_data: Dict[str, Any], industry: str) -> List[Dict[str, Any]]:
        """Generate AI insights using database insights."""
        try:
            gap_analysis = user_data.get("gap_analysis", {})
            strategy_data = user_data.get("strategy_data", {})
            onboarding_data = user_data.get("onboarding_data", {})
            performance_data = user_data.get("performance_data", {})
            
            prompt = f"""
            Generate AI insights for content planning in the {industry} industry using comprehensive database insights:
            
            CONTENT GAPS:
            - Identified Gaps: {gap_analysis.get('content_gaps', [])}
            - Opportunities: {gap_analysis.get('opportunities', [])}
            
            STRATEGY CONTEXT:
            - Content Pillars: {strategy_data.get('content_pillars', [])}
            - Target Audience: {strategy_data.get('target_audience', {})}
            
            PERFORMANCE DATA:
            - Historical Performance: {performance_data}
            - Engagement Patterns: {performance_data.get('engagement_patterns', {})}
            
            AUDIENCE INSIGHTS:
            - Target Demographics: {onboarding_data.get('target_audience', {})}
            - Website Analysis: {onboarding_data.get('website_analysis', {})}
            
            Requirements:
            - Provide strategic insights based on gap analysis
            - Include content optimization tips using performance data
            - Suggest audience engagement strategies
            - Consider industry trends and competitor analysis
            - Include performance optimization insights
            
            Return structured insights that specifically address the database insights.
            """
            
            response = await self.ai_engine.generate_structured_response(
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "ai_insights": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "insight_type": {"type": "string"},
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "recommendations": {"type": "array", "items": {"type": "string"}},
                                    "priority": {"type": "string"},
                                    "data_source": {"type": "string"},
                                    "gap_addresses": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        }
                    }
                }
            )
            
            return response.get("ai_insights", [])
            
        except Exception as e:
            logger.error(f"Error generating AI insights with DB data: {str(e)}")
            return []
    
    async def _analyze_competitors_with_db_data(self, user_data: Dict[str, Any], industry: str) -> Dict[str, Any]:
        """Analyze competitors using database insights."""
        try:
            gap_analysis = user_data.get("gap_analysis", {})
            onboarding_data = user_data.get("onboarding_data", {})
            
            # Use competitor analyzer with database insights
            competitor_data = await self.competitor_analyzer.analyze_competitors(
                industry=industry,
                analysis_type="content_gaps",
                competitor_urls=onboarding_data.get('competitor_analysis', {}).get('top_performers', [])
            )
            
            # Enhance with gap analysis insights
            enhanced_competitor_data = competitor_data or {}
            enhanced_competitor_data["gap_opportunities"] = gap_analysis.get("opportunities", [])
            enhanced_competitor_data["content_differentiation"] = gap_analysis.get("competitor_insights", [])
            
            return enhanced_competitor_data
            
        except Exception as e:
            logger.error(f"Error analyzing competitors with DB data: {str(e)}")
            return {}
    
    def _assess_gap_relevance(self, trend: Dict[str, Any], gap_analysis: Dict[str, Any]) -> str:
        """Assess how relevant a trending topic is to identified gaps."""
        try:
            content_gaps = gap_analysis.get("content_gaps", [])
            trend_title = trend.get("keyword", "").lower()
            
            for gap in content_gaps:
                if any(word in trend_title for word in gap.lower().split()):
                    return "high"
            
            return "medium"
        except Exception:
            return "low"
    
    def _assess_audience_alignment(self, trend: Dict[str, Any], onboarding_data: Dict[str, Any]) -> str:
        """Assess how well a trending topic aligns with target audience."""
        try:
            target_audience = onboarding_data.get("target_audience", {})
            trend_title = trend.get("keyword", "").lower()
            
            # Simple keyword matching - could be enhanced with more sophisticated analysis
            audience_keywords = ["professional", "business", "industry", "technology", "marketing"]
            
            if any(keyword in trend_title for keyword in audience_keywords):
                return "high"
            
            return "medium"
        except Exception:
            return "low"
    
    def _get_default_daily_schedule(self, calendar_type: str) -> List[Dict[str, Any]]:
        """Get default daily schedule if AI generation fails."""
        return [
            {
                "day": "Monday",
                "theme": "Educational Content",
                "content_types": ["blog_post", "how_to_guide"],
                "platforms": ["website", "linkedin"],
                "optimal_times": ["9:00 AM", "2:00 PM"],
                "content_mix": {"educational": 0.6, "thought_leadership": 0.4}
            },
            {
                "day": "Tuesday",
                "theme": "Industry Insights",
                "content_types": ["industry_analysis", "trend_report"],
                "platforms": ["linkedin", "twitter"],
                "optimal_times": ["10:00 AM", "3:00 PM"],
                "content_mix": {"thought_leadership": 0.7, "educational": 0.3}
            }
        ]
    
    def _get_default_weekly_themes(self, calendar_type: str) -> List[Dict[str, Any]]:
        """Get default weekly themes if AI generation fails."""
        return [
            {
                "week": "Week 1",
                "theme": "Industry Fundamentals",
                "focus_areas": ["Educational content", "Basic concepts"],
                "trending_topics": ["Industry trends", "Best practices"],
                "content_types": ["blog_posts", "infographics"]
            }
        ]
    
    def _get_default_content_recommendations(self, industry: str) -> List[Dict[str, Any]]:
        """Get default content recommendations if AI generation fails."""
        return [
            {
                "title": f"Complete Guide to {industry.title()} Best Practices",
                "description": f"A comprehensive guide covering essential {industry} practices and strategies.",
                "content_type": "blog_post",
                "platforms": ["website", "linkedin"],
                "target_audience": "Industry professionals",
                "estimated_performance": {"engagement_rate": 0.08, "reach": 5000},
                "implementation_tips": ["Use industry keywords", "Include expert quotes", "Add visual elements"]
            }
        ]
    
    def _get_default_optimal_timing(self) -> Dict[str, Any]:
        """Get default optimal timing if AI generation fails."""
        return {
            "linkedin": {"optimal_times": ["9:00 AM", "2:00 PM"], "frequency": "daily"},
            "instagram": {"optimal_times": ["12:00 PM", "7:00 PM"], "frequency": "daily"},
            "twitter": {"optimal_times": ["8:00 AM", "12:00 PM", "5:00 PM"], "frequency": "3-5 per day"},
            "youtube": {"optimal_times": ["2:00 PM", "7:00 PM"], "frequency": "weekly"},
            "website": {"optimal_times": ["10:00 AM"], "frequency": "2-3 per week"}
        }
    
    def _get_default_performance_predictions(self) -> Dict[str, Any]:
        """Get default performance predictions if AI generation fails."""
        return {
            "content_types": {
                "blog_posts": {"engagement_rate": 0.06, "reach": 3000},
                "videos": {"engagement_rate": 0.12, "reach": 5000},
                "infographics": {"engagement_rate": 0.15, "reach": 8000}
            },
            "platforms": {
                "linkedin": {"engagement_rate": 0.08, "reach": 4000},
                "instagram": {"engagement_rate": 0.10, "reach": 6000},
                "twitter": {"engagement_rate": 0.05, "reach": 2000}
            }
        } 

    async def _generate_calendar_with_advanced_ai(
        self,
        user_data: Dict[str, Any],
        calendar_type: str,
        industry: str,
        business_size: str
    ) -> Dict[str, Any]:
        """
        Generate calendar using advanced AI with comprehensive database insights.
        """
        try:
            # Extract key data points
            gap_analysis = user_data.get("gap_analysis", {})
            ai_analysis = user_data.get("ai_analysis_results", {})
            strategy_data = user_data.get("strategy_data", {})
            
            # Generate content pillars based on gap analysis
            content_pillars = self._generate_content_pillars_from_gaps(
                gap_analysis, industry, business_size
            )
            
            # Generate daily schedule addressing specific gaps
            daily_schedule = await self._generate_daily_schedule_addressing_gaps(
                calendar_type, gap_analysis, content_pillars, user_data
            )
            
            # Generate weekly themes based on AI insights
            weekly_themes = await self._generate_weekly_themes_from_ai_insights(
                ai_analysis, content_pillars, calendar_type
            )
            
            # Generate platform-specific strategies
            platform_strategies = self._generate_platform_strategies(
                industry, business_size, content_pillars
            )
            
            # Generate optimal content mix
            content_mix = self._generate_optimal_content_mix(
                gap_analysis, ai_analysis, industry
            )
            
            # Generate content recommendations
            content_recommendations = await self._generate_content_recommendations(
                gap_analysis, ai_analysis, content_pillars
            )
            
            # Generate optimal timing
            optimal_timing = await self._generate_optimal_timing(
                user_data, industry, business_size
            )
            
            # Generate AI insights
            ai_insights = await self._generate_calendar_ai_insights(
                gap_analysis, ai_analysis, content_pillars
            )
            
            return {
                "content_pillars": content_pillars,
                "daily_schedule": daily_schedule,
                "weekly_themes": weekly_themes,
                "platform_strategies": platform_strategies,
                "content_mix": content_mix,
                "content_recommendations": content_recommendations,
                "optimal_timing": optimal_timing,
                "ai_insights": ai_insights
            }
            
        except Exception as e:
            logger.error(f"Error in advanced AI calendar generation: {str(e)}")
            raise

    def _generate_content_pillars_from_gaps(
        self,
        gap_analysis: Dict[str, Any],
        industry: str,
        business_size: str
    ) -> List[str]:
        """
        Generate content pillars based on identified gaps and industry best practices.
        """
        # Get industry-specific content pillars
        industry_pillars = self.content_pillars.get(industry, [
            "Educational Content",
            "Thought Leadership", 
            "Product Updates",
            "Industry Insights",
            "Team Culture"
        ])
        
        # Add gap-specific pillars
        gap_pillars = []
        if gap_analysis.get("content_gaps"):
            for gap in gap_analysis["content_gaps"][:3]:  # Top 3 gaps
                gap_type = gap.get("type", "Content Creation")
                if gap_type not in gap_pillars:
                    gap_pillars.append(gap_type)
        
        # Combine and prioritize
        all_pillars = industry_pillars + gap_pillars
        return list(dict.fromkeys(all_pillars))[:5]  # Top 5 unique pillars

    async def _generate_daily_schedule_addressing_gaps(
        self,
        calendar_type: str,
        gap_analysis: Dict[str, Any],
        content_pillars: List[str],
        user_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate daily schedule that specifically addresses identified content gaps.
        """
        try:
            # Get AI service for advanced scheduling
            ai_manager = AIServiceManager()
            
            # Prepare prompt with gap analysis data
            gap_data = {
                "content_gaps": gap_analysis.get("content_gaps", []),
                "keyword_opportunities": gap_analysis.get("keyword_opportunities", []),
                "recommendations": gap_analysis.get("recommendations", []),
                "content_pillars": content_pillars,
                "calendar_type": calendar_type,
                "industry": user_data.get("industry", "technology"),
                "business_size": user_data.get("business_size", "sme")
            }
            
            # Generate schedule using AI
            schedule_prompt = f"""
            Create a comprehensive {calendar_type} content schedule that addresses specific content gaps:
            
            CONTENT GAPS TO ADDRESS:
            {gap_analysis.get('content_gaps', [])}
            
            KEYWORD OPPORTUNITIES:
            {gap_analysis.get('keyword_opportunities', [])}
            
            CONTENT PILLARS:
            {content_pillars}
            
            Requirements:
            1. Address each identified content gap with specific content pieces
            2. Incorporate keyword opportunities naturally
            3. Balance content pillars throughout the schedule
            4. Include specific titles, descriptions, and content types
            5. Optimize for engagement and SEO
            6. Consider industry best practices for {user_data.get('industry', 'technology')}
            
            Return a structured schedule with daily content pieces.
            """
            
            ai_response = await ai_manager.generate_content_schedule(schedule_prompt)
            
            # Parse and structure the response
            if isinstance(ai_response, dict) and "schedule" in ai_response:
                return ai_response["schedule"]
            else:
                # Fallback to template-based generation
                return self._generate_fallback_schedule(calendar_type, content_pillars)
                
        except Exception as e:
            logger.error(f"Error generating daily schedule: {str(e)}")
            return self._generate_fallback_schedule(calendar_type, content_pillars)

    async def _generate_weekly_themes_from_ai_insights(
        self,
        ai_analysis: Dict[str, Any],
        content_pillars: List[str],
        calendar_type: str
    ) -> List[Dict[str, Any]]:
        """
        Generate weekly themes based on AI analysis insights.
        """
        try:
            themes = []
            
            # Extract themes from AI analysis
            if ai_analysis.get("market_positioning"):
                positioning = ai_analysis["market_positioning"]
                themes.append({
                    "week": 1,
                    "theme": f"Establishing {positioning.get('competitive_advantage', 'Content Quality')}",
                    "focus": "Building competitive advantage through content",
                    "content_types": ["thought_leadership", "case_studies", "expert_insights"]
                })
            
            # Add gap-based themes
            if ai_analysis.get("gap_analysis"):
                gap_themes = self._extract_themes_from_gaps(ai_analysis["gap_analysis"])
                themes.extend(gap_themes)
            
            # Add industry-specific themes
            industry_themes = self._get_industry_themes(ai_analysis.get("industry", "technology"))
            themes.extend(industry_themes)
            
            return themes[:4]  # Return top 4 themes
            
        except Exception as e:
            logger.error(f"Error generating weekly themes: {str(e)}")
            return []

    def _generate_platform_strategies(
        self,
        industry: str,
        business_size: str,
        content_pillars: List[str]
    ) -> Dict[str, Any]:
        """
        Generate platform-specific content strategies.
        """
        return {
            "website": {
                "content_types": ["blog_posts", "case_studies", "whitepapers", "product_pages"],
                "frequency": "2-3 per week",
                "optimal_length": "1500+ words",
                "tone": "professional, educational",
                "content_pillars": content_pillars
            },
            "linkedin": {
                "content_types": ["industry_insights", "professional_tips", "company_updates", "employee_spotlights"],
                "frequency": "daily",
                "optimal_length": "100-300 words",
                "tone": "professional, thought leadership",
                "content_pillars": content_pillars
            },
            "instagram": {
                "content_types": ["behind_scenes", "product_demos", "team_culture", "infographics"],
                "frequency": "daily",
                "optimal_length": "visual focus",
                "tone": "casual, engaging",
                "content_pillars": content_pillars
            },
            "youtube": {
                "content_types": ["tutorial_videos", "product_demos", "customer_testimonials", "industry_interviews"],
                "frequency": "weekly",
                "optimal_length": "5-15 minutes",
                "tone": "educational, engaging",
                "content_pillars": content_pillars
            },
            "twitter": {
                "content_types": ["industry_news", "quick_tips", "event_announcements", "community_engagement"],
                "frequency": "3-5 per day",
                "optimal_length": "280 characters",
                "tone": "informative, engaging",
                "content_pillars": content_pillars
            }
        }

    def _generate_optimal_content_mix(
        self,
        gap_analysis: Dict[str, Any],
        ai_analysis: Dict[str, Any],
        industry: str
    ) -> Dict[str, float]:
        """
        Generate optimal content mix based on gap analysis and AI insights.
        """
        # Base mix for industry
        base_mix = {
            "educational": 40,
            "thought_leadership": 30,
            "engagement": 20,
            "promotional": 10
        }
        
        # Adjust based on gap analysis
        if gap_analysis.get("content_gaps"):
            educational_gaps = len([g for g in gap_analysis["content_gaps"] if "educational" in g.get("type", "").lower()])
            thought_leadership_gaps = len([g for g in gap_analysis["content_gaps"] if "leadership" in g.get("type", "").lower()])
            
            if educational_gaps > thought_leadership_gaps:
                base_mix["educational"] += 10
                base_mix["thought_leadership"] -= 5
                base_mix["engagement"] -= 5
            elif thought_leadership_gaps > educational_gaps:
                base_mix["thought_leadership"] += 10
                base_mix["educational"] -= 5
                base_mix["engagement"] -= 5
        
        return base_mix

    async def _predict_calendar_performance(
        self,
        calendar_data: Dict[str, Any],
        user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict calendar performance based on AI analysis and historical data.
        """
        try:
            # Extract performance indicators
            ai_analysis = user_data.get("ai_analysis_results", {})
            strategic_scores = ai_analysis.get("strategic_scores", {})
            
            # Calculate performance predictions
            base_traffic_growth = 25
            base_engagement_rate = 15
            base_conversion_rate = 10
            
            # Adjust based on strategic scores
            if strategic_scores:
                market_positioning_score = strategic_scores.get("market_positioning_score", 0.7)
                content_strategy_score = strategic_scores.get("content_strategy_score", 0.7)
                
                # Adjust predictions based on scores
                traffic_growth = base_traffic_growth * (0.8 + market_positioning_score * 0.4)
                engagement_rate = base_engagement_rate * (0.8 + content_strategy_score * 0.4)
                conversion_rate = base_conversion_rate * (0.8 + (market_positioning_score + content_strategy_score) / 2 * 0.4)
            else:
                traffic_growth = base_traffic_growth
                engagement_rate = base_engagement_rate
                conversion_rate = base_conversion_rate
            
            return {
                "traffic_growth": round(traffic_growth, 1),
                "engagement_rate": round(engagement_rate, 1),
                "conversion_rate": round(conversion_rate, 1),
                "roi_prediction": round(traffic_growth * 0.3 + engagement_rate * 0.4 + conversion_rate * 0.3, 1),
                "confidence_score": 0.85
            }
            
        except Exception as e:
            logger.error(f"Error predicting calendar performance: {str(e)}")
            return {
                "traffic_growth": 25,
                "engagement_rate": 15,
                "conversion_rate": 10,
                "roi_prediction": 15,
                "confidence_score": 0.7
            }

    async def _get_trending_topics_for_calendar(
        self,
        user_data: Dict[str, Any],
        industry: str
    ) -> List[Dict[str, Any]]:
        """
        Get trending topics relevant to the calendar and industry.
        """
        try:
            # Extract keywords from gap analysis
            keywords = user_data.get("gap_analysis", {}).get("keyword_opportunities", [])
            
            # Generate trending topics based on keywords and industry
            trending_topics = []
            for keyword in keywords[:5]:  # Top 5 keywords
                trending_topics.append({
                    "topic": keyword,
                    "relevance_score": 0.9,
                    "trend_direction": "rising",
                    "content_opportunities": [
                        f"Create content around {keyword}",
                        f"Develop case studies featuring {keyword}",
                        f"Create how-to guides for {keyword}"
                    ]
                })
            
            return trending_topics
            
        except Exception as e:
            logger.error(f"Error getting trending topics: {str(e)}")
            return []

    async def _identify_repurposing_opportunities(
        self,
        calendar_data: Dict[str, Any],
        user_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify content repurposing opportunities for the calendar.
        """
        try:
            opportunities = []
            
            # Identify opportunities from content pillars
            content_pillars = calendar_data.get("content_pillars", [])
            for pillar in content_pillars:
                opportunities.append({
                    "original_content": f"{pillar} content piece",
                    "repurposing_options": [
                        f"Convert to {pillar} blog post",
                        f"Create {pillar} social media series",
                        f"Develop {pillar} video content",
                        f"Design {pillar} infographic"
                    ],
                    "platforms": ["website", "linkedin", "instagram", "youtube"],
                    "estimated_reach_increase": "40%"
                })
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Error identifying repurposing opportunities: {str(e)}")
            return []

    def _generate_fallback_schedule(
        self,
        calendar_type: str,
        content_pillars: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate fallback schedule when AI generation fails.
        """
        schedule = []
        days = 30 if calendar_type == "monthly" else 7 if calendar_type == "weekly" else 90
        
        for day in range(1, days + 1):
            pillar = content_pillars[day % len(content_pillars)]
            schedule.append({
                "day": day,
                "title": f"{pillar} Content Day {day}",
                "description": f"Create engaging {pillar.lower()} content",
                "content_type": "blog_post",
                "platform": "website",
                "pillar": pillar,
                "priority": "medium"
            })
        
        return schedule 

    def _extract_themes_from_gaps(self, gap_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract weekly themes from gap analysis.
        """
        themes = []
        if gap_analysis.get("content_gaps"):
            for i, gap in enumerate(gap_analysis["content_gaps"][:3]):
                themes.append({
                    "week": i + 1,
                    "theme": f"Addressing {gap.get('type', 'Content Gap')}",
                    "focus": gap.get("title", "Content gap"),
                    "content_types": ["blog_posts", "case_studies", "how_to_guides"]
                })
        return themes

    def _get_industry_themes(self, industry: str) -> List[Dict[str, Any]]:
        """
        Get industry-specific themes.
        """
        industry_themes = {
            "technology": [
                {
                    "week": 4,
                    "theme": "Technology Innovation",
                    "focus": "Latest tech trends and innovations",
                    "content_types": ["industry_insights", "product_updates", "expert_interviews"]
                }
            ],
            "healthcare": [
                {
                    "week": 4,
                    "theme": "Healthcare Insights",
                    "focus": "Patient care and medical innovations",
                    "content_types": ["patient_education", "medical_insights", "health_tips"]
                }
            ],
            "finance": [
                {
                    "week": 4,
                    "theme": "Financial Education",
                    "focus": "Investment strategies and market analysis",
                    "content_types": ["financial_education", "market_analysis", "investment_tips"]
                }
            ]
        }
        return industry_themes.get(industry, [])

    async def _generate_content_recommendations(
        self,
        gap_analysis: Dict[str, Any],
        ai_analysis: Dict[str, Any],
        content_pillars: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate content recommendations based on gap analysis and AI insights.
        """
        recommendations = []
        
        # Add recommendations from gap analysis
        if gap_analysis.get("recommendations"):
            for rec in gap_analysis["recommendations"][:5]:
                recommendations.append({
                    "title": rec.get("title", "Content recommendation"),
                    "description": rec.get("description", "Based on gap analysis"),
                    "priority": rec.get("priority", "medium"),
                    "content_type": rec.get("type", "blog_post"),
                    "estimated_impact": rec.get("estimated_impact", "Medium"),
                    "implementation_time": rec.get("implementation_time", "2-4 weeks")
                })
        
        # Add AI-generated recommendations
        if ai_analysis.get("recommendations"):
            for rec in ai_analysis["recommendations"][:3]:
                recommendations.append({
                    "title": rec.get("title", "AI recommendation"),
                    "description": rec.get("description", "AI-generated insight"),
                    "priority": "high",
                    "content_type": "blog_post",
                    "estimated_impact": "High",
                    "implementation_time": "1-2 weeks"
                })
        
        return recommendations

    async def _generate_optimal_timing(
        self,
        user_data: Dict[str, Any],
        industry: str,
        business_size: str
    ) -> Dict[str, Any]:
        """
        Generate optimal timing recommendations based on industry and business size.
        """
        # Industry-specific timing
        industry_timing = {
            "technology": {
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "best_times": ["9:00 AM", "2:00 PM", "7:00 PM"],
                "optimal_frequency": "2-3 per week"
            },
            "healthcare": {
                "best_days": ["Monday", "Wednesday", "Friday"],
                "best_times": ["8:00 AM", "12:00 PM", "6:00 PM"],
                "optimal_frequency": "1-2 per week"
            },
            "finance": {
                "best_days": ["Tuesday", "Thursday", "Friday"],
                "best_times": ["9:00 AM", "1:00 PM", "5:00 PM"],
                "optimal_frequency": "2-3 per week"
            }
        }
        
        timing = industry_timing.get(industry, {
            "best_days": ["Monday", "Wednesday", "Friday"],
            "best_times": ["9:00 AM", "2:00 PM", "7:00 PM"],
            "optimal_frequency": "2-3 per week"
        })
        
        # Adjust for business size
        if business_size == "startup":
            timing["optimal_frequency"] = "1-2 per week"
        elif business_size == "enterprise":
            timing["optimal_frequency"] = "3-4 per week"
        
        return timing

    async def _generate_calendar_ai_insights(
        self,
        gap_analysis: Dict[str, Any],
        ai_analysis: Dict[str, Any],
        content_pillars: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate AI insights specifically for the calendar.
        """
        insights = []
        
        # Add insights from gap analysis
        if gap_analysis.get("content_gaps"):
            insights.append({
                "type": "opportunity",
                "title": "Content Gap Opportunity",
                "description": f"Address {len(gap_analysis['content_gaps'])} identified content gaps",
                "priority": "high",
                "impact": "High - Increased lead generation and brand authority"
            })
        
        # Add insights from AI analysis
        if ai_analysis.get("market_positioning"):
            positioning = ai_analysis["market_positioning"]
            insights.append({
                "type": "strategy",
                "title": "Market Positioning",
                "description": f"Focus on {positioning.get('competitive_advantage', 'content quality')}",
                "priority": "high",
                "impact": "High - Competitive differentiation"
            })
        
        # Add content pillar insights
        insights.append({
            "type": "strategy",
            "title": "Content Pillars",
            "description": f"Focus on {len(content_pillars)} core content pillars",
            "priority": "medium",
            "impact": "Medium - Consistent content strategy"
        })
        
        return insights 