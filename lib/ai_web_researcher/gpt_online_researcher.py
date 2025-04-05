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
import time
from pathlib import Path
import sys
from datetime import datetime
import streamlit as st

from lib.alwrity_ui.display_google_serp_results import (
    process_research_results,
    process_search_results,
    display_research_results
)

from .tavily_ai_search import get_tavilyai_results
from .metaphor_basic_neural_web_search import metaphor_search_articles
from .google_serp_search import google_search
from .google_trends_researcher import do_google_trends_analysis
#from .google_gemini_web_researcher import do_gemini_web_research

from loguru import logger
# Configure logger
logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )


def gpt_web_researcher(search_keywords, search_mode, **kwargs):
    """Keyword based web researcher with progress tracking."""
    
    logger.info(f"Starting web research - Keywords: {search_keywords}, Mode: {search_mode}")
    logger.debug(f"Additional parameters: {kwargs}")
    
    try:
        # Initialize result container
        research_results = None
        
        # Create status containers
        status_container = st.empty()
        progress_bar = st.progress(0)
        
        def update_progress(message, progress=None, level="info"):
            if progress is not None:
                progress_bar.progress(progress)
            if level == "error":
                status_container.error(f"🚫 {message}")
            elif level == "warning":
                status_container.warning(f"⚠️ {message}")
            else:
                status_container.info(f"🔄 {message}")
            logger.debug(f"Progress update [{level}]: {message}")

        if search_mode == "google":
            logger.info("Starting Google research pipeline")
            
            try:
                # First try Google SERP
                update_progress("Initiating SERP search...", progress=10)
                serp_results = do_google_serp_search(search_keywords, **kwargs)
                
                if serp_results and serp_results.get('organic'):
                    logger.info("SERP search successful")
                    update_progress("SERP search completed", progress=40)
                    research_results = serp_results
                else:
                    logger.warning("SERP search returned no results, falling back to Gemini")
                    update_progress("No SERP results, trying Gemini...", progress=45)
                    
                    # Keep it commented. Fallback to Gemini
                    #try:
                    #    gemini_results = do_gemini_web_research(search_keywords)
                    #    if gemini_results:
                    #        logger.info("Gemini research successful")
                    #        update_progress("Gemini research completed", progress=80)
                    #        research_results = {
                    #            'source': 'gemini',
                    #            'results': gemini_results
                    #        }
                    #except Exception as gemini_err:
                    #    logger.error(f"Gemini research failed: {gemini_err}")
                    #    update_progress("Gemini research failed", level="warning")
                
                if research_results:
                    update_progress("Processing final results...", progress=90)
                    processed_results = process_research_results(research_results)
                    
                    if processed_results:
                        update_progress("Research completed!", progress=100, level="success")
                        display_research_results(processed_results)
                        return processed_results
                    else:
                        error_msg = "Failed to process research results"
                        logger.warning(error_msg)
                        update_progress(error_msg, level="warning")
                        return None
                else:
                    error_msg = "No results from either SERP or Gemini"
                    logger.warning(error_msg)
                    update_progress(error_msg, level="warning")
                    return None
                    
            except Exception as search_err:
                error_msg = f"Research pipeline failed: {str(search_err)}"
                logger.error(error_msg, exc_info=True)
                update_progress(error_msg, level="error")
                raise

        elif search_mode == "ai":
            logger.info("Starting AI research pipeline")
            
            try:
                # Do Tavily AI Search
                update_progress("Initiating Tavily AI search...", progress=10)
                
                # Extract relevant parameters for Tavily search
                include_domains = kwargs.pop('include_domains', None)
                search_depth = kwargs.pop('search_depth', 'advanced')
                
                # Pass the parameters to get_tavilyai_results
                t_results = get_tavilyai_results(
                    keywords=search_keywords, 
                    max_results=kwargs.get('num_results', 10),
                    include_domains=include_domains,
                    search_depth=search_depth,
                    **kwargs
                )
                
                # Do Metaphor AI Search
                update_progress("Initiating Metaphor AI search...", progress=50)
                metaphor_results, metaphor_titles = do_metaphor_ai_research(search_keywords)
                
                if metaphor_results is None:
                    update_progress("Metaphor AI search failed, continuing with Tavily results only...", level="warning")
                else:
                    update_progress("Metaphor AI search completed successfully", progress=75)
                    
            except Exception as ai_err:
                error_msg = f"AI research pipeline failed: {str(ai_err)}"
                logger.error(error_msg, exc_info=True)
                update_progress(error_msg, level="error")
                raise
                
        else:
            error_msg = f"Unsupported search mode: {search_mode}"
            logger.error(error_msg)
            update_progress(error_msg, level="error")
            raise ValueError(error_msg)
            
    except Exception as err:
        error_msg = f"Failed in gpt_web_researcher: {str(err)}"
        logger.error(error_msg, exc_info=True)
        if 'update_progress' in locals():
            update_progress(error_msg, level="error")
        raise


def do_google_serp_search(search_keywords, status_container, update_progress, **kwargs):
    """Perform Google SERP analysis with sidebar progress tracking."""
    
    logger.info("="*50)
    logger.info("Starting Google SERP Search")
    logger.info("="*50)
    
    try:
        # Validate parameters
        update_progress("Validating search parameters")
        status_container.info("📝 Validating parameters...")
        
        if not search_keywords or not isinstance(search_keywords, str):
            logger.error(f"Invalid search keywords: {search_keywords}")
            raise ValueError("Search keywords must be a non-empty string")
        
        # Update search initiation
        update_progress(f"Initiating search for: '{search_keywords}'")
        status_container.info("🌐 Querying search API...")
        logger.info(f"Search params: {kwargs}")
        
        # Execute search
        g_results = google_search(search_keywords)
        
        if g_results:
            # Log success
            update_progress("Search completed successfully", "success")
            
            # Update statistics
            stats = f"""Found:
                - {len(g_results.get('organic', []))} organic results
                - {len(g_results.get('peopleAlsoAsk', []))} related questions
                - {len(g_results.get('relatedSearches', []))} related searches"""
            update_progress(stats)
            
            # Process results
            update_progress("Processing search results")
            status_container.info("⚡ Processing results...")
            processed_results = process_search_results(g_results)
            
            # Extract titles
            update_progress("Extracting information")
            g_titles = extract_info(g_results, 'titles')
            
            # Final success
            update_progress("Analysis completed successfully", "success")
            status_container.success("✨ Research completed!")
            
            # Clear main status after delay
            time.sleep(1)
            status_container.empty()
            
            return {
                'results': g_results,
                'titles': g_titles,
                'summary': processed_results,
                'stats': {
                    'organic_count': len(g_results.get('organic', [])),
                    'questions_count': len(g_results.get('peopleAlsoAsk', [])),
                    'related_count': len(g_results.get('relatedSearches', []))
                }
            }
            
        else:
            update_progress("No results found", "warning")
            status_container.warning("⚠️ No results found")
            return None
            
    except Exception as err:
        error_msg = f"Search failed: {str(err)}"
        update_progress(error_msg, "error")
        logger.error(error_msg)
        logger.debug("Stack trace:", exc_info=True)
        raise
        
    finally:
        logger.info("="*50)
        logger.info("Google SERP Search function completed")
        logger.info("="*50)


def do_tavily_ai_search(search_keywords, max_results=10, **kwargs):
    """ Common function to do Tavily AI web research."""
    try:
        logger.info(f"Doing Tavily AI search for: {search_keywords}")
        
        # Prepare Tavily search parameters
        tavily_params = {
            'max_results': max_results,
            'search_depth': 'advanced' if kwargs.get('search_depth', 3) > 2 else 'basic',
            'time_range': kwargs.get('time_range', 'year'),
            'include_domains': kwargs.get('include_domains', [""]) if kwargs.get('include_domains') else [""]
        }
        
        # Pass the parameters to get_tavilyai_results
        t_results = get_tavilyai_results(
            keywords=search_keywords,
            **tavily_params
        )
        
        if t_results:
            t_titles = tavily_extract_information(t_results, 'titles')
            t_answer = tavily_extract_information(t_results, 'answer')
            return(t_results, t_titles, t_answer)
        else:
            logger.warning("No results returned from Tavily AI search")
            return None, None, None
    except Exception as err:
        logger.error(f"Failed to do Tavily AI Search: {err}")
        return None, None, None


def do_metaphor_ai_research(search_keywords):
    """
    Perform Metaphor AI research and return results with titles.
    
    Args:
        search_keywords (str): Keywords to search for
        
    Returns:
        tuple: (response_articles, titles) or (None, None) if search fails
    """
    try:
        logger.info(f"Start Semantic/Neural web search with Metaphor: {search_keywords}")
        response_articles = metaphor_search_articles(search_keywords)
        
        if response_articles and 'data' in response_articles:
            m_titles = [result.get('title', '') for result in response_articles['data'].get('results', [])]
            return response_articles, m_titles
        else:
            logger.warning("No valid results from Metaphor search")
            return None, None
            
    except Exception as err:
        logger.error(f"Failed to do Metaphor search: {err}")
        return None, None


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