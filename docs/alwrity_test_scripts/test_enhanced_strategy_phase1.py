"""
Test Enhanced Strategy Service - Phase 1 Implementation
Validates the enhanced strategy service with 30+ strategic inputs and AI recommendations.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

# Import models
from models.enhanced_strategy_models import EnhancedContentStrategy, EnhancedAIAnalysisResult, OnboardingDataIntegration

# Import services
from api.content_planning.services.enhanced_strategy_service import EnhancedStrategyService
from services.enhanced_strategy_db_service import EnhancedStrategyDBService

class TestEnhancedStrategyPhase1:
    """Test class for Enhanced Strategy Service Phase 1 implementation."""
    
    def get_sample_strategy_data(self) -> Dict[str, Any]:
        """Sample strategy data for testing."""
        return {
            'user_id': 1,
            'name': 'Test Enhanced Strategy',
            'industry': 'technology',
            
            # Business Context (8 inputs)
            'business_objectives': {
                'primary': 'Increase brand awareness',
                'secondary': ['Lead generation', 'Customer engagement']
            },
            'target_metrics': {
                'traffic': '50% increase',
                'engagement': '25% improvement',
                'conversions': '15% growth'
            },
            'content_budget': 5000.0,
            'team_size': 3,
            'implementation_timeline': '6 months',
            'market_share': '2.5%',
            'competitive_position': 'challenger',
            'performance_metrics': {
                'current_traffic': 10000,
                'current_engagement': 3.2,
                'current_conversions': 2.1
            },
            
            # Audience Intelligence (6 inputs)
            'content_preferences': {
                'formats': ['blog_posts', 'videos', 'infographics'],
                'topics': ['technology', 'business', 'innovation'],
                'tone': 'professional'
            },
            'consumption_patterns': {
                'peak_times': ['9-11 AM', '2-4 PM'],
                'devices': ['desktop', 'mobile'],
                'channels': ['website', 'social_media']
            },
            'audience_pain_points': [
                'Complex technology solutions',
                'Limited time for research',
                'Need for practical implementation'
            ],
            'buying_journey': {
                'awareness': 'Social media, SEO',
                'consideration': 'Case studies, demos',
                'decision': 'Free trials, consultations'
            },
            'seasonal_trends': {
                'Q1': 'New year planning content',
                'Q2': 'Spring technology updates',
                'Q3': 'Summer optimization',
                'Q4': 'Year-end reviews'
            },
            'engagement_metrics': {
                'avg_time_on_page': 2.5,
                'bounce_rate': 45.2,
                'social_shares': 150
            },
            
            # Competitive Intelligence (5 inputs)
            'top_competitors': [
                'Competitor A',
                'Competitor B',
                'Competitor C'
            ],
            'competitor_content_strategies': {
                'Competitor A': 'High-frequency blog posts',
                'Competitor B': 'Video-focused content',
                'Competitor C': 'Whitepaper strategy'
            },
            'market_gaps': [
                'Interactive content experiences',
                'AI-powered personalization',
                'Industry-specific solutions'
            ],
            'industry_trends': [
                'AI integration',
                'Remote work solutions',
                'Sustainability focus'
            ],
            'emerging_trends': [
                'Voice search optimization',
                'Video-first content',
                'Personalization at scale'
            ],
            
            # Content Strategy (7 inputs)
            'preferred_formats': ['blog_posts', 'videos', 'webinars'],
            'content_mix': {
                'blog_posts': 40,
                'videos': 30,
                'webinars': 20,
                'infographics': 10
            },
            'content_frequency': 'weekly',
            'optimal_timing': {
                'blog_posts': 'Tuesday 9 AM',
                'videos': 'Thursday 2 PM',
                'social_posts': 'Daily 10 AM'
            },
            'quality_metrics': {
                'readability_score': 8.5,
                'engagement_threshold': 3.0,
                'conversion_target': 2.5
            },
            'editorial_guidelines': {
                'tone': 'professional',
                'style': 'clear and concise',
                'formatting': 'scannable'
            },
            'brand_voice': {
                'personality': 'innovative',
                'tone': 'authoritative',
                'style': 'informative'
            },
            
            # Performance & Analytics (4 inputs)
            'traffic_sources': {
                'organic': 45,
                'social': 25,
                'direct': 20,
                'referral': 10
            },
            'conversion_rates': {
                'overall': 2.1,
                'blog_posts': 1.8,
                'videos': 3.2,
                'webinars': 5.5
            },
            'content_roi_targets': {
                'target_roi': 300,
                'cost_per_lead': 50,
                'lifetime_value': 500
            },
            'ab_testing_capabilities': True
        }
    
    def test_enhanced_strategy_model_creation(self):
        """Test creating enhanced strategy model with 30+ inputs."""
        sample_strategy_data = self.get_sample_strategy_data()
        strategy = EnhancedContentStrategy(**sample_strategy_data)
        
        # Verify all fields are set
        assert strategy.user_id == 1
        assert strategy.name == 'Test Enhanced Strategy'
        assert strategy.industry == 'technology'
        
        # Verify business context fields
        assert strategy.business_objectives is not None
        assert strategy.target_metrics is not None
        assert strategy.content_budget == 5000.0
        assert strategy.team_size == 3
        
        # Verify audience intelligence fields
        assert strategy.content_preferences is not None
        assert strategy.consumption_patterns is not None
        assert strategy.audience_pain_points is not None
        
        # Verify competitive intelligence fields
        assert strategy.top_competitors is not None
        assert strategy.market_gaps is not None
        assert strategy.industry_trends is not None
        
        # Verify content strategy fields
        assert strategy.preferred_formats is not None
        assert strategy.content_mix is not None
        assert strategy.content_frequency == 'weekly'
        
        # Verify performance analytics fields
        assert strategy.traffic_sources is not None
        assert strategy.conversion_rates is not None
        assert strategy.ab_testing_capabilities is True
        
        print("✅ Enhanced strategy model creation test passed")
    
    def test_completion_percentage_calculation(self):
        """Test completion percentage calculation for 30+ inputs."""
        sample_strategy_data = self.get_sample_strategy_data()
        strategy = EnhancedContentStrategy(**sample_strategy_data)
        
        # Calculate completion percentage
        completion = strategy.calculate_completion_percentage()
        
        # Should be high since we provided most fields
        assert completion > 80
        assert strategy.completion_percentage > 80
        
        print(f"✅ Completion percentage calculation test passed: {completion}%")
    
    def test_enhanced_strategy_to_dict(self):
        """Test enhanced strategy to_dict method."""
        sample_strategy_data = self.get_sample_strategy_data()
        strategy = EnhancedContentStrategy(**sample_strategy_data)
        strategy_dict = strategy.to_dict()
        
        # Verify all categories are present
        assert 'business_objectives' in strategy_dict
        assert 'content_preferences' in strategy_dict
        assert 'top_competitors' in strategy_dict
        assert 'preferred_formats' in strategy_dict
        assert 'traffic_sources' in strategy_dict
        
        # Verify metadata fields
        assert 'completion_percentage' in strategy_dict
        assert 'created_at' in strategy_dict
        assert 'updated_at' in strategy_dict
        
        print("✅ Enhanced strategy to_dict test passed")
    
    def test_ai_analysis_result_model(self):
        """Test AI analysis result model creation."""
        analysis_data = {
            'user_id': 1,
            'strategy_id': 1,
            'analysis_type': 'comprehensive_strategy',
            'comprehensive_insights': {
                'strategic_positioning': 'Strong market position',
                'content_pillars': ['Educational', 'Thought Leadership', 'Case Studies']
            },
            'audience_intelligence': {
                'persona_insights': 'Tech-savvy professionals',
                'engagement_patterns': 'Peak engagement on Tuesdays'
            },
            'competitive_intelligence': {
                'competitor_analysis': 'Identified 3 key competitors',
                'differentiation_opportunities': ['AI integration', 'Personalization']
            },
            'performance_optimization': {
                'traffic_optimization': 'Focus on organic search',
                'conversion_improvement': 'A/B test landing pages'
            },
            'content_calendar_optimization': {
                'publishing_schedule': 'Tuesday/Thursday posts',
                'content_mix': '40% blog, 30% video, 30% other'
            },
            'processing_time': 2.5,
            'ai_service_status': 'operational'
        }
        
        analysis_result = EnhancedAIAnalysisResult(**analysis_data)
        
        assert analysis_result.user_id == 1
        assert analysis_result.strategy_id == 1
        assert analysis_result.analysis_type == 'comprehensive_strategy'
        assert analysis_result.processing_time == 2.5
        assert analysis_result.ai_service_status == 'operational'
        
        print("✅ AI analysis result model test passed")
    
    def test_onboarding_integration_model(self):
        """Test onboarding data integration model creation."""
        integration_data = {
            'user_id': 1,
            'strategy_id': 1,
            'website_analysis_data': {
                'writing_style': {'tone': 'professional'},
                'target_audience': {'demographics': 'professionals'}
            },
            'research_preferences_data': {
                'content_types': ['blog_posts', 'videos'],
                'research_depth': 'comprehensive'
            },
            'auto_populated_fields': {
                'content_preferences': 'website_analysis',
                'target_audience': 'website_analysis',
                'preferred_formats': 'research_preferences'
            },
            'field_mappings': {
                'writing_style.tone': 'brand_voice.personality',
                'content_types': 'preferred_formats'
            },
            'data_quality_scores': {
                'website_analysis': 85.0,
                'research_preferences': 90.0
            },
            'confidence_levels': {
                'content_preferences': 0.8,
                'target_audience': 0.8,
                'preferred_formats': 0.7
            }
        }
        
        integration = OnboardingDataIntegration(**integration_data)
        
        assert integration.user_id == 1
        assert integration.strategy_id == 1
        assert integration.website_analysis_data is not None
        assert integration.research_preferences_data is not None
        assert integration.auto_populated_fields is not None
        
        print("✅ Onboarding integration model test passed")
    
    def test_enhanced_strategy_service_initialization(self):
        """Test enhanced strategy service initialization."""
        service = EnhancedStrategyService()
        
        # Verify strategic input fields are defined
        assert 'business_context' in service.strategic_input_fields
        assert 'audience_intelligence' in service.strategic_input_fields
        assert 'competitive_intelligence' in service.strategic_input_fields
        assert 'content_strategy' in service.strategic_input_fields
        assert 'performance_analytics' in service.strategic_input_fields
        
        # Verify field counts
        total_fields = sum(len(fields) for fields in service.strategic_input_fields.values())
        assert total_fields >= 30  # 30+ strategic inputs
        
        print(f"✅ Enhanced strategy service initialization test passed: {total_fields} fields")
    
    def test_specialized_prompt_creation(self):
        """Test specialized AI prompt creation."""
        service = EnhancedStrategyService()
        
        strategy_data = {
            'name': 'Test Strategy',
            'industry': 'technology',
            'business_objectives': 'Increase brand awareness',
            'target_metrics': '50% traffic growth',
            'content_budget': 5000,
            'team_size': 3
        }
        
        # Test each analysis type
        analysis_types = [
            'comprehensive_strategy',
            'audience_intelligence',
            'competitive_intelligence',
            'performance_optimization',
            'content_calendar_optimization'
        ]
        
        for analysis_type in analysis_types:
            prompt = service._create_specialized_prompt(analysis_type, strategy_data, None)
            
            assert prompt is not None
            assert len(prompt) > 0
            assert 'Test Strategy' in prompt
            
            # Check for either analysis type or relevant keywords
            if analysis_type == 'performance_optimization':
                assert 'optimization' in prompt.lower()
            elif analysis_type == 'content_calendar_optimization':
                assert 'optimization' in prompt.lower()
            else:
                assert analysis_type in prompt or 'analysis' in prompt.lower()
        
        print("✅ Specialized prompt creation test passed")
    
    def test_fallback_recommendations(self):
        """Test fallback recommendations when AI service fails."""
        service = EnhancedStrategyService()
        
        analysis_types = [
            'comprehensive_strategy',
            'audience_intelligence',
            'competitive_intelligence',
            'performance_optimization',
            'content_calendar_optimization'
        ]
        
        for analysis_type in analysis_types:
            fallback = service._get_fallback_recommendations(analysis_type)
            
            assert fallback is not None
            assert 'recommendations' in fallback
            assert 'insights' in fallback
            assert 'metrics' in fallback
            assert 'score' in fallback['metrics']
            assert 'confidence' in fallback['metrics']
        
        print("✅ Fallback recommendations test passed")
    
    def test_data_quality_calculation(self):
        """Test data quality score calculation."""
        service = EnhancedStrategyService()
        
        data_sources = {
            'website_analysis': {
                'writing_style': {'tone': 'professional'},
                'target_audience': {'demographics': 'professionals'},
                'content_type': {'primary': 'blog_posts'}
            },
            'research_preferences': {
                'content_types': ['blog_posts', 'videos'],
                'research_depth': 'comprehensive'
            }
        }
        
        quality_scores = service._calculate_data_quality_scores(data_sources)
        
        assert 'website_analysis' in quality_scores
        assert 'research_preferences' in quality_scores
        assert quality_scores['website_analysis'] > 0
        assert quality_scores['research_preferences'] > 0
        
        print("✅ Data quality calculation test passed")
    
    def test_confidence_level_calculation(self):
        """Test confidence level calculation for auto-populated fields."""
        service = EnhancedStrategyService()
        
        auto_populated_fields = {
            'content_preferences': 'website_analysis',
            'target_audience': 'website_analysis',
            'preferred_formats': 'research_preferences'
        }
        
        confidence_levels = service._calculate_confidence_levels(auto_populated_fields)
        
        assert 'content_preferences' in confidence_levels
        assert 'target_audience' in confidence_levels
        assert 'preferred_formats' in confidence_levels
        
        # Verify confidence levels are between 0 and 1
        for field, confidence in confidence_levels.items():
            assert 0 <= confidence <= 1
        
        print("✅ Confidence level calculation test passed")
    
    def test_strategic_scores_calculation(self):
        """Test strategic scores calculation from AI recommendations."""
        service = EnhancedStrategyService()
        
        ai_recommendations = {
            'comprehensive_strategy': {
                'metrics': {'score': 85, 'confidence': 0.9}
            },
            'audience_intelligence': {
                'metrics': {'score': 80, 'confidence': 0.8}
            },
            'competitive_intelligence': {
                'metrics': {'score': 75, 'confidence': 0.7}
            }
        }
        
        scores = service._calculate_strategic_scores(ai_recommendations)
        
        assert 'overall_score' in scores
        assert 'content_quality_score' in scores
        assert 'engagement_score' in scores
        assert 'conversion_score' in scores
        assert 'innovation_score' in scores
        
        # Verify scores are calculated
        assert scores['overall_score'] > 0
        
        print("✅ Strategic scores calculation test passed")
    
    def test_market_positioning_extraction(self):
        """Test market positioning extraction from AI recommendations."""
        service = EnhancedStrategyService()
        
        ai_recommendations = {
            'comprehensive_strategy': {
                'metrics': {'score': 85, 'confidence': 0.9}
            }
        }
        
        positioning = service._extract_market_positioning(ai_recommendations)
        
        assert 'industry_position' in positioning
        assert 'competitive_advantage' in positioning
        assert 'market_share' in positioning
        assert 'positioning_score' in positioning
        
        print("✅ Market positioning extraction test passed")
    
    def test_competitive_advantages_extraction(self):
        """Test competitive advantages extraction from AI recommendations."""
        service = EnhancedStrategyService()
        
        ai_recommendations = {
            'competitive_intelligence': {
                'metrics': {'score': 80, 'confidence': 0.8}
            }
        }
        
        advantages = service._extract_competitive_advantages(ai_recommendations)
        
        assert isinstance(advantages, list)
        assert len(advantages) > 0
        
        for advantage in advantages:
            assert 'advantage' in advantage
            assert 'impact' in advantage
            assert 'implementation' in advantage
        
        print("✅ Competitive advantages extraction test passed")
    
    def test_strategic_risks_extraction(self):
        """Test strategic risks extraction from AI recommendations."""
        service = EnhancedStrategyService()
        
        ai_recommendations = {
            'comprehensive_strategy': {
                'metrics': {'score': 85, 'confidence': 0.9}
            }
        }
        
        risks = service._extract_strategic_risks(ai_recommendations)
        
        assert isinstance(risks, list)
        assert len(risks) > 0
        
        for risk in risks:
            assert 'risk' in risk
            assert 'probability' in risk
            assert 'impact' in risk
        
        print("✅ Strategic risks extraction test passed")
    
    def test_opportunity_analysis_extraction(self):
        """Test opportunity analysis extraction from AI recommendations."""
        service = EnhancedStrategyService()
        
        ai_recommendations = {
            'comprehensive_strategy': {
                'metrics': {'score': 85, 'confidence': 0.9}
            }
        }
        
        opportunities = service._extract_opportunity_analysis(ai_recommendations)
        
        assert isinstance(opportunities, list)
        assert len(opportunities) > 0
        
        for opportunity in opportunities:
            assert 'opportunity' in opportunity
            assert 'potential_impact' in opportunity
            assert 'implementation_ease' in opportunity
        
        print("✅ Opportunity analysis extraction test passed")

def run_enhanced_strategy_phase1_tests():
    """Run all Phase 1 tests for enhanced strategy service."""
    print("🚀 Starting Enhanced Strategy Phase 1 Tests")
    print("=" * 50)
    
    test_instance = TestEnhancedStrategyPhase1()
    
    # Run all tests
    test_instance.test_enhanced_strategy_model_creation()
    test_instance.test_completion_percentage_calculation()
    test_instance.test_enhanced_strategy_to_dict()
    test_instance.test_ai_analysis_result_model()
    test_instance.test_onboarding_integration_model()
    test_instance.test_enhanced_strategy_service_initialization()
    test_instance.test_specialized_prompt_creation()
    test_instance.test_fallback_recommendations()
    test_instance.test_data_quality_calculation()
    test_instance.test_confidence_level_calculation()
    test_instance.test_strategic_scores_calculation()
    test_instance.test_market_positioning_extraction()
    test_instance.test_competitive_advantages_extraction()
    test_instance.test_strategic_risks_extraction()
    test_instance.test_opportunity_analysis_extraction()
    
    print("=" * 50)
    print("✅ All Enhanced Strategy Phase 1 Tests Passed!")
    print("🎯 Phase 1 Implementation Complete:")
    print("   - Enhanced database schema with 30+ input fields ✓")
    print("   - Enhanced Strategy Service core implementation ✓")
    print("   - 5 specialized AI prompt implementations ✓")
    print("   - Onboarding data integration ✓")
    print("   - Comprehensive AI recommendations ✓")

if __name__ == "__main__":
    run_enhanced_strategy_phase1_tests() 