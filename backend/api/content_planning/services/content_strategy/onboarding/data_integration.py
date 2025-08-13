"""
Onboarding Data Integration Service
Onboarding data integration and processing.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import traceback

# Import database models
from models.enhanced_strategy_models import (
    OnboardingDataIntegration
)
from models.onboarding import (
    OnboardingSession,
    WebsiteAnalysis,
    ResearchPreferences,
    APIKey
)

logger = logging.getLogger(__name__)

class OnboardingDataIntegrationService:
    """Service for onboarding data integration and processing."""

    def __init__(self):
        self.data_freshness_threshold = timedelta(hours=24)
        self.max_analysis_age = timedelta(days=7)

    async def process_onboarding_data(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Process and integrate all onboarding data for a user."""
        try:
            logger.info(f"Processing onboarding data for user: {user_id}")

            # Get all onboarding data sources
            website_analysis = self._get_website_analysis(user_id, db)
            research_preferences = self._get_research_preferences(user_id, db)
            api_keys_data = self._get_api_keys_data(user_id, db)
            onboarding_session = self._get_onboarding_session(user_id, db)

            # Log data source status
            logger.info(f"Data source status for user {user_id}:")
            logger.info(f"  - Website analysis: {'✅ Found' if website_analysis else '❌ Missing'}")
            logger.info(f"  - Research preferences: {'✅ Found' if research_preferences else '❌ Missing'}")
            logger.info(f"  - API keys data: {'✅ Found' if api_keys_data else '❌ Missing'}")
            logger.info(f"  - Onboarding session: {'✅ Found' if onboarding_session else '❌ Missing'}")

            # Process and integrate data
            integrated_data = {
                'website_analysis': website_analysis,
                'research_preferences': research_preferences,
                'api_keys_data': api_keys_data,
                'onboarding_session': onboarding_session,
                'data_quality': self._assess_data_quality(website_analysis, research_preferences, api_keys_data),
                'processing_timestamp': datetime.utcnow().isoformat()
            }

            # Log data quality assessment
            data_quality = integrated_data['data_quality']
            logger.info(f"Data quality assessment for user {user_id}:")
            logger.info(f"  - Completeness: {data_quality.get('completeness', 0):.2f}")
            logger.info(f"  - Freshness: {data_quality.get('freshness', 0):.2f}")
            logger.info(f"  - Relevance: {data_quality.get('relevance', 0):.2f}")
            logger.info(f"  - Confidence: {data_quality.get('confidence', 0):.2f}")

            # Store integrated data
            await self._store_integrated_data(user_id, integrated_data, db)

            logger.info(f"Onboarding data processed successfully for user: {user_id}")
            return integrated_data

        except Exception as e:
            logger.error(f"Error processing onboarding data for user {user_id}: {str(e)}")
            logger.error("Traceback:\n%s", traceback.format_exc())
            return self._get_fallback_data()

    def _get_website_analysis(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Get website analysis data for the user."""
        try:
            # Get the latest onboarding session for the user
            session = db.query(OnboardingSession).filter(
                OnboardingSession.user_id == user_id
            ).order_by(OnboardingSession.updated_at.desc()).first()
            
            if not session:
                logger.warning(f"No onboarding session found for user {user_id}")
                return {}
            
            # Get the latest website analysis for this session
            website_analysis = db.query(WebsiteAnalysis).filter(
                WebsiteAnalysis.session_id == session.id
            ).order_by(WebsiteAnalysis.updated_at.desc()).first()
            
            if not website_analysis:
                logger.warning(f"No website analysis found for user {user_id}")
                return {}
            
            # Convert to dictionary and add metadata
            analysis_data = website_analysis.to_dict()
            analysis_data['data_freshness'] = self._calculate_freshness(website_analysis.updated_at)
            analysis_data['confidence_level'] = 0.9 if website_analysis.status == 'completed' else 0.5
            
            logger.info(f"Retrieved website analysis for user {user_id}: {website_analysis.website_url}")
            return analysis_data

        except Exception as e:
            logger.error(f"Error getting website analysis for user {user_id}: {str(e)}")
            return {}

    def _get_research_preferences(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Get research preferences data for the user."""
        try:
            # Get the latest onboarding session for the user
            session = db.query(OnboardingSession).filter(
                OnboardingSession.user_id == user_id
            ).order_by(OnboardingSession.updated_at.desc()).first()
            
            if not session:
                logger.warning(f"No onboarding session found for user {user_id}")
                return {}
            
            # Get research preferences for this session
            research_prefs = db.query(ResearchPreferences).filter(
                ResearchPreferences.session_id == session.id
            ).first()
            
            if not research_prefs:
                logger.warning(f"No research preferences found for user {user_id}")
                return {}
            
            # Convert to dictionary and add metadata
            prefs_data = research_prefs.to_dict()
            prefs_data['data_freshness'] = self._calculate_freshness(research_prefs.updated_at)
            prefs_data['confidence_level'] = 0.9
            
            logger.info(f"Retrieved research preferences for user {user_id}")
            return prefs_data

        except Exception as e:
            logger.error(f"Error getting research preferences for user {user_id}: {str(e)}")
            return {}

    def _get_api_keys_data(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Get API keys data for the user."""
        try:
            # Get the latest onboarding session for the user
            session = db.query(OnboardingSession).filter(
                OnboardingSession.user_id == user_id
            ).order_by(OnboardingSession.updated_at.desc()).first()
            
            if not session:
                logger.warning(f"No onboarding session found for user {user_id}")
                return {}
            
            # Get all API keys for this session
            api_keys = db.query(APIKey).filter(
                APIKey.session_id == session.id
            ).all()
            
            if not api_keys:
                logger.warning(f"No API keys found for user {user_id}")
                return {}
            
            # Convert to dictionary format
            api_data = {
                'api_keys': [key.to_dict() for key in api_keys],
                'total_keys': len(api_keys),
                'providers': [key.provider for key in api_keys],
                'data_freshness': self._calculate_freshness(session.updated_at),
                'confidence_level': 0.8
            }
            
            logger.info(f"Retrieved {len(api_keys)} API keys for user {user_id}")
            return api_data

        except Exception as e:
            logger.error(f"Error getting API keys data for user {user_id}: {str(e)}")
            return {}

    def _get_onboarding_session(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Get onboarding session data for the user."""
        try:
            # Get the latest onboarding session for the user
            session = db.query(OnboardingSession).filter(
                OnboardingSession.user_id == user_id
            ).order_by(OnboardingSession.updated_at.desc()).first()
            
            if not session:
                logger.warning(f"No onboarding session found for user {user_id}")
                return {}
            
            # Convert to dictionary
            session_data = {
                'id': session.id,
                'user_id': session.user_id,
                'current_step': session.current_step,
                'progress': session.progress,
                'started_at': session.started_at.isoformat() if session.started_at else None,
                'updated_at': session.updated_at.isoformat() if session.updated_at else None,
                'data_freshness': self._calculate_freshness(session.updated_at),
                'confidence_level': 0.9
            }
            
            logger.info(f"Retrieved onboarding session for user {user_id}: step {session.current_step}, progress {session.progress}%")
            return session_data

        except Exception as e:
            logger.error(f"Error getting onboarding session for user {user_id}: {str(e)}")
            return {}

    def _assess_data_quality(self, website_analysis: Dict, research_preferences: Dict, api_keys_data: Dict) -> Dict[str, Any]:
        """Assess the quality and completeness of onboarding data."""
        try:
            quality_metrics = {
                'overall_score': 0.0,
                'completeness': 0.0,
                'freshness': 0.0,
                'relevance': 0.0,
                'confidence': 0.0
            }

            # Calculate completeness
            total_fields = 0
            filled_fields = 0

            # Website analysis completeness
            website_fields = ['domain', 'industry', 'business_type', 'target_audience', 'content_goals']
            for field in website_fields:
                total_fields += 1
                if website_analysis.get(field):
                    filled_fields += 1

            # Research preferences completeness
            research_fields = ['research_topics', 'content_types', 'target_audience', 'industry_focus']
            for field in research_fields:
                total_fields += 1
                if research_preferences.get(field):
                    filled_fields += 1

            # API keys completeness
            total_fields += 1
            if api_keys_data:
                filled_fields += 1

            quality_metrics['completeness'] = filled_fields / total_fields if total_fields > 0 else 0.0

            # Calculate freshness
            freshness_scores = []
            for data_source in [website_analysis, research_preferences]:
                if data_source.get('data_freshness'):
                    freshness_scores.append(data_source['data_freshness'])
            
            quality_metrics['freshness'] = sum(freshness_scores) / len(freshness_scores) if freshness_scores else 0.0

            # Calculate relevance (based on data presence and quality)
            relevance_score = 0.0
            if website_analysis.get('domain'):
                relevance_score += 0.4
            if research_preferences.get('research_topics'):
                relevance_score += 0.3
            if api_keys_data:
                relevance_score += 0.3
            
            quality_metrics['relevance'] = relevance_score

            # Calculate confidence
            quality_metrics['confidence'] = (quality_metrics['completeness'] + quality_metrics['freshness'] + quality_metrics['relevance']) / 3

            # Calculate overall score
            quality_metrics['overall_score'] = quality_metrics['confidence']

            return quality_metrics

        except Exception as e:
            logger.error(f"Error assessing data quality: {str(e)}")
            return {
                'overall_score': 0.0,
                'completeness': 0.0,
                'freshness': 0.0,
                'relevance': 0.0,
                'confidence': 0.0
            }

    def _calculate_freshness(self, created_at: datetime) -> float:
        """Calculate data freshness score (0.0 to 1.0)."""
        try:
            age = datetime.utcnow() - created_at
            
            if age <= self.data_freshness_threshold:
                return 1.0
            elif age <= self.max_analysis_age:
                # Linear decay from 1.0 to 0.5
                decay_factor = 1.0 - (age - self.data_freshness_threshold) / (self.max_analysis_age - self.data_freshness_threshold) * 0.5
                return max(0.5, decay_factor)
            else:
                return 0.5  # Minimum freshness for old data
                
        except Exception as e:
            logger.error(f"Error calculating data freshness: {str(e)}")
            return 0.5

    def _check_api_data_availability(self, api_key_data: Dict) -> bool:
        """Check if API key has available data."""
        try:
            # Check if API key has been used recently and has data
            if api_key_data.get('last_used') and api_key_data.get('usage_count', 0) > 0:
                return api_key_data.get('data_available', False)
            return False
            
        except Exception as e:
            logger.error(f"Error checking API data availability: {str(e)}")
            return False

    async def _store_integrated_data(self, user_id: int, integrated_data: Dict[str, Any], db: Session) -> None:
        """Store integrated onboarding data."""
        try:
            # Create or update integrated data record
            existing_record = db.query(OnboardingDataIntegration).filter(
                OnboardingDataIntegration.user_id == user_id
            ).first()

            if existing_record:
                # Use legacy columns that are known to exist
                if hasattr(existing_record, 'website_analysis_data'):
                    existing_record.website_analysis_data = integrated_data.get('website_analysis', {})
                if hasattr(existing_record, 'research_preferences_data'):
                    existing_record.research_preferences_data = integrated_data.get('research_preferences', {})
                if hasattr(existing_record, 'api_keys_data'):
                    existing_record.api_keys_data = integrated_data.get('api_keys_data', {})
                existing_record.updated_at = datetime.utcnow()
            else:
                new_kwargs = {
                    'user_id': user_id,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                if 'website_analysis' in integrated_data:
                    new_kwargs['website_analysis_data'] = integrated_data.get('website_analysis', {})
                if 'research_preferences' in integrated_data:
                    new_kwargs['research_preferences_data'] = integrated_data.get('research_preferences', {})
                if 'api_keys_data' in integrated_data:
                    new_kwargs['api_keys_data'] = integrated_data.get('api_keys_data', {})

                new_record = OnboardingDataIntegration(**new_kwargs)
                db.add(new_record)

            db.commit()
            logger.info(f"Integrated onboarding data stored for user: {user_id}")

        except Exception as e:
            logger.error(f"Error storing integrated data for user {user_id}: {str(e)}")
            db.rollback()
            # Soft-fail storage: do not break the refresh path
            return

    def _get_fallback_data(self) -> Dict[str, Any]:
        """Get fallback data when processing fails."""
        return {
            'website_analysis': {},
            'research_preferences': {},
            'api_keys_data': {},
            'onboarding_session': {},
            'data_quality': {
                'overall_score': 0.0,
                'completeness': 0.0,
                'freshness': 0.0,
                'relevance': 0.0,
                'confidence': 0.0
            },
            'processing_timestamp': datetime.utcnow().isoformat()
        }

    async def get_integrated_data(self, user_id: int, db: Session) -> Optional[Dict[str, Any]]:
        """Get previously integrated onboarding data for a user."""
        try:
            record = db.query(OnboardingDataIntegration).filter(
                OnboardingDataIntegration.user_id == user_id
            ).first()

            if record:
                # Reconstruct integrated data from stored fields
                integrated_data = {
                    'website_analysis': record.website_analysis_data or {},
                    'research_preferences': record.research_preferences_data or {},
                    'api_keys_data': record.api_keys_data or {},
                    'onboarding_session': {},
                    'data_quality': self._assess_data_quality(
                        record.website_analysis_data or {},
                        record.research_preferences_data or {},
                        record.api_keys_data or {}
                    ),
                    'processing_timestamp': record.updated_at.isoformat()
                }

                # Check if data is still fresh
                updated_at = record.updated_at
                if datetime.utcnow() - updated_at <= self.data_freshness_threshold:
                    return integrated_data
                else:
                    logger.info(f"Integrated data is stale for user {user_id}, reprocessing...")
                    return await self.process_onboarding_data(user_id, db)

            return None

        except Exception as e:
            logger.error(f"Error getting integrated data for user {user_id}: {str(e)}")
            return None 