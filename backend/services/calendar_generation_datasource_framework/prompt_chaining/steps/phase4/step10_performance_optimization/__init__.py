"""
Step 10: Performance Optimization - Modular Implementation

This module implements performance optimization with a modular architecture:
- Performance analysis and metrics calculation
- Content quality optimization
- Engagement optimization
- ROI and conversion optimization
- Performance prediction and validation

All modules use real data processing without fallback or mock data.
"""

from .performance_analyzer import PerformanceAnalyzer
from .content_quality_optimizer import ContentQualityOptimizer
from .engagement_optimizer import EngagementOptimizer
from .roi_optimizer import ROIOptimizer
from .performance_predictor import PerformancePredictor
from .step10_main import PerformanceOptimizationStep

__all__ = [
    'PerformanceAnalyzer',
    'ContentQualityOptimizer',
    'EngagementOptimizer',
    'ROIOptimizer',
    'PerformancePredictor',
    'PerformanceOptimizationStep'
]
