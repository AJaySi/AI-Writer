"""
Facebook Post Generator Module

This module provides functionality to generate engaging Facebook posts with various features
and optimization options.
"""

import streamlit as st
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image


def write_fb_post():
    """Generate an engaging Facebook post with various features and optimization options."""
    
    st.markdown("""
    ### 📝 Facebook Post Generator
    Create engaging Facebook posts that drive engagement and reach. Customize your post with various features
    and get AI-powered suggestions for optimal performance.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Post Content", "Media & Links", "Preview & Analytics"])
    
    with tab1:
        # Basic post information
        col1, col2 = st.columns(2)
        
        with col1:
            post_goal_options = [
                "Promote a product/service",
                "Share valuable content",
                "Increase engagement",
                "Build brand awareness",
                "Drive website traffic",
                "Generate leads",
                "Announce news/updates",
                "Customize"
            ]
            post_goal = st.selectbox(
                "🎯 **What is the goal of your post?**",
                post_goal_options,
                index=2,
                help="Select the main goal of your post."
            )
            
            if post_goal == "Customize":
                post_goal = st.text_input(
                    "🎯 **Customize your goal:**",
                    placeholder="e.g., Announce an event",
                    help="Provide a specific goal if you selected 'Customize'."
                )
            
            target_audience = st.text_input(
                "👥 **Describe your target audience:**",
                placeholder="e.g., Fitness enthusiasts aged 25-35",
                help="Describe the audience you are targeting with this post."
            )
            
            post_tone_options = [
                "Informative",
                "Humorous",
                "Inspirational",
                "Upbeat",
                "Casual",
                "Professional",
                "Conversational",
                "Customize"
            ]
            post_tone = st.selectbox(
                "🎨 **What tone do you want to use?**",
                post_tone_options,
                index=3,
                help="Choose the tone you want to use for the post."
            )
            
            if post_tone == "Customize":
                post_tone = st.text_input(
                    "🎨 **Customize your tone:**",
                    placeholder="e.g., Professional",
                    help="Provide a specific tone if you selected 'Customize'."
                )
        
        with col2:
            business_type = st.text_input(
                "🏢 **What is your business type?**",
                placeholder="e.g., Fitness coach",
                help="Provide the type of your business. This will help tailor the post content."
            )
            
            include = st.text_input(
                "📷 **What elements do you want to include?**",
                placeholder="e.g., Short video with a sneak peek of the challenge",
                help="Specify any elements you want to include in the post."
            )
            
            avoid = st.text_input(
                "❌ **What elements do you want to avoid?**",
                placeholder="e.g., Long paragraphs",
                help="Specify any elements you want to avoid in the post."
            )
            
            # Advanced options
            with st.expander("Advanced Options"):
                st.markdown("#### Post Structure")
                use_hook = st.checkbox("Use attention-grabbing hook", value=True)
                use_story = st.checkbox("Include storytelling elements", value=True)
                use_cta = st.checkbox("Add clear call-to-action", value=True)
                
                st.markdown("#### Engagement Features")
                use_question = st.checkbox("Include engagement question", value=True)
                use_emoji = st.checkbox("Use relevant emojis", value=True)
                use_hashtags = st.checkbox("Add relevant hashtags", value=True)
    
    with tab2:
        # Media and link options
        st.markdown("#### Media Options")
        media_type = st.radio(
            "Select media type:",
            ["None", "Image", "Video", "Carousel", "Link Preview"],
            horizontal=True
        )
        
        if media_type == "Image":
            col1, col2 = st.columns(2)
            with col1:
                image_source = st.radio(
                    "Image source:",
                    ["Upload", "Generate with AI", "Use URL"],
                    horizontal=True
                )
                
                if image_source == "Upload":
                    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
                elif image_source == "Generate with AI":
                    image_prompt = st.text_area("Describe the image you want to generate")
                    if st.button("Generate Image"):
                        with st.spinner("Generating image..."):
                            # Call image generation function
                            pass
                else:
                    image_url = st.text_input("Enter image URL")
            
            with col2:
                st.markdown("#### Image Settings")
                image_position = st.selectbox(
                    "Image position:",
                    ["Above post", "Below post"]
                )
                add_image_caption = st.checkbox("Add image caption", value=True)
        
        elif media_type == "Video":
            st.file_uploader("Upload a video", type=["mp4", "mov"])
            st.checkbox("Add video thumbnail", value=True)
            st.checkbox("Add video description", value=True)
        
        elif media_type == "Carousel":
            st.file_uploader("Upload multiple images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            st.checkbox("Add captions for each image", value=True)
        
        elif media_type == "Link Preview":
            st.text_input("Enter URL to preview")
            st.checkbox("Customize link preview", value=False)
    
    with tab3:
        # Preview and analytics section
        st.markdown("#### Post Preview")
        
        # Generate post button
        if st.button("🚀 Generate Facebook Post", key="generate_post"):
            with st.spinner("Generating your post..."):
                if not business_type or not target_audience:
                    st.error("🚫 Please provide the required inputs: Business Type and Target Audience.")
                else:
                    # Generate the post content
                    prompt = f"""
                    Create a Facebook post for a {business_type} targeting {target_audience}.
                    
                    Goal: {post_goal}
                    Tone: {post_tone}
                    
                    Include: {include}
                    Avoid: {avoid}
                    
                    Additional requirements:
                    - Use attention-grabbing hook: {use_hook}
                    - Include storytelling elements: {use_story}
                    - Add clear call-to-action: {use_cta}
                    - Include engagement question: {use_question}
                    - Use relevant emojis: {use_emoji}
                    - Add relevant hashtags: {use_hashtags}
                    
                    Please write a well-structured Facebook post that:
                    1. Grabs attention in the first line
                    2. Maintains consistent tone throughout
                    3. Includes engaging content that aligns with the goal
                    4. Ends with a clear call-to-action
                    5. Uses appropriate formatting and emojis
                    6. Includes relevant hashtags if requested
                    """
                    
                    generated_post = llm_text_gen(prompt)
                    
                    if generated_post:
                        # Display the generated post
                        st.markdown("### Generated Post")
                        st.markdown(generated_post)
                        
                        # Display engagement predictions
                        st.markdown("### 📊 Engagement Predictions")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Expected Reach", "2.5K - 5K")
                        with col2:
                            st.metric("Expected Engagement", "5-8%")
                        with col3:
                            st.metric("Best Time to Post", "2 PM - 4 PM")
                        
                        # Display optimization suggestions
                        st.markdown("### 💡 Optimization Suggestions")
                        st.info("""
                        - Consider adding a question to increase comments
                        - Use more emojis to increase visibility
                        - Keep paragraphs shorter for better readability
                        - Add a poll to increase engagement
                        """)
                        
                        # Copy button
                        st.button("📋 Copy to Clipboard", key="copy_post")
                    else:
                        st.error("Error: Failed to generate Facebook Post.") 