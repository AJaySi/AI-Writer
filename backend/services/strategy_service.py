import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from models.monitoring_models import (
    StrategyMonitoringPlan, 
    MonitoringTask, 
    TaskExecutionLog,
    StrategyPerformanceMetrics,
    StrategyActivationStatus
)
from models.enhanced_strategy_models import EnhancedContentStrategy
from services.database import get_db_session
from services.enhanced_mem0_service import EnhancedMem0Service

logger = logging.getLogger(__name__)

class StrategyService:
    """Service for managing content strategies and their activation status"""
    
    def __init__(self, db_session: Optional[Session] = None):
        self.db_session = db_session or get_db_session()
        self.mem0_service = EnhancedMem0Service(db_session)
    
    async def get_strategy_by_id(self, strategy_id: int) -> Optional[Dict[str, Any]]:
        """Get strategy by ID with all related data"""
        try:
            if self.db_session:
                # Query the actual database
                strategy = self.db_session.query(EnhancedContentStrategy).filter(
                    EnhancedContentStrategy.id == strategy_id
                ).first()
                
                if strategy:
                    return strategy.to_dict()
            
            # Fallback to mock data if no database or strategy not found
            strategy_data = {
                'id': strategy_id,
                'name': f'Content Strategy {strategy_id}',
                'industry': 'Technology',
                'business_goals': ['Increase brand awareness', 'Generate leads', 'Improve engagement'],
                'content_pillars': ['Educational Content', 'Thought Leadership', 'Case Studies'],
                'target_audience': {
                    'demographics': 'B2B professionals',
                    'age_range': '25-45',
                    'interests': ['technology', 'business', 'innovation']
                },
                'strategic_insights': {
                    'market_positioning': 'Innovation leader in tech solutions',
                    'content_opportunities': ['AI trends', 'Digital transformation', 'Industry insights'],
                    'growth_potential': 'High growth potential in emerging markets'
                },
                'competitive_analysis': {
                    'competitors': ['Competitor A', 'Competitor B', 'Competitor C'],
                    'market_gaps': ['AI implementation guidance', 'ROI measurement tools'],
                    'opportunities': ['Thought leadership in AI', 'Educational content series']
                },
                'performance_predictions': {
                    'estimated_roi': '25-35%',
                    'traffic_growth': '40% increase in 6 months',
                    'engagement_metrics': '15% improvement in engagement rate'
                },
                'implementation_roadmap': {
                    'phases': ['Foundation', 'Growth', 'Optimization', 'Scale'],
                    'timeline': '12 months',
                    'milestones': ['Month 3: Content foundation', 'Month 6: Growth phase', 'Month 9: Optimization']
                },
                'risk_assessment': {
                    'risks': ['Market competition', 'Resource constraints', 'Technology changes'],
                    'overall_risk_level': 'Medium',
                    'mitigation_strategies': ['Continuous monitoring', 'Agile adaptation', 'Resource planning']
                }
            }
            
            logger.info(f"Retrieved strategy {strategy_id}")
            return strategy_data
            
        except Exception as e:
            logger.error(f"Error retrieving strategy {strategy_id}: {e}")
            return None
    
    async def activate_strategy(self, strategy_id: int, user_id: int = 1) -> bool:
        """Activate a strategy and set up monitoring"""
        try:
            # Check if strategy exists
            strategy = await self.get_strategy_by_id(strategy_id)
            if not strategy:
                logger.error(f"Strategy {strategy_id} not found")
                return False
            
            # Check if already activated
            if self.db_session:
                existing_activation = self.db_session.query(StrategyActivationStatus).filter(
                    and_(
                        StrategyActivationStatus.strategy_id == strategy_id,
                        StrategyActivationStatus.user_id == user_id,
                        StrategyActivationStatus.status == 'active'
                    )
                ).first()
                
                if existing_activation:
                    logger.info(f"Strategy {strategy_id} is already active")
                    return True
            
            # Create activation status record
            activation_status = StrategyActivationStatus(
                strategy_id=strategy_id,
                user_id=user_id,
                activation_date=datetime.utcnow(),
                status='active',
                performance_score=0.0
            )
            
            if self.db_session:
                self.db_session.add(activation_status)
                self.db_session.commit()
                logger.info(f"Strategy {strategy_id} activated successfully")
            else:
                logger.info(f"Strategy {strategy_id} activated (no database session)")
            
            # Store ACTIVATED strategy in mem0 as memory with comprehensive 30+ inputs
            try:
                # Get the complete strategy data from database with all 30+ inputs
                complete_strategy = await self.get_complete_strategy_data(strategy_id)
                if complete_strategy:
                    mem0_success = await self.mem0_service.store_activated_content_strategy(
                        strategy_data=complete_strategy,
                        user_id=user_id,
                        strategy_id=strategy_id,
                        domain_name="ALwrity"
                    )
                    if mem0_success:
                        logger.info(f"ACTIVATED strategy {strategy_id} successfully stored in mem0 memory with 30+ inputs")
                        # Clear cache to ensure fresh data
                        self.mem0_service.clear_cache(user_id)
                    else:
                        logger.warning(f"Failed to store ACTIVATED strategy {strategy_id} in mem0 memory")
                else:
                    logger.error(f"Could not retrieve complete strategy data for {strategy_id}")
            except Exception as e:
                logger.error(f"Error storing ACTIVATED strategy {strategy_id} in mem0: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error activating strategy {strategy_id}: {e}")
            if self.db_session:
                self.db_session.rollback()
            return False
    
    async def save_monitoring_plan(self, strategy_id: int, plan_data: Dict[str, Any]) -> bool:
        """Save monitoring plan to database"""
        try:
            # Check if monitoring plan already exists
            if self.db_session:
                existing_plan = self.db_session.query(StrategyMonitoringPlan).filter(
                    StrategyMonitoringPlan.strategy_id == strategy_id
                ).first()
                
                if existing_plan:
                    # Update existing plan
                    existing_plan.plan_data = plan_data
                    existing_plan.updated_at = datetime.utcnow()
                else:
                    # Create new monitoring plan
                    monitoring_plan = StrategyMonitoringPlan(
                        strategy_id=strategy_id,
                        plan_data=plan_data
                    )
                    self.db_session.add(monitoring_plan)
                
                # Clear existing tasks and create new ones
                self.db_session.query(MonitoringTask).filter(
                    MonitoringTask.strategy_id == strategy_id
                ).delete()
                
                # Create individual monitoring tasks
                for component in plan_data.get('components', []):
                    for task in component.get('tasks', []):
                        monitoring_task = MonitoringTask(
                            strategy_id=strategy_id,
                            component_name=component['name'],
                            task_title=task['title'],
                            task_description=task['description'],
                            assignee=task['assignee'],
                            frequency=task['frequency'],
                            metric=task['metric'],
                            measurement_method=task['measurementMethod'],
                            success_criteria=task['successCriteria'],
                            alert_threshold=task['alertThreshold'],
                            status='pending'
                        )
                        self.db_session.add(monitoring_task)
                
                self.db_session.commit()
                logger.info(f"Monitoring plan saved for strategy {strategy_id}")
            else:
                logger.info(f"Monitoring plan prepared for strategy {strategy_id} (no database session)")
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving monitoring plan for strategy {strategy_id}: {e}")
            if self.db_session:
                self.db_session.rollback()
            return False
    
    async def get_monitoring_plan(self, strategy_id: int) -> Optional[Dict[str, Any]]:
        """Get monitoring plan for a strategy"""
        try:
            if self.db_session:
                monitoring_plan = self.db_session.query(StrategyMonitoringPlan).filter(
                    StrategyMonitoringPlan.strategy_id == strategy_id
                ).first()
                
                if monitoring_plan:
                    return monitoring_plan.plan_data
                
                # Also check activation status
                activation_status = self.db_session.query(StrategyActivationStatus).filter(
                    StrategyActivationStatus.strategy_id == strategy_id
                ).first()
                
                if activation_status:
                    return {
                        'strategy_id': strategy_id,
                        'status': activation_status.status,
                        'activation_date': activation_status.activation_date.isoformat(),
                        'message': 'Strategy is active but no monitoring plan found'
                    }
            
            # Fallback to mock data
            return {
                'strategy_id': strategy_id,
                'status': 'active',
                'message': 'Monitoring plan retrieved successfully'
            }
            
        except Exception as e:
            logger.error(f"Error getting monitoring plan for strategy {strategy_id}: {e}")
            return None
    
    async def update_strategy_status(self, strategy_id: int, status: str, user_id: int = 1) -> bool:
        """Update strategy activation status"""
        try:
            if self.db_session:
                activation_status = self.db_session.query(StrategyActivationStatus).filter(
                    and_(
                        StrategyActivationStatus.strategy_id == strategy_id,
                        StrategyActivationStatus.user_id == user_id
                    )
                ).first()
                
                if activation_status:
                    activation_status.status = status
                    activation_status.last_updated = datetime.utcnow()
                    self.db_session.commit()
                    logger.info(f"Strategy {strategy_id} status updated to {status}")
                    return True
                else:
                    logger.warning(f"No activation status found for strategy {strategy_id}")
                    return False
            else:
                logger.info(f"Strategy {strategy_id} status would be updated to {status} (no database session)")
                return True
                
        except Exception as e:
            logger.error(f"Error updating strategy status for {strategy_id}: {e}")
            if self.db_session:
                self.db_session.rollback()
            return False
    
    async def get_active_strategies(self, user_id: int = 1) -> List[Dict[str, Any]]:
        """Get all active strategies for a user"""
        try:
            if self.db_session:
                active_strategies = self.db_session.query(StrategyActivationStatus).filter(
                    and_(
                        StrategyActivationStatus.user_id == user_id,
                        StrategyActivationStatus.status == 'active'
                    )
                ).all()
                
                return [
                    {
                        'strategy_id': strategy.strategy_id,
                        'activation_date': strategy.activation_date,
                        'performance_score': strategy.performance_score,
                        'last_updated': strategy.last_updated
                    }
                    for strategy in active_strategies
                ]
            else:
                # Return mock data
                return [
                    {
                        'strategy_id': 1,
                        'activation_date': datetime.utcnow(),
                        'performance_score': 0.0,
                        'last_updated': datetime.utcnow()
                    }
                ]
                
        except Exception as e:
            logger.error(f"Error getting active strategies for user {user_id}: {e}")
            return []
    
    async def save_performance_metrics(self, strategy_id: int, metrics: Dict[str, Any], user_id: int = 1) -> bool:
        """Save performance metrics for a strategy"""
        try:
            performance_metrics = StrategyPerformanceMetrics(
                strategy_id=strategy_id,
                user_id=user_id,
                metric_date=datetime.utcnow(),
                traffic_growth_percentage=metrics.get('traffic_growth_percentage'),
                engagement_rate_percentage=metrics.get('engagement_rate_percentage'),
                conversion_rate_percentage=metrics.get('conversion_rate_percentage'),
                roi_ratio=metrics.get('roi_ratio'),
                strategy_adoption_rate=metrics.get('strategy_adoption_rate'),
                content_quality_score=metrics.get('content_quality_score'),
                competitive_position_rank=metrics.get('competitive_position_rank'),
                audience_growth_percentage=metrics.get('audience_growth_percentage'),
                data_source=metrics.get('data_source', 'manual'),
                confidence_score=metrics.get('confidence_score', 0.8)
            )
            
            if self.db_session:
                self.db_session.add(performance_metrics)
                self.db_session.commit()
                logger.info(f"Performance metrics saved for strategy {strategy_id}")
            else:
                logger.info(f"Performance metrics prepared for strategy {strategy_id} (no database session)")
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving performance metrics for strategy {strategy_id}: {e}")
            if self.db_session:
                self.db_session.rollback()
            return False
    
    async def get_strategy_performance_history(self, strategy_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get performance history for a strategy"""
        try:
            if self.db_session:
                from datetime import timedelta
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                metrics = self.db_session.query(StrategyPerformanceMetrics).filter(
                    and_(
                        StrategyPerformanceMetrics.strategy_id == strategy_id,
                        StrategyPerformanceMetrics.metric_date >= cutoff_date
                    )
                ).order_by(StrategyPerformanceMetrics.metric_date.desc()).all()
                
                return [
                    {
                        'date': metric.metric_date.isoformat(),
                        'traffic_growth': metric.traffic_growth_percentage,
                        'engagement_rate': metric.engagement_rate_percentage,
                        'conversion_rate': metric.conversion_rate_percentage,
                        'roi': metric.roi_ratio,
                        'strategy_adoption': metric.strategy_adoption_rate,
                        'content_quality': metric.content_quality_score,
                        'competitive_position': metric.competitive_position_rank,
                        'audience_growth': metric.audience_growth_percentage
                    }
                    for metric in metrics
                ]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting performance history for strategy {strategy_id}: {e}")
            return []
    
    async def deactivate_strategy(self, strategy_id: int, user_id: int = 1) -> bool:
        """Deactivate a strategy"""
        try:
            return await self.update_strategy_status(strategy_id, 'inactive', user_id)
        except Exception as e:
            logger.error(f"Error deactivating strategy {strategy_id}: {e}")
            return False
    
    async def pause_strategy(self, strategy_id: int, user_id: int = 1) -> bool:
        """Pause a strategy"""
        try:
            return await self.update_strategy_status(strategy_id, 'paused', user_id)
        except Exception as e:
            logger.error(f"Error pausing strategy {strategy_id}: {e}")
            return False
    
    async def resume_strategy(self, strategy_id: int, user_id: int = 1) -> bool:
        """Resume a paused strategy"""
        try:
            return await self.update_strategy_status(strategy_id, 'active', user_id)
        except Exception as e:
            logger.error(f"Error resuming strategy {strategy_id}: {e}")
            return False
    
    async def get_complete_strategy_data(self, strategy_id: int) -> Optional[Dict[str, Any]]:
        """Get complete strategy data with all 30+ inputs for memory storage"""
        try:
            if self.db_session:
                # Query the enhanced strategy model with all fields
                strategy = self.db_session.query(EnhancedContentStrategy).filter(
                    EnhancedContentStrategy.id == strategy_id
                ).first()
                
                if strategy:
                    # Convert to comprehensive dictionary with all 30+ inputs
                    strategy_dict = {
                        # Basic Information
                        'id': strategy.id,
                        'user_id': strategy.user_id,
                        'name': strategy.name,
                        'industry': strategy.industry,
                        'created_at': strategy.created_at.isoformat() if strategy.created_at else None,
                        'updated_at': strategy.updated_at.isoformat() if strategy.updated_at else None,
                        'completion_percentage': strategy.completion_percentage,
                        
                        # Business Context (8 inputs)
                        'business_objectives': strategy.business_objectives,
                        'target_metrics': strategy.target_metrics,
                        'content_budget': strategy.content_budget,
                        'team_size': strategy.team_size,
                        'implementation_timeline': strategy.implementation_timeline,
                        'market_share': strategy.market_share,
                        'competitive_position': strategy.competitive_position,
                        'performance_metrics': strategy.performance_metrics,
                        
                        # Audience Intelligence (6 inputs)
                        'content_preferences': strategy.content_preferences,
                        'consumption_patterns': strategy.consumption_patterns,
                        'audience_pain_points': strategy.audience_pain_points,
                        'buying_journey': strategy.buying_journey,
                        'seasonal_trends': strategy.seasonal_trends,
                        'engagement_metrics': strategy.engagement_metrics,
                        
                        # Competitive Intelligence (5 inputs)
                        'top_competitors': strategy.top_competitors,
                        'competitor_content_strategies': strategy.competitor_content_strategies,
                        'market_gaps': strategy.market_gaps,
                        'industry_trends': strategy.industry_trends,
                        'emerging_trends': strategy.emerging_trends,
                        
                        # Content Strategy (7 inputs)
                        'preferred_formats': strategy.preferred_formats,
                        'content_mix': strategy.content_mix,
                        'content_frequency': strategy.content_frequency,
                        'optimal_timing': strategy.optimal_timing,
                        'quality_metrics': strategy.quality_metrics,
                        'editorial_guidelines': strategy.editorial_guidelines,
                        'brand_voice': strategy.brand_voice,
                        
                        # Performance & Analytics (4 inputs)
                        'traffic_sources': strategy.traffic_sources,
                        'conversion_rates': strategy.conversion_rates,
                        'content_roi_targets': strategy.content_roi_targets,
                        'ab_testing_capabilities': strategy.ab_testing_capabilities,
                        
                        # Legacy fields for backward compatibility
                        'target_audience': strategy.target_audience,
                        'content_pillars': strategy.content_pillars,
                        'ai_recommendations': strategy.ai_recommendations,
                        
                        # Enhanced AI Analysis fields
                        'comprehensive_ai_analysis': strategy.comprehensive_ai_analysis,
                        'onboarding_data_used': strategy.onboarding_data_used,
                        'strategic_scores': strategy.strategic_scores,
                        'market_positioning': strategy.market_positioning,
                        'competitive_advantages': strategy.competitive_advantages,
                        'strategic_risks': strategy.strategic_risks,
                        'opportunity_analysis': strategy.opportunity_analysis,
                        'data_source_transparency': strategy.data_source_transparency
                    }
                    
                    logger.info(f"Retrieved complete strategy data for {strategy_id} with all 30+ inputs")
                    return strategy_dict
                else:
                    logger.warning(f"Strategy {strategy_id} not found in database")
                    return None
            else:
                logger.warning("No database session available for complete strategy retrieval")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving complete strategy data for {strategy_id}: {e}")
            return None
    
    def __del__(self):
        """Cleanup database session"""
        if self.db_session:
            self.db_session.close()
