"""
Schedule health monitoring system.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ..utils.error_handling import SchedulingError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class HealthStatus(Enum):
    """Health check status."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class HealthCheck:
    """Health check result."""
    component: str
    status: HealthStatus
    message: str
    details: Dict[str, Any]
    timestamp: datetime

class ScheduleHealthChecker:
    """Schedule health monitoring system."""
    
    def __init__(
        self,
        scheduler,
        check_interval: int = 300,  # 5 minutes
        warning_threshold: int = 3,
        critical_threshold: int = 5
    ):
        """Initialize the health checker.
        
        Args:
            scheduler: ContentScheduler instance
            check_interval: Health check interval in seconds
            warning_threshold: Number of failures before warning
            critical_threshold: Number of failures before critical
        """
        self.logger = logger
        self.scheduler = scheduler
        self.check_interval = check_interval
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        
        # Initialize health check history
        self.health_history = []
        
        # Initialize failure counters
        self.failure_counts = {
            'job_execution': 0,
            'platform_publish': 0,
            'schedule_conflicts': 0,
            'resource_usage': 0
        }
        
        # Initialize monitoring task
        self.monitoring_task = None
    
    async def start_monitoring(self):
        """Start the health monitoring system."""
        try:
            if not self.monitoring_task:
                self.monitoring_task = asyncio.create_task(self._monitor_health())
                self.logger.info("Health monitoring started")
        except Exception as e:
            self.logger.error(f"Failed to start health monitoring: {str(e)}")
            raise SchedulingError(f"Health monitoring start failed: {str(e)}")
    
    async def stop_monitoring(self):
        """Stop the health monitoring system."""
        try:
            if self.monitoring_task:
                self.monitoring_task.cancel()
                self.monitoring_task = None
                self.logger.info("Health monitoring stopped")
        except Exception as e:
            self.logger.error(f"Failed to stop health monitoring: {str(e)}")
            raise SchedulingError(f"Health monitoring stop failed: {str(e)}")
    
    async def _monitor_health(self):
        """Monitor system health periodically."""
        while True:
            try:
                # Perform health checks
                health_checks = await self._perform_health_checks()
                
                # Update health history
                self.health_history.extend(health_checks)
                
                # Trim history if too long
                if len(self.health_history) > 1000:
                    self.health_history = self.health_history[-1000:]
                
                # Check for critical issues
                critical_checks = [
                    check for check in health_checks
                    if check.status == HealthStatus.CRITICAL
                ]
                
                if critical_checks:
                    await self._handle_critical_issues(critical_checks)
                
                # Wait for next check
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Health monitoring error: {str(e)}")
                await asyncio.sleep(self.check_interval)
    
    async def _perform_health_checks(self) -> List[HealthCheck]:
        """Perform all health checks.
        
        Returns:
            List of health check results
        """
        checks = []
        
        try:
            # Check scheduler status
            checks.append(await self._check_scheduler_status())
            
            # Check job execution
            checks.append(await self._check_job_execution())
            
            # Check platform connectivity
            checks.append(await self._check_platform_connectivity())
            
            # Check resource usage
            checks.append(await self._check_resource_usage())
            
            # Check schedule conflicts
            checks.append(await self._check_schedule_conflicts())
            
            # Check database connection
            checks.append(await self._check_database_connection())
            
            # Check job store
            checks.append(await self._check_job_store())
            
            return checks
            
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return [
                HealthCheck(
                    component="health_checker",
                    status=HealthStatus.CRITICAL,
                    message=f"Health check system error: {str(e)}",
                    details={'error': str(e)},
                    timestamp=datetime.utcnow()
                )
            ]
    
    async def _check_scheduler_status(self) -> HealthCheck:
        """Check scheduler status.
        
        Returns:
            Health check result
        """
        try:
            is_running = self.scheduler.scheduler.running
            job_count = len(self.scheduler.scheduler.get_jobs())
            
            if not is_running:
                return HealthCheck(
                    component="scheduler",
                    status=HealthStatus.CRITICAL,
                    message="Scheduler is not running",
                    details={'job_count': job_count},
                    timestamp=datetime.utcnow()
                )
            
            return HealthCheck(
                component="scheduler",
                status=HealthStatus.HEALTHY,
                message="Scheduler is running",
                details={'job_count': job_count},
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return HealthCheck(
                component="scheduler",
                status=HealthStatus.CRITICAL,
                message=f"Scheduler check failed: {str(e)}",
                details={'error': str(e)},
                timestamp=datetime.utcnow()
            )
    
    async def _check_job_execution(self) -> HealthCheck:
        """Check job execution health.
        
        Returns:
            Health check result
        """
        try:
            # Get recent job history
            recent_jobs = [
                job for job in self.scheduler.job_status.values()
                if datetime.utcnow() - job['created_at'] < timedelta(hours=24)
            ]
            
            # Calculate failure rate
            total_jobs = len(recent_jobs)
            failed_jobs = len([
                job for job in recent_jobs
                if job['status'] == 'FAILED'
            ])
            
            failure_rate = failed_jobs / total_jobs if total_jobs > 0 else 0
            
            # Update failure counter
            self.failure_counts['job_execution'] = failed_jobs
            
            if failure_rate >= 0.2:  # 20% failure rate
                return HealthCheck(
                    component="job_execution",
                    status=HealthStatus.CRITICAL,
                    message="High job failure rate detected",
                    details={
                        'total_jobs': total_jobs,
                        'failed_jobs': failed_jobs,
                        'failure_rate': failure_rate
                    },
                    timestamp=datetime.utcnow()
                )
            elif failure_rate >= 0.1:  # 10% failure rate
                return HealthCheck(
                    component="job_execution",
                    status=HealthStatus.WARNING,
                    message="Elevated job failure rate",
                    details={
                        'total_jobs': total_jobs,
                        'failed_jobs': failed_jobs,
                        'failure_rate': failure_rate
                    },
                    timestamp=datetime.utcnow()
                )
            
            return HealthCheck(
                component="job_execution",
                status=HealthStatus.HEALTHY,
                message="Job execution is healthy",
                details={
                    'total_jobs': total_jobs,
                    'failed_jobs': failed_jobs,
                    'failure_rate': failure_rate
                },
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return HealthCheck(
                component="job_execution",
                status=HealthStatus.CRITICAL,
                message=f"Job execution check failed: {str(e)}",
                details={'error': str(e)},
                timestamp=datetime.utcnow()
            )
    
    async def _check_platform_connectivity(self) -> HealthCheck:
        """Check platform connectivity.
        
        Returns:
            Health check result
        """
        try:
            # Get unique platforms from recent jobs
            platforms = set()
            for job in self.scheduler.job_status.values():
                if 'schedule' in job:
                    platforms.update(job['schedule'].platforms)
            
            # Check each platform
            platform_status = {}
            for platform in platforms:
                try:
                    adapter = self.scheduler._get_platform_adapter(platform)
                    # Try to get platform status
                    status = await adapter.get_platform_status()
                    platform_status[platform] = status['status']
                except Exception as e:
                    platform_status[platform] = 'error'
                    self.failure_counts['platform_publish'] += 1
            
            # Check overall status
            if any(status == 'error' for status in platform_status.values()):
                return HealthCheck(
                    component="platform_connectivity",
                    status=HealthStatus.CRITICAL,
                    message="Platform connectivity issues detected",
                    details={'platform_status': platform_status},
                    timestamp=datetime.utcnow()
                )
            
            return HealthCheck(
                component="platform_connectivity",
                status=HealthStatus.HEALTHY,
                message="Platform connectivity is healthy",
                details={'platform_status': platform_status},
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return HealthCheck(
                component="platform_connectivity",
                status=HealthStatus.CRITICAL,
                message=f"Platform connectivity check failed: {str(e)}",
                details={'error': str(e)},
                timestamp=datetime.utcnow()
            )
    
    async def _check_resource_usage(self) -> HealthCheck:
        """Check system resource usage.
        
        Returns:
            Health check result
        """
        try:
            import psutil
            
            # Get system metrics
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            # Check thresholds
            if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
                self.failure_counts['resource_usage'] += 1
                return HealthCheck(
                    component="resource_usage",
                    status=HealthStatus.CRITICAL,
                    message="High resource usage detected",
                    details={
                        'cpu_percent': cpu_percent,
                        'memory_percent': memory_percent,
                        'disk_percent': disk_percent
                    },
                    timestamp=datetime.utcnow()
                )
            elif cpu_percent > 70 or memory_percent > 70 or disk_percent > 70:
                return HealthCheck(
                    component="resource_usage",
                    status=HealthStatus.WARNING,
                    message="Elevated resource usage",
                    details={
                        'cpu_percent': cpu_percent,
                        'memory_percent': memory_percent,
                        'disk_percent': disk_percent
                    },
                    timestamp=datetime.utcnow()
                )
            
            return HealthCheck(
                component="resource_usage",
                status=HealthStatus.HEALTHY,
                message="Resource usage is healthy",
                details={
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory_percent,
                    'disk_percent': disk_percent
                },
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return HealthCheck(
                component="resource_usage",
                status=HealthStatus.CRITICAL,
                message=f"Resource usage check failed: {str(e)}",
                details={'error': str(e)},
                timestamp=datetime.utcnow()
            )
    
    async def _check_schedule_conflicts(self) -> HealthCheck:
        """Check for schedule conflicts.
        
        Returns:
            Health check result
        """
        try:
            # Get all pending schedules
            pending_schedules = [
                job['schedule'] for job in self.scheduler.job_status.values()
                if job['status'] == 'PENDING'
            ]
            
            # Check for conflicts
            conflicts = await self.scheduler.conflict_resolver.detect_conflicts(
                pending_schedules
            )
            
            if conflicts:
                self.failure_counts['schedule_conflicts'] += len(conflicts)
                return HealthCheck(
                    component="schedule_conflicts",
                    status=HealthStatus.WARNING,
                    message="Schedule conflicts detected",
                    details={
                        'conflict_count': len(conflicts),
                        'conflicts': [c.dict() for c in conflicts]
                    },
                    timestamp=datetime.utcnow()
                )
            
            return HealthCheck(
                component="schedule_conflicts",
                status=HealthStatus.HEALTHY,
                message="No schedule conflicts detected",
                details={'conflict_count': 0},
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return HealthCheck(
                component="schedule_conflicts",
                status=HealthStatus.CRITICAL,
                message=f"Schedule conflict check failed: {str(e)}",
                details={'error': str(e)},
                timestamp=datetime.utcnow()
            )
    
    async def _check_database_connection(self) -> HealthCheck:
        """Check database connection health.
        
        Returns:
            Health check result
        """
        try:
            session = self.scheduler.Session()
            session.execute("SELECT 1")
            session.close()
            
            return HealthCheck(
                component="database",
                status=HealthStatus.HEALTHY,
                message="Database connection is healthy",
                details={},
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return HealthCheck(
                component="database",
                status=HealthStatus.CRITICAL,
                message=f"Database connection failed: {str(e)}",
                details={'error': str(e)},
                timestamp=datetime.utcnow()
            )
    
    async def _check_job_store(self) -> HealthCheck:
        """Check job store health.
        
        Returns:
            Health check result
        """
        try:
            # Get job store statistics
            job_count = len(self.scheduler.scheduler.get_jobs())
            store_size = len(self.scheduler.job_status)
            
            if job_count != store_size:
                return HealthCheck(
                    component="job_store",
                    status=HealthStatus.WARNING,
                    message="Job store inconsistency detected",
                    details={
                        'job_count': job_count,
                        'store_size': store_size
                    },
                    timestamp=datetime.utcnow()
                )
            
            return HealthCheck(
                component="job_store",
                status=HealthStatus.HEALTHY,
                message="Job store is healthy",
                details={
                    'job_count': job_count,
                    'store_size': store_size
                },
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return HealthCheck(
                component="job_store",
                status=HealthStatus.CRITICAL,
                message=f"Job store check failed: {str(e)}",
                details={'error': str(e)},
                timestamp=datetime.utcnow()
            )
    
    async def _handle_critical_issues(self, critical_checks: List[HealthCheck]):
        """Handle critical health issues.
        
        Args:
            critical_checks: List of critical health checks
        """
        try:
            # Log critical issues
            for check in critical_checks:
                self.logger.error(
                    f"Critical health issue in {check.component}: {check.message}"
                )
            
            # Attempt recovery actions
            for check in critical_checks:
                if check.component == "scheduler" and not self.scheduler.scheduler.running:
                    await self.scheduler.start()
                
                elif check.component == "database":
                    # Attempt to reconnect
                    self.scheduler.engine.dispose()
                    self.scheduler.engine = create_engine(self.scheduler.db_url)
                    self.scheduler.Session = sessionmaker(bind=self.scheduler.engine)
                
                elif check.component == "job_store":
                    # Attempt to recover job store
                    await self.scheduler._recover_jobs()
            
            # Reset failure counters if recovery successful
            self.failure_counts = {k: 0 for k in self.failure_counts}
            
        except Exception as e:
            self.logger.error(f"Failed to handle critical issues: {str(e)}")
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health check summary.
        
        Returns:
            Dictionary containing health summary
        """
        try:
            # Get latest health checks
            latest_checks = {
                check.component: check
                for check in self.health_history[-len(self.health_history):]
            }
            
            # Calculate overall status
            if any(check.status == HealthStatus.CRITICAL for check in latest_checks.values()):
                overall_status = HealthStatus.CRITICAL
            elif any(check.status == HealthStatus.WARNING for check in latest_checks.values()):
                overall_status = HealthStatus.WARNING
            else:
                overall_status = HealthStatus.HEALTHY
            
            return {
                'status': overall_status.value,
                'components': {
                    component: {
                        'status': check.status.value,
                        'message': check.message,
                        'details': check.details,
                        'timestamp': check.timestamp.isoformat()
                    }
                    for component, check in latest_checks.items()
                },
                'failure_counts': self.failure_counts,
                'last_check': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get health summary: {str(e)}")
            return {
                'status': HealthStatus.UNKNOWN.value,
                'error': str(e),
                'last_check': datetime.utcnow().isoformat()
            } 