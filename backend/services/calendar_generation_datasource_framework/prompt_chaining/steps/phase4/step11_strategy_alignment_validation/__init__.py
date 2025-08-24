"""
Step 11: Strategy Alignment Validation - Modular Implementation

This module implements strategy alignment validation with a modular architecture:
- Strategy alignment validator
- Consistency checker
- Multi-dimensional alignment scoring
- Strategy drift detection and reporting
- Cross-step consistency validation
- Data flow verification between steps

All modules use real data processing without fallback or mock data.
"""

from .strategy_alignment_validator import StrategyAlignmentValidator
from .consistency_checker import ConsistencyChecker
from .step11_main import StrategyAlignmentValidationStep

__all__ = [
    'StrategyAlignmentValidator',
    'ConsistencyChecker',
    'StrategyAlignmentValidationStep'
]
