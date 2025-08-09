from typing import Any, Dict

async def normalize_research_preferences(research_data: Dict[str, Any]) -> Dict[str, Any]:
    if not research_data:
        return {}

    return {
        'content_preferences': {
            'preferred_formats': research_data.get('content_types', []),
            'content_topics': research_data.get('research_topics', []),
            'content_style': research_data.get('writing_style', {}).get('tone', []),
            'content_length': 'Medium (1000-2000 words)',
            'visual_preferences': ['Infographics', 'Charts', 'Diagrams'],
        },
        'audience_intelligence': {
            'target_audience': research_data.get('target_audience', {}).get('demographics', []),
            'pain_points': research_data.get('target_audience', {}).get('pain_points', []),
            'buying_journey': research_data.get('target_audience', {}).get('buying_journey', {}),
            'consumption_patterns': research_data.get('target_audience', {}).get('consumption_patterns', {}),
        },
        'research_goals': {
            'primary_goals': research_data.get('research_topics', []),
            'secondary_goals': research_data.get('content_types', []),
            'success_metrics': ['Website traffic', 'Lead quality', 'Engagement rates'],
        },
        'data_quality': research_data.get('data_quality'),
        'confidence_level': research_data.get('confidence_level', 0.8),
        'data_freshness': research_data.get('data_freshness', 0.8),
    } 