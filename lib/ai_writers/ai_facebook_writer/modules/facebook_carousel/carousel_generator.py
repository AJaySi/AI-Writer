"""
Facebook Carousel Generator

This module provides functionality to generate engaging Facebook carousel posts with
AI-powered content and visuals.
"""

import streamlit as st
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from loguru import logger
import sys
import json

# Import text and image generation
from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

# Configure logging
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

def write_fb_carousel():
    """Main function to render the Facebook Carousel Generator UI."""
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Content Setup", "Visual Elements", "Preview & Export"])
    
    with tab1:
        render_content_setup_tab()
    
    with tab2:
        render_visual_elements_tab()
    
    with tab3:
        render_preview_export_tab()

def render_content_setup_tab():
    """Render the Content Setup tab with input fields for carousel content."""
    st.markdown("### Carousel Content Setup")
    
    # Basic Information
    col1, col2 = st.columns(2)
    
    with col1:
        business_type = st.text_input(
            "Business/Industry Type",
            placeholder="e.g., Fashion, Food, Tech, Health",
            help="Your business or industry type"
        )
        
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Young professionals, Parents, Tech enthusiasts",
            help="Who is your content aimed at?"
        )
        
        carousel_purpose = st.selectbox(
            "Carousel Purpose",
            options=[
                "Product Showcase",
                "How-to Guide",
                "Before and After",
                "Features/Benefits",
                "Customer Success Stories",
                "Product Collection",
                "Service Overview",
                "Educational Series",
                "Brand Story"
            ],
            help="What is the main purpose of your carousel?"
        )
    
    with col2:
        brand_voice = st.selectbox(
            "Brand Voice/Tone",
            options=[
                "Professional",
                "Casual/Friendly",
                "Luxury/Elegant",
                "Educational",
                "Inspirational",
                "Humorous",
                "Authoritative",
                "Empathetic"
            ],
            help="The tone that represents your brand"
        )
        
        key_message = st.text_area(
            "Key Message",
            placeholder="What's the main message you want to convey?",
            help="The primary takeaway for your audience"
        )
        
        num_slides = st.slider(
            "Number of Slides",
            min_value=2,
            max_value=10,
            value=5,
            help="How many slides in your carousel? (Facebook allows up to 10)"
        )
    
    # Carousel Structure
    st.markdown("### Carousel Structure")
    
    structure_options = {
        "Progressive Story": "Tell a story that unfolds across slides",
        "Feature Showcase": "Highlight different features/benefits in each slide",
        "Step-by-Step Guide": "Break down a process into clear steps",
        "Problem-Solution": "Present problems and their solutions",
        "Collection Display": "Showcase a collection of products/services",
        "Before-After Series": "Show transformation or results",
        "FAQ Format": "Address common questions with answers",
        "Tips & Tricks": "Share helpful tips related to your topic"
    }
    
    carousel_structure = st.selectbox(
        "Carousel Structure",
        options=list(structure_options.keys()),
        help="How do you want to structure your carousel content?"
    )
    
    st.info(f"💡 **Structure Description:** {structure_options[carousel_structure]}")
    
    # Content Preferences
    st.markdown("### Content Preferences")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        include_stats = st.checkbox("Include Statistics/Facts", value=True)
        include_testimonials = st.checkbox("Include Testimonials", value=False)
        include_pricing = st.checkbox("Include Pricing", value=False)
    
    with col2:
        include_cta = st.checkbox("Include Call-to-Action", value=True)
        include_hashtags = st.checkbox("Include Hashtags", value=True)
        include_emojis = st.checkbox("Include Emojis", value=True)
    
    with col3:
        include_questions = st.checkbox("Include Questions", value=True)
        include_bullets = st.checkbox("Include Bullet Points", value=True)
        include_numbers = st.checkbox("Include Numbered Lists", value=False)
    
    # Additional Preferences
    st.markdown("### Additional Content")
    
    col1, col2 = st.columns(2)
    
    with col1:
        specific_features = st.text_area(
            "Specific Features/Points to Include",
            placeholder="List specific features, points, or information you want to highlight",
            help="These will be incorporated into your carousel content"
        )
    
    with col2:
        avoid_points = st.text_area(
            "Points to Avoid",
            placeholder="List any topics, terms, or approaches you want to avoid",
            help="These will be excluded from your carousel content"
        )
    
    # Generate button
    if st.button("Generate Carousel Content", type="primary"):
        if not business_type or not target_audience or not key_message:
            st.error("Please fill in the required fields: Business Type, Target Audience, and Key Message")
            return
        
        with st.spinner("Generating your carousel content..."):
            # Generate the carousel content
            carousel_content = generate_carousel_content(
                business_type=business_type,
                target_audience=target_audience,
                carousel_purpose=carousel_purpose,
                brand_voice=brand_voice,
                key_message=key_message,
                num_slides=num_slides,
                carousel_structure=carousel_structure,
                include_stats=include_stats,
                include_testimonials=include_testimonials,
                include_pricing=include_pricing,
                include_cta=include_cta,
                include_hashtags=include_hashtags,
                include_emojis=include_emojis,
                include_questions=include_questions,
                include_bullets=include_bullets,
                include_numbers=include_numbers,
                specific_features=specific_features,
                avoid_points=avoid_points
            )
            
            if carousel_content:
                # Store the content in session state for other tabs
                st.session_state['carousel_content'] = carousel_content
                display_carousel_content(carousel_content)
            else:
                st.error("Failed to generate carousel content. Please try again.")

def render_visual_elements_tab():
    """Render the Visual Elements tab for generating carousel images."""
    st.markdown("### Visual Elements for Your Carousel")
    
    # Check if carousel content has been generated
    if 'carousel_content' not in st.session_state:
        st.info("Please generate carousel content in the 'Content Setup' tab first.")
        return
    
    st.markdown("#### Visual Style Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        visual_style = st.selectbox(
            "Visual Style",
            options=[
                "Modern and Clean",
                "Bold and Vibrant",
                "Minimalist",
                "Luxury/Premium",
                "Playful and Fun",
                "Professional",
                "Artistic/Creative",
                "Natural/Organic",
                "Tech/Digital",
                "Custom"
            ],
            help="The overall visual style for your carousel"
        )
        
        if visual_style == "Custom":
            custom_style = st.text_input(
                "Custom Visual Style",
                placeholder="Describe your desired visual style"
            )
        
        color_scheme = st.selectbox(
            "Color Scheme",
            options=[
                "Brand Colors",
                "Monochromatic",
                "Complementary",
                "Analogous",
                "Neutral",
                "Warm",
                "Cool",
                "Custom"
            ],
            help="Color scheme for your carousel images"
        )
        
        if color_scheme == "Brand Colors":
            brand_colors = st.text_input(
                "Brand Colors (Hex Codes)",
                placeholder="#1877F2, #ffffff, etc.",
                help="Enter your brand colors as hex codes, separated by commas"
            )
    
    with col2:
        image_style = st.selectbox(
            "Image Style",
            options=[
                "Photography",
                "Illustration",
                "3D Rendering",
                "Flat Design",
                "Mixed Media",
                "Custom"
            ],
            help="The style of images to generate"
        )
        
        composition = st.selectbox(
            "Composition",
            options=[
                "Centered",
                "Rule of Thirds",
                "Asymmetrical",
                "Grid Layout",
                "Custom"
            ],
            help="How to compose the visual elements"
        )
        
        text_overlay = st.checkbox(
            "Include Text Overlays",
            value=True,
            help="Add text overlays to the images"
        )
    
    if text_overlay:
        st.markdown("#### Text Overlay Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            font_style = st.selectbox(
                "Font Style",
                options=[
                    "Modern Sans-serif",
                    "Classic Serif",
                    "Handwritten",
                    "Bold Display",
                    "Minimal"
                ],
                help="Style of text to overlay on images"
            )
            
            text_color = st.color_picker(
                "Text Color",
                "#FFFFFF",
                help="Color of the overlay text"
            )
        
        with col2:
            text_position = st.selectbox(
                "Text Position",
                options=[
                    "Center",
                    "Bottom",
                    "Top",
                    "Left",
                    "Right",
                    "Custom"
                ],
                help="Where to position the text overlay"
            )
            
            text_background = st.checkbox(
                "Add Text Background",
                value=True,
                help="Add a semi-transparent background behind text for better readability"
            )
    
    # Generate images button
    if st.button("Generate Carousel Images", type="primary"):
        with st.spinner("Generating visual elements for your carousel..."):
            # Generate the carousel images
            carousel_images = generate_carousel_images(
                carousel_content=st.session_state['carousel_content'],
                visual_style=visual_style,
                custom_style=custom_style if visual_style == "Custom" else None,
                color_scheme=color_scheme,
                brand_colors=brand_colors if color_scheme == "Brand Colors" else None,
                image_style=image_style,
                composition=composition,
                text_overlay=text_overlay,
                font_style=font_style if text_overlay else None,
                text_color=text_color if text_overlay else None,
                text_position=text_position if text_overlay else None,
                text_background=text_background if text_overlay else None
            )
            
            if carousel_images:
                # Store the images in session state for preview
                st.session_state['carousel_images'] = carousel_images
                display_carousel_images(carousel_images)
            else:
                st.error("Failed to generate carousel images. Please try again.")

def render_preview_export_tab():
    """Render the Preview & Export tab for reviewing and exporting the carousel."""
    st.markdown("### Preview Your Carousel")
    
    # Check if both content and images have been generated
    if 'carousel_content' not in st.session_state:
        st.info("Please generate carousel content in the 'Content Setup' tab first.")
        return
    
    if 'carousel_images' not in st.session_state:
        st.info("Please generate carousel images in the 'Visual Elements' tab.")
        return
    
    # Display carousel preview
    st.markdown("#### Final Preview")
    preview_carousel(
        st.session_state['carousel_content'],
        st.session_state['carousel_images']
    )
    
    # Export options
    st.markdown("### Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox(
            "Export Format",
            options=[
                "ZIP (All Files)",
                "PDF Report",
                "Individual Files"
            ],
            help="Choose how to export your carousel"
        )
    
    with col2:
        include_guidelines = st.checkbox(
            "Include Posting Guidelines",
            value=True,
            help="Add best practices and guidelines for posting"
        )
    
    if st.button("Export Carousel", type="primary"):
        with st.spinner("Preparing your carousel for export..."):
            export_carousel(
                carousel_content=st.session_state['carousel_content'],
                carousel_images=st.session_state['carousel_images'],
                export_format=export_format,
                include_guidelines=include_guidelines
            )

def generate_carousel_content(**kwargs) -> Dict[str, Any]:
    """
    Generate carousel content based on user inputs.
    """
    try:
        logger.info(f"[generate_carousel_content] Generating carousel content for {kwargs.get('business_type')}")
        
        # Construct the main prompt
        prompt = f"""You are a Facebook content expert. Create a carousel post in JSON format.

        Create content for a {kwargs.get('business_type')} business targeting {kwargs.get('target_audience')}.
        
        Purpose: {kwargs.get('carousel_purpose')}
        Brand Voice: {kwargs.get('brand_voice')}
        Key Message: {kwargs.get('key_message')}
        Structure Type: {kwargs.get('carousel_structure')}
        Number of Slides: {kwargs.get('num_slides')}
        
        Additional Requirements:
        {f"- Include relevant statistics and facts" if kwargs.get('include_stats') else ""}
        {f"- Include customer testimonials" if kwargs.get('include_testimonials') else ""}
        {f"- Include pricing information" if kwargs.get('include_pricing') else ""}
        {f"- Include strong call-to-action" if kwargs.get('include_cta') else ""}
        {f"- Include relevant hashtags" if kwargs.get('include_hashtags') else ""}
        {f"- Use appropriate emojis" if kwargs.get('include_emojis') else ""}
        {f"- Include engaging questions" if kwargs.get('include_questions') else ""}
        {f"- Use bullet points for clarity" if kwargs.get('include_bullets') else ""}
        {f"- Use numbered lists where appropriate" if kwargs.get('include_numbers') else ""}
        
        Specific Points to Include:
        {kwargs.get('specific_features')}
        
        Points to Avoid:
        {kwargs.get('avoid_points')}
        
        IMPORTANT: Respond ONLY with a valid JSON object using the following structure. Do not include any other text.

        {{
            "main_caption": "Write an engaging main caption for the carousel",
            "slides": [
                {{
                    "slide_number": 1,
                    "content": "Write engaging content for this slide",
                    "image_prompt": "Write a clear image generation prompt",
                    "overlay_text": "Write text to overlay on the image"
                }}
            ],
            "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
            "engagement_prompts": ["Write engaging question 1", "Write call to action 2", "Write engagement prompt 3"]
        }}
        """
        
        # Generate the content using the AI
        logger.info(f"[generate_carousel_content] Sending prompt to AI")
        response = llm_text_gen(prompt)
        
        if not response:
            logger.error(f"[generate_carousel_content] No response from AI")
            st.error("Failed to generate content. Please try again.")
            return None
        
        try:
            # Clean the response - remove any potential markdown formatting or extra text
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            # Parse the JSON response
            carousel_data = json.loads(response)
            
            # Validate the response structure
            required_keys = ['main_caption', 'slides', 'hashtags', 'engagement_prompts']
            if not all(key in carousel_data for key in required_keys):
                logger.error(f"[generate_carousel_content] Missing required keys in response")
                st.error("Generated content is missing required information. Please try again.")
                return None
            
            # Validate slides array
            if not carousel_data['slides'] or len(carousel_data['slides']) < 2:
                logger.error(f"[generate_carousel_content] Not enough slides generated")
                st.error("Not enough slides were generated. Please try again.")
                return None
            
            # Add metadata
            carousel_data['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'business_type': kwargs.get('business_type'),
                'target_audience': kwargs.get('target_audience'),
                'carousel_purpose': kwargs.get('carousel_purpose'),
                'brand_voice': kwargs.get('brand_voice'),
                'structure_type': kwargs.get('carousel_structure')
            }
            
            logger.info(f"[generate_carousel_content] Successfully generated carousel content")
            return carousel_data
            
        except json.JSONDecodeError as e:
            logger.error(f"[generate_carousel_content] JSON parsing error: {str(e)}")
            logger.error(f"[generate_carousel_content] Raw response: {response}")
            st.error("Error parsing the generated content. Please try again.")
            return None
            
    except Exception as e:
        logger.error(f"[generate_carousel_content] Error generating carousel content: {str(e)}")
        st.error("An unexpected error occurred. Please try again.")
        return None

def generate_carousel_images(**kwargs) -> List[str]:
    """
    Generate images for carousel slides.
    
    Args:
        carousel_content (Dict[str, Any]): The generated carousel content
        visual_style (str): Overall visual style
        custom_style (str, optional): Custom style description
        color_scheme (str): Color scheme selection
        brand_colors (str, optional): Brand color hex codes
        image_style (str): Style of images to generate
        composition (str): Image composition style
        text_overlay (bool): Whether to include text overlays
        font_style (str, optional): Style of overlay text
        text_color (str, optional): Color of overlay text
        text_position (str, optional): Position of overlay text
        text_background (bool, optional): Whether to add text background
        
    Returns:
        List[str]: List of paths to generated images
    """
    try:
        logger.info(f"[generate_carousel_images] Generating images with style: {kwargs.get('visual_style')}")
        
        carousel_content = kwargs.get('carousel_content', {})
        slides = carousel_content.get('slides', [])
        
        if not slides:
            logger.error(f"[generate_carousel_images] No slides found in carousel content")
            return None
        
        generated_images = []
        
        for slide in slides:
            # Construct the image generation prompt
            base_prompt = slide['image_prompt']
            
            style_prompt = f"""
            Style Requirements:
            - Visual Style: {kwargs.get('visual_style')}{f" - {kwargs.get('custom_style')}" if kwargs.get('custom_style') else ""}
            - Color Scheme: {kwargs.get('color_scheme')}{f" using colors: {kwargs.get('brand_colors')}" if kwargs.get('brand_colors') else ""}
            - Image Style: {kwargs.get('image_style')}
            - Composition: {kwargs.get('composition')}
            
            Additional Requirements:
            - Create a high-quality image suitable for Facebook carousel post
            - Ensure the image is visually engaging and professional
            - Maintain consistent branding and style across all slides
            - Optimize for mobile viewing
            """
            
            # Add text overlay requirements if enabled
            if kwargs.get('text_overlay'):
                overlay_text = slide.get('overlay_text', '')
                if overlay_text:
                    style_prompt += f"""
                    Text Overlay Requirements:
                    - Add the following text: "{overlay_text}"
                    - Font Style: {kwargs.get('font_style')}
                    - Text Color: {kwargs.get('text_color')}
                    - Text Position: {kwargs.get('text_position')}
                    {f"- Add semi-transparent background behind text" if kwargs.get('text_background') else ""}
                    - Ensure text is clearly readable
                    """
            
            # Combine prompts
            final_prompt = f"{base_prompt}\n\n{style_prompt}"
            
            # Generate the image
            logger.info(f"[generate_carousel_images] Generating image for slide {slide['slide_number']}")
            image_path = generate_image(final_prompt)
            
            if image_path:
                generated_images.append(image_path)
                logger.info(f"[generate_carousel_images] Successfully generated image for slide {slide['slide_number']}")
            else:
                logger.error(f"[generate_carousel_images] Failed to generate image for slide {slide['slide_number']}")
        
        return generated_images if generated_images else None
        
    except Exception as e:
        logger.error(f"[generate_carousel_images] Error generating carousel images: {str(e)}")
        return None

def display_carousel_content(content: Dict[str, Any]):
    """
    Display the generated carousel content in a structured and visually appealing way.
    
    Args:
        content: Dictionary containing the carousel content and metadata
    """
    try:
        # Create tabs for different content views
        tabs = st.tabs(["Full Preview", "Main Caption", "Slides", "Engagement Elements"])
        
        with tabs[0]:  # Full Preview
            st.markdown("### Complete Carousel Content")
            
            # Display metadata
            st.markdown("""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
                    <h4 style='color: #1877F2; margin-top: 0;'>Carousel Details</h4>
                    <p style='margin-bottom: 5px;'><strong>Business Type:</strong> {}</p>
                    <p style='margin-bottom: 5px;'><strong>Target Audience:</strong> {}</p>
                    <p style='margin-bottom: 5px;'><strong>Purpose:</strong> {}</p>
                    <p style='margin-bottom: 5px;'><strong>Brand Voice:</strong> {}</p>
                    <p style='margin-bottom: 0;'><strong>Structure:</strong> {}</p>
                </div>
            """.format(
                content['metadata']['business_type'],
                content['metadata']['target_audience'],
                content['metadata']['carousel_purpose'],
                content['metadata']['brand_voice'],
                content['metadata']['structure_type']
            ), unsafe_allow_html=True)
            
            # Display main caption
            st.markdown("#### Main Caption")
            st.markdown(f"""
                <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                    {content['main_caption']}
                </div>
            """, unsafe_allow_html=True)
            
            # Display slides
            st.markdown("#### Slides")
            for slide in content['slides']:
                with st.expander(f"Slide {slide['slide_number']}"):
                    st.markdown(f"**Content:** {slide['content']}")
                    st.markdown(f"**Image Prompt:** {slide['image_prompt']}")
                    if slide.get('overlay_text'):
                        st.markdown(f"**Overlay Text:** {slide['overlay_text']}")
            
            # Display hashtags and engagement prompts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Hashtags")
                st.markdown(" ".join([f"#{tag}" for tag in content['hashtags']]))
            
            with col2:
                st.markdown("#### Engagement Prompts")
                for prompt in content['engagement_prompts']:
                    st.markdown(f"- {prompt}")
        
        with tabs[1]:  # Main Caption
            st.markdown("### Main Caption")
            st.markdown(f"""
                <div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;'>
                    <h4 style='color: #1877F2; margin-top: 0;'>Caption Preview</h4>
                    {content['main_caption']}
                    <hr>
                    <p><strong>Hashtags:</strong></p>
                    {" ".join([f"#{tag}" for tag in content['hashtags']])}
                </div>
            """, unsafe_allow_html=True)
        
        with tabs[2]:  # Slides
            st.markdown("### Slide Content")
            
            # Create a grid of slides
            cols = st.columns(2)
            for i, slide in enumerate(content['slides']):
                with cols[i % 2]:
                    st.markdown(f"""
                        <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0; margin-bottom: 15px;'>
                            <h4 style='color: #1877F2; margin-top: 0;'>Slide {slide['slide_number']}</h4>
                            <p><strong>Content:</strong><br>{slide['content']}</p>
                            <p><strong>Image Prompt:</strong><br>{slide['image_prompt']}</p>
                            {f"<p><strong>Overlay Text:</strong><br>{slide['overlay_text']}</p>" if slide.get('overlay_text') else ""}
                        </div>
                    """, unsafe_allow_html=True)
        
        with tabs[3]:  # Engagement Elements
            st.markdown("### Engagement Elements")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                        <h4 style='color: #1877F2; margin-top: 0;'>Hashtags</h4>
                        <p>{}</p>
                    </div>
                """.format(" ".join([f"#{tag}" for tag in content['hashtags']])), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;'>
                        <h4 style='color: #1877F2; margin-top: 0;'>Engagement Prompts</h4>
                        <ul style='margin: 0; padding-left: 20px;'>
                            {}
                        </ul>
                    </div>
                """.format("".join([f"<li>{prompt}</li>" for prompt in content['engagement_prompts']])), unsafe_allow_html=True)
            
            # Add download button for the content
            st.download_button(
                label="Download Carousel Content",
                data=json.dumps(content, indent=2),
                file_name=f"carousel_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
    except Exception as e:
        logger.error(f"[display_carousel_content] Error displaying carousel content: {str(e)}")
        st.error("Error displaying carousel content. Please try again.")

def display_carousel_images(images: List[str]):
    """
    Display the generated carousel images in a visually appealing way.
    
    Args:
        images: List of paths to generated images
    """
    try:
        st.markdown("### Generated Carousel Images")
        
        # Create a tabbed interface for different views
        tabs = st.tabs(["Grid View", "Slideshow", "Individual Images"])
        
        with tabs[0]:  # Grid View
            st.markdown("#### Grid View")
            
            # Create a grid of images
            cols = st.columns(2)
            for i, image_path in enumerate(images):
                with cols[i % 2]:
                    st.image(image_path, use_container_width=True)
                    st.markdown(f"""
                        <div style='text-align: center; margin-bottom: 20px;'>
                            <p style='margin-bottom: 10px;'><strong>Slide {i+1}</strong></p>
                            <a href='{image_path}' download='carousel_slide_{i+1}.png' 
                               style='text-decoration: none; background-color: #1877F2; color: white; 
                                      padding: 5px 10px; border-radius: 5px;'>
                                Download Image
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
        
        with tabs[1]:  # Slideshow
            st.markdown("#### Slideshow View")
            
            # Create a simple slideshow
            current_slide = st.slider("Select Slide", 1, len(images), 1)
            st.image(images[current_slide-1], use_container_width=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if current_slide > 1:
                    if st.button("← Previous"):
                        st.session_state['current_slide'] = current_slide - 1
            with col2:
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <p>Slide {current_slide} of {len(images)}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                if current_slide < len(images):
                    if st.button("Next →"):
                        st.session_state['current_slide'] = current_slide + 1
        
        with tabs[2]:  # Individual Images
            st.markdown("#### Individual Images")
            
            for i, image_path in enumerate(images):
                with st.expander(f"Slide {i+1}"):
                    st.image(image_path, use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label=f"Download Slide {i+1}",
                            data=open(image_path, "rb").read(),
                            file_name=f"carousel_slide_{i+1}.png",
                            mime="image/png"
                        )
                    with col2:
                        st.markdown(f"""
                            <div style='background-color: #f8f9fa; padding: 10px; border-radius: 5px;'>
                                <p style='margin: 0;'><strong>Image Details:</strong></p>
                                <p style='margin: 0;'>Format: PNG</p>
                                <p style='margin: 0;'>Optimized for Facebook</p>
                            </div>
                        """, unsafe_allow_html=True)
        
        # Add a download all button
        st.markdown("### Bulk Download")
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px;'>
                <h4 style='margin-top: 0;'>Download All Images</h4>
                <p style='margin-bottom: 10px;'>Get all carousel images in a single ZIP file.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create a ZIP file containing all images
        import io
        import zipfile
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i, image_path in enumerate(images):
                zip_file.write(image_path, f"carousel_slide_{i+1}.png")
        
        st.download_button(
            label="Download All Images (ZIP)",
            data=zip_buffer.getvalue(),
            file_name=f"carousel_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip"
        )
        
    except Exception as e:
        logger.error(f"[display_carousel_images] Error displaying carousel images: {str(e)}")
        st.error("Error displaying carousel images. Please try again.")

def preview_carousel(content: Dict[str, Any], images: List[str]):
    """
    Show a preview of the complete carousel.
    
    Args:
        content: Dictionary containing the carousel content
        images: List of paths to generated images
    """
    try:
        st.markdown("### Carousel Preview")
        
        # Create tabs for different preview modes
        tabs = st.tabs(["Mobile Preview", "Desktop Preview", "Content Overview"])
        
        with tabs[0]:  # Mobile Preview
            st.markdown("#### Mobile View")
            st.markdown("""
                <div style='max-width: 400px; margin: 0 auto; background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>
                        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Facebook_f_logo_%282019%29.svg/100px-Facebook_f_logo_%282019%29.svg.png' 
                             style='width: 24px; height: 24px; vertical-align: middle;'>
                        <span style='margin-left: 10px; font-weight: bold;'>Your Business Page</span>
                    </div>
            """, unsafe_allow_html=True)
            
            # Display the main caption
            st.markdown(f"""
                <div style='margin-bottom: 15px;'>
                    {content['main_caption']}
                </div>
            """, unsafe_allow_html=True)
            
            # Display the carousel images
            current_slide = st.slider("Swipe through slides", 1, len(images), 1, key="mobile_slider")
            st.image(images[current_slide-1], use_container_width=True)
            
            # Display slide indicators
            st.markdown(f"""
                <div style='text-align: center; margin-top: 10px;'>
                    {"".join(['●' if i+1 == current_slide else '○' for i in range(len(images))])}
                </div>
            """, unsafe_allow_html=True)
            
            # Display engagement elements
            st.markdown("""
                <div style='margin-top: 15px;'>
                    <span style='margin-right: 15px;'>👍 Like</span>
                    <span style='margin-right: 15px;'>💬 Comment</span>
                    <span>↗️ Share</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[1]:  # Desktop Preview
            st.markdown("#### Desktop View")
            
            # Create a wider preview container
            st.markdown("""
                <div style='max-width: 800px; margin: 0 auto; background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>
                        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Facebook_f_logo_%282019%29.svg/100px-Facebook_f_logo_%282019%29.svg.png' 
                             style='width: 24px; height: 24px; vertical-align: middle;'>
                        <span style='margin-left: 10px; font-weight: bold;'>Your Business Page</span>
                    </div>
            """, unsafe_allow_html=True)
            
            # Display content and images side by side
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Display the carousel images in a row
                st.image(images[0], use_container_width=True)
                
                # Small image previews
                cols = st.columns(len(images))
                for i, image in enumerate(images):
                    with cols[i]:
                        st.image(image, use_container_width=True)
            
            with col2:
                # Display the main caption and engagement elements
                st.markdown(f"""
                    <div style='padding: 15px;'>
                        <p>{content['main_caption']}</p>
                        <div style='margin-top: 15px;'>
                            <p><strong>Hashtags:</strong></p>
                            <p>{" ".join([f"#{tag}" for tag in content['hashtags']])}</p>
                        </div>
                        <div style='margin-top: 15px;'>
                            <span style='margin-right: 15px;'>👍 Like</span>
                            <span style='margin-right: 15px;'>💬 Comment</span>
                            <span>↗️ Share</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[2]:  # Content Overview
            st.markdown("#### Content Overview")
            
            # Display metadata
            st.markdown("""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
                    <h4 style='color: #1877F2; margin-top: 0;'>Carousel Details</h4>
                    <p><strong>Total Slides:</strong> {}</p>
                    <p><strong>Generated:</strong> {}</p>
                    <p><strong>Purpose:</strong> {}</p>
                </div>
            """.format(
                len(images),
                content['metadata']['generated_at'],
                content['metadata']['carousel_purpose']
            ), unsafe_allow_html=True)
            
            # Display content structure
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Content Elements")
                st.markdown("""
                    - Main Caption
                    - {} Slides
                    - {} Hashtags
                    - {} Engagement Prompts
                """.format(
                    len(content['slides']),
                    len(content['hashtags']),
                    len(content['engagement_prompts'])
                ))
            
            with col2:
                st.markdown("##### Optimization Tips")
                st.markdown("""
                    - Best time to post: 1-4 PM
                    - Tag relevant accounts
                    - Respond to early comments
                    - Share to Stories for more reach
                    - Use all 10 hashtags for maximum visibility
                """)
    
    except Exception as e:
        logger.error(f"[preview_carousel] Error previewing carousel: {str(e)}")
        st.error("Error displaying carousel preview. Please try again.")

def export_carousel(**kwargs):
    """
    Export the carousel in the chosen format.
    
    Args:
        carousel_content (Dict[str, Any]): The carousel content
        carousel_images (List[str]): List of image paths
        export_format (str): Chosen export format
        include_guidelines (bool): Whether to include posting guidelines
    """
    try:
        content = kwargs.get('carousel_content')
        images = kwargs.get('carousel_images')
        export_format = kwargs.get('export_format')
        include_guidelines = kwargs.get('include_guidelines')
        
        if export_format == "ZIP (All Files)":
            # Create a ZIP file containing all carousel assets
            import io
            import zipfile
            from datetime import datetime
            
            # Create guidelines if requested
            if include_guidelines:
                guidelines = f"""
                Facebook Carousel Posting Guidelines
                =================================

                Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                Carousel Details
                ---------------
                - Business Type: {content['metadata']['business_type']}
                - Target Audience: {content['metadata']['target_audience']}
                - Purpose: {content['metadata']['carousel_purpose']}

                Posting Instructions
                -------------------
                1. Upload all images in the correct order
                2. Copy the main caption from caption.txt
                3. Add all hashtags (found in hashtags.txt)
                4. Best posting times: 1-4 PM on weekdays
                5. Share to Stories after posting
                6. Engage with comments within the first hour

                Engagement Strategy
                ------------------
                - Use the provided engagement prompts
                - Respond to comments quickly
                - Tag relevant accounts when appropriate
                - Share to relevant groups
                - Consider boosting the post

                Hashtag Strategy
                ---------------
                - Use all provided hashtags
                - Mix popular and niche hashtags
                - Place hashtags in first comment for cleaner look

                Additional Tips
                --------------
                - Monitor performance for the first 24 hours
                - Save top-performing carousel slides as templates
                - A/B test different carousel orders
                - Use insights to optimize future posts
                """
            
            # Create the ZIP file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                # Add images
                for i, image_path in enumerate(images):
                    zip_file.write(image_path, f"images/slide_{i+1}.png")
                
                # Add content files
                zip_file.writestr("caption.txt", content['main_caption'])
                zip_file.writestr("hashtags.txt", "\n".join([f"#{tag}" for tag in content['hashtags']]))
                zip_file.writestr("engagement_prompts.txt", "\n".join(content['engagement_prompts']))
                
                # Add slides content
                slides_content = "\n\n".join([
                    f"Slide {slide['slide_number']}:\n{slide['content']}"
                    for slide in content['slides']
                ])
                zip_file.writestr("slides_content.txt", slides_content)
                
                # Add metadata
                zip_file.writestr("metadata.json", json.dumps(content['metadata'], indent=2))
                
                # Add guidelines if requested
                if include_guidelines:
                    zip_file.writestr("posting_guidelines.txt", guidelines)
            
            # Offer the ZIP file for download
            st.download_button(
                label="Download Complete Carousel Package",
                data=zip_buffer.getvalue(),
                file_name=f"facebook_carousel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip"
            )
            
            st.success("Your carousel package has been prepared for download!")
            
        elif export_format == "PDF Report":
            # Create a PDF report
            st.info("PDF export functionality coming soon!")
            
        elif export_format == "Individual Files":
            # Offer individual file downloads
            st.markdown("### Download Individual Files")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Content files
                st.markdown("#### Content Files")
                
                st.download_button(
                    label="Download Caption",
                    data=content['main_caption'],
                    file_name="carousel_caption.txt",
                    mime="text/plain"
                )
                
                st.download_button(
                    label="Download Hashtags",
                    data="\n".join([f"#{tag}" for tag in content['hashtags']]),
                    file_name="carousel_hashtags.txt",
                    mime="text/plain"
                )
                
                st.download_button(
                    label="Download Engagement Prompts",
                    data="\n".join(content['engagement_prompts']),
                    file_name="carousel_engagement_prompts.txt",
                    mime="text/plain"
                )
            
            with col2:
                # Image files
                st.markdown("#### Image Files")
                
                for i, image_path in enumerate(images):
                    st.download_button(
                        label=f"Download Slide {i+1}",
                        data=open(image_path, "rb").read(),
                        file_name=f"carousel_slide_{i+1}.png",
                        mime="image/png",
                        key=f"download_slide_{i+1}"
                    )
        
        # Display export success message
        st.success("Export completed successfully!")
        
    except Exception as e:
        logger.error(f"[export_carousel] Error exporting carousel: {str(e)}")
        st.error("Error exporting carousel. Please try again.") 