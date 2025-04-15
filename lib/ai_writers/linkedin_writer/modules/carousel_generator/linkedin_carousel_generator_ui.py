import streamlit as st
import json
from typing import Optional, List
from .linkedin_carousel_generator import LinkedInCarouselGenerator, CarouselSlide

def linkedin_carousel_generator_ui():
    """Streamlit UI for LinkedIn Carousel Generator."""
    st.title("LinkedIn Carousel Generator")
    st.write("Create engaging carousel posts for LinkedIn with AI-powered content generation.")
    
    # Initialize session state
    if 'generator' not in st.session_state:
        st.session_state.generator = LinkedInCarouselGenerator()
    if 'slides' not in st.session_state:
        st.session_state.slides = []
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0
        
    # Sidebar for input parameters
    with st.sidebar:
        st.header("Carousel Parameters")
        topic = st.text_input("Topic", help="Enter the main topic for your carousel")
        num_slides = st.slider("Number of Slides", min_value=3, max_value=10, value=5, 
                             help="Choose how many slides you want in your carousel")
        
        if st.button("Generate Carousel"):
            if not topic:
                st.error("Please enter a topic")
                return
                
            with st.spinner("Generating carousel content..."):
                success = st.session_state.generator.generate_slide_content(topic, num_slides)
                if success:
                    st.session_state.slides = st.session_state.generator.slides
                    st.session_state.current_slide = 0
                    st.success("Carousel content generated successfully!")
                else:
                    st.error("Failed to generate carousel content. Please try again.")
    
    # Main content area
    if st.session_state.slides:
        # Display current slide
        current_slide = st.session_state.slides[st.session_state.current_slide]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"Slide {current_slide.index}")
            st.write("**Heading:**")
            st.write(current_slide.heading)
            st.write("**Subheading:**")
            st.write(current_slide.subheading)
            st.write("**Content:**")
            st.write(current_slide.content)
            st.write("**Image Prompt:**")
            st.write(current_slide.image_prompt)
            
            # Navigation buttons
            col_prev, col_next = st.columns(2)
            with col_prev:
                if st.session_state.current_slide > 0:
                    if st.button("← Previous"):
                        st.session_state.current_slide -= 1
                        st.experimental_rerun()
            with col_next:
                if st.session_state.current_slide < len(st.session_state.slides) - 1:
                    if st.button("Next →"):
                        st.session_state.current_slide += 1
                        st.experimental_rerun()
        
        with col2:
            # Display structured output
            st.subheader("Carousel Structure")
            carousel_data = {
                "slides": [
                    {
                        "index": slide.index,
                        "heading": slide.heading,
                        "subheading": slide.subheading,
                        "content": slide.content,
                        "image_prompt": slide.image_prompt
                    }
                    for slide in st.session_state.slides
                ]
            }
            st.json(carousel_data)
            
            # Export options
            st.download_button(
                "Download as JSON",
                data=json.dumps(carousel_data, indent=2),
                file_name="carousel_content.json",
                mime="application/json"
            )
            
            if st.button("Generate Images"):
                with st.spinner("Generating images for slides..."):
                    for slide in st.session_state.slides:
                        if not slide.image_path:
                            image_path = st.session_state.generator.generate_slide_image(slide)
                            if image_path:
                                slide.image_path = image_path
                                st.success(f"Generated image for slide {slide.index}")
                            else:
                                st.error(f"Failed to generate image for slide {slide.index}")
    
    else:
        st.info("Enter a topic and click 'Generate Carousel' to create your carousel content.") 