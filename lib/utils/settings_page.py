import streamlit as st
from loguru import logger
import asyncio
from lib.web_crawlers.async_web_crawler import AsyncWebCrawlerService
from lib.personalization.style_analyzer import StyleAnalyzer
import sys

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/settings_page.log",
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
        st.markdown(writing_style_content, unsafe_allow_html=True)
        
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
        st.markdown(content_chars_content, unsafe_allow_html=True)
        
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
        st.markdown(target_audience_content, unsafe_allow_html=True)
        
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
        st.markdown(content_type_content, unsafe_allow_html=True)
        
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
        st.markdown(recommended_content, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error displaying style analysis: {str(e)}")
        st.error(f"Error displaying analysis results: {str(e)}")

def render_settings_page():
    """Renders the settings page with all configuration options in tabs"""
    st.title("🛠️ Settings & Configuration")
    
    # Create tabs for different settings categories
    tabs = st.tabs([
        "👷 Content",
        "🩻 Images",
        "🤖 LLM",
        "🕵️ Search",
        "🎨 AI Personalization"
    ])
    
    # Content Settings Tab
    with tabs[0]:
        st.header("Content Personalization")
        blog_length = st.text_input(
            "**Content Length (words)**",
            value="2000",
            key="settings_blog_length",
            help="Approximate word count for blogs. Note: Actual length may vary based on GPT provider and max token count."
        )

        blog_tone_options = ["Casual", "Professional", "How-to", "Beginner", "Research", "Programming", "Social Media", "Customize"]
        blog_tone = st.selectbox(
            "**Content Tone**",
            options=blog_tone_options,
            key="settings_blog_tone",
            help="Select the desired tone for the blog content."
        )

        if blog_tone == "Customize":
            custom_tone = st.text_input(
                "Enter the tone of your content",
                key="settings_custom_tone",
                help="Specify the tone of your content."
            )
            if custom_tone:
                blog_tone = custom_tone
            else:
                st.warning("Please specify the tone of your content.")

        blog_demographic_options = ["Professional", "Gen-Z", "Tech-savvy", "Student", "Digital Marketing", "Customize"]
        blog_demographic = st.selectbox(
            "**Target Audience**",
            options=blog_demographic_options,
            key="settings_blog_demographic",
            help="Select the primary audience for the blog content."
        )

        blog_type = st.selectbox(
            "**Content Type**",
            options=["Informational", "Commercial", "Company", "News", "Finance", "Competitor", "Programming", "Scholar"],
            key="settings_blog_type",
            help="Select the category that best describes the blog content."
        )

        blog_language = st.selectbox(
            "**Content Language**",
            options=["English", "Spanish", "German", "Chinese", "Arabic", "Nepali", "Hindi", "Hindustani", "Customize"],
            key="settings_blog_language",
            help="Select the language in which the blog will be written."
        )

        blog_output_format = st.selectbox(
            "**Content Output Format**",
            options=["markdown", "HTML", "plaintext"],
            key="settings_blog_output_format",
            help="Select the format for the blog output."
        )

    # Images Settings Tab
    with tabs[1]:
        st.header("Images Personalization")
        image_generation_model = st.selectbox(
            "**Image Generation Model**",
            options=["stable-diffusion", "dalle2", "dalle3"],
            key="settings_image_model",
            help="Select the model to generate images for the blog."
        )
        
        number_of_blog_images = st.number_input(
            "**Number of Blog Images**",
            value=1,
            min_value=1,
            max_value=10,
            key="settings_number_of_images",
            help="Specify the number of images to include in the blog."
        )

    # LLM Settings Tab
    with tabs[2]:
        st.header("LLM Personalization")
        gpt_provider = st.selectbox(
            "**GPT Provider**",
            options=["google", "openai", "minstral"],
            key="settings_gpt_provider",
            help="Select the provider for the GPT model."
        )

        model = st.text_input(
            "**Model**",
            value="gemini-1.5-flash-latest",
            key="settings_model",
            help="Specify the model version to use from the selected provider."
        )

        col1, col2 = st.columns(2)
        with col1:
            temperature = st.slider(
                "Temperature",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1,
                key="settings_temperature",
                help="Controls the creativity level of the generated text."
            )
            
            max_tokens = st.selectbox(
                "Max Tokens",
                options=[500, 1000, 2000, 4000, 16000, 32000, 64000],
                index=3,
                key="settings_max_tokens",
                help="Maximum length of the output sequence."
            )

        with col2:
            top_p = st.slider(
                "Top-p",
                min_value=0.0,
                max_value=1.0,
                value=0.9,
                step=0.1,
                key="settings_top_p",
                help="Controls diversity in text generation."
            )
            
            frequency_penalty = st.slider(
                "Frequency Penalty",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.1,
                key="settings_frequency_penalty",
                help="Reduces word repetition in output."
            )

    # Search Settings Tab
    with tabs[3]:
        st.header("Search Engine Personalization")
        geographic_location = st.selectbox(
            "**Geographic Location**",
            options=["us", "in", "fr", "cn"],
            key="settings_geographic_location",
            help="Select the geographic location for tailoring search results."
        )

        search_language = st.selectbox(
            "**Search Language**",
            options=["en", "zn-cn", "de", "hi"],
            key="settings_search_language",
            help="Select the language for the search results."
        )

        number_of_results = st.number_input(
            "**Number of Results**",
            value=10,
            min_value=1,
            max_value=20,
            key="settings_number_of_results",
            help="Specify the number of search results to retrieve."
        )

        time_range = st.selectbox(
            "**Time Range**",
            options=["anytime", "past day", "past week", "past month", "past year"],
            key="settings_time_range",
            help="Select the time range for filtering search results."
        )

        include_domains = st.text_input(
            "**Include Domains**",
            value="",
            key="settings_include_domains",
            help="List specific domains to include in search results (comma-separated)."
        )

        similar_url = st.text_input(
            "**Similar URL**",
            value="",
            key="settings_similar_url",
            help="Provide a URL to find similar results."
        )

    # AI Personalization Tab
    with tabs[4]:
        st.header("🎨 AI Style Analysis")
        st.markdown("""
            <div style='background-color: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <p>Enter a website URL or provide content samples to analyze your writing style and get personalized recommendations.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for the layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Website URL input
            st.markdown("### Website URL")
            url = st.text_input(
                "Enter your website URL",
                placeholder="https://example.com",
                key="settings_website_url",
                help="Provide your website URL to analyze your content style. Leave empty if you want to provide written samples instead."
            )
            
            # Alternative: Written samples
            if not url:
                st.markdown("### Written Samples")
                st.markdown("""
                    <div style='background-color: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                        <p>No website URL? No problem! You can provide written samples of your content instead.</p>
                        <p>Share your best articles, blog posts, or any content that represents your writing style.</p>
                    </div>
                """, unsafe_allow_html=True)
                samples = st.text_area(
                    "Paste your content samples here",
                    key="settings_content_samples",
                    help="Paste 2-3 samples of your best content. This helps ALwrity understand your writing style."
                )
            
            # ALwrity Style button
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
            if st.button("🎨 Analyze Style", use_container_width=True, key="settings_analyze_style"):
                if url:
                    with st.status("Starting style analysis...", expanded=True) as status:
                        try:
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
                                st.error("Failed to crawl the website. Please check the URL and try again.")
                        except Exception as e:
                            status.update(label="Analysis failed", state="error")
                            st.error(f"An error occurred during analysis: {str(e)}")
                elif samples:
                    with st.status("Starting style analysis...", expanded=True) as status:
                        try:
                            # Initialize style analyzer
                            status.update(label="Analyzing content style...", state="running")
                            style_analyzer = StyleAnalyzer()
                            
                            # Perform style analysis
                            style_analysis = style_analyzer.analyze_content_style({"main_content": samples})
                            
                            if style_analysis.get('error'):
                                status.update(label="Analysis failed", state="error")
                                st.error(f"Style analysis failed: {style_analysis['error']}")
                            else:
                                status.update(label="Analysis complete!", state="complete")
                                # Display style analysis results
                                display_style_analysis(style_analysis)
                        except Exception as e:
                            status.update(label="Analysis failed", state="error")
                            st.error(f"An error occurred during analysis: {str(e)}")
                else:
                    st.warning("Please provide either a website URL or content samples to analyze.")

    # Save Settings Button
    if st.button("💾 Save Settings", type="primary", use_container_width=True, key="settings_save_button"):
        # Save all settings to session state
        st.session_state.update({
            'blog_length': blog_length,
            'blog_tone': blog_tone,
            'blog_demographic': blog_demographic,
            'blog_type': blog_type,
            'blog_language': blog_language,
            'blog_output_format': blog_output_format,
            'image_generation_model': image_generation_model,
            'number_of_blog_images': number_of_blog_images,
            'gpt_provider': gpt_provider,
            'model': model,
            'temperature': temperature,
            'top_p': top_p,
            'max_tokens': max_tokens,
            'frequency_penalty': frequency_penalty,
            'geographic_location': geographic_location,
            'search_language': search_language,
            'number_of_results': number_of_results,
            'time_range': time_range,
            'include_domains': include_domains,
            'similar_url': similar_url
        })
        st.success("✅ Settings saved successfully!")