"""
Gap Analysis Routes for Content Planning API
Extracted from the main content_planning.py file for better organization.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger
import json

# Import database service
from services.database import get_db_session, get_db
from services.content_planning_db import ContentPlanningDBService

# Import models
from ..models.requests import ContentGapAnalysisCreate, ContentGapAnalysisRequest
from ..models.responses import ContentGapAnalysisResponse, ContentGapAnalysisFullResponse

# Import utilities
from ...utils.error_handlers import ContentPlanningErrorHandler
from ...utils.response_builders import ResponseBuilder
from ...utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

# Import services
from ...services.gap_analysis_service import GapAnalysisService

# Initialize services
gap_analysis_service = GapAnalysisService()

# Create router
router = APIRouter(prefix="/gap-analysis", tags=["gap-analysis"])

@router.post("/", response_model=ContentGapAnalysisResponse)
async def create_content_gap_analysis(
    analysis: ContentGapAnalysisCreate,
    db: Session = Depends(get_db)
):
    """Create a new content gap analysis."""
    try:
        logger.info(f"Creating content gap analysis for: {analysis.website_url}")
        
        analysis_data = analysis.dict()
        created_analysis = await gap_analysis_service.create_gap_analysis(analysis_data, db)
        
        return ContentGapAnalysisResponse(**created_analysis)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating content gap analysis: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "create_content_gap_analysis")

@router.get("/", response_model=Dict[str, Any])
async def get_content_gap_analyses(
    user_id: Optional[int] = Query(None, description="User ID"),
    strategy_id: Optional[int] = Query(None, description="Strategy ID"),
    force_refresh: bool = Query(False, description="Force refresh gap analysis")
):
    """Get content gap analysis with real AI insights - Database first approach."""
    try:
        logger.info(f"🚀 Starting content gap analysis for user: {user_id}, strategy: {strategy_id}, force_refresh: {force_refresh}")
        
        result = await gap_analysis_service.get_gap_analyses(user_id, strategy_id, force_refresh)
        return result
        
    except Exception as e:
        logger.error(f"❌ Error generating content gap analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating content gap analysis: {str(e)}")

@router.get("/{analysis_id}", response_model=ContentGapAnalysisResponse)
async def get_content_gap_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific content gap analysis by ID."""
    try:
        logger.info(f"Fetching content gap analysis: {analysis_id}")
        
        analysis = await gap_analysis_service.get_gap_analysis_by_id(analysis_id, db)
        return ContentGapAnalysisResponse(**analysis)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting content gap analysis: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_content_gap_analysis")

@router.post("/analyze", response_model=ContentGapAnalysisFullResponse)
async def analyze_content_gaps(request: ContentGapAnalysisRequest):
    """
    Analyze content gaps between your website and competitors.
    """
    try:
        logger.info(f"Starting content gap analysis for: {request.website_url}")
        
        request_data = request.dict()
        result = await gap_analysis_service.analyze_content_gaps(request_data)
        
        return ContentGapAnalysisFullResponse(**result)
        
    except Exception as e:
        logger.error(f"Error analyzing content gaps: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing content gaps: {str(e)}"
        )

@router.get("/user/{user_id}/analyses")
async def get_user_gap_analyses(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all gap analyses for a specific user."""
    try:
        logger.info(f"Fetching gap analyses for user: {user_id}")
        
        analyses = await gap_analysis_service.get_user_gap_analyses(user_id, db)
        return {
            "user_id": user_id,
            "analyses": analyses,
            "total_count": len(analyses)
        }
        
    except Exception as e:
        logger.error(f"Error getting user gap analyses: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_user_gap_analyses")

@router.put("/{analysis_id}", response_model=ContentGapAnalysisResponse)
async def update_content_gap_analysis(
    analysis_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update a content gap analysis."""
    try:
        logger.info(f"Updating content gap analysis: {analysis_id}")
        
        updated_analysis = await gap_analysis_service.update_gap_analysis(analysis_id, update_data, db)
        return ContentGapAnalysisResponse(**updated_analysis)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating content gap analysis: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "update_content_gap_analysis")

@router.delete("/{analysis_id}")
async def delete_content_gap_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """Delete a content gap analysis."""
    try:
        logger.info(f"Deleting content gap analysis: {analysis_id}")
        
        deleted = await gap_analysis_service.delete_gap_analysis(analysis_id, db)
        
        if deleted:
            return {"message": f"Content gap analysis {analysis_id} deleted successfully"}
        else:
            raise ContentPlanningErrorHandler.handle_not_found_error("Content gap analysis", analysis_id)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting content gap analysis: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "delete_content_gap_analysis")
