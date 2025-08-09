from typing import Any, Dict
from datetime import datetime


def calculate_quality_scores_from_raw(data_sources: Dict[str, Any]) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for source, data in data_sources.items():
        if isinstance(data, dict) and data:
            total = len(data)
            non_null = len([v for v in data.values() if v is not None])
            scores[source] = (non_null / total) * 100 if total else 0.0
        else:
            scores[source] = 0.0
    return scores


def calculate_confidence_from_raw(data_sources: Dict[str, Any]) -> Dict[str, float]:
    levels: Dict[str, float] = {}
    if data_sources.get('website_analysis'):
        levels['website_analysis'] = data_sources['website_analysis'].get('confidence_level', 0.8)
    if data_sources.get('research_preferences'):
        levels['research_preferences'] = data_sources['research_preferences'].get('confidence_level', 0.7)
    if data_sources.get('api_keys_data'):
        levels['api_keys_data'] = data_sources['api_keys_data'].get('confidence_level', 0.6)
    return levels


def calculate_data_freshness(onboarding_session: Any) -> Dict[str, Any]:
    try:
        updated_at = None
        if hasattr(onboarding_session, 'updated_at'):
            updated_at = onboarding_session.updated_at
        elif isinstance(onboarding_session, dict):
            updated_at = onboarding_session.get('last_updated') or onboarding_session.get('updated_at')

        if not updated_at:
            return {'status': 'unknown', 'age_days': 'unknown'}

        if isinstance(updated_at, str):
            try:
                updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            except ValueError:
                return {'status': 'unknown', 'age_days': 'unknown'}

        age_days = (datetime.utcnow() - updated_at).days
        if age_days <= 7:
            status = 'fresh'
        elif age_days <= 30:
            status = 'recent'
        elif age_days <= 90:
            status = 'aging'
        else:
            status = 'stale'

        return {
            'status': status,
            'age_days': age_days,
            'last_updated': updated_at.isoformat() if hasattr(updated_at, 'isoformat') else str(updated_at)
        }
    except Exception:
        return {'status': 'unknown', 'age_days': 'unknown'} 