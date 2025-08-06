"""
Strategic Input Field Mappings
Definitions for the 30+ strategic input fields.
"""

# Define the 30+ strategic input fields
STRATEGIC_INPUT_FIELDS = {
    'business_context': [
        'business_objectives', 'target_metrics', 'content_budget', 'team_size',
        'implementation_timeline', 'market_share', 'competitive_position', 'performance_metrics'
    ],
    'audience_intelligence': [
        'content_preferences', 'consumption_patterns', 'audience_pain_points',
        'buying_journey', 'seasonal_trends', 'engagement_metrics'
    ],
    'competitive_intelligence': [
        'top_competitors', 'competitor_content_strategies', 'market_gaps',
        'industry_trends', 'emerging_trends'
    ],
    'content_strategy': [
        'preferred_formats', 'content_mix', 'content_frequency', 'optimal_timing',
        'quality_metrics', 'editorial_guidelines', 'brand_voice'
    ],
    'performance_analytics': [
        'traffic_sources', 'conversion_rates', 'content_roi_targets', 'ab_testing_capabilities'
    ]
}

# Field categories for organization
FIELD_CATEGORIES = {
    'business_context': {
        'name': 'Business Context',
        'description': 'Core business objectives and metrics',
        'fields': STRATEGIC_INPUT_FIELDS['business_context']
    },
    'audience_intelligence': {
        'name': 'Audience Intelligence',
        'description': 'Target audience analysis and insights',
        'fields': STRATEGIC_INPUT_FIELDS['audience_intelligence']
    },
    'competitive_intelligence': {
        'name': 'Competitive Intelligence',
        'description': 'Competitor analysis and market positioning',
        'fields': STRATEGIC_INPUT_FIELDS['competitive_intelligence']
    },
    'content_strategy': {
        'name': 'Content Strategy',
        'description': 'Content planning and execution',
        'fields': STRATEGIC_INPUT_FIELDS['content_strategy']
    },
    'performance_analytics': {
        'name': 'Performance & Analytics',
        'description': 'Performance tracking and optimization',
        'fields': STRATEGIC_INPUT_FIELDS['performance_analytics']
    }
} 