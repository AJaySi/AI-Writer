################################################################
#
# 
# 
##############################################################

import os
import json
from pathlib import Path
import sys
from typing import List, NamedTuple
from loguru import logger
from datetime import datetime

from ..gpt_providers.gemini_pro_text import gemini_text_response
from .tavily_ai_search import get_tavilyai_results
from .metaphor_basic_neural_web_search import metaphor_find_similar, metaphor_search_articles
from .google_serp_search import google_search
from .google_trends_researcher import do_google_trends_analysis
from .web_research_report import write_web_research_report

# Configure logger
logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )


def gpt_web_researcher(search_keywords, time_range=None, include_domains=list(), similar_url=None):
    """ """
    print(f"Web Research:Time Range - {time_range},Search Keywords - {search_keywords},Include URLs - {include_domains}")
    # TBD: Keeping the results directory as fixed, for now.
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "workspace", "web_research_reports",                                                 search_keywords.replace(" ", "_") + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    if not include_domains:
        include_domains = list()
    
    google_search_result = do_google_serp_search(search_keywords)
    tavily_search_result = do_tavily_ai_search(search_keywords, include_domains)
    metaphor_search_result = do_metaphor_ai_research(search_keywords, include_domains, time_range, similar_url)
    gtrends_search_result = do_google_pytrends_analysis(search_keywords)
    # get_rag_results(search_query)
    print(f"\n\nReview the analysis in this file at: {os.environ.get('SEARCH_SAVE_FILE')}\n")


def do_google_serp_search(search_keywords):
    """ """
    try:
        logger.info(f"Doing Google search for: {search_keywords}\n")
        g_results = google_search(search_keywords)
        g_titles = extract_info(g_results, 'titles')
        return(g_results, g_titles)
    except Exception as err:
        logger.error(f"Failed to do Google Serpapi research: {err}")
        # Not failing, as tavily would do same and then GPT-V to search.


def do_tavily_ai_search(search_keywords, include_domains=None):
    """ """
    try:
        # FIXME: Include the follow-up questions as blog FAQs.
        logger.info(f"Doing Tavily AI search for: {search_keywords}")
        t_results = get_tavilyai_results(search_keywords, include_domains)
        t_titles = tavily_extract_information(t_results, 'titles')
        return(t_results, t_titles)
    except Exception as err:
        logger.error(f"Failed to do Tavily AI Search: {err}")


def do_metaphor_ai_research(search_keywords,
        include_domains=None,
        time_range=None,
        similar_url=None):
    """ """
    try:
        logger.info(f"Start Semantic/Neural web search with Metahpor: {search_keywords}")
        response_articles = metaphor_search_articles(
                search_keywords,
                include_domains=include_domains,
                time_range=time_range,
                similar_url=similar_url)
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


def compete_organic_results(query, report, organic_results):
    """ Given a blog content and google search organinc results, create a new blog to compete against them."""
    prompt = f""" As an SEO expert and copywriter, I will provide you with my blog content on topic '{query}', and
        Top google search results. 
        Your task is to rewrite the given blog to make it compete against top position results. 
        Make sure, the new blog has high probability of ranking highest against given organic search result competitors.
        Modify the given blog content following best SEO practises.
        Make sure the blog is original, unique and highly readable.
        Remember, Maintain and adopt the formatting, structure, style and tone of the provided blog content.
        Include relevant emojis in your final blog for visual appeal. Use it sparingly.
        Your response should be well-structured, objective, and critically acclaimed blog article based on provided texts. 

        Remember, your goal is to create a detailed blog article that will compete against given organic result competitors.
        Do not provide explanations, suggestions for your response, reply only with your final response.
        Take your time in crafting your content, do not rush to give the response.
        Blog Content: '{report}'\n
        Organic Search result: '{organic_results}'
        """
    report = gemini_text_response(prompt)
    return report
