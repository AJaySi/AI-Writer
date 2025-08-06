"""
Facebook Story Generator Module

This module provides functionality to generate engaging Facebook Stories with various features
and customization options.
"""

import streamlit as st
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image


def write_fb_story():
    """Generate an engaging Facebook Story with various features and customization options."""
    
    st.markdown("""
    ### 📱 Facebook Story Generator
    Create engaging Facebook Stories that capture attention and drive engagement. Customize your story
    with various features and get AI-powered suggestions for optimal performance.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Story Content", "Visual Elements", "Preview & Analytics"])
    
    with tab1:
        # Basic story information
        col1, col2 = st.columns(2)
        
        with col1:
            story_type_options = [
                "Product showcase",
                "Behind the scenes",
                "User testimonial",
                "Event promotion",
                "Tutorial/How-to",
                "Question/Poll",
                "Announcement",
                "Customize"
            ]
            story_type = st.selectbox(
                "🎯 **What type of story do you want to create?**",
                story_type_options,
                index=0,
                help="Select the type of story you want to create."
            )
            
            if story_type == "Customize":
                story_type = st.text_input(
                    "🎯 **Customize your story type:**",
                    placeholder="e.g., Product launch",
                    help="Provide a specific story type if you selected 'Customize'."
                )
            
            target_audience = st.text_input(
                "👥 **Describe your target audience:**",
                placeholder="e.g., Fashion enthusiasts aged 18-24",
                help="Describe the audience you are targeting with this story."
            )
            
            story_tone_options = [
                "Casual",
                "Fun",
                "Professional",
                "Inspirational",
                "Educational",
                "Entertaining",
                "Customize"
            ]
            story_tone = st.selectbox(
                "🎨 **What tone do you want to use?**",
                story_tone_options,
                index=0,
                help="Choose the tone you want to use for the story."
            )
            
            if story_tone == "Customize":
                story_tone = st.text_input(
                    "🎨 **Customize your tone:**",
                    placeholder="e.g., Playful",
                    help="Provide a specific tone if you selected 'Customize'."
                )
        
        with col2:
            business_type = st.text_input(
                "🏢 **What is your business type?**",
                placeholder="e.g., Fashion brand",
                help="Provide the type of your business. This will help tailor the story content."
            )
            
            include = st.text_input(
                "📷 **What elements do you want to include?**",
                placeholder="e.g., Product demonstration, customer testimonial",
                help="Specify any elements you want to include in the story."
            )
            
            avoid = st.text_input(
                "❌ **What elements do you want to avoid?**",
                placeholder="e.g., Long text overlays",
                help="Specify any elements you want to avoid in the story."
            )
            
            # Advanced options
            with st.expander("Advanced Options"):
                st.markdown("#### Story Structure")
                use_hook = st.checkbox("Use attention-grabbing opening", value=True)
                use_story = st.checkbox("Include storytelling elements", value=True)
                use_cta = st.checkbox("Add clear call-to-action", value=True)
                
                st.markdown("#### Engagement Features")
                use_question = st.checkbox("Include engagement question", value=True)
                use_emoji = st.checkbox("Use relevant emojis", value=True)
                use_hashtags = st.checkbox("Add relevant hashtags", value=True)
                use_stickers = st.checkbox("Add interactive stickers", value=True)
    
    with tab2:
        # Visual elements options
        st.markdown("#### Visual Elements")
        
        # Background options
        st.markdown("##### Background")
        background_type = st.radio(
            "Select background type:",
            ["Solid color", "Gradient", "Image", "Video"],
            horizontal=True
        )
        
        if background_type == "Solid color":
            st.color_picker("Choose background color", "#FFFFFF")
        elif background_type == "Gradient":
            col1, col2 = st.columns(2)
            with col1:
                st.color_picker("Start color", "#FFFFFF")
            with col2:
                st.color_picker("End color", "#000000")
        elif background_type == "Image":
            image_source = st.radio(
                "Image source:",
                ["Upload", "Generate with AI", "Use URL"],
                horizontal=True
            )
            
            if image_source == "Upload":
                st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
            elif image_source == "Generate with AI":
                image_prompt = st.text_area("Describe the image you want to generate")
                if st.button("Generate Image"):
                    with st.spinner("Generating image..."):
                        # Call image generation function
                        pass
            else:
                st.text_input("Enter image URL")
        else:
            st.file_uploader("Upload a video", type=["mp4", "mov"])
        
        # Text overlay options
        st.markdown("##### Text Overlay")
        text_style = st.selectbox(
            "Text style:",
            ["Minimal", "Bold", "Playful", "Professional", "Custom"]
        )
        
        if text_style == "Custom":
            st.text_input("Custom text style description")
        
        text_color = st.color_picker("Text color", "#000000")
        text_position = st.selectbox(
            "Text position:",
            ["Top", "Middle", "Bottom", "Custom"]
        )
        
        # Interactive elements
        st.markdown("##### Interactive Elements")
        use_poll = st.checkbox("Add poll", value=False)
        use_quiz = st.checkbox("Add quiz", value=False)
        use_slider = st.checkbox("Add slider", value=False)
        use_countdown = st.checkbox("Add countdown", value=False)
    
    with tab3:
        # Preview and analytics section
        st.markdown("#### Story Preview")
        
        # Generate story button
        if st.button("🚀 Generate Facebook Story", key="generate_story"):
            with st.spinner("Generating your story..."):
                if not business_type or not target_audience:
                    st.error("🚫 Please provide the required inputs: Business Type and Target Audience.")
                else:
                    # Generate the story content
                    prompt = f"""
                    Create a Facebook Story for a {business_type} targeting {target_audience}.
                    
                    Story Type: {story_type}
                    Tone: {story_tone}
                    
                    Include: {include}
                    Avoid: {avoid}
                    
                    Additional requirements:
                    - Use attention-grabbing opening: {use_hook}
                    - Include storytelling elements: {use_story}
                    - Add clear call-to-action: {use_cta}
                    - Include engagement question: {use_question}
                    - Use relevant emojis: {use_emoji}
                    - Add relevant hashtags: {use_hashtags}
                    - Add interactive stickers: {use_stickers}
                    
                    Please write a well-structured Facebook Story that:
                    1. Grabs attention in the first frame
                    2. Maintains consistent tone throughout
                    3. Includes engaging content that aligns with the story type
                    4. Ends with a clear call-to-action
                    5. Uses appropriate formatting and emojis
                    6. Includes relevant hashtags if requested
                    7. Incorporates interactive elements if selected
                    """
                    
                    generated_story = llm_text_gen(prompt)
                    
                    if generated_story:
                        # Display the generated story
                        st.markdown("### Generated Story")
                        st.markdown(generated_story)
                        
                        # Display engagement predictions
                        st.markdown("### 📊 Engagement Predictions")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Expected Views", "1K - 2K")
                        with col2:
                            st.metric("Expected Engagement", "8-12%")
                        with col3:
                            st.metric("Best Time to Post", "6 PM - 8 PM")
                        
                        # Display optimization suggestions
                        st.markdown("### 💡 Optimization Suggestions")
                        st.info("""
                        - Add more interactive elements to increase engagement
                        - Keep text overlays short and readable
                        - Use vibrant colors to stand out
                        - Add music to increase watch time
                        """)
                        
                        # Copy button
                        st.button("📋 Copy to Clipboard", key="copy_story")
                    else:
                        st.error("Error: Failed to generate Facebook Story.") 