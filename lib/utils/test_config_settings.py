"""Test configuration settings page for ALwrity."""

import streamlit as st
from loguru import logger
import asyncio
from lib.web_crawlers.async_web_crawler import AsyncWebCrawlerService
from pages.style_utils import (
    get_test_config_styles,
    get_glass_container,
    get_info_section,
    get_example_box,
    get_analysis_section,
    get_style_guide_html
)
import sys
from lib.personalization.style_analyzer import StyleAnalyzer

# Set page config - must be the first Streamlit command
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

import yaml
from pathlib import Path
import os
from loguru import logger
from lib.utils.read_main_config_params import get_personalization_settings
from lib.web_crawlers.crawl4ai_web_crawler import analyze_style

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/test_config_settings.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
)

# Apply CSS styles
st.markdown(get_test_config_styles(), unsafe_allow_html=True)

def load_website_url():
    """Load website URL from config file."""
    try:
        logger.debug("Loading website URL from config file")
        config_path = Path(os.environ["ALWRITY_CONFIG"])
        config = yaml.safe_load(config_path.read_text())
        url = config.get('website', {}).get('url', '')
        logger.info(f"Loaded website URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Error loading website URL: {str(e)}", exc_info=True)
        return ''

def display_style_analysis(analysis_results: dict):
    """Display the style analysis results in a structured format."""
    try:
        # Writing Style Section
        st.markdown("### 🎨 Writing Style Analysis")
        writing_style = analysis_results.get("writing_style", {})
        writing_style_content = f"""
            <ul>
                <li><strong>Tone:</strong> {writing_style.get("tone", "N/A")}</li>
                <li><strong>Voice:</strong> {writing_style.get("voice", "N/A")}</li>
                <li><strong>Complexity:</strong> {writing_style.get("complexity", "N/A")}</li>
                <li><strong>Engagement Level:</strong> {writing_style.get("engagement_level", "N/A")}</li>
            </ul>
        """
        st.markdown(get_analysis_section("Writing Style", writing_style_content), unsafe_allow_html=True)
        
        # Content Characteristics Section
        content_chars = analysis_results.get("content_characteristics", {})
        content_chars_content = f"""
            <ul>
                <li><strong>Sentence Structure:</strong> {content_chars.get("sentence_structure", "N/A")}</li>
                <li><strong>Vocabulary Level:</strong> {content_chars.get("vocabulary_level", "N/A")}</li>
                <li><strong>Paragraph Organization:</strong> {content_chars.get("paragraph_organization", "N/A")}</li>
                <li><strong>Content Flow:</strong> {content_chars.get("content_flow", "N/A")}</li>
            </ul>
        """
        st.markdown(get_analysis_section("Content Characteristics", content_chars_content), unsafe_allow_html=True)
        
        # Target Audience Section
        target_audience = analysis_results.get("target_audience", {})
        target_audience_content = f"""
            <ul>
                <li><strong>Demographics:</strong> {', '.join(target_audience.get("demographics", ["N/A"]))}</li>
                <li><strong>Expertise Level:</strong> {target_audience.get("expertise_level", "N/A")}</li>
                <li><strong>Industry Focus:</strong> {target_audience.get("industry_focus", "N/A")}</li>
                <li><strong>Geographic Focus:</strong> {target_audience.get("geographic_focus", "N/A")}</li>
            </ul>
        """
        st.markdown(get_analysis_section("Target Audience", target_audience_content), unsafe_allow_html=True)
        
        # Content Type Section
        content_type = analysis_results.get("content_type", {})
        content_type_content = f"""
            <ul>
                <li><strong>Primary Type:</strong> {content_type.get("primary_type", "N/A")}</li>
                <li><strong>Secondary Types:</strong> {', '.join(content_type.get("secondary_types", ["N/A"]))}</li>
                <li><strong>Purpose:</strong> {content_type.get("purpose", "N/A")}</li>
                <li><strong>Call to Action:</strong> {content_type.get("call_to_action", "N/A")}</li>
            </ul>
        """
        st.markdown(get_analysis_section("Content Type", content_type_content), unsafe_allow_html=True)
        
        # Recommended Settings Section
        recommended = analysis_results.get("recommended_settings", {})
        recommended_content = f"""
            <ul>
                <li><strong>Writing Tone:</strong> {recommended.get("writing_tone", "N/A")}</li>
                <li><strong>Target Audience:</strong> {recommended.get("target_audience", "N/A")}</li>
                <li><strong>Content Type:</strong> {recommended.get("content_type", "N/A")}</li>
                <li><strong>Creativity Level:</strong> {recommended.get("creativity_level", "N/A")}</li>
                <li><strong>Geographic Location:</strong> {recommended.get("geographic_location", "N/A")}</li>
            </ul>
        """
        st.markdown(get_analysis_section("Recommended Settings", recommended_content), unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error displaying style analysis: {str(e)}")
        st.error(f"Error displaying analysis results: {str(e)}")

def render_test_config_settings():
    """Render the test configuration settings page."""
    try:
        logger.info("Starting to render test configuration settings")
        
        # Add back button at the top
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("← Back to Personalization Setup"):
                logger.info("User clicked back to personalization setup")
                # Set session state for navigation
                st.session_state.current_step = 4
                st.session_state.next_step = "personalization_setup"
                # Navigate back to the main page where personalization setup is rendered
                st.switch_page("alwrity.py")
        
        # Title and description
        st.title("🎨 Find Your Style with ALwrity")
        st.markdown(get_glass_container(
            "<p>Enter a website URL or provide content samples to analyze your writing style and get personalized recommendations.</p>"
        ), unsafe_allow_html=True)
        
        # Create two columns for the layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Website URL input
            st.markdown("### Website URL")
            url = st.text_input(
                "Enter your website URL",
                placeholder="https://example.com",
                help="Provide your website URL to analyze your content style. Leave empty if you want to provide written samples instead."
            )
            logger.debug(f"Website URL input value: {url}")
            
            # Alternative: Written samples
            if not url:
                st.markdown("### Written Samples")
                st.markdown(get_info_section("""
                    <p>No website URL? No problem! You can provide written samples of your content instead.</p>
                    <p>Share your best articles, blog posts, or any content that represents your writing style.</p>
                """), unsafe_allow_html=True)
                samples = st.text_area(
                    "Paste your content samples here",
                    help="Paste 2-3 samples of your best content. This helps ALwrity understand your writing style."
                )
                logger.debug(f"Sample text length: {len(samples) if samples else 0}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ALwrity Style button
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
            if st.button("🎨 ALwrity Style", use_container_width=True):
                if url:
                    with st.status("Starting style analysis...", expanded=True) as status:
                        try:
                            logger.info(f"Starting style analysis for URL: {url}")
                            
                            # Step 1: Initialize crawler
                            status.update(label="Step 1/4: Initializing web crawler...", state="running")
                            crawler_service = AsyncWebCrawlerService()
                            
                            # Step 2: Crawl website
                            status.update(label="Step 2/4: Crawling website content...", state="running")
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            result = loop.run_until_complete(crawler_service.crawl_website(url))
                            loop.close()
                            
                            if result.get('success', False):
                                content = result.get('content', {})
                                
                                # Step 3: Initialize style analyzer
                                status.update(label="Step 3/4: Analyzing content style...", state="running")
                                style_analyzer = StyleAnalyzer()
                                
                                # Step 4: Perform style analysis
                                status.update(label="Step 4/4: Generating style recommendations...", state="running")
                                style_analysis = style_analyzer.analyze_content_style(content)
                                
                                if style_analysis.get('error'):
                                    status.update(label="Analysis failed", state="error")
                                    st.error(f"Style analysis failed: {style_analysis['error']}")
                                else:
                                    status.update(label="Analysis complete!", state="complete")
                                    # Display style analysis results
                                    display_style_analysis(style_analysis)
                                    
                                    # Display original content in tabs
                                    tab1, tab2, tab3 = st.tabs(["Content", "Metadata", "Links"])
                                    
                                    with tab1:
                                        st.markdown("### Main Content")
                                        st.markdown(content.get('main_content', 'No content found'))
                                        
                                    with tab2:
                                        st.markdown("### Metadata")
                                        st.markdown(f"""
                                            **Title:** {content.get('title', 'No title found')}
                                            
                                            **Description:** {content.get('description', 'No description found')}
                                            
                                            **Meta Tags:**
                                            {content.get('meta_tags', {})}
                                        """)
                                        
                                    with tab3:
                                        st.markdown("### Links")
                                        for link in content.get('links', []):
                                            st.markdown(f"- [{link.get('text', '')}]({link.get('href', '')})")
                                            
                            else:
                                status.update(label="Crawling failed", state="error")
                                st.error(f"Failed to analyze website: {result.get('error', 'Unknown error')}")
                                
                        except Exception as e:
                            logger.error(f"Error during style analysis: {str(e)}")
                            st.error(f"Analysis failed: {str(e)}")
                elif samples:
                    with st.spinner("Analyzing content samples..."):
                        try:
                            # TODO: Implement sample text analysis
                            st.info("Sample text analysis coming soon!")
                        except Exception as e:
                            logger.error(f"Error analyzing samples: {str(e)}")
                            st.error(f"Analysis failed: {str(e)}")
                else:
                    st.warning("Please provide either a website URL or content samples")
        
        with col2:
            st.markdown("""
                ### How ALwrity Discovers Your Style
                
                **AI-Powered Style Analysis**
                
                ALwrity AI analyzes your existing content to understand your unique writing style and preferences. This helps us generate content that matches your voice perfectly.
                
                **Step 1: Content Analysis**
                
                We'll analyze your website content or written samples to understand:
                
                - Writing tone and voice
                - Vocabulary and language style
                - Content structure and formatting
                - Target audience and engagement style
                
                **Step 2: Style Recommendations**
                
                Based on the analysis, we'll provide:
                
                - Personalized writing guidelines
                - Content structure templates
                - Tone and voice recommendations
                - Audience engagement strategies
                
                **Step 3: Content Generation**
                
                Finally, we'll use these insights to:
                
                - Generate content that matches your style
                - Maintain consistency across all content
                - Optimize for your target audience
                - Ensure brand voice alignment
            """)
                
    except Exception as e:
        logger.error(f"Error in render_test_config_settings: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting test config settings page")
    render_test_config_settings()
    logger.info("Test config settings page rendered successfully") 