"""
Platform adapters for content calendar.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from loguru import logger
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer
from lib.ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main
from lib.ai_seo_tools.seo_structured_data import ai_structured_data
import asyncio
import sys
import os
import json

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/platform_adapters.log",
    rotation="50 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
)

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

class UnifiedPlatformAdapter:
    """Unified adapter for different social media platforms."""
    
    def __init__(self):
        """Initialize the platform adapter."""
        self.platform_handlers = {
            'instagram': self._handle_instagram,
            'linkedin': self._handle_linkedin,
            'twitter': self._handle_twitter,
            'facebook': self._handle_facebook
        }
        logger.info("UnifiedPlatformAdapter initialized")
    
    def generate_content(self, platform: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content for a specific platform.
        
        Args:
            platform: Target platform
            data: Content data
            
        Returns:
            Dictionary containing generated content
        """
        try:
            handler = self.platform_handlers.get(platform.lower())
            if not handler:
                raise ValueError(f"Unsupported platform: {platform}")
            
            return handler(data)
            
        except Exception as e:
            error_msg = f"Error generating content for {platform}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'error': error_msg,
                'content': None
            }
    
    def _handle_instagram(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Instagram content generation."""
        try:
            # Use content title generator for Instagram captions
            caption = ai_title_generator(data)
            return {
                'platform': 'instagram',
                'content': caption
            }
        except Exception as e:
            logger.error(f"Error generating Instagram content: {str(e)}")
            return {
                'platform': 'instagram',
                'error': str(e)
            }
    
    def _handle_linkedin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle LinkedIn content generation."""
        try:
            # Use meta description generator for LinkedIn posts
            post = metadesc_generator_main(data)
            return {
                'platform': 'linkedin',
                'content': post
            }
        except Exception as e:
            logger.error(f"Error generating LinkedIn content: {str(e)}")
            return {
                'platform': 'linkedin',
                'error': str(e)
            }
    
    def _handle_twitter(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Twitter content generation."""
        try:
            # Use content title generator for tweets
            tweet = ai_title_generator(data)
            return {
                'platform': 'twitter',
                'content': tweet
            }
        except Exception as e:
            logger.error(f"Error generating Twitter content: {str(e)}")
            return {
                'platform': 'twitter',
                'error': str(e)
            }
    
    def _handle_facebook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Facebook content generation."""
        try:
            # Use meta description generator for Facebook posts
            post = metadesc_generator_main(data)
            return {
                'platform': 'facebook',
                'content': post
            }
        except Exception as e:
            logger.error(f"Error generating Facebook content: {str(e)}")
            return {
                'platform': 'facebook',
                'error': str(e)
            } 