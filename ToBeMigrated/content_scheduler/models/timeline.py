"""
Timeline models for the Content Scheduler.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

class TimelineViewType(Enum):
    """Types of timeline views."""
    GANTT = "gantt"
    TIMELINE = "timeline"
    LIST = "list"

class TimelineDependencyType(Enum):
    """Types of timeline dependencies."""
    FINISH_TO_START = "finish_to_start"
    START_TO_START = "start_to_start"
    FINISH_TO_FINISH = "finish_to_finish"
    START_TO_FINISH = "start_to_finish"

@dataclass
class TimelineDependency:
    """Timeline dependency model."""
    source_id: str
    target_id: str
    dependency_type: TimelineDependencyType
    lag: Optional[int] = None  # Lag time in minutes

@dataclass
class TimelineTask:
    """Timeline task model."""
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    platform: str
    status: str
    progress: float
    dependencies: List[TimelineDependency]
    metadata: Dict[str, Any]

@dataclass
class TimelineMilestone:
    """Timeline milestone model."""
    id: str
    title: str
    date: datetime
    description: Optional[str] = None
    status: str = "pending"
    metadata: Dict[str, Any] = None

@dataclass
class TimelineView:
    """Timeline view model."""
    view_type: TimelineViewType
    start_date: datetime
    end_date: datetime
    tasks: List[TimelineTask]
    milestones: List[TimelineMilestone]
    dependencies: List[TimelineDependency]
    metadata: Dict[str, Any]

@dataclass
class TimelineProgress:
    """Timeline progress model."""
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    pending_tasks: int
    progress_percentage: float
    by_platform: Dict[str, float]
    by_date: Dict[str, float]
    metadata: Dict[str, Any] 