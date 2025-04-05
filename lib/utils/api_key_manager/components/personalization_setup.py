"""Personalization setup component for the API key manager."""

import streamlit as st
from loguru import logger
import sys
import json
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
        <div class='setup-header'>
            <h2>✨ Personalization Setup</h2>
            <p>Configure your content generation preferences and writing style</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load main config
    main_config = load_main_config()
    
    # Create tabs for different personalization methods
    tab1, tab2 = st.tabs([
        "Manual Settings",
        "ALwrity Personalization"
    ])
    
    with tab1:
        st.markdown("### Manual Settings Configuration")
        
        # Add container for better width control
        st.markdown("""
            <div style='width: 100%; max-width: 100%; margin: 0; padding: 0;'>
        """, unsafe_allow_html=True)
        
        # Create two columns for settings and explanations (1:2 ratio)
        settings_col, info_col = st.columns([1, 2])
        
        with settings_col:
            st.markdown("""
                <div style='padding-right: 2rem;'>
            """, unsafe_allow_html=True)
            
            # Blog Content Characteristics
            st.markdown("#### Blog Content Characteristics")
            blog_settings = main_config.get("Blog Content Characteristics", {})
            
            blog_length = st.text_input(
                "Blog Length",
                value=blog_settings.get("Blog Length", "2000"),
                placeholder="e.g., 2000",
                help="Target word count for your blog posts"
            )
            
            blog_tone = st.selectbox(
                "Blog Tone",
                options=["Professional", "Casual", "Technical", "Conversational"],
                index=["Professional", "Casual", "Technical", "Conversational"].index(blog_settings.get("Blog Tone", "Professional")),
                help="The overall tone of your content"
            )
            
            blog_demographic = st.selectbox(
                "Target Demographic",
                options=["Professional", "General", "Technical", "Academic"],
                index=["Professional", "General", "Technical", "Academic"].index(blog_settings.get("Blog Demographic", "Professional")),
                help="Your primary audience demographic"
            )
            
            blog_type = st.selectbox(
                "Content Type",
                options=["Informational", "Educational", "Entertainment", "Technical"],
                index=["Informational", "Educational", "Entertainment", "Technical"].index(blog_settings.get("Blog Type", "Informational")),
                help="The primary type of content you create"
            )
            
            blog_language = st.selectbox(
                "Content Language",
                options=["English", "Spanish", "French", "German", "Other"],
                index=["English", "Spanish", "French", "German", "Other"].index(blog_settings.get("Blog Language", "English")),
                help="Primary language for your content"
            )
            
            blog_format = st.selectbox(
                "Output Format",
                options=["markdown", "html", "plain text"],
                index=["markdown", "html", "plain text"].index(blog_settings.get("Blog Output Format", "markdown")),
                help="Format of the generated content"
            )
            
            # Blog Images Details
            st.markdown("#### Blog Images")
            image_settings = main_config.get("Blog Images Details", {})
            
            image_model = st.selectbox(
                "Image Generation Model",
                options=["stable-diffusion", "dall-e", "midjourney"],
                index=["stable-diffusion", "dall-e", "midjourney"].index(image_settings.get("Image Generation Model", "stable-diffusion")),
                help="AI model for generating images"
            )
            
            num_images = st.number_input(
                "Number of Images",
                min_value=1,
                max_value=5,
                value=image_settings.get("Number of Blog Images", 1),
                help="Number of images to generate per blog post"
            )
            
            # LLM Options
            st.markdown("#### AI Generation Settings")
            llm_settings = main_config.get("LLM Options", {})
            
            gpt_provider = st.selectbox(
                "AI Provider",
                options=["google", "openai", "anthropic"],
                index=["google", "openai", "anthropic"].index(llm_settings.get("GPT Provider", "google")),
                help="Choose your preferred AI provider"
            )
            
            model = st.text_input(
                "Model",
                value=llm_settings.get("Model", "gemini-1.5-flash-latest"),
                placeholder="e.g., gemini-1.5-flash-latest",
                help="The specific AI model to use"
            )
            
            temperature = st.slider(
                "Creativity Level",
                min_value=0.0,
                max_value=1.0,
                value=float(llm_settings.get("Temperature", 0.7)),
                help="Higher values = more creative, lower values = more focused"
            )
            
            top_p = st.slider(
                "Output Diversity",
                min_value=0.0,
                max_value=1.0,
                value=float(llm_settings.get("Top-p", 0.9)),
                help="Controls diversity of generated content"
            )
            
            max_tokens = st.number_input(
                "Maximum Length",
                min_value=100,
                max_value=8000,
                value=int(llm_settings.get("Max Tokens", 4000)),
                help="Maximum length of generated content"
            )
            
            frequency_penalty = st.slider(
                "Frequency Penalty",
                min_value=-2.0,
                max_value=2.0,
                value=float(llm_settings.get("Frequency Penalty", 1.0)),
                help="Reduces repetition of the same words"
            )
            
            presence_penalty = st.slider(
                "Presence Penalty",
                min_value=-2.0,
                max_value=2.0,
                value=float(llm_settings.get("Presence Penalty", 1.0)),
                help="Encourages discussion of new topics"
            )
            
            # Search Engine Parameters
            st.markdown("#### Search Settings")
            search_settings = main_config.get("Search Engine Parameters", {})
            
            geo_location = st.text_input(
                "Geographic Location",
                value=search_settings.get("Geographic Location", "us"),
                placeholder="e.g., us, uk, ca",
                help="Target geographic location for search results"
            )
            
            search_language = st.selectbox(
                "Search Language",
                options=["en", "es", "fr", "de", "other"],
                index=["en", "es", "fr", "de", "other"].index(search_settings.get("Search Language", "en")),
                help="Language for search results"
            )
            
            num_results = st.number_input(
                "Number of Results",
                min_value=1,
                max_value=50,
                value=search_settings.get("Number of Results", 10),
                help="Number of search results to analyze"
            )
            
            time_range = st.selectbox(
                "Time Range",
                options=["anytime", "day", "week", "month", "year"],
                index=["anytime", "day", "week", "month", "year"].index(search_settings.get("Time Range", "anytime")),
                help="Time range for search results"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with info_col:
            st.markdown("""
                <div style='
                    padding-left: 2rem;
                    border-left: 2px solid #e0e0e0;
                    background-color: #f8f9fa;
                    border-radius: 0 8px 8px 0;
                    margin: -1rem 0;
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                '>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='padding: 0 1rem;'>
                    ### Understanding Your Settings
                    
                    #### Blog Content Settings
                    
                    **Blog Length**
                    - Determines the target word count for your posts
                    - Affects content depth and detail level
                    - Impacts reader engagement and SEO performance
                    - Recommended: 1500-2500 words for comprehensive coverage
                    
                    **Blog Tone**
                    - Professional: Formal, business-oriented, authoritative
                    - Casual: Friendly, conversational, approachable
                    - Technical: Detailed, precise, industry-specific
                    - Conversational: Engaging, relatable, personal
                    
                    **Target Demographic**
                    - Professional: Business audience, decision-makers
                    - General: Broad readership, general public
                    - Technical: Specialized audience, industry experts
                    - Academic: Research-focused, scholarly readers
                    
                    **Content Type**
                    - Informational: Facts, insights, and analysis
                    - Educational: Teaching, tutorials, how-to guides
                    - Entertainment: Engaging, fun, light content
                    - Technical: Detailed analysis, specifications
                    
                    **Content Language**
                    - Select your primary content language
                    - Affects grammar, idioms, and cultural context
                    - Impacts SEO and audience reach
                    
                    **Output Format**
                    - Markdown: Best for most platforms
                    - HTML: For web publishing
                    - Plain Text: For simple content
                    
                    #### Image Generation Settings
                    
                    **Image Generation Model**
                    - Stable Diffusion: Best for general content
                    - DALL-E: Great for creative concepts
                    - Midjourney: Excellent for artistic content
                    
                    **Number of Images**
                    - Consider your content type and platform
                    - More images = better engagement but higher cost
                    - Recommended: 1-2 images per post
                    
                    #### AI Generation Settings
                    
                    **AI Provider**
                    - Google: Balanced, reliable, cost-effective
                    - OpenAI: Creative, nuanced, versatile
                    - Anthropic: Precise, ethical, focused
                    
                    **Model Selection**
                    - Latest models offer best performance
                    - Specialized models for specific needs
                    - Consider cost vs. quality trade-offs
                    
                    **Creativity Level (Temperature)**
                    - 0.0: Focused, consistent, predictable
                    - 0.5: Balanced creativity and coherence
                    - 1.0: Maximum creativity, more varied
                    
                    **Output Diversity (Top-p)**
                    - Controls variety in word choices
                    - Higher values = more diverse vocabulary
                    - Lower values = more focused terminology
                    
                    **Maximum Length**
                    - Affects content completeness
                    - Consider platform limits
                    - Balance detail vs. readability
                    
                    **Frequency & Presence Penalties**
                    - Reduce repetition of words
                    - Encourage topic diversity
                    - Fine-tune content variety
                    
                    #### Search Settings
                    
                    **Geographic Location**
                    - Target specific regions
                    - Affects local SEO
                    - Influences content relevance
                    
                    **Search Language**
                    - Match your content language
                    - Affects result relevance
                    - Impacts SEO performance
                    
                    **Number of Results**
                    - More results = better analysis
                    - Consider processing time
                    - Balance quality vs. speed
                    
                    **Time Range**
                    - Anytime: All available content
                    - Recent: Latest information
                    - Historical: Past content
                    
                    ### Best Practices
                    
                    1. **Start Conservative**
                       - Begin with moderate settings
                       - Adjust based on results
                       - Monitor performance
                    
                    2. **Consider Your Audience**
                       - Match tone to reader expectations
                       - Adjust complexity appropriately
                       - Focus on value delivery
                    
                    3. **Optimize for Platform**
                       - Consider platform limitations
                       - Match format requirements
                       - Optimize for engagement
                    
                    4. **Regular Review**
                       - Monitor content performance
                       - Adjust settings as needed
                       - Stay updated with trends
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Close the container
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add some spacing before the save button
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        if st.button("Save Manual Settings", type="primary", use_container_width=True):
            # Update main config with new values
            main_config["Blog Content Characteristics"] = {
                "Blog Length": blog_length,
                "Blog Tone": blog_tone,
                "Blog Demographic": blog_demographic,
                "Blog Type": blog_type,
                "Blog Language": blog_language,
                "Blog Output Format": blog_format
            }
            
            main_config["Blog Images Details"] = {
                "Image Generation Model": image_model,
                "Number of Blog Images": num_images
            }
            
            main_config["LLM Options"] = {
                "GPT Provider": gpt_provider,
                "Model": model,
                "Temperature": temperature,
                "Top-p": top_p,
                "Max Tokens": max_tokens,
                "Frequency Penalty": frequency_penalty,
                "Presence Penalty": presence_penalty
            }
            
            main_config["Search Engine Parameters"] = {
                "Geographic Location": geo_location,
                "Search Language": search_language,
                "Number of Results": num_results,
                "Time Range": time_range
            }
            
            if save_main_config(main_config):
                st.success("✅ Your personalization settings have been saved successfully!")
            else:
                st.error("Unable to save settings. Please try again.")

    with tab2:
        st.markdown("#### ALwrity Personalization")
        
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
                st.markdown("""
                    <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
                        <p>No website URL? No problem! You can provide written samples of your content instead.</p>
                        <p>Share your best articles, blog posts, or any content that represents your writing style.</p>
                    </div>
                """, unsafe_allow_html=True)
                samples = st.text_area(
                    "Paste your content samples here",
                    help="Paste 2-3 samples of your best content. This helps ALwrity understand your writing style."
                )
                logger.debug(f"Sample text length: {len(samples) if samples else 0}")
            
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
                            # Initialize style analyzer
                            style_analyzer = StyleAnalyzer()
                            
                            # Analyze content samples
                            style_analysis = style_analyzer.analyze_content_style({"main_content": samples})
                            
                            if style_analysis.get('error'):
                                st.error(f"Style analysis failed: {style_analysis['error']}")
                            else:
                                # Display style analysis results
                                display_style_analysis(style_analysis)
                                
                        except Exception as e:
                            logger.error(f"Error analyzing samples: {str(e)}")
                            st.error(f"Analysis failed: {str(e)}")
                else:
                    st.warning("Please provide either a website URL or content samples")
        
        with col2:
            st.markdown(get_glass_container("""
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
            """))
            
            # API Configuration Form
            st.markdown(get_glass_container("""
                ### API Configuration
                
                Configure your API settings for optimal content generation.
            """))
            
            with st.form("ai_config_form"):
                # API Keys
                st.text_input("OpenAI API Key", type="password", key="openai_key")
                st.text_input("Google API Key", type="password", key="google_key")
                st.text_input("SerpAPI Key", type="password", key="serpapi_key")
                
                # Model Selection
                st.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4"], key="model")
                
                # Temperature
                st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, key="temperature")
                
                # Max Tokens
                st.number_input("Max Tokens", 100, 4000, 2000, 100, key="max_tokens")
                
                # Submit button
                submitted = st.form_submit_button("Save Configuration")
                
                if submitted:
                    # Create config directory if it doesn't exist
                    config_dir = Path("config")
                    config_dir.mkdir(exist_ok=True)
                    
                    # Save configuration
                    config = {
                        "openai_key": st.session_state.openai_key,
                        "google_key": st.session_state.google_key,
                        "serpapi_key": st.session_state.serpapi_key,
                        "model": st.session_state.model,
                        "temperature": st.session_state.temperature,
                        "max_tokens": st.session_state.max_tokens
                    }
                    
                    config_file = config_dir / "test_config.json"
                    with open(config_file, "w") as f:
                        json.dump(config, f, indent=4)
                    
                    st.success("Configuration saved successfully!")
    
    # Navigation buttons with correct arguments
    if render_navigation_buttons(4, 5, changes_made=True):
        st.session_state.current_step = 5
        st.rerun()
    
    return {"current_step": 4, "changes_made": True}