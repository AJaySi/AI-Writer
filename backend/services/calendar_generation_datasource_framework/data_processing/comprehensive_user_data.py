"""
Comprehensive User Data Processor

Extracted from calendar_generator_service.py to improve maintainability
and align with 12-step implementation plan. Now includes active strategy
management with 3-tier caching for optimal performance.
"""

import time
from typing import Dict, Any, Optional, List
from loguru import logger

import sys
import os

# Add the services directory to the path for proper imports
services_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

try:
    from onboarding_data_service import OnboardingDataService
    from ai_analytics_service import AIAnalyticsService
    from content_gap_analyzer.ai_engine_service import AIEngineService
    from active_strategy_service import ActiveStrategyService
except ImportError:
    # Fallback for testing environments - create mock classes
    class OnboardingDataService:
        def get_personalized_ai_inputs(self, user_id):
            return {}
    
    class AIAnalyticsService:
        async def generate_strategic_intelligence(self, strategy_id):
            return {"insights": [], "recommendations": []}
    
    class AIEngineService:
        async def generate_content_recommendations(self, data):
            return []
    
    class ActiveStrategyService:
        async def get_active_strategy(self, user_id, force_refresh=False):
            return None


class ComprehensiveUserDataProcessor:
    """Process comprehensive user data from all database sources with active strategy management."""
    
    def __init__(self, db_session=None):
        self.onboarding_service = OnboardingDataService()
        self.active_strategy_service = ActiveStrategyService(db_session)
    
    async def get_comprehensive_user_data(self, user_id: int, strategy_id: Optional[int]) -> Dict[str, Any]:
        """Get comprehensive user data from all database sources."""
        try:
            logger.info(f"Getting comprehensive user data for user {user_id}")
            
            # Get onboarding data (not async)
            onboarding_data = self.onboarding_service.get_personalized_ai_inputs(user_id)
            
            # Get AI analysis results from the working endpoint
            try:
                ai_analytics = AIAnalyticsService()
                ai_analysis_results = await ai_analytics.generate_strategic_intelligence(strategy_id or 1)
            except Exception as e:
                logger.warning(f"Could not get AI analysis results: {str(e)}")
                ai_analysis_results = {"insights": [], "recommendations": []}
            
            # Get gap analysis data from the working endpoint
            try:
                ai_engine = AIEngineService()
                gap_analysis_data = await ai_engine.generate_content_recommendations(onboarding_data)
            except Exception as e:
                logger.warning(f"Could not get gap analysis data: {str(e)}")
                gap_analysis_data = []
            
            # Get active strategy data with 3-tier caching for Phase 1 and Phase 2
            strategy_data = {}
            active_strategy = await self.active_strategy_service.get_active_strategy(user_id)
            
            if active_strategy:
                strategy_data = active_strategy
                logger.info(f"🎯 Retrieved ACTIVE strategy {active_strategy.get('id')} with {len(active_strategy)} fields for user {user_id}")
                logger.info(f"📊 Strategy activation status: {active_strategy.get('activation_status', {}).get('activation_date', 'Not activated')}")
            elif strategy_id:
                # Fallback to specific strategy ID if provided
                from .strategy_data import StrategyDataProcessor
                strategy_processor = StrategyDataProcessor()
                strategy_data = await strategy_processor.get_strategy_data(strategy_id)
                logger.warning(f"⚠️ No active strategy found, using fallback strategy {strategy_id}")
            else:
                logger.warning("⚠️ No active strategy found and no strategy ID provided")
            
            # Get content recommendations
            recommendations_data = await self._get_recommendations_data(user_id, strategy_id)
            
            # Get performance metrics
            performance_data = await self._get_performance_data(user_id, strategy_id)
            
            # Build comprehensive response with enhanced strategy data
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
                "strategy_data": strategy_data,  # Now contains comprehensive strategy data
                "recommendations_data": recommendations_data,
                "performance_data": performance_data,
                "industry": strategy_data.get("industry") or onboarding_data.get("website_analysis", {}).get("industry_focus", "technology"),
                "target_audience": strategy_data.get("target_audience") or onboarding_data.get("website_analysis", {}).get("target_audience", []),
                "business_goals": strategy_data.get("business_objectives") or ["Increase brand awareness", "Generate leads", "Establish thought leadership"],
                "website_analysis": onboarding_data.get("website_analysis", {}),
                "competitor_analysis": onboarding_data.get("competitor_analysis", {}),
                "keyword_analysis": onboarding_data.get("keyword_analysis", {}),
                
                # Enhanced strategy data for 12-step prompt chaining
                "strategy_analysis": strategy_data.get("strategy_analysis", {}),
                "quality_indicators": strategy_data.get("quality_indicators", {})
            }
            
            logger.info(f"✅ Comprehensive user data prepared for user {user_id}")
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"❌ Error getting comprehensive user data: {str(e)}")
            return {
                "user_id": user_id,
                "error": str(e),
                "status": "error"
            }

    async def get_comprehensive_user_data_cached(
        self, 
        user_id: int, 
        strategy_id: Optional[int] = None,
        force_refresh: bool = False,
        db_session = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive user data with caching support.
        This method provides caching while maintaining backward compatibility.
        """
        try:
            # If we have a database session, try to use cache
            if db_session:
                try:
                    from services.comprehensive_user_data_cache_service import ComprehensiveUserDataCacheService
                    cache_service = ComprehensiveUserDataCacheService(db_session)
                    return await cache_service.get_comprehensive_user_data_backward_compatible(
                        user_id, strategy_id, force_refresh=force_refresh
                    )
                except Exception as cache_error:
                    logger.warning(f"Cache service failed, falling back to direct processing: {str(cache_error)}")
            
            # Fallback to direct processing
            return await self.get_comprehensive_user_data(user_id, strategy_id)
            
        except Exception as e:
            logger.error(f"❌ Error in cached method: {str(e)}")
            # Final fallback
            return await self.get_comprehensive_user_data(user_id, strategy_id)
    
    async def _get_recommendations_data(self, user_id: int, strategy_id: Optional[int]) -> List[Dict[str, Any]]:
        """Get content recommendations data."""
        try:
            # This would be implemented based on existing logic
            return []
        except Exception as e:
            logger.warning(f"Could not get recommendations data: {str(e)}")
            return []
    
    async def _get_performance_data(self, user_id: int, strategy_id: Optional[int]) -> Dict[str, Any]:
        """Get performance metrics data."""
        try:
            # This would be implemented based on existing logic
            return {}
        except Exception as e:
            logger.warning(f"Could not get performance data: {str(e)}")
            return {}
