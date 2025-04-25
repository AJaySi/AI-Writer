"""Personalization setup component for the API key manager."""

import streamlit as st
from loguru import logger
import sys
import json
import os
from typing import Dict, Any
from ..manager import APIKeyManager
from ....web_crawlers.async_web_crawler import AsyncWebCrawlerService
from ....personalization.style_analyzer import StyleAnalyzer
from lib.utils.style_utils import (
    get_test_config_styles,
    get_glass_container,
    get_info_section,
    get_example_box,
    get_analysis_section,
    get_style_guide_html
)
from .base import render_navigation_buttons
from .alwrity_integrations import render_alwrity_integrations
import asyncio
import os
from pathlib import Path
import yaml

# Configure logger to output to both file and stdout
logger.remove()  # Remove default handler
logger.add(
    "logs/personalization_setup.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
)

def load_main_config() -> Dict[str, Any]:
    """Load the main configuration file."""
    config_path = os.path.join("lib", "workspace", "alwrity_config", "main_config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading main_config.json: {str(e)}")
        return {}

def save_main_config(config: Dict[str, Any]) -> bool:
    """Save the main configuration file."""
    try:
        config_path = os.path.join("lib", "workspace", "alwrity_config", "main_config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving main_config.json: {str(e)}")
        return False

def display_style_analysis(analysis_results: dict):
    """Display the style analysis results in a structured format."""
    try:
        # Writing Style Section
        writing_style = analysis_results.get("writing_style", {})
        writing_style_content = f"""
            <ul>
                <li><strong>Tone:</strong> {writing_style.get("tone", "N/A")}</li>
                <li><strong>Voice:</strong> {writing_style.get("voice", "N/A")}</li>
                <li><strong>Complexity:</strong> {writing_style.get("complexity", "N/A")}</li>
                <li><strong>Formality:</strong> {writing_style.get("formality", "N/A")}</li>
            </ul>
        """
        st.markdown(get_analysis_section("Writing Style", writing_style_content), unsafe_allow_html=True)
        
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

def render_personalization_setup(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the personalization setup step."""
    logger.info("[render_personalization_setup] Rendering personalization setup component")
    
    st.markdown("""
        # ✨ Personalization Setup
        Configure your content generation preferences and writing style
    """)
    
    # Main section selection using radio buttons
    setup_mode = st.radio(
        "Choose Setup Mode",
        ["Manual Settings", "ALwrity Personalization"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if setup_mode == "Manual Settings":
        # Create tabs for different settings categories
        tabs = st.tabs([
            "Blog Content Characteristics",
            "Blog Images",
            "AI Generation Settings",
            "Search Settings"
        ])
        
        # Blog Content Characteristics Tab
        with tabs[0]:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Blog Content Characteristics")
                
                blog_length = st.text_input(
                    "Blog Length",
                    value="2000",
                    placeholder="e.g., 2000",
                    help="Target word count for your blog posts"
                )
                
                blog_tone = st.selectbox(
                    "Blog Tone",
                    ["Professional", "Casual", "Technical", "Conversational"],
                    help="The overall tone of your content"
                )
                
                blog_demographic = st.selectbox(
                    "Target Demographic",
                    ["Professional", "General", "Technical", "Academic"],
                    help="Your primary audience demographic"
                )
                
                blog_type = st.selectbox(
                    "Content Type",
                    ["Informational", "Educational", "Entertainment", "Technical"],
                    help="The primary type of content you create"
                )
                
                blog_language = st.selectbox(
                    "Content Language",
                    ["English", "Spanish", "French", "German", "Other"],
                    help="Primary language for your content"
                )
                
                blog_format = st.selectbox(
                    "Output Format",
                    ["markdown", "html", "plain text"],
                    help="Format of the generated content"
                )
            
            with col2:
                st.markdown("### Blog Content Settings Guide")
                
                st.markdown("""
                    #### Blog Length
                    - Determines word count target
                    - Affects content depth
                    - Impacts SEO performance
                    
                    #### Blog Tone
                    - Professional: Business-oriented
                    - Casual: Friendly, approachable
                    - Technical: Detailed, precise
                    
                    #### Best Practices
                    - Match tone to audience
                    - Consider SEO requirements
                    - Maintain consistency
                """)
        
        # Blog Images Tab
        with tabs[1]:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Blog Images Settings")
                
                image_model = st.selectbox(
                    "Image Generation Model",
                    ["stable-diffusion", "dall-e", "midjourney"],
                    help="AI model for generating images"
                )
                
                num_images = st.number_input(
                    "Number of Images",
                    min_value=1,
                    max_value=5,
                    value=1,
                    help="Number of images per blog post"
                )
                
                image_style = st.selectbox(
                    "Image Style",
                    ["Realistic", "Artistic", "Professional", "Creative"],
                    help="Style of generated images"
                )
            
            with col2:
                st.markdown("### Image Generation Guide")
                
                st.markdown("""
                    #### Model Selection
                    - Stable Diffusion: Versatile, fast
                    - DALL-E: High quality, creative
                    - Midjourney: Artistic, detailed
                    
                    #### Best Practices
                    - Consider content type
                    - Balance quality vs. speed
                    - Optimize for platforms
                """)
        
        # AI Generation Settings Tab
        with tabs[2]:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### AI Generation Settings")
                
                gpt_provider = st.selectbox(
                    "AI Provider",
                    ["google", "openai", "anthropic"],
                    help="Choose your preferred AI provider"
                )
                
                model = st.text_input(
                    "Model",
                    value="gemini-1.5-flash-latest",
                    help="The specific AI model to use"
                )
                
                temperature = st.slider(
                    "Creativity Level",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.7,
                    help="Higher = more creative, lower = more focused"
                )
                
                max_tokens = st.number_input(
                    "Maximum Length",
                    min_value=100,
                    max_value=8000,
                    value=4000,
                    help="Maximum length of generated content"
                )
            
            with col2:
                st.markdown("### AI Settings Guide")
                
                st.markdown("""
                    #### Provider Selection
                    - Google: Balanced, reliable
                    - OpenAI: Creative, versatile
                    - Anthropic: Precise, ethical
                    
                    #### Temperature Guide
                    - 0.0-0.3: Focused, consistent
                    - 0.4-0.7: Balanced creativity
                    - 0.8-1.0: Highly creative
                """)
        
        # Search Settings Tab
        with tabs[3]:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Search Settings")
                
                geo_location = st.text_input(
                    "Geographic Location",
                    value="us",
                    help="Target geographic location for search"
                )
                
                search_language = st.selectbox(
                    "Search Language",
                    ["en", "es", "fr", "de", "other"],
                    help="Language for search results"
                )
                
                num_results = st.number_input(
                    "Number of Results",
                    min_value=1,
                    max_value=50,
                    value=10,
                    help="Number of search results to analyze"
                )
                
                time_range = st.selectbox(
                    "Time Range",
                    ["anytime", "day", "week", "month", "year"],
                    help="Time range for search results"
                )
            
            with col2:
                st.markdown("### Search Settings Guide")
                
                st.markdown("""
                    #### Location & Language
                    - Affects result relevance
                    - Impacts local SEO
                    - Consider target market
                    
                    #### Search Optimization
                    - Balance quantity vs. quality
                    - Consider time sensitivity
                    - Optimize for accuracy
                """)
        
        # Save button for manual settings
        if st.button("Save Manual Settings", type="primary", use_container_width=True):
            try:
                # Save to main_config.json
                config = {
                    "Blog Content Characteristics": {
                        "Blog Length": blog_length,
                        "Blog Tone": blog_tone,
                        "Blog Demographic": blog_demographic,
                        "Blog Type": blog_type,
                        "Blog Language": blog_language,
                        "Blog Output Format": blog_format
                    },
                    "Blog Images Details": {
                        "Image Generation Model": image_model,
                        "Number of Blog Images": num_images,
                        "Image Style": image_style
                    },
                    "LLM Options": {
                        "GPT Provider": gpt_provider,
                        "Model": model,
                        "Temperature": temperature,
                        "Max Tokens": max_tokens
                    },
                    "Search Engine Parameters": {
                        "Geographic Location": geo_location,
                        "Search Language": search_language,
                        "Number of Results": num_results,
                        "Time Range": time_range
                    }
                }
                
                if save_main_config(config):
                    try:
                        # Read existing .env file content
                        env_lines = []
                        if os.path.exists('.env'):
                            with open('.env', 'r') as f:
                                env_lines = f.readlines()
                        
                        # Remove any existing PERSONALIZATION_DONE entries
                        env_lines = [line for line in env_lines if not line.startswith('PERSONALIZATION_DONE=')]
                        
                        # Add new PERSONALIZATION_DONE entry
                        env_lines.append("PERSONALIZATION_DONE=True\n")
                        
                        # Write back to .env file
                        with open('.env', 'w') as f:
                            f.writelines(env_lines)
                        
                        # Update environment variable and session state
                        os.environ['PERSONALIZATION_DONE'] = "True"
                        st.session_state['personalization_saved'] = True
                        logger.info("Successfully set PERSONALIZATION_DONE=True in .env and environment")
                        st.success("✅ Your personalization settings have been saved successfully!")
                    except Exception as e:
                        logger.error(f"Error updating PERSONALIZATION_DONE: {str(e)}")
                        st.error("Settings saved but failed to update environment. Please try again.")
                else:
                    st.error("Unable to save settings. Please try again.")
            except Exception as e:
                logger.error(f"Error saving settings: {str(e)}")
                st.error(f"Failed to save settings: {str(e)}")
    
    else:  # ALwrity Personalization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Website URL")
            url = st.text_input(
                "Enter your website URL",
                placeholder="https://example.com",
                help="Provide your website URL to analyze your content style"
            )
            
            if not url:
                st.markdown("### Written Samples")
                st.info("No website URL? No problem! Provide written samples instead.")
                samples = st.text_area(
                    "Paste your content samples here",
                    help="Paste 2-3 samples of your best content"
                )
            
            if st.button("🎨 Analyze Style", use_container_width=True):
                # Existing style analysis code...
                pass
        
        with col2:
            st.markdown("### How ALwrity Discovers Your Style")
            
            st.markdown("""
                #### AI-Powered Analysis
                ALwrity analyzes your content to understand:
                - Writing tone and voice
                - Content structure
                - Target audience
                - Engagement style
                
                #### Personalized Recommendations
                We provide:
                - Writing guidelines
                - Content templates
                - Style recommendations
                - Audience insights
            """)
    
    # Navigation buttons
    if render_navigation_buttons(4, 6, changes_made=True):
        try:
            # If user hasn't saved settings manually, mark as skipped
            if 'personalization_saved' not in st.session_state or not st.session_state.get('personalization_saved'):
                # Read existing .env file content
                env_lines = []
                if os.path.exists('.env'):
                    with open('.env', 'r') as f:
                        env_lines = f.readlines()
                
                # Remove any existing PERSONALIZATION_DONE entries
                env_lines = [line for line in env_lines if not line.startswith('PERSONALIZATION_DONE=')]
                
                # Add PERSONALIZATION_DONE=False since user skipped
                env_lines.append("PERSONALIZATION_DONE=False\n")
                
                # Write back to .env file
                with open('.env', 'w') as f:
                    f.writelines(env_lines)
                
                # Update environment variable
                os.environ['PERSONALIZATION_DONE'] = "False"
                logger.info("User skipped personalization. Set PERSONALIZATION_DONE=False")
        except Exception as e:
            logger.error(f"Error updating PERSONALIZATION_DONE on skip: {str(e)}")
            st.error("Error updating environment. You may need to configure personalization later.")
        
        st.session_state.current_step = 5
        st.rerun()
    
    return {"current_step": 4, "changes_made": True}