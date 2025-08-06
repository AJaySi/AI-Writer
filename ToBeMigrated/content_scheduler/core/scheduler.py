"""
Core scheduler implementation using APScheduler.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_MISSED
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use unified database models
from lib.database.models import ContentItem, Schedule, ScheduleStatus, get_engine, get_session, init_db
from ..utils.error_handling import SchedulingError
from .conflict_resolver import ConflictResolver
from .health_checker import ScheduleHealthChecker
from .schedule_validator import ScheduleValidator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ContentScheduler:
    """Core content scheduler implementation."""
    
    def __init__(
        self,
        db_url: str = "sqlite:///content_scheduler.db",
        max_workers: int = 10,
        job_timeout: int = 300,
        max_retries: int = 3,
        retry_delay: int = 300,
        health_check_interval: int = 300,
        validation_config: Dict[str, Any] = None
    ):
        """Initialize the content scheduler.
        
        Args:
            db_url: Database URL for job persistence
            max_workers: Maximum number of worker threads
            job_timeout: Job execution timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            health_check_interval: Health check interval in seconds
            validation_config: Configuration for schedule validation
        """
        self.logger = logger
        self.db_url = db_url
        self.max_workers = max_workers
        self.job_timeout = job_timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Use unified database connection
        self.engine = get_engine(db_url)
        init_db(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
        # Initialize job stores
        self.jobstores = {
            'default': SQLAlchemyJobStore(url=db_url)
        }
        
        # Initialize executors
        self.executors = {
            'default': ThreadPoolExecutor(max_workers),
            'processpool': ProcessPoolExecutor(max_workers)
        }
        
        # Initialize scheduler
        self.scheduler = AsyncIOScheduler(
            jobstores=self.jobstores,
            executors=self.executors,
            timezone='UTC',
            job_defaults={
                'coalesce': True,
                'max_instances': 1,
                'misfire_grace_time': 60
            }
        )
        
        # Initialize conflict resolver
        self.conflict_resolver = ConflictResolver()
        
        # Initialize health checker
        self.health_checker = ScheduleHealthChecker(
            scheduler=self,
            check_interval=health_check_interval
        )
        
        # Initialize validator
        self.validator = ScheduleValidator(validation_config or {})
        
        # Add event listeners
        self.scheduler.add_listener(
            self._handle_job_event,
            EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED
        )
        
        # Track active jobs
        self.active_jobs = {}
        self.job_stats = {
            'total_scheduled': 0,
            'successful': 0,
            'failed': 0,
            'retries': 0
        }

    async def start(self):
        """Start the scheduler."""
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                await self._recover_jobs()
                await self.health_checker.start()
                self.logger.info("Content scheduler started successfully")
        except Exception as e:
            self.logger.error(f"Failed to start scheduler: {str(e)}")
            raise SchedulingError(f"Scheduler startup failed: {str(e)}")

    async def stop(self):
        """Stop the scheduler."""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown(wait=True)
                await self.health_checker.stop()
                self.logger.info("Content scheduler stopped successfully")
        except Exception as e:
            self.logger.error(f"Failed to stop scheduler: {str(e)}")
            raise SchedulingError(f"Scheduler shutdown failed: {str(e)}")

    async def schedule_content(self, content_item: ContentItem, schedule_time: datetime, 
                             platforms: List[str], recurrence: str = None, 
                             validate: bool = True) -> str:
        """Schedule content for publishing.
        
        Args:
            content_item: ContentItem to schedule
            schedule_time: When to publish
            platforms: List of platforms to publish to
            recurrence: Recurrence pattern (optional)
            validate: Whether to validate the schedule
            
        Returns:
            Schedule ID
        """
        try:
            session = self.Session()
            
            # Create schedule record
            schedule = Schedule(
                content_item_id=content_item.id,
                scheduled_time=schedule_time,
                status=ScheduleStatus.SCHEDULED,
                recurrence=recurrence,
                priority=1
            )
            
            session.add(schedule)
            session.commit()
            
            # Schedule the job
            if recurrence:
                job_id = await self._schedule_recurring(schedule, platforms)
            else:
                job_id = await self._schedule_one_time(schedule, platforms)
            
            # Update schedule with job ID
            schedule.result = f"job_id:{job_id}"
            session.commit()
            session.close()
            
            self.job_stats['total_scheduled'] += 1
            self.logger.info(f"Scheduled content {content_item.id} for {schedule_time}")
            
            return str(schedule.id)
            
        except Exception as e:
            self.logger.error(f"Failed to schedule content: {str(e)}")
            if 'session' in locals():
                session.rollback()
                session.close()
            raise SchedulingError(f"Content scheduling failed: {str(e)}")

    async def _schedule_one_time(self, schedule: Schedule, platforms: List[str]) -> str:
        """Schedule a one-time content publish.
        
        Args:
            schedule: Schedule object
            platforms: List of platforms
            
        Returns:
            Job ID
        """
        try:
            job_id = f"one_time_{schedule.content_item_id}_{int(schedule.scheduled_time.timestamp())}"
            
            self.scheduler.add_job(
                self._run_async_job,
                trigger=DateTrigger(run_date=schedule.scheduled_time),
                args=[schedule, platforms],
                id=job_id,
                replace_existing=True,
                misfire_grace_time=self.job_timeout
            )
            
            return job_id
            
        except Exception as e:
            self.logger.error(f"Failed to schedule one-time job: {str(e)}")
            raise SchedulingError(f"One-time scheduling failed: {str(e)}")
    
    async def _schedule_recurring(self, schedule: Schedule, platforms: List[str]) -> str:
        """Schedule a recurring content publish.
        
        Args:
            schedule: Schedule object
            platforms: List of platforms
            
        Returns:
            Job ID
        """
        try:
            job_id = f"recurring_{schedule.content_item_id}_{int(datetime.utcnow().timestamp())}"
            
            # Parse recurrence pattern (simplified)
            if schedule.recurrence == "daily":
                trigger = CronTrigger(hour=schedule.scheduled_time.hour, minute=schedule.scheduled_time.minute)
            elif schedule.recurrence == "weekly":
                trigger = CronTrigger(day_of_week=schedule.scheduled_time.weekday(), 
                                    hour=schedule.scheduled_time.hour, 
                                    minute=schedule.scheduled_time.minute)
            else:
                # Default to daily
                trigger = CronTrigger(hour=schedule.scheduled_time.hour, minute=schedule.scheduled_time.minute)
            
            self.scheduler.add_job(
                self._run_async_job,
                trigger=trigger,
                args=[schedule, platforms],
                id=job_id,
                replace_existing=True,
                misfire_grace_time=self.job_timeout
            )
            
            return job_id
            
        except Exception as e:
            self.logger.error(f"Failed to schedule recurring job: {str(e)}")
            raise SchedulingError(f"Recurring scheduling failed: {str(e)}")
    
    async def _run_async_job(self, schedule: Schedule, platforms: List[str]):
        """Run an async job in the event loop.
        
        Args:
            schedule: Schedule object
            platforms: List of platforms
        """
        try:
            await self._publish_content(schedule, platforms)
        except Exception as e:
            self.logger.error(f"Job execution failed: {str(e)}")
            await self._handle_job_failure(schedule, str(e))

    async def _publish_content(self, schedule: Schedule, platforms: List[str]):
        """Publish content to specified platforms.
        
        Args:
            schedule: Schedule object
            platforms: List of platforms
        """
        try:
            session = self.Session()
            content_item = session.query(ContentItem).get(schedule.content_item_id)
            
            if not content_item:
                raise SchedulingError(f"Content item {schedule.content_item_id} not found")
            
            # Update schedule status
            schedule.status = ScheduleStatus.RUNNING
            session.commit()
            
            # Simulate content publishing (replace with actual platform publishing logic)
            self.logger.info(f"Publishing content '{content_item.title}' to platforms: {platforms}")
            
            # Mark as completed
            schedule.status = ScheduleStatus.COMPLETED
            schedule.result = f"Published to {', '.join(platforms)} at {datetime.utcnow()}"
            session.commit()
            session.close()
            
            self.job_stats['successful'] += 1
            
        except Exception as e:
            session = self.Session()
            schedule.status = ScheduleStatus.FAILED
            schedule.result = f"Failed: {str(e)}"
            session.commit()
            session.close()
            
            self.job_stats['failed'] += 1
            raise

    async def _handle_job_failure(self, schedule: Schedule, error: str):
        """Handle job failure and retry logic.
        
        Args:
            schedule: Schedule object
            error: Error message
        """
        try:
            session = self.Session()
            schedule.status = ScheduleStatus.FAILED
            schedule.result = f"Failed: {error}"
            session.commit()
            session.close()
            
            self.job_stats['failed'] += 1
            self.logger.error(f"Job failed for schedule {schedule.id}: {error}")
            
        except Exception as e:
            self.logger.error(f"Error handling job failure: {str(e)}")

    def _handle_job_event(self, event):
        """Handle scheduler events.
        
        Args:
            event: Scheduler event
        """
        try:
            job_id = event.job_id
            
            if event.code == EVENT_JOB_EXECUTED:
                self.logger.info(f"Job {job_id} executed successfully")
                
            elif event.code == EVENT_JOB_ERROR:
                self.logger.error(f"Job {job_id} failed: {str(event.exception)}")
                
            elif event.code == EVENT_JOB_MISSED:
                self.logger.warning(f"Job {job_id} missed execution time")
                
        except Exception as e:
            self.logger.error(f"Error handling job event: {str(e)}")
    
    async def _recover_jobs(self):
        """Recover pending jobs from the database."""
        try:
            session = self.Session()
            
            # Get all scheduled jobs
            pending_schedules = session.query(Schedule).filter(
                Schedule.status == ScheduleStatus.SCHEDULED
            ).all()
            
            # Reschedule each job
            for schedule in pending_schedules:
                try:
                    content_item = session.query(ContentItem).get(schedule.content_item_id)
                    if content_item:
                        platforms = content_item.platforms if isinstance(content_item.platforms, list) else []
                        await self.schedule_content(content_item, schedule.scheduled_time, platforms, 
                                                  schedule.recurrence, validate=False)
                except Exception as e:
                    self.logger.error(f"Failed to recover schedule {schedule.id}: {str(e)}")
            
            session.close()
            
        except Exception as e:
            self.logger.error(f"Job recovery failed: {str(e)}")
            raise SchedulingError(f"Job recovery failed: {str(e)}")

    def get_job_stats(self) -> Dict[str, int]:
        """Get job statistics.
        
        Returns:
            Dictionary with job statistics
        """
        return self.job_stats.copy()

    def get_active_jobs(self) -> List[Dict[str, Any]]:
        """Get list of active jobs.
        
        Returns:
            List of active job information
        """
        try:
            jobs = []
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                    'trigger': str(job.trigger)
                })
            return jobs
        except Exception as e:
            self.logger.error(f"Error getting active jobs: {str(e)}")
            return [] 