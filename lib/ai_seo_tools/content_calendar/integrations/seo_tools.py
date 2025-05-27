"""SEO tools integration for content calendar."""

import streamlit as st
from loguru import logger
from typing import Dict, Any, List, Optional
import asyncio
import sys
import os
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/seo_tools_integration.log",
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

class SEOToolsIntegration:
    """Integration with SEO tools for content calendar."""
    
    def __init__(self):
        """Initialize the SEO tools integration."""
        self.website_analyzer = WebsiteAnalyzer()
        logger.info("SEOToolsIntegration initialized")
    
    def analyze_content(self, url: str) -> Dict[str, Any]:
        """
        Analyze content for SEO optimization.
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary containing SEO analysis results
        """
        try:
            # Analyze website
            analysis = self.website_analyzer.analyze_website(url)
            if not analysis.get('success', False):
                return {
                    'error': analysis.get('error', 'Unknown error in analysis'),
                    'seo_score': 0,
                    'recommendations': []
                }
            
            # Extract SEO information
            seo_info = analysis['data']['analysis']['seo_info']
            
            return {
                'seo_score': seo_info.get('overall_score', 0),
                'meta_tags': seo_info.get('meta_tags', {}),
                'content': seo_info.get('content', {}),
                'recommendations': seo_info.get('recommendations', [])
            }
            
        except Exception as e:
            error_msg = f"Error analyzing content: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'error': error_msg,
                'seo_score': 0,
                'recommendations': []
            }
    
    def generate_title(self, url: str) -> Dict[str, Any]:
        """
        Generate SEO-optimized title.
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary containing title suggestions
        """
        return ai_title_generator(url)
    
    def optimize_content(self, content: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Optimize content for SEO.
        
        Args:
            content: The content to optimize
            keywords: List of target keywords
            
        Returns:
            Dictionary containing optimization suggestions
        """
        try:
            # Prepare prompt for content optimization
            prompt = f"""Optimize the following content for SEO:
            
            Content: {content}
            Target Keywords: {', '.join(keywords)}
            
            Provide optimization suggestions for:
            1. Keyword usage and placement
            2. Content structure and readability
            3. Meta information
            4. Internal linking opportunities
            5. Content length and depth
            
            Format the response as JSON with 'suggestions' and 'score' keys."""
            
            # Get AI optimization suggestions
            suggestions = llm_text_gen(
                prompt=prompt,
                system_prompt="You are an SEO expert specializing in content optimization.",
                response_format="json_object"
            )
            
            if not suggestions:
                return {
                    'error': 'Failed to generate optimization suggestions',
                    'suggestions': [],
                    'score': 0
                }
            
            return {
                'suggestions': suggestions.get('suggestions', []),
                'score': suggestions.get('score', 0)
            }
            
        except Exception as e:
            error_msg = f"Error optimizing content: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'error': error_msg,
                'suggestions': [],
                'score': 0
            } 