"""
Error Handler for 12-Step Prompt Chaining

This module handles errors and recovery across all 12 steps of the prompt chaining framework.
"""

import traceback
from typing import Dict, Any, Optional, List
from datetime import datetime
from loguru import logger


class ErrorHandler:
    """
    Handles errors and recovery across all 12 steps of the prompt chaining framework.
    
    Responsibilities:
    - Error capture and logging
    - Error classification and analysis
    - Error recovery strategies
    - Fallback mechanisms
    - Error reporting and monitoring
    """
    
    def __init__(self):
        """Initialize the error handler."""
        self.error_history: List[Dict[str, Any]] = []
        self.max_error_history = 100
        self.recovery_strategies = self._initialize_recovery_strategies()
        self.error_patterns = self._initialize_error_patterns()
        
        logger.info("🛡️ Error Handler initialized")
    
    def _initialize_recovery_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Initialize recovery strategies for different error types."""
        return {
            "step_execution_error": {
                "retry_count": 3,
                "retry_delay": 1.0,
                "fallback_strategy": "use_placeholder_data",
                "severity": "medium"
            },
            "context_error": {
                "retry_count": 1,
                "retry_delay": 0.5,
                "fallback_strategy": "reinitialize_context",
                "severity": "high"
            },
            "validation_error": {
                "retry_count": 2,
                "retry_delay": 0.5,
                "fallback_strategy": "skip_validation",
                "severity": "low"
            },
            "ai_service_error": {
                "retry_count": 3,
                "retry_delay": 2.0,
                "fallback_strategy": "use_cached_response",
                "severity": "medium"
            },
            "data_error": {
                "retry_count": 1,
                "retry_delay": 0.5,
                "fallback_strategy": "use_default_data",
                "severity": "medium"
            },
            "timeout_error": {
                "retry_count": 2,
                "retry_delay": 5.0,
                "fallback_strategy": "reduce_complexity",
                "severity": "medium"
            }
        }
    
    def _initialize_error_patterns(self) -> Dict[str, List[str]]:
        """Initialize error patterns for classification."""
        return {
            "step_execution_error": [
                "step execution failed",
                "step validation failed",
                "step timeout",
                "step not found"
            ],
            "context_error": [
                "context validation failed",
                "missing context",
                "invalid context",
                "context corruption"
            ],
            "validation_error": [
                "validation failed",
                "invalid data",
                "missing required field",
                "type error"
            ],
            "ai_service_error": [
                "ai service unavailable",
                "ai service error",
                "api error",
                "rate limit exceeded"
            ],
            "data_error": [
                "data not found",
                "data corruption",
                "invalid data format",
                "missing data"
            ],
            "timeout_error": [
                "timeout",
                "request timeout",
                "execution timeout",
                "service timeout"
            ]
        }
    
    async def handle_error(self, error: Exception, user_id: Optional[int] = None, strategy_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Handle a general error in the 12-step process.
        
        Args:
            error: The exception that occurred
            user_id: Optional user ID for context
            strategy_id: Optional strategy ID for context
            
        Returns:
            Dict containing error response and recovery information
        """
        try:
            # Capture error details
            error_info = self._capture_error(error, user_id, strategy_id)
            
            # Classify error
            error_type = self._classify_error(error)
            
            # Get recovery strategy
            recovery_strategy = self.recovery_strategies.get(error_type, self.recovery_strategies["step_execution_error"])
            
            # Generate error response
            error_response = {
                "status": "error",
                "error_type": error_type,
                "error_message": str(error),
                "error_details": error_info,
                "recovery_strategy": recovery_strategy,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "strategy_id": strategy_id
            }
            
            logger.error(f"❌ Error handled: {error_type} - {str(error)}")
            return error_response
            
        except Exception as e:
            logger.error(f"❌ Error in error handler: {str(e)}")
            return {
                "status": "error",
                "error_type": "error_handler_failure",
                "error_message": f"Error handler failed: {str(e)}",
                "original_error": str(error),
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "strategy_id": strategy_id
            }
    
    async def handle_step_error(self, step_name: str, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an error in a specific step.
        
        Args:
            step_name: Name of the step that failed
            error: The exception that occurred
            context: Current context
            
        Returns:
            Dict containing step error response and recovery information
        """
        try:
            # Capture error details
            error_info = self._capture_error(error, context.get("user_id"), context.get("strategy_id"))
            error_info["step_name"] = step_name
            error_info["step_number"] = self._extract_step_number(step_name)
            error_info["phase"] = context.get("phase", "unknown")
            
            # Classify error
            error_type = self._classify_error(error)
            
            # Get recovery strategy
            recovery_strategy = self.recovery_strategies.get(error_type, self.recovery_strategies["step_execution_error"])
            
            # Generate fallback result
            fallback_result = await self._generate_fallback_result(step_name, error_type, context)
            
            # Generate step error response
            step_error_response = {
                "step_name": step_name,
                "step_number": error_info["step_number"],
                "status": "error",
                "error_type": error_type,
                "error_message": str(error),
                "error_details": error_info,
                "recovery_strategy": recovery_strategy,
                "fallback_result": fallback_result,
                "execution_time": 0.0,
                "quality_score": 0.0,
                "validation_passed": False,
                "timestamp": datetime.now().isoformat(),
                "insights": [f"Step {step_name} failed: {str(error)}"],
                "next_steps": [f"Recover from {step_name} error and continue"]
            }
            
            logger.error(f"❌ Step error handled: {step_name} - {error_type} - {str(error)}")
            return step_error_response
            
        except Exception as e:
            logger.error(f"❌ Error in step error handler: {str(e)}")
            return {
                "step_name": step_name,
                "status": "error",
                "error_type": "step_error_handler_failure",
                "error_message": f"Step error handler failed: {str(e)}",
                "original_error": str(error),
                "timestamp": datetime.now().isoformat()
            }
    
    def _capture_error(self, error: Exception, user_id: Optional[int] = None, strategy_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Capture detailed error information.
        
        Args:
            error: The exception that occurred
            user_id: Optional user ID
            strategy_id: Optional strategy ID
            
        Returns:
            Dict containing error details
        """
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "strategy_id": strategy_id
        }
        
        # Add to error history
        self.error_history.append(error_info)
        
        # Limit history size
        if len(self.error_history) > self.max_error_history:
            self.error_history.pop(0)
        
        return error_info
    
    def _classify_error(self, error: Exception) -> str:
        """
        Classify the error based on error patterns.
        
        Args:
            error: The exception to classify
            
        Returns:
            Error classification
        """
        error_message = str(error).lower()
        
        for error_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                if pattern.lower() in error_message:
                    return error_type
        
        # Default classification
        return "step_execution_error"
    
    def _extract_step_number(self, step_name: str) -> int:
        """
        Extract step number from step name.
        
        Args:
            step_name: Name of the step
            
        Returns:
            Step number
        """
        try:
            return int(step_name.split("_")[-1])
        except (ValueError, IndexError):
            return 0
    
    async def _generate_fallback_result(self, step_name: str, error_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate fallback result for a failed step.
        
        Args:
            step_name: Name of the failed step
            error_type: Type of error that occurred
            context: Current context
            
        Returns:
            Fallback result
        """
        step_number = self._extract_step_number(step_name)
        
        # Generate basic fallback based on step type
        fallback_result = {
            "placeholder": True,
            "step_name": step_name,
            "step_number": step_number,
            "error_type": error_type,
            "fallback_generated_at": datetime.now().isoformat()
        }
        
        # Add step-specific fallback data
        if step_number <= 3:  # Foundation phase
            fallback_result.update({
                "insights": [f"Fallback insights for {step_name}"],
                "recommendations": [f"Fallback recommendation for {step_name}"],
                "analysis": {
                    "summary": f"Fallback analysis for {step_name}",
                    "details": f"Fallback detailed analysis for {step_name}"
                }
            })
        elif step_number <= 6:  # Structure phase
            fallback_result.update({
                "structure_data": {},
                "framework_data": {},
                "timeline_data": {}
            })
        elif step_number <= 9:  # Content phase
            fallback_result.update({
                "content_data": [],
                "themes_data": [],
                "schedule_data": []
            })
        else:  # Optimization phase
            fallback_result.update({
                "optimization_data": {},
                "performance_data": {},
                "validation_data": {}
            })
        
        return fallback_result
    
    def get_error_history(self) -> List[Dict[str, Any]]:
        """
        Get the error history.
        
        Returns:
            List of error history entries
        """
        return self.error_history.copy()
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """
        Get error statistics.
        
        Returns:
            Dict containing error statistics
        """
        if not self.error_history:
            return {
                "total_errors": 0,
                "error_types": {},
                "recent_errors": [],
                "error_rate": 0.0
            }
        
        # Count error types
        error_types = {}
        for error in self.error_history:
            error_type = error.get("error_type", "unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Get recent errors (last 10)
        recent_errors = self.error_history[-10:] if len(self.error_history) > 10 else self.error_history
        
        return {
            "total_errors": len(self.error_history),
            "error_types": error_types,
            "recent_errors": recent_errors,
            "error_rate": len(self.error_history) / max(1, len(self.error_history))
        }
    
    def clear_error_history(self):
        """Clear the error history."""
        self.error_history.clear()
        logger.info("🔄 Error history cleared")
    
    def get_recovery_strategy(self, error_type: str) -> Dict[str, Any]:
        """
        Get recovery strategy for an error type.
        
        Args:
            error_type: Type of error
            
        Returns:
            Recovery strategy
        """
        return self.recovery_strategies.get(error_type, self.recovery_strategies["step_execution_error"])
    
    def add_custom_recovery_strategy(self, error_type: str, strategy: Dict[str, Any]):
        """
        Add a custom recovery strategy.
        
        Args:
            error_type: Type of error
            strategy: Recovery strategy configuration
        """
        self.recovery_strategies[error_type] = strategy
        logger.info(f"📝 Added custom recovery strategy for {error_type}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get health status of the error handler.
        
        Returns:
            Dict containing health status
        """
        return {
            "service": "error_handler",
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "total_errors_handled": len(self.error_history),
            "recovery_strategies_configured": len(self.recovery_strategies),
            "error_patterns_configured": len(self.error_patterns),
            "max_error_history": self.max_error_history
        }
