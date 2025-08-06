"""
Test Data and Fixtures for Content Planning Module
Centralized test data and fixtures for consistent testing across refactoring.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta

class TestData:
    """Centralized test data and fixtures for content planning tests."""
    
    # Sample Strategies
    SAMPLE_STRATEGIES = {
        "technology_strategy": {
            "user_id": 1,
            "name": "Technology Content Strategy",
            "industry": "technology",
            "target_audience": {
                "age_range": "25-45",
                "interests": ["technology", "innovation", "AI", "machine learning"],
                "location": "global",
                "profession": "tech professionals"
            },
            "content_pillars": [
                {"name": "Educational Content", "percentage": 40, "topics": ["AI", "ML", "Cloud Computing"]},
                {"name": "Thought Leadership", "percentage": 30, "topics": ["Industry Trends", "Innovation"]},
                {"name": "Product Updates", "percentage": 20, "topics": ["Product Features", "Releases"]},
                {"name": "Team Culture", "percentage": 10, "topics": ["Company Culture", "Team Stories"]}
            ],
            "ai_recommendations": {
                "priority_topics": ["Artificial Intelligence", "Machine Learning", "Cloud Computing"],
                "content_frequency": "daily",
                "platform_focus": ["LinkedIn", "Website", "Twitter"],
                "optimal_posting_times": {
                    "linkedin": "09:00-11:00",
                    "twitter": "12:00-14:00",
                    "website": "10:00-12:00"
                }
            }
        },
        "healthcare_strategy": {
            "user_id": 2,
            "name": "Healthcare Content Strategy",
            "industry": "healthcare",
            "target_audience": {
                "age_range": "30-60",
                "interests": ["health", "medicine", "wellness", "medical technology"],
                "location": "US",
                "profession": "healthcare professionals"
            },
            "content_pillars": [
                {"name": "Patient Education", "percentage": 35, "topics": ["Health Tips", "Disease Prevention"]},
                {"name": "Medical Insights", "percentage": 30, "topics": ["Medical Research", "Treatment Advances"]},
                {"name": "Industry News", "percentage": 20, "topics": ["Healthcare Policy", "Industry Updates"]},
                {"name": "Expert Opinions", "percentage": 15, "topics": ["Medical Expert Views", "Case Studies"]}
            ],
            "ai_recommendations": {
                "priority_topics": ["Telemedicine", "Digital Health", "Patient Care"],
                "content_frequency": "weekly",
                "platform_focus": ["LinkedIn", "Website", "YouTube"],
                "optimal_posting_times": {
                    "linkedin": "08:00-10:00",
                    "website": "09:00-11:00",
                    "youtube": "18:00-20:00"
                }
            }
        },
        "finance_strategy": {
            "user_id": 3,
            "name": "Finance Content Strategy",
            "industry": "finance",
            "target_audience": {
                "age_range": "25-55",
                "interests": ["finance", "investment", "banking", "financial planning"],
                "location": "global",
                "profession": "finance professionals"
            },
            "content_pillars": [
                {"name": "Financial Education", "percentage": 40, "topics": ["Investment Tips", "Financial Planning"]},
                {"name": "Market Analysis", "percentage": 30, "topics": ["Market Trends", "Economic Updates"]},
                {"name": "Regulatory Updates", "percentage": 20, "topics": ["Compliance", "Regulations"]},
                {"name": "Success Stories", "percentage": 10, "topics": ["Case Studies", "Client Success"]}
            ],
            "ai_recommendations": {
                "priority_topics": ["Digital Banking", "Fintech", "Investment Strategies"],
                "content_frequency": "weekly",
                "platform_focus": ["LinkedIn", "Website", "Twitter"],
                "optimal_posting_times": {
                    "linkedin": "07:00-09:00",
                    "website": "08:00-10:00",
                    "twitter": "12:00-14:00"
                }
            }
        }
    }
    
    # Sample Calendar Events
    SAMPLE_CALENDAR_EVENTS = {
        "blog_post": {
            "strategy_id": 1,
            "title": "The Future of AI in 2024",
            "description": "A comprehensive analysis of AI trends and their impact on various industries",
            "content_type": "blog_post",
            "platform": "website",
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "ai_recommendations": {
                "optimal_time": "09:00",
                "hashtags": ["#AI", "#Technology", "#Innovation", "#2024"],
                "tone": "professional",
                "target_audience": "tech professionals",
                "estimated_read_time": "8 minutes"
            }
        },
        "linkedin_post": {
            "strategy_id": 1,
            "title": "5 Key AI Trends Every Business Should Know",
            "description": "Quick insights on AI trends that are reshaping business strategies",
            "content_type": "social_post",
            "platform": "linkedin",
            "scheduled_date": (datetime.now() + timedelta(days=3)).isoformat(),
            "ai_recommendations": {
                "optimal_time": "08:30",
                "hashtags": ["#AI", "#Business", "#Innovation", "#DigitalTransformation"],
                "tone": "professional",
                "target_audience": "business leaders",
                "estimated_read_time": "3 minutes"
            }
        },
        "video_content": {
            "strategy_id": 1,
            "title": "AI Implementation Guide for SMEs",
            "description": "Step-by-step guide for small and medium enterprises to implement AI solutions",
            "content_type": "video",
            "platform": "youtube",
            "scheduled_date": (datetime.now() + timedelta(days=10)).isoformat(),
            "ai_recommendations": {
                "optimal_time": "18:00",
                "hashtags": ["#AI", "#SME", "#Implementation", "#Guide"],
                "tone": "educational",
                "target_audience": "small business owners",
                "estimated_duration": "15 minutes"
            }
        }
    }
    
    # Sample Gap Analysis Data
    SAMPLE_GAP_ANALYSIS = {
        "technology_analysis": {
            "user_id": 1,
            "website_url": "https://techcompany.com",
            "competitor_urls": [
                "https://competitor1.com",
                "https://competitor2.com",
                "https://competitor3.com"
            ],
            "target_keywords": [
                "artificial intelligence",
                "machine learning",
                "cloud computing",
                "digital transformation",
                "AI implementation"
            ],
            "industry": "technology",
            "analysis_results": {
                "content_gaps": [
                    {
                        "topic": "AI Ethics and Governance",
                        "gap_score": 85,
                        "opportunity_size": "high",
                        "competitor_coverage": "low"
                    },
                    {
                        "topic": "Edge Computing Solutions",
                        "gap_score": 78,
                        "opportunity_size": "medium",
                        "competitor_coverage": "medium"
                    },
                    {
                        "topic": "Quantum Computing Applications",
                        "gap_score": 92,
                        "opportunity_size": "high",
                        "competitor_coverage": "very_low"
                    }
                ],
                "keyword_opportunities": [
                    {
                        "keyword": "AI ethics framework",
                        "search_volume": 1200,
                        "competition": "low",
                        "opportunity_score": 85
                    },
                    {
                        "keyword": "edge computing benefits",
                        "search_volume": 2400,
                        "competition": "medium",
                        "opportunity_score": 72
                    },
                    {
                        "keyword": "quantum computing use cases",
                        "search_volume": 1800,
                        "competition": "low",
                        "opportunity_score": 88
                    }
                ],
                "competitor_insights": [
                    {
                        "competitor": "competitor1.com",
                        "strengths": ["Strong technical content", "Regular updates"],
                        "weaknesses": ["Limited practical guides", "No video content"],
                        "content_frequency": "weekly"
                    },
                    {
                        "competitor": "competitor2.com",
                        "strengths": ["Comprehensive guides", "Video content"],
                        "weaknesses": ["Outdated information", "Poor SEO"],
                        "content_frequency": "monthly"
                    }
                ]
            },
            "recommendations": [
                {
                    "type": "content_creation",
                    "priority": "high",
                    "title": "Create AI Ethics Framework Guide",
                    "description": "Develop comprehensive guide on AI ethics and governance",
                    "estimated_impact": "high",
                    "implementation_time": "2 weeks"
                },
                {
                    "type": "content_optimization",
                    "priority": "medium",
                    "title": "Optimize for Edge Computing Keywords",
                    "description": "Update existing content to target edge computing opportunities",
                    "estimated_impact": "medium",
                    "implementation_time": "1 week"
                }
            ]
        }
    }
    
    # Sample AI Analytics Data
    SAMPLE_AI_ANALYTICS = {
        "content_evolution": {
            "strategy_id": 1,
            "time_period": "30d",
            "results": {
                "content_performance": {
                    "total_posts": 45,
                    "average_engagement": 78.5,
                    "top_performing_topics": ["AI", "Machine Learning", "Cloud Computing"],
                    "engagement_trend": "increasing"
                },
                "audience_growth": {
                    "follower_increase": 12.5,
                    "engagement_rate_change": 8.2,
                    "new_audience_segments": ["tech executives", "AI researchers"]
                },
                "content_recommendations": [
                    {
                        "topic": "AI Ethics",
                        "reason": "High engagement potential, low competition",
                        "priority": "high",
                        "estimated_impact": "15% engagement increase"
                    },
                    {
                        "topic": "Edge Computing",
                        "reason": "Growing trend, audience interest",
                        "priority": "medium",
                        "estimated_impact": "10% engagement increase"
                    }
                ]
            }
        },
        "performance_trends": {
            "strategy_id": 1,
            "metrics": ["engagement_rate", "reach", "conversions"],
            "results": {
                "engagement_rate": {
                    "current": 78.5,
                    "trend": "increasing",
                    "change_percentage": 12.3,
                    "prediction": "85.2 (next 30 days)"
                },
                "reach": {
                    "current": 12500,
                    "trend": "stable",
                    "change_percentage": 5.1,
                    "prediction": "13200 (next 30 days)"
                },
                "conversions": {
                    "current": 45,
                    "trend": "increasing",
                    "change_percentage": 18.7,
                    "prediction": "52 (next 30 days)"
                }
            }
        },
        "strategic_intelligence": {
            "strategy_id": 1,
            "results": {
                "market_positioning": {
                    "industry_position": "emerging_leader",
                    "competitive_advantage": "technical_expertise",
                    "market_share": "growing",
                    "brand_perception": "innovative"
                },
                "opportunity_analysis": [
                    {
                        "opportunity": "AI Ethics Leadership",
                        "potential_impact": "high",
                        "implementation_ease": "medium",
                        "timeline": "3-6 months"
                    },
                    {
                        "opportunity": "Edge Computing Expertise",
                        "potential_impact": "medium",
                        "implementation_ease": "high",
                        "timeline": "1-2 months"
                    }
                ],
                "risk_assessment": [
                    {
                        "risk": "Competitor AI Content",
                        "severity": "medium",
                        "mitigation": "Accelerate AI ethics content creation"
                    },
                    {
                        "risk": "Market Saturation",
                        "severity": "low",
                        "mitigation": "Focus on unique technical perspectives"
                    }
                ]
            }
        }
    }
    
    # Sample Calendar Generation Data
    SAMPLE_CALENDAR_GENERATION = {
        "monthly_calendar": {
            "user_id": 1,
            "strategy_id": 1,
            "calendar_type": "monthly",
            "industry": "technology",
            "business_size": "sme",
            "force_refresh": False,
            "expected_response": {
                "user_id": 1,
                "strategy_id": 1,
                "calendar_type": "monthly",
                "industry": "technology",
                "business_size": "sme",
                "generated_at": "2024-08-01T10:00:00Z",
                "content_pillars": [
                    "Educational Content",
                    "Thought Leadership",
                    "Product Updates",
                    "Industry Insights",
                    "Team Culture"
                ],
                "platform_strategies": {
                    "website": {
                        "content_types": ["blog_posts", "case_studies", "whitepapers"],
                        "frequency": "2-3 per week",
                        "optimal_length": "1500+ words"
                    },
                    "linkedin": {
                        "content_types": ["industry_insights", "professional_tips", "company_updates"],
                        "frequency": "daily",
                        "optimal_length": "100-300 words"
                    },
                    "twitter": {
                        "content_types": ["quick_tips", "industry_news", "engagement"],
                        "frequency": "3-5 per day",
                        "optimal_length": "280 characters"
                    }
                },
                "content_mix": {
                    "educational": 0.4,
                    "thought_leadership": 0.3,
                    "engagement": 0.2,
                    "promotional": 0.1
                },
                "daily_schedule": [
                    {
                        "day": "Monday",
                        "theme": "Educational Content",
                        "content_type": "blog_post",
                        "platform": "website",
                        "topic": "AI Implementation Guide"
                    },
                    {
                        "day": "Tuesday",
                        "theme": "Thought Leadership",
                        "content_type": "linkedin_post",
                        "platform": "linkedin",
                        "topic": "Industry Trends Analysis"
                    }
                ],
                "weekly_themes": [
                    {
                        "week": 1,
                        "theme": "AI and Machine Learning",
                        "focus_areas": ["AI Ethics", "ML Implementation", "AI Trends"]
                    },
                    {
                        "week": 2,
                        "theme": "Cloud Computing",
                        "focus_areas": ["Cloud Security", "Migration Strategies", "Cost Optimization"]
                    }
                ],
                "performance_predictions": {
                    "estimated_engagement": 85.5,
                    "predicted_reach": 15000,
                    "expected_conversions": 25
                }
            }
        }
    }
    
    # Sample Content Optimization Data
    SAMPLE_CONTENT_OPTIMIZATION = {
        "blog_post_optimization": {
            "user_id": 1,
            "title": "The Future of AI in 2024",
            "description": "A comprehensive analysis of AI trends and their impact on various industries",
            "content_type": "blog_post",
            "target_platform": "linkedin",
            "original_content": {
                "title": "AI Trends 2024",
                "content": "Artificial Intelligence is transforming industries across the globe..."
            },
            "expected_response": {
                "user_id": 1,
                "original_content": {
                    "title": "AI Trends 2024",
                    "content": "Artificial Intelligence is transforming industries across the globe..."
                },
                "optimized_content": {
                    "title": "5 AI Trends That Will Dominate 2024",
                    "content": "Discover the top 5 artificial intelligence trends that are reshaping industries in 2024...",
                    "length": "optimized for LinkedIn",
                    "tone": "professional yet engaging"
                },
                "platform_adaptations": [
                    "Shortened for LinkedIn character limit",
                    "Added professional hashtags",
                    "Optimized for mobile reading"
                ],
                "visual_recommendations": [
                    "Include infographic on AI trends",
                    "Add relevant industry statistics",
                    "Use professional stock images"
                ],
                "hashtag_suggestions": [
                    "#AI", "#Technology", "#Innovation", "#2024", "#DigitalTransformation"
                ],
                "keyword_optimization": {
                    "primary_keywords": ["AI trends", "artificial intelligence"],
                    "secondary_keywords": ["technology", "innovation", "2024"],
                    "keyword_density": "optimal"
                },
                "tone_adjustments": {
                    "original_tone": "technical",
                    "optimized_tone": "professional yet accessible",
                    "changes": "Simplified technical jargon, added engaging hooks"
                },
                "length_optimization": {
                    "original_length": "1500 words",
                    "optimized_length": "300 words",
                    "reason": "LinkedIn post optimization"
                },
                "performance_prediction": {
                    "estimated_engagement": 85,
                    "predicted_reach": 2500,
                    "confidence_score": 0.78
                },
                "optimization_score": 0.85
            }
        }
    }
    
    # Sample Error Scenarios
    ERROR_SCENARIOS = {
        "invalid_user_id": {
            "endpoint": "/api/content-planning/strategies/?user_id=999999",
            "expected_status": 404,
            "expected_error": "User not found"
        },
        "invalid_strategy_id": {
            "endpoint": "/api/content-planning/strategies/999999",
            "expected_status": 404,
            "expected_error": "Strategy not found"
        },
        "invalid_request_data": {
            "endpoint": "/api/content-planning/strategies/",
            "method": "POST",
            "data": {
                "user_id": "invalid",
                "name": "",
                "industry": "invalid_industry"
            },
            "expected_status": 422,
            "expected_error": "Validation error"
        },
        "missing_required_fields": {
            "endpoint": "/api/content-planning/strategies/",
            "method": "POST",
            "data": {
                "user_id": 1
                # Missing required fields
            },
            "expected_status": 422,
            "expected_error": "Missing required fields"
        }
    }
    
    # Sample Performance Data
    PERFORMANCE_DATA = {
        "baseline_metrics": {
            "health_endpoint": {"response_time": 0.05, "status_code": 200},
            "strategies_endpoint": {"response_time": 0.12, "status_code": 200},
            "calendar_endpoint": {"response_time": 0.08, "status_code": 200},
            "gap_analysis_endpoint": {"response_time": 0.15, "status_code": 200}
        },
        "acceptable_thresholds": {
            "response_time": 0.5,  # seconds
            "status_code": 200,
            "error_rate": 0.01  # 1%
        }
    }
    
    @classmethod
    def get_strategy_data(cls, industry: str = "technology") -> Dict[str, Any]:
        """Get sample strategy data for specified industry."""
        key = f"{industry}_strategy"
        return cls.SAMPLE_STRATEGIES.get(key, cls.SAMPLE_STRATEGIES["technology_strategy"])
    
    @classmethod
    def get_calendar_event_data(cls, event_type: str = "blog_post") -> Dict[str, Any]:
        """Get sample calendar event data for specified type."""
        return cls.SAMPLE_CALENDAR_EVENTS.get(event_type, cls.SAMPLE_CALENDAR_EVENTS["blog_post"])
    
    @classmethod
    def get_gap_analysis_data(cls, industry: str = "technology") -> Dict[str, Any]:
        """Get sample gap analysis data for specified industry."""
        key = f"{industry}_analysis"
        return cls.SAMPLE_GAP_ANALYSIS.get(key, cls.SAMPLE_GAP_ANALYSIS["technology_analysis"])
    
    @classmethod
    def get_ai_analytics_data(cls, analysis_type: str = "content_evolution") -> Dict[str, Any]:
        """Get sample AI analytics data for specified type."""
        return cls.SAMPLE_AI_ANALYTICS.get(analysis_type, cls.SAMPLE_AI_ANALYTICS["content_evolution"])
    
    @classmethod
    def get_calendar_generation_data(cls, calendar_type: str = "monthly") -> Dict[str, Any]:
        """Get sample calendar generation data for specified type."""
        key = f"{calendar_type}_calendar"
        return cls.SAMPLE_CALENDAR_GENERATION.get(key, cls.SAMPLE_CALENDAR_GENERATION["monthly_calendar"])
    
    @classmethod
    def get_content_optimization_data(cls, content_type: str = "blog_post") -> Dict[str, Any]:
        """Get sample content optimization data for specified type."""
        key = f"{content_type}_optimization"
        return cls.SAMPLE_CONTENT_OPTIMIZATION.get(key, cls.SAMPLE_CONTENT_OPTIMIZATION["blog_post_optimization"])
    
    @classmethod
    def get_error_scenario(cls, scenario_name: str) -> Dict[str, Any]:
        """Get sample error scenario data."""
        return cls.ERROR_SCENARIOS.get(scenario_name, {})
    
    @classmethod
    def get_performance_baseline(cls) -> Dict[str, Any]:
        """Get performance baseline data."""
        return cls.PERFORMANCE_DATA["baseline_metrics"]
    
    @classmethod
    def get_performance_thresholds(cls) -> Dict[str, Any]:
        """Get performance threshold data."""
        return cls.PERFORMANCE_DATA["acceptable_thresholds"]

# Test data factory functions
def create_test_strategy(industry: str = "technology", user_id: int = 1) -> Dict[str, Any]:
    """Create a test strategy with specified parameters."""
    strategy_data = TestData.get_strategy_data(industry).copy()
    strategy_data["user_id"] = user_id
    return strategy_data

def create_test_calendar_event(strategy_id: int = 1, event_type: str = "blog_post") -> Dict[str, Any]:
    """Create a test calendar event with specified parameters."""
    event_data = TestData.get_calendar_event_data(event_type).copy()
    event_data["strategy_id"] = strategy_id
    return event_data

def create_test_gap_analysis(user_id: int = 1, industry: str = "technology") -> Dict[str, Any]:
    """Create a test gap analysis with specified parameters."""
    analysis_data = TestData.get_gap_analysis_data(industry).copy()
    analysis_data["user_id"] = user_id
    return analysis_data

def create_test_ai_analytics(strategy_id: int = 1, analysis_type: str = "content_evolution") -> Dict[str, Any]:
    """Create a test AI analytics request with specified parameters."""
    analytics_data = TestData.get_ai_analytics_data(analysis_type).copy()
    analytics_data["strategy_id"] = strategy_id
    return analytics_data

def create_test_calendar_generation(user_id: int = 1, strategy_id: int = 1, calendar_type: str = "monthly") -> Dict[str, Any]:
    """Create a test calendar generation request with specified parameters."""
    generation_data = TestData.get_calendar_generation_data(calendar_type).copy()
    generation_data["user_id"] = user_id
    generation_data["strategy_id"] = strategy_id
    return generation_data

def create_test_content_optimization(user_id: int = 1, content_type: str = "blog_post") -> Dict[str, Any]:
    """Create a test content optimization request with specified parameters."""
    optimization_data = TestData.get_content_optimization_data(content_type).copy()
    optimization_data["user_id"] = user_id
    return optimization_data

# Validation functions
def validate_strategy_data(data: Dict[str, Any]) -> bool:
    """Validate strategy data structure."""
    required_fields = ["user_id", "name", "industry", "target_audience"]
    return all(field in data for field in required_fields)

def validate_calendar_event_data(data: Dict[str, Any]) -> bool:
    """Validate calendar event data structure."""
    required_fields = ["strategy_id", "title", "description", "content_type", "platform", "scheduled_date"]
    return all(field in data for field in required_fields)

def validate_gap_analysis_data(data: Dict[str, Any]) -> bool:
    """Validate gap analysis data structure."""
    required_fields = ["user_id", "website_url", "competitor_urls"]
    return all(field in data for field in required_fields)

def validate_response_structure(response: Dict[str, Any], expected_keys: List[str]) -> bool:
    """Validate response structure has expected keys."""
    return all(key in response for key in expected_keys)

def validate_performance_metrics(response_time: float, status_code: int, thresholds: Dict[str, Any]) -> bool:
    """Validate performance metrics against thresholds."""
    return (
        response_time <= thresholds.get("response_time", 0.5) and
        status_code == thresholds.get("status_code", 200)
    ) 