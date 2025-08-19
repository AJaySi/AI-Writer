"""
Quality Analysis API Routes
Provides endpoints for AI-powered quality assessment and recommendations.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from services.ai_quality_analysis_service import AIQualityAnalysisService, QualityAnalysisResult
from services.database import get_db
from models.enhanced_strategy_models import EnhancedContentStrategy

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quality-analysis", tags=["quality-analysis"])

@router.post("/{strategy_id}/analyze")
async def analyze_strategy_quality(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Analyze strategy quality using AI and return comprehensive results."""
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )
        
        # Initialize quality analysis service
        quality_service = AIQualityAnalysisService()
        
        # Perform quality analysis
        analysis_result = await quality_service.analyze_strategy_quality(strategy_id)
        
        # Convert result to dictionary for API response
        result_dict = {
            "strategy_id": analysis_result.strategy_id,
            "overall_score": analysis_result.overall_score,
            "overall_status": analysis_result.overall_status.value,
            "confidence_score": analysis_result.confidence_score,
            "analysis_timestamp": analysis_result.analysis_timestamp.isoformat(),
            "metrics": [
                {
                    "name": metric.name,
                    "score": metric.score,
                    "weight": metric.weight,
                    "status": metric.status.value,
                    "description": metric.description,
                    "recommendations": metric.recommendations
                }
                for metric in analysis_result.metrics
            ],
            "recommendations": analysis_result.recommendations
        }
        
        logger.info(f"Quality analysis completed for strategy {strategy_id}")
        
        return {
            "success": True,
            "data": result_dict,
            "message": "Quality analysis completed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing strategy quality for {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze strategy quality: {str(e)}"
        )

@router.get("/{strategy_id}/metrics")
async def get_quality_metrics(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get quality metrics for a strategy."""
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )
        
        # Initialize quality analysis service
        quality_service = AIQualityAnalysisService()
        
        # Perform quick quality analysis (cached if available)
        analysis_result = await quality_service.analyze_strategy_quality(strategy_id)
        
        # Return metrics in a simplified format
        metrics_data = [
            {
                "name": metric.name,
                "score": metric.score,
                "status": metric.status.value,
                "description": metric.description
            }
            for metric in analysis_result.metrics
        ]
        
        return {
            "success": True,
            "data": {
                "strategy_id": strategy_id,
                "overall_score": analysis_result.overall_score,
                "overall_status": analysis_result.overall_status.value,
                "metrics": metrics_data,
                "last_updated": analysis_result.analysis_timestamp.isoformat()
            },
            "message": "Quality metrics retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quality metrics for {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get quality metrics: {str(e)}"
        )

@router.get("/{strategy_id}/recommendations")
async def get_quality_recommendations(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get AI-powered quality improvement recommendations."""
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )
        
        # Initialize quality analysis service
        quality_service = AIQualityAnalysisService()
        
        # Perform quality analysis to get recommendations
        analysis_result = await quality_service.analyze_strategy_quality(strategy_id)
        
        # Get recommendations by category
        recommendations_by_category = {}
        for metric in analysis_result.metrics:
            if metric.recommendations:
                recommendations_by_category[metric.name] = metric.recommendations
        
        return {
            "success": True,
            "data": {
                "strategy_id": strategy_id,
                "overall_recommendations": analysis_result.recommendations,
                "recommendations_by_category": recommendations_by_category,
                "priority_areas": [
                    metric.name for metric in analysis_result.metrics 
                    if metric.status.value in ["needs_attention", "poor"]
                ],
                "last_updated": analysis_result.analysis_timestamp.isoformat()
            },
            "message": "Quality recommendations retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quality recommendations for {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get quality recommendations: {str(e)}"
        )

@router.get("/{strategy_id}/history")
async def get_quality_history(
    strategy_id: int,
    days: int = Query(30, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """Get quality analysis history for a strategy."""
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )
        
        # Initialize quality analysis service
        quality_service = AIQualityAnalysisService()
        
        # Get quality history
        history = await quality_service.get_quality_history(strategy_id, days)
        
        # Convert history to API format
        history_data = [
            {
                "timestamp": result.analysis_timestamp.isoformat(),
                "overall_score": result.overall_score,
                "overall_status": result.overall_status.value,
                "confidence_score": result.confidence_score
            }
            for result in history
        ]
        
        return {
            "success": True,
            "data": {
                "strategy_id": strategy_id,
                "history": history_data,
                "days": days,
                "total_analyses": len(history_data)
            },
            "message": "Quality history retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quality history for {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get quality history: {str(e)}"
        )

@router.get("/{strategy_id}/trends")
async def get_quality_trends(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get quality trends and patterns for a strategy."""
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )
        
        # Initialize quality analysis service
        quality_service = AIQualityAnalysisService()
        
        # Get quality trends
        trends = await quality_service.get_quality_trends(strategy_id)
        
        return {
            "success": True,
            "data": {
                "strategy_id": strategy_id,
                "trends": trends,
                "last_updated": datetime.utcnow().isoformat()
            },
            "message": "Quality trends retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quality trends for {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get quality trends: {str(e)}"
        )

@router.post("/{strategy_id}/quick-assessment")
async def quick_quality_assessment(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Perform a quick quality assessment without full AI analysis."""
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )
        
        # Perform quick assessment based on data completeness
        completeness_score = self._calculate_completeness_score(strategy)
        
        # Determine status based on score
        if completeness_score >= 80:
            status = "excellent"
        elif completeness_score >= 65:
            status = "good"
        elif completeness_score >= 45:
            status = "needs_attention"
        else:
            status = "poor"
        
        return {
            "success": True,
            "data": {
                "strategy_id": strategy_id,
                "completeness_score": completeness_score,
                "status": status,
                "assessment_type": "quick",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Quick assessment completed based on data completeness"
            },
            "message": "Quick quality assessment completed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing quick assessment for {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to perform quick assessment: {str(e)}"
        )

def _calculate_completeness_score(self, strategy: EnhancedContentStrategy) -> float:
    """Calculate completeness score based on filled fields."""
    try:
        # Define required fields for each category
        required_fields = {
            "business_context": [
                'business_objectives', 'target_metrics', 'content_budget',
                'team_size', 'implementation_timeline', 'market_share'
            ],
            "audience_intelligence": [
                'content_preferences', 'consumption_patterns', 'audience_pain_points',
                'buying_journey', 'seasonal_trends', 'engagement_metrics'
            ],
            "competitive_intelligence": [
                'top_competitors', 'competitor_content_strategies', 'market_gaps',
                'industry_trends', 'emerging_trends'
            ],
            "content_strategy": [
                'preferred_formats', 'content_mix', 'content_frequency',
                'optimal_timing', 'quality_metrics', 'editorial_guidelines', 'brand_voice'
            ],
            "performance_analytics": [
                'traffic_sources', 'conversion_rates', 'content_roi_targets',
                'ab_testing_capabilities'
            ]
        }
        
        total_fields = 0
        filled_fields = 0
        
        for category, fields in required_fields.items():
            total_fields += len(fields)
            for field in fields:
                if hasattr(strategy, field) and getattr(strategy, field) is not None:
                    filled_fields += 1
        
        if total_fields == 0:
            return 0.0
        
        return (filled_fields / total_fields) * 100
        
    except Exception as e:
        logger.error(f"Error calculating completeness score: {e}")
        return 0.0

@router.get("/{strategy_id}/dashboard")
async def get_quality_dashboard(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get comprehensive quality dashboard data."""
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )
        
        # Initialize quality analysis service
        quality_service = AIQualityAnalysisService()
        
        # Get comprehensive analysis
        analysis_result = await quality_service.analyze_strategy_quality(strategy_id)
        
        # Get trends
        trends = await quality_service.get_quality_trends(strategy_id)
        
        # Prepare dashboard data
        dashboard_data = {
            "strategy_id": strategy_id,
            "overall_score": analysis_result.overall_score,
            "overall_status": analysis_result.overall_status.value,
            "confidence_score": analysis_result.confidence_score,
            "metrics": [
                {
                    "name": metric.name,
                    "score": metric.score,
                    "status": metric.status.value,
                    "description": metric.description,
                    "recommendations": metric.recommendations
                }
                for metric in analysis_result.metrics
            ],
            "recommendations": analysis_result.recommendations,
            "trends": trends,
            "priority_areas": [
                metric.name for metric in analysis_result.metrics 
                if metric.status.value in ["needs_attention", "poor"]
            ],
            "strengths": [
                metric.name for metric in analysis_result.metrics 
                if metric.status.value == "excellent"
            ],
            "last_updated": analysis_result.analysis_timestamp.isoformat()
        }
        
        return {
            "success": True,
            "data": dashboard_data,
            "message": "Quality dashboard data retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quality dashboard for {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get quality dashboard: {str(e)}"
        )
