"""
Quality Assessment Module for Calendar Generation

Extracted from calendar_generator_service.py to improve maintainability
and align with 12-step implementation plan.
"""

from .strategy_quality import StrategyQualityAssessor

__all__ = [
    "StrategyQualityAssessor"
]
