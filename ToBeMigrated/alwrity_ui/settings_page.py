import streamlit as st
from loguru import logger
import asyncio
from lib.web_crawlers.async_web_crawler import AsyncWebCrawlerService
from lib.personalization.style_analyzer import StyleAnalyzer
from lib.alwrity_ui.dashboard_styles import apply_dashboard_style, render_dashboard_header
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
    """Display the style analysis results in a structured format with premium styling."""
    try:
        # Writing Style Section
        st.markdown("""
            <div class="analysis-section">
                <div class="section-icon">🎨</div>
                <h3>Writing Style Analysis</h3>
            </div>
        """, unsafe_allow_html=True)
        
        writing_style = analysis_results.get("writing_style", {})
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="analysis-card">
                    <div class="metric-item">
                        <span class="metric-label">Tone:</span>
                        <span class="metric-value">{writing_style.get("tone", "N/A")}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Voice:</span>
                        <span class="metric-value">{writing_style.get("voice", "N/A")}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="analysis-card">
                    <div class="metric-item">
                        <span class="metric-label">Complexity:</span>
                        <span class="metric-value">{writing_style.get("complexity", "N/A")}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Engagement:</span>
                        <span class="metric-value">{writing_style.get("engagement_level", "N/A")}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Content Characteristics Section
        st.markdown("""
            <div class="analysis-section">
                <div class="section-icon">📊</div>
                <h3>Content Characteristics</h3>
            </div>
        """, unsafe_allow_html=True)
        
        content_chars = analysis_results.get("content_characteristics", {})
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="analysis-card">
                    <div class="metric-item">
                        <span class="metric-label">Sentence Structure:</span>
                        <span class="metric-value">{content_chars.get("sentence_structure", "N/A")}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Vocabulary Level:</span>
                        <span class="metric-value">{content_chars.get("vocabulary_level", "N/A")}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="analysis-card">
                    <div class="metric-item">
                        <span class="metric-label">Organization:</span>
                        <span class="metric-value">{content_chars.get("paragraph_organization", "N/A")}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Content Flow:</span>
                        <span class="metric-value">{content_chars.get("content_flow", "N/A")}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Target Audience Section
        st.markdown("""
            <div class="analysis-section">
                <div class="section-icon">🎯</div>
                <h3>Target Audience</h3>
            </div>
        """, unsafe_allow_html=True)
        
        target_audience = analysis_results.get("target_audience", {})
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="analysis-card">
                    <div class="metric-item">
                        <span class="metric-label">Demographics:</span>
                        <span class="metric-value">{', '.join(target_audience.get("demographics", ["N/A"]))}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Expertise Level:</span>
                        <span class="metric-value">{target_audience.get("expertise_level", "N/A")}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="analysis-card">
                    <div class="metric-item">
                        <span class="metric-label">Industry Focus:</span>
                        <span class="metric-value">{target_audience.get("industry_focus", "N/A")}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Geographic Focus:</span>
                        <span class="metric-value">{target_audience.get("geographic_focus", "N/A")}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Recommended Settings Section
        st.markdown("""
            <div class="analysis-section">
                <div class="section-icon">⚙️</div>
                <h3>Recommended Settings</h3>
            </div>
        """, unsafe_allow_html=True)
        
        recommended = analysis_results.get("recommended_settings", {})
        st.markdown(f"""
            <div class="recommendations-grid">
                <div class="recommendation-card">
                    <div class="rec-icon">🎭</div>
                    <div class="rec-label">Writing Tone</div>
                    <div class="rec-value">{recommended.get("writing_tone", "N/A")}</div>
                </div>
                <div class="recommendation-card">
                    <div class="rec-icon">👥</div>
                    <div class="rec-label">Target Audience</div>
                    <div class="rec-value">{recommended.get("target_audience", "N/A")}</div>
                </div>
                <div class="recommendation-card">
                    <div class="rec-icon">📝</div>
                    <div class="rec-label">Content Type</div>
                    <div class="rec-value">{recommended.get("content_type", "N/A")}</div>
                </div>
                <div class="recommendation-card">
                    <div class="rec-icon">🎨</div>
                    <div class="rec-label">Creativity Level</div>
                    <div class="rec-value">{recommended.get("creativity_level", "N/A")}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error displaying style analysis: {str(e)}")
        st.error(f"Error displaying analysis results: {str(e)}")

def render_settings_page():
    """Renders the settings page with premium glassmorphic design and all configuration options in tabs"""
    
    # Apply common dashboard styling
    apply_dashboard_style()
    
    # Add settings-specific CSS for tabs and form elements
    st.markdown("""
        <style>
            /* Settings-specific overrides and additions */
            .main .block-container {
                padding: 1rem 1.5rem 1.5rem 1.5rem !important;
                margin: 1rem auto !important;
            }

            .element-container {
                margin-bottom: 0.3rem !important;
            }

            .stMarkdown {
                margin: 0 !important;
                padding: 0 !important;
                margin-bottom: 0.3rem !important;
            }

            /* Enhanced tab styling for settings */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.5rem !important;
                background: rgba(255, 255, 255, 0.35) !important;
                backdrop-filter: blur(30px) !important;
                border-radius: 18px !important;
                padding: 0.8rem !important;
                border: 3px solid rgba(255, 255, 255, 0.4) !important;
                margin-bottom: 1.5rem !important;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.25),
                    inset 0 3px 0 rgba(255, 255, 255, 0.5) !important;
            }

            .stTabs [data-baseweb="tab"] {
                background: rgba(255, 255, 255, 0.3) !important;
                backdrop-filter: blur(25px) !important;
                border-radius: 14px !important;
                color: #ffffff !important;
                border: 2px solid rgba(255, 255, 255, 0.35) !important;
                padding: 1rem 2rem !important;
                font-weight: 800 !important;
                font-size: 1.05rem !important;
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
                margin: 0 !important;
                min-height: 50px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                text-shadow: 0 3px 6px rgba(0, 0, 0, 0.6) !important;
                box-shadow: 
                    0 8px 25px rgba(0, 0, 0, 0.2),
                    inset 0 2px 0 rgba(255, 255, 255, 0.4) !important;
                font-family: 'Inter', sans-serif !important;
            }

            .stTabs [data-baseweb="tab"]:hover {
                background: rgba(255, 255, 255, 0.4) !important;
                backdrop-filter: blur(30px) !important;
                color: #ffffff !important;
                border-color: rgba(255, 255, 255, 0.5) !important;
                transform: translateY(-2px) !important;
                box-shadow: 
                    0 15px 35px rgba(0, 0, 0, 0.3),
                    inset 0 3px 0 rgba(255, 255, 255, 0.5) !important;
            }

            .stTabs [aria-selected="true"] {
                background: rgba(255, 255, 255, 0.5) !important;
                backdrop-filter: blur(35px) !important;
                color: #ffffff !important;
                border-color: rgba(255, 255, 255, 0.6) !important;
                box-shadow: 
                    0 15px 35px rgba(0, 0, 0, 0.3),
                    inset 0 3px 0 rgba(255, 255, 255, 0.6),
                    0 0 0 2px rgba(255, 255, 255, 0.3) !important;
                transform: translateY(-1px) !important;
                font-weight: 900 !important;
                text-shadow: 0 3px 8px rgba(0, 0, 0, 0.7) !important;
            }

            /* Settings sections */
            .settings-section {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(25px);
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                border: 2px solid rgba(255, 255, 255, 0.25);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
                position: relative;
                overflow: hidden;
            }

            .settings-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
                opacity: 0.9;
            }

            .settings-section h2 {
                color: #ffffff !important;
                font-size: 1.6em !important;
                font-weight: 800 !important;
                margin-bottom: 1.2rem !important;
                margin-top: 0 !important;
                text-shadow: 0 3px 12px rgba(0, 0, 0, 0.5) !important;
                display: flex;
                align-items: center;
                gap: 0.6rem;
                letter-spacing: -0.01em;
                padding-bottom: 0.8rem;
                border-bottom: 2px solid rgba(255, 255, 255, 0.2);
                font-family: 'Inter', sans-serif !important;
            }

            /* Form elements with maximum visibility */
            .stSelectbox > div > div,
            .stSelectbox div[data-baseweb="select"] > div {
                background: rgba(255, 255, 255, 0.35) !important;
                backdrop-filter: blur(30px) !important;
                border: 3px solid rgba(255, 255, 255, 0.5) !important;
                border-radius: 12px !important;
                color: #ffffff !important;
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.2),
                    inset 0 2px 0 rgba(255, 255, 255, 0.4) !important;
                min-height: 45px !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
                font-family: 'Inter', sans-serif !important;
            }

            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stNumberInput > div > div > input {
                background: rgba(255, 255, 255, 0.35) !important;
                backdrop-filter: blur(30px) !important;
                border: 3px solid rgba(255, 255, 255, 0.5) !important;
                border-radius: 12px !important;
                color: #ffffff !important;
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.2),
                    inset 0 2px 0 rgba(255, 255, 255, 0.4) !important;
                min-height: 45px !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
                font-family: 'Inter', sans-serif !important;
            }

            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus,
            .stNumberInput > div > div > input:focus {
                border-color: rgba(255, 255, 255, 0.7) !important;
                box-shadow: 
                    0 0 0 4px rgba(255, 255, 255, 0.4),
                    0 15px 35px rgba(0, 0, 0, 0.25) !important;
                background: rgba(255, 255, 255, 0.4) !important;
            }

            .stTextInput > div > div > input::placeholder {
                color: rgba(255, 255, 255, 0.8) !important;
                font-weight: 600 !important;
            }

            /* Enhanced labels */
            .stMarkdown p, .stSelectbox label, .stTextInput label, .stTextArea label, .stSlider label, .stNumberInput label {
                color: #ffffff !important;
                font-weight: 800 !important;
                text-shadow: 
                    0 2px 6px rgba(0, 0, 0, 0.5),
                    0 1px 3px rgba(0, 0, 0, 0.7) !important;
                font-size: 1.05rem !important;
                margin-bottom: 0.4rem !important;
                font-family: 'Inter', sans-serif !important;
                letter-spacing: -0.01em;
            }

            /* Slider styling */
            .stSlider > div > div > div {
                background: rgba(255, 255, 255, 0.5) !important;
                border-radius: 8px !important;
                height: 8px !important;
            }

            .stSlider > div > div > div > div {
                background: #ffffff !important;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
                width: 20px !important;
                height: 20px !important;
            }

            /* Analysis results styling */
            .analysis-section {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin: 2rem 0 1rem 0;
                padding: 1rem;
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(15px);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }

            .section-icon {
                font-size: 1.5em;
                color: #ffffff;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            }

            .analysis-section h3 {
                color: #ffffff;
                font-size: 1.2em;
                font-weight: 600;
                margin: 0;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            }

            .analysis-card {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(15px);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.15);
                margin-bottom: 1rem;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }

            .metric-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.8rem;
                padding-bottom: 0.8rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }

            .metric-item:last-child {
                margin-bottom: 0;
                padding-bottom: 0;
                border-bottom: none;
            }

            .metric-label {
                color: rgba(255, 255, 255, 0.8);
                font-weight: 500;
                font-size: 0.9em;
            }

            .metric-value {
                color: #ffffff;
                font-weight: 600;
                font-size: 0.9em;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
            }

            .recommendations-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
                margin-top: 1rem;
            }

            .recommendation-card {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(15px);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.15);
                text-align: center;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }

            .recommendation-card:hover {
                transform: translateY(-2px);
                background: rgba(255, 255, 255, 0.12);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            }

            .rec-icon {
                font-size: 2em;
                margin-bottom: 0.5rem;
                color: #ffffff;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            }

            .rec-label {
                color: rgba(255, 255, 255, 0.8);
                font-size: 0.9em;
                font-weight: 500;
                margin-bottom: 0.5rem;
            }

            .rec-value {
                color: #ffffff;
                font-weight: 600;
                font-size: 1em;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
            }

            /* Status messages */
            .stSuccess {
                background: rgba(46, 160, 67, 0.2) !important;
                backdrop-filter: blur(15px) !important;
                border: 1px solid rgba(46, 160, 67, 0.3) !important;
                border-radius: 12px !important;
                color: #ffffff !important;
            }

            .stError {
                background: rgba(255, 75, 75, 0.2) !important;
                backdrop-filter: blur(15px) !important;
                border: 1px solid rgba(255, 75, 75, 0.3) !important;
                border-radius: 12px !important;
                color: #ffffff !important;
            }

            .stWarning {
                background: rgba(255, 196, 9, 0.2) !important;
                backdrop-filter: blur(15px) !important;
                border: 1px solid rgba(255, 196, 9, 0.3) !important;
                border-radius: 12px !important;
                color: #ffffff !important;
            }

            .stStatus {
                background: rgba(255, 255, 255, 0.08) !important;
                backdrop-filter: blur(15px) !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                border-radius: 12px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Use the common dashboard header
    render_dashboard_header(
        "⚙️ Settings & Configuration",
        "Customize your AI experience with precision controls for content generation, personalization, and optimization. Fine-tune every aspect to match your unique requirements and style."
    )

    # Create tabs for different settings categories with premium styling
    tabs = st.tabs([
        "📝 Content",
        "🖼️ Images", 
        "🤖 LLM",
        "🔍 Search",
        "🎨 AI Personalization"
    ])
    
    # Content Settings Tab
    with tabs[0]:
        st.markdown("""
            <div class="settings-section">
                <h2>📝 Content Personalization</h2>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
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

            # Initialize custom_tone variable
            custom_tone = ""
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

        with col2:
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
        st.markdown("""
            <div class="settings-section">
                <h2>🖼️ Images Personalization</h2>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            image_generation_model = st.selectbox(
                "**Image Generation Model**",
                options=["stable-diffusion", "dalle2", "dalle3"],
                key="settings_image_model",
                help="Select the model to generate images for the blog."
            )
        
        with col2:
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
        st.markdown("""
            <div class="settings-section">
                <h2>🤖 LLM Personalization</h2>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
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

            temperature = st.slider(
                "**Temperature**",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1,
                key="settings_temperature",
                help="Controls the creativity level of the generated text."
            )
            
            max_tokens = st.selectbox(
                "**Max Tokens**",
                options=[500, 1000, 2000, 4000, 16000, 32000, 64000],
                index=3,
                key="settings_max_tokens",
                help="Maximum length of the output sequence."
            )

        with col2:
            top_p = st.slider(
                "**Top-p**",
                min_value=0.0,
                max_value=1.0,
                value=0.9,
                step=0.1,
                key="settings_top_p",
                help="Controls diversity in text generation."
            )
            
            frequency_penalty = st.slider(
                "**Frequency Penalty**",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.1,
                key="settings_frequency_penalty",
                help="Reduces word repetition in output."
            )

    # Search Settings Tab
    with tabs[3]:
        st.markdown("""
            <div class="settings-section">
                <h2>🔍 Search Engine Personalization</h2>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
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

        with col2:
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
        st.markdown("""
            <div class="settings-section">
                <h2>🎨 AI Style Analysis</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="analysis-card" style="margin-bottom: 2rem;">
                <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.1em; margin: 0; line-height: 1.6;">
                    Enter a website URL or provide content samples to analyze your writing style and get personalized recommendations for optimal AI content generation.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for the layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Website URL input
            st.markdown("#### 🌐 Website URL Analysis")
            url = st.text_input(
                "Enter your website URL",
                placeholder="https://example.com",
                key="settings_website_url",
                help="Provide your website URL to analyze your content style. Leave empty if you want to provide written samples instead."
            )
            
            # Alternative: Written samples
            if not url:
                st.markdown("#### 📝 Written Samples")
                st.markdown("""
                    <div class="analysis-card">
                        <p style="color: rgba(255, 255, 255, 0.9); margin: 0; line-height: 1.6;">
                            No website URL? No problem! You can provide written samples of your content instead.
                            Share your best articles, blog posts, or any content that represents your writing style.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                samples = st.text_area(
                    "Paste your content samples here",
                    key="settings_content_samples",
                    help="Paste 2-3 samples of your best content. This helps ALwrity understand your writing style.",
                    height=200
                )
        
        with col2:
            st.markdown("#### 🎯 Analysis Features")
            st.markdown("""
                <div class="analysis-card">
                    <div style="color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
                        <p><strong>✨ Writing Style:</strong> Tone, voice, complexity analysis</p>
                        <p><strong>📊 Content Analysis:</strong> Structure and vocabulary assessment</p>
                        <p><strong>🎯 Audience Insights:</strong> Target demographic identification</p>
                        <p><strong>⚙️ AI Recommendations:</strong> Personalized settings optimization</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        # Add spacing between categories
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        if st.button("🎨 Analyze Writing Style", use_container_width=True, key="settings_analyze_style", type="primary"):
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
                                tab1, tab2, tab3 = st.tabs(["📄 Content", "📋 Metadata", "🔗 Links"])
                                
                                with tab1:
                                    st.markdown("#### Main Content")
                                    st.markdown(f"""
                                        <div class="analysis-card">
                                            <div style="color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
                                                {content.get('main_content', 'No content found')}
                                            </div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                        
                                with tab2:
                                    st.markdown("#### Website Metadata")
                                    st.markdown(f"""
                                        <div class="analysis-card">
                                            <div class="metric-item">
                                                <span class="metric-label">Title:</span>
                                                <span class="metric-value">{content.get('title', 'No title found')}</span>
                                            </div>
                                            <div class="metric-item">
                                                <span class="metric-label">Description:</span>
                                                <span class="metric-value">{content.get('description', 'No description found')}</span>
                                            </div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                        
                                with tab3:
                                    st.markdown("#### Extracted Links")
                                    links = content.get('links', [])
                                    if links:
                                        for link in links[:10]:  # Show first 10 links
                                            st.markdown(f"""
                                                <div class="analysis-card" style="margin-bottom: 0.5rem;">
                                                    <a href="{link.get('href', '')}" target="_blank" style="color: rgba(255, 255, 255, 0.9); text-decoration: none;">
                                                        {link.get('text', 'No text')[:80]}...
                                                    </a>
                                                </div>
                                            """, unsafe_allow_html=True)
                                    else:
                                        st.markdown("No links found in the content.")
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

    # Save Settings Button with premium styling
    st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
    if st.button("💾 Save All Settings", type="primary", use_container_width=True, key="settings_save_button"):
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
        st.success("✅ Settings saved successfully! Your preferences have been applied to all AI tools.")
        
        # Show a summary of saved settings
        st.markdown("""
            <div class="analysis-card" style="margin-top: 1rem;">
                <h4 style="color: #ffffff; margin-bottom: 1rem;">📋 Settings Summary</h4>
                <div style="color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
                    <p><strong>Content:</strong> {length} words, {tone} tone, {audience} audience</p>
                    <p><strong>Images:</strong> {images} images using {model}</p>
                    <p><strong>AI Model:</strong> {provider} - {ai_model}</p>
                    <p><strong>Search:</strong> {location} region, {results} results</p>
                </div>
            </div>
        """.format(
            length=blog_length,
            tone=blog_tone,
            audience=blog_demographic,
            images=number_of_blog_images,
            model=image_generation_model,
            provider=gpt_provider,
            ai_model=model,
            location=geographic_location,
            results=number_of_results
        ), unsafe_allow_html=True)