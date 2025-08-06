"""
Strategy Routes for Content Planning API
Extracted from the main content_planning.py file for better organization.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

# Import database service
from services.database import get_db_session, get_db
from services.content_planning_db import ContentPlanningDBService

# Import models
from ..models.requests import ContentStrategyCreate
from ..models.responses import ContentStrategyResponse

# Import utilities
from ...utils.error_handlers import ContentPlanningErrorHandler
from ...utils.response_builders import ResponseBuilder
from ...utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

# Import services
from ...services.enhanced_strategy_service import EnhancedStrategyService
from ...services.enhanced_strategy_db_service import EnhancedStrategyDBService

# Create router
router = APIRouter(prefix="/strategies", tags=["strategies"])

@router.post("/", response_model=ContentStrategyResponse)
async def create_content_strategy(
    strategy: ContentStrategyCreate,
    db: Session = Depends(get_db)
):
    """Create a new content strategy."""
    try:
        logger.info(f"Creating content strategy: {strategy.name}")
        
        db_service = EnhancedStrategyDBService(db)
        strategy_service = EnhancedStrategyService(db_service)
        strategy_data = strategy.dict()
        created_strategy = await strategy_service.create_enhanced_strategy(strategy_data, db)
        
        return ContentStrategyResponse(**created_strategy)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating content strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "create_content_strategy")

@router.get("/", response_model=Dict[str, Any])
async def get_content_strategies(
    user_id: Optional[int] = Query(None, description="User ID"),
    strategy_id: Optional[int] = Query(None, description="Strategy ID")
):
    """
    Get content strategies with comprehensive logging for debugging.
    """
    try:
        logger.info(f"🚀 Starting content strategy analysis for user: {user_id}, strategy: {strategy_id}")
        
        # Create a temporary database session for this operation
        from services.database import get_db_session
        temp_db = get_db_session()
        try:
            db_service = EnhancedStrategyDBService(temp_db)
            strategy_service = EnhancedStrategyService(db_service)
            result = await strategy_service.get_enhanced_strategies(user_id, strategy_id, temp_db)
            return result
        finally:
            temp_db.close()
        
    except Exception as e:
        logger.error(f"❌ Error retrieving content strategies: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving content strategies: {str(e)}"
        )

@router.get("/{strategy_id}", response_model=ContentStrategyResponse)
async def get_content_strategy(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific content strategy by ID."""
    try:
        logger.info(f"Fetching content strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        strategy_service = EnhancedStrategyService(db_service)
        strategy_data = await strategy_service.get_enhanced_strategies(strategy_id=strategy_id, db=db)
        strategy = strategy_data.get('strategies', [{}])[0] if strategy_data.get('strategies') else {}
        return ContentStrategyResponse(**strategy)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting content strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_content_strategy")

@router.put("/{strategy_id}", response_model=ContentStrategyResponse)
async def update_content_strategy(
    strategy_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update a content strategy."""
    try:
        logger.info(f"Updating content strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        updated_strategy = await db_service.update_enhanced_strategy(strategy_id, update_data)
        
        if not updated_strategy:
            raise ContentPlanningErrorHandler.handle_not_found_error("Content strategy", strategy_id)
        
        return ContentStrategyResponse(**updated_strategy.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating content strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "update_content_strategy")

@router.delete("/{strategy_id}")
async def delete_content_strategy(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Delete a content strategy."""
    try:
        logger.info(f"Deleting content strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        deleted = await db_service.delete_enhanced_strategy(strategy_id)
        
        if deleted:
            return {"message": f"Content strategy {strategy_id} deleted successfully"}
        else:
            raise ContentPlanningErrorHandler.handle_not_found_error("Content strategy", strategy_id)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting content strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "delete_content_strategy")

@router.get("/{strategy_id}/analytics")
async def get_strategy_analytics(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get analytics for a specific strategy."""
    try:
        logger.info(f"Fetching analytics for strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        analytics = await db_service.get_enhanced_strategies_with_analytics(strategy_id)
        
        if not analytics:
            raise ContentPlanningErrorHandler.handle_not_found_error("Content strategy", strategy_id)
        
        return analytics[0] if analytics else {}
        
    except Exception as e:
        logger.error(f"Error getting strategy analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{strategy_id}/summary")
async def get_strategy_summary(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get a comprehensive summary of a strategy with analytics."""
    try:
        logger.info(f"Fetching summary for strategy: {strategy_id}")
        
        # Get strategy with analytics for comprehensive summary
        db_service = EnhancedStrategyDBService(db)
        strategy_with_analytics = await db_service.get_enhanced_strategies_with_analytics(strategy_id)
        
        if not strategy_with_analytics:
            raise ContentPlanningErrorHandler.handle_not_found_error("Content strategy", strategy_id)
        
        strategy_data = strategy_with_analytics[0]
        
        # Create a comprehensive summary
        summary = {
            "strategy_id": strategy_id,
            "name": strategy_data.get("name", "Unknown Strategy"),
            "completion_percentage": strategy_data.get("completion_percentage", 0),
            "created_at": strategy_data.get("created_at"),
            "updated_at": strategy_data.get("updated_at"),
            "analytics_summary": {
                "total_analyses": len(strategy_data.get("ai_analyses", [])),
                "last_analysis": strategy_data.get("ai_analyses", [{}])[-1] if strategy_data.get("ai_analyses") else None
            }
        }
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting strategy summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 