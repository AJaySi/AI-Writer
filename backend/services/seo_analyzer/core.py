"""
Core SEO Analyzer Module
Contains the main ComprehensiveSEOAnalyzer class and data structures.
"""

from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from loguru import logger

from .analyzers import (
    URLStructureAnalyzer,
    MetaDataAnalyzer,
    ContentAnalyzer,
    TechnicalSEOAnalyzer,
    PerformanceAnalyzer,
    AccessibilityAnalyzer,
    UserExperienceAnalyzer,
    SecurityHeadersAnalyzer,
    KeywordAnalyzer
)
from .utils import HTMLFetcher, AIInsightGenerator


@dataclass
class SEOAnalysisResult:
    """Data class for SEO analysis results"""
    url: str
    timestamp: datetime
    overall_score: int
    health_status: str
    critical_issues: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    data: Dict[str, Any]


class ComprehensiveSEOAnalyzer:
    """
    Comprehensive SEO Analyzer
    Orchestrates all individual analyzers to provide complete SEO analysis.
    """
    
    def __init__(self):
        """Initialize the comprehensive SEO analyzer with all sub-analyzers"""
        self.html_fetcher = HTMLFetcher()
        self.ai_insight_generator = AIInsightGenerator()
        
        # Initialize all analyzers
        self.url_analyzer = URLStructureAnalyzer()
        self.meta_analyzer = MetaDataAnalyzer()
        self.content_analyzer = ContentAnalyzer()
        self.technical_analyzer = TechnicalSEOAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.accessibility_analyzer = AccessibilityAnalyzer()
        self.ux_analyzer = UserExperienceAnalyzer()
        self.security_analyzer = SecurityHeadersAnalyzer()
        self.keyword_analyzer = KeywordAnalyzer()

    def analyze_url_progressive(self, url: str, target_keywords: Optional[List[str]] = None) -> SEOAnalysisResult:
        """
        Progressive analysis method that runs all analyses with enhanced AI insights
        """
        try:
            logger.info(f"Starting enhanced SEO analysis for URL: {url}")
            
            # Fetch HTML content
            html_content = self.html_fetcher.fetch_html(url)
            if not html_content:
                return self._create_error_result(url, "Failed to fetch HTML content")
            
            # Run all analyzers
            analysis_data = {}
            
            logger.info("Running enhanced analyses...")
            analysis_data.update({
                'url_structure': self.url_analyzer.analyze(url),
                'meta_data': self.meta_analyzer.analyze(html_content, url),
                'content_analysis': self.content_analyzer.analyze(html_content, url),
                'keyword_analysis': self.keyword_analyzer.analyze(html_content, target_keywords) if target_keywords else {},
                'technical_seo': self.technical_analyzer.analyze(html_content, url),
                'accessibility': self.accessibility_analyzer.analyze(html_content),
                'user_experience': self.ux_analyzer.analyze(html_content, url)
            })
            
            # Run potentially slower analyses with error handling
            logger.info("Running security headers analysis...")
            try:
                analysis_data['security_headers'] = self.security_analyzer.analyze(url)
            except Exception as e:
                logger.warning(f"Security headers analysis failed: {e}")
                analysis_data['security_headers'] = self._create_fallback_result('security_headers', str(e))
            
            logger.info("Running performance analysis...")
            try:
                analysis_data['performance'] = self.performance_analyzer.analyze(url)
            except Exception as e:
                logger.warning(f"Performance analysis failed: {e}")
                analysis_data['performance'] = self._create_fallback_result('performance', str(e))
            
            # Generate AI-powered insights
            ai_insights = self.ai_insight_generator.generate_insights(analysis_data, url)
            
            # Calculate overall health
            overall_score, health_status, critical_issues, warnings, recommendations = self._calculate_overall_health(analysis_data, ai_insights)
            
            result = SEOAnalysisResult(
                url=url, 
                timestamp=datetime.now(), 
                overall_score=overall_score,
                health_status=health_status, 
                critical_issues=critical_issues,
                warnings=warnings, 
                recommendations=recommendations, 
                data=analysis_data
            )
            
            logger.info(f"Enhanced SEO analysis completed for {url}. Overall score: {overall_score}")
            return result
            
        except Exception as e:
            logger.error(f"Error in enhanced SEO analysis for {url}: {str(e)}")
            return self._create_error_result(url, str(e))

    def _calculate_overall_health(self, analysis_data: Dict[str, Any], ai_insights: List[Dict[str, Any]]) -> tuple:
        """Calculate overall health with enhanced scoring"""
        scores = []
        all_critical_issues = []
        all_warnings = []
        all_recommendations = []
        
        for category, data in analysis_data.items():
            if isinstance(data, dict) and 'score' in data:
                scores.append(data['score'])
                all_critical_issues.extend(data.get('issues', []))
                all_warnings.extend(data.get('warnings', []))
                all_recommendations.extend(data.get('recommendations', []))
        
        # Calculate overall score
        overall_score = sum(scores) // len(scores) if scores else 0
        
        # Determine health status
        if overall_score >= 80:
            health_status = 'excellent'
        elif overall_score >= 60:
            health_status = 'good'
        elif overall_score >= 40:
            health_status = 'needs_improvement'
        else:
            health_status = 'poor'
        
        # Add AI insights to recommendations
        for insight in ai_insights:
            all_recommendations.append({
                'type': 'ai_insight',
                'message': insight['message'],
                'priority': insight['priority'],
                'action': insight['action'],
                'description': insight['description']
            })
        
        return overall_score, health_status, all_critical_issues, all_warnings, all_recommendations

    def _create_fallback_result(self, category: str, error_message: str) -> Dict[str, Any]:
        """Create a fallback result when analysis fails"""
        return {
            'score': 0, 
            'error': f'{category} analysis failed: {error_message}',
            'issues': [{
                'type': 'critical', 
                'message': f'{category} analysis timed out', 
                'location': 'System', 
                'fix': f'Check {category} manually', 
                'action': 'manual_check'
            }],
            'warnings': [{
                'type': 'warning', 
                'message': f'Could not analyze {category}', 
                'location': 'System', 
                'fix': f'Verify {category} manually', 
                'action': 'manual_check'
            }],
            'recommendations': [{
                'type': 'recommendation', 
                'message': f'Check {category} manually', 
                'priority': 'medium', 
                'action': 'manual_check'
            }]
        }

    def _create_error_result(self, url: str, error_message: str) -> SEOAnalysisResult:
        """Create error result with enhanced structure"""
        return SEOAnalysisResult(
            url=url,
            timestamp=datetime.now(),
            overall_score=0,
            health_status='error',
            critical_issues=[{
                'type': 'critical',
                'message': f'Analysis failed: {error_message}',
                'location': 'System',
                'fix': 'Check URL accessibility and try again',
                'action': 'retry_analysis'
            }],
            warnings=[],
            recommendations=[],
            data={}
        ) 