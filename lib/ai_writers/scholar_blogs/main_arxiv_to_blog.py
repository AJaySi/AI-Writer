import sys
import os
import datetime

import tiktoken

from .arxiv_schlorly_research import fetch_arxiv_data, create_dataframe, get_arxiv_main_content
from .arxiv_schlorly_research import arxiv_bibtex, scrape_images_from_arxiv, download_image
from .arxiv_schlorly_research import read_written_ids, extract_arxiv_ids_from_line, append_id_to_file
from .write_research_review_blog import review_research_paper
from .combine_research_and_blog import blog_with_research
from .write_blog_scholar_paper import write_blog_from_paper
from .gpt_providers.gemini_pro_text import gemini_text_response
from .generate_image_from_prompt import generate_image
from .convert_content_to_markdown import convert_tomarkdown_format
from .get_blog_metadata import blog_metadata
from .get_code_examples import gemini_get_code_samples
from .save_blog_to_file import save_blog_to_file
from .take_url_screenshot import screenshot_api

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def blog_arxiv_keyword(query):
    """ Write blog on given arxiv paper."""
    arxiv_id = None
    arxiv_url = None
    bibtex = None
    research_review = None
    column_names = ['Title', 'Date', 'Id', 'Summary', 'PDF URL']
    papers = fetch_arxiv_data(query)
    df = create_dataframe(papers, column_names)

    for paper in papers:
        # Extracting the arxiv_id
        arxiv_id = paper[2].split('/')[-1]
        arxiv_url = "https://browse.arxiv.org/html/" + arxiv_id
        bibtex = arxiv_bibtex(arxiv_id)
        logger.info(f"Get research paper text from the url: {arxiv_url}")
        research_content = get_arxiv_main_content(arxiv_url)
        
        num_tokens = num_tokens_from_string(research_content, "cl100k_base")
        logger.info(f"Number of tokens sent: {num_tokens}")
        # If the number of tokens is below the threshold, process and print the review
        if 1000 < num_tokens < 30000:
            logger.info(f"Writing research review on {paper[0]}")
            research_review = review_research_paper(research_content)
            research_review = f"\n{research_review}\n\n" + f"```{bibtex}```"
            #research_review = research_review + "\n\n\n" + f"{df.to_markdown()}"
            research_review = convert_tomarkdown_format(research_review, "gemini")
            break
        else:
            # Skip to the next iteration if the condition is not met
            continue

    logger.info(f"Final scholar article: \n\n{research_review}\n")
    
    # TBD: Scrape images from research reports and pass to vision to get conclusions out of it.
    #image_urls = scrape_images_from_arxiv(arxiv_url)
    #print("Downloading images found on the page:")
    #for img_url in image_urls:
    #    download_image(img_url, arxiv_url)
    try:
        blog_postprocessing(arxiv_id, research_review)
    except Exception as err:
        logger.error(f"Failed in blog post processing: {err}")
        sys.exit(1)

    logger.info(f"\n\n ################ Finished writing Blog for : #################### \n")


def blog_arxiv_url_list(file_path):
    """ Write blogs on all the arxiv links given in a file. """
    extracted_ids = []
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                arxiv_id = extract_arxiv_ids_from_line(line)
                if arxiv_id:
                    extracted_ids.append(arxiv_id)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError
    except Exception as e:
        logger.error(f"Error while reading the file: {e}")
        raise e

    # Read already written IDs
    written_ids = read_written_ids('papers_already_written_on.txt')

    # Loop through extracted IDs
    for arxiv_id in extracted_ids:
        if arxiv_id not in written_ids:
            # This ID has not been written on yet
            arxiv_url = "https://browse.arxiv.org/html/" + arxiv_id
            logger.info(f"Get research paper text from the url: {arxiv_url}")
            research_content = get_arxiv_main_content(arxiv_url)
            try:
                num_tokens = num_tokens_from_string(research_content, "cl100k_base")
            except Exception as err:
                logger.error(f"Failed in counting tokens: {err}")
                sys.exit(1)
            logger.info(f"Number of tokens sent: {num_tokens}")
            # If the number of tokens is below the threshold, process and print the review
            # FIXME: Docs over 30k tokens, need to be chunked and summarized.
            if 1000 < num_tokens < 30000:
                try:
                    logger.info(f"Getting bibtex for arxiv ID: {arxiv_id}")
                    bibtex = arxiv_bibtex(arxiv_id)
                except Exception as err:
                    logger.error(f"Failed to get Bibtex: {err}")

                try:
                    logger.info(f"Writing a research review..")
                    research_review = review_research_paper(research_content, "gemini")
                    logger.info(f"Research Review: \n{research_review}\n\n")
                except Exception as err:
                    logger.error(f"Failed to write review on research paper: {arxiv_id}{err}")

                research_blog = write_blog_from_paper(research_content, "gemini")
                logger.info(f"\n\nResearch Blog: {research_blog}\n\n")
                research_blog = f"\n{research_review}\n\n" + f"```\n{bibtex}\n```"
                #research_review = blog_with_research(research_review, research_blog, "gemini")
                #logger.info(f"\n\n\nBLOG_WITH_RESEARCh: {research_review}\n\n\n")
                research_review = convert_tomarkdown_format(research_review, "gemini")
                research_review = f"\n{research_review}\n\n" + f"```{bibtex}```"
                logger.info(f"Final blog from research paper: \n\n{research_review}\n\n\n")

                try:
                    blog_postprocessing(arxiv_id, research_review)
                except Exception as err:
                    logger.error(f"Failed in blog post processing: {err}")
                    sys.exit(1)

                logger.info(f"\n\n ################ Finished writing Blog for : #################### \n")
            else:
                # Skip to the next iteration if the condition is not met
                logger.error("FIXME: Docs over 30k tokens, need to be chunked and summarized.")
                continue
        else:
            logger.warning(f"Already written, skip writing on Arxiv paper ID: {arxiv_id}")


def blog_postprocessing(arxiv_id, research_review):
    """ Common function to do blog postprocessing. """
    try:
        append_id_to_file(arxiv_id, "papers_already_written_on.txt")
    except Exception as err:
        logger.error(f"Failed to write/append ID to papers_already_written_on.txt: {err}")
        raise err

    try:
        blog_title, blog_meta_desc, blog_tags, blog_categories = blog_metadata(research_review)
    except Exception as err:
        logger.error(f"Failed to get blog metadata: {err}")
        raise err

    try:
        arxiv_url_scrnsht = f"https://arxiv.org/abs/{arxiv_id}"
        generated_image_filepath = take_paper_screenshot(arxiv_url_scrnsht)
    except Exception as err:
        logger.error(f"Failed to tsk paper screenshot: {err}")
        raise err

    try:
        save_blog_to_file(research_review, blog_title, blog_meta_desc, blog_tags,\
                blog_categories, generated_image_filepath)
    except Exception as err:
        logger.error(f"Failed to save blog to a file: {err}")
        sys.exit(1)


def take_paper_screenshot(arxiv_url):
    """ Common function to take paper screenshot. """
    # fixme: Remove the hardcoding, need add another option OR in config ?
    image_dir = os.path.join(os.getcwd(), "blog_images")
    generated_image_name = f"generated_image_{datetime.datetime.now():%Y-%m-%d-%H-%M-%S}.png"
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    
    if arxiv_url:
        try:
            generated_image_filepath = screenshot_api(arxiv_url, generated_image_filepath)
        except Exception as err:
            logger.error(f"Failed in taking url screenshot: {err}")

    return generated_image_filepath


def num_tokens_from_string(string, encoding_name):
    """Returns the number of tokens in a text string."""
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    except Exception as err:
        logger.error(f"Failed to count tokens: {err}")
        sys.exit(1)
