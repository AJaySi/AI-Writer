import re
import os
import json
import asyncio
from loguru import logger
import PyPDF2
import streamlit as st
import tiktoken
import openai
from datetime import datetime

from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
# Remove the circular import
# from lib.ai_writers.ai_blog_writer.keywords_to_blog_streamlit import write_blog_from_keywords
from lib.ai_writers.speech_to_blog.main_audio_to_blog import generate_audio_blog
from lib.ai_writers.long_form_ai_writer import long_form_generator
from lib.ai_writers.web_url_ai_writer import blog_from_url
from lib.ai_writers.image_ai_writer import blog_from_image
from .blog_from_google_serp import write_blog_google_serp
from lib.blog_metadata.get_blog_metadata import blog_metadata
from lib.gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

# Constants
CONFIG_PATH = os.path.join("lib", "workspace", "alwrity_config", "main_config.json")
DEFAULT_CONFIG = {
    "Search Engine Parameters": {
        "Geographic Location": "us",
        "Search Language": "en",
        "Number of Results": 10,
        "Time Range": "year"
    }
}

# Function to load configuration from JSON file
def load_config():
    """Load configuration from the main config JSON file."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded configuration from {CONFIG_PATH}")
                return config
        else:
            logger.warning(f"Configuration file not found at {CONFIG_PATH}, using defaults")
            return DEFAULT_CONFIG
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return DEFAULT_CONFIG

# Function to get search parameters from config
def get_search_params_from_config():
    """Extract search parameters from the main configuration."""
    config = load_config()
    search_params = config.get("Search Engine Parameters", {})
    
    # Map config values to expected parameter names
    result = {
        "max_results": search_params.get("Number of Results", 10),
        "time_range": search_params.get("Time Range", "year").lower(),
        "geo": search_params.get("Geographic Location", "us"),
        "language": search_params.get("Search Language", "en")
    }
    
    # Normalize time_range to match our options
    time_map = {
        "day": "day",
        "week": "week", 
        "month": "month",
        "year": "year",
        "anytime": "all",
        "all": "all"
    }
    result["time_range"] = time_map.get(result["time_range"].lower(), "year")
    
    logger.info(f"Using search parameters from config: {result}")
    return result

# Function to get blog content characteristics from config
def get_blog_characteristics_from_config():
    """Extract blog content characteristics from the main configuration."""
    config = load_config()
    blog_characteristics = config.get("Blog Content Characteristics", {})
    
    # Map config values to expected parameter names
    result = {
        "blog_length": blog_characteristics.get("Blog Length", "2000"),
        "blog_tone": blog_characteristics.get("Blog Tone", "Professional"),
        "blog_demographic": blog_characteristics.get("Blog Demographic", "Professional"),
        "blog_type": blog_characteristics.get("Blog Type", "Informational"),
        "blog_language": blog_characteristics.get("Blog Language", "English"),
        "blog_output_format": blog_characteristics.get("Blog Output Format", "markdown")
    }
    
    logger.info(f"Using blog characteristics from config: {result}")
    return result

# Function to get blog image details from config
def get_blog_images_from_config():
    """Extract blog image details from the main configuration."""
    config = load_config()
    blog_images = config.get("Blog Images Details", {})
    
    # Map config values to expected parameter names
    result = {
        "image_model": blog_images.get("Image Generation Model", "stable-diffusion"),
        "num_images": int(blog_images.get("Number of Blog Images", 1)),
        "image_style": blog_images.get("Image Style", "Realistic")
    }
    
    logger.info(f"Using blog image details from config: {result}")
    return result

# Function to get LLM options from config
def get_llm_options_from_config():
    """Extract LLM options from the main configuration."""
    config = load_config()
    llm_options = config.get("LLM Options", {})
    
    # Map config values to expected parameter names
    result = {
        "provider": llm_options.get("GPT Provider", "google"),
        "model": llm_options.get("Model", "gemini-1.5-flash-latest"),
        "temperature": float(llm_options.get("Temperature", 0.7)),
        "max_tokens": int(llm_options.get("Max Tokens", 4000))
    }
    
    logger.info(f"Using LLM options from config: {result}")
    return result

# Split a text into smaller chunks of size n, preferably ending at the end of a sentence
def create_chunks(text, n, tokenizer):
    tokens = tokenizer.encode(text)
    """Yield successive n-sized chunks from text."""
    i = 0
    while i < len(tokens):
        # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
        j = min(i + int(1.5 * n), len(tokens))
        while j > i + int(0.5 * n):
            # Decode the tokens and check for full stop or newline
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + int(0.5 * n):
            j = min(i + n, len(tokens))
        yield tokens[i:j]
        i = j


def extract_chunk(document, template_prompt):
    """ Chunking for large documents, exceed context window"""
    prompt = template_prompt.replace('<document>', document)

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Failed to get response from LLM: {err}")
        raise


def blog_from_pdf(pdf_text):
    """ 
    Load in a long PDF and extract key information.
    Chunk up document and process each chunk, then combine them.
    """
    template_prompt=f'''Extract key pieces of information from the given document.

        When you extract a key piece of information, include the closest page number.
        Ex: Extracted Information (Page number)
        \n\nDocument: \"\"\"<document>\"\"\"\n\n'''

    # Initialize tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")
    results = []
    
    chunks = create_chunks(pdf_text, 1000, tokenizer)
    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]

    for chunk in text_chunks:
        try:
            results.append(extract_chunk(chunk, template_prompt))
        except Exception as e:
            logger.error(f"Error processing chunk: {e}")
            # Continue with other chunks even if one fails
            continue

    return results


# Input validation functions
def is_youtube_link(text):
    """Check if text is a valid YouTube link."""
    if text is not None:
        youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        return youtube_regex.match(text)
    return False


def is_web_link(text):
    """Check if text is a valid web link."""
    if text is not None:
        web_regex = re.compile(r'(https?://)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
        return web_regex.match(text)
    return False
    

def process_input(input_text, uploaded_file):
    """
    Determine the type of input provided by the user.
    
    Args:
        input_text (str): The text input from the user
        uploaded_file: The file uploaded by the user
        
    Returns:
        str: The determined input type ("youtube_url", "web_url", "keywords", "PDF_file", "image_file", "audio_file", "video_file", or None)
    """
    # Process text input
    if input_text:
        if is_youtube_link(input_text):
            if input_text.startswith("https://www.youtube.com/") or input_text.startswith("http://www.youtube.com/"):
                return "youtube_url"
            else:
                st.error("Invalid YouTube URL. Please enter a valid URL.")
                return None
        elif is_web_link(input_text):
            return "web_url"
        else:
            return "keywords"
    
    # Process file input
    if uploaded_file is not None:
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type}
        st.write(file_details)
        
        # Handle different file types
        if uploaded_file.type.startswith("text/"):
            content = uploaded_file.read().decode("utf-8")
            st.text(content)
            return "text_file"
        elif uploaded_file.type == "application/pdf":
            return "PDF_file"
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            st.write("Word document uploaded. Add your DOCX processing logic here.")
            return "word_file"
        elif uploaded_file.type.startswith("image/"):
            st.image(uploaded_file)
            return "image_file"
        elif uploaded_file.type.startswith("audio/"):
            st.audio(uploaded_file)
            return "audio_file"
        elif uploaded_file.type.startswith("video/"):
            st.video(uploaded_file)
            return "video_file"
    
    return None


# Content processing functions
def process_keywords_input(user_input, search_params, blog_params, selected_content_type):
    """Process keywords input and generate content based on the selected options."""
    if not user_input or len(user_input.split()) < 2:
        st.error('Please provide at least two keywords for best results')
        return False
    
    # Check for dialog states and handle them directly
    if st.session_state.get("show_title_dialog", False):
        st.warning("Please use the main function to handle title refinement dialog")
        # Clear the dialog state to avoid getting stuck
        st.session_state.show_title_dialog = False
        return False
        
    if st.session_state.get("show_meta_dialog", False):
        st.warning("Please use the main function to handle meta description refinement dialog")
        # Clear the dialog state to avoid getting stuck
        st.session_state.show_meta_dialog = False
        return False
        
    if st.session_state.get("show_snippet_dialog", False):
        st.warning("Please use the main function to handle structured data dialog")
        # Clear the dialog state to avoid getting stuck
        st.session_state.show_snippet_dialog = False
        return False
    
    try:
        if selected_content_type == "Normal-length content":
            st.subheader("Your Generated Blog Post")
            logger.info(f"Generating standard blog post with parameters: {blog_params}")
            
            # Use a direct approach to generate blog content to avoid nested expanders
            # Instead of importing write_blog_from_keywords which contains many expanders
            try:
                # Show simplified progress UI
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Initialize and show progress
                    status_text.info("Initializing blog generation...")
                    progress_bar.progress(0.1)
                    
                    # Initialize parameters
                    from .blog_ai_research_utils import initialize_parameters
                    search_params, blog_params = initialize_parameters(search_params, blog_params)
                    
                    # Step 2: Research phase
                    status_text.info("Researching your topic...")
                    progress_bar.progress(0.2)
                    
                    # Perform research using direct function calls
                    from .blog_ai_research_utils import do_google_serp_search, do_tavily_ai_search
                    
                    # Do Google search
                    status_text.info("Searching Google for relevant information...")
                    google_result = do_google_serp_search(user_input, max_results=search_params.get("max_results", 10))
                    google_success = google_result and 'results' in google_result and google_result['results']
                    progress_bar.progress(0.4)
                    
                    # Do Tavily search if needed
                    tavily_result = None
                    tavily_success = False
                    if not google_success:
                        status_text.info("Performing additional research with Tavily...")
                        tavily_result, _, _ = do_tavily_ai_search(
                            user_input,
                            max_results=search_params.get("max_results", 10),
                            search_depth=search_params.get("search_depth", "basic")
                        )
                        tavily_success = tavily_result is not None
                    progress_bar.progress(0.5)
                    
                    # Step 3: Generate content
                    status_text.info("Generating blog content...")
                    progress_bar.progress(0.6)
                    
                    # Generate content based on search results
                    from .blog_from_google_serp import write_blog_google_serp
                    
                    if google_success:
                        blog_content = write_blog_google_serp(user_input, google_result['results'], blog_params=blog_params)
                    elif tavily_success:
                        blog_content = write_blog_google_serp(user_input, tavily_result, blog_params=blog_params)
                    else:
                        status_text.error("Failed to gather research data. Please try again.")
                        return False
                    
                    # Step 4: Generate metadata and image
                    status_text.info("Adding metadata and final touches...")
                    progress_bar.progress(0.8)
                    
                    # Import functions from keywords_to_blog_streamlit
                    from .keywords_to_blog_streamlit import generate_audio_version
                    
                    # Define a simple update_progress function for compatibility
                    def simple_update_progress(step, total, message):
                        status_text.info(message)
                        progress_bar.progress(step / total)
                    
                    # Generate metadata and image
                    # Import only essential functions needed for core processing
                    from .ai_blog_generator_utils import generate_blog_metadata, generate_blog_image
                    try:
                        # Create a proper status object
                        with st.status("Generating metadata and image...", expanded=True) as status:
                            # Generate metadata
                            blog_title, blog_meta_desc, blog_tags, blog_categories, blog_hashtags, blog_slug = generate_blog_metadata(
                                blog_content, user_input, status)
                            
                            # Generate featured image if metadata is available
                            generated_image_filepath = None
                            if blog_title and blog_meta_desc:
                                generated_image_filepath = generate_blog_image(
                                    blog_title, blog_meta_desc, blog_content, status, blog_tags)
                            
                            # Save blog content to file
                            saved_blog_to_file = None
                            from ...blog_postprocessing.save_blog_to_file import save_blog_to_file
                            if blog_title and blog_meta_desc:
                                saved_blog_to_file = save_blog_to_file(
                                    blog_content, blog_title, blog_meta_desc, blog_tags, 
                                    blog_categories, generated_image_filepath)
                        
                        # Create metadata dictionary with string conversions for table display
                        metadata = {
                            "blog_title": blog_title or "",
                            "blog_meta_desc": blog_meta_desc or "",
                            "blog_tags": ", ".join(blog_tags) if isinstance(blog_tags, list) else str(blog_tags or ""),
                            "blog_categories": ", ".join(blog_categories) if isinstance(blog_categories, list) else str(blog_categories or ""),
                            "blog_hashtags": blog_hashtags or "",
                            "blog_slug": blog_slug or ""
                        }
                    except Exception as e:
                        logger.error(f"Error generating metadata or image: {e}")
                        metadata = {
                            "blog_title": "Generated Blog",
                            "blog_meta_desc": "",
                            "blog_tags": "",
                            "blog_categories": "",
                            "blog_hashtags": "",
                            "blog_slug": ""
                        }
                        generated_image_filepath = None
                        saved_blog_to_file = None
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Final message
                    final_message = st.empty()
                    final_message.success("Blog generation complete!")
                    
                    # Display blog content first (without using expanders)
                    st.markdown("## Content")
                    st.markdown(blog_content)
                    
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
                            generate_audio_version(blog_content)
                    
                    # Display metadata success message
                    if metadata["blog_title"]:
                        st.success(f"✅ Generated metadata for: {metadata['blog_title']}")
                    
                    # Display metadata table (without nesting expanders)
                    st.markdown("---")
                    st.subheader("🏷️ Blog SEO Metadata")
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
                    
                    # Display image if available
                    if generated_image_filepath:
                        st.subheader("🖼️ Featured Image")
                        st.image(generated_image_filepath, caption=metadata["blog_title"] or "Featured Image", use_column_width=True)
                        
                        # Add regenerate button
                        if st.button("🔄 Regenerate Image", key="regenerate_image_simplified"):
                            # Use the function directly to avoid any nested expanders
                            new_image_path = regenerate_blog_image(
                                metadata["blog_title"], 
                                metadata["blog_meta_desc"], 
                                blog_content, 
                                metadata["blog_tags"]
                            )
                            if new_image_path:
                                st.success("✅ Image regenerated successfully!")
                                st.image(new_image_path, caption=metadata["blog_title"], use_column_width=True)
                    else:
                        st.subheader("🖼️ Featured Image")
                        st.info("No image was generated. Try regenerating the blog.")
                    
                    # Add refinement buttons directly, without using helper functions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Refine Blog Title", key="refine_title_simplified", use_container_width=True):
                            st.session_state.show_title_dialog = True
                            st.rerun()
                    with col2:
                        if st.button("🔄 Refine Meta Description", key="refine_meta_simplified", use_container_width=True):
                            st.session_state.show_meta_dialog = True
                            st.rerun()
                    
                    # Add structured data section directly, without using helper functions
                    st.markdown("---")
                    st.markdown("### Get Structured Data")
                    
                    structured_data_col1, structured_data_col2 = st.columns([3, 1])
                    with structured_data_col1:
                        st.info("Rich snippets boost visibility and click-through rates in search results.")
                    with structured_data_col2:
                        if st.button("📊 Generate Rich Snippet", key="snippet_simplified", use_container_width=True):
                            st.session_state.show_snippet_dialog = True
                            st.rerun()
                    
                    # Clear the success message after a delay
                    import time
                    time.sleep(3)
                    final_message.empty()
                    
                    return True
                    
            except Exception as inner_err:
                logger.error(f"Error in simplified blog generation: {inner_err}")
                st.error(f"Failed to generate blog content: {inner_err}")
                return False
                
        elif selected_content_type == "Long-form content":
            logger.info(f"Generating long-form content with parameters: {blog_params}")
            
            # Ensure all blog parameters are properly passed to long-form generator
            long_form_generator(
                user_input, 
                search_params=search_params, 
                blog_params=blog_params
            )
            
            # Show success message briefly then clear it
            success_msg = st.empty()
            success_msg.success(f"Successfully generated long-form content for: {user_input}")
            # Clear the message after 3 seconds
            import time
            time.sleep(3)
            success_msg.empty()
            
            return True
            
        else:
            info_msg = st.empty()
            info_msg.info("AI Agent Team feature is coming soon! This will provide multi-perspective content with different AI experts collaborating on your blog.")
            return False
            
    except Exception as err:
        logger.error(f"An error occurred while generating content: {err}")
        st.error(f"An error occurred while generating content: {err}")
        return False


def process_pdf_input(uploaded_file):
    """Process a PDF file and generate content."""
    # Replace expander with a container to avoid nested expanders
    pdf_container = st.container()
    with pdf_container:
        st.subheader("Processing PDF Document")
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        combined_result = ""
        
        # Show progress with better UI
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        total_pages = len(pdf_reader.pages)
        for page_num, page in enumerate(pdf_reader.pages):
            progress_text.text(f"Processing page {page_num+1}/{total_pages}")
            text += page.extract_text()
            text = text.replace("\n", " ")
            text = re.sub(r"(\w)([A-Z])", r"\1 \2", text)
            
            results = blog_from_pdf(text)
            progress_percent = (page_num + 1) / total_pages
            progress_bar.progress(progress_percent)
            combined_result += str(results[-1])
        
        progress_text.empty()
        progress_bar.empty()
        
    st.subheader("Generated Content from PDF")
    st.markdown(combined_result)
    return True


def process_youtube_or_audio(user_input):
    """Process a YouTube URL or audio file and generate content."""
    if not generate_audio_blog(user_input):
        return False
    return True


def process_web_url(user_input):
    """Process a web URL and generate content."""
    blog_from_url(user_input)
    return True


def process_image_input(user_input, uploaded_file):
    """Process an image file and generate content."""
    blog_from_image(user_input, uploaded_file)
    return True


def handle_content_generation(input_type, user_input, uploaded_file, search_params, blog_params, selected_content_type):
    """
    Handle content generation based on the input type.
    
    Args:
        input_type: The type of input ("youtube_url", "web_url", etc.)
        user_input: The text input from the user
        uploaded_file: The uploaded file (if any)
        search_params: Search parameters
        blog_params: Blog content parameters
        selected_content_type: The selected content type
        
    Returns:
        bool: True if content generation was successful, False otherwise
    """
    # Create a status placeholder instead of a permanent message
    status_message = st.empty()
    status_message.info("Crafting your blog content... Please wait.")
    
    try:
        if input_type == "keywords":
            result = process_keywords_input(user_input, search_params, blog_params, selected_content_type)
            # Clear the status message when done
            status_message.empty()
            return result
        
        elif input_type == "youtube_url" or input_type == "audio_file":
            result = process_youtube_or_audio(user_input)
            status_message.empty()
            return result
        
        elif input_type == "web_url":
            result = process_web_url(user_input)
            status_message.empty()
            return result
        
        elif input_type == "image_file":
            result = process_image_input(user_input, uploaded_file)
            status_message.empty()
            return result
        
        elif input_type == "PDF_file":
            result = process_pdf_input(uploaded_file)
            status_message.empty()
            return result
        
        else:
            status_message.empty()
            st.error(f"Unsupported input type: {input_type}")
            return False
    except Exception as e:
        status_message.empty()
        st.error(f"An error occurred during content generation: {str(e)}")
        return False


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
        tuple: (blog_title, blog_meta_desc, blog_tags, blog_categories, blog_hashtags, blog_slug)
    """
    status.update(label="🔍 Generating title, meta description, tags, categories, hashtags, and slug...")
    try:
        # Get all 6 metadata values from blog_metadata
        blog_title, blog_meta_desc, blog_tags, blog_categories, blog_hashtags, blog_slug = asyncio.run(blog_metadata(blog_markdown_str))
        status.update(label="✅ Generated blog metadata successfully")
        return blog_title, blog_meta_desc, blog_tags, blog_categories, blog_hashtags, blog_slug
    except Exception as err:
        st.error(f"Failed to get blog metadata: {err}")
        logger.error(f"Failed to get blog metadata: {err}")
        status.update(label="❌ Failed to get blog metadata", state="error")
        return None, None, None, None, None, None


def generate_blog_image(blog_title, blog_meta_desc, blog_markdown_str, status, blog_tags=None):
    """
    Generate a featured image for the blog.
    
    Args:
        blog_title (str): Blog title
        blog_meta_desc (str): Blog meta description
        blog_markdown_str (str): Blog content
        status: Streamlit status object
        blog_tags (list, optional): Blog tags to use for image prompt enhancement
        
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
        
        # Extract blog tags if available
        blog_tags_list = blog_tags if isinstance(blog_tags, list) else []
        
        # Attempt image generation with all available parameters
        generated_image_filepath = generate_image(
            user_prompt=text_to_image,
            title=blog_title,
            description=blog_meta_desc,
            tags=blog_tags_list,
            content=blog_markdown_str[:2000]  # Limit content length to avoid too large payloads
        )
        
        # If first attempt failed, try with a simplified prompt
        if not generated_image_filepath:
            logger.warning("First image generation attempt failed, trying with simplified prompt")
            status.update(label="⚠️ First image attempt failed, trying again with simplified prompt...")
            
            # Create a simpler prompt
            simplified_prompt = " ".join(text_to_image.split()[:10])
            generated_image_filepath = generate_image(
                user_prompt=simplified_prompt,
                title=blog_title,
                description=blog_meta_desc,
                tags=blog_tags_list,
                content=blog_markdown_str[:1000]  # Use even shorter content for the retry
            )
        
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


def regenerate_blog_image(blog_title, blog_meta_desc, blog_markdown_str, blog_tags=None):
    """
    Regenerate a blog image on demand.
    
    Args:
        blog_title (str): Blog title
        blog_meta_desc (str): Blog meta description
        blog_markdown_str (str): Blog content
        blog_tags (list, optional): Blog tags to use for image prompt enhancement
        
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
            
            # Extract any tags if available - will be passed as empty list otherwise
            blog_tags_list = blog_tags if isinstance(blog_tags, list) else []
            
            # Generate the image with all parameters
            generated_image_filepath = generate_image(
                user_prompt=prompt,
                title=blog_title,
                description=blog_meta_desc,
                tags=blog_tags_list,
                content=blog_markdown_str[:2000]  # Limit content length to avoid too large payloads
            )
            
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