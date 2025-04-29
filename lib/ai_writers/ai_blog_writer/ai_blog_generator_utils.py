import re
import os
import json
from loguru import logger
import PyPDF2
import streamlit as st
import tiktoken
import openai

from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.ai_writers.keywords_to_blog_streamlit import write_blog_from_keywords
from lib.ai_writers.speech_to_blog.main_audio_to_blog import generate_audio_blog
from lib.ai_writers.long_form_ai_writer import long_form_generator
from lib.ai_writers.web_url_ai_writer import blog_from_url
from lib.ai_writers.image_ai_writer import blog_from_image

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
    
    try:
        if selected_content_type == "Normal-length content":
            st.subheader("Your Generated Blog Post")
            logger.info(f"Generating standard blog post with parameters: {blog_params}")
            
            # Ensure all blog parameters are properly passed
            # This is important as the UI may have settings that aren't in the default blog_params
            short_blog = write_blog_from_keywords(
                user_input, 
                search_params=search_params, 
                blog_params=blog_params
            )
            st.markdown(short_blog)
            return True
            
        elif selected_content_type == "Long-form content":
            logger.info(f"Generating long-form content with parameters: {blog_params}")
            
            # Ensure all blog parameters are properly passed to long-form generator
            long_form_generator(
                user_input, 
                search_params=search_params, 
                blog_params=blog_params
            )
            st.success(f"Successfully generated long-form content for: {user_input}")
            return True
            
        else:
            st.info("AI Agent Team feature is coming soon! This will provide multi-perspective content with different AI experts collaborating on your blog.")
            return False
            
    except Exception as err:
        logger.error(f"An error occurred while generating content: {err}")
        st.error(f"An error occurred while generating content: {err}")
        return False


def process_pdf_input(uploaded_file):
    """Process a PDF file and generate content."""
    with st.expander("Processing PDF Document", expanded=True):
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
    with st.spinner("Crafting your blog content... Please wait."):
        if input_type == "keywords":
            return process_keywords_input(user_input, search_params, blog_params, selected_content_type)
        
        elif input_type == "youtube_url" or input_type == "audio_file":
            return process_youtube_or_audio(user_input)
        
        elif input_type == "web_url":
            return process_web_url(user_input)
        
        elif input_type == "image_file":
            return process_image_input(user_input, uploaded_file)
        
        elif input_type == "PDF_file":
            return process_pdf_input(uploaded_file)
        
        else:
            st.error(f"Unsupported input type: {input_type}")
            return False 