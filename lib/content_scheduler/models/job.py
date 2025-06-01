from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field
from pydantic import BaseModel

class JobStatus(str, Enum):
    """Status of a scheduled job."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    MISSED = "missed"

class JobType(str, Enum):
    """Type of scheduled job."""
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    BATCH = "batch"

class JobPriority(int, Enum):
    """Priority of a scheduled job."""
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class JobMetadata:
    """Metadata for a scheduled job."""
    retry_count: int = 0
    max_retries: int = 3
    retry_delay: int = 300  # seconds
    priority: JobPriority = JobPriority.MEDIUM
    tags: List[str] = field(default_factory=list)
    custom_data: Dict[str, Any] = field(default_factory=dict)

class ScheduledJob(BaseModel):
    """Model for a scheduled job."""
    job_id: str
    content_id: str
    schedule_type: JobType
    status: JobStatus
    platforms: List[str]
    publish_date: datetime
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    cron_expression: Optional[str] = None
    end_date: Optional[datetime] = None
    metadata: JobMetadata = field(default_factory=JobMetadata)
    error: Optional[str] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary."""
        return {
            'job_id': self.job_id,
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
                'retry_count': self.metadata.retry_count,
                'max_retries': self.metadata.max_retries,
                'retry_delay': self.metadata.retry_delay,
                'priority': self.metadata.priority,
                'tags': self.metadata.tags,
                'custom_data': self.metadata.custom_data
            },
            'error': self.error,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScheduledJob':
        """Create job from dictionary."""
        metadata = JobMetadata(
            retry_count=data['metadata']['retry_count'],
            max_retries=data['metadata']['max_retries'],
            retry_delay=data['metadata']['retry_delay'],
            priority=data['metadata']['priority'],
            tags=data['metadata']['tags'],
            custom_data=data['metadata']['custom_data']
        )
        
        return cls(
            job_id=data['job_id'],
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
            next_run=datetime.fromisoformat(data['next_run']) if data.get('next_run') else None
        ) 