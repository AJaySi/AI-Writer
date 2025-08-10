import json
import logging
import traceback
from typing import Any, Dict

from services.ai_service_manager import AIServiceManager, AIServiceType

logger = logging.getLogger(__name__)

# Complete core fields - all 30+ fields that the frontend expects
CORE_FIELDS = [
    # Business Context (8 fields)
    'business_objectives', 'target_metrics', 'content_budget', 'team_size', 'implementation_timeline',
    'market_share', 'competitive_position', 'performance_metrics',
    
    # Audience Intelligence (6 fields)
    'content_preferences', 'consumption_patterns', 'audience_pain_points', 
    'buying_journey', 'seasonal_trends', 'engagement_metrics',
    
    # Competitive Intelligence (5 fields)
    'top_competitors', 'competitor_content_strategies', 'market_gaps', 'industry_trends', 'emerging_trends',
    
    # Content Strategy (7 fields)
    'preferred_formats', 'content_mix', 'content_frequency', 'optimal_timing',
    'quality_metrics', 'editorial_guidelines', 'brand_voice',
    
    # Performance & Analytics (4 fields)
    'traffic_sources', 'conversion_rates', 'content_roi_targets', 'ab_testing_capabilities'
]

JSON_FIELDS = {
    'business_objectives', 'target_metrics', 'content_preferences', 'consumption_patterns',
    'audience_pain_points', 'buying_journey', 'seasonal_trends', 'engagement_metrics',
    'competitor_content_strategies', 'market_gaps', 'industry_trends', 'emerging_trends',
    'content_mix', 'optimal_timing', 'quality_metrics', 'editorial_guidelines',
    'conversion_rates', 'content_roi_targets', 'performance_metrics'
}

ARRAY_FIELDS = {
    'preferred_formats', 'top_competitors', 'market_gaps', 'industry_trends', 'traffic_sources'
}

# Select field options mapping for value normalization
SELECT_FIELD_OPTIONS = {
    'implementation_timeline': ['3 months', '6 months', '1 year', '2 years', 'Ongoing'],
    'competitive_position': ['Leader', 'Challenger', 'Niche', 'Emerging'],
    'content_frequency': ['Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly'],
    'brand_voice': ['Professional', 'Casual', 'Friendly', 'Authoritative', 'Innovative']
}

class AIStructuredAutofillService:
    """Generate the complete Strategy Builder fields strictly from AI using onboarding context only."""

    def __init__(self) -> None:
        self.ai = AIServiceManager()
        self.max_retries = 2  # Maximum retry attempts for malformed JSON

    def _build_context_summary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        website = context.get('website_analysis') or {}
        research = context.get('research_preferences') or {}
        api_keys = context.get('api_keys_data') or {}
        session = context.get('onboarding_session') or {}
        summary = {
            'website_summary': {
                'website_url': website.get('website_url'),
                'industry': website.get('industry'),
                'content_types': website.get('content_types'),
                'target_audience': website.get('target_audience'),
                'performance_metrics': website.get('performance_metrics'),
                'seo_summary': website.get('seo_analysis')
            },
            'research_summary': {
                'audience_segments': research.get('audience_segments'),
                'content_preferences': research.get('content_preferences'),
                'consumption_patterns': research.get('consumption_patterns'),
                'seasonality': research.get('seasonal_trends')
            },
            'api_summary': {
                'providers': api_keys.get('providers'),
                'total_keys': api_keys.get('total_keys')
            },
            'session_summary': {
                'business_size': session.get('business_size'),
                'region': session.get('region')
            }
        }
        try:
            logger.debug(
                "AI Structured Autofill: context presence | website=%s research=%s api=%s session=%s",
                bool(website), bool(research), bool(api_keys), bool(session)
            )
            logger.debug(
                "AI Structured Autofill: website keys=%s research keys=%s",
                len(list(website.keys())) if hasattr(website, 'keys') else 0,
                len(list(research.keys())) if hasattr(research, 'keys') else 0,
            )
        except Exception:
            pass
        return summary

    def _build_schema(self) -> Dict[str, Any]:
        # Simplified schema following Gemini best practices
        # Reduce complexity by flattening nested structures and simplifying constraints
        properties: Dict[str, Any] = {}
        
        # Simplified field definitions - avoid complex constraints that cause 400 errors
        field_definitions = {
            # Core business fields (simplified)
            'business_objectives': {"type": "STRING", "description": "Business goals and objectives"},
            'target_metrics': {"type": "STRING", "description": "KPIs and success metrics"},
            'content_budget': {"type": "NUMBER", "description": "Monthly content budget in dollars"},
            'team_size': {"type": "NUMBER", "description": "Number of people in content team"},
            'implementation_timeline': {"type": "STRING", "description": "Strategy implementation timeline"},
            'market_share': {"type": "STRING", "description": "Current market share percentage"},
            'competitive_position': {"type": "STRING", "description": "Market competitive position"},
            'performance_metrics': {"type": "STRING", "description": "Current performance data"},
            
            # Audience fields (simplified)
            'content_preferences': {"type": "STRING", "description": "Content format and topic preferences"},
            'consumption_patterns': {"type": "STRING", "description": "When and how audience consumes content"},
            'audience_pain_points': {"type": "STRING", "description": "Key audience challenges and pain points"},
            'buying_journey': {"type": "STRING", "description": "Customer journey stages and touchpoints"},
            'seasonal_trends': {"type": "STRING", "description": "Seasonal content patterns and trends"},
            'engagement_metrics': {"type": "STRING", "description": "Current engagement data and metrics"},
            
            # Competitive fields (simplified)
            'top_competitors': {"type": "STRING", "description": "Main competitors"},
            'competitor_content_strategies': {"type": "STRING", "description": "Analysis of competitor content approaches"},
            'market_gaps': {"type": "STRING", "description": "Market opportunities and gaps"},
            'industry_trends': {"type": "STRING", "description": "Current industry trends"},
            'emerging_trends': {"type": "STRING", "description": "Upcoming trends and opportunities"},
            
            # Content strategy fields (simplified)
            'preferred_formats': {"type": "STRING", "description": "Preferred content formats"},
            'content_mix': {"type": "STRING", "description": "Content mix distribution"},
            'content_frequency': {"type": "STRING", "description": "Content publishing frequency"},
            'optimal_timing': {"type": "STRING", "description": "Best times for publishing content"},
            'quality_metrics': {"type": "STRING", "description": "Content quality standards and metrics"},
            'editorial_guidelines': {"type": "STRING", "description": "Style and tone guidelines"},
            'brand_voice': {"type": "STRING", "description": "Brand voice and tone"},
            
            # Performance fields (simplified)
            'traffic_sources': {"type": "STRING", "description": "Primary traffic sources"},
            'conversion_rates': {"type": "STRING", "description": "Target conversion rates and metrics"},
            'content_roi_targets': {"type": "STRING", "description": "ROI goals and targets for content"},
            'ab_testing_capabilities': {"type": "BOOLEAN", "description": "Whether A/B testing capabilities are available"}
        }
        
        # Build properties from field definitions
        for field_id in CORE_FIELDS:
            if field_id in field_definitions:
                properties[field_id] = field_definitions[field_id]
            else:
                # Fallback for any missing fields
                properties[field_id] = {"type": "STRING", "description": f"Value for {field_id}"}
        
        # Use propertyOrdering as recommended by Gemini docs for consistent output
        schema = {
            "type": "OBJECT",
            "properties": properties,
            "required": CORE_FIELDS,  # Make all fields required
            "propertyOrdering": CORE_FIELDS,  # Critical for consistent JSON output
            "description": "Content strategy fields with simplified constraints"
        }
        
        logger.debug("AI Structured Autofill: simplified schema built with %d properties and property ordering", len(CORE_FIELDS))
        return schema

    def _build_prompt(self, context_summary: Dict[str, Any]) -> str:
        # Ultra-simplified prompt to avoid JSON parsing issues
        prompt = (
            "Generate a JSON object with exactly 30 fields for content strategy. Use this exact format:\n\n"
            
            '{\n'
            '"business_objectives": "Increase traffic and leads",\n'
            '"target_metrics": "25% growth, 15% conversion",\n'
            '"content_budget": 3000,\n'
            '"team_size": 3,\n'
            '"implementation_timeline": "6 months",\n'
            '"market_share": "15%",\n'
            '"competitive_position": "Leader",\n'
            '"performance_metrics": "Current metrics data",\n'
            '"content_preferences": "Blog posts, videos",\n'
            '"consumption_patterns": "Peak hours 9-11 AM",\n'
            '"audience_pain_points": "Time constraints, complexity",\n'
            '"buying_journey": "Awareness to Decision",\n'
            '"seasonal_trends": "Q1 planning, Q2 execution",\n'
            '"engagement_metrics": "3.5% engagement rate",\n'
            '"top_competitors": "Competitor A, B, C",\n'
            '"competitor_content_strategies": "Educational content approach",\n'
            '"market_gaps": "AI tools, automation guides",\n'
            '"industry_trends": "AI integration, video content",\n'
            '"emerging_trends": "Voice search, interactive content",\n'
            '"preferred_formats": "Blog posts, videos, infographics",\n'
            '"content_mix": "70% educational, 30% promotional",\n'
            '"content_frequency": "Weekly",\n'
            '"optimal_timing": "Tuesday/Thursday 10 AM",\n'
            '"quality_metrics": "SEO score >90, engagement >3%",\n'
            '"editorial_guidelines": "Professional tone, actionable insights",\n'
            '"brand_voice": "Professional",\n'
            '"traffic_sources": "Organic search, social media",\n'
            '"conversion_rates": "15% conversion, $200 CPA",\n'
            '"content_roi_targets": "15% conversion, 3:1 ROI",\n'
            '"ab_testing_capabilities": true\n'
            '}\n\n'
            
            f"Business context: {json.dumps(context_summary, indent=2)}\n\n"
            "Generate the complete JSON with all 30 fields:"
        )
        logger.debug("AI Structured Autofill: ultra-simplified prompt (%d chars)", len(prompt))
        return prompt

    def _normalize_value(self, key: str, value: Any) -> Any:
        if value is None:
            return None
            
        # Handle numeric fields that might come as text
        if key in ['content_budget', 'team_size']:
            if isinstance(value, (int, float)):
                return value
            elif isinstance(value, str):
                # Extract numeric value from text
                import re
                # Remove currency symbols, commas, and common words
                cleaned = re.sub(r'[$,€£¥]', '', value.lower())
                cleaned = re.sub(r'\b(monthly|yearly|annual|people|person|specialist|creator|writer|editor|team|member)\b', '', cleaned)
                cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                
                # Extract first number found
                numbers = re.findall(r'\d+(?:\.\d+)?', cleaned)
                if numbers:
                    try:
                        num_value = float(numbers[0])
                        # For team_size, convert to integer
                        if key == 'team_size':
                            return int(num_value)
                        return num_value
                    except (ValueError, TypeError):
                        pass
                
                logger.warning(f"Could not extract numeric value from '{key}' field: '{value}'")
                return None
        
        # Handle boolean fields
        if key == 'ab_testing_capabilities':
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                normalized_value = value.lower().strip()
                if normalized_value in ['true', 'yes', 'available', 'enabled', '1']:
                    return True
                elif normalized_value in ['false', 'no', 'unavailable', 'disabled', '0']:
                    return False
                logger.warning(f"Could not parse boolean value for '{key}': '{value}'")
                return None
        
        # Handle select fields with predefined options
        if key in SELECT_FIELD_OPTIONS:
            if isinstance(value, str):
                # Try exact match first (case-insensitive)
                normalized_value = value.lower().strip()
                for option in SELECT_FIELD_OPTIONS[key]:
                    if normalized_value == option.lower():
                        return option
                
                # Try partial matching for common variations
                for option in SELECT_FIELD_OPTIONS[key]:
                    option_lower = option.lower()
                    # Handle common variations
                    if (normalized_value.startswith(option_lower) or 
                        option_lower in normalized_value or
                        normalized_value.endswith(option_lower)):
                        return option
                
                # Special handling for content_frequency
                if key == 'content_frequency':
                    if 'daily' in normalized_value:
                        return 'Daily'
                    elif 'weekly' in normalized_value or 'week' in normalized_value:
                        return 'Weekly'
                    elif 'bi-weekly' in normalized_value or 'biweekly' in normalized_value:
                        return 'Bi-weekly'
                    elif 'monthly' in normalized_value or 'month' in normalized_value:
                        return 'Monthly'
                    elif 'quarterly' in normalized_value or 'quarter' in normalized_value:
                        return 'Quarterly'
                
                # If no match found, return the first option as fallback
                logger.warning(f"Could not normalize select field '{key}' value: '{value}' to valid options: {SELECT_FIELD_OPTIONS[key]}")
                return SELECT_FIELD_OPTIONS[key][0]  # Return first option as fallback
        
        # For all other fields, ensure they're strings and not empty
        if isinstance(value, str):
            # Special handling for multiselect fields
            if key in ['preferred_formats', 'top_competitors', 'market_gaps', 'industry_trends', 'traffic_sources']:
                # Split by comma and clean up each item
                items = [item.strip() for item in value.split(',') if item.strip()]
                if items:
                    return items  # Return as array for multiselect fields
                return None
            return value.strip() if value.strip() else None
        elif isinstance(value, (int, float, bool)):
            return str(value)
        elif isinstance(value, list):
            # For multiselect fields, return the list as-is
            if key in ['preferred_formats', 'top_competitors', 'market_gaps', 'industry_trends', 'traffic_sources']:
                return [str(item) for item in value if item]
            # For other fields, convert arrays to comma-separated strings
            return ', '.join(str(item) for item in value if item)
        else:
            return str(value) if value else None

    def _calculate_success_rate(self, result: Dict[str, Any]) -> float:
        """Calculate the percentage of successfully filled fields."""
        if not isinstance(result, dict):
            return 0.0
        
        filled_fields = 0
        for key in CORE_FIELDS:
            value = result.get(key)
            if value is not None and value != "" and value != []:
                # Additional checks for different data types
                if isinstance(value, str) and value.strip():
                    filled_fields += 1
                elif isinstance(value, (int, float)) and value != 0:
                    filled_fields += 1
                elif isinstance(value, bool):
                    filled_fields += 1
                elif isinstance(value, list) and len(value) > 0:
                    filled_fields += 1
                elif value is not None and value != "":
                    filled_fields += 1
        
        return (filled_fields / len(CORE_FIELDS)) * 100

    def _should_retry(self, result: Dict[str, Any], attempt: int) -> bool:
        """Determine if we should retry based on success rate and attempt count."""
        if attempt >= self.max_retries:
            return False
        
        # Check if result has error
        if 'error' in result:
            logger.info(f"Retry attempt {attempt + 1} due to error: {result.get('error')}")
            return True
        
        # Check success rate - stop immediately if we have 100% success
        success_rate = self._calculate_success_rate(result)
        logger.info(f"Success rate: {success_rate:.1f}% (attempt {attempt + 1})")
        
        # If we have 100% success, don't retry
        if success_rate >= 100.0:
            logger.info(f"Perfect success rate achieved: {success_rate:.1f}% - no retry needed")
            return False
        
        # Retry if success rate is below 80% (more aggressive than 50%)
        if success_rate < 80.0:
            logger.info(f"Retry attempt {attempt + 1} due to low success rate: {success_rate:.1f}% (need 80%+)")
            return True
        
        # Also retry if we're missing more than 6 fields (20% of 30 fields)
        missing_count = len([k for k in CORE_FIELDS if not result.get(k) or result.get(k) == "" or result.get(k) == []])
        if missing_count > 6:
            logger.info(f"Retry attempt {attempt + 1} due to too many missing fields: {missing_count} missing (max 6)")
            return True
        
        return False

    async def generate_autofill_fields(self, user_id: int, context: Dict[str, Any]) -> Dict[str, Any]:
        context_summary = self._build_context_summary(context)
        schema = self._build_schema()
        prompt = self._build_prompt(context_summary)

        logger.info("AIStructuredAutofillService: generating %d fields | user=%s", len(CORE_FIELDS), user_id)
        logger.debug("AIStructuredAutofillService: properties=%d", len(schema.get('properties', {})))
        
        last_result = None
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"AI structured call attempt {attempt + 1}/{self.max_retries + 1}")
                result = await self.ai.execute_structured_json_call(
                    service_type=AIServiceType.STRATEGIC_INTELLIGENCE,
                    prompt=prompt,
                    schema=schema
                )
                last_result = result
                
                # Check if we should retry
                if not self._should_retry(result, attempt):
                    break
                    
                # Add a small delay before retry
                if attempt < self.max_retries:
                    import asyncio
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"AI structured call failed (attempt {attempt + 1}) | user=%s | err=%s", user_id, repr(e))
                logger.error("Traceback:\n%s", traceback.format_exc())
                last_result = {
                    'error': str(e)
                }
                if attempt < self.max_retries:
                    import asyncio
                    await asyncio.sleep(1)
                    continue
                break

        # Process the final result
        if not isinstance(last_result, dict):
            logger.warning("AI did not return a structured JSON object, got: %s", type(last_result))
            return {
                'fields': {},
                'sources': {},
                'meta': {
                    'ai_used': False,
                    'ai_overrides_count': 0,
                    'missing_fields': CORE_FIELDS,
                    'error': f"AI returned {type(last_result)} instead of dict",
                    'attempts': self.max_retries + 1
                }
            }

        # Check if AI returned an error
        if 'error' in last_result:
            logger.warning("AI returned error after all attempts: %s", last_result.get('error'))
            return {
                'fields': {},
                'sources': {},
                'meta': {
                    'ai_used': False,
                    'ai_overrides_count': 0,
                    'missing_fields': CORE_FIELDS,
                    'error': last_result.get('error', 'Unknown AI error'),
                    'attempts': self.max_retries + 1
                }
            }

        # Try to extract fields from malformed JSON if needed
        if len(last_result) < len(CORE_FIELDS) * 0.5:  # If we got less than 50% of fields
            logger.warning("AI returned incomplete result, attempting to extract from raw response")
            # Try to extract key-value pairs from the raw response
            extracted_result = self._extract_fields_from_raw_response(last_result)
            if extracted_result and len(extracted_result) > len(last_result):
                logger.info("Successfully extracted additional fields from raw response")
                last_result = extracted_result

        try:
            logger.debug("AI structured result keys=%d | sample keys=%s", len(list(last_result.keys())), list(last_result.keys())[:8])
        except Exception:
            pass

        # Build UI fields map using only non-null normalized values
        fields: Dict[str, Any] = {}
        sources: Dict[str, str] = {}
        non_null_keys = []
        missing_fields = []
        
        for key in CORE_FIELDS:
            raw_value = last_result.get(key)
            norm_value = self._normalize_value(key, raw_value)
            if norm_value is not None and norm_value != "" and norm_value != []:
                fields[key] = { 'value': norm_value, 'source': 'ai_refresh', 'confidence': 0.8 }
                sources[key] = 'ai_refresh'
                non_null_keys.append(key)
            else:
                missing_fields.append(key)
        
        # Log detailed field analysis
        logger.info("AI structured autofill field analysis:")
        logger.info("✅ Generated fields (%d): %s", len(non_null_keys), non_null_keys)
        logger.info("❌ Missing fields (%d): %s", len(missing_fields), missing_fields)
        
        # Categorize missing fields
        field_categories = {
            'business_context': ['business_objectives', 'target_metrics', 'content_budget', 'team_size', 'implementation_timeline', 'market_share', 'competitive_position', 'performance_metrics'],
            'audience_intelligence': ['content_preferences', 'consumption_patterns', 'audience_pain_points', 'buying_journey', 'seasonal_trends', 'engagement_metrics'],
            'competitive_intelligence': ['top_competitors', 'competitor_content_strategies', 'market_gaps', 'industry_trends', 'emerging_trends'],
            'content_strategy': ['preferred_formats', 'content_mix', 'content_frequency', 'optimal_timing', 'quality_metrics', 'editorial_guidelines', 'brand_voice'],
            'performance_analytics': ['traffic_sources', 'conversion_rates', 'content_roi_targets', 'ab_testing_capabilities']
        }
        
        for category, category_fields in field_categories.items():
            generated_in_category = [f for f in category_fields if f in non_null_keys]
            missing_in_category = [f for f in category_fields if f in missing_fields]
            logger.info("📊 %s: %d/%d fields generated (%s missing: %s)", 
                       category.upper(), len(generated_in_category), len(category_fields), 
                       len(missing_in_category), missing_in_category)
        
        success_rate = self._calculate_success_rate(last_result)

        payload = {
            'fields': fields,
            'sources': sources,
            'meta': {
                'ai_used': len(non_null_keys) > 0,
                'ai_overrides_count': len(non_null_keys),
                'ai_override_fields': non_null_keys,
                'ai_only': True,
                'missing_fields': missing_fields,
                'success_rate': success_rate,
                'attempts': self.max_retries + 1
            }
        }
        logger.info("AI structured autofill completed | non_null_fields=%d missing=%d success_rate=%.1f%% attempts=%d", 
                   len(non_null_keys), len(missing_fields), success_rate, self.max_retries + 1)
        return payload

    def _extract_fields_from_raw_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract fields from malformed JSON response using regex patterns."""
        import re
        
        # Convert result to string for pattern matching
        result_str = str(result)
        
        extracted = {}
        
        # Pattern to match key-value pairs in JSON-like format
        patterns = [
            r'"([^"]+)":\s*"([^"]*)"',  # String values
            r'"([^"]+)":\s*(\d+(?:\.\d+)?)',  # Numeric values
            r'"([^"]+)":\s*(true|false)',  # Boolean values
            r'"([^"]+)":\s*\[([^\]]*)\]',  # Array values
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, result_str)
            for key, value in matches:
                if key in CORE_FIELDS:
                    # Clean up the value
                    if value.lower() in ['true', 'false']:
                        extracted[key] = value.lower() == 'true'
                    elif value.replace('.', '').isdigit():
                        extracted[key] = float(value) if '.' in value else int(value)
                    else:
                        extracted[key] = value.strip('"')
        
        logger.info("Extracted %d fields from raw response: %s", len(extracted), list(extracted.keys()))
        return extracted 