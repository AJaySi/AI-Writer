"""
Step 9: Content Recommendations - Modular Implementation

This module implements content recommendations with a modular architecture:
- Content recommendation generation
- Keyword optimization and analysis
- Gap analysis and opportunity identification
- Performance prediction and validation
- Quality metrics calculation

All modules use real data processing without fallback or mock data.
"""

from .content_recommendation_generator import ContentRecommendationGenerator
from .keyword_optimizer import KeywordOptimizer
from .gap_analyzer import GapAnalyzer
from .performance_predictor import PerformancePredictor
from .quality_metrics_calculator import QualityMetricsCalculator
from .step9_main import ContentRecommendationsStep

__all__ = [
    'ContentRecommendationGenerator',
    'KeywordOptimizer',
    'GapAnalyzer',
    'PerformancePredictor',
    'QualityMetricsCalculator',
    'ContentRecommendationsStep'
]
