"""AI Research Logic Service for ALwrity Backend.

This service handles business logic for AI research configuration and user information
validation, extracted from the legacy Streamlit component.
"""

from typing import Dict, Any, List, Optional
from loguru import logger
import re
from datetime import datetime

class AIResearchLogic:
    """Business logic for AI research configuration and user information."""
    
    def __init__(self):
        """Initialize the AI Research Logic service."""
        self.valid_roles = ["Content Creator", "Marketing Manager", "Business Owner", "Other"]
        self.valid_research_depths = ["Basic", "Standard", "Deep", "Comprehensive"]
        self.valid_content_types = ["Blog Posts", "Social Media", "Technical Articles", "News", "Academic Papers"]
    
    def validate_user_info(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user information for AI research configuration.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Dict containing validation results
        """
        try:
            logger.info("Validating user information for AI research")
            
            errors = []
            validated_data = {}
            
            # Validate full name
            full_name = user_data.get('full_name', '').strip()
            if not full_name or len(full_name) < 2:
                errors.append("Full name must be at least 2 characters long")
            else:
                validated_data['full_name'] = full_name
            
            # Validate email
            email = user_data.get('email', '').strip().lower()
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(email):
                errors.append("Invalid email format")
            else:
                validated_data['email'] = email
            
            # Validate company
            company = user_data.get('company', '').strip()
            if not company:
                errors.append("Company name is required")
            else:
                validated_data['company'] = company
            
            # Validate role
            role = user_data.get('role', '')
            if role not in self.valid_roles:
                errors.append(f"Role must be one of: {', '.join(self.valid_roles)}")
            else:
                validated_data['role'] = role
            
            # Determine validation result
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.info("User information validation successful")
                validated_data['validated_at'] = datetime.now().isoformat()
            else:
                logger.warning(f"User information validation failed: {errors}")
            
            return {
                'valid': is_valid,
                'user_info': validated_data if is_valid else None,
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Error validating user information: {str(e)}")
            return {
                'valid': False,
                'user_info': None,
                'errors': [f"Validation error: {str(e)}"]
            }
    
    def configure_research_preferences(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure research preferences for AI research.
        
        Args:
            preferences: Dictionary containing research preferences
            
        Returns:
            Dict containing configuration results
        """
        try:
            logger.info("Configuring research preferences")
            
            errors = []
            configured_preferences = {}
            
            # Validate research depth
            research_depth = preferences.get('research_depth', '')
            if research_depth not in self.valid_research_depths:
                errors.append(f"Research depth must be one of: {', '.join(self.valid_research_depths)}")
            else:
                configured_preferences['research_depth'] = research_depth
            
            # Validate content types
            content_types = preferences.get('content_types', [])
            if not content_types:
                errors.append("At least one content type must be selected")
            else:
                invalid_types = [ct for ct in content_types if ct not in self.valid_content_types]
                if invalid_types:
                    errors.append(f"Invalid content types: {', '.join(invalid_types)}")
                else:
                    configured_preferences['content_types'] = content_types
            
            # Validate auto research setting
            auto_research = preferences.get('auto_research', False)
            if not isinstance(auto_research, bool):
                errors.append("Auto research must be a boolean value")
            else:
                configured_preferences['auto_research'] = auto_research
            
            # Determine configuration result
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.info("Research preferences configuration successful")
                configured_preferences['configured_at'] = datetime.now().isoformat()
            else:
                logger.warning(f"Research preferences configuration failed: {errors}")
            
            return {
                'valid': is_valid,
                'preferences': configured_preferences if is_valid else None,
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Error configuring research preferences: {str(e)}")
            return {
                'valid': False,
                'preferences': None,
                'errors': [f"Configuration error: {str(e)}"]
            }
    
    def process_research_request(self, topic: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a research request with configured preferences.
        
        Args:
            topic: The research topic
            preferences: Configured research preferences
            
        Returns:
            Dict containing research processing results
        """
        try:
            logger.info(f"Processing research request for topic: {topic}")
            
            # Validate topic
            if not topic or len(topic.strip()) < 3:
                return {
                    'success': False,
                    'topic': topic,
                    'error': 'Topic must be at least 3 characters long'
                }
            
            # Validate preferences
            if not preferences:
                return {
                    'success': False,
                    'topic': topic,
                    'error': 'Research preferences are required'
                }
            
            # Process research based on preferences
            research_depth = preferences.get('research_depth', 'Standard')
            content_types = preferences.get('content_types', [])
            auto_research = preferences.get('auto_research', False)
            
            # Simulate research processing (in real implementation, this would call AI services)
            research_results = {
                'topic': topic,
                'research_depth': research_depth,
                'content_types': content_types,
                'auto_research': auto_research,
                'processed_at': datetime.now().isoformat(),
                'status': 'processed'
            }
            
            logger.info(f"Research request processed successfully for topic: {topic}")
            
            return {
                'success': True,
                'topic': topic,
                'results': research_results
            }
            
        except Exception as e:
            logger.error(f"Error processing research request: {str(e)}")
            return {
                'success': False,
                'topic': topic,
                'error': f"Processing error: {str(e)}"
            }
    
    def get_research_configuration_options(self) -> Dict[str, Any]:
        """
        Get available configuration options for research.
        
        Returns:
            Dict containing all available options
        """
        return {
            'roles': self.valid_roles,
            'research_depths': self.valid_research_depths,
            'content_types': self.valid_content_types,
            'auto_research_options': [True, False]
        }
    
    def validate_complete_research_setup(self, user_info: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate complete research setup including user info and preferences.
        
        Args:
            user_info: User information dictionary
            preferences: Research preferences dictionary
            
        Returns:
            Dict containing complete validation results
        """
        try:
            logger.info("Validating complete research setup")
            
            # Validate user information
            user_validation = self.validate_user_info(user_info)
            
            # Validate research preferences
            preferences_validation = self.configure_research_preferences(preferences)
            
            # Combine results
            all_errors = user_validation.get('errors', []) + preferences_validation.get('errors', [])
            is_complete = user_validation.get('valid', False) and preferences_validation.get('valid', False)
            
            return {
                'complete': is_complete,
                'user_info_valid': user_validation.get('valid', False),
                'preferences_valid': preferences_validation.get('valid', False),
                'errors': all_errors,
                'user_info': user_validation.get('user_info'),
                'preferences': preferences_validation.get('preferences')
            }
            
        except Exception as e:
            logger.error(f"Error validating complete research setup: {str(e)}")
            return {
                'complete': False,
                'user_info_valid': False,
                'preferences_valid': False,
                'errors': [f"Setup validation error: {str(e)}"]
            } 