######################################################
#
# Alwrity, as an AI news writer, will have to be factually correct. 
# We will do multiple rounds of web research and cite our sources. 
# 'include_urls' will focus news articles only from well known sources. 
# Choosing a country will help us get better results.
#
######################################################

import sys
import os
import json
from textwrap import dedent
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(Path('../../.env'))
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen
from ..ai_web_researcher.google_serp_search import perform_serper_news_search


def ai_news_generation(news_keywords, news_country, news_language):
    """ Generate news aritcle based on given keywords. """
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""

    logger.info(f"Researching and Writing News Article on keywords: {news_keywords}")
    # Call on the got-researcher, tavily apis for this. Do google search for organic competition.
    try:
        google_news_result = perform_serper_news_search(news_keywords, news_country, news_language)
        blog_markdown_str = write_news_google_search(news_keywords, news_country, news_language, google_news_result)
        #print(blog_markdown_str)
    except Exception as err:
        logger.error(f"Failed in Google News web research: {err}")
    logger.info("\n######### Draft1: Finished News article from Google web search: ###########\n\n")
    return blog_markdown_str


def write_news_google_search(news_keywords, news_country, news_language, search_results):
    """Combine the given online research and gpt blog content"""
    news_language = get_language_name(news_language)
    news_country = get_country_name(news_country)
    
    prompt = f"""
        As an experienced {news_language} news journalist and editor, 
        I will provide you with my 'News keywords' and its 'google search results'.
        Your goal is to write a News report, backed by given google search results.
        Important, as a news report, its imperative that your content is factually correct and cited.
        
        Follow below guidelines:
        1). Understand and utilize the provided google search result json.
        2). Always provide in-line citations and provide referance links. 
        3). Understand the given news item and adapt your tone accordingly.
        4). Always include the dates when then news was reported.
        6). Do not explain, describe your response.
        7). Your blog should be highly formatted in markdown style and highly readable.
        8). Important: Please read the entire prompt before writing anything. Follow the prompt exactly as I instructed.

        \n\nNews Keywords: "{news_keywords}"\n\n
        Google search Result: "{search_results}"
        """
    logger.info("Generating blog and FAQs from Google web search results.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def get_language_name(language_code):
    languages = {
        "es": "Spanish",
        "vn": "Vietnamese",
        "en": "English",
        "ar": "Arabic",
        "hi": "Hindi",
        "de": "German",
        "zh-cn": "Chinese (Simplified)"
        # Add more language codes and corresponding names as needed
    }
    return languages.get(language_code, "Unknown")

def get_country_name(country_code):
    countries = {
            "es": "Spain",
            "vn": "Vietnam",
            "pk": "Pakistan",
            "in": "India",
            "de": "Germany",
            "cn": "China"
        # Add more country codes and corresponding names as needed
        }
    return countries.get(country_code, "Unknown")
