"""
Technical SEO Crawler Package.

This package provides comprehensive technical SEO analysis capabilities
with advertools integration and AI-powered recommendations.

Components:
- TechnicalSEOCrawler: Core crawler with technical analysis
- TechnicalSEOCrawlerUI: Streamlit interface for the crawler
"""

from .crawler import TechnicalSEOCrawler
from .ui import TechnicalSEOCrawlerUI, render_technical_seo_crawler

__version__ = "1.0.0"
__author__ = "ALwrity"

__all__ = [
    'TechnicalSEOCrawler',
    'TechnicalSEOCrawlerUI', 
    'render_technical_seo_crawler'
] 