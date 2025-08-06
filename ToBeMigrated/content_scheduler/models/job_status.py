"""
Job status model for content scheduling.
"""

from enum import Enum

class JobStatus(str, Enum):
    """Enum representing the status of a scheduled job."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying" 