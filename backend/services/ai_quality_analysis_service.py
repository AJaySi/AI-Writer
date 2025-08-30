"""
AI Quality Analysis Service
Provides AI-powered quality assessment and recommendations for content strategies.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from services.llm_providers.gemini_provider import gemini_structured_json_response
from services.strategy_service import StrategyService
from models.enhanced_strategy_models import EnhancedContentStrategy

logger = logging.getLogger(__name__)

class QualityScore(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_ATTENTION = "needs_attention"
    POOR = "poor"

@dataclass
class QualityMetric:
    name: str
    score: float  # 0-100
    weight: float  # 0-1
    status: QualityScore
    description: str
    recommendations: List[str]

@dataclass
class QualityAnalysisResult:
    overall_score: float
    overall_status: QualityScore
    metrics: List[QualityMetric]
    recommendations: List[str]
    confidence_score: float
    analysis_timestamp: datetime
    strategy_id: int

# Structured JSON schemas for Gemini API
QUALITY_ANALYSIS_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "score": {"type": "NUMBER"},
        "status": {"type": "STRING"},
        "description": {"type": "STRING"},
        "recommendations": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        }
    },
    "propertyOrdering": ["score", "status", "description", "recommendations"]
}

RECOMMENDATIONS_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "recommendations": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "priority_areas": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        }
    },
    "propertyOrdering": ["recommendations", "priority_areas"]
}

class AIQualityAnalysisService:
    """AI-powered quality assessment service for content strategies."""
    
    def __init__(self):
        self.strategy_service = StrategyService()
        
    async def analyze_strategy_quality(self, strategy_id: int) -> QualityAnalysisResult:
        """Analyze strategy quality using AI and return comprehensive results."""
        try:
            logger.info(f"Starting AI quality analysis for strategy {strategy_id}")
            
            # Get strategy data
            strategy_data = await self.strategy_service.get_strategy_by_id(strategy_id)
            if not strategy_data:
                raise ValueError(f"Strategy {strategy_id} not found")
            
            # Perform comprehensive quality analysis
            quality_metrics = await self._analyze_quality_metrics(strategy_data)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(quality_metrics)
            overall_status = self._determine_overall_status(overall_score)
            
            # Generate AI recommendations
            recommendations = await self._generate_ai_recommendations(strategy_data, quality_metrics)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(quality_metrics)
            
            result = QualityAnalysisResult(
                overall_score=overall_score,
                overall_status=overall_status,
                metrics=quality_metrics,
                recommendations=recommendations,
                confidence_score=confidence_score,
                analysis_timestamp=datetime.utcnow(),
                strategy_id=strategy_id
            )
            
            # Save analysis result to database
            await self._save_quality_analysis(result)
            
            logger.info(f"Quality analysis completed for strategy {strategy_id}. Score: {overall_score}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing strategy quality for {strategy_id}: {e}")
            raise
    
    async def _analyze_quality_metrics(self, strategy_data: Dict[str, Any]) -> List[QualityMetric]:
        """Analyze individual quality metrics for a strategy."""
        metrics = []
        
        # 1. Strategic Completeness Analysis
        completeness_metric = await self._analyze_strategic_completeness(strategy_data)
        metrics.append(completeness_metric)
        
        # 2. Audience Intelligence Quality
        audience_metric = await self._analyze_audience_intelligence(strategy_data)
        metrics.append(audience_metric)
        
        # 3. Competitive Intelligence Quality
        competitive_metric = await self._analyze_competitive_intelligence(strategy_data)
        metrics.append(competitive_metric)
        
        # 4. Content Strategy Quality
        content_metric = await self._analyze_content_strategy(strategy_data)
        metrics.append(content_metric)
        
        # 5. Performance Alignment Quality
        performance_metric = await self._analyze_performance_alignment(strategy_data)
        metrics.append(performance_metric)
        
        # 6. Implementation Feasibility
        feasibility_metric = await self._analyze_implementation_feasibility(strategy_data)
        metrics.append(feasibility_metric)
        
        return metrics
    
    async def _analyze_strategic_completeness(self, strategy_data: Dict[str, Any]) -> QualityMetric:
        """Analyze strategic completeness and depth."""
        try:
            # Check required fields
            required_fields = [
                'business_objectives', 'target_metrics', 'content_budget',
                'team_size', 'implementation_timeline', 'market_share'
            ]
            
            filled_fields = sum(1 for field in required_fields if strategy_data.get(field))
            completeness_score = (filled_fields / len(required_fields)) * 100
            
            # AI analysis of strategic depth
            prompt = f"""
            Analyze the strategic completeness of this content strategy:
            
            Business Objectives: {strategy_data.get('business_objectives', 'Not provided')}
            Target Metrics: {strategy_data.get('target_metrics', 'Not provided')}
            Content Budget: {strategy_data.get('content_budget', 'Not provided')}
            Team Size: {strategy_data.get('team_size', 'Not provided')}
            Implementation Timeline: {strategy_data.get('implementation_timeline', 'Not provided')}
            Market Share: {strategy_data.get('market_share', 'Not provided')}
            
            Provide a quality score (0-100), status (excellent/good/needs_attention/poor), description, and specific recommendations for improvement.
            Focus on strategic depth, clarity, and measurability.
            """
            
            ai_response = gemini_structured_json_response(
                prompt=prompt,
                schema=QUALITY_ANALYSIS_SCHEMA,
                temperature=0.3,
                max_tokens=2048
            )
            
            if "error" in ai_response:
                raise ValueError(f"AI analysis failed: {ai_response['error']}")
            
            # Parse AI response
            ai_score = ai_response.get('score', 60.0)
            ai_status = ai_response.get('status', 'needs_attention')
            description = ai_response.get('description', 'Strategic completeness analysis')
            recommendations = ai_response.get('recommendations', [])
            
            # Combine manual and AI scores
            final_score = (completeness_score * 0.4) + (ai_score * 0.6)
            
            return QualityMetric(
                name="Strategic Completeness",
                score=final_score,
                weight=0.25,
                status=self._parse_status(ai_status),
                description=description,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing strategic completeness: {e}")
            raise ValueError(f"Failed to analyze strategic completeness: {str(e)}")
    
    async def _analyze_audience_intelligence(self, strategy_data: Dict[str, Any]) -> QualityMetric:
        """Analyze audience intelligence quality."""
        try:
            audience_fields = [
                'content_preferences', 'consumption_patterns', 'audience_pain_points',
                'buying_journey', 'seasonal_trends', 'engagement_metrics'
            ]
            
            filled_fields = sum(1 for field in audience_fields if strategy_data.get(field))
            completeness_score = (filled_fields / len(audience_fields)) * 100
            
            # AI analysis of audience insights
            prompt = f"""
            Analyze the audience intelligence quality of this content strategy:
            
            Content Preferences: {strategy_data.get('content_preferences', 'Not provided')}
            Consumption Patterns: {strategy_data.get('consumption_patterns', 'Not provided')}
            Audience Pain Points: {strategy_data.get('audience_pain_points', 'Not provided')}
            Buying Journey: {strategy_data.get('buying_journey', 'Not provided')}
            Seasonal Trends: {strategy_data.get('seasonal_trends', 'Not provided')}
            Engagement Metrics: {strategy_data.get('engagement_metrics', 'Not provided')}
            
            Provide a quality score (0-100), status (excellent/good/needs_attention/poor), description, and specific recommendations for improvement.
            Focus on audience understanding, segmentation, and actionable insights.
            """
            
            ai_response = await gemini_structured_json_response(
                prompt=prompt,
                schema=QUALITY_ANALYSIS_SCHEMA,
                temperature=0.3,
                max_tokens=2048
            )
            
            if "error" in ai_response:
                raise ValueError(f"AI analysis failed: {ai_response['error']}")
            
            ai_score = ai_response.get('score', 60.0)
            ai_status = ai_response.get('status', 'needs_attention')
            description = ai_response.get('description', 'Audience intelligence analysis')
            recommendations = ai_response.get('recommendations', [])
            
            final_score = (completeness_score * 0.3) + (ai_score * 0.7)
            
            return QualityMetric(
                name="Audience Intelligence",
                score=final_score,
                weight=0.20,
                status=self._parse_status(ai_status),
                description=description,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing audience intelligence: {e}")
            raise ValueError(f"Failed to analyze audience intelligence: {str(e)}")
    
    async def _analyze_competitive_intelligence(self, strategy_data: Dict[str, Any]) -> QualityMetric:
        """Analyze competitive intelligence quality."""
        try:
            competitive_fields = [
                'top_competitors', 'competitor_content_strategies', 'market_gaps',
                'industry_trends', 'emerging_trends'
            ]
            
            filled_fields = sum(1 for field in competitive_fields if strategy_data.get(field))
            completeness_score = (filled_fields / len(competitive_fields)) * 100
            
            # AI analysis of competitive insights
            prompt = f"""
            Analyze the competitive intelligence quality of this content strategy:
            
            Top Competitors: {strategy_data.get('top_competitors', 'Not provided')}
            Competitor Content Strategies: {strategy_data.get('competitor_content_strategies', 'Not provided')}
            Market Gaps: {strategy_data.get('market_gaps', 'Not provided')}
            Industry Trends: {strategy_data.get('industry_trends', 'Not provided')}
            Emerging Trends: {strategy_data.get('emerging_trends', 'Not provided')}
            
            Provide a quality score (0-100), status (excellent/good/needs_attention/poor), description, and specific recommendations for improvement.
            Focus on competitive positioning, differentiation opportunities, and market insights.
            """
            
            ai_response = await gemini_structured_json_response(
                prompt=prompt,
                schema=QUALITY_ANALYSIS_SCHEMA,
                temperature=0.3,
                max_tokens=2048
            )
            
            if "error" in ai_response:
                raise ValueError(f"AI analysis failed: {ai_response['error']}")
            
            ai_score = ai_response.get('score', 60.0)
            ai_status = ai_response.get('status', 'needs_attention')
            description = ai_response.get('description', 'Competitive intelligence analysis')
            recommendations = ai_response.get('recommendations', [])
            
            final_score = (completeness_score * 0.3) + (ai_score * 0.7)
            
            return QualityMetric(
                name="Competitive Intelligence",
                score=final_score,
                weight=0.15,
                status=self._parse_status(ai_status),
                description=description,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing competitive intelligence: {e}")
            raise ValueError(f"Failed to analyze competitive intelligence: {str(e)}")
    
    async def _analyze_content_strategy(self, strategy_data: Dict[str, Any]) -> QualityMetric:
        """Analyze content strategy quality."""
        try:
            content_fields = [
                'preferred_formats', 'content_mix', 'content_frequency',
                'optimal_timing', 'quality_metrics', 'editorial_guidelines', 'brand_voice'
            ]
            
            filled_fields = sum(1 for field in content_fields if strategy_data.get(field))
            completeness_score = (filled_fields / len(content_fields)) * 100
            
            # AI analysis of content strategy
            prompt = f"""
            Analyze the content strategy quality:
            
            Preferred Formats: {strategy_data.get('preferred_formats', 'Not provided')}
            Content Mix: {strategy_data.get('content_mix', 'Not provided')}
            Content Frequency: {strategy_data.get('content_frequency', 'Not provided')}
            Optimal Timing: {strategy_data.get('optimal_timing', 'Not provided')}
            Quality Metrics: {strategy_data.get('quality_metrics', 'Not provided')}
            Editorial Guidelines: {strategy_data.get('editorial_guidelines', 'Not provided')}
            Brand Voice: {strategy_data.get('brand_voice', 'Not provided')}
            
            Provide a quality score (0-100), status (excellent/good/needs_attention/poor), description, and specific recommendations for improvement.
            Focus on content planning, execution strategy, and quality standards.
            """
            
            ai_response = await gemini_structured_json_response(
                prompt=prompt,
                schema=QUALITY_ANALYSIS_SCHEMA,
                temperature=0.3,
                max_tokens=2048
            )
            
            if "error" in ai_response:
                raise ValueError(f"AI analysis failed: {ai_response['error']}")
            
            ai_score = ai_response.get('score', 60.0)
            ai_status = ai_response.get('status', 'needs_attention')
            description = ai_response.get('description', 'Content strategy analysis')
            recommendations = ai_response.get('recommendations', [])
            
            final_score = (completeness_score * 0.3) + (ai_score * 0.7)
            
            return QualityMetric(
                name="Content Strategy",
                score=final_score,
                weight=0.20,
                status=self._parse_status(ai_status),
                description=description,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing content strategy: {e}")
            raise ValueError(f"Failed to analyze content strategy: {str(e)}")
    
    async def _analyze_performance_alignment(self, strategy_data: Dict[str, Any]) -> QualityMetric:
        """Analyze performance alignment quality."""
        try:
            performance_fields = [
                'traffic_sources', 'conversion_rates', 'content_roi_targets',
                'ab_testing_capabilities'
            ]
            
            filled_fields = sum(1 for field in performance_fields if strategy_data.get(field))
            completeness_score = (filled_fields / len(performance_fields)) * 100
            
            # AI analysis of performance alignment
            prompt = f"""
            Analyze the performance alignment quality:
            
            Traffic Sources: {strategy_data.get('traffic_sources', 'Not provided')}
            Conversion Rates: {strategy_data.get('conversion_rates', 'Not provided')}
            Content ROI Targets: {strategy_data.get('content_roi_targets', 'Not provided')}
            A/B Testing Capabilities: {strategy_data.get('ab_testing_capabilities', 'Not provided')}
            
            Provide a quality score (0-100), status (excellent/good/needs_attention/poor), description, and specific recommendations for improvement.
            Focus on performance measurement, optimization, and ROI alignment.
            """
            
            ai_response = await gemini_structured_json_response(
                prompt=prompt,
                schema=QUALITY_ANALYSIS_SCHEMA,
                temperature=0.3,
                max_tokens=2048
            )
            
            if "error" in ai_response:
                raise ValueError(f"AI analysis failed: {ai_response['error']}")
            
            ai_score = ai_response.get('score', 60.0)
            ai_status = ai_response.get('status', 'needs_attention')
            description = ai_response.get('description', 'Performance alignment analysis')
            recommendations = ai_response.get('recommendations', [])
            
            final_score = (completeness_score * 0.3) + (ai_score * 0.7)
            
            return QualityMetric(
                name="Performance Alignment",
                score=final_score,
                weight=0.15,
                status=self._parse_status(ai_status),
                description=description,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing performance alignment: {e}")
            raise ValueError(f"Failed to analyze performance alignment: {str(e)}")
    
    async def _analyze_implementation_feasibility(self, strategy_data: Dict[str, Any]) -> QualityMetric:
        """Analyze implementation feasibility."""
        try:
            # Check resource availability
            has_budget = bool(strategy_data.get('content_budget'))
            has_team = bool(strategy_data.get('team_size'))
            has_timeline = bool(strategy_data.get('implementation_timeline'))
            
            resource_score = ((has_budget + has_team + has_timeline) / 3) * 100
            
            # AI analysis of feasibility
            prompt = f"""
            Analyze the implementation feasibility of this content strategy:
            
            Content Budget: {strategy_data.get('content_budget', 'Not provided')}
            Team Size: {strategy_data.get('team_size', 'Not provided')}
            Implementation Timeline: {strategy_data.get('implementation_timeline', 'Not provided')}
            Industry: {strategy_data.get('industry', 'Not provided')}
            Market Share: {strategy_data.get('market_share', 'Not provided')}
            
            Provide a quality score (0-100), status (excellent/good/needs_attention/poor), description, and specific recommendations for improvement.
            Focus on resource availability, timeline feasibility, and implementation challenges.
            """
            
            ai_response = await gemini_structured_json_response(
                prompt=prompt,
                schema=QUALITY_ANALYSIS_SCHEMA,
                temperature=0.3,
                max_tokens=2048
            )
            
            if "error" in ai_response:
                raise ValueError(f"AI analysis failed: {ai_response['error']}")
            
            ai_score = ai_response.get('score', 60.0)
            ai_status = ai_response.get('status', 'needs_attention')
            description = ai_response.get('description', 'Implementation feasibility analysis')
            recommendations = ai_response.get('recommendations', [])
            
            final_score = (resource_score * 0.4) + (ai_score * 0.6)
            
            return QualityMetric(
                name="Implementation Feasibility",
                score=final_score,
                weight=0.05,
                status=self._parse_status(ai_status),
                description=description,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing implementation feasibility: {e}")
            raise ValueError(f"Failed to analyze implementation feasibility: {str(e)}")
    
    def _calculate_overall_score(self, metrics: List[QualityMetric]) -> float:
        """Calculate weighted overall quality score."""
        if not metrics:
            return 0.0
        
        weighted_sum = sum(metric.score * metric.weight for metric in metrics)
        total_weight = sum(metric.weight for metric in metrics)
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _determine_overall_status(self, score: float) -> QualityScore:
        """Determine overall quality status based on score."""
        if score >= 85:
            return QualityScore.EXCELLENT
        elif score >= 70:
            return QualityScore.GOOD
        elif score >= 50:
            return QualityScore.NEEDS_ATTENTION
        else:
            return QualityScore.POOR
    
    def _parse_status(self, status_str: str) -> QualityScore:
        """Parse status string to QualityScore enum."""
        status_lower = status_str.lower()
        if status_lower == 'excellent':
            return QualityScore.EXCELLENT
        elif status_lower == 'good':
            return QualityScore.GOOD
        elif status_lower == 'needs_attention':
            return QualityScore.NEEDS_ATTENTION
        elif status_lower == 'poor':
            return QualityScore.POOR
        else:
            return QualityScore.NEEDS_ATTENTION
    
    async def _generate_ai_recommendations(self, strategy_data: Dict[str, Any], metrics: List[QualityMetric]) -> List[str]:
        """Generate AI-powered recommendations for strategy improvement."""
        try:
            # Identify areas needing improvement
            low_metrics = [m for m in metrics if m.status in [QualityScore.NEEDS_ATTENTION, QualityScore.POOR]]
            
            if not low_metrics:
                return ["Strategy quality is excellent. Continue monitoring and optimizing based on performance data."]
            
            # Generate specific recommendations
            prompt = f"""
            Based on the quality analysis of this content strategy, provide 3-5 specific, actionable recommendations for improvement.
            
            Strategy Overview:
            - Industry: {strategy_data.get('industry', 'Not specified')}
            - Business Objectives: {strategy_data.get('business_objectives', 'Not specified')}
            
            Areas needing improvement:
            {chr(10).join([f"- {m.name}: {m.score:.1f}/100" for m in low_metrics])}
            
            Provide specific, actionable recommendations that can be implemented immediately.
            Focus on the most impactful improvements first.
            """
            
            ai_response = await gemini_structured_json_response(
                prompt=prompt,
                schema=RECOMMENDATIONS_SCHEMA,
                temperature=0.3,
                max_tokens=2048
            )
            
            if "error" in ai_response:
                raise ValueError(f"AI recommendations failed: {ai_response['error']}")
            
            recommendations = ai_response.get('recommendations', [])
            return recommendations[:5]  # Limit to 5 recommendations
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {e}")
            raise ValueError(f"Failed to generate AI recommendations: {str(e)}")
    
    def _calculate_confidence_score(self, metrics: List[QualityMetric]) -> float:
        """Calculate confidence score based on data quality and analysis depth."""
        if not metrics:
            return 0.0
        
        # Higher scores indicate more confidence
        avg_score = sum(m.score for m in metrics) / len(metrics)
        
        # More metrics analyzed = higher confidence
        metric_count_factor = min(len(metrics) / 6, 1.0)  # 6 is max expected metrics
        
        confidence = (avg_score * 0.7) + (metric_count_factor * 100 * 0.3)
        return min(confidence, 100.0)
    
    async def _save_quality_analysis(self, result: QualityAnalysisResult) -> bool:
        """Save quality analysis result to database."""
        try:
            # This would save to a quality_analysis_results table
            # For now, we'll log the result
            logger.info(f"Quality analysis saved for strategy {result.strategy_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving quality analysis: {e}")
            return False
    
    async def get_quality_history(self, strategy_id: int, days: int = 30) -> List[QualityAnalysisResult]:
        """Get quality analysis history for a strategy."""
        try:
            # This would query the quality_analysis_results table
            # For now, return empty list
            return []
        except Exception as e:
            logger.error(f"Error getting quality history: {e}")
            return []
    
    async def get_quality_trends(self, strategy_id: int) -> Dict[str, Any]:
        """Get quality trends over time."""
        try:
            # This would analyze quality trends over time
            # For now, return empty data
            return {
                "trend": "stable",
                "change_rate": 0,
                "consistency_score": 0
            }
        except Exception as e:
            logger.error(f"Error getting quality trends: {e}")
            return {"trend": "stable", "change_rate": 0, "consistency_score": 0}
