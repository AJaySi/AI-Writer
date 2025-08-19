#!/usr/bin/env python3
"""
Test script to validate onboarding data existence in the database.
This script checks if onboarding data exists for test users and validates the data flow.
"""

import sys
import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from services.database import get_db_session
from models.onboarding import OnboardingSession, WebsiteAnalysis, ResearchPreferences, APIKey
from models.enhanced_strategy_models import OnboardingDataIntegration
from api.content_planning.services.content_strategy.onboarding.data_integration import OnboardingDataIntegrationService
from api.content_planning.services.content_strategy.autofill.ai_structured_autofill import AIStructuredAutofillService
from services.ai_service_manager import AIServiceManager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('onboarding_test.log')
    ]
)
logger = logging.getLogger(__name__)

class OnboardingDataValidator:
    """Validator for onboarding data existence and quality."""
    
    def __init__(self):
        self.db_session = get_db_session()
        self.data_integration_service = OnboardingDataIntegrationService()
        self.ai_service = AIStructuredAutofillService()
        self.ai_manager = AIServiceManager()
    
    def test_database_connection(self) -> bool:
        """Test database connection."""
        try:
            # Simple query to test connection
            from sqlalchemy import text
            result = self.db_session.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def check_onboarding_sessions(self, user_ids: list = None) -> Dict[int, Dict[str, Any]]:
        """Check onboarding sessions for given user IDs."""
        if user_ids is None:
            user_ids = [1, 2, 3]  # Default test user IDs
        
        results = {}
        
        for user_id in user_ids:
            logger.info(f"🔍 Checking onboarding session for user {user_id}")
            
            try:
                session = self.db_session.query(OnboardingSession).filter(
                    OnboardingSession.user_id == user_id
                ).order_by(OnboardingSession.updated_at.desc()).first()
                
                if session:
                    results[user_id] = {
                        'session_exists': True,
                        'session_id': session.id,
                        'status': session.status,
                        'progress': session.progress,
                        'created_at': session.created_at.isoformat(),
                        'updated_at': session.updated_at.isoformat(),
                        'data': session.to_dict() if hasattr(session, 'to_dict') else str(session)
                    }
                    logger.info(f"✅ Onboarding session found for user {user_id}: {session.status}")
                else:
                    results[user_id] = {
                        'session_exists': False,
                        'error': 'No onboarding session found'
                    }
                    logger.warning(f"❌ No onboarding session found for user {user_id}")
                    
            except Exception as e:
                results[user_id] = {
                    'session_exists': False,
                    'error': str(e)
                }
                logger.error(f"❌ Error checking onboarding session for user {user_id}: {e}")
        
        return results
    
    def check_website_analysis(self, user_ids: list = None) -> Dict[int, Dict[str, Any]]:
        """Check website analysis data for given user IDs."""
        if user_ids is None:
            user_ids = [1, 2, 3]
        
        results = {}
        
        for user_id in user_ids:
            logger.info(f"🔍 Checking website analysis for user {user_id}")
            
            try:
                # Get onboarding session first
                session = self.db_session.query(OnboardingSession).filter(
                    OnboardingSession.user_id == user_id
                ).order_by(OnboardingSession.updated_at.desc()).first()
                
                if not session:
                    results[user_id] = {
                        'website_analysis_exists': False,
                        'error': 'No onboarding session found'
                    }
                    continue
                
                # Get website analysis
                website_analysis = self.db_session.query(WebsiteAnalysis).filter(
                    WebsiteAnalysis.session_id == session.id
                ).order_by(WebsiteAnalysis.updated_at.desc()).first()
                
                if website_analysis:
                    results[user_id] = {
                        'website_analysis_exists': True,
                        'analysis_id': website_analysis.id,
                        'website_url': website_analysis.website_url,
                        'status': website_analysis.status,
                        'created_at': website_analysis.created_at.isoformat(),
                        'updated_at': website_analysis.updated_at.isoformat(),
                        'data_keys': list(website_analysis.to_dict().keys()) if hasattr(website_analysis, 'to_dict') else []
                    }
                    logger.info(f"✅ Website analysis found for user {user_id}: {website_analysis.website_url}")
                else:
                    results[user_id] = {
                        'website_analysis_exists': False,
                        'error': 'No website analysis found'
                    }
                    logger.warning(f"❌ No website analysis found for user {user_id}")
                    
            except Exception as e:
                results[user_id] = {
                    'website_analysis_exists': False,
                    'error': str(e)
                }
                logger.error(f"❌ Error checking website analysis for user {user_id}: {e}")
        
        return results
    
    def check_research_preferences(self, user_ids: list = None) -> Dict[int, Dict[str, Any]]:
        """Check research preferences data for given user IDs."""
        if user_ids is None:
            user_ids = [1, 2, 3]
        
        results = {}
        
        for user_id in user_ids:
            logger.info(f"🔍 Checking research preferences for user {user_id}")
            
            try:
                # Get onboarding session first
                session = self.db_session.query(OnboardingSession).filter(
                    OnboardingSession.user_id == user_id
                ).order_by(OnboardingSession.updated_at.desc()).first()
                
                if not session:
                    results[user_id] = {
                        'research_preferences_exists': False,
                        'error': 'No onboarding session found'
                    }
                    continue
                
                # Get research preferences
                research_prefs = self.db_session.query(ResearchPreferences).filter(
                    ResearchPreferences.session_id == session.id
                ).first()
                
                if research_prefs:
                    results[user_id] = {
                        'research_preferences_exists': True,
                        'prefs_id': research_prefs.id,
                        'research_depth': research_prefs.research_depth,
                        'content_types': research_prefs.content_types,
                        'created_at': research_prefs.created_at.isoformat(),
                        'updated_at': research_prefs.updated_at.isoformat(),
                        'data_keys': list(research_prefs.to_dict().keys()) if hasattr(research_prefs, 'to_dict') else []
                    }
                    logger.info(f"✅ Research preferences found for user {user_id}: {research_prefs.research_depth}")
                else:
                    results[user_id] = {
                        'research_preferences_exists': False,
                        'error': 'No research preferences found'
                    }
                    logger.warning(f"❌ No research preferences found for user {user_id}")
                    
            except Exception as e:
                results[user_id] = {
                    'research_preferences_exists': False,
                    'error': str(e)
                }
                logger.error(f"❌ Error checking research preferences for user {user_id}: {e}")
        
        return results
    
    def check_api_keys(self, user_ids: list = None) -> Dict[int, Dict[str, Any]]:
        """Check API keys data for given user IDs."""
        if user_ids is None:
            user_ids = [1, 2, 3]
        
        results = {}
        
        for user_id in user_ids:
            logger.info(f"🔍 Checking API keys for user {user_id}")
            
            try:
                # Get onboarding session first
                session = self.db_session.query(OnboardingSession).filter(
                    OnboardingSession.user_id == user_id
                ).order_by(OnboardingSession.updated_at.desc()).first()
                
                if not session:
                    results[user_id] = {
                        'api_keys_exist': False,
                        'error': 'No onboarding session found'
                    }
                    continue
                
                # Get API keys
                api_keys = self.db_session.query(APIKey).filter(
                    APIKey.session_id == session.id
                ).all()
                
                if api_keys:
                    results[user_id] = {
                        'api_keys_exist': True,
                        'count': len(api_keys),
                        'providers': [key.provider for key in api_keys],
                        'created_at': api_keys[0].created_at.isoformat() if api_keys else None,
                        'updated_at': api_keys[0].updated_at.isoformat() if api_keys else None
                    }
                    logger.info(f"✅ API keys found for user {user_id}: {len(api_keys)} keys")
                else:
                    results[user_id] = {
                        'api_keys_exist': False,
                        'error': 'No API keys found'
                    }
                    logger.warning(f"❌ No API keys found for user {user_id}")
                    
            except Exception as e:
                results[user_id] = {
                    'api_keys_exist': False,
                    'error': str(e)
                }
                logger.error(f"❌ Error checking API keys for user {user_id}: {e}")
        
        return results
    
    async def test_data_integration_service(self, user_id: int = 1) -> Dict[str, Any]:
        """Test the data integration service."""
        logger.info(f"🔍 Testing data integration service for user {user_id}")
        
        try:
            # Test the process_onboarding_data method
            integrated_data = await self.data_integration_service.process_onboarding_data(user_id, self.db_session)
            
            if integrated_data:
                result = {
                    'success': True,
                    'has_website_analysis': bool(integrated_data.get('website_analysis')),
                    'has_research_preferences': bool(integrated_data.get('research_preferences')),
                    'has_api_keys_data': bool(integrated_data.get('api_keys_data')),
                    'has_onboarding_session': bool(integrated_data.get('onboarding_session')),
                    'data_quality': integrated_data.get('data_quality', {}),
                    'processing_timestamp': integrated_data.get('processing_timestamp'),
                    'context_keys': list(integrated_data.keys())
                }
                
                logger.info(f"✅ Data integration successful for user {user_id}")
                logger.info(f"   Website analysis: {result['has_website_analysis']}")
                logger.info(f"   Research preferences: {result['has_research_preferences']}")
                logger.info(f"   API keys: {result['has_api_keys_data']}")
                logger.info(f"   Onboarding session: {result['has_onboarding_session']}")
                
                return result
            else:
                logger.error(f"❌ Data integration returned None for user {user_id}")
                return {'success': False, 'error': 'No data returned'}
                
        except Exception as e:
            logger.error(f"❌ Data integration failed for user {user_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_ai_service_configuration(self) -> Dict[str, Any]:
        """Test AI service configuration."""
        logger.info("🔍 Testing AI service configuration")
        
        try:
            # Test basic AI service functionality
            test_prompt = "Generate a simple test response"
            test_schema = {
                "type": "OBJECT",
                "properties": {
                    "test_field": {"type": "STRING", "description": "A test field"}
                },
                "required": ["test_field"]
            }
            
            # Test the AI service manager
            result = await self.ai_manager.execute_structured_json_call(
                service_type="STRATEGIC_INTELLIGENCE",
                prompt=test_prompt,
                schema=test_schema
            )
            
            if result and not result.get('error'):
                logger.info("✅ AI service configuration successful")
                return {
                    'success': True,
                    'ai_service_working': True,
                    'test_response': result
                }
            else:
                logger.error(f"❌ AI service test failed: {result.get('error', 'Unknown error')}")
                return {
                    'success': False,
                    'ai_service_working': False,
                    'error': result.get('error', 'Unknown error')
                }
                
        except Exception as e:
            logger.error(f"❌ AI service configuration test failed: {e}")
            return {
                'success': False,
                'ai_service_working': False,
                'error': str(e)
            }
    
    async def test_ai_structured_autofill(self, user_id: int = 1) -> Dict[str, Any]:
        """Test the AI structured autofill service."""
        logger.info(f"🔍 Testing AI structured autofill for user {user_id}")
        
        try:
            # First get the context
            integrated_data = await self.data_integration_service.process_onboarding_data(user_id, self.db_session)
            
            if not integrated_data:
                logger.error(f"❌ No integrated data available for user {user_id}")
                return {'success': False, 'error': 'No integrated data available'}
            
            # Test the AI structured autofill
            result = await self.ai_service.generate_autofill_fields(user_id, integrated_data)
            
            if result:
                meta = result.get('meta', {})
                fields = result.get('fields', {})
                
                test_result = {
                    'success': True,
                    'ai_used': meta.get('ai_used', False),
                    'ai_overrides_count': meta.get('ai_overrides_count', 0),
                    'success_rate': meta.get('success_rate', 0),
                    'attempts': meta.get('attempts', 0),
                    'missing_fields': meta.get('missing_fields', []),
                    'fields_generated': len(fields),
                    'sample_fields': list(fields.keys())[:5] if fields else []
                }
                
                logger.info(f"✅ AI structured autofill test completed for user {user_id}")
                logger.info(f"   AI used: {test_result['ai_used']}")
                logger.info(f"   Fields generated: {test_result['fields_generated']}")
                logger.info(f"   Success rate: {test_result['success_rate']:.1f}%")
                logger.info(f"   Attempts: {test_result['attempts']}")
                
                return test_result
            else:
                logger.error(f"❌ AI structured autofill returned None for user {user_id}")
                return {'success': False, 'error': 'No result returned'}
                
        except Exception as e:
            logger.error(f"❌ AI structured autofill test failed for user {user_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a summary of all test results."""
        logger.info("\n" + "="*80)
        logger.info("📊 ONBOARDING DATA VALIDATION SUMMARY")
        logger.info("="*80)
        
        for test_name, result in results.items():
            logger.info(f"\n🔍 {test_name.upper()}:")
            if isinstance(result, dict):
                for key, value in result.items():
                    if isinstance(value, dict):
                        logger.info(f"   {key}:")
                        for sub_key, sub_value in value.items():
                            logger.info(f"     {sub_key}: {sub_value}")
                    else:
                        logger.info(f"   {key}: {value}")
            else:
                logger.info(f"   {result}")
        
        logger.info("\n" + "="*80)
    
    def cleanup(self):
        """Clean up database session."""
        if self.db_session:
            self.db_session.close()

async def main():
    """Main test function."""
    logger.info("🚀 Starting onboarding data validation tests")
    
    validator = OnboardingDataValidator()
    
    try:
        # Test database connection
        db_connected = validator.test_database_connection()
        if not db_connected:
            logger.error("❌ Cannot proceed without database connection")
            return
        
        # Test user IDs to check
        test_user_ids = [1, 2, 3]
        
        # Run all tests
        results = {
            'database_connection': db_connected,
            'onboarding_sessions': validator.check_onboarding_sessions(test_user_ids),
            'website_analysis': validator.check_website_analysis(test_user_ids),
            'research_preferences': validator.check_research_preferences(test_user_ids),
            'api_keys': validator.check_api_keys(test_user_ids),
            'data_integration': await validator.test_data_integration_service(1),
            'ai_service_config': await validator.test_ai_service_configuration(),
            'ai_structured_autofill': await validator.test_ai_structured_autofill(1)
        }
        
        # Print summary
        validator.print_summary(results)
        
        # Determine overall status
        overall_success = all([
            results['database_connection'],
            any(session.get('session_exists', False) for session in results['onboarding_sessions'].values()),
            results['data_integration']['success'],
            results['ai_service_config']['success']
        ])
        
        if overall_success:
            logger.info("✅ All critical tests passed!")
        else:
            logger.error("❌ Some critical tests failed!")
            
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
    finally:
        validator.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 