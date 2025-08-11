"""
Utility Endpoints
Handles utility endpoints for enhanced content strategies.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from loguru import logger

# Import database
from services.database import get_db_session

# Import services
from ....services.enhanced_strategy_service import EnhancedStrategyService
from ....services.enhanced_strategy_db_service import EnhancedStrategyDBService

# Import utilities
from ....utils.error_handlers import ContentPlanningErrorHandler
from ....utils.response_builders import ResponseBuilder
from ....utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

router = APIRouter(tags=["Strategy Utilities"])

# Helper function to get database session
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

@router.get("/onboarding-data")
async def get_onboarding_data(
    user_id: Optional[int] = Query(None, description="User ID to get onboarding data for"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get onboarding data for enhanced strategy auto-population."""
    try:
        logger.info(f"🚀 Getting onboarding data for user: {user_id}")
        
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        # Ensure we have a valid user_id
        actual_user_id = user_id or 1
        onboarding_data = await enhanced_service._get_onboarding_data(actual_user_id)
        
        logger.info(f"✅ Onboarding data retrieved successfully for user: {actual_user_id}")
        
        return ResponseBuilder.create_success_response(
            message="Onboarding data retrieved successfully",
            data=onboarding_data
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting onboarding data: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_onboarding_data")

@router.get("/tooltips")
async def get_enhanced_strategy_tooltips() -> Dict[str, Any]:
    """Get tooltip data for enhanced strategy fields."""
    try:
        logger.info("🚀 Getting enhanced strategy tooltips")
        
        # Mock tooltip data - in real implementation, this would come from a database
        tooltip_data = {
            "business_objectives": {
                "title": "Business Objectives",
                "description": "Define your primary and secondary business goals that content will support.",
                "examples": ["Increase brand awareness by 25%", "Generate 100 qualified leads per month"],
                "best_practices": ["Be specific and measurable", "Align with overall business strategy"]
            },
            "target_metrics": {
                "title": "Target Metrics",
                "description": "Specify the KPIs that will measure content strategy success.",
                "examples": ["Traffic growth: 30%", "Engagement rate: 5%", "Conversion rate: 2%"],
                "best_practices": ["Set realistic targets", "Track both leading and lagging indicators"]
            },
            "content_budget": {
                "title": "Content Budget",
                "description": "Define your allocated budget for content creation and distribution.",
                "examples": ["$10,000 per month", "15% of marketing budget"],
                "best_practices": ["Include both creation and distribution costs", "Plan for seasonal variations"]
            },
            "team_size": {
                "title": "Team Size",
                "description": "Number of team members dedicated to content creation and management.",
                "examples": ["3 content creators", "1 content manager", "2 designers"],
                "best_practices": ["Consider skill sets and workload", "Plan for growth"]
            },
            "implementation_timeline": {
                "title": "Implementation Timeline",
                "description": "Timeline for implementing your content strategy.",
                "examples": ["3 months for setup", "6 months for full implementation"],
                "best_practices": ["Set realistic milestones", "Allow for iteration"]
            },
            "market_share": {
                "title": "Market Share",
                "description": "Your current market share and target market share.",
                "examples": ["Current: 5%", "Target: 15%"],
                "best_practices": ["Use reliable data sources", "Set achievable targets"]
            },
            "competitive_position": {
                "title": "Competitive Position",
                "description": "Your position relative to competitors in the market.",
                "examples": ["Market leader", "Challenger", "Niche player"],
                "best_practices": ["Be honest about your position", "Identify opportunities"]
            },
            "performance_metrics": {
                "title": "Performance Metrics",
                "description": "Key metrics to track content performance.",
                "examples": ["Organic traffic", "Engagement rate", "Conversion rate"],
                "best_practices": ["Focus on actionable metrics", "Set up proper tracking"]
            }
        }
        
        logger.info("✅ Enhanced strategy tooltips retrieved successfully")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy tooltips retrieved successfully",
            data=tooltip_data
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategy tooltips: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_tooltips")

@router.get("/disclosure-steps")
async def get_enhanced_strategy_disclosure_steps() -> Dict[str, Any]:
    """Get progressive disclosure steps for enhanced strategy."""
    try:
        logger.info("🚀 Getting enhanced strategy disclosure steps")
        
        # Progressive disclosure steps configuration
        disclosure_steps = [
            {
                "id": "business_context",
                "title": "Business Context",
                "description": "Define your business objectives and context",
                "fields": ["business_objectives", "target_metrics", "content_budget", "team_size", "implementation_timeline", "market_share", "competitive_position", "performance_metrics"],
                "is_complete": False,
                "is_visible": True,
                "dependencies": []
            },
            {
                "id": "audience_intelligence",
                "title": "Audience Intelligence",
                "description": "Understand your target audience",
                "fields": ["content_preferences", "consumption_patterns", "audience_pain_points", "buying_journey", "seasonal_trends", "engagement_metrics"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["business_context"]
            },
            {
                "id": "competitive_intelligence",
                "title": "Competitive Intelligence",
                "description": "Analyze your competitive landscape",
                "fields": ["top_competitors", "competitor_content_strategies", "market_gaps", "industry_trends", "emerging_trends"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["audience_intelligence"]
            },
            {
                "id": "content_strategy",
                "title": "Content Strategy",
                "description": "Define your content approach",
                "fields": ["preferred_formats", "content_mix", "content_frequency", "optimal_timing", "quality_metrics", "editorial_guidelines", "brand_voice"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["competitive_intelligence"]
            },
            {
                "id": "distribution_channels",
                "title": "Distribution Channels",
                "description": "Plan your content distribution",
                "fields": ["traffic_sources", "conversion_rates", "content_roi_targets"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["content_strategy"]
            },
            {
                "id": "target_audience",
                "title": "Target Audience",
                "description": "Define your target audience segments",
                "fields": ["target_audience", "content_pillars"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["distribution_channels"]
            }
        ]
        
        logger.info("✅ Enhanced strategy disclosure steps retrieved successfully")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy disclosure steps retrieved successfully",
            data=disclosure_steps
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategy disclosure steps: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_disclosure_steps")

@router.post("/cache/clear")
async def clear_streaming_cache(
    user_id: Optional[int] = Query(None, description="User ID to clear cache for")
):
    """Clear streaming cache for a specific user or all users."""
    try:
        logger.info(f"🚀 Clearing streaming cache for user: {user_id}")
        
        # Import the cache from the streaming endpoints module
        from .streaming_endpoints import streaming_cache
        
        if user_id:
            # Clear cache for specific user
            cache_keys_to_remove = [
                f"strategic_intelligence_{user_id}",
                f"keyword_research_{user_id}"
            ]
            for key in cache_keys_to_remove:
                if key in streaming_cache:
                    del streaming_cache[key]
                    logger.info(f"✅ Cleared cache for key: {key}")
        else:
            # Clear all cache
            streaming_cache.clear()
            logger.info("✅ Cleared all streaming cache")
        
        return ResponseBuilder.create_success_response(
            message="Streaming cache cleared successfully",
            data={"cleared_for_user": user_id}
        )
        
    except Exception as e:
        logger.error(f"❌ Error clearing streaming cache: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "clear_streaming_cache") 