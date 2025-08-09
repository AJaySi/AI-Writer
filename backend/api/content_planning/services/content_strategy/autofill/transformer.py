from typing import Any, Dict


def transform_to_fields(*, website: Dict[str, Any], research: Dict[str, Any], api_keys: Dict[str, Any], session: Dict[str, Any]) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    # Business Context
    if website.get('content_goals'):
        fields['business_objectives'] = {
            'value': website.get('content_goals'),
            'source': 'website_analysis',
            'confidence': website.get('confidence_level')
        }

    if website.get('target_metrics'):
        fields['target_metrics'] = {
            'value': website.get('target_metrics'),
            'source': 'website_analysis',
            'confidence': website.get('confidence_level')
        }
    elif website.get('performance_metrics'):
        fields['target_metrics'] = {
            'value': website.get('performance_metrics'),
            'source': 'website_analysis',
            'confidence': website.get('confidence_level')
        }

    # content_budget with session fallback
    if website.get('content_budget') is not None:
        fields['content_budget'] = {
            'value': website.get('content_budget'),
            'source': 'website_analysis',
            'confidence': website.get('confidence_level')
        }
    elif isinstance(session, dict) and session.get('budget') is not None:
        fields['content_budget'] = {
            'value': session.get('budget'),
            'source': 'onboarding_session',
            'confidence': 0.7
        }

    # team_size with session fallback
    if website.get('team_size') is not None:
        fields['team_size'] = {
            'value': website.get('team_size'),
            'source': 'website_analysis',
            'confidence': website.get('confidence_level')
        }
    elif isinstance(session, dict) and session.get('team_size') is not None:
        fields['team_size'] = {
            'value': session.get('team_size'),
            'source': 'onboarding_session',
            'confidence': 0.7
        }

    # implementation_timeline with session fallback
    if website.get('implementation_timeline'):
        fields['implementation_timeline'] = {
            'value': website.get('implementation_timeline'),
            'source': 'website_analysis',
            'confidence': website.get('confidence_level')
        }
    elif isinstance(session, dict) and session.get('timeline'):
        fields['implementation_timeline'] = {
            'value': session.get('timeline'),
            'source': 'onboarding_session',
            'confidence': 0.7
        }

    # market_share with derive from performance metrics
    if website.get('market_share'):
        fields['market_share'] = {
            'value': website.get('market_share'),
            'source': 'website_analysis',
            'confidence': website.get('confidence_level')
        }
    elif website.get('performance_metrics'):
        fields['market_share'] = {
            'value': website.get('performance_metrics', {}).get('estimated_market_share', None),
            'source': 'website_analysis',
            'confidence': website.get('confidence_level')
        }

    # performance metrics
    fields['performance_metrics'] = {
        'value': website.get('performance_metrics', {}),
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.8)
    }

    # Audience Intelligence
    audience_research = research.get('audience_intelligence', {})
    content_prefs = research.get('content_preferences', {})

    fields['content_preferences'] = {
        'value': content_prefs,
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['consumption_patterns'] = {
        'value': audience_research.get('consumption_patterns', {}),
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['audience_pain_points'] = {
        'value': audience_research.get('pain_points', []),
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['buying_journey'] = {
        'value': audience_research.get('buying_journey', {}),
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['seasonal_trends'] = {
        'value': ['Q1: Planning', 'Q2: Execution', 'Q3: Optimization', 'Q4: Review'],
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.7)
    }

    fields['engagement_metrics'] = {
        'value': {
            'avg_session_duration': website.get('performance_metrics', {}).get('avg_session_duration', 180),
            'bounce_rate': website.get('performance_metrics', {}).get('bounce_rate', 45.5),
            'pages_per_session': 2.5,
        },
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.8)
    }

    # Competitive Intelligence
    fields['top_competitors'] = {
        'value': website.get('competitors', [
            'Competitor A - Industry Leader',
            'Competitor B - Emerging Player',
            'Competitor C - Niche Specialist'
        ]),
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.8)
    }

    fields['competitor_content_strategies'] = {
        'value': ['Educational content', 'Case studies', 'Thought leadership'],
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.7)
    }

    fields['market_gaps'] = {
        'value': website.get('market_gaps', []),
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.8)
    }

    fields['industry_trends'] = {
        'value': ['Digital transformation', 'AI/ML adoption', 'Remote work'],
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.8)
    }

    fields['emerging_trends'] = {
        'value': ['Voice search optimization', 'Video content', 'Interactive content'],
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.7)
    }

    # Content Strategy
    fields['preferred_formats'] = {
        'value': content_prefs.get('preferred_formats', ['Blog posts', 'Whitepapers', 'Webinars', 'Case studies', 'Videos']),
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['content_mix'] = {
        'value': {
            'blog_posts': 40,
            'whitepapers': 20,
            'webinars': 15,
            'case_studies': 15,
            'videos': 10,
        },
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['content_frequency'] = {
        'value': 'Weekly',
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['optimal_timing'] = {
        'value': {
            'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
            'best_times': ['9:00 AM', '1:00 PM', '3:00 PM']
        },
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.7)
    }

    fields['quality_metrics'] = {
        'value': {
            'readability_score': 8.5,
            'engagement_target': 5.0,
            'conversion_target': 2.0
        },
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['editorial_guidelines'] = {
        'value': {
            'tone': content_prefs.get('content_style', ['Professional', 'Educational']),
            'length': content_prefs.get('content_length', 'Medium (1000-2000 words)'),
            'formatting': ['Use headers', 'Include visuals', 'Add CTAs']
        },
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    fields['brand_voice'] = {
        'value': {
            'tone': 'Professional yet approachable',
            'style': 'Educational and authoritative',
            'personality': 'Expert, helpful, trustworthy'
        },
        'source': 'research_preferences',
        'confidence': research.get('confidence_level', 0.8)
    }

    # Performance & Analytics
    fields['traffic_sources'] = {
        'value': website.get('traffic_sources', {}),
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.8)
    }

    fields['conversion_rates'] = {
        'value': {
            'overall': website.get('performance_metrics', {}).get('conversion_rate', 3.2),
            'blog': 2.5,
            'landing_pages': 4.0,
            'email': 5.5,
        },
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.8)
    }

    fields['content_roi_targets'] = {
        'value': {
            'target_roi': 300,
            'cost_per_lead': 50,
            'lifetime_value': 500,
        },
        'source': 'website_analysis',
        'confidence': website.get('confidence_level', 0.7)
    }

    fields['ab_testing_capabilities'] = {
        'value': True,
        'source': 'api_keys_data',
        'confidence': api_keys.get('confidence_level', 0.8)
    }

    return fields 