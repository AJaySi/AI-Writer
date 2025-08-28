"""Base service for Facebook Writer functionality."""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger

# Add the backend path to sys.path to import services
backend_path = Path(__file__).parent.parent.parent.parent
sys.path.append(str(backend_path))

from services.llm_providers.gemini_provider import gemini_text_response, gemini_structured_json_response


class FacebookWriterBaseService:
    """Base service class for Facebook Writer functionality."""
    
    def __init__(self):
        """Initialize the base service."""
        self.logger = logger
        
    def _generate_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        Generate text using Gemini provider.
        
        Args:
            prompt: The prompt to send to the AI
            temperature: Control randomness of output
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response
        """
        try:
            response = gemini_text_response(
                prompt=prompt,
                temperature=temperature,
                top_p=0.9,
                n=40,
                max_tokens=max_tokens,
                system_prompt=None
            )
            return response
        except Exception as e:
            self.logger.error(f"Error generating text: {e}")
            raise
    
    def _generate_structured_response(
        self, 
        prompt: str, 
        schema: Dict[str, Any], 
        temperature: float = 0.3, 
        max_tokens: int = 8192
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response using Gemini provider.
        
        Args:
            prompt: The prompt to send to the AI
            schema: JSON schema for structured output
            temperature: Control randomness (lower for structured output)
            max_tokens: Maximum tokens in response
            
        Returns:
            Structured JSON response
        """
        try:
            response = gemini_structured_json_response(
                prompt=prompt,
                schema=schema,
                temperature=temperature,
                top_p=0.9,
                top_k=40,
                max_tokens=max_tokens,
                system_prompt=None
            )
            return response
        except Exception as e:
            self.logger.error(f"Error generating structured response: {e}")
            raise
    
    def _build_base_prompt(self, business_type: str, target_audience: str, purpose: str) -> str:
        """
        Build a base prompt for Facebook content generation.
        
        Args:
            business_type: Type of business
            target_audience: Target audience description
            purpose: Purpose or goal of the content
            
        Returns:
            Base prompt string
        """
        return f"""
        You are an expert Facebook content creator specializing in creating engaging, high-performing social media content.
        
        Business Context:
        - Business Type: {business_type}
        - Target Audience: {target_audience}
        - Content Purpose: {purpose}
        
        Create content that:
        1. Resonates with the target audience
        2. Aligns with Facebook's best practices
        3. Encourages engagement and interaction
        4. Maintains a professional yet approachable tone
        5. Includes relevant calls-to-action when appropriate
        """
    
    def _create_analytics_prediction(self) -> Dict[str, str]:
        """
        Create default analytics predictions.
        
        Returns:
            Dictionary with analytics predictions
        """
        return {
            "expected_reach": "2.5K - 5K",
            "expected_engagement": "5-8%",
            "best_time_to_post": "2 PM - 4 PM"
        }
    
    def _create_optimization_suggestions(self, content_type: str = "post") -> list:
        """
        Create default optimization suggestions.
        
        Args:
            content_type: Type of content being optimized
            
        Returns:
            List of optimization suggestions
        """
        base_suggestions = [
            "Consider adding a question to increase comments",
            "Use more emojis to increase visibility",
            "Keep paragraphs shorter for better readability"
        ]
        
        if content_type == "post":
            base_suggestions.append("Add a poll to increase engagement")
        elif content_type == "story":
            base_suggestions.append("Include interactive stickers")
        elif content_type == "reel":
            base_suggestions.append("Use trending music for better reach")
        
        return base_suggestions
    
    def _handle_error(self, error: Exception, operation: str) -> Dict[str, Any]:
        """
        Handle errors and return standardized error response.
        
        Args:
            error: The exception that occurred
            operation: Description of the operation that failed
            
        Returns:
            Standardized error response
        """
        error_message = f"Error in {operation}: {str(error)}"
        self.logger.error(error_message)
        
        return {
            "success": False,
            "error": error_message,
            "content": None,
            "metadata": {
                "operation": operation,
                "error_type": type(error).__name__
            }
        }