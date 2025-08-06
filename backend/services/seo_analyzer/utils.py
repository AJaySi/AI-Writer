"""
SEO Analyzer Utilities
Contains utility classes for HTML fetching and AI insight generation.
"""

import requests
from typing import Optional, Dict, List, Any
from loguru import logger


class HTMLFetcher:
    """Utility class for fetching HTML content from URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML content with error handling"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching HTML from {url}: {e}")
            return None


class AIInsightGenerator:
    """Utility class for generating AI-powered insights from analysis data"""
    
    def generate_insights(self, analysis_data: Dict[str, Any], url: str) -> List[Dict[str, Any]]:
        """Generate AI-powered insights based on analysis data"""
        insights = []
        
        # Analyze overall performance
        total_issues = sum(len(data.get('issues', [])) for data in analysis_data.values() if isinstance(data, dict))
        total_warnings = sum(len(data.get('warnings', [])) for data in analysis_data.values() if isinstance(data, dict))
        
        if total_issues > 5:
            insights.append({
                'type': 'critical',
                'message': f'High number of critical issues ({total_issues}) detected',
                'priority': 'high',
                'action': 'fix_critical_issues',
                'description': 'Multiple critical SEO issues need immediate attention to improve search rankings.'
            })
        
        # Content quality insights
        content_data = analysis_data.get('content_analysis', {})
        if content_data.get('word_count', 0) < 300:
            insights.append({
                'type': 'warning',
                'message': 'Content is too thin for good SEO',
                'priority': 'medium',
                'action': 'expand_content',
                'description': 'Add more valuable, relevant content to improve search rankings and user engagement.'
            })
        
        # Technical SEO insights
        technical_data = analysis_data.get('technical_seo', {})
        if not technical_data.get('has_canonical', False):
            insights.append({
                'type': 'critical',
                'message': 'Missing canonical URL can cause duplicate content issues',
                'priority': 'high',
                'action': 'add_canonical',
                'description': 'Canonical URLs help prevent duplicate content penalties.'
            })
        
        # Security insights
        security_data = analysis_data.get('security_headers', {})
        if security_data.get('total_headers', 0) < 3:
            insights.append({
                'type': 'warning',
                'message': 'Insufficient security headers',
                'priority': 'medium',
                'action': 'improve_security',
                'description': 'Security headers protect against common web vulnerabilities.'
            })
        
        # Performance insights
        performance_data = analysis_data.get('performance', {})
        if performance_data.get('load_time', 0) > 3:
            insights.append({
                'type': 'critical',
                'message': 'Page load time is too slow',
                'priority': 'high',
                'action': 'optimize_performance',
                'description': 'Slow loading pages negatively impact user experience and search rankings.'
            })
        
        # URL structure insights
        url_data = analysis_data.get('url_structure', {})
        if not url_data.get('has_https', False):
            insights.append({
                'type': 'critical',
                'message': 'Website is not using HTTPS',
                'priority': 'high',
                'action': 'enable_https',
                'description': 'HTTPS is required for security and is a ranking factor for search engines.'
            })
        
        return insights 