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
from ..ai_web_researcher.gpt_online_researcher import (
        do_google_serp_search as gpt_do_google_serp_search, 
        do_tavily_ai_search as gpt_do_tavily_ai_search,
        do_metaphor_ai_research, do_google_pytrends_analysis)
from .blog_from_google_serp import write_blog_google_serp, blog_with_research
from ..ai_web_researcher.you_web_reseacher import get_rag_results, search_ydc_index
from ..blog_metadata.get_blog_metadata import blog_metadata
from ..blog_postprocessing.save_blog_to_file import save_blog_to_file
from ..gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image


# Function to convert text to speech and save as an audio file
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    return "output.mp3"


# Function to get audio file as a downloadable link
def get_audio_file(audio_file):
    with open(audio_file, "rb") as file:
        data = file.read()
        b64_data = base64.b64encode(data).decode()
        return f'<a href="data:audio/mp3;base64,{b64_data}" download="output.mp3">Download audio file</a>'


def initialize_parameters(search_params=None, blog_params=None):
    """
    Initialize and validate search and blog parameters with defaults.
    
    Args:
        search_params (dict, optional): Search parameters
        blog_params (dict, optional): Blog parameters
        
    Returns:
        tuple: (search_params, blog_params) with defaults applied
    """
    # Initialize search params if not provided
    if search_params is None:
        search_params = {}
    
    # Initialize blog params if not provided
    if blog_params is None:
        blog_params = {}
    
    # Provide default values only for missing keys
    # This ensures we don't override values that were intentionally set to 0 or other falsy values
    if "max_results" not in search_params:
        search_params["max_results"] = 10
    if "search_depth" not in search_params:
        search_params["search_depth"] = "basic"
    if "time_range" not in search_params:
        search_params["time_range"] = "year"
    if "include_domains" not in search_params:
        search_params["include_domains"] = []
    
    # Provide default values only for missing blog parameter keys
    if "blog_length" not in blog_params:
        blog_params["blog_length"] = 2000
    if "blog_tone" not in blog_params:
        blog_params["blog_tone"] = "Professional"
    if "blog_demographic" not in blog_params:
        blog_params["blog_demographic"] = "Professional"
    if "blog_type" not in blog_params:
        blog_params["blog_type"] = "Informational"
    if "blog_language" not in blog_params:
        blog_params["blog_language"] = "English"
    if "blog_output_format" not in blog_params:
        blog_params["blog_output_format"] = "markdown"
    
    # Log the parameters for debugging
    logger.info(f"Using search parameters: {search_params}")
    logger.info(f"Using blog parameters: {blog_params}")
    
    return search_params, blog_params


def perform_google_search(search_keywords, search_params, status, status_container, progress_bar):
    """
    Perform Google SERP search for the given keywords.
    
    Args:
        search_keywords (str): Keywords to search for
        search_params (dict): Search parameters
        status: Streamlit status object
        status_container: Streamlit container for status messages
        progress_bar: Streamlit progress bar
        
    Returns:
        tuple: (google_search_result, g_titles, success_flag)
    """
    def update_progress(message, progress=None, level="info"):
        """Helper function to update progress in Streamlit UI"""
        if progress is not None:
            progress_bar.progress(progress)
        
        if level == "error":
            status_container.error(f"🚫 {message}")
        elif level == "warning":
            status_container.warning(f"⚠️ {message}")
        elif level == "success":
            status_container.success(f"✅ {message}")
        else:
            status_container.info(f"🔄 {message}")
        logger.debug(f"Progress update [{level}]: {message}")
        
    try:
        # Update the function call to include the required parameters and search_params
        status.update(label=f"Starting Google SERP search for: {search_keywords}")
        
        # Add search params to the Google SERP search
        google_search_params = {
            "max_results": search_params.get("max_results", 10)
        }
        
        # Include domains if provided
        if search_params.get("include_domains"):
            google_search_params["include_domains"] = search_params.get("include_domains")
        
        google_search_result = do_google_serp_search(
            search_keywords, 
            status_container=status_container,
            update_progress=update_progress,
            **google_search_params
        )
        
        if google_search_result and google_search_result.get('titles') and len(google_search_result.get('titles', [])) > 0:
            status.update(label=f"✅ Finished with Google web for Search: {search_keywords}")
            g_titles = google_search_result.get('titles', [])
            return google_search_result, g_titles, True
        else:
            # Check if there's an error message in the result
            if google_search_result and 'summary' in google_search_result and 'Error' in google_search_result['summary']:
                error_msg = google_search_result['summary']
                status.update(label=f"❌ Google search failed: {error_msg}", state="error")
                st.error(f"Google SERP search failed: {error_msg}")
            else:
                status.update(label="❌ Failed to get Google SERP results. No valid data returned.", state="error")
                st.error("Google SERP search failed to return valid results.")
            return google_search_result, [], False
    except Exception as err:
        status.update(label=f"❌ Google search error: {str(err)}", state="error")
        st.error(f"Google web research failed: {err}")
        logger.error(f"Failed in Google web research: {err}")
        return None, [], False


def perform_tavily_search(search_keywords, search_params, status):
    """
    Perform Tavily AI search for the given keywords.
    
    Args:
        search_keywords (str): Keywords to search for
        search_params (dict): Search parameters
        status: Streamlit status object
        
    Returns:
        tuple: (tavily_search_result, success_flag)
    """
    try:
        status.update(label=f"🔍 Starting Tavily AI research: {search_keywords}")
        
        # Pass the search parameters to Tavily
        tavily_result_tuple = do_tavily_ai_search(
            search_keywords,
            max_results=search_params.get("max_results", 10),
            search_depth=search_params.get("search_depth", "basic"),
            include_domains=search_params.get("include_domains", []),
            time_range=search_params.get("time_range", "year")
        )
        
        if tavily_result_tuple and len(tavily_result_tuple) == 3:
            tavily_search_result, t_titles, t_answer = tavily_result_tuple
            # If we have either titles or an answer, consider it a success
            if (t_titles and len(t_titles) > 0) or (t_answer and len(t_answer) > 10):
                status.update(label=f"✅ Finished Tavily AI Search on: {search_keywords}", state="complete")
                return tavily_search_result, True
            else:
                status.update(label="❌ Tavily search returned empty results", state="error")
                st.warning("Tavily search didn't find relevant information.")
                return tavily_search_result, False
        else:
            status.update(label="❌ Tavily search returned incomplete results", state="error")
            st.error("Tavily search failed to return valid results.")
            return None, False
            
    except Exception as err:
        status.update(label=f"❌ Tavily search error: {str(err)}", state="error")
        st.error(f"Failed in Tavily web research: {err}")
        logger.error(f"Failed in Tavily web research: {err}")
        return None, False


def generate_blog_content(search_keywords, google_search_result, tavily_search_result, 
                         google_search_success, tavily_search_success, blog_params, status):
    """
    Generate blog content using either Google or Tavily search results.
    
    Args:
        search_keywords (str): Search keywords
        google_search_result: Results from Google search
        tavily_search_result: Results from Tavily search
        google_search_success (bool): Whether Google search was successful
        tavily_search_success (bool): Whether Tavily search was successful
        blog_params (dict): Blog parameters
        status: Streamlit status object
        
    Returns:
        str: Generated blog content or None if generation failed
    """
    # Check if both searches failed - if so, stop the process
    if not google_search_success and not tavily_search_success:
        st.error("⛔ Both Google SERP and Tavily AI searches failed. Unable to generate blog content.")
        st.warning("Please check your API keys in the environment settings and try again.")
        return None

    # Try Google results first if available
    if google_search_success and 'results' in google_search_result:
        try:
            status.update(label=f"✏️ Writing blog from Google Search results...")
            # Pass blog parameters to the blog writing function
            blog_style_info = f"""
            Length: {blog_params.get('blog_length')} words
            Tone: {blog_params.get('blog_tone')}
            Target Audience: {blog_params.get('blog_demographic')}
            Blog Type: {blog_params.get('blog_type')}
            Language: {blog_params.get('blog_language')}
            """
            status.update(label=f"✏️ Writing {blog_params.get('blog_tone')} {blog_params.get('blog_type')} blog for {blog_params.get('blog_demographic')} audience...")
            blog_markdown_str = write_blog_google_serp(search_keywords, google_search_result['results'], blog_params=blog_params)
            status.update(label="✅ Generated content from Google search results", state="complete")
            return blog_markdown_str
        except Exception as err:
            status.update(label=f"❌ Failed to generate content from Google results: {str(err)}", state="error")
            st.error(f"Failed to generate content from Google results: {err}")
            logger.error(f"Failed to process Google search results: {err}")
    
    # If Google failed or had no results, try Tavily
    if tavily_search_success and tavily_search_result:
        try:
            status.update(label=f"✏️ Writing blog from Tavily search results...")
            status.update(label=f"✏️ Writing {blog_params.get('blog_tone')} {blog_params.get('blog_type')} blog for {blog_params.get('blog_demographic')} audience...")
            blog_markdown_str = write_blog_google_serp(search_keywords, tavily_search_result, blog_params=blog_params)
            status.update(label="✅ Generated content from Tavily search results", state="complete")
            return blog_markdown_str
        except Exception as err:
            status.update(label=f"❌ Failed to generate content from Tavily results: {str(err)}", state="error")
            st.error(f"Failed to generate content from Tavily results: {err}")
            logger.error(f"Failed to process Tavily search results: {err}")
    
    # If we still don't have content, show error
    st.error("⛔ Failed to generate any blog content from the research results.")
    return None


def generate_blog_metadata(blog_markdown_str, search_keywords, status):
    """
    Generate metadata for the blog content.
    
    Args:
        blog_markdown_str (str): Blog content
        search_keywords (str): Original search keywords
        status: Streamlit status object
        
    Returns:
        tuple: (blog_title, blog_meta_desc, blog_tags, blog_categories)
    """
    status.update(label="🔍 Generating title, meta description, tags, and categories...")
    try:
        blog_title, blog_meta_desc, blog_tags, blog_categories = asyncio.run(blog_metadata(blog_markdown_str))
        status.update(label="✅ Generated blog metadata successfully")
        return blog_title, blog_meta_desc, blog_tags, blog_categories
    except Exception as err:
        st.error(f"Failed to get blog metadata: {err}")
        logger.error(f"Failed to get blog metadata: {err}")
        status.update(label="❌ Failed to get blog metadata", state="error")
        return None, None, None, None
    

def generate_blog_image(blog_title, blog_meta_desc, blog_markdown_str, status):
    """
    Generate a featured image for the blog.
    
    Args:
        blog_title (str): Blog title
        blog_meta_desc (str): Blog meta description
        blog_markdown_str (str): Blog content
        status: Streamlit status object
        
    Returns:
        str: Path to the generated image or None if generation failed
    """
    try:
        status.update(label="🖼️ Generating featured image for blog...")
        
        # Create a better prompt for image generation
        if blog_title and blog_meta_desc:
            # If we have both title and description, use them
            text_to_image = f"{blog_title}: {blog_meta_desc}"
        elif blog_title:
            # If we only have title, use it
            text_to_image = blog_title
        elif blog_meta_desc:
            # If we only have description, use it
            text_to_image = blog_meta_desc
        else:
            # Fallback to first 200 chars of content
            text_to_image = blog_markdown_str[:200]
        
        # Ensure the prompt is of reasonable length
        if len(text_to_image) > 300:
            text_to_image = text_to_image[:300]
        
        # Log the prompt being used
        logger.info(f"Generating image with prompt: {text_to_image}")
        status.update(label=f"🖼️ Creating image with prompt: \"{text_to_image[:50]}...\"")
        
        # Attempt image generation
        generated_image_filepath = generate_image(text_to_image)
        
        # If first attempt failed, try with a simplified prompt
        if not generated_image_filepath:
            logger.warning("First image generation attempt failed, trying with simplified prompt")
            status.update(label="⚠️ First image attempt failed, trying again with simplified prompt...")
            
            # Create a simpler prompt
            simplified_prompt = " ".join(text_to_image.split()[:10])
            generated_image_filepath = generate_image(simplified_prompt)
        
        if generated_image_filepath:
            status.update(label="✅ Successfully generated featured image")
            return generated_image_filepath
        else:
            status.update(label="❌ Image generation failed - no image created", state="error")
            return None
            
    except Exception as err:
        st.warning(f"Failed in Image generation: {err}")
        logger.error(f"Failed in Image generation: {err}")
        status.update(label="❌ Image generation failed - no image created", state="error")
        return None


def regenerate_blog_image(blog_title, blog_meta_desc, blog_markdown_str):
    """
    Regenerate a blog image on demand.
    
    Args:
        blog_title (str): Blog title
        blog_meta_desc (str): Blog meta description
        blog_markdown_str (str): Blog content
        
    Returns:
        str: Path to the generated image or None if generation failed
    """
    with st.status("Regenerating image...", expanded=True) as status:
        try:
            # Use keywords from title or description
            if blog_title:
                keywords = " ".join(blog_title.split()[:6])
                prompt = f"Blog illustration for: {keywords}"
            elif blog_meta_desc:
                keywords = " ".join(blog_meta_desc.split()[:6])
                prompt = f"Blog illustration for: {keywords}"
            else:
                keywords = blog_markdown_str.split()[:50]
                prompt = f"Blog illustration based on: {' '.join(keywords[:6])}"
                
            status.update(label=f"🖼️ Generating new image with prompt: \"{prompt}\"")
            
            # Generate the image
            generated_image_filepath = generate_image(prompt)
            
            if generated_image_filepath:
                status.update(label="✅ Successfully generated new image", state="complete")
                return generated_image_filepath
            else:
                status.update(label="❌ Image regeneration failed", state="error")
                return None
                
        except Exception as err:
            st.error(f"Failed to regenerate image: {err}")
            logger.error(f"Image regeneration error: {err}")
            status.update(label="❌ Image regeneration failed", state="error")
            return None


def save_blog_content(blog_markdown_str, blog_title, blog_meta_desc, blog_tags, blog_categories, generated_image_filepath, status):
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
    # Initialize parameters with defaults
    search_params, blog_params = initialize_parameters(search_params, blog_params)
    
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
    
    # Set up processing variables
    blog_markdown_str = None
    example_blog_titles = []
    google_search_success = False
    tavily_search_success = False
    blog_title = None
    blog_meta_desc = None
    blog_tags = None
    blog_categories = None
    generated_image_filepath = None
    saved_blog_to_file = None
    
    # STEP 1: Research phase
    update_progress(1, 5, f"Starting web research on '{search_keywords}'")
    logger.info(f"Researching and Writing Blog on keywords: {search_keywords}")
    
    # Create a section header for the research phase
    st.subheader("🔍 Web Research Progress")
    
    # Use a container instead of an expander
    research_container = st.container()
    with research_container:
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
    
    # Check if both searches failed - if so, stop the process
    if not google_search_success and not tavily_search_success:
        update_progress(5, 5, "Research failed")
        progress_placeholder.error("⛔ Both Google SERP and Tavily AI searches failed. Unable to generate blog content.")
        st.warning("Please check your API keys in the environment settings and try again.")
        st.stop()
        return None
    
    # STEP 2: Content generation phase
    update_progress(2, 5, "Generating blog content from research")
    
    # Create a section header for the content generation phase
    st.subheader("✍️ Content Generation Progress")
    
    # Use a container instead of an expander
    content_container = st.container()
    with content_container:
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
                update_progress(5, 5, "Content generation failed")
                progress_placeholder.error("⛔ Failed to generate blog content from research data.")
                st.stop()
                return None
    
    # STEP 3: Metadata & enhancement phase
    update_progress(3, 5, "Generating SEO metadata and enhancements")
    
    # Create a section header for the enhancement phase
    st.subheader("🔍 SEO & Enhancement Progress")
    
    # Use a container instead of an expander
    enhancement_container = st.container()
    with enhancement_container:
        # Create a status element for enhancement updates
        with st.status("Enhancing content...", expanded=True) as status:
            # Generate metadata
            status.update(label="🏷️ Generating SEO metadata (title, description, tags)...")
            blog_title, blog_meta_desc, blog_tags, blog_categories = generate_blog_metadata(
                blog_markdown_str, search_keywords, status
            )
            
            if blog_title and blog_meta_desc:
                status.update(label=f"✅ Generated metadata: \"{blog_title}\"")
                
                # Generate featured image
                status.update(label="🖼️ Creating featured image...")
                generated_image_filepath = generate_blog_image(
                    blog_title, blog_meta_desc, blog_markdown_str, status
                )
                
                # Save blog content to file
                status.update(label="💾 Saving blog content...")
                saved_blog_to_file = save_blog_content(
                    blog_markdown_str, blog_title, blog_meta_desc, blog_tags, 
                    blog_categories, generated_image_filepath, status
                )
                
                status.update(label="✅ Content enhancement complete", state="complete")
            else:
                status.update(label="⚠️ Metadata generation had issues, using simplified format", state="warning")
    
    # STEP 4: Final presentation
    update_progress(4, 5, "Preparing final blog presentation")
    
    # Now display the final blog content
    with final_content_placeholder.container():
        st.markdown("---")
        st.header("📝 Generated Blog Content")
        
        # Display metadata
        if blog_title:
            st.title(blog_title)
        
        if blog_meta_desc:
            st.markdown(f"*{blog_meta_desc}*")
            
        if blog_tags:
            st.markdown(f"**Tags:** {', '.join(blog_tags)}")
            
        if blog_categories:
            st.markdown(f"**Categories:** {', '.join(blog_categories)}")
            
        # Image section with regeneration option
        st.subheader("🖼️ Featured Image")
        image_container = st.container()
        
        # Display featured image
        with image_container:
            if generated_image_filepath:
                st.image(generated_image_filepath, caption=blog_title or "Featured Image", use_column_width=True)
                
                # Add regenerate button
                if st.button("🔄 Regenerate Image", key="regenerate_image"):
                    new_image_path = regenerate_blog_image(blog_title, blog_meta_desc, blog_markdown_str)
                    if new_image_path:
                        generated_image_filepath = new_image_path
                        st.rerun()  # Refresh the page to show the new image
            else:
                st.info("No featured image was generated. Click below to generate one.")
                if st.button("🖼️ Generate Image", key="generate_image"):
                    new_image_path = regenerate_blog_image(blog_title, blog_meta_desc, blog_markdown_str)
                    if new_image_path:
                        generated_image_filepath = new_image_path
                        st.rerun()  # Refresh the page to show the new image
            
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
    
    # Final progress update
    update_progress(5, 5, "Blog generation complete!")
    
    # Replace progress bar with success message
    progress_placeholder.success("✅ Blog generation process completed successfully!")
    
    return blog_markdown_str

# Local wrapper functions to handle the parameter mismatch
def do_google_serp_search(search_keywords, status_container=None, update_progress=None, **kwargs):
    """
    Wrapper function to handle the parameter mismatch with the original function.
    """
    try:
        if status_container is None:
            status_container = st.empty()
        
        if update_progress is None:
            def update_progress(message, progress=None, level="info"):
                if level == "error":
                    status_container.error(message)
                elif level == "warning":
                    status_container.warning(message)
                else:
                    status_container.info(message)
        
        # Create a fixed update_progress function that handles any progress type
        def safe_update_progress(message, progress=None, level="info"):
            try:
                # Handle progress value of different types
                if progress is not None:
                    if isinstance(progress, str):
                        # Try to convert string to float if it represents a number
                        try:
                            progress = float(progress)
                        except ValueError:
                            # If conversion fails, just log the message without updating progress
                            progress = None
                
                # Call the original update_progress with sanitized values
                update_progress(message, progress, level)
            except Exception as err:
                # If there's an error in the progress function, just log to console
                logger.error(f"Error in progress update: {err}")
                # Try one more time with just the message
                try:
                    update_progress(message, None, level)
                except:
                    pass
        
        # Set default search parameters - fix the parameter to use 'max_results' not 'num_results'
        search_params = {
            "max_results": kwargs.get("max_results", 10),
            "include_domains": kwargs.get("include_domains", []),
            "search_depth": kwargs.get("search_depth", "basic")
        }
        
        # Update status to indicate we're checking API keys
        status_container.info("🔑 Checking required API keys...")
        
        # Call the original function with the required parameters
        result = gpt_do_google_serp_search(search_keywords, status_container, safe_update_progress, **search_params)
        return result
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in do_google_serp_search wrapper: {error_msg}")
        
        # Check for common error patterns and display user-friendly messages
        if "SERPER_API_KEY is missing" in error_msg:
            status_container.error("🔑 Google search API key (SERPER_API_KEY) is missing. Please check your environment settings.")
            st.error("Google SERP search failed: API key is missing. Using alternative methods.")
        elif "Progress Value has invalid type" in error_msg:
            # This is an internal error, log it but show a more user-friendly message
            status_container.warning("⚠️ Internal progress tracking error. Continuing with search.")
        else:
            # For unknown errors, show the full error message
            status_container.error(f"🚫 Google search error: {error_msg}")
            st.error(f"Google SERP search failed: {error_msg}")
        
        # Return a minimal result structure to prevent downstream errors
        return {
            'results': {},
            'titles': [],
            'summary': f"Error occurred during search: {error_msg}",
            'stats': {
                'organic_count': 0,
                'questions_count': 0,
                'related_count': 0
            }
        }

def do_tavily_ai_search(keywords, max_results=10, search_depth="basic", include_domains=None, time_range="year"):
    """
    Wrapper function for Tavily search to handle parameter differences.
    
    Args:
        keywords (str): Keywords to search for
        max_results (int): Maximum number of search results to return
        search_depth (str): "basic" or "advanced" search depth
        include_domains (list): List of domains to prioritize in search
        time_range (str): Time range for results ("day", "week", "month", "year", "all")
    """
    status_container = st.empty()
    
    if include_domains is None:
        include_domains = []
    
    try:
        # Show status message
        status_container.info(f"🔍 Preparing Tavily AI search with {search_depth} depth...")
        
        # FIXED: Ensure all parameters have correct types to prevent comparison errors
        tavily_params = {
            'max_results': int(max_results),  # Explicitly convert to int
            'search_depth': str(search_depth),  # Ensure this is a string
            'include_domains': include_domains,
            'time_range': str(time_range)
        }
        
        # Log the parameters for debugging
        logger.info(f"Tavily search parameters: {tavily_params}")
        
        # Check for API key before making the request
        tavily_api_key = os.environ.get("TAVILY_API_KEY")
        if not tavily_api_key:
            status_container.error("🔑 Tavily API key (TAVILY_API_KEY) is missing. Please check your environment settings.")
            st.error("Tavily search failed: API key is missing. Using alternative methods.")
            return None, [], "API key missing"
        
        status_container.info(f"🔍 Searching with Tavily AI using {search_depth} depth for: {keywords}")
        
        # Direct implementation without calling gpt_do_tavily_ai_search to avoid type issues
        try:
            from ..ai_web_researcher.tavily_ai_search import do_tavily_ai_search as tavily_direct_search
            # Call the function directly with correct parameter types
            tavily_raw_results = tavily_direct_search(
                keywords,
                max_results=tavily_params['max_results'],
                search_depth=tavily_params['search_depth'],
                include_domains=tavily_params['include_domains'],
                time_range=tavily_params['time_range']
            )
            
            # Extract the needed information
            if isinstance(tavily_raw_results, tuple) and len(tavily_raw_results) == 3:
                # If already in the right format, use it directly
                return tavily_raw_results
                
            # Process the results to extract titles and answer
            t_results = tavily_raw_results
            t_titles = []
            t_answer = ""
            
            # Extract titles from results if available
            if isinstance(t_results, dict):
                if 'results' in t_results and isinstance(t_results['results'], list):
                    t_titles = [r.get('title', '') for r in t_results['results']]
                    status_container.success(f"✅ Found {len(t_titles)} relevant articles")
                if 'answer' in t_results:
                    t_answer = t_results['answer']
                    status_container.success("✅ Generated a summary answer")
            
            return t_results, t_titles, t_answer
            
        except ImportError:
            # Fall back to the original function if direct import fails
            status_container.warning("⚠️ Using fallback Tavily search method...")
            logger.warning("Using fallback Tavily search method")
            
            # FIXED: Alternative approach - wrap the call in try/except to handle type errors
            try:
                tavily_result = gpt_do_tavily_ai_search(keywords, **tavily_params)
                
                # Format the result to match what the blog writer expects
                if isinstance(tavily_result, tuple) and len(tavily_result) == 3:
                    status_container.success("✅ Tavily search completed successfully")
                    return tavily_result
                
                # If not a tuple with expected values, try to extract what we need
                t_results = tavily_result
                
                # Extract titles and answer if available
                t_titles = []
                t_answer = ""
                
                if isinstance(t_results, dict):
                    if 'results' in t_results and isinstance(t_results['results'], list):
                        t_titles = [r.get('title', '') for r in t_results['results']]
                        status_container.success(f"✅ Found {len(t_titles)} relevant articles")
                    if 'answer' in t_results:
                        t_answer = t_results['answer']
                        status_container.success("✅ Generated a summary answer")
                
                return t_results, t_titles, t_answer
                
            except TypeError as type_err:
                # Handle the specific type error more gracefully
                error_msg = str(type_err)
                logger.error(f"Type error in Tavily search: {error_msg}")
                
                if "'>' not supported" in error_msg:
                    status_container.error("🚫 Tavily search parameter type error. Trying alternative approach...")
                    
                    # Try a simpler approach with minimal parameters
                    try:
                        # Call with only the keyword and fixed max_results
                        tavily_result = gpt_do_tavily_ai_search(keywords, max_results=10)
                        
                        # Minimal processing to extract titles and answer
                        t_results = tavily_result
                        t_titles = []
                        t_answer = ""
                        
                        if isinstance(t_results, dict):
                            if 'results' in t_results and isinstance(t_results['results'], list):
                                t_titles = [r.get('title', '') for r in t_results['results']]
                            if 'answer' in t_results:
                                t_answer = t_results['answer']
                        
                        return t_results, t_titles, t_answer
                    except Exception as inner_err:
                        logger.error(f"Alternative Tavily approach also failed: {inner_err}")
                        raise
                else:
                    # Re-raise other type errors
                    raise
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in do_tavily_ai_search wrapper: {error_msg}")
        
        # Display user-friendly error message
        status_container.error(f"🚫 Tavily search error: {error_msg}")
        st.error(f"Tavily AI search failed: {error_msg}")
        
        # Return empty results to prevent downstream errors
        return None, [], f"Error: {error_msg}"
    
    finally:
        # Clear the status container after a delay
        time.sleep(2)
        status_container.empty()
