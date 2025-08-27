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
import asyncio
import random

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
# Removed old service import - using orchestrator only
from ...services.calendar_generation_service import CalendarGenerationService

# Create router
router = APIRouter(prefix="/calendar-generation", tags=["calendar-generation"])

@router.post("/generate-calendar", response_model=CalendarGenerationResponse)
async def generate_comprehensive_calendar(request: CalendarGenerationRequest, db: Session = Depends(get_db)):
    """
    Generate a comprehensive AI-powered content calendar using database insights.
    This endpoint uses advanced AI analysis and comprehensive user data.
    Now ensures Phase 1 and Phase 2 use the ACTIVE strategy with 3-tier caching.
    """
    try:
        logger.info(f"🎯 Generating comprehensive calendar for user {request.user_id}")
        
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        calendar_data = await calendar_service.generate_comprehensive_calendar(
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
async def optimize_content_for_platform(request: ContentOptimizationRequest, db: Session = Depends(get_db)):
    """
    Optimize content for specific platforms using database insights.
    
    This endpoint optimizes content based on:
    - Historical performance data for the platform
    - Audience preferences from onboarding data
    - Gap analysis insights for content improvement
    - Competitor analysis for differentiation
    - Active strategy data for optimal alignment
    """
    try:
        logger.info(f"🔧 Starting content optimization for user {request.user_id}")
        
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        result = await calendar_service.optimize_content_for_platform(
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
async def predict_content_performance(request: PerformancePredictionRequest, db: Session = Depends(get_db)):
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
        
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        result = await calendar_service.predict_content_performance(
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
async def repurpose_content_across_platforms(request: ContentRepurposingRequest, db: Session = Depends(get_db)):
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
        
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        result = await calendar_service.repurpose_content_across_platforms(
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
    limit: int = Query(10, description="Number of trending topics to return"),
    db: Session = Depends(get_db)
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
        
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        result = await calendar_service.get_trending_topics(
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
    force_refresh: bool = Query(False, description="Force refresh cache"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive user data for calendar generation with intelligent caching.
    This endpoint aggregates all data points needed for the calendar wizard.
    """
    try:
        logger.info(f"Getting comprehensive user data for user_id: {user_id} (force_refresh={force_refresh})")
        
        # Initialize cache service
        from services.comprehensive_user_data_cache_service import ComprehensiveUserDataCacheService
        cache_service = ComprehensiveUserDataCacheService(db)
        
        # Get data with caching
        data, is_cached = await cache_service.get_cached_data(
            user_id, None, force_refresh=force_refresh
        )
        
        if not data:
            raise HTTPException(status_code=500, detail="Failed to retrieve user data")
        
        # Add cache metadata to response
        result = {
            "status": "success",
            "data": data,
            "cache_info": {
                "is_cached": is_cached,
                "force_refresh": force_refresh,
                "timestamp": datetime.utcnow().isoformat()
            },
            "message": f"Comprehensive user data retrieved successfully (cache: {'HIT' if is_cached else 'MISS'})"
        }
        
        logger.info(f"Successfully retrieved comprehensive user data for user_id: {user_id} (cache: {'HIT' if is_cached else 'MISS'})")
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
async def calendar_generation_health_check(db: Session = Depends(get_db)):
    """
    Health check for calendar generation services.
    """
    try:
        logger.info("🏥 Performing calendar generation health check")
        
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        result = await calendar_service.health_check()
        
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

@router.get("/progress/{session_id}")
async def get_calendar_generation_progress(session_id: str, db: Session = Depends(get_db)):
    """
    Get real-time progress of calendar generation for a specific session.
    This endpoint is polled by the frontend modal to show progress updates.
    """
    try:
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        # Get progress from orchestrator only - no fallbacks
        orchestrator_progress = calendar_service.get_orchestrator_progress(session_id)
        
        if not orchestrator_progress:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Return orchestrator progress (data is already in the correct format)
        return {
            "session_id": session_id,
            "status": orchestrator_progress.get("status", "initializing"),
            "current_step": orchestrator_progress.get("current_step", 0),
            "step_progress": orchestrator_progress.get("step_progress", 0),
            "overall_progress": orchestrator_progress.get("overall_progress", 0),
            "step_results": orchestrator_progress.get("step_results", {}),
            "quality_scores": orchestrator_progress.get("quality_scores", {}),
            "transparency_messages": orchestrator_progress.get("transparency_messages", []),
            "educational_content": orchestrator_progress.get("educational_content", []),
            "errors": orchestrator_progress.get("errors", []),
            "warnings": orchestrator_progress.get("warnings", []),
            "estimated_completion": orchestrator_progress.get("estimated_completion"),
            "last_updated": orchestrator_progress.get("last_updated")
        }
        
    except Exception as e:
        logger.error(f"Error getting calendar generation progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get progress")

@router.post("/start")
async def start_calendar_generation(request: CalendarGenerationRequest, db: Session = Depends(get_db)):
    """
    Start calendar generation and return a session ID for progress tracking.
    Prevents duplicate sessions for the same user.
    """
    try:
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        # Check if user already has an active session
        user_id = request.user_id
        existing_session = calendar_service._get_active_session_for_user(user_id)
        
        if existing_session:
            logger.info(f"🔄 User {user_id} already has active session: {existing_session}")
            return {
                "session_id": existing_session,
                "status": "existing",
                "message": "Using existing active session",
                "estimated_duration": "2-3 minutes"
            }
        
        # Generate a unique session ID
        session_id = f"calendar-session-{int(time.time())}-{random.randint(1000, 9999)}"
        
        # Initialize orchestrator session
        success = calendar_service.initialize_orchestrator_session(session_id, request.dict())
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to initialize orchestrator session")
        
        # Start the generation process asynchronously using orchestrator
        # This will run in the background while the frontend polls for progress
        asyncio.create_task(calendar_service.start_orchestrator_generation(session_id, request.dict()))
        
        return {
            "session_id": session_id,
            "status": "started",
            "message": "Calendar generation started successfully with 12-step orchestrator",
            "estimated_duration": "2-3 minutes"
        }
        
    except Exception as e:
        logger.error(f"Error starting calendar generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start calendar generation")

@router.delete("/cancel/{session_id}")
async def cancel_calendar_generation(session_id: str, db: Session = Depends(get_db)):
    """
    Cancel an ongoing calendar generation session.
    """
    try:
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        # Cancel orchestrator session
        if session_id in calendar_service.orchestrator_sessions:
            calendar_service.orchestrator_sessions[session_id]["status"] = "cancelled"
            success = True
        else:
            success = False
        
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {
            "session_id": session_id,
            "status": "cancelled",
            "message": "Calendar generation cancelled successfully"
        }
        
    except Exception as e:
        logger.error(f"Error cancelling calendar generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel calendar generation")

# Cache Management Endpoints
@router.get("/cache/stats")
async def get_cache_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get comprehensive user data cache statistics."""
    try:
        from services.comprehensive_user_data_cache_service import ComprehensiveUserDataCacheService
        cache_service = ComprehensiveUserDataCacheService(db)
        stats = cache_service.get_cache_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get cache stats")

@router.delete("/cache/invalidate/{user_id}")
async def invalidate_user_cache(
    user_id: int,
    strategy_id: Optional[int] = Query(None, description="Strategy ID to invalidate (optional)"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Invalidate cache for a specific user/strategy."""
    try:
        from services.comprehensive_user_data_cache_service import ComprehensiveUserDataCacheService
        cache_service = ComprehensiveUserDataCacheService(db)
        success = cache_service.invalidate_cache(user_id, strategy_id)
        
        if success:
            return {
                "status": "success",
                "message": f"Cache invalidated for user {user_id}" + (f" and strategy {strategy_id}" if strategy_id else ""),
                "user_id": user_id,
                "strategy_id": strategy_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to invalidate cache")
            
    except Exception as e:
        logger.error(f"Error invalidating cache: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to invalidate cache")

@router.post("/cache/cleanup")
async def cleanup_expired_cache(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Clean up expired cache entries."""
    try:
        from services.comprehensive_user_data_cache_service import ComprehensiveUserDataCacheService
        cache_service = ComprehensiveUserDataCacheService(db)
        deleted_count = cache_service.cleanup_expired_cache()
        
        return {
            "status": "success",
            "message": f"Cleaned up {deleted_count} expired cache entries",
            "deleted_count": deleted_count
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up cache: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clean up cache")

@router.get("/sessions")
async def list_active_sessions(db: Session = Depends(get_db)):
    """
    List all active calendar generation sessions.
    """
    try:
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        sessions = []
        for session_id, session_data in calendar_service.orchestrator_sessions.items():
            sessions.append({
                "session_id": session_id,
                "user_id": session_data.get("user_id"),
                "status": session_data.get("status"),
                "start_time": session_data.get("start_time").isoformat() if session_data.get("start_time") else None,
                "progress": session_data.get("progress", {})
            })
        
        return {
            "sessions": sessions,
            "total_sessions": len(sessions),
            "active_sessions": len([s for s in sessions if s["status"] in ["initializing", "running"]])
        }
        
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list sessions")

@router.delete("/sessions/cleanup")
async def cleanup_old_sessions(db: Session = Depends(get_db)):
    """
    Clean up old sessions.
    """
    try:
        # Initialize service with database session for active strategy access
        calendar_service = CalendarGenerationService(db)
        
        # Clean up old sessions for all users
        current_time = datetime.now()
        sessions_to_remove = []
        
        for session_id, session_data in list(calendar_service.orchestrator_sessions.items()):
            start_time = session_data.get("start_time")
            if start_time:
                # Remove sessions older than 1 hour
                if (current_time - start_time).total_seconds() > 3600:  # 1 hour
                    sessions_to_remove.append(session_id)
                # Also remove completed/error sessions older than 10 minutes
                elif session_data.get("status") in ["completed", "error", "cancelled"]:
                    if (current_time - start_time).total_seconds() > 600:  # 10 minutes
                        sessions_to_remove.append(session_id)
        
        # Remove the sessions
        for session_id in sessions_to_remove:
            del calendar_service.orchestrator_sessions[session_id]
            logger.info(f"🧹 Cleaned up old session: {session_id}")
        
        return {
            "status": "success",
            "message": f"Cleaned up {len(sessions_to_remove)} old sessions",
            "cleaned_count": len(sessions_to_remove)
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cleanup sessions")
