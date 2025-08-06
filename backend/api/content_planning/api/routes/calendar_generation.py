"""
Calendar Generation Routes for Content Planning API
Extracted from the main content_planning.py file for better organization.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger
import time

# Import database service
from services.database import get_db_session, get_db
from services.content_planning_db import ContentPlanningDBService

# Import models
from ..models.requests import (
    CalendarGenerationRequest, ContentOptimizationRequest,
    PerformancePredictionRequest, ContentRepurposingRequest,
    TrendingTopicsRequest
)
from ..models.responses import (
    CalendarGenerationResponse, ContentOptimizationResponse,
    PerformancePredictionResponse, ContentRepurposingResponse,
    TrendingTopicsResponse
)

# Import utilities
from ...utils.error_handlers import ContentPlanningErrorHandler
from ...utils.response_builders import ResponseBuilder
from ...utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

# Import services
from ...services.calendar_generation_service import CalendarGenerationService

# Initialize services
calendar_generation_service = CalendarGenerationService()

# Create router
router = APIRouter(prefix="/calendar-generation", tags=["calendar-generation"])

@router.post("/generate-calendar", response_model=CalendarGenerationResponse)
async def generate_comprehensive_calendar(request: CalendarGenerationRequest):
    """
    Generate a comprehensive AI-powered content calendar using database insights.
    This endpoint uses advanced AI analysis and comprehensive user data.
    """
    try:
        logger.info(f"🎯 Generating comprehensive calendar for user {request.user_id}")
        
        calendar_data = await calendar_generation_service.generate_comprehensive_calendar(
            user_id=request.user_id,
            strategy_id=request.strategy_id,
            calendar_type=request.calendar_type,
            industry=request.industry,
            business_size=request.business_size
        )
        
        return CalendarGenerationResponse(**calendar_data)
        
    except Exception as e:
        logger.error(f"❌ Error generating comprehensive calendar: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating comprehensive calendar: {str(e)}"
        )

@router.post("/optimize-content", response_model=ContentOptimizationResponse)
async def optimize_content_for_platform(request: ContentOptimizationRequest):
    """
    Optimize content for specific platforms using database insights.
    
    This endpoint optimizes content based on:
    - Historical performance data for the platform
    - Audience preferences from onboarding data
    - Gap analysis insights for content improvement
    - Competitor analysis for differentiation
    """
    try:
        logger.info(f"🔧 Starting content optimization for user {request.user_id}")
        
        result = await calendar_generation_service.optimize_content_for_platform(
            user_id=request.user_id,
            title=request.title,
            description=request.description,
            content_type=request.content_type,
            target_platform=request.target_platform,
            event_id=request.event_id
        )
        
        return ContentOptimizationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error optimizing content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize content: {str(e)}"
        )

@router.post("/performance-predictions", response_model=PerformancePredictionResponse)
async def predict_content_performance(request: PerformancePredictionRequest):
    """
    Predict content performance using database insights.
    
    This endpoint predicts performance based on:
    - Historical performance data
    - Audience demographics and preferences
    - Content type and platform patterns
    - Gap analysis opportunities
    """
    try:
        logger.info(f"📊 Starting performance prediction for user {request.user_id}")
        
        result = await calendar_generation_service.predict_content_performance(
            user_id=request.user_id,
            content_type=request.content_type,
            platform=request.platform,
            content_data=request.content_data,
            strategy_id=request.strategy_id
        )
        
        return PerformancePredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Error predicting content performance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict content performance: {str(e)}"
        )

@router.post("/repurpose-content", response_model=ContentRepurposingResponse)
async def repurpose_content_across_platforms(request: ContentRepurposingRequest):
    """
    Repurpose content across different platforms using database insights.
    
    This endpoint suggests content repurposing based on:
    - Existing content and strategy data
    - Gap analysis opportunities
    - Platform-specific requirements
    - Audience preferences
    """
    try:
        logger.info(f"🔄 Starting content repurposing for user {request.user_id}")
        
        result = await calendar_generation_service.repurpose_content_across_platforms(
            user_id=request.user_id,
            original_content=request.original_content,
            target_platforms=request.target_platforms,
            strategy_id=request.strategy_id
        )
        
        return ContentRepurposingResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Error repurposing content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to repurpose content: {str(e)}"
        )

@router.get("/trending-topics", response_model=TrendingTopicsResponse)
async def get_trending_topics(
    user_id: int = Query(..., description="User ID"),
    industry: str = Query(..., description="Industry for trending topics"),
    limit: int = Query(10, description="Number of trending topics to return")
):
    """
    Get trending topics relevant to the user's industry and content gaps.
    
    This endpoint provides trending topics based on:
    - Industry-specific trends
    - Gap analysis keyword opportunities
    - Audience alignment assessment
    - Competitor analysis insights
    """
    try:
        logger.info(f"📈 Getting trending topics for user {user_id} in {industry}")
        
        result = await calendar_generation_service.get_trending_topics(
            user_id=user_id,
            industry=industry,
            limit=limit
        )
        
        return TrendingTopicsResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Error getting trending topics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get trending topics: {str(e)}"
        )

@router.get("/comprehensive-user-data")
async def get_comprehensive_user_data(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive user data for calendar generation.
    This endpoint aggregates all data points needed for the calendar wizard.
    """
    try:
        logger.info(f"Getting comprehensive user data for user_id: {user_id}")
        
        result = await calendar_generation_service.get_comprehensive_user_data(user_id)
        
        logger.info(f"Successfully retrieved comprehensive user data for user_id: {user_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error getting comprehensive user data for user_id {user_id}: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving comprehensive user data: {str(e)}"
        )

@router.get("/health")
async def calendar_generation_health_check():
    """
    Health check for calendar generation services.
    """
    try:
        logger.info("🏥 Performing calendar generation health check")
        
        result = await calendar_generation_service.health_check()
        
        logger.info("✅ Calendar generation health check completed")
        return result
        
    except Exception as e:
        logger.error(f"❌ Calendar generation health check failed: {str(e)}")
        return {
            "service": "calendar_generation",
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }
