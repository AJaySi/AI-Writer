"""Content title generator module."""

import os
import json
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from loguru import logger
from typing import Dict, Any, List, Optional
import asyncio
import sys
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/content_title_generator.log",
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

def ai_title_generator(url: str) -> Dict[str, Any]:
    """
    Generate SEO-optimized titles using AI.
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dictionary containing title suggestions and analysis
    """
    try:
        # Initialize analyzer
        analyzer = WebsiteAnalyzer()
        
        # Analyze website
        analysis = analyzer.analyze_website(url)
        if not analysis.get('success', False):
            return {
                'error': analysis.get('error', 'Unknown error in analysis'),
                'patterns': {},
                'suggestions': []
            }
        
        # Extract content and meta information
        content_info = analysis['data']['analysis']['content_info']
        seo_info = analysis['data']['analysis']['seo_info']
        
        # Generate title suggestions using AI
        prompt = f"""Based on the following website content and SEO analysis, generate 5 SEO-optimized title suggestions:
        
        Content Analysis:
        - Word Count: {content_info.get('word_count', 0)}
        - Heading Structure: {content_info.get('heading_structure', {})}
        
        SEO Analysis:
        - Meta Title: {seo_info.get('meta_tags', {}).get('title', {}).get('value', '')}
        - Meta Description: {seo_info.get('meta_tags', {}).get('description', {}).get('value', '')}
        - Keywords: {seo_info.get('meta_tags', {}).get('keywords', {}).get('value', '')}
        
        Generate 5 title suggestions that are:
        1. SEO-optimized
        2. Engaging and click-worthy
        3. Between 50-60 characters
        4. Include relevant keywords
        5. Follow best practices for title optimization
        
        Format the response as JSON with 'suggestions' and 'patterns' keys."""
        
        # Get AI suggestions
        suggestions = llm_text_gen(
            prompt=prompt,
            system_prompt="You are an SEO expert specializing in title optimization.",
            response_format="json_object"
        )
        
        if not suggestions:
            return {
                'error': 'Failed to generate title suggestions',
                'patterns': {},
                'suggestions': []
            }
        
        return {
            'patterns': suggestions.get('patterns', {}),
            'suggestions': suggestions.get('suggestions', [])
        }
        
    except Exception as e:
        error_msg = f"Error generating title suggestions: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            'error': error_msg,
            'patterns': {},
            'suggestions': []
        }

@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(min=1, max=4))
def generate_blog_titles(input_blog_keywords, input_blog_content, input_title_type, input_title_intent, input_language):
    """ Generate SEO optimized blog titles using AI """
    if input_blog_content and input_blog_keywords:
        prompt = f"""As a SEO expert, I will provide you with main 'blog keywords' and 'blog content'.
        Your task is to write 5 SEO optimized blog titles from the given blog keywords and content.

        Follow the below guidelines for generating the blog titles:
        1. Follow all best practices for SEO optimized blog titles.
        2. Optimize your response around the given keywords and content.
        3. Optimize your response for web search intent {input_title_intent}.
        4. Optimize your response for blog type {input_title_type}.
        5. The blog titles should be in {input_language} language.

        Blog keywords: '{input_blog_keywords}'
        Blog content: '{input_blog_content}'
        """
    elif input_blog_keywords and not input_blog_content:
        prompt = f"""As a SEO expert, I will provide you with the main 'keywords' of a blog.
        Your task is to write 5 SEO optimized blog titles from the given blog keywords.

        Follow the below guidelines for generating the blog titles:
        1. Follow all best practices for SEO optimized blog titles.
        2. Optimize your response around the given keywords.
        3. Optimize your response for web search intent {input_title_intent}.
        4. Optimize your response for blog type {input_title_type}.
        5. The blog titles should be in {input_language} language.

        Blog keywords: '{input_blog_keywords}'
        """
    elif input_blog_content and not input_blog_keywords:
        prompt = f"""As a SEO expert, I will provide you with the 'blog content'.
        Your task is to write 5 SEO optimized blog titles from the given blog content.

        Follow the below guidelines for generating the blog titles:
        1. Follow all best practices for SEO optimized blog titles.
        2. Optimize your response around the given content.
        3. Optimize your response for web search intent {input_title_intent}.
        4. Optimize your response for blog type {input_title_type}.
        5. The blog titles should be in {input_language} language.

        Blog content: '{input_blog_content}'
        """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
