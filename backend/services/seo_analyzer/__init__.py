"""
SEO Analyzer Package
A comprehensive, modular SEO analysis system for web applications.

This package provides:
- URL structure analysis
- Meta data analysis
- Content analysis
- Technical SEO analysis
- Performance analysis
- Accessibility analysis
- User experience analysis
- Security headers analysis
- Keyword analysis
- AI-powered insights generation
- Database service for storing and retrieving analysis results
"""

from .core import ComprehensiveSEOAnalyzer, SEOAnalysisResult
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
from .service import SEOAnalysisService

__version__ = "1.0.0"
__author__ = "AI-Writer Team"

__all__ = [
    'ComprehensiveSEOAnalyzer',
    'SEOAnalysisResult',
    'URLStructureAnalyzer',
    'MetaDataAnalyzer',
    'ContentAnalyzer',
    'TechnicalSEOAnalyzer',
    'PerformanceAnalyzer',
    'AccessibilityAnalyzer',
    'UserExperienceAnalyzer',
    'SecurityHeadersAnalyzer',
    'KeywordAnalyzer',
    'HTMLFetcher',
    'AIInsightGenerator',
    'SEOAnalysisService'
] 