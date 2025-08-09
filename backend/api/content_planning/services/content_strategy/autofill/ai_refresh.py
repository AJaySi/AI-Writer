from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
import logging
import traceback

from .autofill_service import AutoFillService
from ...ai_analytics_service import ContentPlanningAIAnalyticsService
from .ai_structured_autofill import AIStructuredAutofillService

logger = logging.getLogger(__name__)

class AutoFillRefreshService:
    """Generates a fresh auto-fill payload for the Strategy Builder.
    This service does NOT persist anything. Intended for refresh flows.
    """

    def __init__(self, db: Session):
        self.db = db
        self.autofill = AutoFillService(db)
        self.ai_analytics = ContentPlanningAIAnalyticsService()
        self.structured_ai = AIStructuredAutofillService()

    async def build_fresh_payload(self, user_id: int, use_ai: bool = True, ai_only: bool = False) -> Dict[str, Any]:
        """Build a fresh auto-fill payload.
        - Reads latest onboarding-integrated data
        - Optionally augments with AI overrides (hook, not persisted)
        - Returns payload in the same shape as AutoFillService.get_autofill, plus meta
        """
        # Base context from onboarding analysis (used for AI context only when ai_only)
        logger.debug("AutoFillRefreshService: processing onboarding context | user=%s", user_id)
        base_context = await self.autofill.integration.process_onboarding_data(user_id, self.db)
        logger.debug(
            "AutoFillRefreshService: context keys=%s | website=%s research=%s api=%s session=%s",
            list(base_context.keys()) if isinstance(base_context, dict) else 'n/a',
            bool((base_context or {}).get('website_analysis')),
            bool((base_context or {}).get('research_preferences')),
            bool((base_context or {}).get('api_keys_data')),
            bool((base_context or {}).get('onboarding_session')),
        )
        try:
            w = (base_context or {}).get('website_analysis') or {}
            r = (base_context or {}).get('research_preferences') or {}
            logger.debug("AutoFillRefreshService: website keys=%s | research keys=%s", len(list(w.keys())) if hasattr(w,'keys') else 0, len(list(r.keys())) if hasattr(r,'keys') else 0)
        except Exception:
            pass

        if ai_only and use_ai:
            logger.info("AutoFillRefreshService: AI-only refresh enabled; generating full 30+ fields via AI")
            try:
                ai_payload = await self.structured_ai.generate_autofill_fields(user_id, base_context)
                meta = ai_payload.get('meta') or {}
                logger.info("AI-only payload meta: ai_used=%s overrides=%s", meta.get('ai_used'), meta.get('ai_overrides_count'))
                return ai_payload
            except Exception as e:
                logger.error("AI-only structured generation failed | user=%s | err=%s", user_id, repr(e))
                logger.error("Traceback:\n%s", traceback.format_exc())
                raise

        # Fallback to previous behavior (DB + sparse overrides)
        payload = await self.autofill.get_autofill(user_id)
        logger.info("AutoFillRefreshService: Base payload fields: %d", len(payload.get('fields', {})))

        ai_overrides: Dict[str, Any] = {}
        if use_ai:
            # Hook to integrate AI-generated overrides for certain fields, if available
            ai_overrides = await self._generate_ai_overrides(user_id, payload)
            if ai_overrides:
                logger.debug("AutoFillRefreshService: merging %d AI overrides", len(ai_overrides))
                # Merge AI overrides into fields while preserving sources/transparency
                fields = payload.get('fields', {})
                for key, override_value in ai_overrides.items():
                    if key in fields and isinstance(fields[key], dict):
                        fields[key]['value'] = override_value
                    else:
                        fields[key] = {'value': override_value, 'source': 'ai_refresh', 'confidence': 0.8}
                payload['fields'] = fields

                # Label sources for overridden fields as coming from AI refresh (non-persistent)
                sources = payload.get('sources', {})
                for key in ai_overrides.keys():
                    sources[key] = 'ai_refresh'
                payload['sources'] = sources

        # If ai_only requested, we still keep onboarding values where AI is silent (fallback), but we track AI usage
        overridden_keys = list(ai_overrides.keys())
        payload['meta'] = {
            'ai_used': len(overridden_keys) > 0,
            'ai_overrides_count': len(overridden_keys),
            'ai_override_fields': overridden_keys,
            'ai_only': ai_only,
        }

        logger.info("AutoFillRefreshService: Applied AI overrides for %d fields: %s", len(ai_overrides), overridden_keys)
        return payload

    async def _generate_ai_overrides(self, user_id: int, base_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Produce AI overrides for selected fields based on current context.
        Calls AI analytics with force refresh to avoid stale DB values.
        Logs raw AI response and mapped overrides for transparency.
        """
        try:
            logger.info(f"AutoFillRefreshService: Invoking AI analytics for user {user_id} with force refresh")
            ai_resp = await self.ai_analytics.get_ai_analytics(user_id=user_id, strategy_id=None, force_refresh=True)  # type: ignore
            # Log high-level response structure
            if isinstance(ai_resp, dict):
                keys = list(ai_resp.keys())
                logger.info(f"AI analytics response keys: {keys}")
                # Optionally log truncated insights/recommendations
                insights = ai_resp.get('insights')
                recs = ai_resp.get('recommendations')
                if insights is not None:
                    logger.info(f"AI insights count: {len(insights) if hasattr(insights, '__len__') else 'n/a'}")
                if recs is not None:
                    logger.info(f"AI recommendations count: {len(recs) if hasattr(recs, '__len__') else 'n/a'}")
            else:
                logger.warning("AI analytics response is not a dict; skipping mapping")
                return {}

            # Minimal, conservative mapping attempt (only if safely found)
            overrides: Dict[str, Any] = {}
            # Example: try to map preferred_formats from recommendations if present
            try:
                recs = ai_resp.get('recommendations') or {}
                if isinstance(recs, dict):
                    pf = recs.get('preferred_formats')
                    if pf:
                        overrides['preferred_formats'] = pf
                # Example: target_metrics from insights/metrics if present
                insights = ai_resp.get('insights') or {}
                if isinstance(insights, dict):
                    tm = insights.get('target_metrics') or insights.get('kpi_targets')
                    if tm:
                        overrides['target_metrics'] = tm
            except Exception as map_err:
                logger.warning(f"AI override mapping encountered an issue: {map_err}")

            logger.info(f"AI override mapping produced {len(overrides)} fields: {list(overrides.keys())}")
            return overrides
        except Exception as e:
            logger.error(f"AI override generation failed: {e}")
            return {} 