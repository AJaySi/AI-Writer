"""
Enhanced Strategy Database Service
Handles database operations for enhanced content strategy functionality.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# Import database models
from models.enhanced_strategy_models import EnhancedContentStrategy, EnhancedAIAnalysisResult, OnboardingDataIntegration

logger = logging.getLogger(__name__)

class EnhancedStrategyDBService:
    """Database service for enhanced content strategy operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_enhanced_strategy(self, strategy_id: int) -> Optional[EnhancedContentStrategy]:
        """Get an enhanced strategy by ID."""
        try:
            return self.db.query(EnhancedContentStrategy).filter(EnhancedContentStrategy.id == strategy_id).first()
        except Exception as e:
            logger.error(f"Error getting enhanced strategy {strategy_id}: {str(e)}")
            return None
    
    async def get_enhanced_strategies(self, user_id: Optional[int] = None, strategy_id: Optional[int] = None) -> List[EnhancedContentStrategy]:
        """Get enhanced strategies with optional filtering."""
        try:
            query = self.db.query(EnhancedContentStrategy)
            
            if user_id:
                query = query.filter(EnhancedContentStrategy.user_id == user_id)
            
            if strategy_id:
                query = query.filter(EnhancedContentStrategy.id == strategy_id)
            
            return query.all()
        except Exception as e:
            logger.error(f"Error getting enhanced strategies: {str(e)}")
            return []
    
    async def create_enhanced_strategy(self, strategy_data: Dict[str, Any]) -> Optional[EnhancedContentStrategy]:
        """Create a new enhanced strategy."""
        try:
            strategy = EnhancedContentStrategy(**strategy_data)
            self.db.add(strategy)
            self.db.commit()
            self.db.refresh(strategy)
            return strategy
        except Exception as e:
            logger.error(f"Error creating enhanced strategy: {str(e)}")
            self.db.rollback()
            return None
    
    async def update_enhanced_strategy(self, strategy_id: int, update_data: Dict[str, Any]) -> Optional[EnhancedContentStrategy]:
        """Update an enhanced strategy."""
        try:
            strategy = await self.get_enhanced_strategy(strategy_id)
            if not strategy:
                return None
            
            for key, value in update_data.items():
                if hasattr(strategy, key):
                    setattr(strategy, key, value)
            
            strategy.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(strategy)
            return strategy
        except Exception as e:
            logger.error(f"Error updating enhanced strategy {strategy_id}: {str(e)}")
            self.db.rollback()
            return None
    
    async def delete_enhanced_strategy(self, strategy_id: int) -> bool:
        """Delete an enhanced strategy."""
        try:
            strategy = await self.get_enhanced_strategy(strategy_id)
            if not strategy:
                return False
            
            self.db.delete(strategy)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting enhanced strategy {strategy_id}: {str(e)}")
            self.db.rollback()
            return False
    
    async def get_enhanced_strategies_with_analytics(self, strategy_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get enhanced strategies with analytics data."""
        try:
            strategies = await self.get_enhanced_strategies(strategy_id=strategy_id)
            result = []
            
            for strategy in strategies:
                strategy_dict = strategy.to_dict() if hasattr(strategy, 'to_dict') else {
                    'id': strategy.id,
                    'name': strategy.name,
                    'industry': strategy.industry,
                    'user_id': strategy.user_id,
                    'created_at': strategy.created_at.isoformat() if strategy.created_at else None,
                    'updated_at': strategy.updated_at.isoformat() if strategy.updated_at else None
                }
                
                # Add analytics data
                analytics = await self.get_ai_analysis_history(strategy.id, limit=5)
                strategy_dict['analytics'] = analytics
                
                result.append(strategy_dict)
            
            return result
        except Exception as e:
            logger.error(f"Error getting enhanced strategies with analytics: {str(e)}")
            return []
    
    async def get_ai_analysis_history(self, strategy_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get AI analysis history for a strategy."""
        try:
            analyses = self.db.query(EnhancedAIAnalysisResult).filter(
                EnhancedAIAnalysisResult.strategy_id == strategy_id
            ).order_by(EnhancedAIAnalysisResult.created_at.desc()).limit(limit).all()
            
            return [analysis.to_dict() if hasattr(analysis, 'to_dict') else {
                'id': analysis.id,
                'analysis_type': analysis.analysis_type,
                'insights': analysis.insights,
                'recommendations': analysis.recommendations,
                'created_at': analysis.created_at.isoformat() if analysis.created_at else None
            } for analysis in analyses]
        except Exception as e:
            logger.error(f"Error getting AI analysis history for strategy {strategy_id}: {str(e)}")
            return []
    
    async def get_onboarding_integration(self, strategy_id: int) -> Optional[Dict[str, Any]]:
        """Get onboarding integration data for a strategy."""
        try:
            integration = self.db.query(OnboardingDataIntegration).filter(
                OnboardingDataIntegration.strategy_id == strategy_id
            ).first()
            
            if integration:
                return integration.to_dict() if hasattr(integration, 'to_dict') else {
                    'id': integration.id,
                    'strategy_id': integration.strategy_id,
                    'data_sources': integration.data_sources,
                    'confidence_scores': integration.confidence_scores,
                    'created_at': integration.created_at.isoformat() if integration.created_at else None
                }
            return None
        except Exception as e:
            logger.error(f"Error getting onboarding integration for strategy {strategy_id}: {str(e)}")
            return None
    
    async def get_strategy_completion_stats(self, user_id: int) -> Dict[str, Any]:
        """Get completion statistics for all strategies of a user."""
        try:
            strategies = await self.get_enhanced_strategies(user_id=user_id)
            
            total_strategies = len(strategies)
            completed_strategies = sum(1 for s in strategies if s.completion_percentage >= 80)
            avg_completion = sum(s.completion_percentage for s in strategies) / total_strategies if total_strategies > 0 else 0
            
            return {
                'total_strategies': total_strategies,
                'completed_strategies': completed_strategies,
                'avg_completion_percentage': avg_completion,
                'user_id': user_id
            }
        except Exception as e:
            logger.error(f"Error getting strategy completion stats for user {user_id}: {str(e)}")
            return {
                'total_strategies': 0,
                'completed_strategies': 0,
                'avg_completion_percentage': 0,
                'user_id': user_id
            }
    
    async def search_enhanced_strategies(self, user_id: int, search_term: str) -> List[EnhancedContentStrategy]:
        """Search enhanced strategies by name or industry."""
        try:
            return self.db.query(EnhancedContentStrategy).filter(
                and_(
                    EnhancedContentStrategy.user_id == user_id,
                    or_(
                        EnhancedContentStrategy.name.ilike(f"%{search_term}%"),
                        EnhancedContentStrategy.industry.ilike(f"%{search_term}%")
                    )
                )
            ).all()
        except Exception as e:
            logger.error(f"Error searching enhanced strategies: {str(e)}")
            return []
    
    async def get_strategy_export_data(self, strategy_id: int) -> Optional[Dict[str, Any]]:
        """Get comprehensive export data for a strategy."""
        try:
            strategy = await self.get_enhanced_strategy(strategy_id)
            if not strategy:
                return None
            
            # Get strategy data
            strategy_data = strategy.to_dict() if hasattr(strategy, 'to_dict') else {
                'id': strategy.id,
                'name': strategy.name,
                'industry': strategy.industry,
                'user_id': strategy.user_id,
                'created_at': strategy.created_at.isoformat() if strategy.created_at else None,
                'updated_at': strategy.updated_at.isoformat() if strategy.updated_at else None
            }
            
            # Get analytics data
            analytics = await self.get_ai_analysis_history(strategy_id, limit=10)
            
            # Get onboarding integration
            onboarding = await self.get_onboarding_integration(strategy_id)
            
            return {
                'strategy': strategy_data,
                'analytics': analytics,
                'onboarding_integration': onboarding,
                'exported_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting strategy export data for strategy {strategy_id}: {str(e)}")
            return None 