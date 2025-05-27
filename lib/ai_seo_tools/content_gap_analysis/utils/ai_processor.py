"""
AI processor module for content gap analysis.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from loguru import logger
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer
from lib.ai_seo_tools.content_gap_analysis.utils.data_collector import DataCollector
from lib.ai_seo_tools.content_gap_analysis.utils.content_parser import ContentParser
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
import asyncio
import sys
import os
import json
import re
from collections import Counter

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/ai_processor.log",
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

class ProgressTracker:
    """Tracks progress of AI processing tasks."""
    
    def __init__(self):
        """Initialize the progress tracker."""
        self._progress = {
            'status': 'initializing',
            'current_step': 'Starting',
            'progress': 0,
            'details': 'Initializing...'
        }
    
    def update(self, progress_data: Dict[str, Any]) -> None:
        """
        Update progress information.
        
        Args:
            progress_data: Dictionary containing progress information
                - status: Current status ('initializing', 'in_progress', 'completed', 'error')
                - current_step: Description of current step
                - progress: Progress percentage (0-100)
                - details: Additional details about current step
        """
        if not isinstance(progress_data, dict):
            raise ValueError("Progress data must be a dictionary")
            
        required_fields = ['status', 'current_step', 'progress', 'details']
        for field in required_fields:
            if field not in progress_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate progress value
        progress = progress_data.get('progress', 0)
        if not isinstance(progress, (int, float)) or progress < 0 or progress > 100:
            raise ValueError("Progress must be a number between 0 and 100")
        
        # Validate status
        valid_statuses = ['initializing', 'in_progress', 'completed', 'error']
        status = progress_data.get('status')
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        # Update progress
        self._progress.update(progress_data)
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Get current progress information.
        
        Returns:
            Dictionary containing current progress information
        """
        return self._progress.copy()
    
    def reset(self) -> None:
        """Reset progress to initial state."""
        self._progress = {
            'status': 'initializing',
            'current_step': 'Starting',
            'progress': 0,
            'details': 'Initializing...'
        }

class AIProcessor:
    """Processes and enhances content analysis using AI techniques."""
    
    def __init__(self):
        """Initialize the AI processor."""
        self.cache = {}
        self.progress = ProgressTracker()
        self.system_prompts = {
            'content_analysis': """You are an expert SEO and content analyst. Your task is to analyze content and provide detailed insights.
                Focus on:
                1. Content quality and structure
                2. Topic coverage and depth
                3. SEO optimization
                4. User engagement potential
                5. Content gaps and opportunities
                
                Provide your analysis in a structured format with specific, actionable recommendations.
                Use clear metrics and examples to support your insights.""",
            
            'competitor_analysis': """You are an expert competitive analyst. Your task is to analyze competitor data and provide strategic insights.
                Focus on:
                1. Content strategy differences
                2. Competitive advantages
                3. Content gaps and opportunities
                4. Market positioning
                5. Strategic recommendations
                
                Provide your analysis in a structured format with specific, actionable recommendations.
                Include competitive benchmarks and improvement opportunities.""",
            
            'keyword_analysis': """You are an expert keyword analyst. Your task is to analyze keyword data and provide strategic insights.
                Focus on:
                1. Keyword opportunities
                2. Search intent patterns
                3. Content format suggestions
                4. Topic clusters
                5. Strategic recommendations
                
                Provide your analysis in a structured format with specific, actionable recommendations.
                Include keyword metrics and content strategy suggestions.""",
            
            'recommendation_analysis': """You are an expert content strategist. Your task is to analyze recommendations and provide implementation insights.
                Focus on:
                1. Implementation feasibility
                2. Expected impact
                3. Resource requirements
                4. Timeline suggestions
                5. Risk assessment
                
                Provide your analysis in a structured format with specific, actionable guidance.
                Include implementation steps and success metrics."""
        }
    
    def analyze_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze website content using AI techniques.
        
        Args:
            data: Dictionary containing website content and metadata
            
        Returns:
            Dictionary containing AI-enhanced analysis
        """
        try:
            self.progress.update({'status': 'in_progress', 'current_step': 'Analyzing content structure'})
            
            url = data.get('url', '')
            industry = data.get('industry', '')
            content = data.get('content', {})
            
            # Generate AI prompt for content analysis
            prompt = f"""
            Analyze the following website content and provide detailed insights:

            URL: {url}
            Industry: {industry}
            Content: {content}

            Please provide a comprehensive analysis covering:
            1. Content Quality Assessment
               - Structure and organization
               - Readability and engagement
               - Technical elements
               - SEO optimization

            2. Topic Analysis
               - Coverage and depth
               - Relevance to industry
               - Content gaps
               - Opportunities

            3. Performance Metrics
               - User engagement potential
               - SEO effectiveness
               - Content value

            4. Strategic Recommendations
               - Content improvements
               - SEO enhancements
               - Engagement strategies
               - Implementation steps

            Format your response in a clear, structured manner with specific examples and actionable recommendations.
            """
            
            self.progress.update({'current_step': 'Analyzing content structure'})
            
            # Get AI analysis with custom system prompt
            ai_analysis = llm_text_gen(prompt, system_prompt=self.system_prompts['content_analysis'])
            
            self.progress.update({'current_step': 'Evaluating content quality'})
            
            # Extract content metrics
            content_metrics = self._analyze_content_metrics(content)
            
            self.progress.update({'current_step': 'Assessing SEO elements'})
            
            # Analyze content evolution
            evolution_analysis = self._analyze_content_evolution(content)
            
            self.progress.update({'current_step': 'Analyzing topic trends'})
            
            # Analyze topic trends
            topic_trends = self._analyze_topic_trends(content, industry)
            
            self.progress.update({'current_step': 'Analyzing performance trends'})
            
            # Analyze performance trends
            performance_trends = self._analyze_performance_trends(content)
            
            self.progress.update({'current_step': 'Generating content insights'})
            
            # Generate AI insights
            insights = self._generate_content_insights(content_metrics, evolution_analysis, topic_trends, performance_trends)
            
            self.progress.update({'current_step': 'Creating visual representation'})
            
            # Generate visual representation
            visualization = self._generate_content_visualization(content, insights)
            
            self.progress.update({'status': 'completed', 'current_step': 'Completed content analysis'})
            
            return {
                'content_metrics': content_metrics,
                'content_evolution': evolution_analysis,
                'topic_trends': topic_trends,
                'performance_trends': performance_trends,
                'ai_insights': insights,
                'ai_analysis': ai_analysis,
                'visualization': visualization
            }
            
        except Exception as e:
            if self.progress.get_progress().get('status') == 'in_progress':
                self.progress.update({'status': 'error', 'current_step': 'Error in content analysis', 'details': str(e)})
            st.error(f"Error in AI content analysis: {str(e)}")
            return {
                'error': str(e),
                'content_metrics': {},
                'content_evolution': {},
                'topic_trends': {},
                'performance_trends': {},
                'ai_insights': {},
                'ai_analysis': {},
                'visualization': None
            }
    
    def analyze_competitors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze competitor content using AI techniques.
        
        Args:
            data: Dictionary containing competitor data and analysis
            
        Returns:
            Dictionary containing AI-enhanced competitor analysis
        """
        try:
            self.progress.update({'status': 'in_progress', 'current_step': 'Analyzing competitor content'})
            
            competitors = data.get('competitors', [])
            analysis = data.get('analysis', {})
            
            # Generate AI prompt for competitor analysis
            prompt = f"""
            Analyze the following competitor data and provide strategic insights:

            Competitors: {competitors}
            Analysis: {analysis}

            Please provide a comprehensive analysis covering:
            1. Content Strategy Analysis
               - Content types and formats
               - Topic coverage
               - Content quality
               - Engagement strategies

            2. Competitive Position
               - Market positioning
               - Unique advantages
               - Content gaps
               - Opportunities

            3. Performance Metrics
               - Content effectiveness
               - User engagement
               - SEO performance
               - Market share

            4. Strategic Recommendations
               - Content improvements
               - Competitive advantages
               - Market positioning
               - Implementation steps

            Format your response in a clear, structured manner with specific examples and actionable recommendations.
            """
            
            self.progress.update({'current_step': 'Evaluating market position'})
            
            # Get AI analysis with custom system prompt
            ai_analysis = llm_text_gen(prompt, system_prompt=self.system_prompts['competitor_analysis'])
            
            self.progress.update({'current_step': 'Identifying content gaps'})
            
            # Analyze competitor trends
            trend_analysis = self._analyze_competitor_trends(competitors, analysis)
            
            self.progress.update({'current_step': 'Generating competitive insights'})
            
            # Generate competitive insights
            insights = self._generate_competitive_insights(competitors, analysis, trend_analysis)
            
            self.progress.update({'current_step': 'Creating visual representation'})
            
            # Generate visual representation
            visualization = self._generate_competitor_visualization(competitors, insights)
            
            self.progress.update({'status': 'completed', 'current_step': 'Completed competitor analysis'})
            
            return {
                'competitor_trends': trend_analysis,
                'competitive_insights': insights,
                'ai_analysis': ai_analysis,
                'visualization': visualization
            }
            
        except Exception as e:
            if self.progress.get_progress().get('status') == 'in_progress':
                self.progress.update({'status': 'error', 'current_step': 'Error in competitor analysis', 'details': str(e)})
            st.error(f"Error in AI competitor analysis: {str(e)}")
            return {
                'error': str(e),
                'competitor_trends': {},
                'competitive_insights': {},
                'ai_analysis': {},
                'visualization': None
            }
    
    def analyze_keywords(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze keywords using AI techniques.
        
        Args:
            data: Dictionary containing keyword data
            
        Returns:
            Dictionary containing AI-enhanced keyword analysis
        """
        try:
            self.progress.update({'status': 'in_progress', 'current_step': 'Analyzing keyword trends'})
            
            industry = data.get('industry', '')
            keywords = data.get('keywords', {})
            
            # Generate AI prompt for keyword analysis
            prompt = f"""
            Analyze the following keyword data and provide strategic insights:

            Industry: {industry}
            Keywords: {keywords}

            Please provide a comprehensive analysis covering:
            1. Keyword Opportunity Analysis
               - Search volume trends
               - Competition levels
               - Difficulty scores
               - Potential impact

            2. Search Intent Analysis
               - User intent patterns
               - Content type alignment
               - Topic clusters
               - Content gaps

            3. Content Strategy
               - Format recommendations
               - Topic suggestions
               - Implementation approach
               - Success metrics

            4. Strategic Recommendations
               - Keyword targeting
               - Content development
               - Implementation steps
               - Performance tracking

            Format your response in a clear, structured manner with specific examples and actionable recommendations.
            """
            
            self.progress.update({'current_step': 'Evaluating search intent'})
            
            # Get AI analysis with custom system prompt
            ai_analysis = llm_text_gen(prompt, system_prompt=self.system_prompts['keyword_analysis'])
            
            self.progress.update({'current_step': 'Identifying opportunities'})
            
            # Analyze keyword trends
            trend_analysis = self._analyze_keyword_trends(keywords)
            
            self.progress.update({'current_step': 'Analyzing search intent'})
            
            # Analyze search intent
            intent_analysis = self._analyze_search_intent(keywords)
            
            self.progress.update({'current_step': 'Generating keyword insights'})
            
            # Generate keyword insights
            insights = self._generate_keyword_insights(keywords, trend_analysis, intent_analysis)
            
            self.progress.update({'current_step': 'Creating visual representation'})
            
            # Generate visual representation
            visualization = self._generate_keyword_visualization(keywords, insights)
            
            self.progress.update({'status': 'completed', 'current_step': 'Completed keyword analysis'})
            
            return {
                'keyword_trends': trend_analysis,
                'search_intent': intent_analysis,
                'keyword_insights': insights,
                'ai_analysis': ai_analysis,
                'visualization': visualization
            }
            
        except Exception as e:
            if self.progress.get_progress().get('status') == 'in_progress':
                self.progress.update({'status': 'error', 'current_step': 'Error in keyword analysis', 'details': str(e)})
            st.error(f"Error in AI keyword analysis: {str(e)}")
            return {
                'error': str(e),
                'keyword_trends': {},
                'search_intent': {},
                'keyword_insights': {},
                'ai_analysis': {},
                'visualization': None
            }
    
    def analyze_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze recommendations using AI techniques.
        
        Args:
            data: Dictionary containing recommendations and analysis
            
        Returns:
            Dictionary containing AI-enhanced recommendation analysis
        """
        try:
            self.progress.update({'status': 'in_progress', 'current_step': 'Analyzing recommendation impact'})
            
            recommendations = data.get('recommendations', {})
            analysis = data.get('analysis', {})
            
            # Generate AI prompt for recommendation analysis
            prompt = f"""
            Analyze the following recommendations and provide implementation insights:

            Recommendations: {recommendations}
            Analysis: {analysis}

            Please provide a comprehensive analysis covering:
            1. Implementation Feasibility
               - Resource requirements
               - Technical complexity
               - Timeline estimates
               - Risk assessment

            2. Expected Impact
               - SEO improvements
               - User engagement
               - Content quality
               - Business value

            3. Implementation Strategy
               - Priority order
               - Dependencies
               - Success metrics
               - Monitoring plan

            4. Risk Management
               - Potential challenges
               - Mitigation strategies
               - Contingency plans
               - Success criteria

            Format your response in a clear, structured manner with specific examples and actionable guidance.
            """
            
            self.progress.update({'current_step': 'Assessing expected impact'})
            
            # Get AI analysis with custom system prompt
            ai_analysis = llm_text_gen(prompt, system_prompt=self.system_prompts['recommendation_analysis'])
            
            self.progress.update({'current_step': 'Analyzing resource requirements'})
            
            # Analyze recommendation impact
            impact_analysis = self._analyze_recommendation_impact(recommendations, analysis)
            
            self.progress.update({'current_step': 'Generating strategic insights'})
            
            # Generate strategic insights
            insights = self._generate_strategic_insights(recommendations, analysis, impact_analysis)
            
            self.progress.update({'current_step': 'Creating visual representation'})
            
            # Generate visual representation
            visualization = self._generate_recommendation_visualization(recommendations, insights)
            
            self.progress.update({'status': 'completed', 'current_step': 'Completed recommendation analysis'})
            
            return {
                'impact_analysis': impact_analysis,
                'strategic_insights': insights,
                'ai_analysis': ai_analysis,
                'visualization': visualization
            }
            
        except Exception as e:
            if self.progress.get_progress().get('status') == 'in_progress':
                self.progress.update({'status': 'error', 'current_step': 'Error in recommendation analysis', 'details': str(e)})
            st.error(f"Error in AI recommendation analysis: {str(e)}")
            return {
                'error': str(e),
                'impact_analysis': {},
                'strategic_insights': {},
                'ai_analysis': {},
                'visualization': None
            }
    
    def _analyze_content_metrics(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content metrics using AI."""
        prompt = f"""
        Analyze the following content and provide detailed metrics:

        Content: {content}

        Please provide:
        1. Content Quality Metrics
           - Structure score
           - Readability score
           - Engagement score
           - SEO score

        2. Technical Metrics
           - Content length
           - Internal linking
           - Meta tags
           - Technical elements

        3. Performance Indicators
           - User engagement potential
           - SEO effectiveness
           - Content value
           - Improvement areas

        Format your response in a clear, structured manner with specific metrics and scores.
        """
        
        try:
            metrics = llm_text_gen(prompt, system_prompt=self.system_prompts['content_analysis'])
            return metrics
        except Exception as e:
            st.error(f"Error analyzing content metrics: {str(e)}")
            return {
                'quality_score': 0,
                'readability_score': 0,
                'engagement_score': 0,
                'seo_score': 0
            }
    
    def _analyze_content_evolution(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content evolution using AI."""
        prompt = f"""
        Analyze the following content evolution:

        Content: {content}

        Please provide:
        1. Timeline Analysis
           - Content development stages
           - Key milestones
           - Evolution patterns
           - Growth indicators

        2. Performance Metrics
           - Depth scores over time
           - Coverage scores over time
           - Engagement trends
           - SEO performance

        3. Evolution Insights
           - Content improvements
           - Strategy changes
           - Success factors
           - Future opportunities

        Format your response in a clear, structured manner with specific metrics and insights.
        """
        
        try:
            evolution = llm_text_gen(prompt, system_prompt=self.system_prompts['content_analysis'])
            return evolution
        except Exception as e:
            st.error(f"Error analyzing content evolution: {str(e)}")
            return {
                'timeline': [],
                'depth_scores': [],
                'coverage_scores': []
            }
    
    def _analyze_topic_trends(self, content: Dict[str, Any], industry: str) -> Dict[str, Any]:
        """Analyze topic trends using AI."""
        prompt = f"""
        Analyze topic trends for the following content and industry:

        Content: {content}
        Industry: {industry}

        Please provide:
        1. Topic Analysis
           - Current topic coverage
           - Emerging topics
           - Declining topics
           - Industry alignment

        2. Trend Matrix
           - Topic popularity
           - Growth potential
           - Competition level
           - Implementation priority

        3. Strategic Insights
           - Content opportunities
           - Topic gaps
           - Industry trends
           - Action items

        Format your response in a clear, structured manner with specific metrics and recommendations.
        """
        
        try:
            trends = llm_text_gen(prompt, system_prompt=self.system_prompts['content_analysis'])
            return trends
        except Exception as e:
            st.error(f"Error analyzing topic trends: {str(e)}")
            return {
                'trend_matrix': []
            }
    
    def _analyze_performance_trends(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance trends using AI."""
        prompt = f"""
        Analyze performance trends for the following content:

        Content: {content}

        Please provide:
        1. Engagement Metrics
           - User interaction
           - Time on page
           - Bounce rate
           - Conversion rate

        2. Content Performance
           - Traffic trends
           - Engagement patterns
           - Conversion metrics
           - ROI indicators

        3. Improvement Areas
           - Performance gaps
           - Optimization opportunities
           - Success factors
           - Action items

        Format your response in a clear, structured manner with specific metrics and recommendations.
        """
        
        try:
            trends = llm_text_gen(prompt, system_prompt=self.system_prompts['content_analysis'])
            return trends
        except Exception as e:
            st.error(f"Error analyzing performance trends: {str(e)}")
            return {
                'engagement': {},
                'conversion': {}
            }
    
    def _analyze_competitor_trends(self, competitors: List[str], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor trends using AI."""
        prompt = f"""
        Analyze competitor trends:

        Competitors: {competitors}
        Analysis: {analysis}

        Please provide:
        1. Market Position
           - Market share
           - Growth trends
           - Competitive advantages
           - Market dynamics

        2. Strategy Analysis
           - Content approach
           - Marketing tactics
           - User engagement
           - Success factors

        3. Competitive Insights
           - Market opportunities
           - Threat assessment
           - Strategic gaps
           - Action items

        Format your response in a clear, structured manner with specific metrics and recommendations.
        """
        
        try:
            trends = llm_text_gen(prompt, system_prompt=self.system_prompts['competitor_analysis'])
            return trends
        except Exception as e:
            st.error(f"Error analyzing competitor trends: {str(e)}")
            return {}
    
    def _analyze_keyword_trends(self, keywords: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze keyword trends using AI."""
        prompt = f"""
        Analyze keyword trends:

        Keywords: {keywords}

        Please provide:
        1. Performance Metrics
           - Search volume
           - Competition level
           - Difficulty score
           - Trend direction

        2. Opportunity Analysis
           - Growth potential
           - Competition gaps
           - Content needs
           - Implementation priority

        3. Strategic Insights
           - Keyword opportunities
           - Content strategy
           - Implementation steps
           - Success metrics

        Format your response in a clear, structured manner with specific metrics and recommendations.
        """
        
        try:
            trends = llm_text_gen(prompt, system_prompt=self.system_prompts['keyword_analysis'])
            return trends
        except Exception as e:
            st.error(f"Error analyzing keyword trends: {str(e)}")
            return {}
    
    def _analyze_search_intent(self, keywords: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze search intent using AI."""
        prompt = f"""
        Analyze search intent:

        Keywords: {keywords}

        Please provide:
        1. Intent Analysis
           - User intent types
           - Content needs
           - User journey
           - Conversion potential

        2. Content Strategy
           - Format recommendations
           - Topic suggestions
           - Implementation approach
           - Success metrics

        3. Strategic Insights
           - Content opportunities
           - User engagement
           - Conversion optimization
           - Action items

        Format your response in a clear, structured manner with specific metrics and recommendations.
        """
        
        try:
            intent = llm_text_gen(prompt, system_prompt=self.system_prompts['keyword_analysis'])
            return intent
        except Exception as e:
            st.error(f"Error analyzing search intent: {str(e)}")
            return {
                'summary': []
            }
    
    def _analyze_recommendation_impact(self, recommendations: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze recommendation impact using AI."""
        prompt = f"""
        Analyze recommendation impact:

        Recommendations: {recommendations}
        Analysis: {analysis}

        Please provide:
        1. Impact Assessment
           - SEO improvements
           - User engagement
           - Content quality
           - Business value

        2. Implementation Analysis
           - Resource requirements
           - Technical complexity
           - Timeline estimates
           - Risk assessment

        3. Strategic Insights
           - Priority order
           - Dependencies
           - Success metrics
           - Monitoring plan

        Format your response in a clear, structured manner with specific metrics and recommendations.
        """
        
        try:
            impact = llm_text_gen(prompt, system_prompt=self.system_prompts['recommendation_analysis'])
            return impact
        except Exception as e:
            st.error(f"Error analyzing recommendation impact: {str(e)}")
            return {
                'seo': {},
                'engagement': {}
            }
    
    def _generate_content_insights(self, metrics: Dict[str, Any], evolution: Dict[str, Any], trends: Dict[str, Any], performance: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content insights using AI."""
        prompt = f"""
        Generate content insights:

        Metrics: {metrics}
        Evolution: {evolution}
        Trends: {trends}
        Performance: {performance}

        Please provide:
        1. Quality Insights
           - Content strengths
           - Improvement areas
           - Best practices
           - Action items

        2. Engagement Insights
           - User behavior
           - Interaction patterns
           - Conversion factors
           - Optimization opportunities

        3. SEO Insights
           - Technical optimization
           - Content optimization
           - Performance factors
           - Implementation steps

        Format your response in a clear, structured manner with specific insights and recommendations.
        """
        
        try:
            insights = llm_text_gen(prompt, system_prompt=self.system_prompts['content_analysis'])
            return insights
        except Exception as e:
            st.error(f"Error generating content insights: {str(e)}")
            return {
                'quality': [],
                'engagement': [],
                'seo': []
            }
    
    def _generate_competitive_insights(self, competitors: List[str], analysis: Dict[str, Any], trends: Dict[str, Any]) -> Dict[str, Any]:
        """Generate competitive insights using AI."""
        prompt = f"""
        Generate competitive insights:

        Competitors: {competitors}
        Analysis: {analysis}
        Trends: {trends}

        Please provide:
        1. Content Strategy
           - Market position
           - Competitive advantages
           - Content gaps
           - Opportunities

        2. Market Insights
           - Industry trends
           - User preferences
           - Market dynamics
           - Growth potential

        3. Strategic Recommendations
           - Content improvements
           - Market positioning
           - Implementation steps
           - Success metrics

        Format your response in a clear, structured manner with specific insights and recommendations.
        """
        
        try:
            insights = llm_text_gen(prompt, system_prompt=self.system_prompts['competitor_analysis'])
            return insights
        except Exception as e:
            st.error(f"Error generating competitive insights: {str(e)}")
            return {
                'content': [],
                'strategy': []
            }
    
    def _generate_keyword_insights(self, keywords: Dict[str, Any], trends: Dict[str, Any], intent: Dict[str, Any]) -> Dict[str, Any]:
        """Generate keyword insights using AI."""
        prompt = f"""
        Generate keyword insights:

        Keywords: {keywords}
        Trends: {trends}
        Intent: {intent}

        Please provide:
        1. Opportunity Analysis
           - Keyword potential
           - Content needs
           - Implementation priority
           - Success metrics

        2. Content Strategy
           - Topic clusters
           - Format recommendations
           - Implementation approach
           - Performance tracking

        3. Strategic Recommendations
           - Keyword targeting
           - Content development
           - Implementation steps
           - Success metrics

        Format your response in a clear, structured manner with specific insights and recommendations.
        """
        
        try:
            insights = llm_text_gen(prompt, system_prompt=self.system_prompts['keyword_analysis'])
            return insights
        except Exception as e:
            st.error(f"Error generating keyword insights: {str(e)}")
            return {
                'opportunities': [],
                'strategy': []
            }
    
    def _generate_strategic_insights(self, recommendations: Dict[str, Any], analysis: Dict[str, Any], impact: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic insights using AI."""
        prompt = f"""
        Generate strategic insights:

        Recommendations: {recommendations}
        Analysis: {analysis}
        Impact: {impact}

        Please provide:
        1. Content Strategy
           - Implementation approach
           - Resource requirements
           - Timeline estimates
           - Success metrics

        2. Technical Strategy
           - Technical requirements
           - Implementation steps
           - Risk assessment
           - Monitoring plan

        3. Strategic Recommendations
           - Priority order
           - Dependencies
           - Success criteria
           - Action items

        Format your response in a clear, structured manner with specific insights and recommendations.
        """
        
        try:
            insights = llm_text_gen(prompt, system_prompt=self.system_prompts['recommendation_analysis'])
            return insights
        except Exception as e:
            st.error(f"Error generating strategic insights: {str(e)}")
            return {
                'content': [],
                'technical': []
            }
    
    def _generate_content_visualization(self, content: Dict[str, Any], insights: Dict[str, Any]) -> str:
        """Generate visual representation of content analysis."""
        try:
            # Create a prompt for image generation
            prompt = f"""
            Create a visual representation of content analysis with the following insights:
            
            Content Quality: {insights.get('quality', [])}
            Engagement Metrics: {insights.get('engagement', [])}
            SEO Performance: {insights.get('seo', [])}
            
            The image should be professional, data-driven, and easy to understand.
            """
            
            # Generate image
            image_path = generate_image(
                user_prompt=prompt,
                title="Content Analysis Visualization",
                description="Visual representation of content analysis insights",
                aspect_ratio="16:9"
            )
            
            return image_path
            
        except Exception as e:
            st.error(f"Error generating content visualization: {str(e)}")
            return None
    
    def _generate_competitor_visualization(self, competitors: List[str], insights: Dict[str, Any]) -> str:
        """Generate visual representation of competitor analysis."""
        try:
            # Create a prompt for image generation
            prompt = f"""
            Create a visual representation of competitor analysis with the following insights:
            
            Market Position: {insights.get('strategy', [])}
            Competitive Advantages: {insights.get('content', [])}
            
            The image should be professional, data-driven, and easy to understand.
            """
            
            # Generate image
            image_path = generate_image(
                user_prompt=prompt,
                title="Competitor Analysis Visualization",
                description="Visual representation of competitor analysis insights",
                aspect_ratio="16:9"
            )
            
            return image_path
            
        except Exception as e:
            st.error(f"Error generating competitor visualization: {str(e)}")
            return None
    
    def _generate_keyword_visualization(self, keywords: Dict[str, Any], insights: Dict[str, Any]) -> str:
        """Generate visual representation of keyword analysis."""
        try:
            # Create a prompt for image generation
            prompt = f"""
            Create a visual representation of keyword analysis with the following insights:
            
            Keyword Opportunities: {insights.get('opportunities', [])}
            Content Strategy: {insights.get('strategy', [])}
            
            The image should be professional, data-driven, and easy to understand.
            """
            
            # Generate image
            image_path = generate_image(
                user_prompt=prompt,
                title="Keyword Analysis Visualization",
                description="Visual representation of keyword analysis insights",
                aspect_ratio="16:9"
            )
            
            return image_path
            
        except Exception as e:
            st.error(f"Error generating keyword visualization: {str(e)}")
            return None
    
    def _generate_recommendation_visualization(self, recommendations: Dict[str, Any], insights: Dict[str, Any]) -> str:
        """Generate visual representation of recommendation analysis."""
        try:
            # Create a prompt for image generation
            prompt = f"""
            Create a visual representation of recommendation analysis with the following insights:
            
            Content Strategy: {insights.get('content', [])}
            Technical Strategy: {insights.get('technical', [])}
            
            The image should be professional, data-driven, and easy to understand.
            """
            
            # Generate image
            image_path = generate_image(
                user_prompt=prompt,
                title="Recommendation Analysis Visualization",
                description="Visual representation of recommendation analysis insights",
                aspect_ratio="16:9"
            )
            
            return image_path
            
        except Exception as e:
            st.error(f"Error generating recommendation visualization: {str(e)}")
            return None 