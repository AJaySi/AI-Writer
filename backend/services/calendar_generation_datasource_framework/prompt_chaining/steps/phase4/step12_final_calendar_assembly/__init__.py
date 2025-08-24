"""
Step 12: Final Calendar Assembly - Modular Implementation

This module implements the final calendar assembly with a modular architecture:
- Calendar assembly engine (core orchestrator)
- Journey storyteller (narrative creation)
- Calendar enhancement engine (final polish)
- Export & delivery manager (multiple output formats)
- Quality assurance engine (final validation)

All modules use real data processing without fallback or mock data.
This is the pinnacle step that brings together all 11 previous steps
into a cohesive, actionable, and beautiful calendar.
"""

from .calendar_assembly_engine import CalendarAssemblyEngine
from .journey_storyteller import JourneyStoryteller
from .calendar_enhancement_engine import CalendarEnhancementEngine
from .export_delivery_manager import ExportDeliveryManager
from .quality_assurance_engine import QualityAssuranceEngine
from .step12_main import FinalCalendarAssemblyStep

__all__ = [
    'CalendarAssemblyEngine',
    'JourneyStoryteller',
    'CalendarEnhancementEngine',
    'ExportDeliveryManager',
    'QualityAssuranceEngine',
    'FinalCalendarAssemblyStep'
]
