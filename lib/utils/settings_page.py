import streamlit as st

def render_settings_page():
    """Renders the settings page with all configuration options in tabs"""
    
    st.title("🛠️ Settings & Configuration")
    
    # Create tabs for different settings categories
    tabs = st.tabs([
        "👷 Content",
        "🩻 Images",
        "🤖 LLM",
        "🕵️ Search"
    ])
    
    # Content Settings Tab
    with tabs[0]:
        st.header("Content Personalization")
        blog_length = st.text_input(
            "**Content Length (words)**",
            value="2000",
            help="Approximate word count for blogs. Note: Actual length may vary based on GPT provider and max token count."
        )

        blog_tone_options = ["Casual", "Professional", "How-to", "Beginner", "Research", "Programming", "Social Media", "Customize"]
        blog_tone = st.selectbox(
            "**Content Tone**",
            options=blog_tone_options,
            help="Select the desired tone for the blog content."
        )

        if blog_tone == "Customize":
            custom_tone = st.text_input(
                "Enter the tone of your content",
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
            help="Select the primary audience for the blog content."
        )

        blog_type = st.selectbox(
            "**Content Type**",
            options=["Informational", "Commercial", "Company", "News", "Finance", "Competitor", "Programming", "Scholar"],
            help="Select the category that best describes the blog content."
        )

        blog_language = st.selectbox(
            "**Content Language**",
            options=["English", "Spanish", "German", "Chinese", "Arabic", "Nepali", "Hindi", "Hindustani", "Customize"],
            help="Select the language in which the blog will be written."
        )

        blog_output_format = st.selectbox(
            "**Content Output Format**",
            options=["markdown", "HTML", "plaintext"],
            help="Select the format for the blog output."
        )

    # Images Settings Tab
    with tabs[1]:
        st.header("Images Personalization")
        image_generation_model = st.selectbox(
            "**Image Generation Model**",
            options=["stable-diffusion", "dalle2", "dalle3"],
            help="Select the model to generate images for the blog."
        )
        
        number_of_blog_images = st.number_input(
            "**Number of Blog Images**",
            value=1,
            min_value=1,
            max_value=10,
            help="Specify the number of images to include in the blog."
        )

    # LLM Settings Tab
    with tabs[2]:
        st.header("LLM Personalization")
        gpt_provider = st.selectbox(
            "**GPT Provider**",
            options=["google", "openai", "minstral"],
            help="Select the provider for the GPT model."
        )

        model = st.text_input(
            "**Model**",
            value="gemini-1.5-flash-latest",
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
                help="Controls the creativity level of the generated text."
            )
            
            max_tokens = st.selectbox(
                "Max Tokens",
                options=[500, 1000, 2000, 4000, 16000, 32000, 64000],
                index=3,
                help="Maximum length of the output sequence."
            )

        with col2:
            top_p = st.slider(
                "Top-p",
                min_value=0.0,
                max_value=1.0,
                value=0.9,
                step=0.1,
                help="Controls diversity in text generation."
            )
            
            frequency_penalty = st.slider(
                "Frequency Penalty",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Reduces word repetition in output."
            )

    # Search Settings Tab
    with tabs[3]:
        st.header("Search Engine Personalization")
        geographic_location = st.selectbox(
            "**Geographic Location**",
            options=["us", "in", "fr", "cn"],
            help="Select the geographic location for tailoring search results."
        )

        search_language = st.selectbox(
            "**Search Language**",
            options=["en", "zn-cn", "de", "hi"],
            help="Select the language for the search results."
        )

        number_of_results = st.number_input(
            "**Number of Results**",
            value=10,
            min_value=1,
            max_value=20,
            help="Specify the number of search results to retrieve."
        )

        time_range = st.selectbox(
            "**Time Range**",
            options=["anytime", "past day", "past week", "past month", "past year"],
            help="Select the time range for filtering search results."
        )

        include_domains = st.text_input(
            "**Include Domains**",
            value="",
            help="List specific domains to include in search results (comma-separated)."
        )

        similar_url = st.text_input(
            "**Similar URL**",
            value="",
            help="Provide a URL to find similar results."
        )

    # Save Settings Button
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
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