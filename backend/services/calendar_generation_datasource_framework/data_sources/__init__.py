"""
Data Sources Package for Calendar Generation Framework

Individual modules for each data source to ensure separation of concerns
and maintainability as the framework grows.
"""

from .content_strategy_source import ContentStrategyDataSource
from .gap_analysis_source import GapAnalysisDataSource
from .keywords_source import KeywordsDataSource
from .content_pillars_source import ContentPillarsDataSource
from .performance_source import PerformanceDataSource
from .ai_analysis_source import AIAnalysisDataSource

__all__ = [
    "ContentStrategyDataSource",
    "GapAnalysisDataSource", 
    "KeywordsDataSource",
    "ContentPillarsDataSource",
    "PerformanceDataSource",
    "AIAnalysisDataSource"
]
