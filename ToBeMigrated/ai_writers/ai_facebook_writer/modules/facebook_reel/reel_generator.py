"""
Facebook Reel Generator Module

This module provides functionality to generate Facebook Reel content using AI.
It leverages text and image generation capabilities to create engaging reel content.
"""

import streamlit as st
import os
import sys
from loguru import logger
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import text generation
from .....gpt_providers.text_generation.main_text_generation import llm_text_gen

# Import image generation
from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

# Configure logging
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

def write_fb_reel():
    """
    Main function to render the Facebook Reel Generator UI and handle the generation process.
    """
    # Add back to dashboard button with minimal top margin
    st.markdown("""
        <div style='margin-top: 1rem; margin-bottom: 1rem;'>
            <a href="/" class="streamlit-button" style='text-decoration: none; color: white; background-color: #1877F2; padding: 0.5rem 1rem; border-radius: 0.5rem;'>← Back to Dashboard</a>
        </div>
    """, unsafe_allow_html=True)
    
    # Main title card with improved spacing
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 1.5rem; border-radius: 5px; margin-bottom: 1.5rem;'>
            <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 0.5rem;'>
                <span style='font-size: 2rem; margin-right: 0.5rem;'>🎥</span>
                <h1 style='color: #1877F2; margin: 0;'>Facebook Reel Generator</h1>
            </div>
            <p style='text-align: center; margin: 0;'>Create engaging Facebook Reels with AI-powered content</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Reel Content", "Visual Elements", "Advanced Options"])
    
    with tab1:
        render_reel_content_tab()
    
    with tab2:
        render_visual_elements_tab()
    
    with tab3:
        render_advanced_options_tab()

def render_reel_content_tab():
    """Render the Reel Content tab with input fields and generation options."""
    st.markdown("### Reel Content Settings")
    
    # Create columns for input fields
    col1, col2 = st.columns(2)
    
    with col1:
        business_type = st.text_input(
            "Business/Industry Type",
            placeholder="e.g., Fashion, Food, Fitness, Tech",
            help="The type of business or industry you're creating content for"
        )
        
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Young professionals, Parents, Fitness enthusiasts",
            help="Who is your content aimed at?"
        )
        
        reel_purpose = st.selectbox(
            "Reel Purpose",
            options=[
                "Product Showcase",
                "Tutorial/How-to",
                "Behind the Scenes",
                "Customer Testimonials",
                "Brand Story",
                "Promotion/Offer",
                "Educational Content",
                "Entertainment"
            ],
            help="What is the main purpose of your reel?"
        )
    
    with col2:
        brand_voice = st.selectbox(
            "Brand Voice/Tone",
            options=[
                "Professional",
                "Casual/Friendly",
                "Humorous",
                "Inspirational",
                "Educational",
                "Luxury/Elegant",
                "Energetic",
                "Relaxed"
            ],
            help="The tone and voice that represents your brand"
        )
        
        key_message = st.text_area(
            "Key Message",
            placeholder="What's the main message you want to convey in your reel?",
            help="The primary message or takeaway for your audience"
        )
        
        call_to_action = st.selectbox(
            "Call to Action",
            options=[
                "Follow Us",
                "Shop Now",
                "Learn More",
                "Sign Up",
                "Share",
                "Comment",
                "Save for Later",
                "Custom"
            ],
            help="What action do you want viewers to take after watching?"
        )
        
        if call_to_action == "Custom":
            custom_cta = st.text_input(
                "Custom Call to Action",
                placeholder="Enter your custom call to action"
            )
        else:
            custom_cta = ""
    
    # Additional content options
    st.markdown("### Content Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_hashtags = st.checkbox("Include Hashtag Suggestions", value=True)
        include_hook = st.checkbox("Include Hook/Opening", value=True)
        include_transitions = st.checkbox("Include Transition Suggestions", value=True)
    
    with col2:
        include_text_overlays = st.checkbox("Include Text Overlay Suggestions", value=True)
        include_engagement_tips = st.checkbox("Include Engagement Tips", value=True)
        include_trending_topics = st.checkbox("Include Trending Topics", value=True)
    
    # Generate button
    if st.button("Generate Reel Content", type="primary"):
        if not business_type or not target_audience or not key_message:
            st.error("Please fill in the required fields: Business Type, Target Audience, and Key Message")
            return
        
        with st.spinner("Generating your Facebook Reel content..."):
            # Generate the reel content
            reel_content = generate_reel_content(
                business_type=business_type,
                target_audience=target_audience,
                reel_purpose=reel_purpose,
                brand_voice=brand_voice,
                key_message=key_message,
                call_to_action=call_to_action,
                custom_cta=custom_cta,
                include_hashtags=include_hashtags,
                include_hook=include_hook,
                include_transitions=include_transitions,
                include_text_overlays=include_text_overlays,
                include_engagement_tips=include_engagement_tips,
                include_trending_topics=include_trending_topics
            )
            
            # Display the generated content
            if reel_content:
                st.markdown("### Generated Reel Content")
                
                # Create a container with a nice background for the content
                st.markdown("""
                    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #1877F2; margin-bottom: 20px;'>
                        <h4 style='color: #1877F2;'>Your Facebook Reel Script</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                # Parse and display the content in a structured way
                display_reel_content(reel_content)
                
                # Add a download button for the content
                st.download_button(
                    label="Download Reel Content",
                    data=reel_content,
                    file_name=f"facebook_reel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
                # Store the content in session state for the visual elements tab
                st.session_state['reel_content'] = reel_content
            else:
                st.error("Failed to generate reel content. Please try again.")

def render_visual_elements_tab():
    """Render the Visual Elements tab for generating images and visual content."""
    st.markdown("### Visual Elements for Your Reel")
    
    # Check if reel content has been generated
    if 'reel_content' not in st.session_state:
        st.info("Please generate reel content in the 'Reel Content' tab first.")
        return
    
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
            <p><strong>Note:</strong> This feature generates visual elements for your reel. Music and video elements are coming soon.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Visual element options
    st.markdown("#### Generate Visual Elements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        visual_style = st.selectbox(
            "Visual Style",
            options=[
                "Modern and Clean",
                "Bold and Vibrant",
                "Minimalist",
                "Playful and Fun",
                "Professional",
                "Lifestyle",
                "Product-Focused",
                "Custom"
            ],
            help="The overall visual style for your reel"
        )
        
        if visual_style == "Custom":
            custom_style = st.text_input(
                "Custom Visual Style",
                placeholder="Describe your desired visual style"
            )
        else:
            custom_style = ""
        
        num_images = st.slider(
            "Number of Images to Generate",
            min_value=1,
            max_value=5,
            value=3,
            help="How many visual elements would you like to generate?"
        )
    
    with col2:
        image_aspect_ratio = st.selectbox(
            "Image Aspect Ratio",
            options=[
                "9:16 (Vertical - Reel)",
                "1:1 (Square)",
                "16:9 (Horizontal)",
                "4:5 (Instagram Portrait)"
            ],
            help="The aspect ratio for your visual elements"
        )
        
        image_quality = st.select_slider(
            "Image Quality",
            options=["Basic", "Standard", "High", "Premium"],
            value="Standard",
            help="The quality level for generated images"
        )
    
    # Image generation prompt customization
    st.markdown("#### Customize Image Generation")
    
    image_prompt_style = st.radio(
        "Image Prompt Style",
        options=["Automatic", "Custom"],
        help="Choose how to generate the image prompts"
    )
    
    if image_prompt_style == "Custom":
        custom_image_prompt = st.text_area(
            "Custom Image Prompt",
            placeholder="Enter a custom prompt for image generation",
            help="Describe what you want the image to look like"
        )
    else:
        custom_image_prompt = ""
    
    # Generate images button
    if st.button("Generate Visual Elements", type="primary"):
        with st.spinner("Generating visual elements for your reel..."):
            # Generate images based on the reel content
            images = generate_reel_images(
                reel_content=st.session_state['reel_content'],
                visual_style=visual_style,
                custom_style=custom_style if visual_style == "Custom" else None,
                num_images=num_images,
                image_aspect_ratio=image_aspect_ratio,
                image_quality=image_quality,
                custom_image_prompt=custom_image_prompt if image_prompt_style == "Custom" else None
            )
            
            # Display the generated images
            if images:
                st.markdown("### Generated Visual Elements")
                
                # Display images in a grid
                cols = st.columns(min(3, len(images)))
                for i, image_path in enumerate(images):
                    with cols[i % len(cols)]:
                        st.image(image_path, use_container_width=True)
                        st.download_button(
                            label=f"Download Image {i+1}",
                            data=open(image_path, "rb").read(),
                            file_name=f"reel_image_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                            mime="image/png"
                        )
            else:
                st.error("Failed to generate visual elements. Please try again.")
    
    # Coming soon features
    st.markdown("### Coming Soon Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
                <h4>🎵 Music Suggestions</h4>
                <p>AI-powered music recommendations that match your reel's mood and content.</p>
                <span style='background-color: #6c757d; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;'>Coming Soon</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
                <h4>🎬 Video Elements</h4>
                <p>Generate video clips, transitions, and effects to enhance your reel.</p>
                <span style='background-color: #6c757d; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;'>Coming Soon</span>
            </div>
        """, unsafe_allow_html=True)

def render_advanced_options_tab():
    """Render the Advanced Options tab for additional customization."""
    st.markdown("### Advanced Options")
    
    # Check if reel content has been generated
    if 'reel_content' not in st.session_state:
        st.info("Please generate reel content in the 'Reel Content' tab first.")
        return
    
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
            <p><strong>Note:</strong> These advanced options allow for more customization of your reel content.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Advanced content options
    st.markdown("#### Content Customization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        content_length = st.select_slider(
            "Content Length",
            options=["Short (15s)", "Medium (30s)", "Long (60s)"],
            value="Medium (30s)",
            help="The target length for your reel content"
        )
        
        language_style = st.selectbox(
            "Language Style",
            options=[
                "Simple and Clear",
                "Professional",
                "Casual",
                "Technical",
                "Persuasive",
                "Storytelling"
            ],
            help="The language style for your content"
        )
    
    with col2:
        include_stats = st.checkbox("Include Statistics/Facts", value=False)
        include_quotes = st.checkbox("Include Quote Suggestions", value=False)
        include_emoji = st.checkbox("Include Emoji Suggestions", value=True)
    
    # AI model options
    st.markdown("#### AI Model Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        creativity_level = st.select_slider(
            "Creativity Level",
            options=["Conservative", "Balanced", "Creative", "Very Creative"],
            value="Balanced",
            help="How creative should the AI be in generating content"
        )
    
    with col2:
        ai_provider = st.selectbox(
            "AI Provider",
            options=["Auto-Select", "OpenAI", "Google Gemini", "Anthropic Claude"],
            help="Which AI provider to use for content generation"
        )
    
    # Generate with advanced options button
    if st.button("Regenerate with Advanced Options", type="primary"):
        with st.spinner("Regenerating your Facebook Reel content with advanced options..."):
            # Get the original content parameters from session state
            original_params = st.session_state.get('reel_params', {})
            
            # Update with advanced options
            advanced_params = {
                **original_params,
                'content_length': content_length,
                'language_style': language_style,
                'include_stats': include_stats,
                'include_quotes': include_quotes,
                'include_emoji': include_emoji,
                'creativity_level': creativity_level,
                'ai_provider': ai_provider
            }
            
            # Generate the reel content with advanced options
            reel_content = generate_reel_content_advanced(advanced_params)
            
            # Display the generated content
            if reel_content:
                st.markdown("### Regenerated Reel Content")
                
                # Create a container with a nice background for the content
                st.markdown("""
                    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #1877F2; margin-bottom: 20px;'>
                        <h4 style='color: #1877F2;'>Your Facebook Reel Script</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                # Parse and display the content in a structured way
                display_reel_content(reel_content)
                
                # Add a download button for the content
                st.download_button(
                    label="Download Reel Content",
                    data=reel_content,
                    file_name=f"facebook_reel_advanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
                # Update the content in session state
                st.session_state['reel_content'] = reel_content
            else:
                st.error("Failed to regenerate reel content. Please try again.")

def generate_reel_content(
    business_type: str,
    target_audience: str,
    reel_purpose: str,
    brand_voice: str,
    key_message: str,
    call_to_action: str,
    custom_cta: str = "",
    include_hashtags: bool = True,
    include_hook: bool = True,
    include_transitions: bool = True,
    include_text_overlays: bool = True,
    include_engagement_tips: bool = True,
    include_trending_topics: bool = True
) -> str:
    """
    Generate Facebook Reel content based on user inputs.
    
    Args:
        business_type: The type of business or industry
        target_audience: The target audience for the reel
        reel_purpose: The purpose of the reel
        brand_voice: The brand voice or tone
        key_message: The key message to convey
        call_to_action: The call to action
        custom_cta: Custom call to action text if "Custom" is selected
        include_hashtags: Whether to include hashtag suggestions
        include_hook: Whether to include a hook/opening
        include_transitions: Whether to include transition suggestions
        include_text_overlays: Whether to include text overlay suggestions
        include_engagement_tips: Whether to include engagement tips
        include_trending_topics: Whether to include trending topics
        
    Returns:
        str: The generated reel content
    """
    try:
        # Store parameters in session state for advanced options
        st.session_state['reel_params'] = {
            'business_type': business_type,
            'target_audience': target_audience,
            'reel_purpose': reel_purpose,
            'brand_voice': brand_voice,
            'key_message': key_message,
            'call_to_action': call_to_action,
            'custom_cta': custom_cta,
            'include_hashtags': include_hashtags,
            'include_hook': include_hook,
            'include_transitions': include_transitions,
            'include_text_overlays': include_text_overlays,
            'include_engagement_tips': include_engagement_tips,
            'include_trending_topics': include_trending_topics
        }
        
        # Construct the prompt for the AI
        prompt = f"""
        Create a detailed Facebook Reel script for a {business_type} business targeting {target_audience}.
        
        The purpose of this reel is: {reel_purpose}
        The brand voice/tone should be: {brand_voice}
        The key message to convey is: {key_message}
        The call to action should be: {call_to_action}{f" - {custom_cta}" if custom_cta else ""}
        
        Please provide a complete Facebook Reel script with the following elements:
        
        1. A hook (first 3 seconds) that grabs attention
        2. Main content (15-30 seconds) that delivers the key message
        3. A strong call-to-action at the end
        
        Additional elements to include:
        {f"- Hashtag suggestions relevant to the content and industry" if include_hashtags else ""}
        {f"- Text overlay suggestions for key points" if include_text_overlays else ""}
        {f"- Transition suggestions between scenes" if include_transitions else ""}
        {f"- Engagement tips to encourage interaction" if include_engagement_tips else ""}
        {f"- Trending topics that could be incorporated" if include_trending_topics else ""}
        
        Format the output as a structured script with clear sections and timing suggestions.
        """
        
        # Generate the content using the AI
        logger.info(f"[generate_reel_content] Generating reel content for {business_type}")
        response = llm_text_gen(prompt)
        
        if response:
            logger.info(f"[generate_reel_content] Successfully generated reel content")
            return response
        else:
            logger.error(f"[generate_reel_content] Failed to generate reel content")
            return None
            
    except Exception as e:
        logger.error(f"[generate_reel_content] Error generating reel content: {str(e)}")
        return None

def generate_reel_content_advanced(params: Dict[str, Any]) -> str:
    """
    Generate Facebook Reel content with advanced options.
    
    Args:
        params: Dictionary of parameters for content generation
        
    Returns:
        str: The generated reel content
    """
    try:
        # Extract parameters
        business_type = params.get('business_type', '')
        target_audience = params.get('target_audience', '')
        reel_purpose = params.get('reel_purpose', '')
        brand_voice = params.get('brand_voice', '')
        key_message = params.get('key_message', '')
        call_to_action = params.get('call_to_action', '')
        custom_cta = params.get('custom_cta', '')
        content_length = params.get('content_length', 'Medium (30s)')
        language_style = params.get('language_style', 'Simple and Clear')
        include_stats = params.get('include_stats', False)
        include_quotes = params.get('include_quotes', False)
        include_emoji = params.get('include_emoji', True)
        creativity_level = params.get('creativity_level', 'Balanced')
        ai_provider = params.get('ai_provider', 'Auto-Select')
        
        # Construct the advanced prompt
        prompt = f"""
        Create a detailed Facebook Reel script for a {business_type} business targeting {target_audience}.
        
        The purpose of this reel is: {reel_purpose}
        The brand voice/tone should be: {brand_voice}
        The key message to convey is: {key_message}
        The call to action should be: {call_to_action}{f" - {custom_cta}" if custom_cta else ""}
        
        Advanced requirements:
        - Content length: {content_length}
        - Language style: {language_style}
        - Creativity level: {creativity_level}
        {f"- Include relevant statistics or facts to support the message" if include_stats else ""}
        {f"- Include quote suggestions that could be used in the reel" if include_quotes else ""}
        {f"- Include emoji suggestions for text overlays" if include_emoji else ""}
        
        Please provide a complete Facebook Reel script with the following elements:
        
        1. A hook (first 3 seconds) that grabs attention
        2. Main content that delivers the key message
        3. A strong call-to-action at the end
        
        Format the output as a structured script with clear sections and timing suggestions.
        """
        
        # Generate the content using the AI
        logger.info(f"[generate_reel_content_advanced] Generating advanced reel content for {business_type}")
        response = llm_text_gen(prompt)
        
        if response:
            logger.info(f"[generate_reel_content_advanced] Successfully generated advanced reel content")
            return response
        else:
            logger.error(f"[generate_reel_content_advanced] Failed to generate advanced reel content")
            return None
            
    except Exception as e:
        logger.error(f"[generate_reel_content_advanced] Error generating advanced reel content: {str(e)}")
        return None

def generate_reel_images(
    reel_content: str,
    visual_style: str,
    custom_style: Optional[str] = None,
    num_images: int = 3,
    image_aspect_ratio: str = "9:16 (Vertical - Reel)",
    image_quality: str = "Standard",
    custom_image_prompt: Optional[str] = None
) -> List[str]:
    """
    Generate images for a Facebook Reel based on the content.
    
    Args:
        reel_content: The generated reel content
        visual_style: The visual style for the images
        custom_style: Custom style description if "Custom" is selected
        num_images: Number of images to generate
        image_aspect_ratio: The aspect ratio for the images
        image_quality: The quality level for the images
        custom_image_prompt: Custom prompt for image generation
        
    Returns:
        List[str]: List of paths to the generated images
    """
    try:
        logger.info(f"[generate_reel_images] Generating {num_images} images for reel")
        
        # Extract key elements from the reel content
        prompt = f"""
        Based on the following Facebook Reel content, extract {num_images} key visual elements or scenes that would make compelling images.
        For each element, provide a detailed description that would work well for AI image generation.
        
        Reel Content:
        {reel_content}
        
        For each visual element, provide:
        1. A descriptive title
        2. A detailed image generation prompt that includes:
           - The main subject
           - The setting/background
           - The mood/atmosphere
           - The style ({visual_style}{f" - {custom_style}" if custom_style else ""})
           - The aspect ratio ({image_aspect_ratio})
           - The quality level ({image_quality})
        
        Format each element as:
        TITLE: [title]
        PROMPT: [detailed prompt]
        
        Generate exactly {num_images} elements.
        """
        
        # Generate the image prompts using the AI
        logger.info(f"[generate_reel_images] Generating image prompts")
        response = llm_text_gen(prompt)
        
        if not response:
            logger.error(f"[generate_reel_images] Failed to generate image prompts")
            return []
        
        # Parse the response to extract the image prompts
        image_prompts = []
        current_title = ""
        current_prompt = ""
        
        for line in response.split('\n'):
            if line.startswith("TITLE:"):
                if current_title and current_prompt:
                    image_prompts.append((current_title, current_prompt))
                current_title = line.replace("TITLE:", "").strip()
                current_prompt = ""
            elif line.startswith("PROMPT:"):
                current_prompt = line.replace("PROMPT:", "").strip()
            elif current_prompt and line.strip():
                current_prompt += " " + line.strip()
        
        # Add the last prompt if there is one
        if current_title and current_prompt:
            image_prompts.append((current_title, current_prompt))
        
        # If we don't have enough prompts, generate generic ones
        while len(image_prompts) < num_images:
            image_prompts.append((f"Generic Image {len(image_prompts)+1}", 
                                f"A visually appealing image related to {visual_style} style for a Facebook Reel"))
        
        # Generate the images
        image_paths = []
        for i, (title, prompt) in enumerate(image_prompts[:num_images]):
            # Use custom prompt if provided
            if custom_image_prompt and i == 0:
                prompt = custom_image_prompt
            
            logger.info(f"[generate_reel_images] Generating image {i+1}: {title}")
            image_path = generate_image(prompt)
            
            if image_path:
                image_paths.append(image_path)
                logger.info(f"[generate_reel_images] Successfully generated image {i+1}")
            else:
                logger.error(f"[generate_reel_images] Failed to generate image {i+1}")
        
        return image_paths
        
    except Exception as e:
        logger.error(f"[generate_reel_images] Error generating reel images: {str(e)}")
        return []

def display_reel_content(content: str):
    """
    Display the reel content in a structured and visually appealing way.
    
    Args:
        content: The generated reel content
    """
    # Check if the content contains markdown code blocks
    if "```markdown" in content:
        # Extract the content from the markdown code block
        try:
            # Find the start and end of the markdown block
            start_idx = content.find("```markdown") + len("```markdown")
            end_idx = content.find("```", start_idx)
            if end_idx == -1:  # If no closing markdown block found
                end_idx = len(content)
            
            # Extract the markdown content
            markdown_content = content[start_idx:end_idx].strip()
            
            # Split the content into sections
            sections = markdown_content.split('\n\n')
            
            # Create tabs for different sections
            if len(sections) > 1:
                tabs = st.tabs(["Full Script", "Hook", "Main Content", "Call to Action", "Additional Elements"])
                
                with tabs[0]:  # Full Script
                    st.markdown(markdown_content)
                
                # Try to identify and display other sections
                hook_section = ""
                main_content = ""
                cta_section = ""
                additional_elements = ""
                
                for section in sections:
                    section_lower = section.lower()
                    if "hook" in section_lower or "opening" in section_lower or "first 3 seconds" in section_lower or "0-3 seconds" in section_lower:
                        hook_section = section
                    elif "main content" in section_lower or "key message" in section_lower or "15-30 seconds" in section_lower:
                        main_content = section
                    elif "call to action" in section_lower or "cta" in section_lower or "end" in section_lower:
                        cta_section = section
                    elif "hashtag" in section_lower or "text overlay" in section_lower or "transition" in section_lower or "engagement" in section_lower or "trending" in section_lower or "additional" in section_lower:
                        additional_elements += section + "\n\n"
                
                with tabs[1]:  # Hook
                    if hook_section:
                        st.markdown(hook_section)
                    else:
                        st.info("No specific hook section identified in the content.")
                
                with tabs[2]:  # Main Content
                    if main_content:
                        st.markdown(main_content)
                    else:
                        st.info("No specific main content section identified in the content.")
                
                with tabs[3]:  # Call to Action
                    if cta_section:
                        st.markdown(cta_section)
                    else:
                        st.info("No specific call to action section identified in the content.")
                
                with tabs[4]:  # Additional Elements
                    if additional_elements:
                        st.markdown(additional_elements)
                    else:
                        st.info("No additional elements identified in the content.")
            else:
                # If we can't split into sections, just display the content
                st.markdown(markdown_content)
        except Exception as e:
            logger.error(f"Error processing markdown content: {str(e)}")
            # Fallback to displaying the raw content
            st.markdown(content)
    else:
        # If no markdown code block, use the original approach
        # Split the content into sections
        sections = content.split('\n\n')
        
        # Create tabs for different sections
        if len(sections) > 1:
            tabs = st.tabs(["Full Script", "Hook", "Main Content", "Call to Action", "Additional Elements"])
            
            with tabs[0]:  # Full Script
                # Replace newlines with HTML line breaks
                formatted_content = content.replace('\n', '<br>')
                st.markdown(f"""
                    <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                        {formatted_content}
                    </div>
                """, unsafe_allow_html=True)
            
            # Try to identify and display other sections
            hook_section = ""
            main_content = ""
            cta_section = ""
            additional_elements = ""
            
            for section in sections:
                section_lower = section.lower()
                if "hook" in section_lower or "opening" in section_lower or "first 3 seconds" in section_lower or "0-3 seconds" in section_lower:
                    hook_section = section
                elif "main content" in section_lower or "key message" in section_lower or "15-30 seconds" in section_lower:
                    main_content = section
                elif "call to action" in section_lower or "cta" in section_lower or "end" in section_lower:
                    cta_section = section
                elif "hashtag" in section_lower or "text overlay" in section_lower or "transition" in section_lower or "engagement" in section_lower or "trending" in section_lower or "additional" in section_lower:
                    additional_elements += section + "\n\n"
            
            with tabs[1]:  # Hook
                if hook_section:
                    # Replace newlines with HTML line breaks
                    formatted_hook = hook_section.replace('\n', '<br>')
                    st.markdown(f"""
                        <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                            {formatted_hook}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No specific hook section identified in the content.")
            
            with tabs[2]:  # Main Content
                if main_content:
                    # Replace newlines with HTML line breaks
                    formatted_main = main_content.replace('\n', '<br>')
                    st.markdown(f"""
                        <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                            {formatted_main}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No specific main content section identified in the content.")
            
            with tabs[3]:  # Call to Action
                if cta_section:
                    # Replace newlines with HTML line breaks
                    formatted_cta = cta_section.replace('\n', '<br>')
                    st.markdown(f"""
                        <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                            {formatted_cta}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No specific call to action section identified in the content.")
            
            with tabs[4]:  # Additional Elements
                if additional_elements:
                    # Replace newlines with HTML line breaks
                    formatted_additional = additional_elements.replace('\n', '<br>')
                    st.markdown(f"""
                        <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                            {formatted_additional}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No additional elements identified in the content.")
        else:
            # If we can't split into sections, just display the content
            # Replace newlines with HTML line breaks
            formatted_content = content.replace('\n', '<br>')
            st.markdown(f"""
                <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                    {formatted_content}
                </div>
            """, unsafe_allow_html=True) 