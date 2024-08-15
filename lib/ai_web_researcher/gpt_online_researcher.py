################################################################
# 
# ## Features
#
# - **Web Research**: Alwrity enables users to conduct web research efficiently. 
# By providing keywords or topics of interest, users can initiate searches across multiple platforms simultaneously.
#
# - **Google SERP Search**: The tool integrates with Google Search Engine Results Pages (SERP) 
# to retrieve relevant information based on user queries. It offers insights into organic search results, 
# People Also Ask, and related searches.
#
# - **Tavily AI Integration**: Alwrity leverages Tavily AI's capabilities to enhance web research. 
# It utilizes advanced algorithms to search for information and extract relevant data from various sources.
#
# - **Metaphor AI Semantic Search**: Alwrity employs Metaphor AI's semantic search technology to find related articles and content. 
# By analyzing context and meaning, it delivers precise and accurate results.
#
# - **Google Trends Analysis**: The tool provides Google Trends analysis for user-defined keywords. 
# It helps users understand the popularity and trends associated with specific topics over time.
# 
##############################################################

import os
import json
from pathlib import Path
import sys
from datetime import datetime

from .tavily_ai_search import get_tavilyai_results
from .metaphor_basic_neural_web_search import metaphor_find_similar, metaphor_search_articles
from .google_serp_search import google_search
from .google_trends_researcher import do_google_trends_analysis

from loguru import logger
# Configure logger
logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )



def gpt_web_researcher(search_keywords):
    """ Keyword based web researcher, basic, neural and Semantic search."""
    
    try:
        google_search_result = do_google_serp_search(search_keywords)
        tavily_search_result = do_tavily_ai_search(search_keywords)
        metaphor_search_result = do_metaphor_ai_research(search_keywords)
        gtrends_search_result = do_google_pytrends_analysis(search_keywords)
        # get_rag_results(search_query)
        print(f"\n\nReview the analysis in this file at: {os.environ.get('SEARCH_SAVE_FILE')}\n")
    except Exception as err:
        logger.error(f"Failed in gpt_web_researcher: {err}")


def do_google_serp_search(search_keywords):
    """ COmmon function to do google SERP analysis and return results. """

    # FIXME: Add a return filter to either return full json, titles, PAA, relatedsearches etc.
    try:
        logger.info(f"Doing Google search for: {search_keywords}\n")
        g_results = google_search(search_keywords)
        g_titles = extract_info(g_results, 'titles')
        return(g_results, g_titles)
    except Exception as err:
        logger.error(f"Failed to do Google Serpapi research: {err}")
        # Not failing, as tavily would do same and then GPT-V to search.


def do_tavily_ai_search(search_keywords, max_results=10):
    """ Common function to do Tavily AI web research."""
    try:
        # FIXME: Include the follow-up questions as blog FAQs.
        logger.info(f"Doing Tavily AI search for: {search_keywords}")
        t_results = get_tavilyai_results(search_keywords, max_results)
        t_titles = tavily_extract_information(t_results, 'titles')
        t_answer = tavily_extract_information(t_results, 'answer')
        return(t_results, t_titles, t_answer)
    except Exception as err:
        logger.error(f"Failed to do Tavily AI Search: {err}")


def do_metaphor_ai_research(search_keywords):
    """ """
    try:
        logger.info(f"Start Semantic/Neural web search with Metahpor: {search_keywords}")
        response_articles = metaphor_search_articles(search_keywords)
        m_titles = metaphor_extract_titles_or_text(response_articles, return_titles=True)
        return(response_articles, m_titles)
    except Exception as err:
        logger.error(f"Failed to do Metaphor search: {err}")


def do_google_pytrends_analysis(search_keywords):
    """ """
    try:
        logger.info(f"Do Google Trends analysis for given keywords: {search_keywords}")
        return(do_google_trends_analysis(search_keywords))
    except Exception as err:
        logger.error(f"Failed to do google trends analysis: {err}")


def metaphor_extract_titles_or_text(json_data, return_titles=True):
    """
    Extract either titles or text from the given JSON structure.

    Args:
        json_data (list): List of Result objects in JSON format.
        return_titles (bool): If True, return titles. If False, return text.

    Returns:
        list: List of titles or text.
    """
    if return_titles:
        return [(result.title) for result in json_data]
    else:
        return [result.text for result in json_data]


def extract_info(json_data, info_type):
    """
    Extract information (titles, peopleAlsoAsk, or relatedSearches) from the given JSON.

    Args:
        json_data (dict): The JSON data.
        info_type (str): The type of information to extract (titles, peopleAlsoAsk, relatedSearches).

    Returns:
        list or None: A list containing the requested information, or None if the type is invalid.
    """
    if info_type == "titles":
        return [result.get("title") for result in json_data.get("organic", [])]
    elif info_type == "peopleAlsoAsk":
        return [item.get("question") for item in json_data.get("peopleAlsoAsk", [])]
    elif info_type == "relatedSearches":
        return [item.get("query") for item in json_data.get("relatedSearches", [])]
    else:
        print("Invalid info_type. Please use 'titles', 'peopleAlsoAsk', or 'relatedSearches'.")
        return None


def tavily_extract_information(json_data, keyword):
    """
    Extract information from the given JSON based on the specified keyword.

    Args:
        json_data (dict): The JSON data.
        keyword (str): The keyword (title, content, answer, follow-query).

    Returns:
        list or str: The extracted information based on the keyword.
    """
    if keyword == 'titles':
        return [result['title'] for result in json_data['results']]
    elif keyword == 'content':
        return [result['content'] for result in json_data['results']]
    elif keyword == 'answer':
        return json_data['answer']
    elif keyword == 'follow-query':
        return json_data['follow_up_questions']
    else:
        return f"Invalid keyword: {keyword}"
