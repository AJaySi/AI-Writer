"""
Gap analyzer integration for content calendar.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from loguru import logger
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer
from lib.ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
import asyncio
import sys
import os
import json
from datetime import datetime

# Configure logger for content calendar debugging
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> | <yellow>{function}</yellow> | {message}",
    filter=lambda record: "content_calendar" in record["name"].lower()
)

class GapAnalyzerIntegration:
    """Integrates content gap analysis with content calendar."""
    
    def __init__(self):
        """Initialize the gap analyzer integration."""
        self.gap_analyzer = ContentGapAnalysis()
        logger.debug("GapAnalyzerIntegration initialized for content calendar")
    
    def analyze_gaps(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content gaps.
        
        Args:
            data: Dictionary containing content data
            
        Returns:
            Dictionary containing gap analysis results
        """
        try:
            logger.debug(f"Starting gap analysis with data: {json.dumps(data, indent=2)}")
            # Run gap analysis
            results = self.gap_analyzer.analyze(data)
            logger.debug(f"Gap analysis completed with results: {json.dumps(results, indent=2)}")
            return results
            
        except Exception as e:
            error_msg = f"Error analyzing content gaps: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'error': error_msg,
                'gaps': [],
                'recommendations': []
            }
    
    def get_topic_suggestions(
        self,
        gap_analysis: Dict[str, Any],
        platform: str,
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get topic suggestions for a specific platform based on gap analysis.
        
        Args:
            gap_analysis: Results from gap analysis
            platform: Target platform for content
            count: Number of suggestions to generate
            
        Returns:
            List of topic suggestions
        """
        try:
            logger.debug(f"Generating topic suggestions for platform: {platform}, count: {count}")
            suggestions = []
            
            for gap in gap_analysis.get('processed_gaps', []):
                # Generate platform-specific topics
                platform_topics = self.ai_processor.generate_platform_topics(
                    gap=gap,
                    platform=platform,
                    count=count
                )
                logger.debug(f"Generated topics for gap: {json.dumps(platform_topics, indent=2)}")
                suggestions.extend(platform_topics)
            
            logger.debug(f"Total suggestions generated: {len(suggestions)}")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating topic suggestions: {str(e)}")
            return []
    
    def analyze_topic_relevance(
        self,
        topic: Dict[str, Any],
        gap_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze how well a topic addresses content gaps.
        
        Args:
            topic: Topic to analyze
            gap_analysis: Results from gap analysis
            
        Returns:
            Dictionary containing relevance analysis
        """
        try:
            logger.debug(f"Analyzing topic relevance: {json.dumps(topic, indent=2)}")
            relevance = self.ai_processor.analyze_topic_relevance(
                topic=topic,
                gaps=gap_analysis.get('gaps', [])
            )
            
            logger.debug(f"Topic relevance analysis completed: {json.dumps(relevance, indent=2)}")
            return relevance
            
        except Exception as e:
            logger.error(f"Error analyzing topic relevance: {str(e)}")
            return {
                'error': str(e),
                'score': 0
            } 