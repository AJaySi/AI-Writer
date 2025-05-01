import os
import streamlit as st
from loguru import logger

from lib.utils.voice_processing import record_voice
from lib.ai_writers.ai_blog_writer.blog_writer_styles import apply_blog_writer_styles
from lib.ai_writers.ai_blog_writer.ai_blog_generator_utils import (
    CONFIG_PATH,
    load_config,
    get_search_params_from_config,
    get_blog_characteristics_from_config,
    get_blog_images_from_config,
    get_llm_options_from_config,
    process_input,
    handle_content_generation
)

apply_blog_writer_styles()

def display_input_section():
    """Display the input section with text area, file upload, and voice recording options."""
    # Main container with columns for better organization
    col1, col2, col3 = st.columns([2, 1.5, 0.5])
    
    # First column: Keywords input
    with col1:
        st.markdown("### 📌 Content Source")
        user_input = st.text_area(
            'Power your content with keywords or a website URL',
            help='Provide keywords, a blog title, YouTube link, or web URL to generate targeted content.',
            placeholder="Examples:\n- Keywords: AI tools, digital marketing\n- Blog Title: The Future of AI in Marketing\n- YouTube Link: https://youtube.com/...\n- Web URL: https://example.com/...",
            height=150
        )
    
    # Second column: File uploader
    with col2:
        st.markdown("### 📁 File Upload")
        uploaded_file = st.file_uploader(
            "Add files to enhance your content",
                                         type=["txt", "pdf", "docx", "jpg", "jpeg", "png", "mp3", "wav", "mp4", "mkv", "avi"],
            help='Upload documents, images, or media files to incorporate additional information in your blog.'
        )
    
    # Third column: Voice input
    with col3:
        st.markdown("### 🎤 Voice")
        audio_input = record_voice()
        if audio_input:
            st.success("Voice recorded!")
    
    return user_input, uploaded_file, audio_input


def display_content_type_selection(inside_expander=False):
    """Display the content type selection section and return the selected type.
    
    Args:
        inside_expander (bool): If True, adjust heading levels for display inside an expander.
    """
    # Content options in a cleaner layout
    if not inside_expander:
        st.markdown("### 🔧 Content Configuration")
        st.markdown("#### Select Content Type")
    else:
        st.markdown("#### Content Type")
    
    # Content type selection with better UI
    content_type = st.radio(
        "Choose the format and length of your blog content",
        ["Standard Blog Post", "Comprehensive Long-form", "AI Agent Team (Beta)"],
        horizontal=True,
        help="Standard: 800-1200 words | Long-form: 1500+ words | AI Agent: Experimental multi-perspective content"
    )
    
    # Map the friendly content type names to the original options
    content_type_map = {
        "Standard Blog Post": "Normal-length content",
        "Comprehensive Long-form": "Long-form content",
        "AI Agent Team (Beta)": "Experimental - AI Agents team"
    }
    
    return content_type, content_type_map[content_type]


def display_content_characteristics_tab():
    """Display the Content Characteristics tab and return the selected options."""
    st.markdown("#### Blog Content Characteristics")
    
    # Load default values from configuration
    config_blog_chars = get_blog_characteristics_from_config()
    
    # Blog length
    blog_length = st.number_input(
        "Blog Length (words)",
        min_value=500,
        max_value=5000,
        value=int(config_blog_chars.get("blog_length", 2000)),
        step=100,
        help="Target word count for your blog post"
    )
    
    # Blog tone
    tone_options = ["Professional", "Casual", "Formal", "Conversational", "Authoritative", "Friendly"]
    default_tone = config_blog_chars.get("blog_tone", "Professional")
    default_tone_index = tone_options.index(default_tone) if default_tone in tone_options else 0
    
    blog_tone = st.selectbox(
        "Blog Tone",
        options=tone_options,
        index=default_tone_index,
        help="The overall tone and style of your blog content"
    )
    
    # Blog demographic
    demographic_options = ["Professional", "General", "Technical", "Beginner", "Expert", "Student"]
    default_demo = config_blog_chars.get("blog_demographic", "Professional")
    default_demo_index = demographic_options.index(default_demo) if default_demo in demographic_options else 0
    
    blog_demographic = st.selectbox(
        "Target Audience",
        options=demographic_options,
        index=default_demo_index,
        help="Who your blog content is primarily written for"
    )
    
    # Blog type
    type_options = ["Informational", "How-to", "List", "Review", "Tutorial", "Opinion"]
    default_type = config_blog_chars.get("blog_type", "Informational")
    default_type_index = type_options.index(default_type) if default_type in type_options else 0
    
    blog_type = st.selectbox(
        "Blog Type",
        options=type_options,
        index=default_type_index,
        help="The format and purpose of your blog content"
    )
    
    # Blog language
    language_options = ["English", "Spanish", "French", "German", "Italian", "Portuguese"]
    default_lang = config_blog_chars.get("blog_language", "English")
    default_lang_index = language_options.index(default_lang) if default_lang in language_options else 0
    
    blog_language = st.selectbox(
        "Blog Language",
        options=language_options,
        index=default_lang_index,
        help="The language your blog will be written in"
    )
    
    # Blog output format
    format_options = ["markdown", "html", "plain text"]
    default_format = config_blog_chars.get("blog_output_format", "markdown").lower()
    default_format_index = format_options.index(default_format) if default_format in format_options else 0
    
    blog_output_format = st.selectbox(
        "Output Format",
        options=format_options,
        index=default_format_index,
        help="The format in which the blog content will be generated"
    )
    
    # Show current configuration source
    if os.path.exists(CONFIG_PATH):
        st.success(f"✅ Using blog characteristics from configuration file")
    else:
        st.info("ℹ️ Using default blog characteristics (no configuration file found)")
    
    return {
        "blog_length": blog_length,
        "blog_tone": blog_tone,
        "blog_demographic": blog_demographic,
        "blog_type": blog_type,
        "blog_language": blog_language,
        "blog_output_format": blog_output_format
    }


def display_content_analysis_tab():
    """Display the Content & Analysis Options tab and return the selected options."""
    st.markdown("#### Content & Analysis Options")
    
    # Create two columns for better organization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Content Enhancements**")
        create_seo_tags = st.checkbox(
            '✅ Generate SEO metadata',
            value=True,
            help='Create schema markup, meta tags, and social media metadata'
        )
        generate_social_media = st.checkbox(
            '✅ Create social media posts',
            value=False,
            help="Generate matching social content for Facebook, Twitter, and LinkedIn"
        )
        add_table_of_contents = st.checkbox(
            '✅ Add table of contents',
            value=True,
            help="Include an auto-generated table of contents at the beginning of the blog"
        )
    
    with col2:
        st.markdown("**Analysis & Improvement**")
        content_analysis = st.checkbox(
            '✅ Perform content analysis',
            value=False,
            help="Include proofreading, readability score, and improvement suggestions"
        )
        enhance_readability = st.checkbox(
            '✅ Enhance readability',
            value=True,
            help="Optimize sentence structure and vocabulary for better readability"
        )
        fact_checking = st.checkbox(
            '✅ Basic fact verification',
            value=False,
            help="Verify key facts from multiple sources when possible"
        )
    
    st.markdown("---")
    st.markdown("**Formatting Options**")
    
    # Create two columns for formatting options
    fmt_col1, fmt_col2 = st.columns(2)
    
    with fmt_col1:
        section_headings = st.checkbox(
            '✅ Use section headings',
            value=True,
            help="Include clear section headings throughout the blog"
        )
        include_lists = st.checkbox(
            '✅ Use bullet points and lists',
            value=True,
            help="Format appropriate content as bullet points or numbered lists"
        )
    
    with fmt_col2:
        include_quotes = st.checkbox(
            '✅ Include relevant quotes',
            value=False,
            help="Add expert quotes or important statements as blockquotes"
        )
        use_subheadings = st.checkbox(
            '✅ Use subheadings',
            value=True,
            help="Break down sections with descriptive subheadings"
        )
    
    return {
        "create_seo_tags": create_seo_tags,
        "generate_social_media": generate_social_media,
        "add_table_of_contents": add_table_of_contents,
        "content_analysis": content_analysis,
        "enhance_readability": enhance_readability,
        "fact_checking": fact_checking,
        "section_headings": section_headings,
        "include_lists": include_lists,
        "include_quotes": include_quotes,
        "use_subheadings": use_subheadings
    }


def display_blog_images_tab():
    """Display the Blog Images Details tab and return the selected options."""
    st.markdown("#### Blog Images Settings")
    
    # Load default values from configuration
    config_images = get_blog_images_from_config()
    
    # Image generation model selection
    model_options = ["stable-diffusion", "dall-e", "midjourney", "imagen"]
    default_model = config_images.get("image_model", "stable-diffusion")
    default_model_index = model_options.index(default_model) if default_model in model_options else 0
    
    image_model = st.selectbox(
        "Image Generation Model",
        options=model_options,
        index=default_model_index,
        help="AI model used to generate blog images"
    )
    
    # Number of blog images
    num_images = st.number_input(
        "Number of Blog Images",
        min_value=0,
        max_value=10,
        value=config_images.get("num_images", 1),
        step=1,
        help="Number of images to generate for the blog"
    )
    
    # Image style
    style_options = ["Realistic", "Artistic", "Cartoon", "Minimalist", "Corporate", "Vibrant"]
    default_style = config_images.get("image_style", "Realistic")
    default_style_index = style_options.index(default_style) if default_style in style_options else 0
    
    image_style = st.selectbox(
        "Image Style",
        options=style_options,
        index=default_style_index,
        help="Visual style of the generated images"
    )
    
    # Additional image options
    st.markdown("**Additional Image Options**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_featured = st.checkbox(
            '✅ Generate featured image',
            value=True,
            help="Create a featured header image for the blog"
        )
        add_captions = st.checkbox(
            '✅ Add image captions',
            value=True,
            help="Generate descriptive captions for each image"
        )
    
    with col2:
        use_alt_text = st.checkbox(
            '✅ Generate alt text',
            value=True,
            help="Create accessibility alt text for all images"
        )
        optimize_images = st.checkbox(
            '✅ Optimize image placement',
            value=True,
            help="Intelligently place images throughout the content"
        )
    
    # Show current configuration source
    if os.path.exists(CONFIG_PATH):
        st.success(f"✅ Using image settings from configuration file")
    else:
        st.info("ℹ️ Using default image settings (no configuration file found)")
    
    return {
        "image_model": image_model,
        "num_images": num_images,
        "image_style": image_style,
        "generate_featured": generate_featured,
        "add_captions": add_captions,
        "use_alt_text": use_alt_text,
        "optimize_placement": optimize_images
    }


def display_llm_options_tab():
    """Display the LLM Options tab and return the selected options."""
    st.markdown("#### Language Model Settings")
    
    # Load default values from configuration
    config_llm = get_llm_options_from_config()
    
    # LLM provider selection
    provider_options = ["google", "openai", "anthropic", "local"]
    default_provider = config_llm.get("provider", "google")
    default_provider_index = provider_options.index(default_provider) if default_provider in provider_options else 0
    
    llm_provider = st.selectbox(
        "AI Provider",
        options=provider_options,
        index=default_provider_index,
        help="The AI provider to use for content generation"
    )
    
    # Model selection (dynamic based on provider)
    if llm_provider == "google":
        model_options = ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-pro"]
    elif llm_provider == "openai":
        model_options = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
    elif llm_provider == "anthropic":
        model_options = ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
    else:
        model_options = ["llama-3-70b", "mistral-large", "local-model"]
    
    default_model = config_llm.get("model", "gemini-1.5-flash-latest")
    default_model_index = 0
    if default_model in model_options:
        default_model_index = model_options.index(default_model)
    
    llm_model = st.selectbox(
        "AI Model",
        options=model_options,
        index=default_model_index,
        help="The specific AI model to use for content generation"
    )
    
    # Create two columns for temperature and max tokens
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature setting
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=config_llm.get("temperature", 0.7),
            step=0.1,
            help="Controls randomness: lower values are more deterministic, higher values more creative"
        )
    
    with col2:
        # Max tokens
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=1000,
            max_value=32000,
            value=config_llm.get("max_tokens", 4000),
            step=1000,
            help="Maximum length of generated content (in tokens)"
        )
    
    # Advanced LLM options
    st.markdown("---")
    st.markdown("**Advanced LLM Options**")
    show_advanced_llm = st.checkbox("Show advanced LLM parameters", value=False)
    
    advanced_params = {}
    if show_advanced_llm:
        # Top-p (nucleus sampling)
        top_p = st.slider(
            "Top-p (Nucleus Sampling)",
            min_value=0.1,
            max_value=1.0,
            value=0.9,
            step=0.1,
            help="Controls diversity via nucleus sampling: 1.0 considers all tokens, lower values restrict to more likely tokens"
        )
        
        # Top-k
        top_k = st.slider(
            "Top-k",
            min_value=1,
            max_value=100,
            value=40,
            step=1,
            help="Controls diversity by limiting to top k tokens: higher values allow more diversity"
        )
        
        # Presence penalty
        presence_penalty = st.slider(
            "Presence Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=0.0,
            step=0.1,
            help="Penalizes repeated tokens: positive values discourage repetition"
        )
        
        advanced_params = {
            "top_p": top_p,
            "top_k": top_k,
            "presence_penalty": presence_penalty
        }
    
    # Show current configuration source
    if os.path.exists(CONFIG_PATH):
        st.success(f"✅ Using LLM settings from configuration file")
    else:
        st.info("ℹ️ Using default LLM settings (no configuration file found)")
    
    return {
        "provider": llm_provider,
        "model": llm_model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        **advanced_params
    }


def display_search_settings_tab():
    """Display the Search Settings tab and return the selected options."""
    st.markdown("#### AI Search Configuration")
    st.markdown("Control how the AI researches your topic")
    
    # Load default values from configuration
    config_search_params = get_search_params_from_config()
    
    # Number of search results
    max_results = st.slider(
        "Maximum Results",
        min_value=5,
        max_value=30,
        value=config_search_params.get("max_results", 10),
        step=5,
        help="Maximum number of search results to use for research"
    )
    
    # Search depth
    search_depth = st.radio(
        "Search Depth",
        options=["basic", "advanced"],
        index=0,
        horizontal=True,
        help="Basic: Faster but less comprehensive. Advanced: More thorough but slower."
    )
    
    # Include domains
    include_domains = st.text_input(
        "Include Domains (Optional)",
        value="",
        help="Comma-separated list of domains to prioritize in search (e.g., wikipedia.org,nih.gov)"
    )
    
    # Time range - use value from config
    time_options = ["day", "week", "month", "year", "all"]
    default_time_index = time_options.index(config_search_params.get("time_range", "year")) if config_search_params.get("time_range", "year") in time_options else 3  # Default to "year" (index 3)
    
    time_range = st.select_slider(
        "Time Range",
        options=time_options,
        value=time_options[default_time_index],
        help="Limit search results to a specific time period"
    )
    
    # Show current configuration source
    if os.path.exists(CONFIG_PATH):
        st.success(f"✅ Using search defaults from configuration file")
    else:
        st.info("ℹ️ Using default search settings (no configuration file found)")
    
    # Replace expander with checkbox for configuration display
    show_config = st.checkbox("Show configuration details", value=False)
    if show_config:
        st.markdown("""
        **Configuration File Location**  
        Search parameters are loaded from the main configuration file at:  
        `lib/workspace/alwrity_config/main_config.json`
        
        You can modify this file to change the default search settings.
        """)
        
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as f:
                    config_content = f.read()
                st.code(config_content, language="json")
            except:
                st.warning("Could not read configuration file")
    
    st.info("These settings control how the AI performs web research for your content. More thorough searches may take longer but produce better results.")
    
    # Process include_domains from string to list if provided
    domains_list = []
    if include_domains:
        domains_list = [domain.strip() for domain in include_domains.split(",") if domain.strip()]
    
    return {
        "max_results": max_results,
        "search_depth": search_depth,
        "time_range": time_range,
        "include_domains": domains_list
    }


def display_advanced_options():
    """Display all advanced options tabs and return the selected configurations."""
    
    with st.expander("⚙️ Advanced Options for Personalization, Analysis, Images, LLM, and Search", expanded=False):
        content_type, selected_content_type = display_content_type_selection(inside_expander=True)

        tabs = st.tabs(["Personalization", "Analysis Options", "Blog Images Details", "LLM Options", "Search Settings"])
        
        with tabs[0]:  # Content Characteristics
            blog_params = display_content_characteristics_tab()
        
        with tabs[1]:  # Combined Content & Analysis Options
            content_analysis_params = display_content_analysis_tab()
        
        with tabs[2]:  # Blog Images Details
            image_params = display_blog_images_tab()
        
        with tabs[3]:  # LLM Options
            llm_params = display_llm_options_tab()
        
        with tabs[4]:  # Search Settings
            search_params = display_search_settings_tab()
    
    return content_type, selected_content_type, blog_params, content_analysis_params, image_params, llm_params, search_params


def blog_from_keyword():
    """Input blog keywords, research and write a factual blog with enhanced UI."""
    
    # Get user inputs
    user_input, uploaded_file, audio_input = display_input_section()
    
    # Display advanced options and get configurations
    content_type, selected_content_type, blog_params, content_analysis_params, image_params, llm_params, search_params = display_advanced_options()
    
    # Generate button with icon and clearer purpose
    st.markdown("")  # Add spacing
    generate_pressed = st.button("✨ Generate Blog Content", use_container_width=True)
    
    # Processing logic
    if generate_pressed:
        st.empty()
        
        if not uploaded_file and not user_input and not audio_input:
            st.error("Please provide at least one input source (keywords, file, or voice recording)")
            st.stop()
        
        input_type = process_input(user_input, uploaded_file)
        
        # Use the utility function to handle content generation
        handle_content_generation(input_type, user_input, uploaded_file, search_params, blog_params, selected_content_type)


def ai_blog_writer_page():
    """Render the AI Blog Writer page with enhanced styling."""
    logger.info("Rendering AI Blog Writer page")
    
    # Apply shared blog writer styles
    apply_blog_writer_styles()
    
    # Back button with icon
    if st.button("← Back to Dashboard", key="back_to_dashboard"):
        logger.info("User clicked back button, returning to ai writer dashboard")
        st.query_params.clear()
        st.rerun()
    
    # Enhanced header with icon
    st.markdown("""
        <div class="page-header">
            <h1>✍️ AI Blog Writer</h1>
            <p>Create engaging, SEO-optimized blog content with AI assistance. Our advanced algorithms help you generate high-quality, relevant articles for any topic or niche.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Call the blog generator function with enhanced UI
    logger.info("Calling blog_from_keyword function")
    blog_from_keyword()
    
    logger.info("Finished rendering AI Blog Writer page")