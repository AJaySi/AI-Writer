"""
Service Constants for Content Strategy
Configuration and settings for the enhanced strategy service.
"""

# Performance optimization settings
PROMPT_VERSIONS = {
    'comprehensive_strategy': 'v2.1',
    'audience_intelligence': 'v2.0',
    'competitive_intelligence': 'v2.0',
    'performance_optimization': 'v2.1',
    'content_calendar_optimization': 'v2.0'
}

QUALITY_THRESHOLDS = {
    'min_confidence': 0.7,
    'min_completeness': 0.8,
    'max_response_time': 30.0  # seconds
}

CACHE_SETTINGS = {
    'ai_analysis_cache_ttl': 3600,  # 1 hour
    'onboarding_data_cache_ttl': 1800,  # 30 minutes
    'strategy_cache_ttl': 7200,  # 2 hours
    'max_cache_size': 1000  # Maximum cached items
}

# Service constants
SERVICE_CONSTANTS = {
    'prompt_versions': PROMPT_VERSIONS,
    'quality_thresholds': QUALITY_THRESHOLDS,
    'cache_settings': CACHE_SETTINGS
} 