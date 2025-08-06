"""Personalization Logic Service for ALwrity Backend.

This service handles business logic for content personalization settings,
extracted from the legacy Streamlit component.
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from datetime import datetime

class PersonalizationLogic:
    """Business logic for content personalization and brand voice configuration."""
    
    def __init__(self):
        """Initialize the Personalization Logic service."""
        self.valid_writing_styles = ["Professional", "Casual", "Technical", "Conversational", "Academic"]
        self.valid_tones = ["Formal", "Semi-Formal", "Neutral", "Friendly", "Humorous"]
        self.valid_content_lengths = ["Concise", "Standard", "Detailed", "Comprehensive"]
        self.valid_personality_traits = ["Professional", "Innovative", "Friendly", "Trustworthy", "Creative", "Expert"]
        self.valid_readability_levels = ["Simple", "Standard", "Advanced", "Expert"]
        self.valid_content_structures = ["Introduction", "Key Points", "Examples", "Conclusion", "Call-to-Action"]
    
    def validate_content_style(self, style_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate content style configuration.
        
        Args:
            style_data: Dictionary containing content style settings
            
        Returns:
            Dict containing validation results
        """
        try:
            logger.info("Validating content style configuration")
            
            errors = []
            validated_style = {}
            
            # Validate writing style
            writing_style = style_data.get('writing_style', '')
            if writing_style not in self.valid_writing_styles:
                errors.append(f"Writing style must be one of: {', '.join(self.valid_writing_styles)}")
            else:
                validated_style['writing_style'] = writing_style
            
            # Validate tone
            tone = style_data.get('tone', '')
            if tone not in self.valid_tones:
                errors.append(f"Tone must be one of: {', '.join(self.valid_tones)}")
            else:
                validated_style['tone'] = tone
            
            # Validate content length
            content_length = style_data.get('content_length', '')
            if content_length not in self.valid_content_lengths:
                errors.append(f"Content length must be one of: {', '.join(self.valid_content_lengths)}")
            else:
                validated_style['content_length'] = content_length
            
            # Determine validation result
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.info("Content style validation successful")
                validated_style['validated_at'] = datetime.now().isoformat()
            else:
                logger.warning(f"Content style validation failed: {errors}")
            
            return {
                'valid': is_valid,
                'style_config': validated_style if is_valid else None,
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Error validating content style: {str(e)}")
            return {
                'valid': False,
                'style_config': None,
                'errors': [f"Style validation error: {str(e)}"]
            }
    
    def configure_brand_voice(self, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure brand voice settings.
        
        Args:
            brand_data: Dictionary containing brand voice settings
            
        Returns:
            Dict containing configuration results
        """
        try:
            logger.info("Configuring brand voice settings")
            
            errors = []
            configured_brand = {}
            
            # Validate personality traits
            personality_traits = brand_data.get('personality_traits', [])
            if not personality_traits:
                errors.append("At least one personality trait must be selected")
            else:
                invalid_traits = [trait for trait in personality_traits if trait not in self.valid_personality_traits]
                if invalid_traits:
                    errors.append(f"Invalid personality traits: {', '.join(invalid_traits)}")
                else:
                    configured_brand['personality_traits'] = personality_traits
            
            # Validate voice description (optional but if provided, must be valid)
            voice_description = brand_data.get('voice_description', '').strip()
            if voice_description and len(voice_description) < 10:
                errors.append("Voice description must be at least 10 characters long")
            elif voice_description:
                configured_brand['voice_description'] = voice_description
            
            # Validate keywords (optional)
            keywords = brand_data.get('keywords', '').strip()
            if keywords:
                configured_brand['keywords'] = keywords
            
            # Determine configuration result
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.info("Brand voice configuration successful")
                configured_brand['configured_at'] = datetime.now().isoformat()
            else:
                logger.warning(f"Brand voice configuration failed: {errors}")
            
            return {
                'valid': is_valid,
                'brand_config': configured_brand if is_valid else None,
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Error configuring brand voice: {str(e)}")
            return {
                'valid': False,
                'brand_config': None,
                'errors': [f"Brand configuration error: {str(e)}"]
            }
    
    def process_advanced_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process advanced content generation settings.
        
        Args:
            settings: Dictionary containing advanced settings
            
        Returns:
            Dict containing processing results
        """
        try:
            logger.info("Processing advanced content generation settings")
            
            errors = []
            processed_settings = {}
            
            # Validate SEO optimization (boolean)
            seo_optimization = settings.get('seo_optimization', False)
            if not isinstance(seo_optimization, bool):
                errors.append("SEO optimization must be a boolean value")
            else:
                processed_settings['seo_optimization'] = seo_optimization
            
            # Validate readability level
            readability_level = settings.get('readability_level', '')
            if readability_level not in self.valid_readability_levels:
                errors.append(f"Readability level must be one of: {', '.join(self.valid_readability_levels)}")
            else:
                processed_settings['readability_level'] = readability_level
            
            # Validate content structure
            content_structure = settings.get('content_structure', [])
            if not content_structure:
                errors.append("At least one content structure element must be selected")
            else:
                invalid_structures = [struct for struct in content_structure if struct not in self.valid_content_structures]
                if invalid_structures:
                    errors.append(f"Invalid content structure elements: {', '.join(invalid_structures)}")
                else:
                    processed_settings['content_structure'] = content_structure
            
            # Determine processing result
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.info("Advanced settings processing successful")
                processed_settings['processed_at'] = datetime.now().isoformat()
            else:
                logger.warning(f"Advanced settings processing failed: {errors}")
            
            return {
                'valid': is_valid,
                'advanced_settings': processed_settings if is_valid else None,
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Error processing advanced settings: {str(e)}")
            return {
                'valid': False,
                'advanced_settings': None,
                'errors': [f"Advanced settings error: {str(e)}"]
            }
    
    def process_personalization_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process complete personalization settings including all components.
        
        Args:
            settings: Dictionary containing complete personalization settings
            
        Returns:
            Dict containing processing results
        """
        try:
            logger.info("Processing complete personalization settings")
            
            # Validate content style
            content_style = settings.get('content_style', {})
            style_validation = self.validate_content_style(content_style)
            
            # Configure brand voice
            brand_voice = settings.get('brand_voice', {})
            brand_validation = self.configure_brand_voice(brand_voice)
            
            # Process advanced settings
            advanced_settings = settings.get('advanced_settings', {})
            advanced_validation = self.process_advanced_settings(advanced_settings)
            
            # Combine results
            all_errors = (
                style_validation.get('errors', []) +
                brand_validation.get('errors', []) +
                advanced_validation.get('errors', [])
            )
            
            is_complete = (
                style_validation.get('valid', False) and
                brand_validation.get('valid', False) and
                advanced_validation.get('valid', False)
            )
            
            if is_complete:
                # Combine all valid settings
                complete_settings = {
                    'content_style': style_validation.get('style_config'),
                    'brand_voice': brand_validation.get('brand_config'),
                    'advanced_settings': advanced_validation.get('advanced_settings'),
                    'processed_at': datetime.now().isoformat()
                }
                
                logger.info("Complete personalization settings processed successfully")
                
                return {
                    'valid': True,
                    'settings': complete_settings,
                    'errors': []
                }
            else:
                logger.warning(f"Personalization settings processing failed: {all_errors}")
                
                return {
                    'valid': False,
                    'settings': None,
                    'errors': all_errors
                }
                
        except Exception as e:
            logger.error(f"Error processing personalization settings: {str(e)}")
            return {
                'valid': False,
                'settings': None,
                'errors': [f"Personalization processing error: {str(e)}"]
            }
    
    def get_personalization_configuration_options(self) -> Dict[str, Any]:
        """
        Get available configuration options for personalization.
        
        Returns:
            Dict containing all available options
        """
        return {
            'writing_styles': self.valid_writing_styles,
            'tones': self.valid_tones,
            'content_lengths': self.valid_content_lengths,
            'personality_traits': self.valid_personality_traits,
            'readability_levels': self.valid_readability_levels,
            'content_structures': self.valid_content_structures,
            'seo_optimization_options': [True, False]
        }
    
    def generate_content_guidelines(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content guidelines based on personalization settings.
        
        Args:
            settings: Validated personalization settings
            
        Returns:
            Dict containing content guidelines
        """
        try:
            logger.info("Generating content guidelines from personalization settings")
            
            content_style = settings.get('content_style', {})
            brand_voice = settings.get('brand_voice', {})
            advanced_settings = settings.get('advanced_settings', {})
            
            guidelines = {
                'writing_style': content_style.get('writing_style', 'Professional'),
                'tone': content_style.get('tone', 'Neutral'),
                'content_length': content_style.get('content_length', 'Standard'),
                'brand_personality': brand_voice.get('personality_traits', []),
                'seo_optimized': advanced_settings.get('seo_optimization', False),
                'readability_level': advanced_settings.get('readability_level', 'Standard'),
                'required_sections': advanced_settings.get('content_structure', []),
                'generated_at': datetime.now().isoformat()
            }
            
            logger.info("Content guidelines generated successfully")
            
            return {
                'success': True,
                'guidelines': guidelines
            }
            
        except Exception as e:
            logger.error(f"Error generating content guidelines: {str(e)}")
            return {
                'success': False,
                'error': f"Guidelines generation error: {str(e)}"
            } 