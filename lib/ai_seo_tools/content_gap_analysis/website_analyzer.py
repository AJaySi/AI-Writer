"""Website analyzer module for content gap analysis."""

import streamlit as st
from loguru import logger
from typing import Dict, Any, List, Optional
import asyncio
import sys
import os
import json
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer as BaseWebsiteAnalyzer
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/content_gap_website_analyzer.log",
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

class WebsiteAnalyzer(BaseWebsiteAnalyzer):
    """Extended website analyzer for content gap analysis."""
    
    def __init__(self):
        """Initialize the website analyzer."""
        super().__init__()
        logger.info("ContentGapWebsiteAnalyzer initialized")
    
    def analyze_content_gaps(self, url: str, competitor_urls: List[str]) -> Dict[str, Any]:
        """
        Analyze content gaps between the target website and competitors.
        
        Args:
            url: The target URL to analyze
            competitor_urls: List of competitor URLs to compare against
            
        Returns:
            Dictionary containing content gap analysis results
        """
        try:
            # Analyze target website
            target_analysis = self.analyze_website(url)
            if not target_analysis.get('success', False):
                return {
                    'error': target_analysis.get('error', 'Unknown error in target analysis'),
                    'gaps': [],
                    'recommendations': []
                }
            
            # Analyze competitor websites
            competitor_analyses = []
            for competitor_url in competitor_urls:
                analysis = self.analyze_website(competitor_url)
                if analysis.get('success', False):
                    competitor_analyses.append(analysis['data'])
            
            # Generate content gap analysis using AI
            prompt = f"""Analyze content gaps between the target website and competitors:
            
            Target Website:
            {json.dumps(target_analysis['data'], indent=2)}
            
            Competitor Websites:
            {json.dumps(competitor_analyses, indent=2)}
            
            Identify:
            1. Missing content topics
            2. Content depth differences
            3. Keyword gaps
            4. Content structure improvements
            5. Content quality recommendations
            
            Format the response as JSON with 'gaps' and 'recommendations' keys."""
            
            # Get AI analysis
            analysis = llm_text_gen(
                prompt=prompt,
                system_prompt="You are an SEO expert specializing in content gap analysis.",
                response_format="json_object"
            )
            
            if not analysis:
                return {
                    'error': 'Failed to generate content gap analysis',
                    'gaps': [],
                    'recommendations': []
                }
            
            return {
                'gaps': analysis.get('gaps', []),
                'recommendations': analysis.get('recommendations', [])
            }
            
        except Exception as e:
            error_msg = f"Error analyzing content gaps: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'error': error_msg,
                'gaps': [],
                'recommendations': []
            }

    def analyze(self, url: str) -> Dict[str, Any]:
        """
        Analyze a website for content gaps and SEO opportunities.
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Initialize progress tracking
            progress = {
                'status': 'in_progress',
                'current_stage': 'content_analysis',
                'current_step': 'Initializing analysis',
                'progress': 0,
                'details': 'Starting website analysis...'
            }
            self.progress.update(progress)
            
            # Get base website analysis
            logger.info("Starting base website analysis")
            website_analysis = self.analyze_website(url)
            
            if not website_analysis.get('success', False):
                error_msg = website_analysis.get('error', 'Unknown error in website analysis')
                logger.error(f"Error in website analysis: {error_msg}")
                progress['status'] = 'error'
                progress['details'] = error_msg
                self.progress.update(progress)
                return {
                    'error': error_msg,
                    'error_details': website_analysis.get('error_details', {}),
                    'progress': progress
                }
            
            # Extract SEO metrics from the analysis
            seo_metrics = self._extract_seo_metrics(website_analysis['data'])
            
            # Extract performance metrics
            performance_metrics = self._extract_performance_metrics(website_analysis['data'])
            
            # Update progress
            progress['status'] = 'completed'
            progress['progress'] = 100
            progress['details'] = 'Analysis completed successfully'
            self.progress.update(progress)
            
            return {
                'success': True,
                'data': {
                    'seo_metrics': seo_metrics,
                    'performance_metrics': performance_metrics,
                    'website_analysis': website_analysis['data']
                },
                'progress': progress
            }
            
        except Exception as e:
            error_msg = f"Error in content gap analysis: {str(e)}"
            logger.error(error_msg, exc_info=True)
            progress['status'] = 'error'
            progress['details'] = error_msg
            self.progress.update(progress)
            return {
                'error': error_msg,
                'error_details': {
                    'type': type(e).__name__,
                    'traceback': str(e.__traceback__)
                },
                'progress': progress
            }
    
    def _extract_seo_metrics(self, website_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract SEO-related metrics from website analysis."""
        try:
            seo_info = website_analysis.get('analysis', {}).get('seo_info', {})
            return {
                'overall_score': seo_info.get('overall_score', 0),
                'meta_tags': {
                    'title': seo_info.get('meta_tags', {}).get('title', {}),
                    'description': seo_info.get('meta_tags', {}).get('description', {}),
                    'keywords': seo_info.get('meta_tags', {}).get('keywords', {})
                },
                'content': {
                    'word_count': seo_info.get('content', {}).get('word_count', 0),
                    'readability_score': seo_info.get('content', {}).get('readability_score', 0),
                    'content_quality_score': seo_info.get('content', {}).get('content_quality_score', 0)
                }
            }
        except Exception as e:
            logger.error(f"Error extracting SEO metrics: {str(e)}", exc_info=True)
            return {}
    
    def _extract_performance_metrics(self, website_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract performance metrics from website analysis."""
        try:
            performance_info = website_analysis.get('analysis', {}).get('performance', {})
            return {
                'load_time': performance_info.get('load_time', 0),
                'page_size': performance_info.get('page_size', 0),
                'resource_count': performance_info.get('resource_count', 0),
                'performance_score': performance_info.get('performance_score', 0)
            }
        except Exception as e:
            logger.error(f"Error extracting performance metrics: {str(e)}", exc_info=True)
            return {}
    
    def _extract_content_metrics(self, website_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content-related metrics from website analysis."""
        try:
            content_info = website_analysis['analysis']['content_info']
            return {
                'word_count': content_info.get('word_count', 0),
                'heading_count': content_info.get('heading_count', 0),
                'image_count': content_info.get('image_count', 0),
                'link_count': content_info.get('link_count', 0),
                'has_meta_description': content_info.get('has_meta_description', False),
                'has_robots_txt': content_info.get('has_robots_txt', False),
                'has_sitemap': content_info.get('has_sitemap', False)
            }
        except Exception as e:
            logger.error(f"Error extracting content metrics: {str(e)}", exc_info=True)
            return {}
    
    def _extract_technical_info(self, website_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract technical information from website analysis."""
        try:
            basic_info = website_analysis.get('analysis', {}).get('basic_info', {})
            return {
                'title': basic_info.get('title', ''),
                'meta_description': basic_info.get('meta_description', ''),
                'headers': basic_info.get('headers', {}),
                'robots_txt': basic_info.get('robots_txt', ''),
                'sitemap': basic_info.get('sitemap', ''),
                'server_info': basic_info.get('server_info', {}),
                'security_info': basic_info.get('security_info', {})
            }
        except Exception as e:
            logger.error(f"Error extracting technical info: {str(e)}", exc_info=True)
            return {}
    
    def _generate_insights(self, content_metrics: Dict[str, Any], seo_metrics: Dict[str, Any]) -> List[str]:
        """Generate content insights based on analysis results."""
        try:
            insights = []
            
            # Content insights
            if content_metrics['word_count'] < 300:
                insights.append("Content length is below recommended minimum (300 words)")
            elif content_metrics['word_count'] > 2000:
                insights.append("Content length is above recommended maximum (2000 words)")
                
            if content_metrics['heading_count'] < 2:
                insights.append("Content structure could be improved with more headings")
                
            if content_metrics['image_count'] == 0:
                insights.append("Consider adding images to improve content engagement")
                
            # SEO insights
            if seo_metrics.get('overall_score', 0) < 60:
                insights.append("SEO optimization needs significant improvement")
            elif seo_metrics.get('overall_score', 0) < 80:
                insights.append("SEO optimization has room for improvement")
                
            if not content_metrics['has_meta_description']:
                insights.append("Missing meta description - important for SEO")
                
            if not content_metrics['has_robots_txt']:
                insights.append("Missing robots.txt - important for search engine crawling")
                
            if not content_metrics['has_sitemap']:
                insights.append("Missing sitemap.xml - important for search engine indexing")
                
            return insights
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}", exc_info=True)
            return [] 