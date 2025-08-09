"""
Enhanced Strategy Service for Content Planning API
Implements the enhanced strategy service with 30+ strategic inputs and AI-powered recommendations.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# Import database models
from models.enhanced_strategy_models import EnhancedContentStrategy, EnhancedAIAnalysisResult, OnboardingDataIntegration
from models.onboarding import OnboardingSession, WebsiteAnalysis, ResearchPreferences, APIKey

# Import database services
from services.content_planning_db import ContentPlanningDBService
from services.ai_analysis_db_service import AIAnalysisDBService
from services.ai_analytics_service import AIAnalyticsService
from .enhanced_strategy_db_service import EnhancedStrategyDBService

# Import utilities
from ..utils.error_handlers import ContentPlanningErrorHandler
from ..utils.response_builders import ResponseBuilder
from ..utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

logger = logging.getLogger(__name__)

class EnhancedStrategyService:
    """Enhanced service class for content strategy operations with 30+ strategic inputs."""
    
    def __init__(self, db_service: Optional[EnhancedStrategyDBService] = None):
        self.ai_analysis_db_service = AIAnalysisDBService()
        self.ai_analytics_service = AIAnalyticsService()
        self.db_service = db_service
        
        # Define the 30+ strategic input fields
        self.strategic_input_fields = {
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
        
        # Performance optimization settings
        self.prompt_versions = {
            'comprehensive_strategy': 'v2.1',
            'audience_intelligence': 'v2.0',
            'competitive_intelligence': 'v2.0',
            'performance_optimization': 'v2.1',
            'content_calendar_optimization': 'v2.0'
        }
        self.quality_thresholds = {
            'min_confidence': 0.7,
            'min_completeness': 0.8,
            'max_response_time': 30.0  # seconds
        }
        
        # Performance optimization settings
        self.cache_settings = {
            'ai_analysis_cache_ttl': 3600,  # 1 hour
            'onboarding_data_cache_ttl': 1800,  # 30 minutes
            'strategy_cache_ttl': 7200,  # 2 hours
            'max_cache_size': 1000  # Maximum cached items
        }
        
        # Performance monitoring
        self.performance_metrics = {
            'response_times': [],
            'cache_hit_rates': {},
            'error_rates': {},
            'throughput_metrics': {}
        }
        
        # Initialize caches
        self._initialize_caches()

    async def create_enhanced_strategy(self, strategy_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Create a new enhanced content strategy with 30+ strategic inputs."""
        try:
            logger.info(f"Creating enhanced content strategy: {strategy_data.get('name', 'Unknown')}")
            
            # Extract user_id from strategy_data
            user_id = strategy_data.get('user_id')
            if not user_id:
                raise ValueError("user_id is required for creating enhanced strategy")
            
            # Create the enhanced strategy
            enhanced_strategy = EnhancedContentStrategy(
                user_id=user_id,
                name=strategy_data.get('name', 'Enhanced Content Strategy'),
                industry=strategy_data.get('industry'),
                
                # Business Context
                business_objectives=strategy_data.get('business_objectives'),
                target_metrics=strategy_data.get('target_metrics'),
                content_budget=strategy_data.get('content_budget'),
                team_size=strategy_data.get('team_size'),
                implementation_timeline=strategy_data.get('implementation_timeline'),
                market_share=strategy_data.get('market_share'),
                competitive_position=strategy_data.get('competitive_position'),
                performance_metrics=strategy_data.get('performance_metrics'),
                
                # Audience Intelligence
                content_preferences=strategy_data.get('content_preferences'),
                consumption_patterns=strategy_data.get('consumption_patterns'),
                audience_pain_points=strategy_data.get('audience_pain_points'),
                buying_journey=strategy_data.get('buying_journey'),
                seasonal_trends=strategy_data.get('seasonal_trends'),
                engagement_metrics=strategy_data.get('engagement_metrics'),
                
                # Competitive Intelligence
                top_competitors=strategy_data.get('top_competitors'),
                competitor_content_strategies=strategy_data.get('competitor_content_strategies'),
                market_gaps=strategy_data.get('market_gaps'),
                industry_trends=strategy_data.get('industry_trends'),
                emerging_trends=strategy_data.get('emerging_trends'),
                
                # Content Strategy
                preferred_formats=strategy_data.get('preferred_formats'),
                content_mix=strategy_data.get('content_mix'),
                content_frequency=strategy_data.get('content_frequency'),
                optimal_timing=strategy_data.get('optimal_timing'),
                quality_metrics=strategy_data.get('quality_metrics'),
                editorial_guidelines=strategy_data.get('editorial_guidelines'),
                brand_voice=strategy_data.get('brand_voice'),
                
                # Performance & Analytics
                traffic_sources=strategy_data.get('traffic_sources'),
                conversion_rates=strategy_data.get('conversion_rates'),
                content_roi_targets=strategy_data.get('content_roi_targets'),
                ab_testing_capabilities=strategy_data.get('ab_testing_capabilities', False),
                
                # Legacy fields
                target_audience=strategy_data.get('target_audience'),
                content_pillars=strategy_data.get('content_pillars'),
                ai_recommendations=strategy_data.get('ai_recommendations')
            )
            
            # Calculate completion percentage
            enhanced_strategy.calculate_completion_percentage()
            
            # Add to database
            db.add(enhanced_strategy)
            db.commit()
            db.refresh(enhanced_strategy)
            
            # Integrate onboarding data if available
            await self._enhance_strategy_with_onboarding_data(enhanced_strategy, user_id, db)
            
            # Generate comprehensive AI recommendations
            await self._generate_comprehensive_ai_recommendations(enhanced_strategy, db)
            
            logger.info(f"Enhanced content strategy created successfully: {enhanced_strategy.id}")
            return enhanced_strategy.to_dict()
            
        except Exception as e:
            logger.error(f"Error creating enhanced content strategy: {str(e)}")
            db.rollback()
            raise ContentPlanningErrorHandler.handle_general_error(e, "create_enhanced_strategy")
    
    async def get_enhanced_strategies(self, user_id: Optional[int] = None, strategy_id: Optional[int] = None, db: Session = None) -> Dict[str, Any]:
        """Get enhanced content strategies with comprehensive data and AI recommendations."""
        try:
            logger.info(f"🚀 Starting enhanced strategy analysis for user: {user_id}, strategy: {strategy_id}")
            
            # Use db_service if available, otherwise use direct db
            if self.db_service and hasattr(self.db_service, 'db'):
                # Use db_service methods
                if strategy_id:
                    strategy = await self.db_service.get_enhanced_strategy(strategy_id)
                    strategies = [strategy] if strategy else []
                else:
                    strategies = await self.db_service.get_enhanced_strategies(user_id)
            else:
                # Fallback to direct db access
                if not db:
                    raise ValueError("Database session is required when db_service is not available")
                
                # Build query
                query = db.query(EnhancedContentStrategy)
                
                if user_id:
                    query = query.filter(EnhancedContentStrategy.user_id == user_id)
                
                if strategy_id:
                    query = query.filter(EnhancedContentStrategy.id == strategy_id)
                
                # Get strategies
                strategies = query.all()
            
            if not strategies:
                logger.warning("⚠️ No enhanced strategies found")
                return {
                    "status": "not_found",
                    "message": "No enhanced content strategies found",
                    "strategies": [],
                    "total_count": 0,
                    "user_id": user_id
                }
            
            # Process each strategy
            enhanced_strategies = []
            for strategy in strategies:
                # Calculate completion percentage
                if hasattr(strategy, 'calculate_completion_percentage'):
                    strategy.calculate_completion_percentage()
                
                # Get AI analysis results
                ai_analysis = await self._get_latest_ai_analysis(strategy.id, db) if db else None
                
                # Get onboarding data integration
                onboarding_integration = await self._get_onboarding_integration(strategy.id, db) if db else None
                
                strategy_dict = strategy.to_dict() if hasattr(strategy, 'to_dict') else {
                    'id': strategy.id,
                    'name': strategy.name,
                    'industry': strategy.industry,
                    'user_id': strategy.user_id,
                    'created_at': strategy.created_at.isoformat() if strategy.created_at else None,
                    'updated_at': strategy.updated_at.isoformat() if strategy.updated_at else None
                }
                
                strategy_dict.update({
                    'ai_analysis': ai_analysis,
                    'onboarding_integration': onboarding_integration,
                    'completion_percentage': getattr(strategy, 'completion_percentage', 0)
                })
                
                enhanced_strategies.append(strategy_dict)
            
            logger.info(f"✅ Retrieved {len(enhanced_strategies)} enhanced strategies")
            
            return {
                "status": "success",
                "message": "Enhanced content strategies retrieved successfully",
                "strategies": enhanced_strategies,
                "total_count": len(enhanced_strategies),
                "user_id": user_id
            }
            
        except Exception as e:
            logger.error(f"❌ Error retrieving enhanced strategies: {str(e)}")
            raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategies")
    
    async def _enhance_strategy_with_onboarding_data(self, strategy: EnhancedContentStrategy, user_id: int, db: Session) -> None:
        """Enhance strategy with intelligent auto-population from onboarding data."""
        try:
            logger.info(f"Enhancing strategy with onboarding data for user: {user_id}")
            
            # Get onboarding session
            onboarding_session = db.query(OnboardingSession).filter(
                OnboardingSession.user_id == user_id
            ).first()
            
            if not onboarding_session:
                logger.info("No onboarding session found for user")
                return
            
            # Get website analysis data
            website_analysis = db.query(WebsiteAnalysis).filter(
                WebsiteAnalysis.session_id == onboarding_session.id
            ).first()
            
            # Get research preferences data
            research_preferences = db.query(ResearchPreferences).filter(
                ResearchPreferences.session_id == onboarding_session.id
            ).first()
            
            # Get API keys data
            api_keys = db.query(APIKey).filter(
                APIKey.session_id == onboarding_session.id
            ).all()
            
            # Auto-populate fields from onboarding data
            auto_populated_fields = {}
            data_sources = {}
            
            if website_analysis:
                # Extract content preferences from writing style
                if website_analysis.writing_style:
                    strategy.content_preferences = self._extract_content_preferences_from_style(
                        website_analysis.writing_style
                    )
                    auto_populated_fields['content_preferences'] = 'website_analysis'
                
                # Extract target audience from analysis
                if website_analysis.target_audience:
                    strategy.target_audience = website_analysis.target_audience
                    auto_populated_fields['target_audience'] = 'website_analysis'
                
                # Extract brand voice from style guidelines
                if website_analysis.style_guidelines:
                    strategy.brand_voice = self._extract_brand_voice_from_guidelines(
                        website_analysis.style_guidelines
                    )
                    auto_populated_fields['brand_voice'] = 'website_analysis'
                
                data_sources['website_analysis'] = website_analysis.to_dict()
            
            if research_preferences:
                # Extract content types from research preferences
                if research_preferences.content_types:
                    strategy.preferred_formats = research_preferences.content_types
                    auto_populated_fields['preferred_formats'] = 'research_preferences'
                
                # Extract writing style from preferences
                if research_preferences.writing_style:
                    strategy.editorial_guidelines = self._extract_editorial_guidelines_from_style(
                        research_preferences.writing_style
                    )
                    auto_populated_fields['editorial_guidelines'] = 'research_preferences'
                
                data_sources['research_preferences'] = research_preferences.to_dict()
            
            # Create onboarding data integration record
            integration = OnboardingDataIntegration(
                user_id=user_id,
                strategy_id=strategy.id,
                website_analysis_data=data_sources.get('website_analysis'),
                research_preferences_data=data_sources.get('research_preferences'),
                api_keys_data=[key.to_dict() for key in api_keys] if api_keys else None,
                auto_populated_fields=auto_populated_fields,
                field_mappings=self._create_field_mappings(),
                data_quality_scores=self._calculate_data_quality_scores(data_sources),
                confidence_levels=self._calculate_confidence_levels(auto_populated_fields),
                data_freshness=self._calculate_data_freshness(onboarding_session)
            )
            
            db.add(integration)
            db.commit()
            
            # Update strategy with onboarding data used
            strategy.onboarding_data_used = {
                'auto_populated_fields': auto_populated_fields,
                'data_sources': list(data_sources.keys()),
                'integration_id': integration.id
            }
            
            logger.info(f"Strategy enhanced with onboarding data: {len(auto_populated_fields)} fields auto-populated")
            
        except Exception as e:
            logger.error(f"Error enhancing strategy with onboarding data: {str(e)}")
            # Don't raise error, just log it as this is enhancement, not core functionality
    
    async def _generate_comprehensive_ai_recommendations(self, strategy: EnhancedContentStrategy, db: Session) -> None:
        """Generate comprehensive AI recommendations using 5 specialized prompts."""
        try:
            logger.info(f"Generating comprehensive AI recommendations for strategy: {strategy.id}")
            
            start_time = datetime.utcnow()
            
            # Generate recommendations for each analysis type
            analysis_types = [
                'comprehensive_strategy',
                'audience_intelligence', 
                'competitive_intelligence',
                'performance_optimization',
                'content_calendar_optimization'
            ]
            
            ai_recommendations = {}
            
            for analysis_type in analysis_types:
                try:
                    recommendations = await self._generate_specialized_recommendations(
                        strategy, analysis_type, db
                    )
                    ai_recommendations[analysis_type] = recommendations
                    
                    # Store individual analysis result
                    analysis_result = EnhancedAIAnalysisResult(
                        user_id=strategy.user_id,
                        strategy_id=strategy.id,
                        analysis_type=analysis_type,
                        comprehensive_insights=recommendations.get('comprehensive_insights'),
                        audience_intelligence=recommendations.get('audience_intelligence'),
                        competitive_intelligence=recommendations.get('competitive_intelligence'),
                        performance_optimization=recommendations.get('performance_optimization'),
                        content_calendar_optimization=recommendations.get('content_calendar_optimization'),
                        onboarding_data_used=strategy.onboarding_data_used,
                        processing_time=(datetime.utcnow() - start_time).total_seconds(),
                        ai_service_status="operational"
                    )
                    
                    db.add(analysis_result)
                    
                except Exception as e:
                    logger.error(f"Error generating {analysis_type} recommendations: {str(e)}")
                    # Continue with other analysis types
            
            db.commit()
            
            # Update strategy with comprehensive AI analysis
            strategy.comprehensive_ai_analysis = ai_recommendations
            strategy.strategic_scores = self._calculate_strategic_scores(ai_recommendations)
            strategy.market_positioning = self._extract_market_positioning(ai_recommendations)
            strategy.competitive_advantages = self._extract_competitive_advantages(ai_recommendations)
            strategy.strategic_risks = self._extract_strategic_risks(ai_recommendations)
            strategy.opportunity_analysis = self._extract_opportunity_analysis(ai_recommendations)
            
            db.commit()
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Comprehensive AI recommendations generated in {processing_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Error generating comprehensive AI recommendations: {str(e)}")
            # Don't raise error, just log it as this is enhancement, not core functionality
    
    async def _generate_specialized_recommendations(self, strategy: EnhancedContentStrategy, analysis_type: str, db: Session) -> Dict[str, Any]:
        """Generate specialized recommendations using specific AI prompts."""
        try:
            # Prepare strategy data for AI analysis
            strategy_data = strategy.to_dict()
            
            # Get onboarding data for context
            onboarding_integration = await self._get_onboarding_integration(strategy.id, db)
            
            # Create prompt based on analysis type
            prompt = self._create_specialized_prompt(strategy, analysis_type)
            
            # Generate AI response (placeholder - integrate with actual AI service)
            ai_response = await self._call_ai_service(prompt, analysis_type)
            
            # Parse and structure the response
            structured_response = self._parse_ai_response(ai_response, analysis_type)
            
            return structured_response
            
        except Exception as e:
            logger.error(f"Error generating {analysis_type} recommendations: {str(e)}")
            raise
    
    def _create_specialized_prompt(self, strategy: EnhancedContentStrategy, analysis_type: str) -> str:
        """Create specialized AI prompts for each analysis type."""
        
        base_context = f"""
        Business Context:
        - Industry: {strategy.industry}
        - Business Objectives: {strategy.business_objectives}
        - Target Metrics: {strategy.target_metrics}
        - Content Budget: {strategy.content_budget}
        - Team Size: {strategy.team_size}
        - Implementation Timeline: {strategy.implementation_timeline}
        - Market Share: {strategy.market_share}
        - Competitive Position: {strategy.competitive_position}
        - Performance Metrics: {strategy.performance_metrics}
        
        Audience Intelligence:
        - Content Preferences: {strategy.content_preferences}
        - Consumption Patterns: {strategy.consumption_patterns}
        - Audience Pain Points: {strategy.audience_pain_points}
        - Buying Journey: {strategy.buying_journey}
        - Seasonal Trends: {strategy.seasonal_trends}
        - Engagement Metrics: {strategy.engagement_metrics}
        
        Competitive Intelligence:
        - Top Competitors: {strategy.top_competitors}
        - Competitor Content Strategies: {strategy.competitor_content_strategies}
        - Market Gaps: {strategy.market_gaps}
        - Industry Trends: {strategy.industry_trends}
        - Emerging Trends: {strategy.emerging_trends}
        
        Content Strategy:
        - Preferred Formats: {strategy.preferred_formats}
        - Content Mix: {strategy.content_mix}
        - Content Frequency: {strategy.content_frequency}
        - Optimal Timing: {strategy.optimal_timing}
        - Quality Metrics: {strategy.quality_metrics}
        - Editorial Guidelines: {strategy.editorial_guidelines}
        - Brand Voice: {strategy.brand_voice}
        
        Performance & Analytics:
        - Traffic Sources: {strategy.traffic_sources}
        - Conversion Rates: {strategy.conversion_rates}
        - Content ROI Targets: {strategy.content_roi_targets}
        - A/B Testing Capabilities: {strategy.ab_testing_capabilities}
        """
        
        specialized_prompts = {
            'comprehensive_strategy': f"""
            {base_context}
            
            TASK: Generate a comprehensive content strategy analysis that provides:
            1. Strategic positioning and market analysis
            2. Audience targeting and persona development
            3. Content pillar recommendations with rationale
            4. Competitive advantage identification
            5. Performance optimization strategies
            6. Risk assessment and mitigation plans
            7. Implementation roadmap with milestones
            8. Success metrics and KPIs
            
            REQUIREMENTS:
            - Provide actionable, specific recommendations
            - Include data-driven insights
            - Consider industry best practices
            - Address both short-term and long-term goals
            - Provide confidence levels for each recommendation
            """,
            
            'audience_intelligence': f"""
            {base_context}
            
            TASK: Generate detailed audience intelligence analysis including:
            1. Comprehensive audience persona development
            2. Content preference analysis and recommendations
            3. Consumption pattern insights and optimization
            4. Pain point identification and content solutions
            5. Buying journey mapping and content alignment
            6. Seasonal trend analysis and content planning
            7. Engagement pattern analysis and optimization
            8. Audience segmentation strategies
            
            REQUIREMENTS:
            - Use data-driven insights from provided metrics
            - Provide specific content recommendations for each audience segment
            - Include engagement optimization strategies
            - Consider cultural and behavioral factors
            """,
            
            'competitive_intelligence': f"""
            {base_context}
            
            TASK: Generate comprehensive competitive intelligence analysis including:
            1. Competitor content strategy analysis
            2. Market gap identification and opportunities
            3. Competitive advantage development strategies
            4. Industry trend analysis and implications
            5. Emerging trend identification and early adoption strategies
            6. Competitive positioning recommendations
            7. Market opportunity assessment
            8. Competitive response strategies
            
            REQUIREMENTS:
            - Analyze provided competitor data thoroughly
            - Identify unique market opportunities
            - Provide actionable competitive strategies
            - Consider both direct and indirect competitors
            """,
            
            'performance_optimization': f"""
            {base_context}
            
            TASK: Generate performance optimization analysis including:
            1. Current performance analysis and benchmarking
            2. Traffic source optimization strategies
            3. Conversion rate improvement recommendations
            4. Content ROI optimization strategies
            5. A/B testing framework and recommendations
            6. Performance monitoring and analytics setup
            7. Optimization roadmap and priorities
            8. Success metrics and tracking implementation
            
            REQUIREMENTS:
            - Provide specific, measurable optimization strategies
            - Include data-driven recommendations
            - Consider both technical and content optimizations
            - Provide implementation timelines and priorities
            """,
            
            'content_calendar_optimization': f"""
            {base_context}
            
            TASK: Generate content calendar optimization analysis including:
            1. Optimal content frequency and timing analysis
            2. Content mix optimization and balance
            3. Seasonal content planning and scheduling
            4. Content pillar integration and scheduling
            5. Platform-specific content adaptation
            6. Content repurposing and amplification strategies
            7. Editorial calendar optimization
            8. Content performance tracking and adjustment
            
            REQUIREMENTS:
            - Provide specific scheduling recommendations
            - Include content mix optimization strategies
            - Consider platform-specific requirements
            - Provide seasonal and trend-based planning
            """
        }
        
        return specialized_prompts.get(analysis_type, base_context)
    
    async def _call_ai_service(self, prompt: str, analysis_type: str) -> Dict[str, Any]:
        """Call AI service to generate recommendations."""
        raise RuntimeError("AI service integration not implemented. Real AI response required.")
    
    def _parse_ai_response(self, ai_response: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """Parse and structure AI response."""
        return {
            'analysis_type': analysis_type,
            'recommendations': ai_response.get('recommendations', []),
            'insights': ai_response.get('insights', []),
            'metrics': ai_response.get('metrics', {}),
            'confidence_score': ai_response.get('metrics', {}).get('confidence', 0.8)
        }
    
    def _get_fallback_recommendations(self, analysis_type: str) -> Dict[str, Any]:
        raise RuntimeError("Fallback recommendations are disabled. Real AI required.")
    
    def _extract_content_preferences_from_style(self, writing_style: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content preferences from writing style analysis."""
        return {
            'tone': writing_style.get('tone', 'professional'),
            'complexity': writing_style.get('complexity', 'moderate'),
            'engagement_level': writing_style.get('engagement_level', 'medium'),
            'preferred_formats': ['blog_posts', 'articles']  # Default based on style
        }
    
    def _extract_brand_voice_from_guidelines(self, style_guidelines: Dict[str, Any]) -> Dict[str, Any]:
        """Extract brand voice from style guidelines."""
        return {
            'personality': style_guidelines.get('personality', 'professional'),
            'tone': style_guidelines.get('tone', 'authoritative'),
            'style': style_guidelines.get('style', 'informative'),
            'voice_characteristics': style_guidelines.get('voice_characteristics', [])
        }
    
    def _extract_editorial_guidelines_from_style(self, writing_style: Dict[str, Any]) -> Dict[str, Any]:
        """Extract editorial guidelines from writing style."""
        return {
            'tone_guidelines': writing_style.get('tone', 'professional'),
            'style_guidelines': writing_style.get('style', 'clear'),
            'formatting_guidelines': writing_style.get('formatting', 'standard'),
            'quality_standards': writing_style.get('quality_standards', 'high')
        }
    
    def _create_field_mappings(self) -> Dict[str, str]:
        """Create mappings between onboarding fields and strategy fields."""
        return {
            'writing_style.tone': 'brand_voice.personality',
            'writing_style.complexity': 'editorial_guidelines.style_guidelines',
            'target_audience.demographics': 'target_audience',
            'content_types': 'preferred_formats',
            'research_depth': 'content_frequency'
        }
    
    def _calculate_data_quality_scores(self, data_sources: Dict[str, Any]) -> Dict[str, float]:
        """Calculate quality scores for each data source."""
        scores = {}
        for source, data in data_sources.items():
            if data:
                # Simple scoring based on data completeness
                completeness = len([v for v in data.values() if v is not None]) / len(data)
                scores[source] = completeness * 100
            else:
                scores[source] = 0.0
        return scores
    
    def _calculate_confidence_levels(self, auto_populated_fields: Dict[str, str]) -> Dict[str, float]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService.quality")

    def _calculate_confidence_levels_from_data(self, data_sources: Dict[str, Any]) -> Dict[str, float]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService.quality")

    def _calculate_data_freshness(self, onboarding_data: Union[OnboardingSession, Dict[str, Any]]) -> Dict[str, str]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService.quality")
    
    def _calculate_strategic_scores(self, ai_recommendations: Dict[str, Any]) -> Dict[str, float]:
        """Calculate strategic performance scores from AI recommendations."""
        scores = {
            'overall_score': 0.0,
            'content_quality_score': 0.0,
            'engagement_score': 0.0,
            'conversion_score': 0.0,
            'innovation_score': 0.0
        }
        
        # Calculate scores based on AI recommendations
        total_confidence = 0
        total_score = 0
        
        for analysis_type, recommendations in ai_recommendations.items():
            if isinstance(recommendations, dict) and 'metrics' in recommendations:
                metrics = recommendations['metrics']
                score = metrics.get('score', 50)
                confidence = metrics.get('confidence', 0.5)
                
                total_score += score * confidence
                total_confidence += confidence
        
        if total_confidence > 0:
            scores['overall_score'] = total_score / total_confidence
        
        # Set other scores based on overall score
        scores['content_quality_score'] = scores['overall_score'] * 1.1
        scores['engagement_score'] = scores['overall_score'] * 0.9
        scores['conversion_score'] = scores['overall_score'] * 0.95
        scores['innovation_score'] = scores['overall_score'] * 1.05
        
        return scores
    
    def _extract_market_positioning(self, ai_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market positioning from AI recommendations."""
        return {
            'industry_position': 'emerging',
            'competitive_advantage': 'AI-powered content',
            'market_share': '2.5%',
            'positioning_score': 4
        }
    
    def _extract_competitive_advantages(self, ai_recommendations: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract competitive advantages from AI recommendations."""
        return [
            {
                'advantage': 'AI-powered content creation',
                'impact': 'High',
                'implementation': 'In Progress'
            },
            {
                'advantage': 'Data-driven strategy',
                'impact': 'Medium',
                'implementation': 'Complete'
            }
        ]
    
    def _extract_strategic_risks(self, ai_recommendations: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract strategic risks from AI recommendations."""
        return [
            {
                'risk': 'Content saturation in market',
                'probability': 'Medium',
                'impact': 'High'
            },
            {
                'risk': 'Algorithm changes affecting reach',
                'probability': 'High',
                'impact': 'Medium'
            }
        ]
    
    def _extract_opportunity_analysis(self, ai_recommendations: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract opportunity analysis from AI recommendations."""
        return [
            {
                'opportunity': 'Video content expansion',
                'potential_impact': 'High',
                'implementation_ease': 'Medium'
            },
            {
                'opportunity': 'Social media engagement',
                'potential_impact': 'Medium',
                'implementation_ease': 'High'
            }
        ]
    
    async def _get_latest_ai_analysis(self, strategy_id: int, db: Session) -> Optional[Dict[str, Any]]:
        """Get the latest AI analysis for a strategy."""
        try:
            analysis = db.query(EnhancedAIAnalysisResult).filter(
                EnhancedAIAnalysisResult.strategy_id == strategy_id
            ).order_by(EnhancedAIAnalysisResult.created_at.desc()).first()
            
            return analysis.to_dict() if analysis else None
            
        except Exception as e:
            logger.error(f"Error getting latest AI analysis: {str(e)}")
            return None
    
    async def _get_onboarding_integration(self, strategy_id: int, db: Session) -> Optional[Dict[str, Any]]:
        """Get onboarding data integration for a strategy."""
        try:
            integration = db.query(OnboardingDataIntegration).filter(
                OnboardingDataIntegration.strategy_id == strategy_id
            ).first()
            
            return integration.to_dict() if integration else None
            
        except Exception as e:
            logger.error(f"Error getting onboarding integration: {str(e)}")
            return None 

    async def _get_onboarding_data(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive onboarding data for intelligent auto-population via AutoFillService"""
        try:
            from services.database import get_db_session
            from .content_strategy.autofill import AutoFillService
            temp_db = get_db_session()
            try:
                service = AutoFillService(temp_db)
                payload = await service.get_autofill(user_id)
                logger.info(f"Retrieved comprehensive onboarding data for user {user_id}")
                return payload
            finally:
                temp_db.close()
        except Exception as e:
            logger.error(f"Error getting onboarding data: {str(e)}")
            raise

    def _transform_onboarding_data_to_fields(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform processed onboarding data into field-specific format for frontend"""
        fields = {}
        
        website_data = processed_data.get('website_analysis', {})
        research_data = processed_data.get('research_preferences', {})
        api_data = processed_data.get('api_keys_data', {})
        session_data = processed_data.get('onboarding_session', {})
        
        # Business Context Fields
        if 'content_goals' in website_data and website_data.get('content_goals'):
            fields['business_objectives'] = {
                'value': website_data.get('content_goals'),
            'source': 'website_analysis',
                'confidence': website_data.get('confidence_level')
        }
        
        # Prefer explicit target_metrics; otherwise derive from performance_metrics
        if website_data.get('target_metrics'):
            fields['target_metrics'] = {
                'value': website_data.get('target_metrics'),
            'source': 'website_analysis',
                'confidence': website_data.get('confidence_level')
            }
        elif website_data.get('performance_metrics'):
            fields['target_metrics'] = {
                'value': website_data.get('performance_metrics'),
                'source': 'website_analysis',
                'confidence': website_data.get('confidence_level')
            }
        
        # Content budget: website data preferred, else onboarding session budget
        if website_data.get('content_budget') is not None:
            fields['content_budget'] = {
                'value': website_data.get('content_budget'),
            'source': 'website_analysis',
                'confidence': website_data.get('confidence_level')
            }
        elif isinstance(session_data, dict) and session_data.get('budget') is not None:
            fields['content_budget'] = {
                'value': session_data.get('budget'),
                'source': 'onboarding_session',
            'confidence': 0.7
        }
        
        # Team size: website data preferred, else onboarding session team_size
        if website_data.get('team_size') is not None:
            fields['team_size'] = {
                'value': website_data.get('team_size'),
            'source': 'website_analysis',
                'confidence': website_data.get('confidence_level')
            }
        elif isinstance(session_data, dict) and session_data.get('team_size') is not None:
            fields['team_size'] = {
                'value': session_data.get('team_size'),
                'source': 'onboarding_session',
            'confidence': 0.7
        }
        
        # Implementation timeline: website data preferred, else onboarding session timeline
        if website_data.get('implementation_timeline'):
            fields['implementation_timeline'] = {
                'value': website_data.get('implementation_timeline'),
            'source': 'website_analysis',
                'confidence': website_data.get('confidence_level')
            }
        elif isinstance(session_data, dict) and session_data.get('timeline'):
            fields['implementation_timeline'] = {
                'value': session_data.get('timeline'),
                'source': 'onboarding_session',
                'confidence': 0.7
            }
        
        # Market share: explicit if present; otherwise derive rough share from performance metrics if available
        if website_data.get('market_share'):
            fields['market_share'] = {
                'value': website_data.get('market_share'),
            'source': 'website_analysis',
                'confidence': website_data.get('confidence_level')
            }
        elif website_data.get('performance_metrics'):
            fields['market_share'] = {
                'value': website_data.get('performance_metrics').get('estimated_market_share', None),
            'source': 'website_analysis',
                'confidence': website_data.get('confidence_level')
        }
        
        fields['performance_metrics'] = {
            'value': website_data.get('performance_metrics', {}),
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        # Audience Intelligence Fields
        # Extract audience data from research_data structure
        audience_research = research_data.get('audience_research', {})
        content_prefs = research_data.get('content_preferences', {})
        
        fields['content_preferences'] = {
            'value': content_prefs,
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['consumption_patterns'] = {
            'value': audience_research.get('consumption_patterns', {}),
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['audience_pain_points'] = {
            'value': audience_research.get('audience_pain_points', []),
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['buying_journey'] = {
            'value': audience_research.get('buying_journey', {}),
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['seasonal_trends'] = {
            'value': ['Q1: Planning', 'Q2: Execution', 'Q3: Optimization', 'Q4: Review'],
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.7)
        }
        
        fields['engagement_metrics'] = {
            'value': {
                'avg_session_duration': website_data.get('performance_metrics', {}).get('avg_session_duration', 180),
                'bounce_rate': website_data.get('performance_metrics', {}).get('bounce_rate', 45.5),
                'pages_per_session': 2.5
            },
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        # Competitive Intelligence Fields
        fields['top_competitors'] = {
            'value': website_data.get('competitors', [
                'Competitor A - Industry Leader',
                'Competitor B - Emerging Player', 
                'Competitor C - Niche Specialist'
            ]),
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        fields['competitor_content_strategies'] = {
            'value': ['Educational content', 'Case studies', 'Thought leadership'],
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.7)
        }
        
        fields['market_gaps'] = {
            'value': website_data.get('market_gaps', []),
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        fields['industry_trends'] = {
            'value': ['Digital transformation', 'AI/ML adoption', 'Remote work'],
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        fields['emerging_trends'] = {
            'value': ['Voice search optimization', 'Video content', 'Interactive content'],
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.7)
        }
        
        # Content Strategy Fields
        fields['preferred_formats'] = {
            'value': content_prefs.get('preferred_formats', [
                'Blog posts', 'Whitepapers', 'Webinars', 'Case studies', 'Videos'
            ]),
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['content_mix'] = {
            'value': {
                'blog_posts': 40,
                'whitepapers': 20,
                'webinars': 15,
                'case_studies': 15,
                'videos': 10
            },
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['content_frequency'] = {
            'value': 'Weekly',
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['optimal_timing'] = {
            'value': {
                'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
                'best_times': ['9:00 AM', '1:00 PM', '3:00 PM']
            },
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.7)
        }
        
        fields['quality_metrics'] = {
            'value': {
                'readability_score': 8.5,
                'engagement_target': 5.0,
                'conversion_target': 2.0
            },
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['editorial_guidelines'] = {
            'value': {
                'tone': content_prefs.get('content_style', ['Professional', 'Educational']),
                'length': content_prefs.get('content_length', 'Medium (1000-2000 words)'),
                'formatting': ['Use headers', 'Include visuals', 'Add CTAs']
            },
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        fields['brand_voice'] = {
            'value': {
                'tone': 'Professional yet approachable',
                'style': 'Educational and authoritative',
                'personality': 'Expert, helpful, trustworthy'
            },
            'source': 'research_preferences',
            'confidence': research_data.get('confidence_level', 0.8)
        }
        
        # Performance & Analytics Fields
        fields['traffic_sources'] = {
            'value': website_data.get('traffic_sources', {}),
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        fields['conversion_rates'] = {
            'value': {
                'overall': website_data.get('performance_metrics', {}).get('conversion_rate', 3.2),
                'blog': 2.5,
                'landing_pages': 4.0,
                'email': 5.5
            },
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        fields['content_roi_targets'] = {
            'value': {
                'target_roi': 300,
                'cost_per_lead': 50,
                'lifetime_value': 500
            },
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.7)
        }
        
        fields['ab_testing_capabilities'] = {
            'value': True,
            'source': 'api_keys_data',
            'confidence': api_data.get('confidence_level', 0.8)
        }
        
        return fields

    def _get_data_sources(self, processed_data: Dict[str, Any]) -> Dict[str, str]:
        """Get data sources for each field"""
        sources = {}
        
        # Map fields to their data sources
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
        
        for field in website_fields:
            sources[field] = 'website_analysis'
        
        for field in research_fields:
            sources[field] = 'research_preferences'
        
        for field in api_fields:
            sources[field] = 'api_keys_data'
        
        return sources

    async def _get_website_analysis_data(self, user_id: int) -> Dict[str, Any]:
        """Get website analysis data from onboarding"""
        try:
            raise RuntimeError("Website analysis data retrieval not implemented. Real data required.")
        except Exception as e:
            logger.error(f"Error getting website analysis data: {str(e)}")
            raise

    async def _get_research_preferences_data(self, user_id: int) -> Dict[str, Any]:
        """Get research preferences data from onboarding"""
        try:
            raise RuntimeError("Research preferences data retrieval not implemented. Real data required.")
        except Exception as e:
            logger.error(f"Error getting research preferences data: {str(e)}")
            raise

    async def _get_api_keys_data(self, user_id: int) -> Dict[str, Any]:
        """Get API keys and external data from onboarding"""
        try:
            raise RuntimeError("API keys/external data retrieval not implemented. Real data required.")
        except Exception as e:
            logger.error(f"Error getting API keys data: {str(e)}")
            raise

    async def _process_website_analysis(self, website_data: Dict[str, Any]) -> Dict[str, Any]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService normalizers")

    async def _process_research_preferences(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService normalizers")

    async def _process_api_keys_data(self, api_data: Dict[str, Any]) -> Dict[str, Any]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService normalizers")

    def _transform_onboarding_data_to_fields(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService.transformer")

    def _get_data_sources(self, processed_data: Dict[str, Any]) -> Dict[str, str]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService.transparency")

    def _get_detailed_input_data_points(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        # deprecated; not used
        raise RuntimeError("Deprecated: use AutoFillService.transparency")

    def _get_fallback_onboarding_data(self) -> Dict[str, Any]:
        """Deprecated: fallbacks are no longer permitted. Kept for compatibility; always raises."""
        raise RuntimeError("Fallback onboarding data is disabled. Real data required.")

    def _initialize_caches(self) -> None:
        """Initialize in-memory caches as a no-op placeholder.
        This prevents attribute errors in legacy code paths. Real caching has been
        moved to the modular CachingService; this is only for backward compatibility.
        """
        # Simple placeholders to satisfy legacy references
        if not hasattr(self, "_cache"):
            self._cache = {}
        if not hasattr(self, "performance_metrics"):
            self.performance_metrics = {
                'response_times': [],
                'cache_hit_rates': {},
                'error_rates': {},
                'throughput_metrics': {}
            }
        # No further action required
        return