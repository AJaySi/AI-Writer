"""
Streamlit UI for Enhanced Blog Outline Generator

This module provides a user-friendly interface for generating comprehensive blog outlines
with AI-powered content and image generation capabilities.
"""

import streamlit as st
import asyncio
from pathlib import Path
from typing import Optional, Dict, List
import json
import time
from datetime import datetime

from .get_blog_outline import (
    BlogOutlineGenerator,
    OutlineConfig,
    ContentType,
    ContentDepth,
    OutlineStyle
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 4px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .section-card {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .content-preview {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .image-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .stats-card {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .edit-section {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .subsection-list {
        margin-left: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def edit_section_content(section: str, content: str) -> str:
    """Edit section content with advanced options."""
    st.markdown('<div class="edit-section">', unsafe_allow_html=True)
    
    # Content editing
    edited_content = st.text_area(
        "Edit Content",
        value=content,
        height=300,
        key=f"content_edit_{section}"
    )
    
    # Word count and formatting
    col1, col2 = st.columns(2)
    with col1:
        word_count = len(edited_content.split())
        st.info(f"Word Count: {word_count}")
    
    with col2:
        formatting = st.multiselect(
            "Formatting Options",
            ["Bold", "Italic", "Lists", "Code Blocks", "Links"],
            key=f"format_{section}"
        )
    
    # AI enhancement options
    with st.expander("AI Enhancement Options"):
        enhance_options = st.multiselect(
            "Select Enhancements",
            ["Improve Clarity", "Add Examples", "Expand Details", "Add Statistics", "Improve SEO"],
            key=f"enhance_{section}"
        )
        
        if st.button("Apply Enhancements", key=f"apply_enhance_{section}"):
            with st.spinner("Applying enhancements..."):
                # TODO: Implement AI enhancement logic
                st.success("Enhancements applied!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return edited_content

def edit_subsections(section: str, subsections: List[str]) -> List[str]:
    """Edit subsections with reordering and editing capabilities."""
    st.markdown('<div class="edit-section">', unsafe_allow_html=True)
    
    # Reorder subsections
    st.markdown("### Reorder Subsections")
    for i, subsection in enumerate(subsections):
        col1, col2 = st.columns([4, 1])
        with col1:
            subsections[i] = st.text_input(
                f"Subsection {i+1}",
                value=subsection,
                key=f"subsection_{section}_{i}"
            )
        with col2:
            if st.button("↑", key=f"move_up_{section}_{i}") and i > 0:
                subsections[i], subsections[i-1] = subsections[i-1], subsections[i]
                st.experimental_rerun()
            if st.button("↓", key=f"move_down_{section}_{i}") and i < len(subsections)-1:
                subsections[i], subsections[i+1] = subsections[i+1], subsections[i]
                st.experimental_rerun()
    
    # Add/remove subsections
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Subsection", key=f"add_sub_{section}"):
            subsections.append("New Subsection")
            st.experimental_rerun()
    with col2:
        if st.button("Remove Last Subsection", key=f"remove_sub_{section}"):
            if subsections:
                subsections.pop()
                st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return subsections

def edit_section_metadata(section: str, generator: BlogOutlineGenerator):
    """Edit section metadata and settings."""
    st.markdown('<div class="edit-section">', unsafe_allow_html=True)
    
    # Section settings
    st.markdown("### Section Settings")
    
    # Image settings
    if generator.config.include_images:
        col1, col2 = st.columns(2)
        with col1:
            new_image_style = st.selectbox(
                "Image Style",
                ["realistic", "illustration", "minimalist", "photographic", "artistic"],
                key=f"img_style_{section}"
            )
        with col2:
            new_image_engine = st.selectbox(
                "Image Engine",
                ["Gemini-AI", "Dalle3", "Stability-AI"],
                key=f"img_engine_{section}"
            )
        
        if st.button("Regenerate Image", key=f"regen_img_{section}"):
            with st.spinner("Regenerating image..."):
                # TODO: Implement image regeneration logic
                st.success("Image regenerated!")
    
    # Content settings
    st.markdown("### Content Settings")
    col1, col2 = st.columns(2)
    with col1:
        target_word_count = st.number_input(
            "Target Word Count",
            min_value=100,
            max_value=2000,
            value=500,
            step=100,
            key=f"word_count_{section}"
        )
    with col2:
        content_depth = st.selectbox(
            "Content Depth",
            [depth.value for depth in ContentDepth],
            key=f"depth_{section}"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_section(section: str, subsections: List[str], content: Optional[Dict] = None, generator: Optional[BlogOutlineGenerator] = None):
    """Display a section with its content and subsections."""
    st.markdown(f"""
        <div class="section-card">
            <h2>{section}</h2>
    """, unsafe_allow_html=True)
    
    # Section editing controls
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"### {section}")
    with col2:
        edit_mode = st.checkbox("Edit Mode", key=f"edit_mode_{section}")
    
    if content:
        # Display content with word count
        word_count = len(content.content.split())
        st.markdown(f"""
            <div class="content-preview">
                <p><strong>Content Preview</strong> ({word_count} words)</p>
                {content.content[:500]}...
            </div>
        """, unsafe_allow_html=True)
        
        # Display image if available
        if content.image_path:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(content.image_path, caption=section, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display image prompt in expander
            if content.image_prompt:
                with st.expander("View Image Prompt"):
                    st.code(content.image_prompt, language="text")
        
        # Edit mode controls
        if edit_mode:
            # Edit content
            edited_content = edit_section_content(section, content.content)
            content.content = edited_content
            
            # Edit subsections
            edited_subsections = edit_subsections(section, subsections)
            subsections[:] = edited_subsections
            
            # Edit metadata
            if generator:
                edit_section_metadata(section, generator)
    
    # Display subsections
    st.markdown("### Subsections")
    st.markdown('<div class="subsection-list">', unsafe_allow_html=True)
    for subsection in subsections:
        st.markdown(f"- {subsection}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_stats(generator, outline):
    """Display statistics about the generated outline."""
    total_sections = len(outline)
    total_subsections = sum(len(subsections) for subsections in outline.values())
    total_content = sum(len(content.content.split()) for content in generator.section_contents.values())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="stats-card">
                <h3>📊 Statistics</h3>
                <p>Total Sections: {total_sections}</p>
                <p>Total Subsections: {total_subsections}</p>
                <p>Estimated Word Count: {total_content}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stats-card">
                <h3>🎯 Target</h3>
                <p>Target Word Count: {generator.config.target_word_count}</p>
                <p>Content Depth: {generator.config.content_depth.value}</p>
                <p>Style: {generator.config.outline_style.value}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stats-card">
                <h3>📝 Content Type</h3>
                <p>Type: {generator.config.content_type.value}</p>
                <p>Audience: {generator.config.target_audience}</p>
                <p>Language: {generator.config.language}</p>
            </div>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Blog Outline Generator",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header with description
    st.title("Blog Outline Generator")
    st.markdown("""
        Generate comprehensive blog outlines with AI-powered content and images.
        Customize your outline with various options and get detailed content for each section.
    """)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Basic settings
        topic = st.text_input("Blog Topic", placeholder="Enter your blog topic")
        content_type = st.selectbox(
            "Content Type",
            [type.value for type in ContentType]
        )
        content_depth = st.selectbox(
            "Content Depth",
            [depth.value for depth in ContentDepth]
        )
        outline_style = st.selectbox(
            "Outline Style",
            [style.value for style in OutlineStyle]
        )
        
        # Content structure
        st.subheader("Content Structure")
        target_word_count = st.slider("Target Word Count", 500, 5000, 2000, 100)
        num_main_sections = st.slider("Number of Main Sections", 3, 10, 5)
        num_subsections = st.slider("Subsections per Section", 2, 5, 3)
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            include_intro = st.checkbox("Include Introduction", value=True)
            include_conclusion = st.checkbox("Include Conclusion", value=True)
            include_faqs = st.checkbox("Include FAQs", value=True)
            include_resources = st.checkbox("Include Resources", value=True)
            
            # Image settings
            st.subheader("Image Settings")
            include_images = st.checkbox("Include Images", value=True)
            if include_images:
                image_style = st.selectbox(
                    "Image Style",
                    ["realistic", "illustration", "minimalist", "photographic", "artistic"]
                )
                image_engine = st.selectbox(
                    "Image Engine",
                    ["Gemini-AI", "Dalle3", "Stability-AI"]
                )
            
            # Target audience and language
            st.subheader("Target Audience")
            target_audience = st.text_input("Target Audience", value="general")
            language = st.text_input("Language", value="English")
            
            # Keywords and exclusions
            st.subheader("Content Optimization")
            keywords = st.text_area("Keywords (comma-separated)")
            exclude_topics = st.text_area("Topics to Exclude (comma-separated)")
    
    # Main content area
    if topic:
        # Create configuration
        config = OutlineConfig(
            content_type=ContentType(content_type),
            content_depth=ContentDepth(content_depth),
            outline_style=OutlineStyle(outline_style),
            target_word_count=target_word_count,
            num_main_sections=num_main_sections,
            num_subsections_per_section=num_subsections,
            include_introduction=include_intro,
            include_conclusion=include_conclusion,
            include_faqs=include_faqs,
            include_resources=include_resources,
            include_images=include_images,
            image_style=image_style if include_images else "realistic",
            image_engine=image_engine if include_images else "Gemini-AI",
            target_audience=target_audience,
            language=language,
            keywords=[k.strip() for k in keywords.split(',')] if keywords else None,
            exclude_topics=[t.strip() for t in exclude_topics.split(',')] if exclude_topics else None
        )
        
        # Initialize generator
        generator = BlogOutlineGenerator(config)
        
        # Generate outline
        if st.button("Generate Outline"):
            with st.spinner("Generating outline and content..."):
                try:
                    # Add progress bar
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    outline = asyncio.run(generator.generate_outline(topic))
                    
                    # Display results
                    st.success("Outline generated successfully!")
                    
                    # Display statistics
                    display_stats(generator, outline)
                    
                    # Output format selection
                    output_format = st.radio(
                        "Output Format",
                        ["Preview", "Markdown", "JSON", "HTML"]
                    )
                    
                    if output_format == "Preview":
                        # Display outline with content and images
                        for section, subsections in outline.items():
                            content = generator.section_contents.get(section)
                            display_section(section, subsections, content)
                    
                    elif output_format == "Markdown":
                        st.code(generator.to_markdown(), language="markdown")
                        st.download_button(
                            "Download Markdown",
                            generator.to_markdown(),
                            file_name="blog_outline.md",
                            mime="text/markdown"
                        )
                    
                    elif output_format == "JSON":
                        json_output = json.dumps({
                            "outline": outline,
                            "contents": {
                                section: {
                                    "title": content.title,
                                    "content": content.content,
                                    "image_prompt": content.image_prompt,
                                    "image_path": content.image_path
                                }
                                for section, content in generator.section_contents.items()
                            }
                        }, indent=2)
                        st.code(json_output, language="json")
                        st.download_button(
                            "Download JSON",
                            json_output,
                            file_name="blog_outline.json",
                            mime="application/json"
                        )
                    
                    elif output_format == "HTML":
                        # Add HTML export functionality
                        html_output = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>{topic} - Blog Outline</title>
                            <style>
                                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                                .section {{ margin-bottom: 30px; }}
                                .content {{ background: #f8f9fa; padding: 15px; border-radius: 4px; }}
                                img {{ max-width: 100%; height: auto; }}
                            </style>
                        </head>
                        <body>
                            <h1>{topic}</h1>
                            {generator.to_markdown().replace('#', '##')}
                        </body>
                        </html>
                        """
                        st.code(html_output, language="html")
                        st.download_button(
                            "Download HTML",
                            html_output,
                            file_name="blog_outline.html",
                            mime="text/html"
                        )
                
                except Exception as e:
                    st.error(f"Error generating outline: {str(e)}")
    else:
        st.info("Please enter a blog topic to get started.")

if __name__ == "__main__":
    main() 