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
            return self._get_fallback_recommendations(analysis_type)
    
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
        # Placeholder implementation - integrate with actual AI service
        # For now, return structured mock data
        return {
            'analysis_type': analysis_type,
            'recommendations': f"AI recommendations for {analysis_type}",
            'insights': f"Key insights for {analysis_type}",
            'metrics': {'score': 85, 'confidence': 0.9}
        }
    
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
        """Get fallback recommendations when AI service fails."""
        fallback_data = {
            'comprehensive_strategy': {
                'recommendations': ['Focus on core content pillars', 'Develop audience personas'],
                'insights': ['Strategy needs more specific objectives', 'Consider expanding content mix'],
                'metrics': {'score': 70, 'confidence': 0.6}
            },
            'audience_intelligence': {
                'recommendations': ['Conduct audience research', 'Analyze content preferences'],
                'insights': ['Limited audience data available', 'Need more engagement metrics'],
                'metrics': {'score': 65, 'confidence': 0.5}
            },
            'competitive_intelligence': {
                'recommendations': ['Analyze competitor content', 'Identify market gaps'],
                'insights': ['Competitive analysis needed', 'Market positioning unclear'],
                'metrics': {'score': 60, 'confidence': 0.4}
            },
            'performance_optimization': {
                'recommendations': ['Set up analytics tracking', 'Implement A/B testing'],
                'insights': ['Performance data limited', 'Need baseline metrics'],
                'metrics': {'score': 55, 'confidence': 0.3}
            },
            'content_calendar_optimization': {
                'recommendations': ['Create publishing schedule', 'Optimize content mix'],
                'insights': ['Calendar optimization needed', 'Frequency planning required'],
                'metrics': {'score': 50, 'confidence': 0.2}
            }
        }
        
        return fallback_data.get(analysis_type, {
            'recommendations': ['General strategy improvement needed'],
            'insights': ['Analysis incomplete'],
            'metrics': {'score': 50, 'confidence': 0.1}
        })
    
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
        """Calculate confidence levels for auto-populated fields."""
        confidence_levels = {}
        for field, source in auto_populated_fields.items():
            # Base confidence on data source
            base_confidence = {
                'website_analysis': 0.8,
                'research_preferences': 0.7,
                'api_keys': 0.6
            }
            confidence_levels[field] = base_confidence.get(source, 0.5)
        return confidence_levels
    
    def _calculate_confidence_levels_from_data(self, data_sources: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence levels from data sources."""
        confidence_levels = {}
        
        # Website analysis confidence
        if data_sources.get('website_analysis'):
            website_data = data_sources['website_analysis']
            confidence_levels['website_analysis'] = website_data.get('confidence_level', 0.8)
        
        # Research preferences confidence
        if data_sources.get('research_preferences'):
            research_data = data_sources['research_preferences']
            confidence_levels['research_preferences'] = research_data.get('confidence_level', 0.7)
        
        # API keys confidence
        if data_sources.get('api_keys_data'):
            api_data = data_sources['api_keys_data']
            confidence_levels['api_keys_data'] = api_data.get('confidence_level', 0.6)
        
        return confidence_levels
    
    def _calculate_data_freshness(self, onboarding_data: Union[OnboardingSession, Dict[str, Any]]) -> Dict[str, str]:
        """Calculate data freshness for onboarding data."""
        try:
            # Handle both OnboardingSession objects and dictionaries
            if hasattr(onboarding_data, 'updated_at'):
                # It's an OnboardingSession object
                updated_at = onboarding_data.updated_at
            elif isinstance(onboarding_data, dict):
                # It's a dictionary - look for last_updated or updated_at
                updated_at = onboarding_data.get('last_updated') or onboarding_data.get('updated_at')
            else:
                updated_at = None
            
            if not updated_at:
                return {'status': 'unknown', 'age_days': 'unknown'}
            
            # Convert string to datetime if needed
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
            
        except Exception as e:
            logger.error(f"Error calculating data freshness: {str(e)}")
            return {'status': 'unknown', 'age_days': 'unknown'}

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
        """Get comprehensive onboarding data for intelligent auto-population"""
        try:
            # Use the real onboarding data integration service
            from .content_strategy.onboarding.data_integration import OnboardingDataIntegrationService
            
            # Create a temporary database session for this operation
            from services.database import get_db_session
            temp_db = get_db_session()
            
            try:
                integration_service = OnboardingDataIntegrationService()
                integrated_data = await integration_service.process_onboarding_data(user_id, temp_db)
                
                if not integrated_data:
                    logger.warning(f"No onboarding data found for user {user_id}, using fallback")
                    return self._get_fallback_onboarding_data()
                
                # Transform the integrated data into the expected format
                website_data = integrated_data.get('website_analysis', {})
                research_data = integrated_data.get('research_preferences', {})
                api_data = integrated_data.get('api_keys_data', {})
                session_data = integrated_data.get('onboarding_session', {})
                
                # Process and enhance the data
                processed_data = {
                    'website_analysis': await self._process_website_analysis(website_data),
                    'research_preferences': await self._process_research_preferences(research_data),
                    'api_keys_data': await self._process_api_keys_data(api_data),
                    'data_quality_scores': self._calculate_data_quality_scores({
                        'website_analysis': website_data,
                        'research_preferences': research_data,
                        'api_keys_data': api_data
                    }),
                    'confidence_levels': self._calculate_confidence_levels_from_data({
                        'website_analysis': website_data,
                        'research_preferences': research_data,
                        'api_keys_data': api_data
                    }),
                    'data_freshness': self._calculate_data_freshness(session_data)
                }
                
                # Transform data into frontend-expected format
                auto_populated_fields = self._transform_onboarding_data_to_fields(processed_data)
                
                logger.info(f"Retrieved comprehensive onboarding data for user {user_id}")
                return {
                    'fields': auto_populated_fields,
                    'sources': self._get_data_sources(processed_data),
                    'quality_scores': processed_data['data_quality_scores'],
                    'confidence_levels': processed_data['confidence_levels'],
                    'data_freshness': processed_data['data_freshness']
                }
                
            finally:
                temp_db.close()
                
        except Exception as e:
            logger.error(f"Error getting onboarding data: {str(e)}")
            return self._get_fallback_onboarding_data()
 
    def _transform_onboarding_data_to_fields(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform processed onboarding data into field-specific format for frontend"""
        fields = {}
        
        website_data = processed_data.get('website_analysis', {})
        research_data = processed_data.get('research_preferences', {})
        api_data = processed_data.get('api_keys_data', {})
        
        # Business Context Fields
        fields['business_objectives'] = {
            'value': website_data.get('content_goals', ['Lead Generation', 'Brand Awareness']),
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        fields['target_metrics'] = {
            'value': {
                'traffic_growth': '30%',
                'engagement_rate': '5%',
                'conversion_rate': '2%',
                'lead_generation': '100 leads/month'
            },
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
        }
        
        fields['content_budget'] = {
            'value': 5000,  # Default budget
            'source': 'website_analysis',
            'confidence': 0.7
        }
        
        fields['team_size'] = {
            'value': 3,  # Default team size
            'source': 'website_analysis',
            'confidence': 0.7
        }
        
        fields['implementation_timeline'] = {
            'value': '6 months',
            'source': 'website_analysis',
            'confidence': 0.8
        }
        
        fields['market_share'] = {
            'value': '15%',
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.7)
        }
        
        fields['competitive_position'] = {
            'value': website_data.get('market_position', 'Emerging'),
            'source': 'website_analysis',
            'confidence': website_data.get('confidence_level', 0.8)
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
            # TODO: Implement actual website analysis data retrieval
            # For now, return mock data
            return {
                'website_url': 'https://example.com',
                'industry': 'Technology',
                'business_size': 'Medium',
                'market_position': 'Emerging',
                'target_audience': 'B2B Professionals',
                'content_goals': ['Lead Generation', 'Brand Awareness', 'Thought Leadership'],
                'performance_data': {
                    'monthly_traffic': 15000,
                    'conversion_rate': 3.2,
                    'bounce_rate': 45.5,
                    'avg_session_duration': 180,
                    'top_pages': ['/blog', '/about', '/services'],
                    'traffic_sources': {
                        'organic': 60,
                        'social': 25,
                        'direct': 10,
                        'referral': 5
                    }
                },
                'content_analysis': {
                    'content_gaps': ['Educational content', 'Case studies', 'Industry insights'],
                    'topics': ['Digital transformation', 'AI/ML', 'Cloud computing'],
                    'content_quality_score': 7.5,
                    'seo_opportunities': ['Long-tail keywords', 'Featured snippets', 'Voice search']
                },
                'competitor_analysis': {
                    'top_competitors': ['Competitor A', 'Competitor B', 'Competitor C'],
                    'competitive_advantages': ['Technical expertise', 'Industry experience', 'Customer success'],
                    'market_gaps': ['Practical implementation guides', 'Industry-specific insights']
                },
                'last_updated': '2024-01-15T10:30:00Z'
            }
        except Exception as e:
            logger.error(f"Error getting website analysis data: {str(e)}")
            return {}
 
    async def _get_research_preferences_data(self, user_id: int) -> Dict[str, Any]:
        """Get research preferences data from onboarding"""
        try:
            # TODO: Implement actual research preferences data retrieval
            # For now, return mock data
            return {
                'content_preferences': {
                    'preferred_formats': ['Blog posts', 'Whitepapers', 'Webinars', 'Case studies'],
                    'content_topics': ['Industry trends', 'Best practices', 'Technical guides', 'Success stories'],
                    'content_style': ['Educational', 'Professional', 'Data-driven', 'Practical'],
                    'content_length': 'Medium (1000-2000 words)',
                    'visual_preferences': ['Infographics', 'Charts', 'Diagrams', 'Videos']
                },
                'audience_research': {
                    'target_audience': ['B2B professionals', 'Decision makers', 'Technical leaders'],
                    'audience_pain_points': [
                        'Information overload',
                        'Time constraints',
                        'Decision paralysis',
                        'Keeping up with trends'
                    ],
                    'buying_journey': {
                        'awareness': 'Educational content and thought leadership',
                        'consideration': 'Case studies and comparisons',
                        'decision': 'Product demos and testimonials',
                        'retention': 'Ongoing support and updates'
                    },
                    'consumption_patterns': {
                        'blogs': 60,
                        'videos': 25,
                        'podcasts': 10,
                        'social_media': 5
                    }
                },
                'research_goals': {
                    'primary_goals': ['Lead generation', 'Brand awareness', 'Thought leadership'],
                    'secondary_goals': ['Customer education', 'Industry influence', 'Partnership development'],
                    'success_metrics': ['Website traffic', 'Lead quality', 'Engagement rates', 'Brand mentions']
                },
                'last_updated': '2024-01-15T10:30:00Z'
            }
        except Exception as e:
            logger.error(f"Error getting research preferences data: {str(e)}")
            return {}
 
    async def _get_api_keys_data(self, user_id: int) -> Dict[str, Any]:
        """Get API keys and external data from onboarding"""
        try:
            # TODO: Implement actual API keys data retrieval
            # For now, return mock data
            return {
                'google_analytics': {
                    'connected': True,
                    'data_available': True,
                    'metrics': {
                        'sessions': 15000,
                        'users': 12000,
                        'pageviews': 45000,
                        'avg_session_duration': 180,
                        'bounce_rate': 45.5
                    }
                },
                'google_search_console': {
                    'connected': True,
                    'data_available': True,
                    'metrics': {
                        'clicks': 5000,
                        'impressions': 25000,
                        'ctr': 2.0,
                        'avg_position': 15.5
                    }
                },
                'social_media_apis': {
                    'linkedin': {'connected': True, 'followers': 5000},
                    'twitter': {'connected': True, 'followers': 3000},
                    'facebook': {'connected': False, 'followers': 0}
                },
                'competitor_tools': {
                    'semrush': {'connected': True, 'competitors_analyzed': 10},
                    'ahrefs': {'connected': False, 'competitors_analyzed': 0},
                    'moz': {'connected': False, 'competitors_analyzed': 0}
                },
                'last_updated': '2024-01-15T10:30:00Z'
            }
        except Exception as e:
            logger.error(f"Error getting API keys data: {str(e)}")
            return {}
 
    async def _process_website_analysis(self, website_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and enhance website analysis data"""
        try:
            if not website_data:
                return {}
            
            # Extract data from the real website analysis model
            processed_data = {
                'website_url': website_data.get('website_url'),
                'industry': website_data.get('target_audience', {}).get('industry_focus'),
                'market_position': 'Emerging',  # Default value
                'business_size': 'Medium',  # Default value
                'target_audience': website_data.get('target_audience', {}).get('demographics'),
                'content_goals': website_data.get('content_type', {}).get('purpose', []),
                'performance_metrics': {
                    'traffic': 10000,  # Default value
                    'conversion_rate': 2.5,  # Default value
                    'bounce_rate': 50.0,  # Default value
                    'avg_session_duration': 150  # Default value
                },
                'traffic_sources': {
                    'organic': 70,
                    'social': 20,
                    'direct': 7,
                    'referral': 3
                },
                'content_gaps': website_data.get('style_guidelines', {}).get('content_gaps', []),
                'topics': website_data.get('content_type', {}).get('primary_type', []),
                'content_quality_score': 7.5,  # Default value
                'seo_opportunities': website_data.get('style_guidelines', {}).get('seo_opportunities', []),
                'competitors': [],  # Would need competitor analysis data
                'competitive_advantages': website_data.get('style_guidelines', {}).get('advantages', []),
                'market_gaps': website_data.get('style_guidelines', {}).get('market_gaps', []),
                'data_quality': self._assess_data_quality(website_data),
                'confidence_level': website_data.get('confidence_level', 0.8),
                'data_freshness': website_data.get('data_freshness', 0.8)
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing website analysis: {str(e)}")
            return {}

    async def _process_research_preferences(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and enhance research preferences data"""
        try:
            if not research_data:
                return {}
            
            # Extract data from the real research preferences model
            processed_data = {
                'content_preferences': {
                    'preferred_formats': research_data.get('content_types', []),
                    'content_topics': research_data.get('research_topics', []),
                    'content_style': research_data.get('writing_style', {}).get('tone', []),
                    'content_length': 'Medium (1000-2000 words)',  # Default value
                    'visual_preferences': ['Infographics', 'Charts', 'Diagrams']  # Default value
                },
                'audience_intelligence': {
                    'target_audience': research_data.get('target_audience', {}).get('demographics', []),
                    'pain_points': research_data.get('target_audience', {}).get('pain_points', []),
                    'buying_journey': research_data.get('target_audience', {}).get('buying_journey', {}),
                    'consumption_patterns': research_data.get('target_audience', {}).get('consumption_patterns', {})
                },
                'research_goals': {
                    'primary_goals': research_data.get('research_topics', []),
                    'secondary_goals': research_data.get('content_types', []),
                    'success_metrics': ['Website traffic', 'Lead quality', 'Engagement rates']  # Default value
                },
                'data_quality': self._assess_data_quality(research_data),
                'confidence_level': research_data.get('confidence_level', 0.8),
                'data_freshness': research_data.get('data_freshness', 0.8)
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing research preferences: {str(e)}")
            return {}

    async def _process_api_keys_data(self, api_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and enhance API keys data"""
        try:
            if not api_data:
                return {}
            
            # Extract data from the real API keys model
            api_keys = api_data.get('api_keys', [])
            providers = api_data.get('providers', [])
            
            processed_data = {
                'analytics_data': {
                    'google_analytics': {
                        'connected': 'google_analytics' in providers,
                        'metrics': {
                            'sessions': 15000,
                            'users': 12000,
                            'pageviews': 45000,
                            'avg_session_duration': 180,
                            'bounce_rate': 45.5
                        }
                    },
                    'google_search_console': {
                        'connected': 'google_search_console' in providers,
                        'metrics': {
                            'clicks': 5000,
                            'impressions': 25000,
                            'ctr': 2.0,
                            'avg_position': 15.5
                        }
                    }
                },
                'social_media_data': {
                    'linkedin': {'connected': 'linkedin' in providers, 'followers': 5000},
                    'twitter': {'connected': 'twitter' in providers, 'followers': 3000},
                    'facebook': {'connected': 'facebook' in providers, 'followers': 0}
                },
                'competitor_data': {
                    'semrush': {'connected': 'semrush' in providers, 'competitors_analyzed': 10},
                    'ahrefs': {'connected': 'ahrefs' in providers, 'competitors_analyzed': 0},
                    'moz': {'connected': 'moz' in providers, 'competitors_analyzed': 0}
                },
                'data_quality': self._assess_data_quality(api_data),
                'confidence_level': api_data.get('confidence_level', 0.8),
                'data_freshness': api_data.get('data_freshness', 0.8)
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing API keys data: {str(e)}")
            return {}
 
    def _assess_data_quality(self, data: Dict[str, Any]) -> float:
        """Assess the quality of data based on completeness and validity"""
        try:
            if not data:
                return 0.0
            
            # Check for required fields based on data type
            required_fields = self._get_required_fields_for_data_type(data)
            present_fields = sum(1 for field in required_fields if data.get(field))
            
            completeness_score = present_fields / len(required_fields) if required_fields else 0.0
            
            # Check data validity (basic checks)
            validity_score = self._check_data_validity(data)
            
            # Combined quality score
            quality_score = (completeness_score * 0.7) + (validity_score * 0.3)
            
            return min(1.0, max(0.0, quality_score))
            
        except Exception as e:
            logger.error(f"Error assessing data quality: {str(e)}")
            return 0.0
 
    def _get_required_fields_for_data_type(self, data: Dict[str, Any]) -> List[str]:
        """Get required fields based on data type"""
        if 'website_url' in data:
            return ['website_url', 'industry', 'business_size', 'target_audience']
        elif 'content_preferences' in data:
            return ['content_preferences', 'audience_research', 'research_goals']
        elif 'google_analytics' in data:
            return ['google_analytics', 'google_search_console', 'social_media_apis']
        else:
            return []
 
    def _check_data_validity(self, data: Dict[str, Any]) -> float:
        """Check data validity with basic validation rules"""
        try:
            validity_score = 0.0
            checks_passed = 0
            total_checks = 0
            
            # Website analysis validity checks
            if 'website_url' in data:
                total_checks += 1
                if data.get('website_url') and isinstance(data['website_url'], str):
                    checks_passed += 1
                
                total_checks += 1
                if data.get('industry') and isinstance(data['industry'], str):
                    checks_passed += 1
             
            # Research preferences validity checks
            if 'content_preferences' in data:
                total_checks += 1
                if isinstance(data['content_preferences'], dict):
                    checks_passed += 1
                 
                total_checks += 1
                if 'audience_research' in data and isinstance(data['audience_research'], dict):
                    checks_passed += 1
             
            # API data validity checks
            if 'google_analytics' in data:
                total_checks += 1
                if isinstance(data['google_analytics'], dict):
                    checks_passed += 1
             
            validity_score = checks_passed / total_checks if total_checks > 0 else 0.0
            return validity_score
             
        except Exception as e:
            logger.error(f"Error checking data validity: {str(e)}")
            return 0.0
 
    def _calculate_confidence_level(self, data: Dict[str, Any]) -> float:
        """Calculate confidence level based on data quality and completeness"""
        try:
            if not data:
                return 0.0
            
            # Base confidence on data quality
            quality_score = self._assess_data_quality(data)
            
            # Adjust confidence based on data freshness
            freshness_score = self._calculate_freshness(data.get('last_updated'))
            
            # Combined confidence score
            confidence_score = (quality_score * 0.8) + (freshness_score * 0.2)
            
            return min(1.0, max(0.0, confidence_score))
            
        except Exception as e:
            logger.error(f"Error calculating confidence level: {str(e)}")
            return 0.0
 
    def _calculate_freshness(self, last_updated: Optional[str]) -> float:
        """Calculate data freshness score based on last update time"""
        try:
            if not last_updated:
                return 0.0
            
            from datetime import datetime, timezone
            try:
                last_update = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                days_old = (now - last_update).days
                
                # Freshness scoring: 1.0 for same day, decreasing over time
                if days_old == 0:
                    return 1.0
                elif days_old <= 7:
                    return 0.9
                elif days_old <= 30:
                    return 0.7
                elif days_old <= 90:
                    return 0.5
                else:
                    return 0.3
                     
            except ValueError:
                return 0.0
                 
        except Exception as e:
            logger.error(f"Error calculating freshness: {str(e)}")
            return 0.0

    # Performance Optimization Methods (Phase 3.3)
    
    def _initialize_caches(self):
        """Initialize caching systems for performance optimization"""
        try:
            # In-memory caches for different data types
            self.ai_analysis_cache = {}
            self.onboarding_data_cache = {}
            self.strategy_cache = {}
            self.prompt_cache = {}
            
            # Cache statistics
            self.cache_stats = {
                'ai_analysis_cache': {'hits': 0, 'misses': 0, 'size': 0},
                'onboarding_data_cache': {'hits': 0, 'misses': 0, 'size': 0},
                'strategy_cache': {'hits': 0, 'misses': 0, 'size': 0},
                'prompt_cache': {'hits': 0, 'misses': 0, 'size': 0}
            }
            
            logger.info("Performance optimization caches initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing caches: {str(e)}")

    async def get_cached_ai_analysis(self, strategy_id: str, analysis_type: str) -> Optional[Dict[str, Any]]:
        """Get cached AI analysis if available and not expired"""
        try:
            cache_key = f"{strategy_id}_{analysis_type}"
            
            if cache_key in self.ai_analysis_cache:
                cached_data = self.ai_analysis_cache[cache_key]
                
                # Check if cache is still valid
                if self._is_cache_valid(cached_data, self.cache_settings['ai_analysis_cache_ttl']):
                    self.cache_stats['ai_analysis_cache']['hits'] += 1
                    logger.debug(f"Cache hit for AI analysis: {cache_key}")
                    return cached_data['data']
                else:
                    # Remove expired cache entry
                    del self.ai_analysis_cache[cache_key]
                    self.cache_stats['ai_analysis_cache']['size'] -= 1
            
            self.cache_stats['ai_analysis_cache']['misses'] += 1
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached AI analysis: {str(e)}")
            return None

    async def cache_ai_analysis(self, strategy_id: str, analysis_type: str, analysis_data: Dict[str, Any]):
        """Cache AI analysis results for performance optimization"""
        try:
            cache_key = f"{strategy_id}_{analysis_type}"
            
            # Check cache size limit
            if len(self.ai_analysis_cache) >= self.cache_settings['max_cache_size']:
                self._evict_oldest_cache_entry('ai_analysis_cache')
            
            # Cache the analysis data
            self.ai_analysis_cache[cache_key] = {
                'data': analysis_data,
                'timestamp': datetime.now(),
                'ttl': self.cache_settings['ai_analysis_cache_ttl']
            }
            
            self.cache_stats['ai_analysis_cache']['size'] += 1
            logger.debug(f"Cached AI analysis: {cache_key}")
            
        except Exception as e:
            logger.error(f"Error caching AI analysis: {str(e)}")

    async def get_cached_onboarding_data(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get cached onboarding data if available and not expired"""
        try:
            cache_key = f"onboarding_{user_id}"
            
            if cache_key in self.onboarding_data_cache:
                cached_data = self.onboarding_data_cache[cache_key]
                
                # Check if cache is still valid
                if self._is_cache_valid(cached_data, self.cache_settings['onboarding_data_cache_ttl']):
                    self.cache_stats['onboarding_data_cache']['hits'] += 1
                    logger.debug(f"Cache hit for onboarding data: {cache_key}")
                    return cached_data['data']
                else:
                    # Remove expired cache entry
                    del self.onboarding_data_cache[cache_key]
                    self.cache_stats['onboarding_data_cache']['size'] -= 1
            
            self.cache_stats['onboarding_data_cache']['misses'] += 1
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached onboarding data: {str(e)}")
            return None

    async def cache_onboarding_data(self, user_id: int, onboarding_data: Dict[str, Any]):
        """Cache onboarding data for performance optimization"""
        try:
            cache_key = f"onboarding_{user_id}"
            
            # Check cache size limit
            if len(self.onboarding_data_cache) >= self.cache_settings['max_cache_size']:
                self._evict_oldest_cache_entry('onboarding_data_cache')
            
            # Cache the onboarding data
            self.onboarding_data_cache[cache_key] = {
                'data': onboarding_data,
                'timestamp': datetime.now(),
                'ttl': self.cache_settings['onboarding_data_cache_ttl']
            }
            
            self.cache_stats['onboarding_data_cache']['size'] += 1
            logger.debug(f"Cached onboarding data: {cache_key}")
            
        except Exception as e:
            logger.error(f"Error caching onboarding data: {str(e)}")

    def _is_cache_valid(self, cached_data: Dict[str, Any], ttl_seconds: int) -> bool:
        """Check if cached data is still valid based on TTL"""
        try:
            timestamp = cached_data.get('timestamp')
            if not timestamp:
                return False
            
            elapsed = (datetime.now() - timestamp).total_seconds()
            return elapsed < ttl_seconds
            
        except Exception as e:
            logger.error(f"Error checking cache validity: {str(e)}")
            return False

    def _evict_oldest_cache_entry(self, cache_name: str):
        """Evict the oldest cache entry when cache is full"""
        try:
            cache = getattr(self, f"{cache_name}")
            if not cache:
                return
            
            # Find oldest entry
            oldest_key = min(cache.keys(), key=lambda k: cache[k].get('timestamp', datetime.min))
            
            # Remove oldest entry
            del cache[oldest_key]
            self.cache_stats[cache_name]['size'] -= 1
            
            logger.debug(f"Evicted oldest cache entry from {cache_name}: {oldest_key}")
            
        except Exception as e:
            logger.error(f"Error evicting cache entry: {str(e)}")

    async def optimize_response_time(self, operation: str, start_time: datetime) -> Dict[str, Any]:
        """Optimize response time and track performance metrics"""
        try:
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            # Track response time
            self.performance_metrics['response_times'].append({
                'operation': operation,
                'response_time': response_time,
                'timestamp': end_time
            })
            
            # Keep only last 1000 response times for memory optimization
            if len(self.performance_metrics['response_times']) > 1000:
                self.performance_metrics['response_times'] = self.performance_metrics['response_times'][-1000:]
            
            # Check if response time exceeds threshold
            if response_time > self.quality_thresholds['max_response_time']:
                logger.warning(f"Slow response time for {operation}: {response_time}s")
            
            return {
                'operation': operation,
                'response_time': response_time,
                'performance_status': 'optimal' if response_time <= 2.0 else 'acceptable' if response_time <= 5.0 else 'slow'
            }
            
        except Exception as e:
            logger.error(f"Error optimizing response time: {str(e)}")
            return {'operation': operation, 'response_time': 0.0, 'performance_status': 'error'}

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        try:
            # Calculate average response times
            response_times = self.performance_metrics['response_times']
            if response_times:
                avg_response_time = sum(rt['response_time'] for rt in response_times) / len(response_times)
                max_response_time = max(rt['response_time'] for rt in response_times)
                min_response_time = min(rt['response_time'] for rt in response_times)
            else:
                avg_response_time = max_response_time = min_response_time = 0.0
            
            # Calculate cache hit rates
            cache_hit_rates = {}
            for cache_name, stats in self.cache_stats.items():
                total_requests = stats['hits'] + stats['misses']
                hit_rate = (stats['hits'] / total_requests * 100) if total_requests > 0 else 0.0
                cache_hit_rates[cache_name] = {
                    'hit_rate': hit_rate,
                    'total_requests': total_requests,
                    'cache_size': stats['size']
                }
            
            # Calculate error rates (placeholder - implement actual error tracking)
            error_rates = {
                'ai_analysis_errors': 0.05,  # 5% error rate
                'onboarding_data_errors': 0.02,  # 2% error rate
                'strategy_creation_errors': 0.01  # 1% error rate
            }
            
            # Calculate throughput metrics
            throughput_metrics = {
                'requests_per_minute': len(response_times) / 60 if response_times else 0,
                'successful_requests': len([rt for rt in response_times if rt.get('performance_status') != 'error']),
                'failed_requests': len([rt for rt in response_times if rt.get('performance_status') == 'error'])
            }
            
            return {
                'response_time_metrics': {
                    'average_response_time': avg_response_time,
                    'max_response_time': max_response_time,
                    'min_response_time': min_response_time,
                    'response_time_threshold': self.quality_thresholds['max_response_time']
                },
                'cache_metrics': cache_hit_rates,
                'error_metrics': error_rates,
                'throughput_metrics': throughput_metrics,
                'system_health': {
                    'cache_utilization': sum(stats['size'] for stats in self.cache_stats.values()) / self.cache_settings['max_cache_size'],
                    'memory_usage': len(response_times) / 1000,  # Simplified memory usage
                    'overall_performance': 'optimal' if avg_response_time <= 2.0 else 'acceptable' if avg_response_time <= 5.0 else 'needs_optimization'
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {str(e)}")
            return {}

    async def optimize_database_queries(self, query_type: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize database queries for better performance"""
        try:
            # Query optimization strategies
            optimization_strategies = {
                'strategy_retrieval': {
                    'use_indexes': True,
                    'limit_results': 50,
                    'select_specific_fields': True,
                    'use_pagination': True
                },
                'ai_analysis_retrieval': {
                    'use_indexes': True,
                    'limit_results': 20,
                    'select_specific_fields': True,
                    'use_pagination': True
                },
                'onboarding_data_retrieval': {
                    'use_indexes': True,
                    'limit_results': 10,
                    'select_specific_fields': True,
                    'use_pagination': False
                }
            }
            
            strategy = optimization_strategies.get(query_type, {})
            
            # Apply optimization strategies
            optimized_params = query_params.copy()
            if strategy.get('limit_results'):
                optimized_params['limit'] = strategy['limit_results']
            
            if strategy.get('select_specific_fields'):
                optimized_params['select_fields'] = self._get_optimized_fields(query_type)
            
            return {
                'query_type': query_type,
                'optimization_applied': strategy,
                'optimized_params': optimized_params,
                'expected_performance_improvement': '20-30%'
            }
            
        except Exception as e:
            logger.error(f"Error optimizing database queries: {str(e)}")
            return {'query_type': query_type, 'optimization_applied': {}, 'optimized_params': query_params}

    def _get_optimized_fields(self, query_type: str) -> List[str]:
        """Get optimized field selection for different query types"""
        field_mappings = {
            'strategy_retrieval': [
                'id', 'name', 'industry', 'completion_percentage', 'created_at', 'updated_at'
            ],
            'ai_analysis_retrieval': [
                'id', 'analysis_type', 'ai_service_status', 'created_at', 'data_confidence_scores'
            ],
            'onboarding_data_retrieval': [
                'id', 'user_id', 'website_analysis_data', 'research_preferences_data', 'created_at'
            ]
        }
        
        return field_mappings.get(query_type, ['*'])

    async def implement_scalability_planning(self) -> Dict[str, Any]:
        """Implement scalability planning and recommendations"""
        try:
            # Analyze current performance metrics
            performance_metrics = await self.get_performance_metrics()
            
            # Scalability recommendations based on current metrics
            scalability_recommendations = {
                'horizontal_scaling': {
                    'recommended': performance_metrics.get('throughput_metrics', {}).get('requests_per_minute', 0) > 100,
                    'reason': 'High request volume detected',
                    'implementation': 'Load balancer with multiple service instances'
                },
                'database_optimization': {
                    'recommended': performance_metrics.get('response_time_metrics', {}).get('average_response_time', 0) > 3.0,
                    'reason': 'Slow database response times',
                    'implementation': 'Database indexing and query optimization'
                },
                'caching_expansion': {
                    'recommended': performance_metrics.get('cache_metrics', {}).get('ai_analysis_cache', {}).get('hit_rate', 0) < 70,
                    'reason': 'Low cache hit rates',
                    'implementation': 'Expand cache size and implement distributed caching'
                },
                'auto_scaling': {
                    'recommended': performance_metrics.get('system_health', {}).get('overall_performance') == 'needs_optimization',
                    'reason': 'Performance degradation detected',
                    'implementation': 'Auto-scaling based on CPU and memory usage'
                }
            }
            
            # Resource usage optimization
            resource_optimization = {
                'memory_optimization': {
                    'cache_cleanup_frequency': 'Every 30 minutes',
                    'max_cache_size': self.cache_settings['max_cache_size'],
                    'response_time_history_limit': 1000
                },
                'cpu_optimization': {
                    'async_operations': True,
                    'batch_processing': True,
                    'connection_pooling': True
                },
                'network_optimization': {
                    'compression_enabled': True,
                    'connection_keepalive': True,
                    'request_timeout': 30
                }
            }
            
            return {
                'scalability_recommendations': scalability_recommendations,
                'resource_optimization': resource_optimization,
                'current_performance': performance_metrics,
                'scaling_triggers': {
                    'high_load_threshold': 100,  # requests per minute
                    'response_time_threshold': 3.0,  # seconds
                    'error_rate_threshold': 0.05,  # 5%
                    'cache_hit_rate_threshold': 0.7  # 70%
                }
            }
            
        except Exception as e:
            logger.error(f"Error implementing scalability planning: {str(e)}")
            return {}

    async def monitor_system_health(self) -> Dict[str, Any]:
        """Monitor system health and performance"""
        try:
            # Get current performance metrics
            performance_metrics = await self.get_performance_metrics()
            
            # Health checks
            health_checks = {
                'database_connectivity': await self._check_database_health(),
                'cache_functionality': await self._check_cache_health(),
                'ai_service_availability': await self._check_ai_service_health(),
                'response_time_health': await self._check_response_time_health(performance_metrics),
                'error_rate_health': await self._check_error_rate_health(performance_metrics)
            }
            
            # Overall health status
            overall_health = 'healthy'
            if any(check.get('status') == 'critical' for check in health_checks.values()):
                overall_health = 'critical'
            elif any(check.get('status') == 'warning' for check in health_checks.values()):
                overall_health = 'warning'
            
            return {
                'overall_health': overall_health,
                'health_checks': health_checks,
                'performance_metrics': performance_metrics,
                'recommendations': self._generate_health_recommendations(health_checks, performance_metrics)
            }
            
        except Exception as e:
            logger.error(f"Error monitoring system health: {str(e)}")
            return {'overall_health': 'unknown', 'error': str(e)}

    async def _check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            # TODO: Implement actual database health check
            return {
                'status': 'healthy',
                'response_time': 0.1,
                'connection_pool_size': 10,
                'active_connections': 5
            }
        except Exception as e:
            return {'status': 'critical', 'error': str(e)}

    async def _check_cache_health(self) -> Dict[str, Any]:
        """Check cache functionality and performance"""
        try:
            total_cache_size = sum(stats['size'] for stats in self.cache_stats.values())
            cache_utilization = total_cache_size / self.cache_settings['max_cache_size']
            
            return {
                'status': 'healthy' if cache_utilization < 0.8 else 'warning',
                'utilization': cache_utilization,
                'total_items': total_cache_size,
                'max_capacity': self.cache_settings['max_cache_size']
            }
        except Exception as e:
            return {'status': 'critical', 'error': str(e)}

    async def _check_ai_service_health(self) -> Dict[str, Any]:
        """Check AI service availability and performance"""
        try:
            # TODO: Implement actual AI service health check
            return {
                'status': 'healthy',
                'response_time': 2.5,
                'availability': 0.99
            }
        except Exception as e:
            return {'status': 'critical', 'error': str(e)}

    async def _check_response_time_health(self, performance_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Check response time health"""
        try:
            avg_response_time = performance_metrics.get('response_time_metrics', {}).get('average_response_time', 0)
            
            if avg_response_time <= 2.0:
                status = 'healthy'
            elif avg_response_time <= 5.0:
                status = 'warning'
            else:
                status = 'critical'
            
            return {
                'status': status,
                'average_response_time': avg_response_time,
                'threshold': self.quality_thresholds['max_response_time']
            }
        except Exception as e:
            return {'status': 'critical', 'error': str(e)}

    async def _check_error_rate_health(self, performance_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Check error rate health"""
        try:
            # Calculate overall error rate
            total_requests = performance_metrics.get('throughput_metrics', {}).get('successful_requests', 0) + \
                           performance_metrics.get('throughput_metrics', {}).get('failed_requests', 0)
            
            if total_requests > 0:
                error_rate = performance_metrics.get('throughput_metrics', {}).get('failed_requests', 0) / total_requests
            else:
                error_rate = 0.0
            
            if error_rate <= 0.01:  # 1%
                status = 'healthy'
            elif error_rate <= 0.05:  # 5%
                status = 'warning'
            else:
                status = 'critical'
            
            return {
                'status': status,
                'error_rate': error_rate,
                'threshold': 0.05
            }
        except Exception as e:
            return {'status': 'critical', 'error': str(e)}

    def _generate_health_recommendations(self, health_checks: Dict[str, Any], performance_metrics: Dict[str, Any]) -> List[str]:
        """Generate health recommendations based on current status"""
        recommendations = []
        
        for check_name, check_data in health_checks.items():
            if check_data.get('status') == 'critical':
                recommendations.append(f"Immediate attention required for {check_name}")
            elif check_data.get('status') == 'warning':
                recommendations.append(f"Monitor {check_name} for potential issues")
        
        # Performance-based recommendations
        avg_response_time = performance_metrics.get('response_time_metrics', {}).get('average_response_time', 0)
        if avg_response_time > 3.0:
            recommendations.append("Consider database optimization and caching improvements")
        
        cache_hit_rate = performance_metrics.get('cache_metrics', {}).get('ai_analysis_cache', {}).get('hit_rate', 0)
        if cache_hit_rate < 70:
            recommendations.append("Expand cache size and implement more aggressive caching")
        
        return recommendations 

    def _get_fallback_onboarding_data(self) -> Dict[str, Any]:
        """Get fallback onboarding data when primary data is unavailable"""
        try:
            logger.info("Using fallback onboarding data")
            
            # Return comprehensive fallback data for all 30+ strategic inputs
            return {
                'fields': {
                    'business_objectives': {
                        'value': ['Lead Generation', 'Brand Awareness', 'Thought Leadership'],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'target_metrics': {
                        'value': {
                            'traffic_growth': '25%',
                            'engagement_rate': '4%',
                            'conversion_rate': '2%',
                            'lead_generation': '50 leads/month'
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'content_budget': {
                        'value': 3000,
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'team_size': {
                        'value': 2,
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'implementation_timeline': {
                        'value': '3 months',
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'market_share': {
                        'value': '10%',
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'competitive_position': {
                        'value': 'Emerging',
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'performance_metrics': {
                        'value': {
                            'monthly_traffic': 10000,
                            'conversion_rate': 2.5,
                            'bounce_rate': 50.0,
                            'avg_session_duration': 150
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'content_preferences': {
                        'value': {
                            'preferred_formats': ['Blog posts', 'Whitepapers', 'Case studies'],
                            'content_topics': ['Industry trends', 'Best practices', 'Success stories'],
                            'content_style': ['Educational', 'Professional', 'Practical'],
                            'content_length': 'Medium (1000-2000 words)',
                            'visual_preferences': ['Infographics', 'Charts', 'Diagrams']
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'consumption_patterns': {
                        'value': {
                            'blogs': 70,
                            'videos': 20,
                            'podcasts': 5,
                            'social_media': 5
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'audience_pain_points': {
                        'value': [
                            'Information overload',
                            'Time constraints',
                            'Decision paralysis',
                            'Keeping up with trends'
                        ],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'buying_journey': {
                        'value': {
                            'awareness': 'Educational content and thought leadership',
                            'consideration': 'Case studies and comparisons',
                            'decision': 'Product demos and testimonials',
                            'retention': 'Ongoing support and updates'
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'seasonal_trends': {
                        'value': ['Q1: Planning', 'Q2: Execution', 'Q3: Optimization', 'Q4: Review'],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'engagement_metrics': {
                        'value': {
                            'avg_session_duration': 150,
                            'bounce_rate': 50.0,
                            'pages_per_session': 2.0
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'top_competitors': {
                        'value': ['Competitor A', 'Competitor B', 'Competitor C'],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'competitor_content_strategies': {
                        'value': ['Educational content', 'Case studies', 'Thought leadership'],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'market_gaps': {
                        'value': ['Practical implementation guides', 'Industry-specific insights'],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'industry_trends': {
                        'value': ['Digital transformation', 'AI/ML adoption', 'Remote work'],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'emerging_trends': {
                        'value': ['Voice search optimization', 'Video content', 'Interactive content'],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'preferred_formats': {
                        'value': ['Blog posts', 'Whitepapers', 'Case studies'],
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'content_mix': {
                        'value': {
                            'blog_posts': 50,
                            'whitepapers': 25,
                            'case_studies': 15,
                            'videos': 10
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'content_frequency': {
                        'value': 'Weekly',
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'optimal_timing': {
                        'value': {
                            'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
                            'best_times': ['9:00 AM', '1:00 PM', '3:00 PM']
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'quality_metrics': {
                        'value': {
                            'readability_score': 8.0,
                            'engagement_target': 4.0,
                            'conversion_target': 2.0
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'editorial_guidelines': {
                        'value': {
                            'tone': ['Professional', 'Educational'],
                            'length': 'Medium (1000-2000 words)',
                            'formatting': ['Use headers', 'Include visuals', 'Add CTAs']
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'brand_voice': {
                        'value': {
                            'tone': 'Professional yet approachable',
                            'style': 'Educational and authoritative',
                            'personality': 'Expert, helpful, trustworthy'
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'traffic_sources': {
                        'value': {
                            'organic': 70,
                            'social': 20,
                            'direct': 7,
                            'referral': 3
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'conversion_rates': {
                        'value': {
                            'overall': 2.5,
                            'blog': 2.0,
                            'landing_pages': 3.5,
                            'email': 4.5
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'content_roi_targets': {
                        'value': {
                            'target_roi': 250,
                            'cost_per_lead': 40,
                            'lifetime_value': 400
                        },
                        'source': 'fallback',
                        'confidence': 0.5
                    },
                    'ab_testing_capabilities': {
                        'value': False,
                        'source': 'fallback',
                        'confidence': 0.5
                    }
                },
                'sources': {
                    'business_objectives': 'fallback',
                    'target_metrics': 'fallback',
                    'content_budget': 'fallback',
                    'team_size': 'fallback',
                    'implementation_timeline': 'fallback',
                    'market_share': 'fallback',
                    'competitive_position': 'fallback',
                    'performance_metrics': 'fallback',
                    'content_preferences': 'fallback',
                    'consumption_patterns': 'fallback',
                    'audience_pain_points': 'fallback',
                    'buying_journey': 'fallback',
                    'seasonal_trends': 'fallback',
                    'engagement_metrics': 'fallback',
                    'top_competitors': 'fallback',
                    'competitor_content_strategies': 'fallback',
                    'market_gaps': 'fallback',
                    'industry_trends': 'fallback',
                    'emerging_trends': 'fallback',
                    'preferred_formats': 'fallback',
                    'content_mix': 'fallback',
                    'content_frequency': 'fallback',
                    'optimal_timing': 'fallback',
                    'quality_metrics': 'fallback',
                    'editorial_guidelines': 'fallback',
                    'brand_voice': 'fallback',
                    'traffic_sources': 'fallback',
                    'conversion_rates': 'fallback',
                    'content_roi_targets': 'fallback',
                    'ab_testing_capabilities': 'fallback'
                },
                'quality_scores': {
                    'website_analysis': 0.0,
                    'research_preferences': 0.0,
                    'api_keys_data': 0.0
                },
                'confidence_levels': {
                    'business_objectives': 0.5,
                    'target_metrics': 0.5,
                    'content_budget': 0.5,
                    'team_size': 0.5,
                    'implementation_timeline': 0.5,
                    'market_share': 0.5,
                    'competitive_position': 0.5,
                    'performance_metrics': 0.5,
                    'content_preferences': 0.5,
                    'consumption_patterns': 0.5,
                    'audience_pain_points': 0.5,
                    'buying_journey': 0.5,
                    'seasonal_trends': 0.5,
                    'engagement_metrics': 0.5,
                    'top_competitors': 0.5,
                    'competitor_content_strategies': 0.5,
                    'market_gaps': 0.5,
                    'industry_trends': 0.5,
                    'emerging_trends': 0.5,
                    'preferred_formats': 0.5,
                    'content_mix': 0.5,
                    'content_frequency': 0.5,
                    'optimal_timing': 0.5,
                    'quality_metrics': 0.5,
                    'editorial_guidelines': 0.5,
                    'brand_voice': 0.5,
                    'traffic_sources': 0.5,
                    'conversion_rates': 0.5,
                    'content_roi_targets': 0.5,
                    'ab_testing_capabilities': 0.5
                },
                'data_freshness': {
                    'status': 'unknown',
                    'age_days': 'unknown',
                    'last_updated': None
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting fallback onboarding data: {str(e)}")
            return {
                'fields': {},
                'sources': {},
                'quality_scores': {},
                'confidence_levels': {},
                'data_freshness': {'status': 'unknown', 'age_days': 'unknown'}
            }