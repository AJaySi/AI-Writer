"""
Keyword researcher for content gap analysis.
"""

from typing import Dict, Any, List, Optional
import streamlit as st
from loguru import logger
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer
from lib.ai_seo_tools.content_gap_analysis.utils.data_collector import DataCollector
from lib.ai_seo_tools.content_gap_analysis.utils.content_parser import ContentParser
from lib.ai_seo_tools.content_gap_analysis.utils.ai_processor import AIProcessor, ProgressTracker
import asyncio
import sys
import os
import json
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main
from lib.ai_seo_tools.seo_structured_data import ai_structured_data

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/keyword_researcher.log",
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

class KeywordResearcher:
    """Researches and analyzes keywords for content strategy."""
    
    def __init__(self):
        """Initialize the keyword researcher."""
        self.ai_processor = AIProcessor()
        self.progress = ProgressTracker()
        
        # Define analysis stages
        self.stages = {
            'keyword_analysis': {
                'name': 'Keyword Analysis',
                'steps': [
                    'Initializing keyword research',
                    'Analyzing keyword trends',
                    'Evaluating search intent',
                    'Identifying opportunities',
                    'Generating keyword insights'
                ]
            }
        }
    
    def analyze(self, industry: str, url: str) -> Dict[str, Any]:
        """
        Analyze keywords for content strategy.
        
        Args:
            industry: Industry category
            url: Target website URL
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            self.progress.start_stage('keyword_analysis')
            self.progress.next_step()
            
            # Analyze keyword trends
            trend_analysis = self._analyze_keyword_trends(industry)
            self.progress.next_step()
            
            # Evaluate search intent
            intent_analysis = self._evaluate_search_intent(trend_analysis)
            self.progress.next_step()
            
            # Identify opportunities
            opportunities = self._identify_opportunities(trend_analysis, intent_analysis)
            self.progress.next_step()
            
            # Generate insights
            insights = self._generate_keyword_insights(trend_analysis, intent_analysis, opportunities)
            self.progress.next_step()
            
            self.progress.complete_stage()
            
            return {
                'trend_analysis': trend_analysis,
                'intent_analysis': intent_analysis,
                'opportunities': opportunities,
                'insights': insights
            }
            
        except Exception as e:
            if self.progress.current_stage:
                self.progress.update_progress(0, f"Error in {self.progress.stages[self.progress.current_stage]['name']}: {str(e)}")
            st.error(f"Error analyzing keywords: {str(e)}")
            return {
                'error': str(e),
                'trend_analysis': {},
                'intent_analysis': {},
                'opportunities': [],
                'insights': []
            }
    
    def _analyze_keyword_trends(self, industry: str) -> Dict[str, Any]:
        """Analyze keyword trends."""
        try:
            # Get AI analysis for keyword trends
            analysis = self.ai_processor.analyze_keywords({
                'industry': industry,
                'keywords': {}  # Keywords will be fetched by AI processor
            })
            
            return {
                'trends': analysis.get('keyword_trends', {}),
                'search_intent': analysis.get('search_intent', {}),
                'keyword_insights': analysis.get('keyword_insights', {})
            }
        except Exception as e:
            st.error(f"Error analyzing keyword trends: {str(e)}")
            return {}
    
    def _evaluate_search_intent(self, trend_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate search intent."""
        try:
            intent_analysis = {
                'informational': [],
                'transactional': [],
                'navigational': [],
                'commercial': []
            }
            
            # Categorize keywords by intent
            for keyword, data in trend_analysis.get('trends', {}).items():
                intent = data.get('intent', 'informational')
                if intent in intent_analysis:
                    intent_analysis[intent].append({
                        'keyword': keyword,
                        'volume': data.get('volume', 0),
                        'difficulty': data.get('difficulty', 0)
                    })
            
            return intent_analysis
        except Exception as e:
            st.error(f"Error evaluating search intent: {str(e)}")
            return {}
    
    def _identify_opportunities(self, trend_analysis: Dict[str, Any], intent_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify keyword opportunities."""
        try:
            opportunities = []
            
            # Analyze each intent category
            for intent, keywords in intent_analysis.items():
                for keyword_data in keywords:
                    # Calculate opportunity score
                    volume = keyword_data.get('volume', 0)
                    difficulty = keyword_data.get('difficulty', 0)
                    opportunity_score = volume * (1 - difficulty/100)
                    
                    if opportunity_score > 50:  # Threshold for good opportunities
                        opportunities.append({
                            'keyword': keyword_data['keyword'],
                            'intent': intent,
                            'volume': volume,
                            'difficulty': difficulty,
                            'opportunity_score': opportunity_score
                        })
            
            # Sort by opportunity score
            opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
            
            return opportunities
        except Exception as e:
            st.error(f"Error identifying opportunities: {str(e)}")
            return []
    
    def _generate_keyword_insights(self, trend_analysis: Dict[str, Any], intent_analysis: Dict[str, Any], opportunities: List[Dict[str, Any]]) -> List[str]:
        """Generate keyword insights."""
        try:
            insights = []
            
            # Trend insights
            if trend_analysis.get('trends'):
                insights.append(f"Analyzed {len(trend_analysis['trends'])} keywords for trends")
            
            # Intent insights
            for intent, keywords in intent_analysis.items():
                if keywords:
                    insights.append(f"Found {len(keywords)} {intent} keywords")
            
            # Opportunity insights
            if opportunities:
                insights.append(f"Identified {len(opportunities)} high-potential keyword opportunities")
            
            return insights
        except Exception as e:
            st.error(f"Error generating keyword insights: {str(e)}")
            return []
    
    def _generate_titles(self, industry: str) -> dict:
        """
        Generate keyword-based titles using the title generator.
        
        Args:
            industry (str): The industry to generate titles for
            
        Returns:
            dict: Generated titles and patterns
        """
        return ai_title_generator(industry)
    
    def _analyze_meta_descriptions(self, industry: str) -> dict:
        """
        Analyze meta descriptions for keyword usage.
        
        Args:
            industry (str): The industry to analyze
            
        Returns:
            dict: Meta description analysis results
        """
        return metadesc_generator_main(industry)
    
    def _analyze_structured_data(self, industry: str) -> dict:
        """
        Analyze structured data implementation.
        
        Args:
            industry (str): The industry to analyze
            
        Returns:
            dict: Structured data analysis results
        """
        return ai_structured_data(industry)
    
    def _extract_keywords(self, titles: dict, meta_analysis: dict) -> list:
        """
        Extract keywords from titles and meta descriptions.
        
        Args:
            titles (dict): Generated titles
            meta_analysis (dict): Meta description analysis
            
        Returns:
            list: Extracted keywords with metrics
        """
        prompt = f"""
        As an SEO expert, analyze the following content and extract relevant keywords with their metrics:

        Titles: {titles}
        Meta Descriptions: {meta_analysis}

        Please provide a JSON response with the following structure:
        {{
            "keywords": [
                {{
                    "keyword": "string",
                    "search_volume": "number",
                    "difficulty": "number",
                    "relevance_score": "number",
                    "content_type": "string"
                }}
            ],
            "summary": {{
                "total_keywords": "number",
                "high_opportunity_keywords": "number",
                "recommended_focus_areas": ["string"]
            }}
        }}

        Focus on:
        1. Primary keywords and their variations
        2. Long-tail keywords
        3. Industry-specific terminology
        4. Search volume and difficulty metrics
        5. Content type recommendations
        """

        try:
            response = llm_text_gen(prompt, json_struct={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "keyword": {"type": "string"},
                                "search_volume": {"type": "number"},
                                "difficulty": {"type": "number"},
                                "relevance_score": {"type": "number"},
                                "content_type": {"type": "string"}
                            }
                        }
                    },
                    "summary": {
                        "type": "object",
                        "properties": {
                            "total_keywords": {"type": "number"},
                            "high_opportunity_keywords": {"type": "number"},
                            "recommended_focus_areas": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            })
            return response
        except Exception as e:
            st.error(f"Error extracting keywords: {e}")
            return []
    
    def _analyze_search_intent(self, ai_insights: dict) -> dict:
        """
        Analyze search intent from AI insights.
        
        Args:
            ai_insights (dict): AI-processed insights
            
        Returns:
            dict: Search intent analysis
        """
        prompt = f"""
        As an SEO expert, analyze the following content insights and determine the search intent:

        Content Insights: {ai_insights}

        Please provide a JSON response with the following structure:
        {{
            "informational": [
                {{
                    "keyword": "string",
                    "intent_type": "string",
                    "content_suggestions": ["string"]
                }}
            ],
            "transactional": [
                {{
                    "keyword": "string",
                    "intent_type": "string",
                    "content_suggestions": ["string"]
                }}
            ],
            "navigational": [
                {{
                    "keyword": "string",
                    "intent_type": "string",
                    "content_suggestions": ["string"]
                }}
            ],
            "summary": {{
                "dominant_intent": "string",
                "content_strategy_recommendations": ["string"]
            }}
        }}

        Focus on:
        1. Identifying primary search intent for each keyword
        2. Suggesting appropriate content types
        3. Providing content strategy recommendations
        4. Analyzing user behavior patterns
        """

        try:
            response = llm_text_gen(prompt, json_struct={
                "type": "object",
                "properties": {
                    "informational": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "keyword": {"type": "string"},
                                "intent_type": {"type": "string"},
                                "content_suggestions": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            }
                        }
                    },
                    "transactional": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "keyword": {"type": "string"},
                                "intent_type": {"type": "string"},
                                "content_suggestions": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            }
                        }
                    },
                    "navigational": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "keyword": {"type": "string"},
                                "intent_type": {"type": "string"},
                                "content_suggestions": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            }
                        }
                    },
                    "summary": {
                        "type": "object",
                        "properties": {
                            "dominant_intent": {"type": "string"},
                            "content_strategy_recommendations": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            })
            return response
        except Exception as e:
            st.error(f"Error analyzing search intent: {e}")
            return {
                'informational': [],
                'transactional': [],
                'navigational': []
            }
    
    def _suggest_content_formats(self, ai_insights: dict) -> list:
        """
        Suggest content formats based on AI insights.
        
        Args:
            ai_insights (dict): AI-processed insights
            
        Returns:
            list: Suggested content formats
        """
        prompt = f"""
        As a content strategy expert, analyze the following insights and suggest appropriate content formats:

        AI Insights: {ai_insights}

        Please provide a JSON response with the following structure:
        {{
            "content_formats": [
                {{
                    "format": "string",
                    "description": "string",
                    "use_cases": ["string"],
                    "recommended_topics": ["string"],
                    "estimated_impact": "string"
                }}
            ],
            "format_strategy": {{
                "primary_formats": ["string"],
                "secondary_formats": ["string"],
                "implementation_priority": ["string"]
            }}
        }}

        Focus on:
        1. Identifying the most effective content formats
        2. Matching formats to user intent
        3. Suggesting specific use cases
        4. Providing implementation guidance
        """

        try:
            response = llm_text_gen(prompt, json_struct={
                "type": "object",
                "properties": {
                    "content_formats": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "format": {"type": "string"},
                                "description": {"type": "string"},
                                "use_cases": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "recommended_topics": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "estimated_impact": {"type": "string"}
                            }
                        }
                    },
                    "format_strategy": {
                        "type": "object",
                        "properties": {
                            "primary_formats": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "secondary_formats": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "implementation_priority": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            })
            return response
        except Exception as e:
            st.error(f"Error suggesting content formats: {e}")
            return []
    
    def _create_topic_clusters(self, ai_insights: dict) -> dict:
        """
        Create topic clusters from AI insights.
        
        Args:
            ai_insights (dict): AI-processed insights
            
        Returns:
            dict: Topic clusters and relationships
        """
        prompt = f"""
        As a content organization expert, analyze the following insights and create topic clusters:

        AI Insights: {ai_insights}

        Please provide a JSON response with the following structure:
        {{
            "clusters": [
                {{
                    "cluster_name": "string",
                    "main_topics": ["string"],
                    "subtopics": ["string"],
                    "related_keywords": ["string"],
                    "content_opportunities": ["string"]
                }}
            ],
            "relationships": {{
                "cluster_connections": [
                    {{
                        "source": "string",
                        "target": "string",
                        "relationship_type": "string",
                        "strength": "number"
                    }}
                ],
                "content_hierarchy": {{
                    "primary_topics": ["string"],
                    "secondary_topics": ["string"],
                    "tertiary_topics": ["string"]
                }}
            }}
        }}

        Focus on:
        1. Identifying main topic clusters
        2. Organizing subtopics and related keywords
        3. Mapping relationships between clusters
        4. Suggesting content opportunities
        """

        try:
            response = llm_text_gen(prompt, json_struct={
                "type": "object",
                "properties": {
                    "clusters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "cluster_name": {"type": "string"},
                                "main_topics": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "subtopics": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "related_keywords": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "content_opportunities": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            }
                        }
                    },
                    "relationships": {
                        "type": "object",
                        "properties": {
                            "cluster_connections": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "source": {"type": "string"},
                                        "target": {"type": "string"},
                                        "relationship_type": {"type": "string"},
                                        "strength": {"type": "number"}
                                    }
                                }
                            },
                            "content_hierarchy": {
                                "type": "object",
                                "properties": {
                                    "primary_topics": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "secondary_topics": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "tertiary_topics": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            })
            return response
        except Exception as e:
            st.error(f"Error creating topic clusters: {e}")
            return {
                'clusters': [],
                'relationships': {}
            } 