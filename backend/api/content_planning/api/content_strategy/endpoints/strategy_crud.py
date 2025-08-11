"""
Strategy CRUD Endpoints
Handles CRUD operations for enhanced content strategies.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from loguru import logger
import json
from datetime import datetime

# Import database
from services.database import get_db_session

# Import services
from ....services.enhanced_strategy_service import EnhancedStrategyService
from ....services.enhanced_strategy_db_service import EnhancedStrategyDBService

# Import models
from models.enhanced_strategy_models import EnhancedContentStrategy

# Import utilities
from ....utils.error_handlers import ContentPlanningErrorHandler
from ....utils.response_builders import ResponseBuilder
from ....utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

router = APIRouter(tags=["Strategy CRUD"])

# Helper function to get database session
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
async def create_enhanced_strategy(
    strategy_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new enhanced content strategy."""
    try:
        logger.info(f"Creating enhanced strategy: {strategy_data.get('name', 'Unknown')}")
        
        # Validate required fields
        required_fields = ['user_id', 'name']
        for field in required_fields:
            if field not in strategy_data or not strategy_data[field]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Parse and validate data types
        def parse_float(value: Any) -> Optional[float]:
            if value is None or value == "":
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        def parse_int(value: Any) -> Optional[int]:
            if value is None or value == "":
                return None
            try:
                return int(value)
            except (ValueError, TypeError):
                return None
        
        def parse_json(value: Any) -> Optional[Any]:
            if value is None or value == "":
                return None
            if isinstance(value, str):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return value
        
        def parse_array(value: Any) -> Optional[list]:
            if value is None or value == "":
                return []
            if isinstance(value, str):
                try:
                    parsed = json.loads(value)
                    return parsed if isinstance(parsed, list) else [parsed]
                except json.JSONDecodeError:
                    return [value]
            elif isinstance(value, list):
                return value
            else:
                return [value]
        
        # Parse numeric fields
        numeric_fields = ['content_budget', 'team_size', 'market_share', 'ab_testing_capabilities']
        for field in numeric_fields:
            if field in strategy_data:
                strategy_data[field] = parse_float(strategy_data[field])
        
        # Parse array fields
        array_fields = ['content_preferences', 'consumption_patterns', 'audience_pain_points', 
                       'buying_journey', 'seasonal_trends', 'engagement_metrics', 'top_competitors',
                       'competitor_content_strategies', 'market_gaps', 'industry_trends', 
                       'emerging_trends', 'preferred_formats', 'content_mix', 'content_frequency',
                       'optimal_timing', 'quality_metrics', 'editorial_guidelines', 'brand_voice',
                       'traffic_sources', 'conversion_rates', 'content_roi_targets', 'target_audience',
                       'content_pillars']
        
        for field in array_fields:
            if field in strategy_data:
                strategy_data[field] = parse_array(strategy_data[field])
        
        # Parse JSON fields
        json_fields = ['business_objectives', 'target_metrics', 'performance_metrics', 
                      'competitive_position', 'ai_recommendations']
        for field in json_fields:
            if field in strategy_data:
                strategy_data[field] = parse_json(strategy_data[field])
        
        # Create strategy
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        result = await enhanced_service.create_enhanced_strategy(strategy_data, db)
        
        logger.info(f"Enhanced strategy created successfully: {result.get('strategy_id')}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['strategy_created'],
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating enhanced strategy: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "create_enhanced_strategy")

@router.get("/")
async def get_enhanced_strategies(
    user_id: Optional[int] = Query(None, description="User ID to filter strategies"),
    strategy_id: Optional[int] = Query(None, description="Specific strategy ID"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get enhanced content strategies."""
    try:
        logger.info(f"Getting enhanced strategies for user: {user_id}, strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        strategies_data = await enhanced_service.get_enhanced_strategies(user_id, strategy_id, db)
        
        logger.info(f"Retrieved {strategies_data.get('total_count', 0)} strategies")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['strategies_retrieved'],
            data=strategies_data
        )
        
    except Exception as e:
        logger.error(f"Error getting enhanced strategies: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategies")

@router.get("/{strategy_id}")
async def get_enhanced_strategy_by_id(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get a specific enhanced strategy by ID."""
    try:
        logger.info(f"Getting enhanced strategy by ID: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        strategies_data = await enhanced_service.get_enhanced_strategies(strategy_id=strategy_id, db=db)
        
        if strategies_data.get("status") == "not_found" or not strategies_data.get("strategies"):
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        strategy = strategies_data["strategies"][0]
        
        logger.info(f"Retrieved strategy: {strategy.get('name')}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['strategy_retrieved'],
            data=strategy
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting enhanced strategy by ID: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_by_id")

@router.put("/{strategy_id}")
async def update_enhanced_strategy(
    strategy_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update an enhanced strategy."""
    try:
        logger.info(f"Updating enhanced strategy: {strategy_id}")
        
        # Check if strategy exists
        existing_strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not existing_strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        # Update strategy fields
        for field, value in update_data.items():
            if hasattr(existing_strategy, field):
                setattr(existing_strategy, field, value)
        
        existing_strategy.updated_at = datetime.utcnow()
        
        # Save to database
        db.commit()
        db.refresh(existing_strategy)
        
        logger.info(f"Enhanced strategy updated successfully: {strategy_id}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['strategy_updated'],
            data=existing_strategy.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating enhanced strategy: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "update_enhanced_strategy")

@router.delete("/{strategy_id}")
async def delete_enhanced_strategy(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete an enhanced strategy."""
    try:
        logger.info(f"Deleting enhanced strategy: {strategy_id}")
        
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        # Delete strategy
        db.delete(strategy)
        db.commit()
        
        logger.info(f"Enhanced strategy deleted successfully: {strategy_id}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['strategy_deleted'],
            data={"strategy_id": strategy_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting enhanced strategy: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "delete_enhanced_strategy") 