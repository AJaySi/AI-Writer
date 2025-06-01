from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

class ScheduleType(str, Enum):
    """Type of schedule."""
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    BATCH = "batch"

class ScheduleStatus(str, Enum):
    """Status of a schedule."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ERROR = "error"

@dataclass
class ScheduleMetadata:
    """Metadata for a schedule."""
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    priority: int = 0
    custom_data: Dict[str, Any] = field(default_factory=dict)
    notification_settings: Dict[str, Any] = field(default_factory=dict)

class Schedule(BaseModel):
    """Model representing a content publishing schedule."""
    
    content_id: str = Field(..., description="ID of the content to be published")
    content: Dict[str, Any] = Field(..., description="Content to be published")
    publish_date: datetime = Field(..., description="When to publish the content")
    platforms: List[str] = Field(..., description="List of platforms to publish to")
    schedule_type: str = Field(default="one_time", description="Type of schedule ('one_time' or 'recurring')")
    cron_expression: Optional[str] = Field(None, description="Cron expression for recurring schedules")
    end_date: Optional[datetime] = Field(None, description="End date for recurring schedules")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the schedule")
    
    class Config:
        """Pydantic model configuration."""
        arbitrary_types_allowed = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert schedule to dictionary."""
        return {
            'schedule_id': self.schedule_id,
            'content_id': self.content_id,
            'schedule_type': self.schedule_type,
            'status': self.status,
            'platforms': self.platforms,
            'publish_date': self.publish_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'cron_expression': self.cron_expression,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'metadata': {
                'description': self.metadata.description,
                'tags': self.metadata.tags,
                'priority': self.metadata.priority,
                'custom_data': self.metadata.custom_data,
                'notification_settings': self.metadata.notification_settings
            },
            'error': self.error,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'job_ids': self.job_ids
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Schedule':
        """Create schedule from dictionary."""
        metadata = ScheduleMetadata(
            description=data['metadata'].get('description'),
            tags=data['metadata'].get('tags', []),
            priority=data['metadata'].get('priority', 0),
            custom_data=data['metadata'].get('custom_data', {}),
            notification_settings=data['metadata'].get('notification_settings', {})
        )
        
        return cls(
            schedule_id=data['schedule_id'],
            content_id=data['content_id'],
            schedule_type=data['schedule_type'],
            status=data['status'],
            platforms=data['platforms'],
            publish_date=datetime.fromisoformat(data['publish_date']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            cron_expression=data.get('cron_expression'),
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
            metadata=metadata,
            error=data.get('error'),
            last_run=datetime.fromisoformat(data['last_run']) if data.get('last_run') else None,
            next_run=datetime.fromisoformat(data['next_run']) if data.get('next_run') else None,
            job_ids=data.get('job_ids', [])
        )
    
    def is_active(self) -> bool:
        """Check if schedule is active."""
        return self.status == ScheduleStatus.ACTIVE
    
    def is_completed(self) -> bool:
        """Check if schedule is completed."""
        return self.status == ScheduleStatus.COMPLETED
    
    def is_cancelled(self) -> bool:
        """Check if schedule is cancelled."""
        return self.status == ScheduleStatus.CANCELLED
    
    def is_error(self) -> bool:
        """Check if schedule has error."""
        return self.status == ScheduleStatus.ERROR
    
    def is_recurring(self) -> bool:
        """Check if schedule is recurring."""
        return self.schedule_type == ScheduleType.RECURRING
    
    def is_one_time(self) -> bool:
        """Check if schedule is one-time."""
        return self.schedule_type == ScheduleType.ONE_TIME
    
    def is_batch(self) -> bool:
        """Check if schedule is batch."""
        return self.schedule_type == ScheduleType.BATCH
    
    def add_job_id(self, job_id: str):
        """Add a job ID to the schedule."""
        if job_id not in self.job_ids:
            self.job_ids.append(job_id)
    
    def remove_job_id(self, job_id: str):
        """Remove a job ID from the schedule."""
        if job_id in self.job_ids:
            self.job_ids.remove(job_id)
    
    def update_status(self, status: ScheduleStatus, error: Optional[str] = None):
        """Update schedule status."""
        self.status = status
        self.error = error
        self.updated_at = datetime.now()
    
    def update_next_run(self, next_run: datetime):
        """Update next run time."""
        self.next_run = next_run
        self.updated_at = datetime.now()
    
    def update_last_run(self, last_run: datetime):
        """Update last run time."""
        self.last_run = last_run
        self.updated_at = datetime.now() 