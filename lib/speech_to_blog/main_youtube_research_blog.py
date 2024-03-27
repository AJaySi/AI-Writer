import json
import os
import sys
from loguru import logger

# Import from local packages
from .gpt_providers.openai_chat_completion import openai_chatgpt
from .gpt_providers.gpt_vision_img_details import analyze_and_extract_details_from_image
from .generate_image_from_prompt import generate_image
from .write_blogs_from_youtube_videos import youtube_to_blog
from .wordpress_blog_uploader import compress_image, upload_blog_post, upload_media
from .gpt_online_researcher import do_online_research
from .save_blog_to_file import save_blog_to_file
from .optimize_images_for_upload import optimize_image
from .combine_research_and_blog import blog_with_research
from .get_blog_meta_desc import generate_blog_description
from .get_blog_title import generate_blog_title
from .get_tags import get_blog_tags
from .get_blog_category import get_blog_categories
from .convert_content_to_markdown import convert_tomarkdown_format
from .convert_markdown_to_html import convert_markdown_to_html
from .utils.youtube_keyword_research import research_yt

# Configuring the logger
logger.remove()
logger.add(sys.stdout, colorize=True, format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

# Constants for directory paths
IMAGE_DIR = os.path.join(os.getcwd(), "blog_images")
OUTPUT_PATH = os.path.join(os.getcwd(), "blogs")


def generate_youtube_research_blog(yt_keywords):
    """
    Research YouTube based on given keywords and get top video URLs.
    """
    for ayt_keyword in yt_keywords:
        yt_research_response = ''
        data = {}
        logger.info(f"Researching YouTube top videos for: {yt_keywords}")
        try:
            yt_research_response = research_yt(ayt_keyword)
            if not yt_research_response:
                yt_research_response = research_yt(ayt_keyword)
        except Exception as err:
            logger.error(f"Failed to do YouTube Research: {err}")

        if not yt_research_response.strip():
            logger.warning("Error: JSON data is empty.")
            yt_research_response = research_yt(ayt_keyword)
        else:
            try:
                aggregated_data = load_response_json(yt_research_response, ayt_keyword)
            except Exception as err:
                logger.error(f"Failed to load json response: {err}")
                sys.exit(1)

            for title, a_yt_url, views, references, quickstart_code in zip(
                    aggregated_data["titles"], aggregated_data["urls"], aggregated_data["views"],
                    aggregated_data["references"], aggregated_data["quickstart_codes"]):
                blog_markdown_str = ""
                if a_yt_url != "No URL Provided":
                    # Transcribe the audio using whisper model.
                    try:
                        logger.info(f"Starting to write blog on URL: {a_yt_url}")
                        blog_markdown_str, yt_title = youtube_to_blog(a_yt_url)
                        logger.warning("\n\n--------------- First Draft of the Blog: --------\n\n")
                        logger.info(f"{blog_markdown_str}\n")
                        logger.warning("--------------------END of First draft----------\n\n")
                        if not yt_title or not blog_markdown_str:
                            logger.error("No content or title for audio to proceed.")
                            sys.exit(1)
                    except Exception as e:
                        logger.error(f"Error in youtube_to_blog: {e}")
                        sys.exit(1)
                sys.exit(1)

                if title != "Unknown Title":
                    print(f"Title: {title}")
                if url != "No URL Provided":
                    print(f"URL: {url}")
                if views != "No View Count":
                    print(f"Views: {views}")
                if references:  # Checks if references list is not empty
                    print(f"References: {', '.join(references)}")
                if quickstart_code != "Code coming soon":
                    print(f"Quickstart Code: {quickstart_code}")
                print()  # Adds a newline for separation between entries



def load_response_json(yt_research_response, yt_keyword):
    """
    Load and parse the YouTube research response JSON.
    """
    try:
        logger.info(f"Loading the JSON data for parsing: {yt_research_response}")
        data = json.loads(yt_research_response.replace('`', '').strip())

        if isinstance(data, dict):
            results_key = next((key for key in data if key.lower().startswith("result")), None)
            if results_key:
                research_yt_dict = process_results(data[results_key])
        elif isinstance(data, list):
            research_yt_dict = process_results(data)

    except json.JSONDecodeError as e:
        logger.error(f"load_response_json: Failed to parse JSON data: {e}")
        generate_youtube_research_blog([yt_keyword])

    return research_yt_dict


def process_results(results):
    """
    Process the results from the YouTube research JSON and return the aggregated data.
    
    Args:
        results (list): List of dictionaries containing YouTube video details.

    Returns:
        dict: A dictionary containing lists of titles, URLs, views, references, and quickstart codes.

    Raises:
        Exception: If an error occurs during the processing of individual entries.
    """
    titles = []
    urls = []
    views_list = []
    references_list = []
    quickstart_codes = []

    for entry in results:
        try:
            titles.append(entry.get("Title", "Unknown Title"))
            urls.append(entry.get("URL", "No URL Provided"))
            views_list.append(entry.get("Views", "No View Count"))
            references_list.append(entry.get("References", []))
            quickstart_codes.append(entry.get("Quickstart_Code", "Code coming soon"))
        except Exception as e:
            logger.error(f"Error processing yt resulr entry: {e}")
            continue

    return {
        "titles": titles,
        "urls": urls,
        "views": views_list,
        "references": references_list,
        "quickstart_codes": quickstart_codes
    }
