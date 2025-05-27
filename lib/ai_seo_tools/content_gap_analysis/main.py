"""
Main module for content gap analysis.
"""

from typing import Dict, Any, List, Optional
import streamlit as st
from loguru import logger
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer
from .competitor_analyzer import CompetitorAnalyzer
from .keyword_researcher import KeywordResearcher
from .recommendation_engine import RecommendationEngine
from .utils.ai_processor import AIProcessor, ProgressTracker
from .utils.storage import ContentGapAnalysisStorage
from datetime import datetime
import asyncio
import sys
import os
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from .utils.content_parser import ContentParser

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/content_gap_analysis.log",
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

class ContentGapAnalysis:
    """Main class for content gap analysis."""
    
    def __init__(self, db_session=None):
        """Initialize the content gap analysis components."""
        self.website_analyzer = WebsiteAnalyzer()
        self.competitor_analyzer = CompetitorAnalyzer()
        self.keyword_researcher = KeywordResearcher()
        self.recommendation_engine = RecommendationEngine()
        self.ai_processor = AIProcessor()
        self.progress = ProgressTracker()
        self.storage = ContentGapAnalysisStorage(db_session) if db_session else None
        
        # Define analysis phases
        self.phases = {
            'website_analysis': {
                'name': 'Website Analysis',
                'steps': [
                    'Initializing website analysis',
                    'Analyzing website content',
                    'Evaluating SEO elements',
                    'Generating website insights'
                ]
            },
            'competitor_analysis': {
                'name': 'Competitor Analysis',
                'steps': [
                    'Initializing competitor analysis',
                    'Analyzing competitor content',
                    'Comparing market position',
                    'Generating competitive insights'
                ]
            },
            'keyword_analysis': {
                'name': 'Keyword Analysis',
                'steps': [
                    'Initializing keyword research',
                    'Analyzing keyword trends',
                    'Evaluating search intent',
                    'Generating keyword insights'
                ]
            },
            'recommendation_generation': {
                'name': 'Recommendation Generation',
                'steps': [
                    'Initializing recommendation engine',
                    'Analyzing content gaps',
                    'Generating recommendations',
                    'Creating implementation plan'
                ]
            }
        }
        
        logger.info("ContentGapAnalysis initialized")
    
    def analyze(self, url: str, industry: str, competitor_urls: Optional[List[str]] = None, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Run the complete content gap analysis workflow.
        
        Args:
            url: Target website URL
            industry: Industry category
            competitor_urls: Optional list of competitor URLs
            user_id: Optional user ID for storing results
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            results = {}
            start_time = datetime.utcnow()
            
            # Phase 1: Website Analysis
            self.progress.start_stage('website_analysis')
            self.progress.next_step()
            
            website_analysis = self.website_analyzer.analyze(url)
            results['website'] = website_analysis
            
            self.progress.next_step()
            self.progress.complete_stage()
            
            # Phase 2: Competitor Analysis
            if competitor_urls:
                self.progress.start_stage('competitor_analysis')
                self.progress.next_step()
                
                competitor_analysis = self.competitor_analyzer.analyze(competitor_urls, industry)
                results['competitors'] = competitor_analysis
                
                self.progress.next_step()
                self.progress.complete_stage()
            
            # Phase 3: Keyword Analysis
            self.progress.start_stage('keyword_analysis')
            self.progress.next_step()
            
            keyword_analysis = self.keyword_researcher.analyze(industry, url)
            results['keywords'] = keyword_analysis
            
            self.progress.next_step()
            self.progress.complete_stage()
            
            # Phase 4: Recommendation Generation
            self.progress.start_stage('recommendation_generation')
            self.progress.next_step()
            
            recommendations = self.recommendation_engine.generate_recommendations(
                website_analysis,
                competitor_analysis if competitor_urls else None,
                keyword_analysis
            )
            results['recommendations'] = recommendations
            
            self.progress.next_step()
            self.progress.complete_stage()
            
            # Calculate analysis duration
            end_time = datetime.utcnow()
            results['duration'] = (end_time - start_time).total_seconds()
            
            # Store results if user_id is provided and storage is available
            if user_id and self.storage:
                analysis_id = self.storage.save_analysis(user_id, url, industry, results)
                if analysis_id:
                    results['analysis_id'] = analysis_id
            
            return results
            
        except Exception as e:
            if self.progress.current_stage:
                self.progress.update_progress(0, f"Error in {self.progress.stages[self.progress.current_stage]['name']}: {str(e)}")
            st.error(f"Error in content gap analysis: {str(e)}")
            return {
                'error': str(e),
                'website': {},
                'competitors': [],
                'keywords': {},
                'recommendations': []
            }
    
    def get_analysis(self, analysis_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve stored analysis results.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Dictionary containing analysis results if found, None otherwise
        """
        if not self.storage:
            st.error("Storage not initialized")
            return None
        return self.storage.get_analysis(analysis_id)
    
    def get_user_analyses(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all analyses for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of analysis summaries
        """
        if not self.storage:
            st.error("Storage not initialized")
            return []
        return self.storage.get_user_analyses(user_id)
    
    def update_recommendation_status(self, recommendation_id: int, status: str) -> bool:
        """
        Update the status of a recommendation.
        
        Args:
            recommendation_id: Recommendation ID
            status: New status
            
        Returns:
            True if successful, False otherwise
        """
        if not self.storage:
            st.error("Storage not initialized")
            return False
        return self.storage.update_recommendation_status(recommendation_id, status)
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """
        Delete an analysis and all related data.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            True if successful, False otherwise
        """
        if not self.storage:
            st.error("Storage not initialized")
            return False
        return self.storage.delete_analysis(analysis_id)
    
    def get_analysis_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of the analysis results.
        
        Args:
            results: Dictionary containing analysis results
            
        Returns:
            Dictionary containing summary metrics and insights
        """
        try:
            self.progress.start_stage('summary_generation')
            self.progress.next_step()
            
            summary = {
                'website_metrics': self._summarize_website_metrics(results.get('website', {})),
                'competitor_insights': self._summarize_competitor_insights(results.get('competitors', {})),
                'keyword_opportunities': self._summarize_keyword_opportunities(results.get('keywords', {})),
                'recommendation_highlights': self._summarize_recommendations(results.get('recommendations', {})),
                'ai_insights': results.get('ai_insights', {})
            }
            
            self.progress.complete_stage()
            return summary
            
        except Exception as e:
            if self.progress.current_stage:
                self.progress.update_progress(0, f"Error generating summary: {str(e)}")
            st.error(f"Error generating analysis summary: {str(e)}")
            return {
                'error': str(e),
                'website_metrics': {},
                'competitor_insights': {},
                'keyword_opportunities': {},
                'recommendation_highlights': {},
                'ai_insights': {}
            }
    
    def export_results(self, results: Dict[str, Any], format: str = 'json') -> str:
        """
        Export analysis results in the specified format.
        
        Args:
            results: Dictionary containing analysis results
            format: Export format ('json' or 'csv')
            
        Returns:
            String containing exported results
        """
        try:
            self.progress.start_stage('export')
            self.progress.next_step()
            
            if format.lower() == 'json':
                import json
                exported = json.dumps(results, indent=2)
            elif format.lower() == 'csv':
                import pandas as pd
                # Convert results to DataFrame and then to CSV
                df = pd.DataFrame(results)
                exported = df.to_csv(index=False)
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            self.progress.complete_stage()
            return exported
            
        except Exception as e:
            if self.progress.current_stage:
                self.progress.update_progress(0, f"Error exporting results: {str(e)}")
            st.error(f"Error exporting results: {str(e)}")
            return str(e)
    
    def _summarize_website_metrics(self, website_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of website metrics."""
        try:
            return {
                'content_score': website_data.get('content_score', 0),
                'seo_score': website_data.get('seo_score', 0),
                'structure_score': website_data.get('structure_score', 0),
                'key_insights': website_data.get('insights', [])[:5]  # Top 5 insights
            }
        except Exception as e:
            st.error(f"Error summarizing website metrics: {str(e)}")
            return {}
    
    def _summarize_competitor_insights(self, competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of competitor insights."""
        try:
            return {
                'market_position': competitor_data.get('market_position', {}),
                'content_gaps': competitor_data.get('content_gaps', [])[:5],  # Top 5 gaps
                'competitive_advantages': competitor_data.get('advantages', [])[:5]  # Top 5 advantages
            }
        except Exception as e:
            st.error(f"Error summarizing competitor insights: {str(e)}")
            return {}
    
    def _summarize_keyword_opportunities(self, keyword_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of keyword opportunities."""
        try:
            return {
                'top_keywords': keyword_data.get('top_keywords', [])[:10],  # Top 10 keywords
                'search_intent': keyword_data.get('search_intent', {}),
                'opportunities': keyword_data.get('opportunities', [])[:5]  # Top 5 opportunities
            }
        except Exception as e:
            st.error(f"Error summarizing keyword opportunities: {str(e)}")
            return {}
    
    def _summarize_recommendations(self, recommendation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of recommendations."""
        try:
            return {
                'priority_recommendations': recommendation_data.get('priority_recommendations', [])[:5],  # Top 5 recommendations
                'implementation_timeline': recommendation_data.get('timeline', {}),
                'expected_impact': recommendation_data.get('impact', {})
            }
        except Exception as e:
            st.error(f"Error summarizing recommendations: {str(e)}")
            return {} 