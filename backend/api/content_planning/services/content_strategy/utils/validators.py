"""
Validation Service
Data validation utilities.
"""

import logging
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ValidationService:
    """Service for data validation and business rule checking."""

    def __init__(self):
        self.validation_patterns = {
            'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            'url': re.compile(r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'),
            'phone': re.compile(r'^\+?1?\d{9,15}$'),
            'domain': re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'),
            'alphanumeric': re.compile(r'^[a-zA-Z0-9\s]+$'),
            'numeric': re.compile(r'^\d+(\.\d+)?$'),
            'integer': re.compile(r'^\d+$')
        }
        
        self.business_rules = {
            'content_budget': {
                'min_value': 0,
                'max_value': 1000000,
                'required': True
            },
            'team_size': {
                'min_value': 1,
                'max_value': 100,
                'required': True
            },
            'implementation_timeline': {
                'min_days': 1,
                'max_days': 365,
                'required': True
            },
            'market_share': {
                'min_value': 0,
                'max_value': 100,
                'required': False
            }
        }

    def validate_field(self, field_name: str, value: Any, field_type: str = 'string', **kwargs) -> Dict[str, Any]:
        """Validate a single field."""
        try:
            validation_result = {
                'field_name': field_name,
                'value': value,
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'validation_timestamp': datetime.utcnow().isoformat()
            }
            
            # Check if value is required
            if kwargs.get('required', False) and (value is None or value == ''):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' is required")
                return validation_result
            
            # Skip validation if value is None and not required
            if value is None or value == '':
                return validation_result
            
            # Type-specific validation
            if field_type == 'email':
                validation_result = self._validate_email(field_name, value, validation_result)
            elif field_type == 'url':
                validation_result = self._validate_url(field_name, value, validation_result)
            elif field_type == 'phone':
                validation_result = self._validate_phone(field_name, value, validation_result)
            elif field_type == 'domain':
                validation_result = self._validate_domain(field_name, value, validation_result)
            elif field_type == 'alphanumeric':
                validation_result = self._validate_alphanumeric(field_name, value, validation_result)
            elif field_type == 'numeric':
                validation_result = self._validate_numeric(field_name, value, validation_result)
            elif field_type == 'integer':
                validation_result = self._validate_integer(field_name, value, validation_result)
            elif field_type == 'date':
                validation_result = self._validate_date(field_name, value, validation_result)
            elif field_type == 'json':
                validation_result = self._validate_json(field_name, value, validation_result)
            else:
                validation_result = self._validate_string(field_name, value, validation_result)
            
            # Length validation
            if 'min_length' in kwargs and len(str(value)) < kwargs['min_length']:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be at least {kwargs['min_length']} characters long")
            
            if 'max_length' in kwargs and len(str(value)) > kwargs['max_length']:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be no more than {kwargs['max_length']} characters long")
            
            # Range validation for numeric fields
            if field_type in ['numeric', 'integer']:
                if 'min_value' in kwargs and float(value) < kwargs['min_value']:
                    validation_result['is_valid'] = False
                    validation_result['errors'].append(f"Field '{field_name}' must be at least {kwargs['min_value']}")
                
                if 'max_value' in kwargs and float(value) > kwargs['max_value']:
                    validation_result['is_valid'] = False
                    validation_result['errors'].append(f"Field '{field_name}' must be no more than {kwargs['max_value']}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating field {field_name}: {str(e)}")
            return {
                'field_name': field_name,
                'value': value,
                'is_valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': [],
                'validation_timestamp': datetime.utcnow().isoformat()
            }

    def validate_business_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against business rules."""
        try:
            validation_result = {
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'field_validations': {},
                'validation_timestamp': datetime.utcnow().isoformat()
            }
            
            for field_name, rules in self.business_rules.items():
                if field_name in data:
                    field_validation = self.validate_field(
                        field_name,
                        data[field_name],
                        **rules
                    )
                    validation_result['field_validations'][field_name] = field_validation
                    
                    if not field_validation['is_valid']:
                        validation_result['is_valid'] = False
                        validation_result['errors'].extend(field_validation['errors'])
                    
                    validation_result['warnings'].extend(field_validation['warnings'])
                elif rules.get('required', False):
                    validation_result['is_valid'] = False
                    validation_result['errors'].append(f"Required field '{field_name}' is missing")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating business rules: {str(e)}")
            return {
                'is_valid': False,
                'errors': [f"Business rule validation error: {str(e)}"],
                'warnings': [],
                'field_validations': {},
                'validation_timestamp': datetime.utcnow().isoformat()
            }

    def validate_strategy_data(self, strategy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate content strategy data specifically."""
        try:
            validation_result = {
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'field_validations': {},
                'validation_timestamp': datetime.utcnow().isoformat()
            }
            
            # Required fields for content strategy
            required_fields = [
                'business_objectives', 'target_metrics', 'content_budget',
                'team_size', 'implementation_timeline'
            ]
            
            for field in required_fields:
                if field not in strategy_data or strategy_data[field] is None or strategy_data[field] == '':
                    validation_result['is_valid'] = False
                    validation_result['errors'].append(f"Required field '{field}' is missing")
                else:
                    # Validate specific field types
                    if field == 'content_budget':
                        field_validation = self.validate_field(field, strategy_data[field], 'numeric', min_value=0, max_value=1000000)
                    elif field == 'team_size':
                        field_validation = self.validate_field(field, strategy_data[field], 'integer', min_value=1, max_value=100)
                    elif field == 'implementation_timeline':
                        field_validation = self.validate_field(field, strategy_data[field], 'string', min_length=1, max_length=500)
                    else:
                        field_validation = self.validate_field(field, strategy_data[field], 'string', min_length=1)
                    
                    validation_result['field_validations'][field] = field_validation
                    
                    if not field_validation['is_valid']:
                        validation_result['is_valid'] = False
                        validation_result['errors'].extend(field_validation['errors'])
                    
                    validation_result['warnings'].extend(field_validation['warnings'])
            
            # Validate optional fields
            optional_fields = {
                'market_share': ('numeric', {'min_value': 0, 'max_value': 100}),
                'competitive_position': ('string', {'max_length': 1000}),
                'content_preferences': ('string', {'max_length': 2000}),
                'audience_pain_points': ('string', {'max_length': 2000}),
                'top_competitors': ('string', {'max_length': 1000}),
                'industry_trends': ('string', {'max_length': 1000})
            }
            
            for field, (field_type, validation_params) in optional_fields.items():
                if field in strategy_data and strategy_data[field]:
                    field_validation = self.validate_field(field, strategy_data[field], field_type, **validation_params)
                    validation_result['field_validations'][field] = field_validation
                    
                    if not field_validation['is_valid']:
                        validation_result['warnings'].extend(field_validation['errors'])
                    
                    validation_result['warnings'].extend(field_validation['warnings'])
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating strategy data: {str(e)}")
            return {
                'is_valid': False,
                'errors': [f"Strategy validation error: {str(e)}"],
                'warnings': [],
                'field_validations': {},
                'validation_timestamp': datetime.utcnow().isoformat()
            }

    def _validate_email(self, field_name: str, value: str, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate email format."""
        try:
            if not self.validation_patterns['email'].match(value):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be a valid email address")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Email validation error: {str(e)}")
            return validation_result

    def _validate_url(self, field_name: str, value: str, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate URL format."""
        try:
            if not self.validation_patterns['url'].match(value):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be a valid URL")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating URL: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"URL validation error: {str(e)}")
            return validation_result

    def _validate_phone(self, field_name: str, value: str, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate phone number format."""
        try:
            if not self.validation_patterns['phone'].match(value):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be a valid phone number")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating phone: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Phone validation error: {str(e)}")
            return validation_result

    def _validate_domain(self, field_name: str, value: str, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate domain format."""
        try:
            if not self.validation_patterns['domain'].match(value):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be a valid domain")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating domain: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Domain validation error: {str(e)}")
            return validation_result

    def _validate_alphanumeric(self, field_name: str, value: str, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate alphanumeric format."""
        try:
            if not self.validation_patterns['alphanumeric'].match(value):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must contain only letters, numbers, and spaces")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating alphanumeric: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Alphanumeric validation error: {str(e)}")
            return validation_result

    def _validate_numeric(self, field_name: str, value: Union[str, int, float], validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate numeric format."""
        try:
            if isinstance(value, (int, float)):
                return validation_result
            
            if not self.validation_patterns['numeric'].match(str(value)):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be a valid number")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating numeric: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Numeric validation error: {str(e)}")
            return validation_result

    def _validate_integer(self, field_name: str, value: Union[str, int], validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate integer format."""
        try:
            if isinstance(value, int):
                return validation_result
            
            if not self.validation_patterns['integer'].match(str(value)):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be a valid integer")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating integer: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Integer validation error: {str(e)}")
            return validation_result

    def _validate_date(self, field_name: str, value: Union[str, datetime], validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate date format."""
        try:
            if isinstance(value, datetime):
                return validation_result
            
            # Try to parse date string
            try:
                datetime.fromisoformat(str(value).replace('Z', '+00:00'))
            except ValueError:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be a valid date")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating date: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Date validation error: {str(e)}")
            return validation_result

    def _validate_json(self, field_name: str, value: Union[str, dict, list], validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JSON format."""
        try:
            if isinstance(value, (dict, list)):
                return validation_result
            
            import json
            try:
                json.loads(str(value))
            except json.JSONDecodeError:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be valid JSON")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating JSON: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"JSON validation error: {str(e)}")
            return validation_result

    def _validate_string(self, field_name: str, value: str, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate string format."""
        try:
            if not isinstance(value, str):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Field '{field_name}' must be a string")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating string: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"String validation error: {str(e)}")
            return validation_result

    def generate_validation_error_message(self, validation_result: Dict[str, Any]) -> str:
        """Generate a user-friendly error message from validation results."""
        try:
            if validation_result['is_valid']:
                return "Validation passed successfully"
            
            if 'errors' in validation_result and validation_result['errors']:
                error_count = len(validation_result['errors'])
                if error_count == 1:
                    return f"Validation error: {validation_result['errors'][0]}"
                else:
                    return f"Validation failed with {error_count} errors: {'; '.join(validation_result['errors'])}"
            
            return "Validation failed with unknown errors"
            
        except Exception as e:
            logger.error(f"Error generating validation error message: {str(e)}")
            return "Error generating validation message"

    def get_validation_summary(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of multiple validation results."""
        try:
            summary = {
                'total_validations': len(validation_results),
                'passed_validations': 0,
                'failed_validations': 0,
                'total_errors': 0,
                'total_warnings': 0,
                'field_summary': {},
                'validation_timestamp': datetime.utcnow().isoformat()
            }
            
            for result in validation_results:
                if result.get('is_valid', False):
                    summary['passed_validations'] += 1
                else:
                    summary['failed_validations'] += 1
                
                summary['total_errors'] += len(result.get('errors', []))
                summary['total_warnings'] += len(result.get('warnings', []))
                
                field_name = result.get('field_name', 'unknown')
                if field_name not in summary['field_summary']:
                    summary['field_summary'][field_name] = {
                        'validations': 0,
                        'errors': 0,
                        'warnings': 0
                    }
                
                summary['field_summary'][field_name]['validations'] += 1
                summary['field_summary'][field_name]['errors'] += len(result.get('errors', []))
                summary['field_summary'][field_name]['warnings'] += len(result.get('warnings', []))
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating validation summary: {str(e)}")
            return {
                'total_validations': 0,
                'passed_validations': 0,
                'failed_validations': 0,
                'total_errors': 0,
                'total_warnings': 0,
                'field_summary': {},
                'validation_timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            } 