"""
AI Recommendations Service
AI recommendation generation and analysis.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

# Import database models
from models.enhanced_strategy_models import EnhancedContentStrategy, EnhancedAIAnalysisResult

# Import modular components
from .prompt_engineering import PromptEngineeringService
from .quality_validation import QualityValidationService

logger = logging.getLogger(__name__)

class AIRecommendationsService:
    """Service for AI recommendation generation."""
    
    def __init__(self):
        self.prompt_engineering_service = PromptEngineeringService()
        self.quality_validation_service = QualityValidationService()
        
        # Analysis types for comprehensive recommendations
        self.analysis_types = [
            'comprehensive_strategy',
            'audience_intelligence', 
            'competitive_intelligence',
            'performance_optimization',
            'content_calendar_optimization'
        ]
    
    async def generate_comprehensive_recommendations(self, strategy: EnhancedContentStrategy, db: Session) -> None:
        """Generate comprehensive AI recommendations using 5 specialized prompts."""
        try:
            logger.info(f"Generating comprehensive AI recommendations for strategy: {strategy.id}")
            
            start_time = datetime.utcnow()
            
            # Generate recommendations for each analysis type
            ai_recommendations = {}
            
            for analysis_type in self.analysis_types:
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
            strategy.strategic_scores = self.quality_validation_service.calculate_strategic_scores(ai_recommendations)
            strategy.market_positioning = self.quality_validation_service.extract_market_positioning(ai_recommendations)
            strategy.competitive_advantages = self.quality_validation_service.extract_competitive_advantages(ai_recommendations)
            strategy.strategic_risks = self.quality_validation_service.extract_strategic_risks(ai_recommendations)
            strategy.opportunity_analysis = self.quality_validation_service.extract_opportunity_analysis(ai_recommendations)
            
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
            
            # Create prompt based on analysis type
            prompt = self.prompt_engineering_service.create_specialized_prompt(strategy, analysis_type)
            
            # Generate AI response
            ai_response = await self._call_ai_service(prompt, analysis_type)
            
            # Parse and structure the response
            structured_response = self._parse_ai_response(ai_response, analysis_type)
            
            return structured_response
            
        except Exception as e:
            logger.error(f"Error generating {analysis_type} recommendations: {str(e)}")
            return self._get_fallback_recommendations(analysis_type)
    
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
            'insights': ['Limited data available for analysis'],
            'metrics': {'score': 50, 'confidence': 0.3}
        })
    
    async def get_latest_ai_analysis(self, strategy_id: int, db: Session) -> Optional[Dict[str, Any]]:
        """Get latest AI analysis for a strategy."""
        try:
            analysis = db.query(EnhancedAIAnalysisResult).filter(
                EnhancedAIAnalysisResult.strategy_id == strategy_id
            ).order_by(EnhancedAIAnalysisResult.created_at.desc()).first()
            
            return analysis.to_dict() if analysis else None
            
        except Exception as e:
            logger.error(f"Error getting latest AI analysis: {str(e)}")
            return None 