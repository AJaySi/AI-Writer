"""
Base Step Class for 12-Step Prompt Chaining

This module provides the base class for all steps in the 12-step prompt chaining framework.
Each step inherits from this base class and implements specific functionality.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from loguru import logger


class PromptStep(ABC):
    """
    Base class for all steps in the 12-step prompt chaining framework.
    
    Each step is responsible for:
    - Executing specific calendar generation logic
    - Validating step results
    - Providing step-specific insights
    - Contributing to overall calendar quality
    """
    
    def __init__(self, name: str, step_number: int):
        """
        Initialize the base step.
        
        Args:
            name: Human-readable name of the step
            step_number: Sequential number of the step (1-12)
        """
        self.name = name
        self.step_number = step_number
        self.execution_time = 0
        self.status = "initialized"
        self.error_message = None
        self.quality_score = 0.0
        
        logger.info(f"🎯 Initialized {self.name} (Step {step_number})")
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the step logic.
        
        Args:
            context: Current context containing user data and previous step results
            
        Returns:
            Dict containing step results and insights
        """
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """
        Get the AI prompt template for this step.
        
        Returns:
            String containing the prompt template
        """
        pass
    
    @abstractmethod
    def validate_result(self, result: Dict[str, Any]) -> bool:
        """
        Validate the step result.
        
        Args:
            result: Step result to validate
            
        Returns:
            True if validation passes, False otherwise
        """
        pass
    
    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the complete step execution including timing and validation.
        
        Args:
            context: Current context containing user data and previous step results
            
        Returns:
            Dict containing step results, metadata, and validation status
        """
        try:
            start_time = time.time()
            self.status = "running"
            
            logger.info(f"🚀 Starting {self.name} (Step {self.step_number})")
            
            # Execute step logic
            result = await self.execute(context)
            
            # Calculate execution time
            self.execution_time = time.time() - start_time
            
            # Validate result
            validation_passed = self.validate_result(result)
            
            # Calculate quality score
            self.quality_score = self._calculate_quality_score(result, validation_passed)
            
            # Prepare step response
            step_response = {
                "step_name": self.name,
                "step_number": self.step_number,
                "status": "completed" if validation_passed else "failed",
                "execution_time": self.execution_time,
                "quality_score": self.quality_score,
                "validation_passed": validation_passed,
                "timestamp": datetime.now().isoformat(),
                "result": result,
                "insights": self._extract_insights(result),
                "next_steps": self._get_next_steps(result)
            }
            
            if not validation_passed:
                step_response["error_message"] = "Step validation failed"
                self.status = "failed"
                self.error_message = "Step validation failed"
            else:
                self.status = "completed"
            
            logger.info(f"✅ {self.name} completed in {self.execution_time:.2f}s (Quality: {self.quality_score:.2f})")
            return step_response
            
        except Exception as e:
            self.execution_time = time.time() - start_time if 'start_time' in locals() else 0
            self.status = "error"
            self.error_message = str(e)
            self.quality_score = 0.0
            
            logger.error(f"❌ {self.name} failed: {str(e)}")
            
            return {
                "step_name": self.name,
                "step_number": self.step_number,
                "status": "error",
                "execution_time": self.execution_time,
                "quality_score": 0.0,
                "validation_passed": False,
                "timestamp": datetime.now().isoformat(),
                "error_message": str(e),
                "result": {},
                "insights": [],
                "next_steps": []
            }
    
    def _calculate_quality_score(self, result: Dict[str, Any], validation_passed: bool) -> float:
        """
        Calculate quality score for the step result.
        
        Args:
            result: Step result
            validation_passed: Whether validation passed
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        if not validation_passed:
            return 0.0
        
        # Base quality score
        base_score = 0.8
        
        # Adjust based on result completeness
        if result and len(result) > 0:
            base_score += 0.1
        
        # Adjust based on execution time (faster is better, but not too fast)
        if 0.1 <= self.execution_time <= 10.0:
            base_score += 0.05
        
        # Adjust based on insights generated
        insights = self._extract_insights(result)
        if insights and len(insights) > 0:
            base_score += 0.05
        
        return min(base_score, 1.0)
    
    def _extract_insights(self, result: Dict[str, Any]) -> List[str]:
        """
        Extract insights from step result.
        
        Args:
            result: Step result
            
        Returns:
            List of insights
        """
        insights = []
        
        if not result:
            return insights
        
        # Extract key insights based on step type
        if "insights" in result:
            insights.extend(result["insights"])
        
        if "recommendations" in result:
            insights.extend([f"Recommendation: {rec}" for rec in result["recommendations"][:3]])
        
        if "analysis" in result:
            insights.append(f"Analysis completed: {result['analysis'].get('summary', 'N/A')}")
        
        return insights[:5]  # Limit to 5 insights
    
    def _get_next_steps(self, result: Dict[str, Any]) -> List[str]:
        """
        Get next steps based on current result.
        
        Args:
            result: Step result
            
        Returns:
            List of next steps
        """
        next_steps = []
        
        if not result:
            return next_steps
        
        # Add step-specific next steps
        if self.step_number < 12:
            next_steps.append(f"Proceed to Step {self.step_number + 1}")
        
        # Add result-specific next steps
        if "next_actions" in result:
            next_steps.extend(result["next_actions"])
        
        return next_steps
    
    def get_step_info(self) -> Dict[str, Any]:
        """
        Get information about this step.
        
        Returns:
            Dict containing step information
        """
        return {
            "name": self.name,
            "step_number": self.step_number,
            "status": self.status,
            "quality_score": self.quality_score,
            "execution_time": self.execution_time,
            "error_message": self.error_message,
            "prompt_template": self.get_prompt_template()
        }
    
    def reset(self):
        """Reset step state for re-execution."""
        self.execution_time = 0
        self.status = "initialized"
        self.error_message = None
        self.quality_score = 0.0
        logger.info(f"🔄 Reset {self.name} (Step {self.step_number})")


class PlaceholderStep(PromptStep):
    """
    Placeholder step implementation for development and testing.
    """
    
    def __init__(self, name: str, step_number: int):
        super().__init__(name, step_number)
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute placeholder step logic."""
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        return {
            "placeholder": True,
            "step_name": self.name,
            "step_number": self.step_number,
            "insights": [f"Placeholder insights for {self.name}"],
            "recommendations": [f"Placeholder recommendation for {self.name}"],
            "analysis": {
                "summary": f"Placeholder analysis for {self.name}",
                "details": f"Detailed placeholder analysis for {self.name}"
            }
        }
    
    def get_prompt_template(self) -> str:
        """Get placeholder prompt template."""
        return f"Placeholder prompt template for {self.name}"
    
    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validate placeholder result."""
        return result is not None and "placeholder" in result
