"""
Quality Handler for LinkedIn Content Generation

Handles content quality analysis and metrics conversion.
"""

from typing import Dict, Any, Optional
from models.linkedin_models import ContentQualityMetrics
from loguru import logger


class QualityHandler:
    """Handles content quality analysis and metrics conversion."""
    
    def __init__(self, quality_analyzer=None):
        self.quality_analyzer = quality_analyzer
    
    def create_quality_metrics(
        self, 
        content: str, 
        sources: list, 
        industry: str,
        grounding_enabled: bool = False
    ) -> Optional[ContentQualityMetrics]:
        """
        Create ContentQualityMetrics object from quality analysis.
        
        Args:
            content: Content to analyze
            sources: Research sources used
            industry: Target industry
            grounding_enabled: Whether grounding was used
            
        Returns:
            ContentQualityMetrics object or None if analysis fails
        """
        if not grounding_enabled or not self.quality_analyzer:
            return None
            
        try:
            quality_analysis = self.quality_analyzer.analyze_content_quality(
                content=content,
                sources=sources,
                industry=industry
            )
            
            # Convert the analysis result to ContentQualityMetrics format
            return ContentQualityMetrics(
                overall_score=quality_analysis.get('overall_score', 0.0),
                factual_accuracy=quality_analysis.get('metrics', {}).get('factual_accuracy', 0.0),
                source_verification=quality_analysis.get('metrics', {}).get('source_verification', 0.0),
                professional_tone=quality_analysis.get('metrics', {}).get('professional_tone', 0.0),
                industry_relevance=quality_analysis.get('metrics', {}).get('industry_relevance', 0.0),
                citation_coverage=quality_analysis.get('metrics', {}).get('citation_coverage', 0.0),
                content_length=quality_analysis.get('content_length', 0),
                word_count=quality_analysis.get('word_count', 0),
                analysis_timestamp=quality_analysis.get('analysis_timestamp', ''),
                recommendations=quality_analysis.get('recommendations', [])
            )
        except Exception as e:
            logger.warning(f"Quality metrics creation failed: {e}")
            return None
