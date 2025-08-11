"""
Analytics Endpoints
Handles analytics and AI analysis endpoints for enhanced content strategies.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime

# Import database
from services.database import get_db_session

# Import services
from ....services.enhanced_strategy_service import EnhancedStrategyService
from ....services.enhanced_strategy_db_service import EnhancedStrategyDBService

# Import models
from models.enhanced_strategy_models import EnhancedContentStrategy, EnhancedAIAnalysisResult

# Import utilities
from ....utils.error_handlers import ContentPlanningErrorHandler
from ....utils.response_builders import ResponseBuilder
from ....utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

router = APIRouter(tags=["Strategy Analytics"])

# Helper function to get database session
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

@router.get("/{strategy_id}/analytics")
async def get_enhanced_strategy_analytics(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get analytics data for an enhanced strategy."""
    try:
        logger.info(f"Getting analytics for strategy: {strategy_id}")
        
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        # Calculate completion statistics
        strategy.calculate_completion_percentage()
        
        # Get AI analysis results
        ai_analyses = db.query(EnhancedAIAnalysisResult).filter(
            EnhancedAIAnalysisResult.strategy_id == strategy_id
        ).order_by(EnhancedAIAnalysisResult.created_at.desc()).all()
        
        analytics_data = {
            "strategy_id": strategy_id,
            "completion_percentage": strategy.completion_percentage,
            "total_fields": 30,
            "completed_fields": len([f for f in strategy.get_field_values() if f is not None and f != ""]),
            "ai_analyses_count": len(ai_analyses),
            "last_ai_analysis": ai_analyses[0].to_dict() if ai_analyses else None,
            "created_at": strategy.created_at.isoformat() if strategy.created_at else None,
            "updated_at": strategy.updated_at.isoformat() if strategy.updated_at else None
        }
        
        logger.info(f"Retrieved analytics for strategy: {strategy_id}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['analytics_retrieved'],
            data=analytics_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting strategy analytics: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_analytics")

@router.get("/{strategy_id}/ai-analyses")
async def get_enhanced_strategy_ai_analysis(
    strategy_id: int,
    limit: int = Query(10, description="Number of AI analysis results to return"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get AI analysis results for an enhanced strategy."""
    try:
        logger.info(f"Getting AI analyses for strategy: {strategy_id}, limit: {limit}")
        
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        # Get AI analysis results
        ai_analyses = db.query(EnhancedAIAnalysisResult).filter(
            EnhancedAIAnalysisResult.strategy_id == strategy_id
        ).order_by(EnhancedAIAnalysisResult.created_at.desc()).limit(limit).all()
        
        analyses_data = [analysis.to_dict() for analysis in ai_analyses]
        
        logger.info(f"Retrieved {len(analyses_data)} AI analyses for strategy: {strategy_id}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['ai_analyses_retrieved'],
            data={
                "strategy_id": strategy_id,
                "analyses": analyses_data,
                "total_count": len(analyses_data)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting AI analyses: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_ai_analysis")

@router.get("/{strategy_id}/completion")
async def get_enhanced_strategy_completion_stats(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get completion statistics for an enhanced strategy."""
    try:
        logger.info(f"Getting completion stats for strategy: {strategy_id}")
        
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        # Calculate completion statistics
        strategy.calculate_completion_percentage()
        
        # Get field values and categorize them
        field_values = strategy.get_field_values()
        completed_fields = []
        incomplete_fields = []
        
        for field_name, value in field_values.items():
            if value is not None and value != "":
                completed_fields.append(field_name)
            else:
                incomplete_fields.append(field_name)
        
        completion_stats = {
            "strategy_id": strategy_id,
            "completion_percentage": strategy.completion_percentage,
            "total_fields": 30,
            "completed_fields_count": len(completed_fields),
            "incomplete_fields_count": len(incomplete_fields),
            "completed_fields": completed_fields,
            "incomplete_fields": incomplete_fields,
            "last_updated": strategy.updated_at.isoformat() if strategy.updated_at else None
        }
        
        logger.info(f"Retrieved completion stats for strategy: {strategy_id}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['completion_stats_retrieved'],
            data=completion_stats
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting completion stats: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_completion_stats")

@router.get("/{strategy_id}/onboarding-integration")
async def get_enhanced_strategy_onboarding_integration(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get onboarding integration data for an enhanced strategy."""
    try:
        logger.info(f"Getting onboarding integration for strategy: {strategy_id}")
        
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        # Get onboarding integration data
        onboarding_data = strategy.onboarding_data_used if hasattr(strategy, 'onboarding_data_used') else {}
        
        integration_data = {
            "strategy_id": strategy_id,
            "onboarding_integration": onboarding_data,
            "has_onboarding_data": bool(onboarding_data),
            "auto_populated_fields": onboarding_data.get('auto_populated_fields', {}),
            "data_sources": onboarding_data.get('data_sources', []),
            "integration_id": onboarding_data.get('integration_id')
        }
        
        logger.info(f"Retrieved onboarding integration for strategy: {strategy_id}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['onboarding_integration_retrieved'],
            data=integration_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting onboarding integration: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_onboarding_integration")

@router.post("/{strategy_id}/ai-recommendations")
async def generate_enhanced_ai_recommendations(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Generate AI recommendations for an enhanced strategy."""
    try:
        logger.info(f"Generating AI recommendations for strategy: {strategy_id}")
        
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        # Generate AI recommendations
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        # This would call the AI service to generate recommendations
        # For now, we'll return a placeholder
        recommendations = {
            "strategy_id": strategy_id,
            "recommendations": [
                {
                    "type": "content_optimization",
                    "title": "Optimize Content Strategy",
                    "description": "Based on your current strategy, consider focusing on pillar content and topic clusters.",
                    "priority": "high",
                    "estimated_impact": "Increase organic traffic by 25%"
                }
            ],
            "generated_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Generated AI recommendations for strategy: {strategy_id}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['ai_recommendations_generated'],
            data=recommendations
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating AI recommendations: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "generate_enhanced_ai_recommendations")

@router.post("/{strategy_id}/ai-analysis/regenerate")
async def regenerate_enhanced_strategy_ai_analysis(
    strategy_id: int,
    analysis_type: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Regenerate AI analysis for an enhanced strategy."""
    try:
        logger.info(f"Regenerating AI analysis for strategy: {strategy_id}, type: {analysis_type}")
        
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Enhanced strategy with ID {strategy_id} not found"
            )
        
        # Regenerate AI analysis
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        # This would call the AI service to regenerate analysis
        # For now, we'll return a placeholder
        analysis_result = {
            "strategy_id": strategy_id,
            "analysis_type": analysis_type,
            "status": "regenerated",
            "regenerated_at": datetime.utcnow().isoformat(),
            "result": {
                "insights": ["New insight 1", "New insight 2"],
                "recommendations": ["New recommendation 1", "New recommendation 2"]
            }
        }
        
        logger.info(f"Regenerated AI analysis for strategy: {strategy_id}")
        return ResponseBuilder.success_response(
            message=SUCCESS_MESSAGES['ai_analysis_regenerated'],
            data=analysis_result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error regenerating AI analysis: {str(e)}")
        return ContentPlanningErrorHandler.handle_general_error(e, "regenerate_enhanced_strategy_ai_analysis") 