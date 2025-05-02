import sys
import os
import asyncio
from textwrap import dedent
from pathlib import Path
from datetime import datetime
import streamlit as st
from gtts import gTTS
import base64
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv(Path('../../.env'))
# Logger setup
from loguru import logger
logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

# Import other necessary modules
from ...ai_web_researcher.gpt_online_researcher import (
        do_metaphor_ai_research, do_google_pytrends_analysis)
from .blog_from_google_serp import write_blog_google_serp, blog_with_research
from ...blog_metadata.get_blog_metadata import blog_metadata
from ...blog_postprocessing.save_blog_to_file import save_blog_to_file
from ...gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
from ...ai_seo_tools.content_title_generator import generate_blog_titles
from ...ai_seo_tools.meta_desc_generator import generate_blog_metadesc
from ...ai_seo_tools.seo_structured_data import ai_structured_data

# Import search functions from the research utils module
from .blog_ai_research_utils import (
    initialize_parameters,
    perform_google_search,
    perform_tavily_search,
    do_google_serp_search,
    do_tavily_ai_search
)


def save_blog_content(blog_markdown_str, blog_title, blog_meta_desc, blog_tags, blog_categories, generated_image_filepath, status, blog_hashtags=None, blog_slug=None):
    """
    Save the blog content to a file.
    
    Args:
        blog_markdown_str (str): Blog content
        blog_title (str): Blog title
        blog_meta_desc (str): Blog meta description
        blog_tags (list): Blog tags
        blog_categories (list): Blog categories
        generated_image_filepath (str): Path to the generated image
        status: Streamlit status object
        blog_hashtags (str, optional): Social media hashtags
        blog_slug (str, optional): SEO-friendly URL slug
        
    Returns:
        str: Path to the saved file or None if saving failed
    """
    try:
        status.update(label="💾 Saving blog content to file...")
        saved_blog_to_file = save_blog_to_file(blog_markdown_str, blog_title, blog_meta_desc,
                                               blog_tags, blog_categories, generated_image_filepath)
        status.update(label=f"✅ Saved the content to: {saved_blog_to_file}")
        return saved_blog_to_file
    except Exception as err:
        st.error(f"Failed to save blog to file: {err}")
        logger.error(f"Failed to save blog to file: {err}")
        status.update(label="❌ Failed to save blog to file", state="error")
        return None


def generate_audio_version(blog_markdown_str, status=None):
    """
    Generate an audio version of the blog content.
    
    Args:
        blog_markdown_str (str): Blog content
        status: Streamlit status object (optional)
        
    Returns:
        bool: True if audio generation was successful, False otherwise
    """
    try:
        if status:
            status.update(label="🔊 Generating audio version of the blog...")
        else:
            st.info("🔊 Generating audio version...")
            
        # Only generate audio for reasonable-sized blogs (to avoid errors with very large text)
        if blog_markdown_str and len(blog_markdown_str) < 50000:  # Max ~50KB of text
            tts = gTTS(text=blog_markdown_str[:40000], lang='en', slow=False)  # Use first 40K chars to be safe
            tts.save("delete_me.mp3")
            st.audio("delete_me.mp3")
            st.download_button(
                label="📥 Download Audio File",
                data=open("delete_me.mp3", "rb").read(),
                file_name="blog_audio.mp3",
                mime="audio/mp3"
            )
            if status:
                status.update(label="✅ Audio version generated successfully", state="complete")
            else:
                st.success("✅ Audio version generated successfully")
            return True
        else:
            st.warning("Blog content too large for audio generation")
            if status:
                status.update(label="⚠️ Blog content too large for audio generation", state="complete")
            return False
    except Exception as err:
        st.warning(f"Failed to generate audio version: {err}")
        logger.error(f"Failed to generate audio version: {err}")
        if status:
            status.update(label="❌ Failed to generate audio version", state="error")
        return False


# Helper functions for write_blog_from_keywords
def setup_progress_tracking():
    """Set up progress tracking elements for blog generation."""
    # Create a placeholder for the final blog content
    final_content_placeholder = st.empty()
    
    # Create progress tracking
    progress_placeholder = st.empty()
    with progress_placeholder.container():
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(step, total_steps, message):
            """Update the progress bar and status message"""
            progress_value = min(step / total_steps, 1.0)
            progress_bar.progress(progress_value)
            status_text.info(f"Step {step}/{total_steps}: {message}")
            
            # When process is complete, clear the progress info
            if step == total_steps:
                import time
                time.sleep(3)  # Show the complete message for 3 seconds
                progress_bar.empty()
                status_text.empty()
    
    return final_content_placeholder, progress_placeholder, progress_bar, status_text, update_progress


def perform_research_phase(search_keywords, search_params, update_progress):
    """
    Perform the research phase of blog generation.
    
    Args:
        search_keywords (str): Keywords to research
        search_params (dict): Search parameters
        update_progress (function): Function to update progress
        
    Returns:
        tuple: Google search results, Tavily search results, success flags, and blog titles
    """
    update_progress(1, 5, f"Starting web research on '{search_keywords}'")
    logger.info(f"Researching and Writing Blog on keywords: {search_keywords}")
    
    # Create a section header for the research phase
    st.subheader("🔍 Web Research Progress")
    
    # Use a collapsible expander for research details
    with st.expander("Research Details", expanded=True):
        example_blog_titles = []
        
        # Create a status element for research updates
        with st.status("Web research in progress...", expanded=True) as status:
            status.update(label=f"📊 Performing web research on: {search_keywords}")
            
            # Create status container and progress tracking for Google SERP
            status_container = st.empty()
            research_progress = st.progress(0)
            
            # Google Search
            status.update(label="🔍 Performing Google search...")
            google_search_result, g_titles, google_search_success = perform_google_search(
                search_keywords, search_params, status, status_container, research_progress
            )
            if g_titles:
                example_blog_titles.append(g_titles)
                status.update(label=f"✅ Google search complete - found {len(g_titles)} relevant resources")
            else:
                status.update(label="⚠️ Google search yielded limited results")
            
            # Tavily Search
            status.update(label="🔍 Performing Tavily AI search...")
            tavily_search_result, tavily_search_success = perform_tavily_search(
                search_keywords, search_params, status
            )
            
            if tavily_search_success:
                status.update(label="✅ Tavily AI search complete", state="complete")
            elif google_search_success:
                status.update(label="⚠️ Tavily search had issues, but Google search was successful")
            else:
                status.update(label="❌ Both search methods encountered issues", state="error")
    
    # Clear the progress indicators
    status_container.empty()
    research_progress.empty()
    
    return google_search_result, tavily_search_result, google_search_success, tavily_search_success, example_blog_titles


def generate_content_phase(search_keywords, google_search_result, tavily_search_result, 
                          google_search_success, tavily_search_success, blog_params, update_progress):
    """
    Generate blog content from research results.
    
    Args:
        search_keywords (str): Keywords to research
        google_search_result: Results from Google search
        tavily_search_result: Results from Tavily search
        google_search_success (bool): Whether Google search was successful
        tavily_search_success (bool): Whether Tavily search was successful
        blog_params (dict): Blog parameters
        update_progress (function): Function to update progress
        
    Returns:
        str: Generated blog content or None if generation failed
    """
    # Import content generation function here to avoid circular import
    from .ai_blog_generator_utils import generate_blog_content
    
    update_progress(2, 5, "Generating blog content from research")
    
    # Create a section header for the content generation phase
    st.subheader("✍️ Content Generation Progress")
    
    # Use a collapsible expander for content generation details
    with st.expander("Content Generation Details", expanded=True):
        # Create a status element for content generation updates
        with st.status("Content generation in progress...", expanded=True) as status:
            if google_search_success:
                source = "Google search results"
            else:
                source = "Tavily AI research"
                
            status.update(label=f"📝 Creating {blog_params.get('blog_tone')} {blog_params.get('blog_type')} content for {blog_params.get('blog_demographic')} audience...")
            
            blog_markdown_str = generate_blog_content(
                search_keywords, google_search_result, tavily_search_result, 
                google_search_success, tavily_search_success, blog_params, status
            )
            
            if blog_markdown_str:
                status.update(label=f"✅ Successfully generated ~{len(blog_markdown_str.split())} words of content using {source}", state="complete")
            else:
                status.update(label="❌ Content generation failed", state="error")
    
    return blog_markdown_str


def generate_metadata_and_image(blog_markdown_str, search_keywords, blog_tags, update_progress):
    """
    Generate metadata and featured image for the blog.
    
    Args:
        blog_markdown_str (str): Blog content
        search_keywords (str): Keywords used for research
        blog_tags (list): Blog tags 
        update_progress (function): Function to update progress
        
    Returns:
        tuple: Blog metadata and image filepath
    """
    # Import metadata and image generation functions here to avoid circular import
    from .ai_blog_generator_utils import generate_blog_metadata, generate_blog_image
    
    update_progress(3, 5, "Generating SEO metadata and enhancements")
    
    # Create a section header for the enhancement phase
    st.subheader("🔍 SEO & Enhancement Progress")
    
    # Use a collapsible expander for enhancement details
    with st.expander("Enhancement Details", expanded=True):
        blog_title = None
        blog_meta_desc = None
        blog_categories = None
        blog_hashtags = None
        blog_slug = None
        generated_image_filepath = None
        saved_blog_to_file = None
        
        # Create a status element for enhancement updates
        with st.status("Enhancing content...", expanded=True) as status:
            # Generate metadata
            status.update(label="🏷️ Generating SEO metadata (title, description, tags)...")
            blog_title, blog_meta_desc, blog_tags, blog_categories, blog_hashtags, blog_slug = generate_blog_metadata(
                blog_markdown_str, search_keywords, status
            )
            
            # Check if there are updated values in session state
            if 'blog_title' in st.session_state:
                blog_title = st.session_state.blog_title
                status.update(label=f"✅ Using refined title: \"{blog_title}\"")
                
            if 'blog_meta_desc' in st.session_state:
                blog_meta_desc = st.session_state.blog_meta_desc
                status.update(label=f"✅ Using refined meta description")
            
            if blog_title and blog_meta_desc:
                status.update(label=f"✅ Generated metadata: \"{blog_title}\"")
                
                # Generate featured image
                status.update(label="🖼️ Creating featured image...")
                generated_image_filepath = generate_blog_image(
                    blog_title, blog_meta_desc, blog_markdown_str, status, blog_tags
                )
                
                # Save blog content to file
                status.update(label="💾 Saving blog content...")
                saved_blog_to_file = save_blog_content(
                    blog_markdown_str, blog_title, blog_meta_desc, blog_tags, 
                    blog_categories, generated_image_filepath, status, blog_hashtags, blog_slug
                )
                
                status.update(label="✅ Content enhancement complete", state="complete")
            else:
                status.update(label="⚠️ Metadata generation had issues, using simplified format", state="warning")
                
            # Add buttons for metadata refinement
            create_metadata_refinement_ui()
            
            # Add rich snippet section
            create_structured_data_ui()
    
    metadata = {
        "blog_title": blog_title,
        "blog_meta_desc": blog_meta_desc,
        "blog_tags": blog_tags,
        "blog_categories": blog_categories,
        "blog_hashtags": blog_hashtags,
        "blog_slug": blog_slug
    }
    
    return metadata, generated_image_filepath, saved_blog_to_file


def create_metadata_refinement_ui():
    """Create UI elements for refining blog metadata (title and meta description)."""
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refine Blog Title", key="refine_title_main", use_container_width=True):
            st.session_state.show_title_dialog = True
            st.rerun()
    with col2:
        if st.button("🔄 Refine Meta Description", key="refine_meta_main", use_container_width=True):
            st.session_state.show_meta_dialog = True
            st.rerun()


def create_structured_data_ui():
    """Create UI elements for generating structured data."""
    st.markdown("---")
    structured_data_col1, structured_data_col2 = st.columns([3, 1])
    
    with structured_data_col1:
        # Educational popover explaining why rich snippets are important
        with st.expander("ℹ️ Why Rich Snippets Are Important for SEO"):
            st.markdown("""
            ### Rich Snippets: Boosting Your SEO and Click-Through Rates
            
            **What are Rich Snippets?**
            
            Rich snippets are enhanced search results that display additional information directly in search engine results pages (SERPs). They're created using structured data markup (JSON-LD) that helps search engines understand your content better.
            
            **Why are they important?**
            
            1. **Increased Visibility**: Rich snippets stand out in search results with stars, images, and additional information
            
            2. **Higher Click-Through Rates (CTR)**: Studies show rich snippets can increase CTR by 30-150%
            
            3. **Improved SEO**: They help search engines understand your content better, potentially improving rankings
            
            4. **Enhanced User Experience**: Users can see key information before clicking, leading to more qualified traffic
            
            5. **Mobile-Friendly**: Rich snippets are especially effective on mobile searches
            
            **Common types of rich snippets include:**
            - Articles/Blogs (with author, date, image)
            - Products (with ratings, price, availability)
            - Recipes (with cooking time, ratings, calories)
            - Events (with date, location, ticket info)
            - Local Business (with address, hours, ratings)
            
            Adding structured data to your content is a powerful SEO technique that requires minimal effort but provides significant benefits.
            """)
    
    with structured_data_col2:
        # Button to generate rich snippet
        if st.button("📊 Generate Rich Snippet", key="snippet_main", use_container_width=True):
            st.session_state.show_snippet_dialog = True
            st.rerun()


def display_featured_image(blog_title, blog_meta_desc, blog_markdown_str, blog_tags, generated_image_filepath):
    """
    Display the featured image with regeneration options.
    
    Args:
        blog_title (str): Blog title
        blog_meta_desc (str): Blog meta description
        blog_markdown_str (str): Blog content
        blog_tags (list): Blog tags
        generated_image_filepath (str): Path to the generated image
        
    Returns:
        str: Updated image filepath if regenerated, otherwise original filepath
    """
    # Import image regeneration function here to avoid circular import
    from .ai_blog_generator_utils import regenerate_blog_image
    
    st.subheader("🖼️ Featured Image")
    image_container = st.container()
    
    # Display featured image
    with image_container:
        if generated_image_filepath:
            st.image(generated_image_filepath, caption=blog_title or "Featured Image", use_column_width=True)
            
            # Add regenerate button
            if st.button("🔄 Regenerate Image", key="regenerate_image"):
                new_image_path = regenerate_blog_image(blog_title, blog_meta_desc, blog_markdown_str, blog_tags)
                if new_image_path:
                    return new_image_path
        else:
            st.info("No featured image was generated. Click below to generate one.")
            if st.button("🖼️ Generate Image", key="generate_image"):
                new_image_path = regenerate_blog_image(blog_title, blog_meta_desc, blog_markdown_str, blog_tags)
                if new_image_path:
                    return new_image_path
    
    return generated_image_filepath


def display_blog_content_and_audio(blog_markdown_str, saved_blog_to_file):
    """
    Display the blog content and audio generation option.
    
    Args:
        blog_markdown_str (str): Blog content
        saved_blog_to_file (str): Path to the saved blog file
    """
    # Display blog content
    st.markdown("## Content")
    st.markdown(blog_markdown_str)
    
    # Show file save information if available
    if saved_blog_to_file:
        st.success(f"✅ Blog saved to: {saved_blog_to_file}")
    
    # Add the audio generation button
    st.markdown("---")
    audio_col1, audio_col2 = st.columns([1, 3])
    with audio_col1:
        generate_audio_button = st.button("🔊 Generate Audio Version", use_container_width=True)
    
    with audio_col2:
        if generate_audio_button:
            generate_audio_version(blog_markdown_str)


def display_final_metadata_table(metadata, update_progress):
    """
    Display the final metadata table and options.
    
    Args:
        metadata (dict): Blog metadata
        update_progress (function): Function to update progress
    """
    update_progress(4, 5, "Preparing final blog presentation")
    
    st.markdown("---")
    # Display metadata in a collapsible expander to save space
    with st.expander("🏷️ Metadata", expanded=True):
        st.table({
            "Metadata": ["Blog Title", "Meta Description", "Tags", "Categories", "Hashtags", "Slug"],
            "Value": [
                metadata["blog_title"], 
                metadata["blog_meta_desc"], 
                metadata["blog_tags"], 
                metadata["blog_categories"], 
                metadata["blog_hashtags"], 
                metadata["blog_slug"]
            ]
        })

        # Add buttons in columns for refining metadata
        create_metadata_refinement_ui()
        
        # Add a row for structured data with a "Generate Rich Snippet" button
        st.markdown("---")
        st.markdown("### Get Structured Data")
        
        # Add structured data UI
        create_structured_data_ui()

        # Create snippet generation dialog if button is clicked
        if st.session_state.get("show_snippet_dialog", False):
            display_structured_data_dialog(metadata["blog_title"], metadata["blog_tags"])


def display_structured_data_dialog(blog_title, blog_tags):
    """
    Display the structured data generation dialog.
    
    Args:
        blog_title (str): Blog title
        blog_tags (list): Blog tags
    """
    with st.expander("Structured Data Generation Tool", expanded=True):
        st.subheader("Generate Structured Data (Rich Snippets)")
        
        # Close button at the top
        if st.button("Close", key="close_structured_data"):
            st.session_state.show_snippet_dialog = False
            st.rerun()
        
        # Simplified blog URL input
        blog_url = st.text_input(
            "Blog URL:",
            placeholder="https://yourblog.com/your-article",
            help="Enter the URL where this blog will be published"
        )
        
        # Auto-fill content type to "Article" since we're working with a blog
        content_type = "Article"
        st.info(f"Content Type: {content_type} (Auto-selected for blog content)")
        
        # Form for additional article details
        with st.form(key="structured_data_form"):
            st.markdown("#### Article Details")
            
            # Pre-fill with blog title and other metadata
            article_title = st.text_input("Headline:", value=blog_title if blog_title else "")
            article_author = st.text_input("Author:", value="")
            article_date = st.date_input("Date Published:", value=datetime.now())
            article_keywords = st.text_input("Keywords:", value=blog_tags if blog_tags else "")
            
            submit_structured_data = st.form_submit_button("Generate JSON-LD")
        
        if submit_structured_data:
            if not blog_url:
                st.error("Please enter a blog URL to generate structured data.")
            else:
                # Create details dictionary
                details = {
                    "Headline": article_title,
                    "Author": article_author,
                    "Date Published": article_date,
                    "Keywords": article_keywords
                }
                
                # Call the imported ai_structured_data function or recreate its functionality
                with st.spinner("Generating structured data..."):
                    # Import and use the function from the module directly
                    from ...ai_seo_tools.seo_structured_data import generate_json_data
                    
                    # Generate the structured data
                    structured_data = generate_json_data(content_type, details, blog_url)
                    
                    if structured_data:
                        st.success("✅ Structured data generated successfully!")
                        st.markdown("### Generated JSON-LD Code")
                        st.code(structured_data, language="json")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download JSON-LD",
                            data=structured_data,
                            file_name=f"{content_type}_structured_data.json",
                            mime="application/json",
                        )
                        
                        # Implementation instructions
                        with st.expander("How to Implement This Code"):
                            st.markdown("""
                            ### Adding this JSON-LD to your website:
                            
                            1. **Copy the generated JSON-LD code** above
                            
                            2. **Add it to the `<head>` section of your HTML** like this:
                            ```html
                            <script type="application/ld+json">
                            [PASTE YOUR JSON-LD CODE HERE]
                            </script>
                            ```
                            
                            3. **Verify the implementation** using Google's Rich Results Test tool:
                            [https://search.google.com/test/rich-results](https://search.google.com/test/rich-results)
                            
                            4. **Monitor your search appearance** in Google Search Console
                            """)
                    else:
                        st.error("Failed to generate structured data. Please check your inputs and try again.")


def display_title_refinement_dialog(blog_title, blog_tags):
    """
    Display a dialog for refining the blog title.
    
    Args:
        blog_title (str): Current blog title
        blog_tags (list): Blog tags for context
    """
    with st.expander("Blog Title Refinement Tool", expanded=True):
        st.subheader("Generate Better Blog Titles")
        
        # Form for title generation
        with st.form(key="title_generation_form"):
            st.markdown("#### Title Generation Parameters")
            
            # Pre-fill with blog tags if available
            keywords = st.text_input("Target Keywords:", 
                               value=blog_tags if blog_tags else "",
                               help="Enter primary keywords to target in the title")
            
            blog_type = st.selectbox(
                "Blog Type:",
                ["How-to Guide", "Tutorial", "List Post", "Informational", "Case Study", "Opinion Piece", "Review"],
                index=0,
                help="Select the type of blog you're creating"
            )
            
            search_intent = st.selectbox(
                "Search Intent:",
                ["Informational", "Commercial", "Navigational", "Transactional"],
                index=0,
                help="Select the primary search intent your title should address"
            )
            
            language = st.selectbox(
                "Language:",
                ["English", "Spanish", "French", "German", "Italian"],
                index=0
            )
            
            submit_title = st.form_submit_button("Generate Title Suggestions")
        
        if submit_title:
            with st.spinner("Generating title suggestions..."):
                # Import and use the function from the module
                from ...ai_seo_tools.content_title_generator import generate_blog_titles
                
                # Generate the titles
                title_suggestions = generate_blog_titles(
                    target_keywords=keywords,
                    blog_type=blog_type,
                    search_intent=search_intent,
                    language=language
                )
                
                if title_suggestions:
                    st.success("✅ Generated title suggestions!")
                    
                    # Display each title with an option to select it
                    st.markdown("### Select a Title or Modify")
                    
                    selected_title = st.text_input(
                        "Selected or Modified Title:",
                        value=blog_title if blog_title else (title_suggestions[0] if title_suggestions else ""),
                        help="Select one of the suggested titles or modify it to your preference"
                    )
                    
                    if st.button("Confirm Title"):
                        st.session_state.blog_title = selected_title
                        st.session_state.show_title_dialog = False
                        st.success(f"Title updated to: {selected_title}")
                        st.rerun()
                    
                    # Display all suggestions
                    for i, title in enumerate(title_suggestions):
                        st.markdown(f"**Option {i+1}:** {title}")
                else:
                    st.error("Failed to generate title suggestions. Please try different parameters.")


def display_meta_description_dialog(blog_meta_desc, blog_tags):
    """
    Display a dialog for refining the meta description.
    
    Args:
        blog_meta_desc (str): Current meta description
        blog_tags (list): Blog tags for context
    """
    with st.expander("Meta Description Refinement Tool", expanded=True):
        st.subheader("Generate Optimized Meta Descriptions")
        
        # Form for meta description generation
        with st.form(key="meta_desc_generation_form"):
            st.markdown("#### Meta Description Parameters")
            
            # Pre-fill with blog tags if available
            keywords = st.text_input("Target Keywords:", 
                               value=blog_tags if blog_tags else "",
                               help="Enter primary keywords to target in the meta description")
            
            tone = st.selectbox(
                "Tone:",
                ["Informative", "Engaging", "Professional", "Conversational", "Humorous", "Urgent"],
                index=0,
                help="Select the tone for your meta description"
            )
            
            search_intent = st.selectbox(
                "Search Intent:",
                ["Informational", "Commercial", "Navigational", "Transactional"],
                index=0,
                help="Select the primary search intent your meta description should address"
            )
            
            language = st.selectbox(
                "Language:",
                ["English", "Spanish", "French", "German", "Italian"],
                index=0
            )
            
            submit_meta = st.form_submit_button("Generate Meta Description Suggestions")
        
        if submit_meta:
            with st.spinner("Generating meta description suggestions..."):
                # Import and use the function from the module
                from ...ai_seo_tools.meta_desc_generator import generate_blog_metadesc
                
                # Generate the meta descriptions
                meta_suggestions = generate_blog_metadesc(
                    target_keywords=keywords,
                    tone=tone,
                    search_intent=search_intent,
                    language=language
                )
                
                if meta_suggestions:
                    st.success("✅ Generated meta description suggestions!")
                    
                    # Display each meta description with an option to select it
                    st.markdown("### Select a Meta Description or Modify")
                    
                    selected_meta = st.text_area(
                        "Selected or Modified Meta Description:",
                        value=blog_meta_desc if blog_meta_desc else (meta_suggestions[0] if meta_suggestions else ""),
                        height=100,
                        help="Select one of the suggested meta descriptions or modify it to your preference"
                    )
                    
                    if st.button("Confirm Meta Description"):
                        st.session_state.blog_meta_desc = selected_meta
                        st.session_state.show_meta_dialog = False
                        st.success(f"Meta description updated!")
                        st.rerun()
                    
                    # Display all suggestions
                    for i, meta in enumerate(meta_suggestions):
                        st.markdown(f"**Option {i+1}:** {meta}")
                else:
                    st.error("Failed to generate meta description suggestions. Please try different parameters.")


def write_blog_from_keywords(search_keywords, url=None, search_params=None, blog_params=None):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    
    Args:
        search_keywords (str): Keywords to research and write about
        url (str, optional): Optional URL to use as a source
        search_params (dict, optional): Dictionary of search parameters including:
            - max_results: Maximum number of search results (default: 10)
            - search_depth: "basic" or "advanced" search depth (default: "basic") 
            - include_domains: List of domains to prioritize in search
            - time_range: Time range for results (default: "year")
        blog_params (dict, optional): Dictionary of blog content characteristics including:
            - blog_length: Target word count (default: 2000)
            - blog_tone: Tone of the content (default: "Professional")
            - blog_demographic: Target audience (default: "Professional")
            - blog_type: Type of blog post (default: "Informational")
            - blog_language: Language for the blog (default: "English")
            - blog_output_format: Format for the blog (default: "markdown")
    """
    # Check if we need to display any dialog boxes first
    if st.session_state.get("show_title_dialog") and "blog_title" in st.session_state:
        display_title_refinement_dialog(st.session_state.blog_title, None)
        return None
    
    if st.session_state.get("show_meta_dialog") and "blog_meta_desc" in st.session_state:
        display_meta_description_dialog(st.session_state.blog_meta_desc, None)
        return None
    
    if st.session_state.get("show_snippet_dialog"):
        # Get blog title and tags to pass to the dialog
        blog_title = st.session_state.get("blog_title", "")
        blog_tags = st.session_state.get("blog_tags", "")
        display_structured_data_dialog(blog_title, blog_tags)
        return None
    
    # Initialize parameters with defaults
    search_params, blog_params = initialize_parameters(search_params, blog_params)
    
    # Set up progress tracking
    final_content_placeholder, progress_placeholder, progress_bar, status_text, update_progress = setup_progress_tracking()
    
    # STEP 1: Research phase
    google_search_result, tavily_search_result, google_search_success, tavily_search_success, example_blog_titles = perform_research_phase(
        search_keywords, search_params, update_progress
    )
    
    # Check if both searches failed - if so, stop the process
    if not google_search_success and not tavily_search_success:
        update_progress(5, 5, "Research failed")
        progress_placeholder.error("⛔ Both Google SERP and Tavily AI searches failed. Unable to generate blog content.")
        st.warning("Please check your API keys in the environment settings and try again.")
        st.stop()
        return None
    
    # STEP 2: Content generation phase
    blog_markdown_str = generate_content_phase(
        search_keywords, google_search_result, tavily_search_result, 
        google_search_success, tavily_search_success, blog_params, update_progress
    )
    
    if not blog_markdown_str:
        update_progress(5, 5, "Content generation failed")
        progress_placeholder.error("⛔ Failed to generate blog content from research data.")
        st.stop()
        return None
    
    # STEP 3: Metadata & enhancement phase
    metadata, generated_image_filepath, saved_blog_to_file = generate_metadata_and_image(
        blog_markdown_str, search_keywords, None, update_progress
    )
    
    # Display image with regeneration option
    updated_image_filepath = display_featured_image(
        metadata["blog_title"], metadata["blog_meta_desc"], 
        blog_markdown_str, metadata["blog_tags"], generated_image_filepath
    )
    
    if updated_image_filepath != generated_image_filepath:
        generated_image_filepath = updated_image_filepath
        st.rerun()  # Refresh the page to show the new image
    
    # Display blog content and audio option
    display_blog_content_and_audio(blog_markdown_str, saved_blog_to_file)
    
    # STEP 4: Final presentation
    with final_content_placeholder.container():
        display_final_metadata_table(metadata, update_progress)
        
        # If there's a button click to generate a structured data snippet, handle it
        if st.session_state.get("show_snippet_dialog", False):
            display_structured_data_dialog(metadata["blog_title"], metadata["blog_tags"])
    
    # Final progress update
    update_progress(5, 5, "Blog generation complete!")
    
    # Replace progress bar with success message
    progress_placeholder.success("✅ Blog generation process completed successfully!")
    
    return blog_markdown_str
