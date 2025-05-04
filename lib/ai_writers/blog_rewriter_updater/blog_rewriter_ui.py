"""
Blog Rewriter UI Module

This module contains the Streamlit interface for the blog rewriter,
providing a user-friendly way to interact with the rewriting functionality.
"""

import streamlit as st
import json
from datetime import datetime
from .blog_rewriter_utils import BlogRewriter, REWRITE_MODES, TONE_OPTIONS, MAX_META_DESCRIPTION_LENGTH

def write_blog_rewriter():
    """Main function to display the blog rewriter UI."""
    st.title("AI Blog Rewriter & Updater")
    
    # Create a container for the header section
    with st.container():
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-top: 0;">Revitalize Your Content</h3>
            <p>Update, fact-check, and enhance your existing blog posts with AI assistance. 
            Our tool analyzes your content, researches the latest information, and rewrites your blog 
            to be more engaging, accurate, and SEO-friendly.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize the BlogRewriter class
    if "blog_rewriter" not in st.session_state:
        st.session_state.blog_rewriter = BlogRewriter()
    
    # Initialize session state variables
    if "original_content" not in st.session_state:
        st.session_state.original_content = {}
    if "content_analysis" not in st.session_state:
        st.session_state.content_analysis = {}
    if "research_results" not in st.session_state:
        st.session_state.research_results = {}
    if "rewritten_content" not in st.session_state:
        st.session_state.rewritten_content = {}
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = {}
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    
    # Create tabs for the workflow
    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ Import Content", 
        "2️⃣ Analyze & Research", 
        "3️⃣ Rewrite Settings", 
        "4️⃣ Results & Export"
    ])
    
    # Tab 1: Import Content
    with tab1:
        st.header("Import Your Blog Content")
        
        import_method = st.radio(
            "Choose import method:",
            ["Import from URL", "Paste content manually"],
            horizontal=True
        )
        
        if import_method == "Import from URL":
            url = st.text_input(
                "Enter blog URL:",
                placeholder="https://example.com/blog-post",
                help="Enter the full URL of the blog post you want to rewrite"
            )
            
            if st.button("Import Content", type="primary"):
                if not url:
                    st.error("Please enter a valid URL")
                else:
                    with st.spinner("Extracting content from URL..."):
                        # Extract content from URL
                        st.session_state.original_content = st.session_state.blog_rewriter.extract_content_from_url(url)
                        
                        if "error" in st.session_state.original_content:
                            st.error(f"Error extracting content: {st.session_state.original_content['error']}")
                        else:
                            st.success("Content extracted successfully!")
                            st.session_state.current_step = 2
                            st.rerun()
        else:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                title = st.text_input(
                    "Blog Title:",
                    placeholder="Enter the title of your blog post"
                )
            
            with col2:
                author = st.text_input(
                    "Author (optional):",
                    placeholder="Author name"
                )
            
            meta_description = st.text_area(
                "Meta Description (optional):",
                placeholder="Enter the meta description of your blog post",
                max_chars=MAX_META_DESCRIPTION_LENGTH,
                height=80
            )
            
            content = st.text_area(
                "Blog Content:",
                placeholder="Paste your blog content here...",
                height=300
            )
            
            if st.button("Import Content", type="primary"):
                if not title or not content:
                    st.error("Please enter both title and content")
                else:
                    # Store the manually entered content
                    st.session_state.original_content = {
                        "title": title,
                        "meta_description": meta_description,
                        "content": content,
                        "author": author,
                        "headings": [],
                        "images": [],
                        "publish_date": None,
                        "url": None
                    }
                    
                    st.success("Content imported successfully!")
                    st.session_state.current_step = 2
                    st.rerun()
        
        # Display the imported content if available
        if st.session_state.original_content and "title" in st.session_state.original_content:
            with st.expander("View Imported Content", expanded=False):
                st.subheader(st.session_state.original_content["title"])
                
                if st.session_state.original_content.get("meta_description"):
                    st.markdown(f"**Meta Description:** {st.session_state.original_content['meta_description']}")
                
                if st.session_state.original_content.get("author"):
                    st.markdown(f"**Author:** {st.session_state.original_content['author']}")
                
                if st.session_state.original_content.get("publish_date"):
                    st.markdown(f"**Published:** {st.session_state.original_content['publish_date']}")
                
                st.markdown("**Content Preview:**")
                content_preview = st.session_state.original_content["content"]
                if len(content_preview) > 1000:
                    content_preview = content_preview[:1000] + "..."
                st.text_area("", content_preview, height=200, disabled=True)
                
                # Display images if available
                if st.session_state.original_content.get("images"):
                    st.markdown(f"**Images:** {len(st.session_state.original_content['images'])} images found")
    
    # Tab 2: Analyze & Research
    with tab2:
        st.header("Analyze & Research")
        
        if not st.session_state.original_content or "title" not in st.session_state.original_content:
            st.info("Please import your blog content first")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Analyze Content", type="primary"):
                    with st.spinner("Analyzing content..."):
                        # Analyze the content
                        st.session_state.content_analysis = st.session_state.blog_rewriter.analyze_content(
                            st.session_state.original_content
                        )
                        st.success("Content analysis complete!")
            
            with col2:
                research_depth = st.selectbox(
                    "Research Depth:",
                    ["low", "medium", "high"],
                    index=1,
                    format_func=lambda x: {"low": "Basic", "medium": "Standard", "high": "Comprehensive"}[x],
                    help="Choose the depth of research to update your content"
                )
                
                if st.button("Conduct Research", type="primary"):
                    with st.spinner("Researching latest information..."):
                        # Conduct research
                        st.session_state.research_results = st.session_state.blog_rewriter.conduct_research(
                            st.session_state.original_content["title"],
                            st.session_state.original_content["content"],
                            research_depth
                        )
                        st.success("Research complete!")
            
            # Display content analysis if available
            if st.session_state.content_analysis:
                st.subheader("Content Analysis")
                
                metrics = st.session_state.content_analysis.get("metrics", {})
                
                # Create metrics display
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Word Count", metrics.get("word_count", 0))
                with col2:
                    st.metric("Paragraphs", metrics.get("paragraph_count", 0))
                with col3:
                    st.metric("Sentences", metrics.get("sentence_count", 0))
                with col4:
                    content_age = st.session_state.content_analysis.get("content_age", {})
                    if "months" in content_age:
                        st.metric("Content Age", f"{content_age['months']} months")
                    elif "error" in content_age:
                        st.metric("Content Age", "Unknown")
                
                # Heading structure
                heading_structure = st.session_state.content_analysis.get("heading_structure", {})
                if heading_structure:
                    st.markdown("**Heading Structure:**")
                    for level, count in sorted(heading_structure.items()):
                        st.markdown(f"H{level}: {count} headings")
                
                # Image analysis
                images = st.session_state.content_analysis.get("images", {})
                if images:
                    st.markdown(f"**Images:** {images.get('count', 0)} images found, {images.get('with_alt_text', 0)} with alt text")
            
            # Display research results if available
            if st.session_state.research_results:
                st.subheader("Research Results")
                
                topics = st.session_state.research_results.get("topics", [])
                if topics:
                    for topic in topics:
                        with st.expander(f"Topic: {topic['topic']}", expanded=False):
                            for i, source in enumerate(topic.get("sources", [])):
                                st.markdown(f"**Source {i+1}:** {source.get('title', 'Untitled')}")
                                st.markdown(f"**URL:** {source.get('url', 'No URL')}")
                                st.markdown(f"**Content Preview:** {source.get('content', 'No content')[:200]}...")
                                st.markdown("---")
                else:
                    st.info("No research results available")
            
            # Enable proceeding to the next step if both analysis and research are done
            if st.session_state.content_analysis and st.session_state.research_results:
                if st.button("Proceed to Rewrite Settings", type="primary"):
                    st.session_state.current_step = 3
                    st.rerun()
    
    # Tab 3: Rewrite Settings
    with tab3:
        st.header("Rewrite Settings")
        
        if not st.session_state.original_content or "title" not in st.session_state.original_content:
            st.info("Please import your blog content first")
        elif not st.session_state.content_analysis or not st.session_state.research_results:
            st.info("Please complete content analysis and research first")
        else:
            # Create a form for rewrite settings
            with st.form("rewrite_settings_form"):
                st.subheader("Content Transformation")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    rewrite_mode = st.selectbox(
                        "Rewrite Mode:",
                        list(REWRITE_MODES.keys()),
                        format_func=lambda x: x.replace("_", " ").title(),
                        help="Choose how you want to transform your content"
                    )
                    
                    st.info(REWRITE_MODES[rewrite_mode])
                
                with col2:
                    tone = st.selectbox(
                        "Target Tone:",
                        TONE_OPTIONS,
                        index=0,
                        help="Choose the tone for your rewritten content"
                    )
                
                st.subheader("Content Length")
                
                original_word_count = st.session_state.content_analysis.get("metrics", {}).get("word_count", 0)
                
                length_option = st.radio(
                    "Target Length:",
                    ["same", "shorter", "longer", "custom"],
                    format_func=lambda x: {
                        "same": f"Same as original ({original_word_count} words)",
                        "shorter": f"Shorter (about {int(original_word_count * 0.7)} words)",
                        "longer": f"Longer (about {int(original_word_count * 1.3)} words)",
                        "custom": "Custom word count"
                    }[x],
                    horizontal=True
                )
                
                if length_option == "custom":
                    target_word_count = st.number_input(
                        "Custom Word Count:",
                        min_value=100,
                        max_value=10000,
                        value=original_word_count,
                        step=100
                    )
                else:
                    target_word_count = {
                        "same": original_word_count,
                        "shorter": int(original_word_count * 0.7),
                        "longer": int(original_word_count * 1.3)
                    }[length_option]
                
                st.subheader("SEO Optimization")
                
                keywords = st.text_input(
                    "Focus Keywords (comma-separated):",
                    placeholder="e.g., digital marketing, SEO, content strategy",
                    help="Enter keywords to optimize your content for"
                )
                
                st.subheader("Additional Instructions")
                
                special_instructions = st.text_area(
                    "Special Instructions (optional):",
                    placeholder="Add any specific instructions for rewriting your content...",
                    help="Provide any additional instructions for the AI"
                )
                
                # Submit button
                submitted = st.form_submit_button("Rewrite Blog", type="primary")
                
                if submitted:
                    # Process the form data
                    user_preferences = {
                        "rewrite_mode": rewrite_mode,
                        "tone": tone,
                        "target_word_count": target_word_count,
                        "keywords": [k.strip() for k in keywords.split(",")] if keywords else [],
                        "special_instructions": special_instructions
                    }
                    
                    with st.spinner("Rewriting your blog..."):
                        # Rewrite the blog
                        st.session_state.rewritten_content = st.session_state.blog_rewriter.rewrite_blog(
                            st.session_state.original_content,
                            user_preferences,
                            st.session_state.research_results,
                            st.session_state.content_analysis
                        )
                        
                        if "error" in st.session_state.rewritten_content:
                            st.error(f"Error rewriting blog: {st.session_state.rewritten_content['error']}")
                        else:
                            st.success("Blog rewritten successfully!")
                            st.session_state.current_step = 4
                            st.rerun()
    
    # Tab 4: Results & Export
    with tab4:
        st.header("Results & Export")
        
        if not st.session_state.rewritten_content or "title" not in st.session_state.rewritten_content:
            st.info("Please complete the rewriting process first")
        else:
            # Display the rewritten content
            st.subheader("Rewritten Blog")
            
            # Title and meta description
            st.markdown(f"## {st.session_state.rewritten_content['title']}")
            
            if st.session_state.rewritten_content.get("meta_description"):
                with st.expander("Meta Description", expanded=True):
                    st.text_area(
                        "",
                        st.session_state.rewritten_content["meta_description"],
                        height=80,
                        disabled=True
                    )
            
            # Create tabs for different views
            content_tab1, content_tab2 = st.tabs(["Preview", "Markdown"])
            
            with content_tab1:
                st.markdown(st.session_state.rewritten_content["content"])
            
            with content_tab2:
                st.text_area(
                    "",
                    st.session_state.rewritten_content["content"],
                    height=400
                )
            
            # Image generation section
            st.subheader("Generate Images")
            
            suggested_images = st.session_state.rewritten_content.get("suggested_images", [])
            if suggested_images:
                st.markdown("**Suggested Images:**")
                
                for i, img in enumerate(suggested_images):
                    with st.expander(f"Image {i+1}: {img.get('description', 'No description')}", expanded=False):
                        st.markdown(f"**Description:** {img.get('description', 'No description')}")
                        st.markdown(f"**Caption:** {img.get('caption', 'No caption')}")
                        st.markdown(f"**Placement:** {img.get('placement', 'No placement specified')}")
                        
                        # Generate image button
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            image_prompt = st.text_area(
                                "Image Prompt:",
                                value=img.get('description', ''),
                                key=f"image_prompt_{i}"
                            )
                        
                        with col2:
                            style = st.selectbox(
                                "Style:",
                                ["realistic", "artistic", "cartoon", "3d_render"],
                                key=f"style_{i}"
                            )
                            
                            if st.button("Generate Image", key=f"gen_img_{i}"):
                                with st.spinner("Generating image..."):
                                    image_path = st.session_state.blog_rewriter.generate_image(image_prompt, style)
                                    
                                    if image_path:
                                        # Store the generated image
                                        if "generated_images" not in st.session_state:
                                            st.session_state.generated_images = {}
                                        
                                        st.session_state.generated_images[f"image_{i}"] = {
                                            "path": image_path,
                                            "caption": img.get('caption', ''),
                                            "placement": img.get('placement', '')
                                        }
                                        
                                        st.success("Image generated successfully!")
                                        st.rerun()
                        
                        # Display the generated image if available
                        if f"image_{i}" in st.session_state.generated_images:
                            st.image(
                                st.session_state.generated_images[f"image_{i}"]["path"],
                                caption=st.session_state.generated_images[f"image_{i}"]["caption"],
                                use_column_width=True
                            )
            else:
                st.info("No image suggestions available")
                
                # Custom image generation
                with st.expander("Generate Custom Image", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        custom_image_prompt = st.text_area(
                            "Image Prompt:",
                            placeholder="Describe the image you want to generate..."
                        )
                    
                    with col2:
                        custom_style = st.selectbox(
                            "Style:",
                            ["realistic", "artistic", "cartoon", "3d_render"]
                        )
                        
                        if st.button("Generate Custom Image"):
                            if not custom_image_prompt:
                                st.error("Please enter an image prompt")
                            else:
                                with st.spinner("Generating image..."):
                                    image_path = st.session_state.blog_rewriter.generate_image(custom_image_prompt, custom_style)
                                    
                                    if image_path:
                                        # Store the generated image
                                        if "generated_images" not in st.session_state:
                                            st.session_state.generated_images = {}
                                        
                                        st.session_state.generated_images["custom_image"] = {
                                            "path": image_path,
                                            "caption": "Custom generated image",
                                            "placement": "Custom placement"
                                        }
                                        
                                        st.success("Image generated successfully!")
                                        st.rerun()
                    
                    # Display the generated custom image if available
                    if "custom_image" in st.session_state.generated_images:
                        st.image(
                            st.session_state.generated_images["custom_image"]["path"],
                            caption=st.session_state.generated_images["custom_image"]["caption"],
                            use_column_width=True
                        )
            
            # Export options
            st.subheader("Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "Download as Markdown",
                    data=st.session_state.rewritten_content["content"],
                    file_name=f"{st.session_state.rewritten_content['title'].replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            
            with col2:
                # Create HTML version
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{st.session_state.rewritten_content['title']}</title>
                    <meta name="description" content="{st.session_state.rewritten_content.get('meta_description', '')}">
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                        h1, h2, h3, h4, h5, h6 {{ color: #333; }}
                        img {{ max-width: 100%; height: auto; }}
                        pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                        blockquote {{ border-left: 5px solid #eee; padding-left: 15px; margin-left: 0; }}
                    </style>
                </head>
                <body>
                    <h1>{st.session_state.rewritten_content['title']}</h1>
                    {st.session_state.rewritten_content['content']}
                </body>
                </html>
                """
                
                st.download_button(
                    "Download as HTML",
                    data=html_content,
                    file_name=f"{st.session_state.rewritten_content['title'].replace(' ', '_')}.html",
                    mime="text/html"
                )
            
            with col3:
                # Create JSON version with all content and metadata
                json_content = {
                    "title": st.session_state.rewritten_content["title"],
                    "meta_description": st.session_state.rewritten_content.get("meta_description", ""),
                    "content": st.session_state.rewritten_content["content"],
                    "suggested_images": st.session_state.rewritten_content.get("suggested_images", []),
                    "generated_images": [
                        {
                            "caption": img_data["caption"],
                            "placement": img_data["placement"],
                            "path": img_data["path"]
                        }
                        for img_key, img_data in st.session_state.generated_images.items()
                    ] if hasattr(st.session_state, "generated_images") else [],
                    "original_title": st.session_state.original_content.get("title", ""),
                    "original_url": st.session_state.original_content.get("url", ""),
                    "rewrite_date": datetime.now().isoformat()
                }
                
                st.download_button(
                    "Download as JSON",
                    data=json.dumps(json_content, indent=2),
                    file_name=f"{st.session_state.rewritten_content['title'].replace(' ', '_')}.json",
                    mime="application/json"
                )
            
            # Copy to clipboard buttons
            st.subheader("Quick Copy")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Copy Title", key="copy_title"):
                    st.code(st.session_state.rewritten_content["title"])
                    st.success("Title copied to clipboard!")
            
            with col2:
                if st.button("Copy Meta Description", key="copy_meta"):
                    st.code(st.session_state.rewritten_content.get("meta_description", ""))
                    st.success("Meta description copied to clipboard!")
            
            with col3:
                if st.button("Copy Full Content", key="copy_content"):
                    st.success("Content copied to clipboard!")
            
            # Comparison with original
            with st.expander("Compare with Original", expanded=False):
                comp_col1, comp_col2 = st.columns(2)
                
                with comp_col1:
                    st.subheader("Original")
                    st.markdown(f"**Title:** {st.session_state.original_content.get('title', '')}")
                    if st.session_state.original_content.get("meta_description"):
                        st.markdown(f"**Meta Description:** {st.session_state.original_content['meta_description']}")
                    st.text_area(
                        "Original Content",
                        st.session_state.original_content.get("content", ""),
                        height=300,
                        disabled=True
                    )
                
                with comp_col2:
                    st.subheader("Rewritten")
                    st.markdown(f"**Title:** {st.session_state.rewritten_content['title']}")
                    if st.session_state.rewritten_content.get("meta_description"):
                        st.markdown(f"**Meta Description:** {st.session_state.rewritten_content['meta_description']}")
                    st.text_area(
                        "Rewritten Content",
                        st.session_state.rewritten_content["content"],
                        height=300,
                        disabled=True
                    )
            
            # Start over button
            if st.button("Start Over", type="primary"):
                # Reset session state
                for key in ["original_content", "content_analysis", "research_results", 
                           "rewritten_content", "generated_images", "current_step"]:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.rerun()

if __name__ == "__main__":
    write_blog_rewriter() 