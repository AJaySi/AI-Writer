from typing import Any, Dict


def build_data_sources_map(website: Dict[str, Any], research: Dict[str, Any], api_keys: Dict[str, Any]) -> Dict[str, str]:
    sources: Dict[str, str] = {}

    website_fields = ['business_objectives', 'target_metrics', 'content_budget', 'team_size',
                      'implementation_timeline', 'market_share', 'competitive_position',
                      'performance_metrics', 'engagement_metrics', 'top_competitors',
                      'competitor_content_strategies', 'market_gaps', 'industry_trends',
                      'emerging_trends', 'traffic_sources', 'conversion_rates', 'content_roi_targets']

    research_fields = ['content_preferences', 'consumption_patterns', 'audience_pain_points',
                       'buying_journey', 'seasonal_trends', 'preferred_formats', 'content_mix',
                       'content_frequency', 'optimal_timing', 'quality_metrics', 'editorial_guidelines',
                       'brand_voice']

    api_fields = ['ab_testing_capabilities']

    for f in website_fields:
        sources[f] = 'website_analysis'
    for f in research_fields:
        sources[f] = 'research_preferences'
    for f in api_fields:
        sources[f] = 'api_keys_data'

    return sources


def build_input_data_points(*, website_raw: Dict[str, Any], research_raw: Dict[str, Any], api_raw: Dict[str, Any]) -> Dict[str, Any]:
    input_data_points: Dict[str, Any] = {}

    if website_raw:
        input_data_points['business_objectives'] = {
            'website_content': website_raw.get('content_goals', 'Not available'),
            'meta_description': website_raw.get('meta_description', 'Not available'),
            'about_page': website_raw.get('about_page_content', 'Not available'),
            'page_title': website_raw.get('page_title', 'Not available'),
            'content_analysis': website_raw.get('content_analysis', {})
        }

    if research_raw:
        input_data_points['target_metrics'] = {
            'research_preferences': research_raw.get('target_audience', 'Not available'),
            'industry_benchmarks': research_raw.get('industry_benchmarks', 'Not available'),
            'competitor_analysis': research_raw.get('competitor_analysis', 'Not available'),
            'market_research': research_raw.get('market_research', 'Not available')
        }

    if research_raw:
        input_data_points['content_preferences'] = {
            'user_preferences': research_raw.get('content_types', 'Not available'),
            'industry_trends': research_raw.get('industry_trends', 'Not available'),
            'consumption_patterns': research_raw.get('consumption_patterns', 'Not available'),
            'audience_research': research_raw.get('audience_research', 'Not available')
        }

    if website_raw or research_raw:
        input_data_points['preferred_formats'] = {
            'existing_content': website_raw.get('existing_content_types', 'Not available') if website_raw else 'Not available',
            'engagement_metrics': website_raw.get('engagement_metrics', 'Not available') if website_raw else 'Not available',
            'platform_analysis': research_raw.get('platform_preferences', 'Not available') if research_raw else 'Not available',
            'content_performance': website_raw.get('content_performance', 'Not available') if website_raw else 'Not available'
        }

    if research_raw:
        input_data_points['content_frequency'] = {
            'audience_research': research_raw.get('content_frequency_preferences', 'Not available'),
            'industry_standards': research_raw.get('industry_frequency', 'Not available'),
            'competitor_frequency': research_raw.get('competitor_frequency', 'Not available'),
            'optimal_timing': research_raw.get('optimal_timing', 'Not available')
        }

    if website_raw:
        input_data_points['content_budget'] = {
            'website_analysis': website_raw.get('budget_indicators', 'Not available'),
            'industry_standards': website_raw.get('industry_budget', 'Not available'),
            'company_size': website_raw.get('company_size', 'Not available'),
            'market_position': website_raw.get('market_position', 'Not available')
        }

    if website_raw:
        input_data_points['team_size'] = {
            'company_profile': website_raw.get('company_profile', 'Not available'),
            'content_volume': website_raw.get('content_volume', 'Not available'),
            'industry_standards': website_raw.get('industry_team_size', 'Not available'),
            'budget_constraints': website_raw.get('budget_constraints', 'Not available')
        }

    if research_raw:
        input_data_points['implementation_timeline'] = {
            'project_scope': research_raw.get('project_scope', 'Not available'),
            'resource_availability': research_raw.get('resource_availability', 'Not available'),
            'industry_timeline': research_raw.get('industry_timeline', 'Not available'),
            'complexity_assessment': research_raw.get('complexity_assessment', 'Not available')
        }

    return input_data_points 