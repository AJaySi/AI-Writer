""" Package for writing getting-started and how to guides. """

import os
import sys
import datetime
import json

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from .scrape_github_readme import get_gh_details_vision, get_readme_content
from .scrape_github_readme import research_github_topics, check_if_already_written
from .github_getting_started import github_readme_blog
from .gpt_online_researcher import do_online_research
from .faqs_generator_blog import generate_blog_faq
from .get_blog_metadata import blog_metadata
from .save_blog_to_file import save_blog_to_file
from .arxiv_schlorly_research import read_written_ids, extract_arxiv_ids_from_line, append_id_to_file



def blog_from_github(github_opts, flag):
    """ Module for writing getting started code examples from github. """
    if 'url' in flag:
        try:
            write_from_url(github_opts)
        except Exception as err:
            logger.error(f"Failed to write from github url: {github_opts}")
            sys.exit(1)
    elif 'csv' in flag:
        try:
            gh_urls = []
            with open(github_opts, 'r') as file:
                # Read each line in the file
                for gh_url in file:
                    gh_urls.append(gh_url.strip())
        except FileNotFoundError:
            logger.error(f"CSV File not found: {file_path}")
        except Exception as e:
            logger.error(f"CSV: An error occurred: {str(e)}")

        for gh_url in gh_urls:
            try:
                write_from_url(gh_url.strip())
            except Exception as err:
                logger.error(f"Failed to write blog from github: {err}")



def write_from_url(gh_url):
    # String to store the blog content.
    howto_blog = ''
    # The url was not found in already_written data.
    if not check_if_already_written(gh_url):
        logger.info(f"Writing getting started from url: {gh_url}")
    else:
        logger.error(f"Skipping, already written on url: {gh_url}")
        return

    # Direct link to the raw content of README file
    # fixme: Remove the hardcoding, need add another option OR in config ?
    image_dir = os.path.join(os.getcwd(), "blog_images")
    generated_image_name = f"screenshot_image_{datetime.datetime.now():%Y-%m-%d-%H-%M-%S}.png"
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    try:
        logger.info(f"Getting github repo details from vision model: {generated_image_filepath}")
        gh_json = get_gh_details_vision(gh_url, generated_image_filepath)
    except Exception as err:
        logger.error(f"Failed to get gemini vision details from GH repo image: {err}")
        sys.exit(1)
    howto_blog = "```" + f"\nGithub URL:{gh_url}\nStars:{gh_json.get('stars')}\n"
    howto_blog += f"Forks:{gh_json.get('forks')}\n"
    howto_blog += f"Description:{gh_json.get('about')}\nBranch:{gh_json.get('branch_name')}\n" + "```\n\n"

    raw_readme_url_base = "https://raw.githubusercontent.com/" + "/".join(gh_url.split("/")[-2:])
    if gh_json.get('branch_name'):
        raw_readme_url = raw_readme_url_base + f"/{gh_json.get('branch_name')}/" + "README.md"
    else:
        raw_readme_url = raw_readme_url_base + f"/main/" + "README.md"
    logger.info(f"Using this url to fetch the README file: {raw_readme_url}")

    try:
        # Get and print the main content
        readme_content = get_readme_content(raw_readme_url)
    except Exception as err:
        logger.error(f"Failed to get README from URL: {raw_readme_url}: {err}")
    # If the readme is still None, try with master branch.
    if not readme_content:
        raw_readme_url = raw_readme_url_base + f"/master/" + "README.md"
        logger.warning(f"Trying with master branch: {raw_readme_url}")
        readme_content = get_readme_content(raw_readme_url)
        if not readme_content:
            logger.error(f"Still failed to get the README: {readme_content}")
            sys.exit(1)
    
    # Create a getting-started blog, adapted from the GH url README.
    howto_blog += github_readme_blog(readme_content, "gemini")

    # Do online research for faqs on the github url.
    try:
        # Repo names are misnomers for others search, include its decription too.
        # Which, skews the result favourably towards its home/paid pages.
        #online_query = f"{''.join(gh_url.split('/')[-1:])} " + gh_json.get('about')
        online_query = f"{''.join(gh_url.split('/')[-1:])} "
        logger.info("Do web research with Tavily & Metaphor AI.")
        research_report = do_online_research(online_query, "gemini", gh_url)
    except Exception as err:
        logger.error(f"failed to do online research: {err}")

    # Generate FAQs from the online research report.
    try:
        blog_faqs = generate_blog_faq(research_report, "gemini")
        howto_blog += f"\n\n## {''.join(gh_url.split('/')[-1:])} FAQs\n\n" + blog_faqs
    except Exception as err:
        logger.error(f"Failed to generate FAQs from web research_report: {err}")

    logger.info(f"\n\nFinal Blog Content: {howto_blog}\n\n")

    try:
        blog_title, blog_meta_desc, blog_tags, blog_categories = blog_metadata(howto_blog, "gemini")
    except Exception as err:
        logger.error(f"Failed to get blog metadata: {err}")
        raise err

    try:
        save_blog_to_file(howto_blog, blog_title, blog_meta_desc, blog_tags,\
            blog_categories, generated_image_filepath)
    except Exception as err:
        logger.error(f"Failed to save blog to a file: {err}")
        sys.exit(1)

    try:
        append_id_to_file(gh_url, "papers_already_written_on.txt")
    except Exception as err:
        logger.error(f"Failed to write/append ID to papers_already_written_on.txt: {err}")
        raise err
