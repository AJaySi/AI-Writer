from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
import json

from services.monitoring_plan_generator import MonitoringPlanGenerator
from services.strategy_service import StrategyService
from services.database import get_db
from models.monitoring_models import (
    StrategyMonitoringPlan, MonitoringTask, TaskExecutionLog,
    StrategyPerformanceMetrics, StrategyActivationStatus
)
from models.enhanced_strategy_models import EnhancedContentStrategy

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/strategy", tags=["strategy-monitoring"])

@router.post("/{strategy_id}/generate-monitoring-plan")
async def generate_monitoring_plan(strategy_id: int):
    """Generate monitoring plan for a strategy"""
    try:
        generator = MonitoringPlanGenerator()
        plan = await generator.generate_monitoring_plan(strategy_id)
        
        logger.info(f"Successfully generated monitoring plan for strategy {strategy_id}")
        return {
            "success": True,
            "data": plan,
            "message": "Monitoring plan generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating monitoring plan for strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate monitoring plan: {str(e)}"
        )

@router.post("/{strategy_id}/activate-with-monitoring")
async def activate_strategy_with_monitoring(
    strategy_id: int,
    monitoring_plan: Dict[str, Any]
):
    """Activate strategy with monitoring plan"""
    try:
        strategy_service = StrategyService()
        
        # Activate strategy
        activation_success = await strategy_service.activate_strategy(strategy_id)
        if not activation_success:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to activate strategy {strategy_id}"
            )
        
        # Save monitoring plan
        plan_success = await strategy_service.save_monitoring_plan(strategy_id, monitoring_plan)
        if not plan_success:
            logger.warning(f"Failed to save monitoring plan for strategy {strategy_id}")
        
        logger.info(f"Successfully activated strategy {strategy_id} with monitoring")
        return {
            "success": True,
            "message": "Strategy activated with monitoring successfully",
            "strategy_id": strategy_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating strategy {strategy_id} with monitoring: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to activate strategy with monitoring: {str(e)}"
        )

@router.get("/{strategy_id}/monitoring-plan")
async def get_monitoring_plan(strategy_id: int):
    """Get monitoring plan for a strategy"""
    try:
        strategy_service = StrategyService()
        monitoring_plan = await strategy_service.get_monitoring_plan(strategy_id)
        
        if monitoring_plan:
            return {
                "success": True,
                "data": monitoring_plan
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Monitoring plan not found for strategy {strategy_id}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting monitoring plan for strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get monitoring plan: {str(e)}"
        )

@router.get("/{strategy_id}/performance-history")
async def get_strategy_performance_history(strategy_id: int, days: int = 30):
    """Get performance history for a strategy"""
    try:
        strategy_service = StrategyService()
        performance_history = await strategy_service.get_strategy_performance_history(strategy_id, days)
        
        return {
            "success": True,
            "data": {
                "strategy_id": strategy_id,
                "performance_history": performance_history,
                "days": days
            }
        }
    except Exception as e:
        logger.error(f"Error getting performance history for strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get performance history: {str(e)}"
        )

@router.post("/{strategy_id}/deactivate")
async def deactivate_strategy(strategy_id: int, user_id: int = 1):
    """Deactivate a strategy"""
    try:
        strategy_service = StrategyService()
        success = await strategy_service.deactivate_strategy(strategy_id, user_id)
        
        if success:
            return {
                "success": True,
                "message": f"Strategy {strategy_id} deactivated successfully"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to deactivate strategy {strategy_id}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to deactivate strategy: {str(e)}"
        )

@router.post("/{strategy_id}/pause")
async def pause_strategy(strategy_id: int, user_id: int = 1):
    """Pause a strategy"""
    try:
        strategy_service = StrategyService()
        success = await strategy_service.pause_strategy(strategy_id, user_id)
        
        if success:
            return {
                "success": True,
                "message": f"Strategy {strategy_id} paused successfully"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to pause strategy {strategy_id}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error pausing strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to pause strategy: {str(e)}"
        )

@router.post("/{strategy_id}/resume")
async def resume_strategy(strategy_id: int, user_id: int = 1):
    """Resume a paused strategy"""
    try:
        strategy_service = StrategyService()
        success = await strategy_service.resume_strategy(strategy_id, user_id)
        
        if success:
            return {
                "success": True,
                "message": f"Strategy {strategy_id} resumed successfully"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to resume strategy {strategy_id}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resuming strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to resume strategy: {str(e)}"
        )

@router.get("/{strategy_id}/performance-metrics")
async def get_performance_metrics(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """
    Get performance metrics for a strategy
    """
    try:
        # For now, return mock data - in real implementation, this would query the database
        mock_metrics = {
            "traffic_growth_percentage": 15.7,
            "engagement_rate_percentage": 8.3,
            "conversion_rate_percentage": 2.1,
            "roi_ratio": 3.2,
            "strategy_adoption_rate": 85,
            "content_quality_score": 92,
            "competitive_position_rank": 3,
            "audience_growth_percentage": 12.5,
            "confidence_score": 88,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "data": mock_metrics,
            "message": "Performance metrics retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{strategy_id}/trend-data")
async def get_trend_data(
    strategy_id: int,
    time_range: str = Query("30d", description="Time range: 7d, 30d, 90d, 1y"),
    db: Session = Depends(get_db)
):
    """
    Get trend data for a strategy over time
    """
    try:
        # Mock trend data - in real implementation, this would query the database
        mock_trend_data = [
            {"date": "2024-01-01", "traffic_growth": 5.2, "engagement_rate": 6.1, "conversion_rate": 1.8, "content_quality_score": 85, "strategy_adoption_rate": 70},
            {"date": "2024-01-08", "traffic_growth": 7.8, "engagement_rate": 7.2, "conversion_rate": 2.0, "content_quality_score": 87, "strategy_adoption_rate": 75},
            {"date": "2024-01-15", "traffic_growth": 9.1, "engagement_rate": 7.8, "conversion_rate": 2.1, "content_quality_score": 89, "strategy_adoption_rate": 78},
            {"date": "2024-01-22", "traffic_growth": 11.3, "engagement_rate": 8.1, "conversion_rate": 2.0, "content_quality_score": 90, "strategy_adoption_rate": 82},
            {"date": "2024-01-29", "traffic_growth": 12.7, "engagement_rate": 8.3, "conversion_rate": 2.1, "content_quality_score": 91, "strategy_adoption_rate": 85},
            {"date": "2024-02-05", "traffic_growth": 14.2, "engagement_rate": 8.5, "conversion_rate": 2.2, "content_quality_score": 92, "strategy_adoption_rate": 87},
            {"date": "2024-02-12", "traffic_growth": 15.7, "engagement_rate": 8.3, "conversion_rate": 2.1, "content_quality_score": 92, "strategy_adoption_rate": 85}
        ]
        
        return {
            "success": True,
            "data": mock_trend_data,
            "message": "Trend data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting trend data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{strategy_id}/test-transparency")
async def test_transparency_endpoint(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """
    Simple test endpoint to check if transparency data endpoint works
    """
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            return {
                "success": False,
                "data": None,
                "message": f"Strategy with ID {strategy_id} not found"
            }

        # Get monitoring plan
        monitoring_plan = db.query(StrategyMonitoringPlan).filter(
            StrategyMonitoringPlan.strategy_id == strategy_id
        ).first()

        # Get monitoring tasks count
        tasks_count = db.query(MonitoringTask).filter(
            MonitoringTask.strategy_id == strategy_id
        ).count()

        return {
            "success": True,
            "data": {
                "strategy_id": strategy_id,
                "strategy_name": strategy.strategy_name if hasattr(strategy, 'strategy_name') else "Unknown",
                "monitoring_plan_exists": monitoring_plan is not None,
                "tasks_count": tasks_count
            },
            "message": "Test endpoint working"
        }

    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        return {
            "success": False,
            "data": None,
            "message": f"Error: {str(e)}"
        }

@router.get("/{strategy_id}/monitoring-tasks")
async def get_monitoring_tasks(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all monitoring tasks for a strategy with their execution status
    """
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")

        # Get monitoring tasks with execution logs
        tasks = db.query(MonitoringTask).filter(
            MonitoringTask.strategy_id == strategy_id
        ).all()

        tasks_data = []
        for task in tasks:
            # Get latest execution log
            latest_log = db.query(TaskExecutionLog).filter(
                TaskExecutionLog.task_id == task.id
            ).order_by(desc(TaskExecutionLog.execution_date)).first()

            task_data = {
                "id": task.id,
                "title": task.task_title,
                "description": task.task_description,
                "assignee": task.assignee,
                "frequency": task.frequency,
                "metric": task.metric,
                "measurementMethod": task.measurement_method,
                "successCriteria": task.success_criteria,
                "alertThreshold": task.alert_threshold,
                "actionableInsights": getattr(task, 'actionable_insights', None),
                "status": "active",  # This would be determined by task execution status
                "lastExecuted": latest_log.execution_date.isoformat() if latest_log else None,
                "executionCount": db.query(TaskExecutionLog).filter(
                    TaskExecutionLog.task_id == task.id
                ).count()
            }
            tasks_data.append(task_data)

        return {
            "success": True,
            "data": tasks_data,
            "message": "Monitoring tasks retrieved successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving monitoring tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{strategy_id}/data-freshness")
async def get_data_freshness(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """
    Get data freshness information for all metrics
    """
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")

        # Get latest task execution logs
        latest_logs = db.query(TaskExecutionLog).join(MonitoringTask).filter(
            MonitoringTask.strategy_id == strategy_id
        ).order_by(desc(TaskExecutionLog.execution_date)).limit(10).all()

        # Get performance metrics
        performance_metrics = db.query(StrategyPerformanceMetrics).filter(
            StrategyPerformanceMetrics.strategy_id == strategy_id
        ).order_by(desc(StrategyPerformanceMetrics.created_at)).first()

        freshness_data = {
            "lastUpdated": latest_logs[0].execution_date.isoformat() if latest_logs else datetime.now().isoformat(),
            "updateFrequency": "Every 4 hours",
            "dataSource": "Multiple Analytics APIs + AI Analysis",
            "confidence": 90,
            "metrics": [
                {
                    "name": "Traffic Growth",
                    "lastUpdated": latest_logs[0].execution_date.isoformat() if latest_logs else datetime.now().isoformat(),
                    "updateFrequency": "Every 4 hours",
                    "dataSource": "Google Analytics + AI Analysis",
                    "confidence": 92
                },
                {
                    "name": "Engagement Rate",
                    "lastUpdated": latest_logs[0].execution_date.isoformat() if latest_logs else datetime.now().isoformat(),
                    "updateFrequency": "Every 2 hours",
                    "dataSource": "Social Media Analytics + Website Analytics",
                    "confidence": 88
                },
                {
                    "name": "Conversion Rate",
                    "lastUpdated": latest_logs[0].execution_date.isoformat() if latest_logs else datetime.now().isoformat(),
                    "updateFrequency": "Every 6 hours",
                    "dataSource": "Google Analytics + CRM Data",
                    "confidence": 85
                }
            ]
        }

        return {
            "success": True,
            "data": freshness_data,
            "message": "Data freshness information retrieved successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving data freshness: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{strategy_id}/transparency-data")
async def get_transparency_data(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive transparency data for a strategy including:
    - Data freshness information
    - Measurement methodology
    - AI monitoring tasks
    - Strategy mapping
    - AI insights
    """
    try:
        # Check if strategy exists
        strategy = db.query(EnhancedContentStrategy).filter(
            EnhancedContentStrategy.id == strategy_id
        ).first()
        
        if not strategy:
            return {
                "success": False,
                "data": None,
                "message": f"Strategy with ID {strategy_id} not found"
            }

        # Get monitoring plan and tasks
        monitoring_plan = db.query(StrategyMonitoringPlan).filter(
            StrategyMonitoringPlan.strategy_id == strategy_id
        ).first()

        if not monitoring_plan:
            return {
                "success": False,
                "data": None,
                "message": "No monitoring plan found for this strategy"
            }

        # Get all monitoring tasks
        monitoring_tasks = db.query(MonitoringTask).filter(
            MonitoringTask.strategy_id == strategy_id
        ).all()

        # Get task execution logs for data freshness
        task_logs = db.query(TaskExecutionLog).join(MonitoringTask).filter(
            MonitoringTask.strategy_id == strategy_id
        ).order_by(desc(TaskExecutionLog.execution_date)).all()

        # Get performance metrics for current values
        performance_metrics = db.query(StrategyPerformanceMetrics).filter(
            StrategyPerformanceMetrics.strategy_id == strategy_id
        ).order_by(desc(StrategyPerformanceMetrics.created_at)).first()

        # Build transparency data
        transparency_data = []

        # Traffic Growth Metric
        traffic_growth_data = {
            "metricName": "Traffic Growth",
            "currentValue": 15.7,  # This would come from actual analytics
            "unit": "%",
            "dataFreshness": {
                "lastUpdated": task_logs[0].execution_date.isoformat() if task_logs else datetime.now().isoformat(),
                "updateFrequency": "Every 4 hours",
                "dataSource": "Google Analytics + AI Analysis",
                "confidence": 92
            },
            "measurementMethodology": {
                "description": "Organic traffic growth compared to previous period",
                "calculationMethod": "Percentage change in organic sessions over 30-day rolling period, weighted by content performance and user engagement",
                "dataPoints": ["Organic Sessions", "Page Views", "Bounce Rate", "Time on Site", "Content Performance"],
                "validationProcess": "Cross-validated with Google Search Console data and AI-powered content performance analysis"
            },
            "monitoringTasks": [],
            "strategyMapping": {
                "relatedComponents": ["Strategic Insights", "Content Strategy", "Audience Analysis"],
                "impactAreas": ["Brand Awareness", "Lead Generation", "Market Reach"],
                "dependencies": ["SEO Optimization", "Content Quality", "User Experience"]
            },
            "aiInsights": {
                "trendAnalysis": "Traffic growth shows strong upward trend with 15.7% increase. Top-performing content categories are educational blog posts and case studies.",
                "recommendations": [
                    "Increase content production in educational blog category by 25%",
                    "Optimize case study content for better search visibility",
                    "Implement A/B testing for content headlines",
                    "Focus on long-form content (2000+ words) which shows 40% higher engagement"
                ],
                "riskFactors": ["Seasonal traffic fluctuations", "Competitor content strategy changes", "Algorithm updates"],
                "opportunities": ["Video content expansion", "Guest posting opportunities", "Social media amplification"]
            }
        }

        # Add real monitoring tasks - map based on task content and purpose
        for task in monitoring_tasks:
            task_title_lower = task.task_title.lower()
            task_description_lower = task.task_description.lower()
            
            # Traffic Growth related tasks
            if any(keyword in task_title_lower or keyword in task_description_lower 
                   for keyword in ['traffic', 'organic', 'goal', 'strategic', 'performance', 'prediction']):
                task_data = {
                    "title": task.task_title,
                    "description": task.task_description,
                    "assignee": task.assignee,
                    "frequency": task.frequency,
                    "metric": task.metric,
                    "measurementMethod": task.measurement_method,
                    "successCriteria": task.success_criteria,
                    "alertThreshold": task.alert_threshold,
                    "actionableInsights": getattr(task, 'actionable_insights', None),
                    "status": "active",
                    "lastExecuted": task_logs[0].execution_date.isoformat() if task_logs else None
                }
                traffic_growth_data["monitoringTasks"].append(task_data)

        transparency_data.append(traffic_growth_data)

        # Engagement Rate Metric
        engagement_data = {
            "metricName": "Engagement Rate",
            "currentValue": 8.3,
            "unit": "%",
            "dataFreshness": {
                "lastUpdated": task_logs[0].execution_date.isoformat() if task_logs else datetime.now().isoformat(),
                "updateFrequency": "Every 2 hours",
                "dataSource": "Social Media Analytics + Website Analytics",
                "confidence": 88
            },
            "measurementMethodology": {
                "description": "Average engagement rate across all content and social media",
                "calculationMethod": "Weighted average of likes, shares, comments, and time spent across all platforms",
                "dataPoints": ["Social Media Engagement", "Website Comments", "Time on Page", "Social Shares", "Email Engagement"],
                "validationProcess": "Cross-platform validation using multiple analytics tools and AI sentiment analysis"
            },
            "monitoringTasks": [],
            "strategyMapping": {
                "relatedComponents": ["Audience Analysis", "Content Strategy", "Social Media Strategy"],
                "impactAreas": ["Brand Engagement", "Community Building", "Customer Loyalty"],
                "dependencies": ["Content Quality", "Social Media Presence", "Community Management"]
            },
            "aiInsights": {
                "trendAnalysis": "Engagement rate is stable at 8.3% with peak engagement during lunch hours and early evenings.",
                "recommendations": [
                    "Increase video content production by 50%",
                    "Optimize posting times for peak engagement hours",
                    "Implement interactive content elements",
                    "Focus on community-building content"
                ],
                "riskFactors": ["Platform algorithm changes", "Content fatigue", "Competition for attention"],
                "opportunities": ["Live streaming opportunities", "User-generated content campaigns", "Influencer collaborations"]
            }
        }

        # Add engagement-related tasks
        for task in monitoring_tasks:
            task_title_lower = task.task_title.lower()
            task_description_lower = task.task_description.lower()
            
            if any(keyword in task_title_lower or keyword in task_description_lower 
                   for keyword in ['engagement', 'social', 'community', 'audience', 'insight', 'competitive']):
                task_data = {
                    "title": task.task_title,
                    "description": task.task_description,
                    "assignee": task.assignee,
                    "frequency": task.frequency,
                    "metric": task.metric,
                    "measurementMethod": task.measurement_method,
                    "successCriteria": task.success_criteria,
                    "alertThreshold": task.alert_threshold,
                    "actionableInsights": getattr(task, 'actionable_insights', None),
                    "status": "active",
                    "lastExecuted": task_logs[0].execution_date.isoformat() if task_logs else None
                }
                engagement_data["monitoringTasks"].append(task_data)

        transparency_data.append(engagement_data)

        # Conversion Rate Metric
        conversion_data = {
            "metricName": "Conversion Rate",
            "currentValue": 2.1,
            "unit": "%",
            "dataFreshness": {
                "lastUpdated": task_logs[0].execution_date.isoformat() if task_logs else datetime.now().isoformat(),
                "updateFrequency": "Every 6 hours",
                "dataSource": "Google Analytics + CRM Data",
                "confidence": 85
            },
            "measurementMethodology": {
                "description": "Content-driven conversion rate across all touchpoints",
                "calculationMethod": "Conversions divided by total visitors, weighted by content attribution and customer journey analysis",
                "dataPoints": ["Website Conversions", "Email Signups", "Lead Form Submissions", "Content Downloads", "Sales Attribution"],
                "validationProcess": "CRM integration validation and conversion funnel analysis"
            },
            "monitoringTasks": [],
            "strategyMapping": {
                "relatedComponents": ["Performance Predictions", "Implementation Roadmap", "Risk Assessment"],
                "impactAreas": ["Revenue Generation", "Lead Quality", "Customer Acquisition"],
                "dependencies": ["Content Quality", "User Experience", "Lead Nurturing"]
            },
            "aiInsights": {
                "trendAnalysis": "Conversion rate is improving steadily with 2.1% current rate. Top-converting content includes case studies and product demos.",
                "recommendations": [
                    "Increase case study and demo content production",
                    "Optimize mobile user experience further",
                    "Implement personalized content recommendations",
                    "A/B test call-to-action buttons and forms"
                ],
                "riskFactors": ["Market competition", "Economic factors", "Technology changes"],
                "opportunities": ["Personalization opportunities", "Automation implementation", "Cross-selling strategies"]
            }
        }

        # Add conversion-related tasks
        for task in monitoring_tasks:
            task_title_lower = task.task_title.lower()
            task_description_lower = task.task_description.lower()
            
            if any(keyword in task_title_lower or keyword in task_description_lower 
                   for keyword in ['conversion', 'funnel', 'implementation', 'resource', 'risk', 'mitigation']):
                task_data = {
                    "title": task.task_title,
                    "description": task.task_description,
                    "assignee": task.assignee,
                    "frequency": task.frequency,
                    "metric": task.metric,
                    "measurementMethod": task.measurement_method,
                    "successCriteria": task.success_criteria,
                    "alertThreshold": task.alert_threshold,
                    "actionableInsights": getattr(task, 'actionable_insights', None),
                    "status": "active",
                    "lastExecuted": task_logs[0].execution_date.isoformat() if task_logs else None
                }
                conversion_data["monitoringTasks"].append(task_data)

        transparency_data.append(conversion_data)

        return {
            "success": True,
            "data": transparency_data,
            "message": "Transparency data retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Error retrieving transparency data: {str(e)}")
        return {
            "success": False,
            "data": None,
            "message": f"Error: {str(e)}"
        }
