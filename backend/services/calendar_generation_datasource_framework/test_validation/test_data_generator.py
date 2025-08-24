"""
Test Data Generator for 12-Step Calendar Generation Validation
Generates realistic test data for validation and testing purposes.
"""

import json
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class TestStrategyData:
    """Test strategy data structure."""
    strategy_id: int
    strategy_name: str
    industry: str
    target_audience: Dict[str, Any]
    content_pillars: List[str]
    business_goals: List[str]
    kpi_mapping: Dict[str, Any]
    brand_voice: str
    editorial_guidelines: List[str]
    competitive_landscape: Dict[str, Any]


@dataclass
class TestUserData:
    """Test user data structure."""
    user_id: int
    onboarding_data: Dict[str, Any]
    ai_analysis_results: Dict[str, Any]
    gap_analysis: Dict[str, Any]
    performance_data: Dict[str, Any]
    recommendations_data: Dict[str, Any]


class TestDataGenerator:
    """
    Generates realistic test data for validation and testing.
    """
    
    def __init__(self):
        self.industries = [
            "technology", "healthcare", "finance", "education", 
            "ecommerce", "marketing", "consulting", "real_estate"
        ]
        
        self.content_pillars = [
            "Industry Insights", "Product Updates", "Customer Success",
            "Thought Leadership", "Best Practices", "Company News",
            "Tutorials & Guides", "Case Studies", "Expert Interviews"
        ]
        
        self.business_goals = [
            "Increase brand awareness", "Generate leads", "Establish thought leadership",
            "Improve customer engagement", "Drive website traffic", "Boost conversions",
            "Enhance customer retention", "Expand market reach"
        ]
        
        self.target_audience_segments = [
            "C-level executives", "Marketing professionals", "Sales teams",
            "Product managers", "Developers", "Small business owners",
            "Enterprise decision makers", "Industry professionals"
        ]
    
    def generate_test_strategy_data(self, strategy_id: int = 1) -> TestStrategyData:
        """Generate realistic test strategy data."""
        
        industry = random.choice(self.industries)
        strategy_name = f"{industry.title()} Content Strategy {strategy_id}"
        
        # Generate target audience
        target_audience = {
            "primary": random.choice(self.target_audience_segments),
            "secondary": random.choice(self.target_audience_segments),
            "demographics": {
                "age_range": "25-45",
                "location": "Global",
                "company_size": random.choice(["SME", "Enterprise", "Startup"])
            },
            "interests": [
                "Industry trends", "Best practices", "Innovation",
                "Professional development", "Technology adoption"
            ]
        }
        
        # Generate content pillars (3-6 pillars)
        num_pillars = random.randint(3, 6)
        content_pillars = random.sample(self.content_pillars, num_pillars)
        
        # Generate business goals (3-5 goals)
        num_goals = random.randint(3, 5)
        business_goals = random.sample(self.business_goals, num_goals)
        
        # Generate KPI mapping
        kpi_mapping = {
            "awareness": ["Website traffic", "Social media reach", "Brand mentions"],
            "engagement": ["Time on page", "Social shares", "Comments"],
            "conversion": ["Lead generation", "Email signups", "Demo requests"],
            "retention": ["Return visitors", "Email open rates", "Customer satisfaction"]
        }
        
        # Generate brand voice
        brand_voices = ["Professional", "Friendly", "Authoritative", "Innovative", "Trustworthy"]
        brand_voice = random.choice(brand_voices)
        
        # Generate editorial guidelines
        editorial_guidelines = [
            "Use clear, concise language",
            "Include data and statistics when possible",
            "Focus on actionable insights",
            "Maintain consistent tone and style",
            "Include relevant examples and case studies"
        ]
        
        # Generate competitive landscape
        competitive_landscape = {
            "top_competitors": [
                f"Competitor {i+1}" for i in range(random.randint(3, 6))
            ],
            "competitive_advantages": [
                "Unique industry expertise",
                "Comprehensive solution offering",
                "Strong customer relationships",
                "Innovative technology approach"
            ],
            "market_positioning": f"Leading {industry} solution provider"
        }
        
        return TestStrategyData(
            strategy_id=strategy_id,
            strategy_name=strategy_name,
            industry=industry,
            target_audience=target_audience,
            content_pillars=content_pillars,
            business_goals=business_goals,
            kpi_mapping=kpi_mapping,
            brand_voice=brand_voice,
            editorial_guidelines=editorial_guidelines,
            competitive_landscape=competitive_landscape
        )
    
    def generate_test_user_data(self, user_id: int = 1, strategy_id: int = 1) -> TestUserData:
        """Generate realistic test user data."""
        
        # Generate onboarding data
        onboarding_data = {
            "website_analysis": {
                "industry_focus": random.choice(self.industries),
                "target_audience": random.choice(self.target_audience_segments),
                "current_content_volume": random.randint(10, 100),
                "content_gaps": [
                    "Industry-specific insights",
                    "Technical tutorials",
                    "Customer success stories",
                    "Thought leadership content"
                ]
            },
            "competitor_analysis": {
                "top_performers": [
                    f"Competitor {i+1}" for i in range(random.randint(3, 6))
                ],
                "content_themes": [
                    "Industry trends", "Best practices", "Product updates",
                    "Customer success", "Expert insights"
                ],
                "performance_metrics": {
                    "engagement_rate": random.uniform(2.0, 8.0),
                    "conversion_rate": random.uniform(1.0, 5.0),
                    "traffic_growth": random.uniform(10.0, 50.0)
                }
            },
            "keyword_analysis": {
                "high_value_keywords": [
                    f"keyword_{i+1}" for i in range(random.randint(10, 20))
                ],
                "search_volume": random.randint(1000, 10000),
                "competition_level": random.choice(["Low", "Medium", "High"]),
                "opportunity_score": random.uniform(0.6, 0.9)
            }
        }
        
        # Generate AI analysis results
        ai_analysis_results = {
            "strategic_intelligence": {
                "market_trends": [
                    "Increased focus on digital transformation",
                    "Growing demand for automation solutions",
                    "Rising importance of data security"
                ],
                "content_opportunities": [
                    "Industry-specific case studies",
                    "Technical implementation guides",
                    "Expert interview series"
                ],
                "competitive_insights": [
                    "Gap in thought leadership content",
                    "Opportunity for technical tutorials",
                    "Need for customer success stories"
                ]
            },
            "performance_predictions": {
                "expected_traffic_growth": random.uniform(20.0, 80.0),
                "engagement_improvement": random.uniform(15.0, 40.0),
                "conversion_rate_boost": random.uniform(10.0, 30.0)
            }
        }
        
        # Generate gap analysis
        gap_analysis = {
            "content_gaps": [
                {
                    "gap_type": "Topic Coverage",
                    "description": "Missing content on emerging technologies",
                    "priority": "High",
                    "impact_score": random.uniform(0.7, 0.9)
                },
                {
                    "gap_type": "Content Format",
                    "description": "Need for video tutorials and webinars",
                    "priority": "Medium",
                    "impact_score": random.uniform(0.5, 0.8)
                }
            ],
            "keyword_opportunities": [
                {
                    "keyword": f"opportunity_keyword_{i+1}",
                    "search_volume": random.randint(500, 5000),
                    "competition": random.choice(["Low", "Medium"]),
                    "relevance_score": random.uniform(0.8, 0.95)
                }
                for i in range(random.randint(5, 10))
            ],
            "competitor_insights": [
                {
                    "competitor": f"Competitor {i+1}",
                    "strength": random.choice(["Content quality", "Publishing frequency", "SEO optimization"]),
                    "opportunity": "Gap in technical content coverage"
                }
                for i in range(random.randint(3, 6))
            ]
        }
        
        # Generate performance data
        performance_data = {
            "content_performance": {
                "top_performing_content": [
                    {
                        "title": f"Top Content {i+1}",
                        "views": random.randint(1000, 10000),
                        "engagement_rate": random.uniform(3.0, 8.0),
                        "conversion_rate": random.uniform(2.0, 6.0)
                    }
                    for i in range(random.randint(3, 8))
                ],
                "underperforming_content": [
                    {
                        "title": f"Underperforming Content {i+1}",
                        "views": random.randint(100, 500),
                        "engagement_rate": random.uniform(0.5, 2.0),
                        "conversion_rate": random.uniform(0.1, 1.0)
                    }
                    for i in range(random.randint(2, 5))
                ]
            },
            "platform_performance": {
                "blog": {
                    "traffic": random.randint(5000, 50000),
                    "engagement": random.uniform(2.0, 6.0),
                    "conversions": random.randint(100, 1000)
                },
                "social_media": {
                    "reach": random.randint(10000, 100000),
                    "engagement": random.uniform(1.0, 4.0),
                    "followers": random.randint(1000, 10000)
                },
                "email": {
                    "subscribers": random.randint(500, 5000),
                    "open_rate": random.uniform(15.0, 35.0),
                    "click_rate": random.uniform(2.0, 8.0)
                }
            }
        }
        
        # Generate recommendations data
        recommendations_data = {
            "content_recommendations": [
                {
                    "type": "Blog Post",
                    "title": f"Recommended Content {i+1}",
                    "topic": random.choice([
                        "Industry trends", "Best practices", "Case study",
                        "Tutorial", "Expert interview", "Product update"
                    ]),
                    "priority": random.choice(["High", "Medium", "Low"]),
                    "expected_impact": random.uniform(0.6, 0.9)
                }
                for i in range(random.randint(5, 15))
            ],
            "optimization_recommendations": [
                {
                    "area": random.choice(["SEO", "Content Quality", "Publishing Schedule", "Distribution"]),
                    "recommendation": f"Optimization recommendation {i+1}",
                    "impact": random.uniform(0.3, 0.8)
                }
                for i in range(random.randint(3, 8))
            ]
        }
        
        return TestUserData(
            user_id=user_id,
            onboarding_data=onboarding_data,
            ai_analysis_results=ai_analysis_results,
            gap_analysis=gap_analysis,
            performance_data=performance_data,
            recommendations_data=recommendations_data
        )
    
    def generate_comprehensive_test_data(self, user_id: int = 1, strategy_id: int = 1) -> Dict[str, Any]:
        """Generate comprehensive test data for validation."""
        
        strategy_data = self.generate_test_strategy_data(strategy_id)
        user_data = self.generate_test_user_data(user_id, strategy_id)
        
        return {
            "user_id": user_id,
            "strategy_id": strategy_id,
            "strategy_data": asdict(strategy_data),
            "onboarding_data": user_data.onboarding_data,
            "ai_analysis_results": user_data.ai_analysis_results,
            "gap_analysis": user_data.gap_analysis,
            "performance_data": user_data.performance_data,
            "recommendations_data": user_data.recommendations_data,
            "industry": strategy_data.industry,
            "target_audience": strategy_data.target_audience,
            "business_goals": strategy_data.business_goals,
            "website_analysis": user_data.onboarding_data["website_analysis"],
            "competitor_analysis": user_data.onboarding_data["competitor_analysis"],
            "keyword_analysis": user_data.onboarding_data["keyword_analysis"],
            "strategy_analysis": {
                "completeness_score": random.uniform(0.7, 0.95),
                "quality_score": random.uniform(0.75, 0.9),
                "alignment_score": random.uniform(0.8, 0.95)
            },
            "quality_indicators": {
                "data_completeness": random.uniform(0.8, 0.95),
                "strategic_alignment": random.uniform(0.75, 0.9),
                "market_relevance": random.uniform(0.8, 0.95)
            }
        }
    
    def save_test_data(self, data: Dict[str, Any], filename: str = None):
        """Save test data to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_data_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"💾 Test data saved to: {filename}")
    
    def load_test_data(self, filename: str) -> Dict[str, Any]:
        """Load test data from JSON file."""
        with open(filename, 'r') as f:
            return json.load(f)


# Test data generation functions
def generate_test_data_for_validation(user_id: int = 1, strategy_id: int = 1) -> Dict[str, Any]:
    """Generate test data specifically for validation testing."""
    generator = TestDataGenerator()
    return generator.generate_comprehensive_test_data(user_id, strategy_id)


def create_test_data_files():
    """Create sample test data files for different scenarios."""
    generator = TestDataGenerator()
    
    # Generate multiple test scenarios
    test_scenarios = [
        {"user_id": 1, "strategy_id": 1, "description": "Standard technology company"},
        {"user_id": 2, "strategy_id": 2, "description": "Healthcare startup"},
        {"user_id": 3, "strategy_id": 3, "description": "Financial services enterprise"}
    ]
    
    for scenario in test_scenarios:
        data = generator.generate_comprehensive_test_data(
            scenario["user_id"], 
            scenario["strategy_id"]
        )
        
        filename = f"test_data_user_{scenario['user_id']}_strategy_{scenario['strategy_id']}.json"
        generator.save_test_data(data, filename)
        
        print(f"✅ Generated test data for: {scenario['description']}")


if __name__ == "__main__":
    # Generate sample test data
    print("🧪 Generating Test Data for Validation...")
    create_test_data_files()
    print("✅ Test data generation completed!")
