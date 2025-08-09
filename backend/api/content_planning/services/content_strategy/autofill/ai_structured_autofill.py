import json
import logging
import traceback
from typing import Any, Dict

from services.ai_service_manager import AIServiceManager, AIServiceType

logger = logging.getLogger(__name__)

CORE_FIELDS = [
    'business_objectives','target_metrics','content_budget','team_size','implementation_timeline',
    'market_share','competitive_position','performance_metrics','content_preferences','consumption_patterns',
    'audience_pain_points','buying_journey','seasonal_trends','engagement_metrics','top_competitors',
    'competitor_content_strategies','market_gaps','industry_trends','emerging_trends','preferred_formats',
    'content_mix','content_frequency','optimal_timing','quality_metrics','editorial_guidelines','brand_voice',
    'traffic_sources','conversion_rates','content_roi_targets','ab_testing_capabilities'
]

JSON_FIELDS = {
    'business_objectives', 'target_metrics', 'content_preferences'
}
ARRAY_FIELDS = {
    'preferred_formats'
}

class AIStructuredAutofillService:
    """Generate the complete 30+ Strategy Builder fields strictly from AI using onboarding context only."""

    def __init__(self) -> None:
        self.ai = AIServiceManager()

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
        # Build a Gemini SDK-compatible Schema (dict equivalent), not JSON Schema.
        # Avoid unsupported keys like oneOf/additionalProperties.
        properties: Dict[str, Any] = {}
        typed_overrides: Dict[str, Any] = {
            # Use STRING for complex JSON-bearing fields to avoid OBJECT property constraints
            'business_objectives': {"type": "STRING"},
            'target_metrics': {"type": "STRING"},
            'content_preferences': {"type": "STRING"},
            # Known arrays
            'preferred_formats': {"type": "ARRAY", "items": {"type": "STRING"}},
            # Known selects
            'content_frequency': {"type": "STRING"},
        }
        for key in CORE_FIELDS:
            properties[key] = typed_overrides.get(key, {"type": "STRING"})
        schema = {
            "type": "OBJECT",
            "properties": properties,
            # Property ordering can help response consistency per Gemini docs
            "propertyOrdering": CORE_FIELDS,
        }
        logger.debug("AI Structured Autofill: schema built (SDK) with %d properties", len(CORE_FIELDS))
        return schema

    def _build_prompt(self, context_summary: Dict[str, Any]) -> str:
        prompt = (
            "You are a senior content strategy system. Using ONLY the provided context (do not copy raw\n"
            "values), infer professional, actionable values for ALL of the following 30+ strategy fields.\n"
            "Output strictly valid JSON matching the given schema. Provide concise, business-ready values.\n"
            "If you are uncertain, infer the most reasonable assumption for a small business. Do not leave\n"
            "fields empty.\n\n"
            f"CONTEXT:\n{json.dumps(context_summary, indent=2)}\n\n"
            "FIELDS TO PRODUCE (keys only; values inferred):\n"
            f"{CORE_FIELDS}\n"
        )
        logger.debug("AI Structured Autofill: prompt preview=%d chars", len(prompt))
        return prompt

    def _normalize_value(self, key: str, value: Any) -> Any:
        if value is None:
            return None
        # Parse JSON-bearing fields if they arrived as JSON strings
        if key in JSON_FIELDS:
            if isinstance(value, str):
                try:
                    return json.loads(value)
                except Exception:
                    # Keep as string if not valid JSON
                    return value
            return value
        # Coerce arrays from comma-separated strings where applicable
        if key in ARRAY_FIELDS:
            if isinstance(value, str):
                split = [s.strip() for s in value.split(',') if s.strip()]
                return split if split else None
            if isinstance(value, list):
                return [str(v) for v in value]
            return None
        return value

    async def generate_autofill_fields(self, user_id: int, context: Dict[str, Any]) -> Dict[str, Any]:
        context_summary = self._build_context_summary(context)
        schema = self._build_schema()
        prompt = self._build_prompt(context_summary)

        logger.info("AIStructuredAutofillService: generating 30+ fields | user=%s", user_id)
        logger.debug("AIStructuredAutofillService: properties=%d", len(schema.get('properties', {})))
        try:
            result = await self.ai.execute_structured_json_call(
                service_type=AIServiceType.STRATEGIC_INTELLIGENCE,
                prompt=prompt,
                schema=schema
            )
        except Exception as e:
            logger.error("AI structured call failed | user=%s | err=%s", user_id, repr(e))
            logger.error("Traceback:\n%s", traceback.format_exc())
            raise

        if not isinstance(result, dict):
            raise ValueError("AI did not return a structured JSON object")

        try:
            logger.debug("AI structured result keys=%d | sample keys=%s", len(list(result.keys())), list(result.keys())[:8])
        except Exception:
            pass

        # Build UI fields map using only non-null normalized values
        fields: Dict[str, Any] = {}
        sources: Dict[str, str] = {}
        non_null_keys = []
        for key in CORE_FIELDS:
            raw_value = result.get(key)
            norm_value = self._normalize_value(key, raw_value)
            if norm_value is not None and norm_value != "" and norm_value != []:
                fields[key] = { 'value': norm_value, 'source': 'ai_refresh', 'confidence': 0.8 }
                sources[key] = 'ai_refresh'
                non_null_keys.append(key)
        missing_fields = [k for k in CORE_FIELDS if k not in non_null_keys]

        payload = {
            'fields': fields,
            'sources': sources,
            'meta': {
                'ai_used': len(non_null_keys) > 0,
                'ai_overrides_count': len(non_null_keys),
                'ai_override_fields': non_null_keys,
                'ai_only': True,
                'missing_fields': missing_fields
            }
        }
        logger.info("AI structured autofill completed | non_null_fields=%d missing=%d", len(non_null_keys), len(missing_fields))
        return payload 