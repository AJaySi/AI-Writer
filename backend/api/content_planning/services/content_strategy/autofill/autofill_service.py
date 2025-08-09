from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from ..onboarding.data_integration import OnboardingDataIntegrationService

# Local module imports (to be created in this batch)
from .normalizers.website_normalizer import normalize_website_analysis
from .normalizers.research_normalizer import normalize_research_preferences
from .normalizers.api_keys_normalizer import normalize_api_keys
from .transformer import transform_to_fields
from .quality import calculate_quality_scores_from_raw, calculate_confidence_from_raw, calculate_data_freshness
from .transparency import build_data_sources_map, build_input_data_points
from .schema import validate_output


class AutoFillService:
    """Facade for building Content Strategy auto-fill payload."""

    def __init__(self, db: Session):
        self.db = db
        self.integration = OnboardingDataIntegrationService()

    async def get_autofill(self, user_id: int) -> Dict[str, Any]:
        # 1) Collect raw integration data
        integrated = await self.integration.process_onboarding_data(user_id, self.db)
        if not integrated:
            raise RuntimeError("No onboarding data available for user")

        website_raw = integrated.get('website_analysis', {})
        research_raw = integrated.get('research_preferences', {})
        api_raw = integrated.get('api_keys_data', {})
        session_raw = integrated.get('onboarding_session', {})

        # 2) Normalize raw sources
        website = await normalize_website_analysis(website_raw)
        research = await normalize_research_preferences(research_raw)
        api_keys = await normalize_api_keys(api_raw)

        # 3) Quality/confidence/freshness (computed from raw, but returned as meta)
        quality_scores = calculate_quality_scores_from_raw({
            'website_analysis': website_raw,
            'research_preferences': research_raw,
            'api_keys_data': api_raw,
        })
        confidence_levels = calculate_confidence_from_raw({
            'website_analysis': website_raw,
            'research_preferences': research_raw,
            'api_keys_data': api_raw,
        })
        data_freshness = calculate_data_freshness(session_raw)

        # 4) Transform to frontend field map
        fields = transform_to_fields(
            website=website,
            research=research,
            api_keys=api_keys,
            session=session_raw,
        )

        # 5) Transparency maps
        sources = build_data_sources_map(website, research, api_keys)
        input_data_points = build_input_data_points(
            website_raw=website_raw,
            research_raw=research_raw,
            api_raw=api_raw,
        )

        payload = {
            'fields': fields,
            'sources': sources,
            'quality_scores': quality_scores,
            'confidence_levels': confidence_levels,
            'data_freshness': data_freshness,
            'input_data_points': input_data_points,
        }

        # Validate structure strictly
        validate_output(payload)
        return payload 