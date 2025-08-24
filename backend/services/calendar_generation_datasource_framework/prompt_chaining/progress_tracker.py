"""
Progress Tracker for 12-Step Prompt Chaining

This module tracks and reports progress across all 12 steps of the prompt chaining framework.
"""

import time
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from loguru import logger


class ProgressTracker:
    """
    Tracks and reports progress across all 12 steps of the prompt chaining framework.
    
    Responsibilities:
    - Progress initialization and setup
    - Real-time progress updates
    - Progress callbacks and notifications
    - Progress statistics and analytics
    - Progress persistence and recovery
    """
    
    def __init__(self):
        """Initialize the progress tracker."""
        self.total_steps = 0
        self.completed_steps = 0
        self.current_step = 0
        self.step_progress: Dict[str, Dict[str, Any]] = {}
        self.start_time = None
        self.end_time = None
        self.progress_callback: Optional[Callable] = None
        self.progress_history: List[Dict[str, Any]] = []
        self.max_history_size = 100
        
        logger.info("📊 Progress Tracker initialized")
    
    def initialize(self, total_steps: int, progress_callback: Optional[Callable] = None):
        """
        Initialize progress tracking.
        
        Args:
            total_steps: Total number of steps to track
            progress_callback: Optional callback function for progress updates
        """
        self.total_steps = total_steps
        self.completed_steps = 0
        self.current_step = 0
        self.step_progress = {}
        self.start_time = time.time()
        self.end_time = None
        self.progress_callback = progress_callback
        self.progress_history = []
        
        logger.info(f"📊 Progress tracking initialized for {total_steps} steps")
        logger.info(f"📊 Initial state - total_steps: {self.total_steps}, completed_steps: {self.completed_steps}, current_step: {self.current_step}")
    
    def update_progress(self, step_name: str, step_result: Dict[str, Any]):
        """
        Update progress with step result.
        
        Args:
            step_name: Name of the completed step
            step_result: Result from the step
        """
        try:
            logger.info(f"📊 ProgressTracker.update_progress called for {step_name}")
            logger.info(f"📋 Step result keys: {list(step_result.keys()) if step_result else 'None'}")
            
            # Update step progress
            step_number = step_result.get("step_number", 0)
            execution_time = step_result.get("execution_time", 0.0)
            quality_score = step_result.get("quality_score", 0.0)
            status = step_result.get("status", "unknown")
            
            logger.info(f"🔢 Step number: {step_number}, Status: {status}, Quality: {quality_score}")
            
            self.step_progress[step_name] = {
                "step_number": step_number,
                "step_name": step_result.get("step_name", step_name),
                "status": status,
                "execution_time": execution_time,
                "quality_score": quality_score,
                "completed_at": datetime.now().isoformat(),
                "insights": step_result.get("insights", []),
                "next_steps": step_result.get("next_steps", [])
            }
            
            # Update counters
            if status == "completed":
                self.completed_steps += 1
            elif status == "timeout" or status == "error" or status == "failed":
                # Don't increment completed steps for failed steps
                logger.warning(f"Step {step_number} failed with status: {status}")
            
            self.current_step = max(self.current_step, step_number)
            
            # Add to history
            self._add_to_history(step_name, step_result)
            
            # Trigger callback
            if self.progress_callback:
                try:
                    logger.info(f"🔄 Calling progress callback for {step_name}")
                    progress_data = self.get_progress()
                    logger.info(f"📊 Progress data: {progress_data}")
                    self.progress_callback(progress_data)
                    logger.info(f"✅ Progress callback completed for {step_name}")
                except Exception as e:
                    logger.error(f"❌ Error in progress callback: {str(e)}")
            else:
                logger.warning(f"⚠️ No progress callback registered for {step_name}")
            
            logger.info(f"📊 Progress updated: {self.completed_steps}/{self.total_steps} steps completed")
            
        except Exception as e:
            logger.error(f"❌ Error updating progress for {step_name}: {str(e)}")
            import traceback
            logger.error(f"📋 Traceback: {traceback.format_exc()}")
    
    def _add_to_history(self, step_name: str, step_result: Dict[str, Any]):
        """Add progress update to history."""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "step_name": step_name,
            "step_number": step_result.get("step_number", 0),
            "status": step_result.get("status", "unknown"),
            "execution_time": step_result.get("execution_time", 0.0),
            "quality_score": step_result.get("quality_score", 0.0),
            "completed_steps": self.completed_steps,
            "total_steps": self.total_steps,
            "progress_percentage": self.get_progress_percentage()
        }
        
        self.progress_history.append(history_entry)
        
        # Limit history size
        if len(self.progress_history) > self.max_history_size:
            self.progress_history.pop(0)
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Get current progress information.
        
        Returns:
            Dict containing current progress
        """
        current_time = time.time()
        elapsed_time = current_time - self.start_time if self.start_time else 0
        
        # Calculate estimated time remaining
        estimated_time_remaining = self._calculate_estimated_time_remaining(elapsed_time)
        
        # Calculate overall quality score
        overall_quality_score = self._calculate_overall_quality_score()
        
        progress_data = {
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "current_step": self.current_step,
            "progress_percentage": self.get_progress_percentage(),
            "elapsed_time": elapsed_time,
            "estimated_time_remaining": estimated_time_remaining,
            "overall_quality_score": overall_quality_score,
            "current_phase": self._get_current_phase(),
            "step_details": self.step_progress.copy(),
            "status": self._get_overall_status(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Debug logging
        logger.info(f"📊 Progress tracker returning data:")
        logger.info(f"   - total_steps: {progress_data['total_steps']}")
        logger.info(f"   - completed_steps: {progress_data['completed_steps']}")
        logger.info(f"   - current_step: {progress_data['current_step']}")
        logger.info(f"   - progress_percentage: {progress_data['progress_percentage']}")
        
        return progress_data
    
    def get_progress_percentage(self) -> float:
        """
        Get progress percentage.
        
        Returns:
            Progress percentage (0.0 to 100.0)
        """
        if self.total_steps == 0:
            return 0.0
        
        return (self.completed_steps / self.total_steps) * 100.0
    
    def _calculate_estimated_time_remaining(self, elapsed_time: float) -> float:
        """
        Calculate estimated time remaining.
        
        Args:
            elapsed_time: Time elapsed so far
            
        Returns:
            Estimated time remaining in seconds
        """
        if self.completed_steps == 0:
            return 0.0
        
        # Calculate average time per step
        average_time_per_step = elapsed_time / self.completed_steps
        
        # Estimate remaining time
        remaining_steps = self.total_steps - self.completed_steps
        estimated_remaining = average_time_per_step * remaining_steps
        
        return estimated_remaining
    
    def _calculate_overall_quality_score(self) -> float:
        """
        Calculate overall quality score from all completed steps.
        
        Returns:
            Overall quality score (0.0 to 1.0)
        """
        if not self.step_progress:
            return 0.0
        
        quality_scores = [
            step_data["quality_score"]
            for step_data in self.step_progress.values()
            if step_data["status"] == "completed"
        ]
        
        if not quality_scores:
            return 0.0
        
        # Calculate weighted average (later steps have more weight)
        total_weight = 0
        weighted_sum = 0
        
        for step_data in self.step_progress.values():
            if step_data["status"] == "completed":
                step_number = step_data["step_number"]
                quality_score = step_data["quality_score"]
                weight = step_number  # Weight by step number
                weighted_sum += quality_score * weight
                total_weight += weight
        
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        return min(overall_score, 1.0)
    
    def _get_current_phase(self) -> str:
        """
        Get the current phase based on step number.
        
        Returns:
            Current phase name
        """
        if self.current_step <= 3:
            return "Phase 1: Foundation"
        elif self.current_step <= 6:
            return "Phase 2: Structure"
        elif self.current_step <= 9:
            return "Phase 3: Content"
        elif self.current_step <= 12:
            return "Phase 4: Optimization"
        else:
            return "Unknown"
    
    def _get_overall_status(self) -> str:
        """
        Get the overall status of the process.
        
        Returns:
            Overall status
        """
        if self.completed_steps == 0:
            return "not_started"
        elif self.completed_steps < self.total_steps:
            return "in_progress"
        else:
            return "completed"
    
    def get_step_progress(self, step_name: str) -> Optional[Dict[str, Any]]:
        """
        Get progress for a specific step.
        
        Args:
            step_name: Name of the step
            
        Returns:
            Step progress information or None if not found
        """
        return self.step_progress.get(step_name)
    
    def get_progress_history(self) -> List[Dict[str, Any]]:
        """
        Get the progress history.
        
        Returns:
            List of progress history entries
        """
        return self.progress_history.copy()
    
    def get_progress_statistics(self) -> Dict[str, Any]:
        """
        Get detailed progress statistics.
        
        Returns:
            Dict containing progress statistics
        """
        if not self.step_progress:
            return {
                "total_steps": self.total_steps,
                "completed_steps": 0,
                "average_execution_time": 0.0,
                "average_quality_score": 0.0,
                "fastest_step": None,
                "slowest_step": None,
                "best_quality_step": None,
                "worst_quality_step": None
            }
        
        # Calculate statistics
        execution_times = [
            step_data["execution_time"]
            for step_data in self.step_progress.values()
            if step_data["status"] == "completed"
        ]
        
        quality_scores = [
            step_data["quality_score"]
            for step_data in self.step_progress.values()
            if step_data["status"] == "completed"
        ]
        
        # Find fastest and slowest steps
        fastest_step = min(self.step_progress.items(), key=lambda x: x[1]["execution_time"])[0] if execution_times else None
        slowest_step = max(self.step_progress.items(), key=lambda x: x[1]["execution_time"])[0] if execution_times else None
        
        # Find best and worst quality steps
        best_quality_step = max(self.step_progress.items(), key=lambda x: x[1]["quality_score"])[0] if quality_scores else None
        worst_quality_step = min(self.step_progress.items(), key=lambda x: x[1]["quality_score"])[0] if quality_scores else None
        
        return {
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "average_execution_time": sum(execution_times) / len(execution_times) if execution_times else 0.0,
            "average_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0.0,
            "fastest_step": fastest_step,
            "slowest_step": slowest_step,
            "best_quality_step": best_quality_step,
            "worst_quality_step": worst_quality_step,
            "total_execution_time": sum(execution_times),
            "overall_quality_score": self._calculate_overall_quality_score()
        }
    
    def mark_completed(self):
        """Mark the process as completed."""
        self.end_time = time.time()
        self.completed_steps = self.total_steps
        self.current_step = self.total_steps
        
        logger.info("✅ Progress tracking marked as completed")
    
    def reset(self):
        """Reset progress tracking."""
        self.total_steps = 0
        self.completed_steps = 0
        self.current_step = 0
        self.step_progress = {}
        self.start_time = None
        self.end_time = None
        self.progress_history = []
        
        logger.info("🔄 Progress tracking reset")
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get health status of the progress tracker.
        
        Returns:
            Dict containing health status
        """
        return {
            "service": "progress_tracker",
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "progress_percentage": self.get_progress_percentage(),
            "history_size": len(self.progress_history),
            "max_history_size": self.max_history_size,
            "callback_configured": self.progress_callback is not None
        }
