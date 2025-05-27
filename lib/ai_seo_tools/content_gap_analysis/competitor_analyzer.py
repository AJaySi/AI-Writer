"""
Competitor analyzer for content gap analysis.
"""

from typing import Dict, Any, List, Optional
import streamlit as st
from collections import Counter, defaultdict
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

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/competitor_analyzer.log",
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

class CompetitorAnalyzer:
    """Analyzes competitor content and market position."""
    
    def __init__(self):
        """Initialize the competitor analyzer."""
        self.website_analyzer = WebsiteAnalyzer()
        self.ai_processor = AIProcessor()
        self.progress = ProgressTracker()
        
        # Define analysis stages
        self.stages = {
            'competitor_analysis': {
                'name': 'Competitor Analysis',
                'steps': [
                    'Initializing competitor analysis',
                    'Analyzing competitor content',
                    'Evaluating market position',
                    'Identifying content gaps',
                    'Generating competitive insights'
                ]
            }
        }
        
        logger.info("CompetitorAnalyzer initialized")
    
    def analyze(self, competitor_urls: List[str], industry: str) -> Dict[str, Any]:
        """
        Analyze competitor websites.
        
        Args:
            competitor_urls: List of competitor URLs to analyze
            industry: Industry category
            
        Returns:
            Dictionary containing competitor analysis results
        """
        try:
            results = {
                'competitors': [],
                'market_position': {},
                'content_gaps': [],
                'advantages': []
            }
            
            # Analyze each competitor
            for url in competitor_urls:
                competitor_analysis = self.website_analyzer.analyze_website(url)
                if competitor_analysis.get('success', False):
                    results['competitors'].append({
                        'url': url,
                        'analysis': competitor_analysis['data']
                    })
            
            # Generate market position analysis using AI
            prompt = f"""Analyze the market position of competitors in the {industry} industry:
            
            Competitor Analyses:
            {json.dumps(results['competitors'], indent=2)}
            
            Provide:
            1. Market position analysis
            2. Content gaps
            3. Competitive advantages
            
            Format the response as JSON with 'market_position', 'content_gaps', and 'advantages' keys."""
            
            # Get AI analysis
            analysis = llm_text_gen(
                prompt=prompt,
                system_prompt="You are an SEO expert specializing in competitive analysis.",
                response_format="json_object"
            )
            
            if analysis:
                results['market_position'] = analysis.get('market_position', {})
                results['content_gaps'] = analysis.get('content_gaps', [])
                results['advantages'] = analysis.get('advantages', [])
            
            return results
            
        except Exception as e:
            error_msg = f"Error analyzing competitors: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'error': error_msg,
                'competitors': [],
                'market_position': {},
                'content_gaps': [],
                'advantages': []
            }
    
    def _analyze_competitor_content(self, competitor_urls: List[str]) -> Dict[str, Any]:
        """Analyze competitor content."""
        try:
            content_analysis = {}
            
            for url in competitor_urls:
                # Get AI analysis for each competitor
                analysis = self.ai_processor.analyze_content({
                    'url': url,
                    'content': {}  # Content will be fetched by AI processor
                })
                
                content_analysis[url] = {
                    'content_metrics': analysis.get('content_metrics', {}),
                    'content_evolution': analysis.get('content_evolution', {}),
                    'topic_trends': analysis.get('topic_trends', {}),
                    'performance_trends': analysis.get('performance_trends', {})
                }
            
            return content_analysis
        except Exception as e:
            st.error(f"Error analyzing competitor content: {str(e)}")
            return {}
    
    def _evaluate_market_position(self, content_analysis: Dict[str, Any], industry: str) -> Dict[str, Any]:
        """Evaluate market position."""
        try:
            market_position = {
                'industry_rank': 0,
                'content_quality_rank': 0,
                'market_share': 0,
                'competitive_advantages': [],
                'competitive_disadvantages': []
            }
            
            # Calculate industry rank based on content quality
            content_quality_scores = [
                analysis.get('content_metrics', {}).get('quality_score', 0)
                for analysis in content_analysis.values()
            ]
            
            if content_quality_scores:
                market_position['content_quality_rank'] = sum(content_quality_scores) / len(content_quality_scores)
            
            # Identify competitive advantages and disadvantages
            for url, analysis in content_analysis.items():
                quality_score = analysis.get('content_metrics', {}).get('quality_score', 0)
                
                if quality_score > market_position['content_quality_rank']:
                    market_position['competitive_advantages'].append({
                        'url': url,
                        'advantage': 'Higher content quality',
                        'score': quality_score
                    })
                elif quality_score < market_position['content_quality_rank']:
                    market_position['competitive_disadvantages'].append({
                        'url': url,
                        'disadvantage': 'Lower content quality',
                        'score': quality_score
                    })
            
            return market_position
        except Exception as e:
            st.error(f"Error evaluating market position: {str(e)}")
            return {}
    
    def _identify_content_gaps(self, content_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify content gaps."""
        try:
            content_gaps = []
            
            # Analyze content coverage
            all_topics = set()
            for analysis in content_analysis.values():
                topics = analysis.get('topic_trends', {}).get('topics', [])
                all_topics.update(topics)
            
            # Identify missing topics for each competitor
            for url, analysis in content_analysis.items():
                covered_topics = set(analysis.get('topic_trends', {}).get('topics', []))
                missing_topics = all_topics - covered_topics
                
                if missing_topics:
                    content_gaps.append({
                        'url': url,
                        'missing_topics': list(missing_topics),
                        'gap_type': 'topic_coverage'
                    })
            
            return content_gaps
        except Exception as e:
            st.error(f"Error identifying content gaps: {str(e)}")
            return []
    
    def _generate_competitive_insights(self, content_analysis: Dict[str, Any], market_position: Dict[str, Any], content_gaps: List[Dict[str, Any]]) -> List[str]:
        """Generate competitive insights."""
        try:
            insights = []
            
            # Market position insights
            if market_position.get('content_quality_rank', 0) > 80:
                insights.append("Strong market position with high content quality")
            elif market_position.get('content_quality_rank', 0) > 60:
                insights.append("Moderate market position with room for improvement")
            else:
                insights.append("Weak market position requiring significant improvement")
            
            # Content gap insights
            if content_gaps:
                insights.append(f"Identified {len(content_gaps)} content gaps across competitors")
            
            # Competitive advantage insights
            if market_position.get('competitive_advantages'):
                insights.append(f"Found {len(market_position['competitive_advantages'])} competitive advantages")
            
            return insights
        except Exception as e:
            st.error(f"Error generating competitive insights: {str(e)}")
            return []
    
    def _run_seo_analysis(self, url: str) -> dict:
        """
        Run SEO analysis on competitor website.
        
        Args:
            url (str): The URL to analyze
            
        Returns:
            dict: SEO analysis results
        """
        # Run website analysis using the new analyzer
        analysis = self.website_analyzer.analyze_website(url)
        
        if not analysis.get('success', False):
            return {
                'error': analysis.get('error', 'Unknown error in SEO analysis'),
                'onpage_seo': {},
                'url_seo': {}
            }
        
        # Extract SEO information from the analysis
        seo_info = analysis['data']['analysis']['seo_info']
        basic_info = analysis['data']['analysis']['basic_info']
        
        return {
            'onpage_seo': {
                'meta_tags': seo_info.get('meta_tags', {}),
                'content': seo_info.get('content', {}),
                'recommendations': seo_info.get('recommendations', [])
            },
            'url_seo': {
                'title': basic_info.get('title', ''),
                'meta_description': basic_info.get('meta_description', ''),
                'has_robots_txt': bool(basic_info.get('robots_txt')),
                'has_sitemap': bool(basic_info.get('sitemap'))
            }
        }
    
    def _analyze_title_patterns(self, url: str) -> dict:
        """
        Analyze title patterns using the title generator.
        
        Args:
            url (str): The URL to analyze
            
        Returns:
            dict: Title pattern analysis results
        """
        # Use title generator to analyze patterns
        title_analysis = ai_title_generator(url)
        
        return {
            'patterns': title_analysis.get('patterns', {}),
            'suggestions': title_analysis.get('suggestions', [])
        }
    
    def _compare_competitors(self, results: dict) -> dict:
        """
        Compare results across all competitors.
        
        Args:
            results (dict): Analysis results for all competitors
            
        Returns:
            dict: Comparative analysis results
        """
        comparison = {
            'content_comparison': self._compare_content(results),
            'seo_comparison': self._compare_seo(results),
            'title_comparison': self._compare_titles(results),
            'performance_metrics': self._compare_performance(results),
            'content_gaps': self._identify_content_gaps(results)
        }
        
        # Add AI-enhanced insights
        comparison['ai_insights'] = self.ai_processor.analyze_competitor_comparison(comparison)
        
        return comparison
    
    def _compare_content(self, results: dict) -> dict:
        """Compare content structure across competitors."""
        content_comparison = {
            'topic_distribution': self._analyze_topic_distribution(results),
            'content_depth': self._analyze_content_depth(results),
            'content_formats': self._analyze_content_formats(results),
            'content_quality': self._analyze_content_quality(results)
        }
        
        return content_comparison
    
    def _analyze_topic_distribution(self, results: dict) -> dict:
        """Analyze topic distribution across competitors."""
        all_topics = []
        topic_frequency = Counter()
        
        for url, data in results.items():
            topics = data['content_structure'].get('topics', [])
            all_topics.extend([t['topic'] for t in topics])
            topic_frequency.update([t['topic'] for t in topics])
        
        return {
            'common_topics': [topic for topic, count in topic_frequency.most_common(10)],
            'unique_topics': list(set(all_topics)),
            'topic_frequency': dict(topic_frequency.most_common()),
            'topic_coverage': len(set(all_topics)) / len(all_topics) if all_topics else 0
        }
    
    def _analyze_content_depth(self, results: dict) -> dict:
        """Analyze content depth across competitors."""
        depth_metrics = {
            'word_counts': {},
            'section_counts': {},
            'heading_distribution': defaultdict(list),
            'content_hierarchy': {}
        }
        
        for url, data in results.items():
            content_structure = data['content_structure']
            
            # Word count analysis
            depth_metrics['word_counts'][url] = content_structure.get('text_statistics', {}).get('word_count', 0)
            
            # Section analysis
            depth_metrics['section_counts'][url] = len(content_structure.get('sections', []))
            
            # Heading distribution
            for level, count in content_structure.get('hierarchy', {}).get('heading_distribution', {}).items():
                depth_metrics['heading_distribution'][level].append(count)
            
            # Content hierarchy
            depth_metrics['content_hierarchy'][url] = content_structure.get('hierarchy', {})
        
        return depth_metrics
    
    def _analyze_content_formats(self, results: dict) -> dict:
        """Analyze content formats across competitors."""
        format_analysis = {
            'format_types': defaultdict(int),
            'format_distribution': defaultdict(list),
            'format_effectiveness': {}
        }
        
        for url, data in results.items():
            sections = data['content_structure'].get('sections', [])
            
            for section in sections:
                format_type = section.get('type', 'unknown')
                format_analysis['format_types'][format_type] += 1
                format_analysis['format_distribution'][format_type].append({
                    'url': url,
                    'heading': section.get('heading', ''),
                    'word_count': section.get('word_count', 0)
                })
        
        return format_analysis
    
    def _analyze_content_quality(self, results: dict) -> dict:
        """Analyze content quality across competitors."""
        quality_metrics = {
            'readability_scores': {},
            'content_structure_scores': {},
            'engagement_metrics': {},
            'overall_quality': {}
        }
        
        for url, data in results.items():
            content_structure = data['content_structure']
            
            # Readability analysis
            readability = content_structure.get('readability', {})
            quality_metrics['readability_scores'][url] = {
                'flesch_score': readability.get('flesch_score', 0),
                'avg_sentence_length': readability.get('avg_sentence_length', 0),
                'avg_word_length': readability.get('avg_word_length', 0)
            }
            
            # Structure analysis
            hierarchy = content_structure.get('hierarchy', {})
            quality_metrics['content_structure_scores'][url] = {
                'has_proper_hierarchy': hierarchy.get('has_proper_hierarchy', False),
                'heading_distribution': hierarchy.get('heading_distribution', {}),
                'max_depth': hierarchy.get('max_depth', 0)
            }
        
        return quality_metrics
    
    def _compare_seo(self, results: dict) -> dict:
        """Compare SEO metrics across competitors."""
        seo_comparison = {
            'onpage_metrics': defaultdict(list),
            'technical_metrics': defaultdict(list),
            'content_metrics': defaultdict(list),
            'overall_seo_score': {}
        }
        
        for url, data in results.items():
            seo_info = data.get('website_analysis', {}).get('analysis', {}).get('seo_info', {})
            
            # On-page SEO metrics
            meta_tags = seo_info.get('meta_tags', {})
            seo_comparison['onpage_metrics']['title_score'].append(
                100 if meta_tags.get('title', {}).get('status') == 'good' else 50
            )
            seo_comparison['onpage_metrics']['description_score'].append(
                100 if meta_tags.get('description', {}).get('status') == 'good' else 50
            )
            seo_comparison['onpage_metrics']['keywords_score'].append(
                100 if meta_tags.get('keywords', {}).get('status') == 'good' else 50
            )
            
            # Technical SEO metrics
            technical = data.get('website_analysis', {}).get('analysis', {}).get('basic_info', {})
            seo_comparison['technical_metrics']['has_robots_txt'].append(
                100 if technical.get('robots_txt') else 0
            )
            seo_comparison['technical_metrics']['has_sitemap'].append(
                100 if technical.get('sitemap') else 0
            )
            
            # Content SEO metrics
            content = seo_info.get('content', {})
            seo_comparison['content_metrics']['readability_score'].append(
                content.get('readability_score', 0)
            )
            seo_comparison['content_metrics']['content_quality_score'].append(
                content.get('content_quality_score', 0)
            )
            
            # Overall SEO score
            seo_comparison['overall_seo_score'][url] = seo_info.get('overall_score', 0)
        
        return seo_comparison
    
    def _compare_titles(self, results: dict) -> dict:
        """Compare title patterns across competitors."""
        title_comparison = {
            'pattern_distribution': defaultdict(int),
            'length_distribution': defaultdict(list),
            'keyword_usage': defaultdict(int),
            'format_preferences': defaultdict(int)
        }
        
        for url, data in results.items():
            title_patterns = data['title_patterns']
            
            # Pattern analysis
            for pattern in title_patterns.get('patterns', {}):
                title_comparison['pattern_distribution'][pattern] += 1
            
            # Length analysis
            for suggestion in title_patterns.get('suggestions', []):
                title_comparison['length_distribution'][len(suggestion)].append(suggestion)
            
            # Keyword analysis
            for suggestion in title_patterns.get('suggestions', []):
                words = suggestion.lower().split()
                for word in words:
                    if len(word) > 3:  # Filter out short words
                        title_comparison['keyword_usage'][word] += 1
        
        return title_comparison
    
    def _compare_performance(self, results: dict) -> dict:
        """Compare performance metrics across competitors."""
        performance_metrics = {
            'content_effectiveness': {},
            'engagement_metrics': {},
            'technical_performance': {},
            'overall_performance': {}
        }
        
        for url, data in results.items():
            # Content effectiveness
            content_structure = data['content_structure']
            performance_metrics['content_effectiveness'][url] = {
                'content_depth': content_structure.get('text_statistics', {}).get('word_count', 0),
                'content_quality': content_structure.get('readability', {}).get('flesch_score', 0),
                'content_structure': content_structure.get('hierarchy', {}).get('has_proper_hierarchy', False)
            }
            
            # Technical performance
            seo_analysis = data['seo_analysis']
            performance_metrics['technical_performance'][url] = {
                'onpage_score': sum(1 for v in seo_analysis.get('onpage_seo', {}).values() if v),
                'technical_score': sum(1 for v in seo_analysis.get('url_seo', {}).values() if v)
            }
        
        return performance_metrics
    
    def _find_missing_topics(self, results: dict) -> List[Dict[str, Any]]:
        """Find topics that are missing or underrepresented."""
        all_topics = set()
        topic_coverage = defaultdict(int)
        
        # Collect all topics and their coverage
        for url, data in results.items():
            topics = data['content_structure'].get('topics', [])
            for topic in topics:
                all_topics.add(topic['topic'])
                topic_coverage[topic['topic']] += 1
        
        # Identify missing or underrepresented topics
        missing_topics = []
        total_competitors = len(results)
        
        for topic in all_topics:
            coverage = topic_coverage[topic] / total_competitors
            if coverage < 0.5:  # Topic covered by less than 50% of competitors
                missing_topics.append({
                    'topic': topic,
                    'coverage': coverage,
                    'opportunity_score': 1 - coverage
                })
        
        return sorted(missing_topics, key=lambda x: x['opportunity_score'], reverse=True)
    
    def _identify_opportunities(self, results: dict) -> List[Dict[str, Any]]:
        """Identify content opportunities based on analysis."""
        opportunities = []
        
        # Analyze content depth opportunities
        depth_metrics = self._analyze_content_depth(results)
        avg_word_count = sum(depth_metrics['word_counts'].values()) / len(depth_metrics['word_counts'])
        
        for url, word_count in depth_metrics['word_counts'].items():
            if word_count < avg_word_count * 0.7:  # Content depth significantly below average
                opportunities.append({
                    'type': 'content_depth',
                    'url': url,
                    'current_value': word_count,
                    'target_value': avg_word_count,
                    'opportunity_score': (avg_word_count - word_count) / avg_word_count
                })
        
        # Analyze format opportunities
        format_analysis = self._analyze_content_formats(results)
        for format_type, distribution in format_analysis['format_distribution'].items():
            if len(distribution) < len(results) * 0.3:  # Format used by less than 30% of competitors
                opportunities.append({
                    'type': 'content_format',
                    'format': format_type,
                    'current_coverage': len(distribution) / len(results),
                    'opportunity_score': 1 - (len(distribution) / len(results))
                })
        
        return sorted(opportunities, key=lambda x: x['opportunity_score'], reverse=True)
    
    def _analyze_format_gaps(self, results: dict) -> List[Dict[str, Any]]:
        """Analyze gaps in content formats."""
        format_gaps = []
        format_analysis = self._analyze_content_formats(results)
        
        # Identify underutilized formats
        for format_type, count in format_analysis['format_types'].items():
            if count < len(results) * 0.3:  # Format used by less than 30% of competitors
                format_gaps.append({
                    'format': format_type,
                    'current_usage': count,
                    'potential_impact': 'high' if count < len(results) * 0.2 else 'medium',
                    'suggested_implementation': self._generate_format_suggestions(format_type)
                })
        
        return format_gaps
    
    def _analyze_quality_gaps(self, results: dict) -> List[Dict[str, Any]]:
        """Analyze gaps in content quality."""
        quality_gaps = []
        quality_metrics = self._analyze_content_quality(results)
        
        # Analyze readability gaps
        readability_scores = quality_metrics['readability_scores']
        avg_flesch = sum(score['flesch_score'] for score in readability_scores.values()) / len(readability_scores)
        
        for url, scores in readability_scores.items():
            if scores['flesch_score'] < avg_flesch * 0.8:  # Readability significantly below average
                quality_gaps.append({
                    'type': 'readability',
                    'url': url,
                    'current_score': scores['flesch_score'],
                    'target_score': avg_flesch,
                    'improvement_needed': avg_flesch - scores['flesch_score']
                })
        
        return quality_gaps
    
    def _analyze_seo_gaps(self, results: dict) -> List[Dict[str, Any]]:
        """Analyze gaps in SEO implementation."""
        seo_gaps = []
        seo_comparison = self._compare_seo(results)
        
        # Analyze on-page SEO gaps
        for metric, values in seo_comparison['onpage_metrics'].items():
            avg_value = sum(values) / len(values)
            for url, value in zip(results.keys(), values):
                if value < avg_value * 0.7:  # Significantly below average
                    seo_gaps.append({
                        'type': 'onpage_seo',
                        'metric': metric,
                        'url': url,
                        'current_value': value,
                        'target_value': avg_value,
                        'improvement_needed': avg_value - value
                    })
        
        # Analyze technical SEO gaps
        for metric, values in seo_comparison['technical_metrics'].items():
            avg_value = sum(values) / len(values)
            for url, value in zip(results.keys(), values):
                if value < avg_value * 0.7:  # Significantly below average
                    seo_gaps.append({
                        'type': 'technical_seo',
                        'metric': metric,
                        'url': url,
                        'current_value': value,
                        'target_value': avg_value,
                        'improvement_needed': avg_value - value
                    })
        
        # Analyze content SEO gaps
        for metric, values in seo_comparison['content_metrics'].items():
            avg_value = sum(values) / len(values)
            for url, value in zip(results.keys(), values):
                if value < avg_value * 0.7:  # Significantly below average
                    seo_gaps.append({
                        'type': 'content_seo',
                        'metric': metric,
                        'url': url,
                        'current_value': value,
                        'target_value': avg_value,
                        'improvement_needed': avg_value - value
                    })
        
        return seo_gaps
    
    def _generate_format_suggestions(self, format_type: str) -> List[str]:
        """Generate suggestions for implementing specific content formats."""
        format_suggestions = {
            'article': [
                'Create in-depth articles with comprehensive coverage',
                'Include expert quotes and statistics',
                'Add visual elements and infographics'
            ],
            'blog_post': [
                'Write engaging blog posts with personal insights',
                'Include call-to-actions',
                'Add social sharing buttons'
            ],
            'how-to': [
                'Create step-by-step guides',
                'Include screenshots or videos',
                'Add troubleshooting sections'
            ],
            'case_study': [
                'Present real-world examples',
                'Include metrics and results',
                'Add client testimonials'
            ]
        }
        
        return format_suggestions.get(format_type, [
            'Research successful examples',
            'Analyze competitor implementation',
            'Create unique value proposition'
        ]) 