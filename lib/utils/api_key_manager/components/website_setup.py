"""Website setup component for the API key manager."""

import streamlit as st
from loguru import logger
from ...website_analyzer import analyze_website
from ...website_analyzer.analyzer import WebsiteAnalyzer
import asyncio
import sys
from typing import Dict, Any
from ..manager import APIKeyManager
from .base import render_navigation_buttons
import os

# Configure logger to output to both file and stdout
logger.remove()  # Remove default handler
logger.add(
    "logs/website_setup.log",
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

def render_website_setup(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the website setup step.
    
    Args:
        api_key_manager (APIKeyManager): The API key manager instance
        
    Returns:
        Dict[str, Any]: Current state
    """
    logger.info("[render_website_setup] Rendering website setup component")
    
    st.markdown("### Step 2: Enter Your Website URL for Analysis (Optional)")
    
    # Create two columns for input and results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Get existing website URL from environment or .env file
        existing_url = os.getenv('WEBSITE_URL', None)
        if not existing_url and os.path.exists('.env'):
            try:
                with open('.env', 'r') as f:
                    for line in f:
                        if line.strip().startswith('WEBSITE_URL='):
                            existing_url = line.strip().split('=')[1]
                            break
            except Exception as e:
                logger.error(f"[render_website_setup] Failed to read existing URL from .env: {str(e)}")
        
        # If existing_url is 'no_website_provided', set it to empty for better UX
        if existing_url == 'no_website_provided':
            existing_url = ''
        
        url = st.text_input(
            "Enter your website URL, if you own one",
            value=existing_url if existing_url else "",
            placeholder="https://example.com"
        )
        logger.info(f"[render_website_setup] URL input value: {url}")
        
        # Save URL to .env file
        try:
            # Check if WEBSITE_URL already exists in .env file
            website_url_exists = False
            env_lines = []
            
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    for line in f:
                        if line.strip().startswith('WEBSITE_URL='):
                            website_url_exists = True
                            # Replace the existing WEBSITE_URL line with the new value
                            if url:
                                env_lines.append(f"WEBSITE_URL={url}\n")
                            else:
                                env_lines.append("WEBSITE_URL=no_website_provided\n")
                        else:
                            env_lines.append(line)
            
            # If WEBSITE_URL doesn't exist, add it
            if not website_url_exists:
                if url:
                    env_lines.append(f"WEBSITE_URL={url}\n")
                else:
                    env_lines.append("WEBSITE_URL=no_website_provided\n")
            
            # Write all lines back to the .env file
            with open('.env', 'w') as f:
                f.writelines(env_lines)
            
            # Set environment variable
            if url:
                os.environ['WEBSITE_URL'] = url
                logger.info(f"[render_website_setup] Saved website URL to .env: {url}")
            else:
                os.environ['WEBSITE_URL'] = "no_website_provided"
                logger.info("[render_website_setup] Set default website URL: no_website_provided")
                
        except Exception as e:
            logger.error(f"[render_website_setup] Failed to save website URL: {str(e)}")
        
        analyze_type = st.radio(
            "Analysis Type",
            ["Basic Website Analysis", "Full Website Analysis with SEO"],
            horizontal=True,
            label_visibility="hidden",
            help="Choose between basic website analysis or comprehensive SEO analysis"
        )
        
        if st.button("Analyze Website"):
            if url:
                with st.spinner("Analyzing website..."):
                    try:
                        logger.info(f"[render_website_setup] Starting website analysis for URL: {url}")
                        
                        # Call the analyze_website function
                        results = analyze_website(url)
                        
                        # Replace the old SEO analysis code with the new analyzer
                        analyzer = WebsiteAnalyzer()
                        seo_results = analyzer.analyze_website(url)
                        if seo_results.get('success', False):
                            results['data']['seo_analysis'] = seo_results['data']['analysis']['seo_info']
                        else:
                            results['data']['seo_analysis'] = {
                                'error': seo_results.get('error', 'Unknown error in SEO analysis'),
                                'overall_score': 0,
                                'meta_tags': {},
                                'content': {},
                                'recommendations': []
                            }
                        
                        logger.debug(f"[render_website_setup] Analysis results received: {results.get('success', False)}")
                        
                        # Store results in session state
                        st.session_state.website_analysis = results
                        logger.info("[render_website_setup] Results stored in session state")
                        
                        if not results.get('success', False):
                            error_msg = results.get('error', 'Analysis failed')
                            logger.error(f"[render_website_setup] Analysis failed: {error_msg}")
                            st.error(error_msg)
                        else:
                            logger.info("[render_website_setup] Analysis completed successfully")
                            st.success("✅ Website analysis completed successfully!")
                    except Exception as e:
                        error_msg = f"Analysis failed: {str(e)}"
                        logger.error(f"[render_website_setup] {error_msg}")
                        st.error(error_msg)
            else:
                logger.warning("[render_website_setup] No URL provided")
                st.warning("Please enter a valid URL")
    
    with col2:
        # Check if we have analysis results
        if 'website_analysis' in st.session_state:
            results = st.session_state.website_analysis
            
            if results.get('success', False):
                data = results.get('data', {})
                analysis = data.get('analysis', {})
                
                # Create tabs for different sections
                if analyze_type == "Full Website Analysis with SEO":
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "Basic Metrics",
                        "Content Analysis",
                        "SEO Analysis",
                        "Technical SEO",
                        "Strategy"
                    ])
                else:
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "Basic Metrics",
                        "Content Analysis",
                        "Technical Info",
                        "Strategy"
                    ])
                
                with tab1:
                    st.markdown("##### Basic Metrics")
                    basic_info = analysis.get('basic_info', {})
                    st.write(f"Status Code: {basic_info.get('status_code')}")
                    st.write(f"Content Type: {basic_info.get('content_type')}")
                    st.write(f"Title: {basic_info.get('title')}")
                    st.write(f"Meta Description: {basic_info.get('meta_description')}")
                    
                    # SSL Info
                    ssl_info = analysis.get('ssl_info', {})
                    if ssl_info.get('has_ssl'):
                        st.success("SSL Certificate is valid")
                        st.write(f"Expiry: {ssl_info.get('expiry')}")
                    else:
                        st.error("No valid SSL certificate found")
                
                with tab2:
                    st.markdown("##### Content Analysis")
                    content_info = analysis.get('content_info', {})
                    
                    # Content Overview
                    st.markdown("###### 📊 Content Overview")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Word Count", content_info.get('word_count', 0))
                    with col2:
                        st.metric("Headings", content_info.get('heading_count', 0))
                    with col3:
                        st.metric("Images", content_info.get('image_count', 0))
                    with col4:
                        st.metric("Links", content_info.get('link_count', 0))
                
                if analyze_type == "Full Analysis with SEO":
                    with tab3:
                        st.markdown("##### SEO Analysis")
                        seo_data = data.get('seo_analysis', {})
                        
                        # Display SEO Score
                        seo_score = seo_data.get('overall_score', 0)
                        st.markdown(f"### SEO Score: {seo_score}/100")
                        st.progress(seo_score / 100)
                        
                        # Meta Tags Analysis
                        st.markdown("#### Meta Tags Analysis")
                        meta_analysis = seo_data.get('meta_tags', {})
                        for key, value in meta_analysis.items():
                            if isinstance(value, bool):
                                st.write(f"{'✅' if value else '❌'} {key.replace('_', ' ').title()}")
                            elif isinstance(value, dict):
                                st.write(f"**{key.replace('_', ' ').title()}:**")
                                st.write(f"Status: {value.get('status', 'N/A')}")
                                st.write(f"Value: {value.get('value', 'N/A')}")
                                if value.get('recommendation'):
                                    st.write(f"Recommendation: {value['recommendation']}")
                            else:
                                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                        
                        # Content Analysis
                        st.markdown("#### AI Content Analysis")
                        content_analysis = seo_data.get('content', {})
                        st.write(f"**Word Count:** {content_analysis.get('word_count', 0)}")
                        st.write(f"**Readability Score:** {content_analysis.get('readability_score', 0)}/100")
                        st.write(f"**Content Quality Score:** {content_analysis.get('content_quality_score', 0)}/100")
                        
                        # Recommendations
                        st.markdown("#### SEO Recommendations")
                        recommendations = seo_data.get('recommendations', [])
                        for rec in recommendations:
                            st.write(f"**{rec.get('priority', '').upper()} Priority - {rec.get('category', '')}**")
                            st.write(f"Issue: {rec.get('issue', '')}")
                            st.write(f"Recommendation: {rec.get('recommendation', '')}")
                            st.write(f"Impact: {rec.get('impact', '')}")
                            st.write("---")
                    
                    with tab4:
                        st.markdown("##### Technical SEO")
                        technical_seo = seo_data.get('technical_analysis', {})
                        
                        # Mobile Friendliness
                        st.markdown("#### Mobile Friendliness")
                        mobile_friendly = technical_seo.get('mobile_friendly', False)
                        st.write(f"{'✅' if mobile_friendly else '❌'} Mobile Friendly")
                        
                        # Page Speed
                        st.markdown("#### Page Speed")
                        speed_metrics = technical_seo.get('speed_metrics', {})
                        for metric, value in speed_metrics.items():
                            st.write(f"**{metric.replace('_', ' ').title()}:** {value}")
                        
                        # Technical Issues
                        st.markdown("#### Technical Issues")
                        issues = technical_seo.get('issues', [])
                        for issue in issues:
                            st.write(f"• {issue}")
                
                with tab4 if analyze_type == "Basic Website Analysis" else tab5:
                    st.markdown("##### Strategy Recommendations")
                    strategy_info = analysis.get('strategy', {})
                    
                    if strategy_info:
                        for category, recommendations in strategy_info.items():
                            st.markdown(f"###### {category.replace('_', ' ').title()}")
                            for rec in recommendations:
                                st.write(f"• {rec}")
                    else:
                        st.info("No strategy recommendations available")
            else:
                error_msg = results.get('error', 'Analysis failed')
                logger.error(f"[render_website_setup] Displaying error: {error_msg}")
                st.error(error_msg)
        else:
            logger.debug("[render_website_setup] No analysis results in session state")
            st.info("Enter a URL and click 'Analyze Website' to see results")
    
    # Navigation buttons
    if render_navigation_buttons(2, 5, True):
        # Move to next step (AI Research Setup)
        st.session_state.current_step = 3
        st.session_state.next_step = "ai_research_setup"
        st.rerun()
    
    return {"current_step": 2, "changes_made": True}