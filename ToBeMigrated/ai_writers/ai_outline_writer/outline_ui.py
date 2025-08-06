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
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    /* Add specific styling for the generate outline button */
    .generate-outline-button {
        width: 100%;
        margin: 20px 0;
    }
    .generate-outline-button > button {
        width: 100%;
        height: 50px;
        font-size: 1.2rem;
    }
    .section-card {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        width: 100%;
    }
    .content-preview {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
        width: 100%;
    }
    .image-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
        width: 100%;
    }
    .stats-card {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        width: 100%;
    }
    .edit-section {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
        width: 100%;
    }
    .subsection-list {
        margin-left: 20px;
        width: 100%;
    }
    /* Main container width */
    .main .block-container {
        max-width: 100%;
        padding: 2rem;
    }
    /* Full width for the outline display */
    .outline-container {
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
        padding: 20px;
    }
    /* Section styling */
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    .subsection-item {
        font-size: 1.1rem;
        color: #34495e;
        margin: 0.5rem 0;
        padding-left: 1rem;
    }
    /* Content area styling */
    .content-area {
        background-color: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    /* Make sure all Streamlit elements use full width */
    .stMarkdown, .stText, .stTextArea, .stSelectbox, .stSlider {
        width: 100% !important;
    }
    /* Full width for code blocks */
    .stCodeBlock {
        width: 100% !important;
    }
    /* Full width for the main content */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    /* Adjust the main content area */
    .main .block-container > div {
        max-width: 100%;
    }
    /* Make sure the outline content uses full width */
    .outline-content {
        width: 100%;
        max-width: 100%;
        margin: 0;
        padding: 0;
    }
    /* Adjust the preview section */
    .preview-section {
        width: 100%;
        max-width: 100%;
        margin: 0;
        padding: 1rem;
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
            <div class="section-header">{section}</div>
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
        
        # Image generation and display - Always show if images are enabled
        if generator and generator.config.include_images:
            st.markdown("### Image Generation")
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                image_style = st.selectbox(
                    "Image Style",
                    ["realistic", "illustration", "minimalist", "photographic", "artistic"],
                    index=["realistic", "illustration", "minimalist", "photographic", "artistic"].index(generator.config.image_style),
                    key=f"img_style_{section}"
                )
            
            with col2:
                image_engine = st.selectbox(
                    "Image Engine",
                    ["Gemini-AI", "Dalle3", "Stability-AI"],
                    index=["Gemini-AI", "Dalle3", "Stability-AI"].index(generator.config.image_engine),
                    key=f"img_engine_{section}"
                )
            
            with col3:
                if st.button("Generate Image", key=f"gen_img_{section}"):
                    with st.spinner(f"Generating image for {section}..."):
                        # Update config with selected options
                        generator.config.image_style = image_style
                        generator.config.image_engine = image_engine
                        image_path = generator.generate_section_image(section)
                        if image_path:
                            st.success("Image generated successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to generate image")
            
            # Display existing image if available
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
            st.markdown("### Edit Content")
            # Edit content
            edited_content = edit_section_content(section, content.content)
            if edited_content != content.content:
                content.content = edited_content
                st.experimental_rerun()
            
            st.markdown("### Edit Subsections")
            # Edit subsections
            edited_subsections = edit_subsections(section, subsections)
            if edited_subsections != subsections:
                subsections[:] = edited_subsections
                st.experimental_rerun()
            
            st.markdown("### Edit Metadata")
            # Edit metadata
            if generator:
                edit_section_metadata(section, generator)
        else:
            # Display subsections in view mode
            st.markdown("### Subsections")
            st.markdown('<div class="subsection-list">', unsafe_allow_html=True)
            for subsection in subsections:
                st.markdown(f'<div class="subsection-item">• {subsection}</div>', unsafe_allow_html=True)
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
    # Header with description
    st.title("Blog Outline Generator")
    st.markdown("""
        Generate comprehensive blog outlines with AI-powered content and images.
        Customize your outline with various options and get detailed content for each section.
    """)
    
    # Main content area with full width
    st.markdown('<div class="outline-container">', unsafe_allow_html=True)
    
    # Move topic input to main area and make it more prominent
    st.markdown("### Enter Your Blog Topic")
    topic = st.text_input("", placeholder="Enter your blog topic here for creating outline...", key="blog_topic")
    
    st.markdown("---")  # Add a separator
    st.markdown("### Configuration Options")
    
    # Create tabs for different configuration sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Content Type & Target",
        "📊 Content Structure",
        "🎨 Style & Sections",
        "🖼️ Image & Optimization"
    ])
    
    with tab1:
        st.markdown("#### Content Type & Target")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            content_type = st.selectbox(
                "Content Type",
                [type.value for type in ContentType],
                index=[type.value for type in ContentType].index(ContentType.GUIDE.value),
                help="Select the type of content you want to generate"
            )
        
        with col2:
            target_audience = st.selectbox(
                "Target Audience",
                ["General", "Technical", "Professional", "Academic", "Business", "Students", "Developers"],
                index=0,
                help="Select your target audience"
            )
        
        with col3:
            language = st.selectbox(
                "Language",
                ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese", "Korean"],
                index=0,
                help="Select the language for your content"
            )
    
    with tab2:
        st.markdown("#### Content Structure")
        col1, col2 = st.columns(2)
        
        with col1:
            num_main_sections = st.slider(
                "Number of Main Sections",
                min_value=3,
                max_value=10,
                value=5,
                step=1,
                help="Choose how many main sections your outline should have"
            )
            
            num_subsections = st.slider(
                "Subsections per Section",
                min_value=2,
                max_value=5,
                value=3,
                step=1,
                help="Choose how many subsections each main section should have"
            )
        
        with col2:
            target_word_count = st.slider(
                "Target Word Count",
                min_value=500,
                max_value=5000,
                value=2000,
                step=100,
                help="Set your target word count for the entire blog post"
            )
            
            # Display content statistics
            st.markdown("##### Content Statistics")
            st.markdown(f"""
                - Estimated Sections: {num_main_sections}
                - Total Subsections: {num_main_sections * num_subsections}
                - Target Word Count: {target_word_count}
                - Average Words per Section: {target_word_count // num_main_sections}
            """)
    
    with tab3:
        st.markdown("#### Style & Sections")
        col1, col2 = st.columns(2)
        
        with col1:
            content_depth = st.selectbox(
                "Content Depth",
                [depth.value for depth in ContentDepth],
                index=[depth.value for depth in ContentDepth].index(ContentDepth.INTERMEDIATE.value),
                help="Select the depth of content coverage"
            )
            
            outline_style = st.selectbox(
                "Outline Style",
                [style.value for style in OutlineStyle],
                index=[style.value for style in OutlineStyle].index(OutlineStyle.MODERN.value),
                help="Select the style of your outline"
            )
        
        with col2:
            st.markdown("##### Additional Sections")
            include_intro = st.checkbox("Include Introduction", value=True, help="Add an introduction section")
            include_conclusion = st.checkbox("Include Conclusion", value=True, help="Add a conclusion section")
            include_faqs = st.checkbox("Include FAQs", value=True, help="Add a FAQ section")
            include_resources = st.checkbox("Include Resources", value=True, help="Add a resources section")
    
    with tab4:
        st.markdown("#### Image & Optimization")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Image Settings")
            include_images = st.checkbox("Enable Image Generation", value=True, help="Enable AI image generation for sections")
            
            if include_images:
                image_style = st.selectbox(
                    "Image Style",
                    ["realistic", "illustration", "minimalist", "photographic", "artistic"],
                    index=0,
                    help="Select the style for generated images"
                )
                
                image_engine = st.selectbox(
                    "Image Engine",
                    ["Gemini-AI", "Dalle3", "Stability-AI"],
                    index=0,
                    help="Select the AI engine for image generation"
                )
        
        with col2:
            st.markdown("##### Content Optimization")
            keywords = st.text_area(
                "Keywords (comma-separated)",
                help="Enter keywords for SEO optimization, separated by commas"
            )
            
            exclude_topics = st.text_area(
                "Topics to Exclude (comma-separated)",
                help="Enter topics you want to exclude from the content"
            )
    
    st.markdown("---")  # Add a separator before the generate button
    
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
    
    # Store the generated outline in session state
    if 'outline' not in st.session_state:
        st.session_state.outline = None
    if 'section_contents' not in st.session_state:
        st.session_state.section_contents = {}
    
    # Generate outline button with full width
    st.markdown('<div class="generate-outline-button">', unsafe_allow_html=True)
    if not topic:
        st.warning("Please enter a blog topic to generate the outline.")
    if st.button("Generate Outline", type="primary", use_container_width=True, disabled=not topic):
        with st.spinner("Generating outline and content..."):
            try:
                # Add progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                outline = generator.generate_outline(topic)
                st.session_state.outline = outline
                st.session_state.section_contents = generator.section_contents
                
                # Display results
                st.success("Outline generated successfully!")
                
                # Add copy button and display outline in full width
                st.markdown('<div class="outline-content">', unsafe_allow_html=True)
                outline_text = json.dumps(outline, indent=2)
                st.code(outline_text, language="json")
                st.button("Copy Outline", key="copy_outline", 
                        help="Copy the outline to clipboard",
                        on_click=lambda: st.write(f'<script>navigator.clipboard.writeText(`{outline_text}`)</script>', 
                                                unsafe_allow_html=True))
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display statistics
                display_stats(generator, outline)
                
                # Output format selection
                output_format = st.radio(
                    "Output Format",
                    ["Preview", "Markdown", "JSON", "HTML"]
                )
                
                if output_format == "Preview":
                    # Display outline with content and images
                    st.markdown('<div class="preview-section">', unsafe_allow_html=True)
                    for section, subsections in outline.items():
                        content = generator.section_contents.get(section)
                        display_section(section, subsections, content, generator)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                elif output_format == "Markdown":
                    markdown_output = generator.to_markdown()
                    st.markdown('<div class="outline-content">', unsafe_allow_html=True)
                    st.code(markdown_output, language="markdown")
                    st.download_button(
                        "Download Markdown",
                        markdown_output,
                        file_name="blog_outline.md",
                        mime="text/markdown"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
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
                    st.markdown('<div class="outline-content">', unsafe_allow_html=True)
                    st.code(json_output, language="json")
                    st.download_button(
                        "Download JSON",
                        json_output,
                        file_name="blog_outline.json",
                        mime="application/json"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                elif output_format == "HTML":
                    html_output = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>{topic} - Blog Outline</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; max-width: 100%; margin: 0 auto; padding: 20px; }}
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
                    st.markdown('<div class="outline-content">', unsafe_allow_html=True)
                    st.code(html_output, language="html")
                    st.download_button(
                        "Download HTML",
                        html_output,
                        file_name="blog_outline.html",
                        mime="text/html"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Error generating outline: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display the outline if it exists in session state
    if st.session_state.outline:
        st.markdown('<div class="preview-section">', unsafe_allow_html=True)
        for section, subsections in st.session_state.outline.items():
            content = st.session_state.section_contents.get(section)
            display_section(section, subsections, content, generator)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close the outline container

if __name__ == "__main__":
    main() 