"""
Data Processor Service
Data processing utilities.
"""

import logging
import json
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DataProcessorService:
    """Service for data processing utilities."""

    def __init__(self):
        self.cleaning_patterns = {
            'html_tags': re.compile(r'<[^>]+>'),
            'extra_whitespace': re.compile(r'\s+'),
            'special_chars': re.compile(r'[^\w\s\-.,!?;:()]'),
            'multiple_spaces': re.compile(r'\s{2,}'),
            'leading_trailing_spaces': re.compile(r'^\s+|\s+$')
        }

    def transform_data_structure(self, data: Union[Dict, List, str], target_format: str = 'dict') -> Union[Dict, List, str]:
        """Transform data between different structures."""
        try:
            if target_format == 'dict':
                if isinstance(data, dict):
                    return data
                elif isinstance(data, list):
                    return {str(i): item for i, item in enumerate(data)}
                elif isinstance(data, str):
                    try:
                        return json.loads(data)
                    except json.JSONDecodeError:
                        return {'value': data}
                else:
                    return {'value': str(data)}
            
            elif target_format == 'list':
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return list(data.values())
                elif isinstance(data, str):
                    return [data]
                else:
                    return [str(data)]
            
            elif target_format == 'string':
                if isinstance(data, str):
                    return data
                elif isinstance(data, (dict, list)):
                    return json.dumps(data, default=str)
                else:
                    return str(data)
            
            else:
                logger.warning(f"Unknown target format: {target_format}")
                return data
                
        except Exception as e:
            logger.error(f"Error transforming data structure: {str(e)}")
            return data

    def clean_text_data(self, text: str, cleaning_level: str = 'standard') -> str:
        """Clean and normalize text data."""
        try:
            if not isinstance(text, str):
                text = str(text)
            
            if cleaning_level == 'minimal':
                # Basic cleaning
                cleaned = self.cleaning_patterns['leading_trailing_spaces'].sub('', text)
                cleaned = self.cleaning_patterns['multiple_spaces'].sub(' ', cleaned)
                return cleaned.strip()
            
            elif cleaning_level == 'standard':
                # Standard cleaning
                cleaned = self.cleaning_patterns['html_tags'].sub('', text)
                cleaned = self.cleaning_patterns['leading_trailing_spaces'].sub('', cleaned)
                cleaned = self.cleaning_patterns['multiple_spaces'].sub(' ', cleaned)
                return cleaned.strip()
            
            elif cleaning_level == 'aggressive':
                # Aggressive cleaning
                cleaned = self.cleaning_patterns['html_tags'].sub('', text)
                cleaned = self.cleaning_patterns['special_chars'].sub('', cleaned)
                cleaned = self.cleaning_patterns['leading_trailing_spaces'].sub('', cleaned)
                cleaned = self.cleaning_patterns['multiple_spaces'].sub(' ', cleaned)
                return cleaned.strip()
            
            else:
                logger.warning(f"Unknown cleaning level: {cleaning_level}")
                return text.strip()
                
        except Exception as e:
            logger.error(f"Error cleaning text data: {str(e)}")
            return str(text)

    def clean_dict_data(self, data: Dict[str, Any], cleaning_level: str = 'standard') -> Dict[str, Any]:
        """Clean dictionary data recursively."""
        try:
            cleaned_data = {}
            
            for key, value in data.items():
                # Clean key
                cleaned_key = self.clean_text_data(str(key), cleaning_level)
                
                # Clean value
                if isinstance(value, str):
                    cleaned_value = self.clean_text_data(value, cleaning_level)
                elif isinstance(value, dict):
                    cleaned_value = self.clean_dict_data(value, cleaning_level)
                elif isinstance(value, list):
                    cleaned_value = [self.clean_text_data(str(item), cleaning_level) if isinstance(item, str) else item for item in value]
                else:
                    cleaned_value = value
                
                cleaned_data[cleaned_key] = cleaned_value
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Error cleaning dict data: {str(e)}")
            return data

    def enrich_data_with_metadata(self, data: Dict[str, Any], source: str = 'unknown') -> Dict[str, Any]:
        """Enrich data with metadata."""
        try:
            enriched_data = data.copy()
            
            # Add metadata
            enriched_data['_metadata'] = {
                'processed_at': datetime.utcnow().isoformat(),
                'source': source,
                'data_type': self._determine_data_type(data),
                'size': len(str(data)),
                'field_count': len(data) if isinstance(data, dict) else 0
            }
            
            return enriched_data
            
        except Exception as e:
            logger.error(f"Error enriching data with metadata: {str(e)}")
            return data

    def _determine_data_type(self, data: Any) -> str:
        """Determine the type of data."""
        try:
            if isinstance(data, dict):
                return 'object'
            elif isinstance(data, list):
                return 'array'
            elif isinstance(data, str):
                return 'string'
            elif isinstance(data, (int, float)):
                return 'number'
            elif isinstance(data, bool):
                return 'boolean'
            else:
                return 'unknown'
                
        except Exception as e:
            logger.error(f"Error determining data type: {str(e)}")
            return 'unknown'

    def validate_data_completeness(self, data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
        """Validate data completeness against required fields."""
        try:
            validation_result = {
                'is_complete': True,
                'missing_fields': [],
                'present_fields': [],
                'completeness_score': 0.0,
                'validation_timestamp': datetime.utcnow().isoformat()
            }
            
            present_count = 0
            for field in required_fields:
                if field in data and data[field] is not None and data[field] != '':
                    validation_result['present_fields'].append(field)
                    present_count += 1
                else:
                    validation_result['missing_fields'].append(field)
            
            # Calculate completeness score
            if required_fields:
                validation_result['completeness_score'] = present_count / len(required_fields)
                validation_result['is_complete'] = validation_result['completeness_score'] >= 0.8
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating data completeness: {str(e)}")
            return {
                'is_complete': False,
                'missing_fields': required_fields,
                'present_fields': [],
                'completeness_score': 0.0,
                'validation_timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }

    def normalize_field_values(self, data: Dict[str, Any], field_mappings: Dict[str, str]) -> Dict[str, Any]:
        """Normalize field values based on mappings."""
        try:
            normalized_data = {}
            
            for original_field, normalized_field in field_mappings.items():
                if original_field in data:
                    normalized_data[normalized_field] = data[original_field]
            
            return normalized_data
            
        except Exception as e:
            logger.error(f"Error normalizing field values: {str(e)}")
            return data

    def merge_data_sources(self, data_sources: List[Dict[str, Any]], merge_strategy: str = 'prefer_first') -> Dict[str, Any]:
        """Merge multiple data sources."""
        try:
            if not data_sources:
                return {}
            
            if len(data_sources) == 1:
                return data_sources[0]
            
            merged_data = {}
            
            if merge_strategy == 'prefer_first':
                # Prefer first non-empty value
                for source in data_sources:
                    for key, value in source.items():
                        if key not in merged_data or merged_data[key] is None or merged_data[key] == '':
                            merged_data[key] = value
            
            elif merge_strategy == 'prefer_last':
                # Prefer last non-empty value
                for source in data_sources:
                    for key, value in source.items():
                        if value is not None and value != '':
                            merged_data[key] = value
            
            elif merge_strategy == 'combine':
                # Combine all values
                for source in data_sources:
                    for key, value in source.items():
                        if key not in merged_data:
                            merged_data[key] = []
                        if isinstance(merged_data[key], list):
                            merged_data[key].append(value)
                        else:
                            merged_data[key] = [merged_data[key], value]
            
            elif merge_strategy == 'intersection':
                # Only include fields present in all sources
                common_keys = set(data_sources[0].keys())
                for source in data_sources[1:]:
                    common_keys = common_keys.intersection(set(source.keys()))
                
                for key in common_keys:
                    values = [source[key] for source in data_sources if key in source]
                    merged_data[key] = values[0] if values else None
            
            return merged_data
            
        except Exception as e:
            logger.error(f"Error merging data sources: {str(e)}")
            return data_sources[0] if data_sources else {}

    def filter_data_by_criteria(self, data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Filter data based on criteria."""
        try:
            filtered_data = {}
            
            for key, value in data.items():
                include_field = True
                
                # Check if field should be included based on criteria
                if 'include_fields' in criteria and key not in criteria['include_fields']:
                    include_field = False
                
                if 'exclude_fields' in criteria and key in criteria['exclude_fields']:
                    include_field = False
                
                # Check value-based criteria
                if 'min_length' in criteria and isinstance(value, str) and len(value) < criteria['min_length']:
                    include_field = False
                
                if 'max_length' in criteria and isinstance(value, str) and len(value) > criteria['max_length']:
                    include_field = False
                
                if 'required_values' in criteria and key in criteria['required_values']:
                    if value not in criteria['required_values'][key]:
                        include_field = False
                
                if include_field:
                    filtered_data[key] = value
            
            return filtered_data
            
        except Exception as e:
            logger.error(f"Error filtering data by criteria: {str(e)}")
            return data

    def format_data_for_output(self, data: Dict[str, Any], output_format: str = 'json') -> Union[str, Dict[str, Any]]:
        """Format data for different output formats."""
        try:
            if output_format == 'json':
                return json.dumps(data, indent=2, default=str)
            
            elif output_format == 'dict':
                return data
            
            elif output_format == 'csv':
                # Convert to CSV format (simplified)
                csv_lines = []
                if data:
                    # Headers
                    headers = list(data.keys())
                    csv_lines.append(','.join(headers))
                    
                    # Values
                    values = [str(data.get(header, '')) for header in headers]
                    csv_lines.append(','.join(values))
                
                return '\n'.join(csv_lines)
            
            elif output_format == 'xml':
                # Convert to XML format (simplified)
                xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<data>']
                
                for key, value in data.items():
                    xml_lines.append(f'  <{key}>{value}</{key}>')
                
                xml_lines.append('</data>')
                return '\n'.join(xml_lines)
            
            else:
                logger.warning(f"Unknown output format: {output_format}")
                return data
                
        except Exception as e:
            logger.error(f"Error formatting data for output: {str(e)}")
            return str(data)

    def validate_data_types(self, data: Dict[str, Any], type_schema: Dict[str, str]) -> Dict[str, Any]:
        """Validate data types against a schema."""
        try:
            validation_result = {
                'is_valid': True,
                'type_errors': [],
                'validation_timestamp': datetime.utcnow().isoformat()
            }
            
            for field, expected_type in type_schema.items():
                if field in data:
                    value = data[field]
                    actual_type = self._determine_data_type(value)
                    
                    if actual_type != expected_type:
                        validation_result['type_errors'].append({
                            'field': field,
                            'expected_type': expected_type,
                            'actual_type': actual_type,
                            'value': value
                        })
                        validation_result['is_valid'] = False
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating data types: {str(e)}")
            return {
                'is_valid': False,
                'type_errors': [{'error': str(e)}],
                'validation_timestamp': datetime.utcnow().isoformat()
            }

    def sanitize_sensitive_data(self, data: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
        """Sanitize sensitive data fields."""
        try:
            sanitized_data = data.copy()
            
            for field in sensitive_fields:
                if field in sanitized_data:
                    value = sanitized_data[field]
                    if isinstance(value, str) and len(value) > 4:
                        # Replace with asterisks, keeping first and last character
                        sanitized_data[field] = value[0] + '*' * (len(value) - 2) + value[-1]
                    else:
                        sanitized_data[field] = '***'
            
            return sanitized_data
            
        except Exception as e:
            logger.error(f"Error sanitizing sensitive data: {str(e)}")
            return data

    def calculate_data_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate statistics about the data."""
        try:
            stats = {
                'total_fields': len(data),
                'string_fields': 0,
                'numeric_fields': 0,
                'boolean_fields': 0,
                'object_fields': 0,
                'array_fields': 0,
                'null_fields': 0,
                'empty_fields': 0,
                'average_field_length': 0.0
            }
            
            total_length = 0
            field_count = 0
            
            for key, value in data.items():
                if value is None:
                    stats['null_fields'] += 1
                elif value == '':
                    stats['empty_fields'] += 1
                else:
                    data_type = self._determine_data_type(value)
                    if data_type == 'string':
                        stats['string_fields'] += 1
                        total_length += len(str(value))
                        field_count += 1
                    elif data_type == 'number':
                        stats['numeric_fields'] += 1
                    elif data_type == 'boolean':
                        stats['boolean_fields'] += 1
                    elif data_type == 'object':
                        stats['object_fields'] += 1
                    elif data_type == 'array':
                        stats['array_fields'] += 1
            
            if field_count > 0:
                stats['average_field_length'] = total_length / field_count
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating data statistics: {str(e)}")
            return {
                'error': str(e),
                'total_fields': 0
            } 