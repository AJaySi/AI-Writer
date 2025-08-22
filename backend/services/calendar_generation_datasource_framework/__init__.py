"""
Calendar Generation Data Source Framework

A scalable framework for managing evolving data sources in calendar generation
without requiring architectural changes. Supports dynamic data source registration,
AI prompt enhancement, quality gates, and evolution management.

Key Components:
- DataSourceInterface: Abstract base for all data sources
- DataSourceRegistry: Central registry for managing data sources
- StrategyAwarePromptBuilder: AI prompt enhancement with strategy context
- QualityGateManager: Comprehensive quality validation system
- DataSourceEvolutionManager: Evolution management for data sources
"""

from .interfaces import DataSourceInterface, DataSourceType, DataSourcePriority, DataSourceValidationResult
from .registry import DataSourceRegistry
from .prompt_builder import StrategyAwarePromptBuilder
from .quality_gates import QualityGateManager
from .evolution_manager import DataSourceEvolutionManager

# Import individual data sources
from .data_sources import (
    ContentStrategyDataSource,
    GapAnalysisDataSource,
    KeywordsDataSource,
    ContentPillarsDataSource,
    PerformanceDataSource,
    AIAnalysisDataSource
)

# Import individual quality gates
from .quality_gates import (
    ContentUniquenessGate,
    ContentMixGate,
    ChainContextGate,
    CalendarStructureGate,
    EnterpriseStandardsGate,
    KPIIntegrationGate
)

__version__ = "2.0.0"
__author__ = "ALwrity Team"

__all__ = [
    # Core interfaces
    "DataSourceInterface",
    "DataSourceType", 
    "DataSourcePriority",
    "DataSourceValidationResult",
    
    # Core services
    "DataSourceRegistry",
    "StrategyAwarePromptBuilder",
    "QualityGateManager",
    "DataSourceEvolutionManager",
    
    # Data sources
    "ContentStrategyDataSource",
    "GapAnalysisDataSource",
    "KeywordsDataSource", 
    "ContentPillarsDataSource",
    "PerformanceDataSource",
    "AIAnalysisDataSource",
    
    # Quality gates
    "ContentUniquenessGate",
    "ContentMixGate",
    "ChainContextGate",
    "CalendarStructureGate", 
    "EnterpriseStandardsGate",
    "KPIIntegrationGate"
]
