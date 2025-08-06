"""
Enhanced Strategy Service - Core Module
Main orchestration service for content strategy operations.
"""

import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from sqlalchemy.orm import Session

# Import database models
from models.enhanced_strategy_models import EnhancedContentStrategy, EnhancedAIAnalysisResult

# Import modular services
from ..ai_analysis.ai_recommendations import AIRecommendationsService
from ..ai_analysis.prompt_engineering import PromptEngineeringService
from ..ai_analysis.quality_validation import QualityValidationService

# Import onboarding services
from ..onboarding.data_integration import OnboardingDataIntegrationService
from ..onboarding.field_transformation import FieldTransformationService
from ..onboarding.data_quality import DataQualityService

# Import performance services
from ..performance.caching import CachingService
from ..performance.optimization import PerformanceOptimizationService
from ..performance.health_monitoring import HealthMonitoringService

# Import utils services
from ..utils.data_processors import DataProcessorService
from ..utils.validators import ValidationService

# Import core components
from .field_mappings import STRATEGIC_INPUT_FIELDS
from .constants import SERVICE_CONSTANTS

logger = logging.getLogger(__name__)

class EnhancedStrategyService:
    """Enhanced content strategy service with modular architecture."""

    def __init__(self):
        # Initialize AI analysis services
        self.ai_recommendations_service = AIRecommendationsService()
        self.prompt_engineering_service = PromptEngineeringService()
        self.quality_validation_service = QualityValidationService()

        # Initialize onboarding services
        self.onboarding_data_service = OnboardingDataIntegrationService()
        self.field_transformation_service = FieldTransformationService()
        self.data_quality_service = DataQualityService()

        # Initialize performance services
        self.caching_service = CachingService()
        self.performance_optimization_service = PerformanceOptimizationService()
        self.health_monitoring_service = HealthMonitoringService()

        # Initialize utils services
        self.data_processor_service = DataProcessorService()
        self.validation_service = ValidationService()

    async def create_enhanced_strategy(self, strategy_data: Dict[str, Any], user_id: int, db: Session) -> EnhancedContentStrategy:
        """Create enhanced content strategy with all integrations."""
        try:
            logger.info(f"Creating enhanced strategy for user: {user_id}")

            # Validate strategy data
            validation_result = self.validation_service.validate_strategy_data(strategy_data)
            if not validation_result['is_valid']:
                logger.error(f"Strategy validation failed: {validation_result['errors']}")
                raise ValueError(f"Invalid strategy data: {'; '.join(validation_result['errors'])}")

            # Process onboarding data
            onboarding_data = await self._process_onboarding_data(user_id, db)
            
            # Transform onboarding data to fields
            field_transformations = self.field_transformation_service.transform_onboarding_data_to_fields(onboarding_data)
            
            # Merge strategy data with onboarding data
            enhanced_strategy_data = self._merge_strategy_with_onboarding(strategy_data, field_transformations)

            # Create strategy object
            strategy = EnhancedContentStrategy(
                user_id=user_id,
                **enhanced_strategy_data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Save to database
            db.add(strategy)
            db.commit()
            db.refresh(strategy)

            # Generate AI recommendations
            await self.ai_recommendations_service.generate_comprehensive_recommendations(strategy, db)

            # Cache strategy data
            await self.caching_service.cache_strategy(strategy.id, strategy.to_dict())

            logger.info(f"Enhanced strategy created successfully: {strategy.id}")
            return strategy

        except Exception as e:
            logger.error(f"Error creating enhanced strategy: {str(e)}")
            db.rollback()
            raise

    async def get_enhanced_strategy(self, strategy_id: int, db: Session) -> Optional[EnhancedContentStrategy]:
        """Get enhanced strategy with cached data."""
        try:
            # Try to get from cache first
            cached_strategy = await self.caching_service.get_cached_strategy(strategy_id)
            if cached_strategy:
                logger.info(f"Retrieved strategy {strategy_id} from cache")
                return cached_strategy

            # Get from database
            strategy = db.query(EnhancedContentStrategy).filter(
                EnhancedContentStrategy.id == strategy_id
            ).first()

            if strategy:
                # Cache the strategy
                await self.caching_service.cache_strategy(strategy_id, strategy.to_dict())

            return strategy

        except Exception as e:
            logger.error(f"Error getting enhanced strategy: {str(e)}")
            return None

    async def update_enhanced_strategy(self, strategy_id: int, update_data: Dict[str, Any], db: Session) -> Optional[EnhancedContentStrategy]:
        """Update enhanced strategy."""
        try:
            strategy = db.query(EnhancedContentStrategy).filter(
                EnhancedContentStrategy.id == strategy_id
            ).first()

            if not strategy:
                return None

            # Validate update data
            validation_result = self.validation_service.validate_strategy_data(update_data)
            if not validation_result['is_valid']:
                logger.error(f"Strategy update validation failed: {validation_result['errors']}")
                raise ValueError(f"Invalid update data: {'; '.join(validation_result['errors'])}")

            # Update strategy fields
            for field, value in update_data.items():
                if hasattr(strategy, field):
                    setattr(strategy, field, value)

            strategy.updated_at = datetime.utcnow()

            # Save to database
            db.commit()
            db.refresh(strategy)

            # Invalidate cache
            await self.caching_service.invalidate_cache('strategy_cache', str(strategy_id))

            # Regenerate AI recommendations if needed
            if self._should_regenerate_ai_recommendations(update_data):
                await self.ai_recommendations_service.generate_comprehensive_recommendations(strategy, db)

            logger.info(f"Enhanced strategy updated successfully: {strategy_id}")
            return strategy

        except Exception as e:
            logger.error(f"Error updating enhanced strategy: {str(e)}")
            db.rollback()
            raise

    async def get_onboarding_data(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Get onboarding data for auto-population."""
        try:
            # Try to get from cache first
            cached_data = await self.caching_service.get_cached_onboarding_data(user_id)
            if cached_data:
                logger.info(f"Retrieved onboarding data for user {user_id} from cache")
                return cached_data

            # Process onboarding data
            onboarding_data = await self._process_onboarding_data(user_id, db)
            
            # Cache the data
            await self.caching_service.cache_onboarding_data(user_id, onboarding_data)

            return onboarding_data

        except Exception as e:
            logger.error(f"Error getting onboarding data: {str(e)}")
            return {}

    async def get_ai_analysis(self, strategy_id: int, analysis_type: str, db: Session) -> Optional[Dict[str, Any]]:
        """Get AI analysis results."""
        try:
            # Try to get from cache first
            cached_analysis = await self.caching_service.get_cached_ai_analysis(strategy_id, analysis_type)
            if cached_analysis:
                logger.info(f"Retrieved AI analysis for strategy {strategy_id} from cache")
                return cached_analysis

            # Get from database
            analysis = db.query(EnhancedAIAnalysisResult).filter(
                EnhancedAIAnalysisResult.strategy_id == strategy_id,
                EnhancedAIAnalysisResult.analysis_type == analysis_type
            ).order_by(EnhancedAIAnalysisResult.created_at.desc()).first()

            if analysis:
                analysis_data = analysis.to_dict()
                # Cache the analysis
                await self.caching_service.cache_ai_analysis(strategy_id, analysis_type, analysis_data)
                return analysis_data

            return None

        except Exception as e:
            logger.error(f"Error getting AI analysis: {str(e)}")
            return None

    async def get_system_health(self, db: Session) -> Dict[str, Any]:
        """Get system health status."""
        try:
            return await self.health_monitoring_service.check_system_health(
                db, 
                self.caching_service, 
                self.ai_recommendations_service
            )
        except Exception as e:
            logger.error(f"Error getting system health: {str(e)}")
            return {
                'overall_status': 'error',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    async def get_performance_report(self) -> Dict[str, Any]:
        """Get performance optimization report."""
        try:
            return await self.performance_optimization_service.get_performance_report()
        except Exception as e:
            logger.error(f"Error getting performance report: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    async def _process_onboarding_data(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Process onboarding data for a user."""
        try:
            # Get integrated onboarding data
            integrated_data = await self.onboarding_data_service.process_onboarding_data(user_id, db)
            
            # Assess data quality
            quality_assessment = self.data_quality_service.assess_onboarding_data_quality(integrated_data)
            
            # Add quality assessment to integrated data
            integrated_data['quality_assessment'] = quality_assessment
            
            return integrated_data

        except Exception as e:
            logger.error(f"Error processing onboarding data: {str(e)}")
            return {}

    def _merge_strategy_with_onboarding(self, strategy_data: Dict[str, Any], field_transformations: Dict[str, Any]) -> Dict[str, Any]:
        """Merge strategy data with onboarding field transformations."""
        try:
            merged_data = strategy_data.copy()
            
            # Add auto-populated fields from onboarding data
            if 'fields' in field_transformations:
                for field_name, field_value in field_transformations['fields'].items():
                    if field_name not in merged_data or not merged_data[field_name]:
                        merged_data[field_name] = field_value
            
            # Add data sources information
            if 'sources' in field_transformations:
                merged_data['data_sources'] = field_transformations['sources']
            
            return merged_data

        except Exception as e:
            logger.error(f"Error merging strategy with onboarding: {str(e)}")
            return strategy_data

    def _should_regenerate_ai_recommendations(self, update_data: Dict[str, Any]) -> bool:
        """Determine if AI recommendations should be regenerated."""
        try:
            # Fields that would trigger AI recommendation regeneration
            ai_trigger_fields = [
                'business_objectives', 'target_metrics', 'content_budget',
                'team_size', 'implementation_timeline', 'market_share',
                'competitive_position', 'content_preferences', 'audience_pain_points',
                'top_competitors', 'industry_trends'
            ]
            
            return any(field in update_data for field in ai_trigger_fields)

        except Exception as e:
            logger.error(f"Error checking if AI recommendations should be regenerated: {str(e)}")
            return False

    def get_strategic_input_fields(self) -> List[Dict[str, Any]]:
        """Get strategic input field definitions."""
        return STRATEGIC_INPUT_FIELDS

    def get_service_constants(self) -> Dict[str, Any]:
        """Get service configuration constants."""
        return SERVICE_CONSTANTS

    async def validate_strategy_data(self, strategy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate strategy data using the validation service."""
        try:
            return self.validation_service.validate_strategy_data(strategy_data)
        except Exception as e:
            logger.error(f"Error validating strategy data: {str(e)}")
            return {
                'is_valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': [],
                'field_validations': {},
                'validation_timestamp': datetime.utcnow().isoformat()
            }

    async def process_data_for_output(self, data: Dict[str, Any], output_format: str = 'json') -> Union[str, Dict[str, Any]]:
        """Process data for different output formats."""
        try:
            return self.data_processor_service.format_data_for_output(data, output_format)
        except Exception as e:
            logger.error(f"Error processing data for output: {str(e)}")
            return str(data)

    async def optimize_strategy_operation(self, operation_name: str, operation_func, *args, **kwargs) -> Dict[str, Any]:
        """Optimize strategy operations with performance monitoring."""
        try:
            return await self.performance_optimization_service.optimize_response_time(
                operation_name, operation_func, *args, **kwargs
            )
        except Exception as e:
            logger.error(f"Error optimizing strategy operation: {str(e)}")
            return {
                'result': None,
                'response_time': 0.0,
                'optimization_suggestions': ['Error occurred during optimization'],
                'performance_status': 'error'
            } 