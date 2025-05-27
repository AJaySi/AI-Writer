"""
Content Gap Analysis Tool for Alwrity.
"""

from .ui import ContentGapAnalysisUI
from .main import ContentGapAnalysis
from .keyword_researcher import KeywordResearcher
from .competitor_analyzer import CompetitorAnalyzer
from .website_analyzer import WebsiteAnalyzer
from .recommendation_engine import RecommendationEngine
from .utils.ai_processor import AIProcessor

__all__ = [
    'ContentGapAnalysisUI',
    'ContentGapAnalysis',
    'KeywordResearcher',
    'CompetitorAnalyzer',
    'WebsiteAnalyzer',
    'RecommendationEngine',
    'AIProcessor'
]

def run_content_gap_analysis():
    """Run the Content Gap Analysis tool."""
    # Initialize the UI with proper configuration
    ui = ContentGapAnalysisUI()
    
    # Set up the page configuration
    st.set_page_config(
        page_title="Content Gap Analysis",
        page_icon="📊",
        layout="wide"
    )
    
    # Run the UI
    ui.run() 