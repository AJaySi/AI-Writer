"""
Recommendation engine for content gap analysis.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from loguru import logger
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer
from lib.ai_seo_tools.content_gap_analysis.utils.data_collector import DataCollector
from lib.ai_seo_tools.content_gap_analysis.utils.content_parser import ContentParser
from lib.ai_seo_tools.content_gap_analysis.utils.ai_processor import AIProcessor, ProgressTracker
from lib.ai_seo_tools.content_title_generator import ai_title_generator
import asyncio
import sys
import os
import json
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/recommendation_engine.log",
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

class RecommendationEngine:
    """
    Generates content recommendations based on analysis results.
    """
    
    def __init__(self):
        """Initialize the recommendation engine with required components."""
        self.ai_processor = AIProcessor()
        self.progress = ProgressTracker()
        
        # Define analysis stages
        self.stages = {
            'recommendation_generation': {
                'name': 'Recommendation Generation',
                'steps': [
                    'Initializing recommendation engine',
                    'Analyzing content gaps',
                    'Evaluating opportunities',
                    'Generating recommendations',
                    'Creating implementation plan'
                ]
            }
        }
    
    def generate_recommendations(self, website_analysis: Dict[str, Any], competitor_analysis: Optional[Dict[str, Any]], keyword_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content recommendations.
        
        Args:
            website_analysis: Website analysis results
            competitor_analysis: Optional competitor analysis results
            keyword_analysis: Keyword analysis results
            
        Returns:
            Dictionary containing recommendations
        """
        try:
            self.progress.start_stage('recommendation_generation')
            self.progress.next_step()
            
            # Analyze content gaps
            content_gaps = self._analyze_content_gaps(website_analysis, competitor_analysis, keyword_analysis)
            self.progress.next_step()
            
            # Evaluate opportunities
            opportunities = self._evaluate_opportunities(content_gaps, keyword_analysis)
            self.progress.next_step()
            
            # Generate recommendations
            recommendations = self._generate_recommendations(content_gaps, opportunities)
            self.progress.next_step()
            
            # Create implementation plan
            implementation_plan = self._create_implementation_plan(recommendations)
            self.progress.next_step()
            
            self.progress.complete_stage()
            
            return {
                'content_gaps': content_gaps,
                'opportunities': opportunities,
                'recommendations': recommendations,
                'implementation_plan': implementation_plan
            }
            
        except Exception as e:
            if self.progress.current_stage:
                self.progress.update_progress(0, f"Error in {self.progress.stages[self.progress.current_stage]['name']}: {str(e)}")
            st.error(f"Error generating recommendations: {str(e)}")
            return {
                'error': str(e),
                'content_gaps': [],
                'opportunities': [],
                'recommendations': [],
                'implementation_plan': {}
            }
    
    def _analyze_content_gaps(self, website_analysis: Dict[str, Any], competitor_analysis: Optional[Dict[str, Any]], keyword_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze content gaps."""
        try:
            content_gaps = []
            
            # Analyze website content gaps
            website_gaps = self._analyze_website_gaps(website_analysis)
            content_gaps.extend(website_gaps)
            
            # Analyze competitor gaps if available
            if competitor_analysis:
                competitor_gaps = self._analyze_competitor_gaps(competitor_analysis)
                content_gaps.extend(competitor_gaps)
            
            # Analyze keyword gaps
            keyword_gaps = self._analyze_keyword_gaps(keyword_analysis)
            content_gaps.extend(keyword_gaps)
            
            return content_gaps
        except Exception as e:
            st.error(f"Error analyzing content gaps: {str(e)}")
            return []
    
    def _analyze_website_gaps(self, website_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze website content gaps."""
        try:
            gaps = []
            
            # Check content quality
            quality_metrics = website_analysis.get('quality_metrics', {})
            if quality_metrics.get('readability_score', 0) < 70:
                gaps.append({
                    'type': 'content_quality',
                    'issue': 'Low readability score',
                    'score': quality_metrics.get('readability_score', 0),
                    'recommendation': 'Improve content readability'
                })
            
            # Check SEO elements
            seo_metrics = website_analysis.get('seo_metrics', {})
            if seo_metrics.get('seo_score', 0) < 70:
                gaps.append({
                    'type': 'seo',
                    'issue': 'Low SEO score',
                    'score': seo_metrics.get('seo_score', 0),
                    'recommendation': 'Enhance SEO optimization'
                })
            
            return gaps
        except Exception as e:
            st.error(f"Error analyzing website gaps: {str(e)}")
            return []
    
    def _analyze_competitor_gaps(self, competitor_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze competitor content gaps."""
        try:
            gaps = []
            
            # Check content gaps
            content_gaps = competitor_analysis.get('content_gaps', [])
            for gap in content_gaps:
                gaps.append({
                    'type': 'competitor',
                    'issue': f"Missing topic: {', '.join(gap.get('missing_topics', []))}",
                    'recommendation': 'Create content for missing topics'
                })
            
            return gaps
        except Exception as e:
            st.error(f"Error analyzing competitor gaps: {str(e)}")
            return []
    
    def _analyze_keyword_gaps(self, keyword_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze keyword gaps."""
        try:
            gaps = []
            
            # Check keyword opportunities
            opportunities = keyword_analysis.get('opportunities', [])
            for opportunity in opportunities:
                gaps.append({
                    'type': 'keyword',
                    'issue': f"Keyword opportunity: {opportunity.get('keyword')}",
                    'volume': opportunity.get('volume', 0),
                    'difficulty': opportunity.get('difficulty', 0),
                    'recommendation': f"Target keyword: {opportunity.get('keyword')}"
                })
            
            return gaps
        except Exception as e:
            st.error(f"Error analyzing keyword gaps: {str(e)}")
            return []
    
    def _evaluate_opportunities(self, content_gaps: List[Dict[str, Any]], keyword_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate content opportunities."""
        try:
            opportunities = []
            
            # Evaluate each gap
            for gap in content_gaps:
                # Calculate priority score
                priority_score = self._calculate_priority_score(gap, keyword_analysis)
                
                if priority_score > 50:  # Threshold for good opportunities
                    opportunities.append({
                        'type': gap.get('type'),
                        'issue': gap.get('issue'),
                        'recommendation': gap.get('recommendation'),
                        'priority_score': priority_score
                    })
            
            # Sort by priority score
            opportunities.sort(key=lambda x: x['priority_score'], reverse=True)
            
            return opportunities
        except Exception as e:
            st.error(f"Error evaluating opportunities: {str(e)}")
            return []
    
    def _calculate_priority_score(self, gap: Dict[str, Any], keyword_analysis: Dict[str, Any]) -> float:
        """Calculate priority score for a gap."""
        try:
            base_score = 0
            
            # Base score based on gap type
            if gap.get('type') == 'content_quality':
                base_score = 70
            elif gap.get('type') == 'seo':
                base_score = 80
            elif gap.get('type') == 'competitor':
                base_score = 60
            elif gap.get('type') == 'keyword':
                base_score = 50
            
            # Adjust score based on keyword data
            if gap.get('type') == 'keyword':
                keyword = gap.get('issue', '').split(': ')[-1]
                keyword_data = keyword_analysis.get('trend_analysis', {}).get('trends', {}).get(keyword, {})
                if keyword_data:
                    base_score += keyword_data.get('volume', 0) * 0.1
                    base_score -= keyword_data.get('difficulty', 0) * 0.2
            
            return min(100, max(0, base_score))
        except Exception as e:
            st.error(f"Error calculating priority score: {str(e)}")
            return 0
    
    def _generate_recommendations(self, content_gaps: List[Dict[str, Any]], opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate content recommendations."""
        try:
            recommendations = []
            
            # Generate recommendations for each opportunity
            for opportunity in opportunities:
                recommendations.append({
                    'type': opportunity.get('type'),
                    'issue': opportunity.get('issue'),
                    'recommendation': opportunity.get('recommendation'),
                    'priority': opportunity.get('priority_score', 0),
                    'implementation_steps': self._generate_implementation_steps(opportunity)
                })
            
            return recommendations
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return []
    
    def _generate_implementation_steps(self, opportunity: Dict[str, Any]) -> List[str]:
        """Generate implementation steps for a recommendation."""
        try:
            steps = []
            
            if opportunity.get('type') == 'content_quality':
                steps = [
                    'Review current content structure',
                    'Improve readability and formatting',
                    'Enhance content organization',
                    'Update content based on best practices'
                ]
            elif opportunity.get('type') == 'seo':
                steps = [
                    'Audit current SEO implementation',
                    'Optimize meta tags and descriptions',
                    'Improve content structure for SEO',
                    'Implement technical SEO improvements'
                ]
            elif opportunity.get('type') == 'competitor':
                steps = [
                    'Research competitor content',
                    'Identify unique value proposition',
                    'Create content for missing topics',
                    'Optimize content for target keywords'
                ]
            elif opportunity.get('type') == 'keyword':
                steps = [
                    'Research keyword intent',
                    'Create content strategy',
                    'Develop content for target keyword',
                    'Optimize content for search'
                ]
            
            return steps
        except Exception as e:
            st.error(f"Error generating implementation steps: {str(e)}")
            return []
    
    def _create_implementation_plan(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create implementation plan."""
        try:
            plan = {
                'phases': [],
                'timeline': {},
                'resources': {},
                'success_metrics': {}
            }
            
            # Create phases based on recommendation types
            phases = {
                'content_quality': 'Content Enhancement',
                'seo': 'SEO Optimization',
                'competitor': 'Competitive Content',
                'keyword': 'Keyword Targeting'
            }
            
            # Group recommendations by phase
            for phase_name in phases.values():
                phase_recommendations = [
                    rec for rec in recommendations
                    if phases.get(rec.get('type')) == phase_name
                ]
                
                if phase_recommendations:
                    plan['phases'].append({
                        'name': phase_name,
                        'recommendations': phase_recommendations,
                        'duration': '2-4 weeks',
                        'resources': ['Content team', 'SEO team'],
                        'success_metrics': [
                            'Content quality score',
                            'SEO performance',
                            'User engagement'
                        ]
                    })
            
            return plan
        except Exception as e:
            st.error(f"Error creating implementation plan: {str(e)}")
            return {}
    
    def _generate_content_topics(self, ai_insights: dict) -> list:
        """
        Generate content topic suggestions.
        
        Args:
            ai_insights (dict): AI-processed insights
            
        Returns:
            list: Content topic suggestions
        """
        # TODO: Implement content topic generation
        return []
    
    def _suggest_content_formats(self, ai_insights: dict) -> list:
        """
        Suggest content formats based on analysis.
        
        Args:
            ai_insights (dict): AI-processed insights
            
        Returns:
            list: Content format suggestions
        """
        # TODO: Implement content format suggestions
        return []
    
    def _calculate_priority_scores(self, ai_insights: dict) -> dict:
        """
        Calculate priority scores for recommendations.
        
        Args:
            ai_insights (dict): AI-processed insights
            
        Returns:
            dict: Priority scores for each recommendation
        """
        # TODO: Implement priority scoring
        return {}
    
    def _create_timeline(self, ai_insights: dict) -> dict:
        """
        Create implementation timeline for recommendations.
        
        Args:
            ai_insights (dict): AI-processed insights
            
        Returns:
            dict: Implementation timeline
        """
        # TODO: Implement timeline creation
        return {
            'short_term': [],
            'medium_term': [],
            'long_term': []
        }
    
    def _generate_specific_suggestions(self, recommendations: dict, analysis_results: dict) -> dict:
        """
        Generate specific content suggestions using existing tools.
        
        Args:
            recommendations (dict): General recommendations
            analysis_results (dict): Analysis results
            
        Returns:
            dict: Specific content suggestions
        """
        suggestions = {}
        
        # Generate titles for suggested topics
        for topic in recommendations['content_topics']:
            suggestions[topic] = {
                'titles': ai_title_generator(topic),
                'meta_descriptions': metadesc_generator_main(topic),
                'structured_data': ai_structured_data(topic)
            }
        
        return suggestions 