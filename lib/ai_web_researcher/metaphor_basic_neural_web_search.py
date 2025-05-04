import os
import sys
import pandas as pd
from io import StringIO
from pathlib import Path

from metaphor_python import Metaphor
from datetime import datetime, timedelta

import streamlit as st 
from loguru import logger
from tqdm import tqdm
from tabulate import tabulate
from collections import namedtuple
import textwrap
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from dotenv import load_dotenv
load_dotenv(Path('../../.env'))

from exa_py import Exa

from tenacity import (retry, stop_after_attempt, wait_random_exponential,)# for exponential backoff
from .gpt_summarize_web_content import summarize_web_content
from .gpt_competitor_analysis import summarize_competitor_content
from .common_utils import save_in_file, cfg_search_param


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_metaphor_client():
    """
    Get the Metaphor client.

    Returns:
        Metaphor: An instance of the Metaphor client.
    """
    METAPHOR_API_KEY = os.environ.get('METAPHOR_API_KEY')
    if not METAPHOR_API_KEY:
        logger.error("METAPHOR_API_KEY environment variable not set!")
        st.error("METAPHOR_API_KEY environment variable not set!")
        raise ValueError("METAPHOR_API_KEY environment variable not set!")
    return Exa(METAPHOR_API_KEY)


def metaphor_rag_search():
    """ Mainly used for researching blog sections. """
    metaphor = get_metaphor_client()
    query = "blog research"  # Example query, this can be parameterized as needed
    results = metaphor.search(query)
    if not results:
        logger.error("No results found for the query.")
        st.error("No results found for the query.")
        return None
    
    # Process the results (this is a placeholder, actual processing logic will depend on requirements)
    processed_results = [result['title'] for result in results]
    
    # Display the results
    st.write("Search Results:")
    st.write(processed_results)
    
    return processed_results

def metaphor_find_similar(similar_url, usecase, num_results=5, start_published_date=None, end_published_date=None,
                         include_domains=None, exclude_domains=None, include_text=None, exclude_text=None,
                         summary_query=None, progress_bar=None):
    """Find similar content using Metaphor API."""
    
    try:
        # Initialize progress if not provided
        if progress_bar is None:
            progress_bar = st.progress(0.0)
        
        # Update progress
        progress_bar.progress(0.1, text="Initializing search...")
        
        # Get Metaphor client
        metaphor = get_metaphor_client()
        logger.info(f"Initialized Metaphor client for URL: {similar_url}")
        
        # Prepare search parameters
        search_params = {
            "highlights": True,
            "num_results": num_results,
        }
        
        # Add optional parameters if provided
        if start_published_date:
            search_params["start_published_date"] = start_published_date
        if end_published_date:
            search_params["end_published_date"] = end_published_date
        if include_domains:
            search_params["include_domains"] = include_domains
        if exclude_domains:
            search_params["exclude_domains"] = exclude_domains
        if include_text:
            search_params["include_text"] = include_text
        if exclude_text:
            search_params["exclude_text"] = exclude_text
            
        # Add summary query
        if summary_query:
            search_params["summary"] = summary_query
        else:
            search_params["summary"] = {"query": f"Find {usecase} similar to the given URL."}
        
        logger.debug(f"Search parameters: {search_params}")
        
        # Update progress
        progress_bar.progress(0.2, text="Preparing search parameters...")
        
        # Make API call
        logger.info("Calling Metaphor API find_similar_and_contents...")
        search_response = metaphor.find_similar_and_contents(
            similar_url,
            **search_params
        )
        
        if search_response and hasattr(search_response, 'results'):
            competitors = search_response.results
            total_results = len(competitors)
            
            # Update progress
            progress_bar.progress(0.3, text=f"Found {total_results} results...")
            
            # Process results
            processed_results = []
            for i, result in enumerate(competitors):
                # Calculate progress as decimal (0.0-1.0)
                progress = 0.3 + (0.6 * (i / total_results))
                progress_text = f"Processing result {i+1}/{total_results}..."
                progress_bar.progress(progress, text=progress_text)
                
                # Process each result
                processed_result = {
                    "Title": result.title,
                    "URL": result.url,
                    "Content Summary": result.text if hasattr(result, 'text') else "No content available"
                }
                processed_results.append(processed_result)
            
            # Update progress
            progress_bar.progress(0.9, text="Finalizing results...")
            
            # Create DataFrame
            df = pd.DataFrame(processed_results)
            
            # Update progress
            progress_bar.progress(1.0, text="Analysis completed!")
            
            return df, search_response
            
        else:
            logger.warning("No results found in search response")
            progress_bar.progress(1.0, text="No results found")
            return pd.DataFrame(), search_response
            
    except Exception as e:
        logger.error(f"Error in metaphor_find_similar: {str(e)}", exc_info=True)
        if progress_bar:
            progress_bar.progress(1.0, text="Error occurred during analysis")
        raise


def calculate_date_range(time_range: str) -> tuple:
    """
    Calculate start and end dates based on time range selection.
    
    Args:
        time_range (str): One of 'past_day', 'past_week', 'past_month', 'past_year', 'anytime'
        
    Returns:
        tuple: (start_date, end_date) in ISO format with milliseconds
    """
    now = datetime.utcnow()
    end_date = now.strftime('%Y-%m-%dT%H:%M:%S.999Z')
    
    if time_range == 'past_day':
        start_date = (now - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    elif time_range == 'past_week':
        start_date = (now - timedelta(weeks=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    elif time_range == 'past_month':
        start_date = (now - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    elif time_range == 'past_year':
        start_date = (now - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    else:  # anytime
        start_date = None
        end_date = None
    
    return start_date, end_date

def metaphor_search_articles(query, search_options: dict = None):
    """
    Search for articles using the Metaphor/Exa API.

    Args:
        query (str): The search query.
        search_options (dict): Search configuration options including:
            - num_results (int): Number of results to retrieve
            - use_autoprompt (bool): Whether to use autoprompt
            - include_domains (list): List of domains to include
            - time_range (str): One of 'past_day', 'past_week', 'past_month', 'past_year', 'anytime'
            - exclude_domains (list): List of domains to exclude

    Returns:
        dict: Search results and metadata
    """
    exa = get_metaphor_client()
    try:
        # Initialize default search options
        if search_options is None:
            search_options = {}

        # Get config parameters or use defaults
        try:
            include_domains, _, num_results, _ = cfg_search_param('exa')
        except Exception as cfg_err:
            logger.warning(f"Failed to load config parameters: {cfg_err}. Using defaults.")
            include_domains = None
            num_results = 10

        # Calculate date range based on time_range option
        time_range = search_options.get('time_range', 'anytime')
        start_published_date, end_published_date = calculate_date_range(time_range)

        # Prepare search parameters
        search_params = {
            'num_results': search_options.get('num_results', num_results),
            'summary': True,  # Always get summaries
            'include_domains': search_options.get('include_domains', include_domains),
            'use_autoprompt': search_options.get('use_autoprompt', True),
        }

        # Add date parameters only if they are not None
        if start_published_date:
            search_params['start_published_date'] = start_published_date
        if end_published_date:
            search_params['end_published_date'] = end_published_date

        logger.info(f"Exa web search with params: {search_params} and Query: {query}")
        
        # Execute search
        search_response = exa.search_and_contents(
            query,
            **search_params
        )
            
        if not search_response or not hasattr(search_response, 'results'):
            logger.warning("No results returned from Exa search")
            return None

        # Get cost information safely
        try:
            cost_dollars = {
                'total': float(search_response.cost_dollars['total']),
            } if hasattr(search_response, 'cost_dollars') else None
        except Exception as cost_err:
            logger.warning(f"Error processing cost information: {cost_err}")
            cost_dollars = None

        # Format response to match expected structure
        formatted_response = {
            "data": {
                "requestId": getattr(search_response, 'request_id', None),
                "resolvedSearchType": "neural",
                "results": [
                    {
                        "id": result.url,
                        "title": result.title,
                        "url": result.url,
                        "publishedDate": result.published_date if hasattr(result, 'published_date') else None,
                        "author": getattr(result, 'author', None),
                        "score": getattr(result, 'score', 0),
                        "summary": result.summary if hasattr(result, 'summary') else None,
                        "text": result.text if hasattr(result, 'text') else None,
                        "image": getattr(result, 'image', None),
                        "favicon": getattr(result, 'favicon', None)
                    }
                    for result in search_response.results
                ],
                "costDollars": cost_dollars
            }
        }

        # Get AI-generated answer from Metaphor
        try:
            exa_answer = get_exa_answer(query)
            if exa_answer:
                formatted_response.update(exa_answer)
        except Exception as exa_err:
            logger.warning(f"Error getting Exa answer: {exa_err}")
        
        # Get AI-generated answer from Tavily
        try:
            # Import the function directly from the module
            import importlib
            tavily_module = importlib.import_module('lib.ai_web_researcher.tavily_ai_search')
            if hasattr(tavily_module, 'do_tavily_ai_search'):
                tavily_response = tavily_module.do_tavily_ai_search(query)
                if tavily_response and 'answer' in tavily_response:
                    formatted_response.update({
                        "tavily_answer": tavily_response.get("answer"),
                        "tavily_citations": tavily_response.get("citations", []),
                        "tavily_cost_dollars": tavily_response.get("costDollars", {"total": 0})
                    })
            else:
                logger.warning("do_tavily_ai_search function not found in tavily_ai_search module")
        except Exception as tavily_err:
            logger.warning(f"Error getting Tavily answer: {tavily_err}")
        
        # Return the formatted response without displaying it
        # The display will be handled by gpt_web_researcher
        return formatted_response

    except Exception as e:
        logger.error(f"Error in Exa searching articles: {e}")
        return None

def streamlit_display_metaphor_results(metaphor_response, search_keywords=None):
    """Display Metaphor search results in Streamlit."""
    
    if not metaphor_response:
        st.error("No search results found.")
        return
    
    # Add debug logging
    logger.debug(f"Displaying Metaphor results. Type: {type(metaphor_response)}")
    if isinstance(metaphor_response, dict):
        logger.debug(f"Metaphor response keys: {metaphor_response.keys()}")
    
    # Initialize session state variables if they don't exist
    if 'search_insights' not in st.session_state:
        st.session_state.search_insights = None
    if 'metaphor_response' not in st.session_state:
        st.session_state.metaphor_response = None
    if 'insights_generated' not in st.session_state:
        st.session_state.insights_generated = False
    
    # Store the current response in session state
    st.session_state.metaphor_response = metaphor_response
    
    # Display search results
    st.subheader("🔍 Search Results")
    
    # Calculate metrics - handle different data structures
    results = []
    if isinstance(metaphor_response, dict):
        if 'data' in metaphor_response and 'results' in metaphor_response['data']:
            results = metaphor_response['data']['results']
        elif 'results' in metaphor_response:
            results = metaphor_response['results']
    
    total_results = len(results)
    avg_relevance = sum(r.get('score', 0) for r in results) / total_results if total_results > 0 else 0
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Results", total_results)
    with col2:
        st.metric("Average Relevance Score", f"{avg_relevance:.2f}")
    
    # Display AI-generated answers if available
    if 'tavily_answer' in metaphor_response or 'metaphor_answer' in metaphor_response:
        st.subheader("🤖 AI-Generated Answers")
        
        if 'tavily_answer' in metaphor_response:
            st.markdown("**Tavily AI Answer:**")
            st.write(metaphor_response['tavily_answer'])
        
        if 'metaphor_answer' in metaphor_response:
            st.markdown("**Metaphor AI Answer:**")
            st.write(metaphor_response['metaphor_answer'])
    
    # Get Search Insights button
    if st.button("Generate Search Insights", key="metaphor_generate_insights_button"):
        st.session_state.insights_generated = True
        st.rerun()
    
    # Display insights if they exist in session state
    if st.session_state.search_insights:
        st.subheader("🔍 Search Insights")
        st.write(st.session_state.search_insights)
    
    # Display search results in a data editor
    st.subheader("📊 Detailed Results")
    
    # Prepare data for display
    results_data = []
    for result in results:
        result_data = {
            'Title': result.get('title', ''),
            'URL': result.get('url', ''),
            'Snippet': result.get('summary', ''),
            'Relevance Score': result.get('score', 0),
            'Published Date': result.get('publishedDate', '')
        }
        results_data.append(result_data)
    
    # Create DataFrame
    df = pd.DataFrame(results_data)
    
    # Display the DataFrame if it's not empty
    if not df.empty:
        # Configure columns
        st.dataframe(
            df,
            column_config={
                "Title": st.column_config.TextColumn(
                    "Title",
                    help="Title of the search result",
                    width="large",
                ),
                "URL": st.column_config.LinkColumn(
                    "URL",
                    help="Link to the search result",
                    width="medium",
                    display_text="Visit Article",
                ),
                "Snippet": st.column_config.TextColumn(
                    "Snippet",
                    help="Summary of the search result",
                    width="large",
                ),
                "Relevance Score": st.column_config.NumberColumn(
                    "Relevance Score",
                    help="Relevance score of the search result",
                    format="%.2f",
                    width="small",
                ),
                "Published Date": st.column_config.DateColumn(
                    "Published Date",
                    help="Publication date of the search result",
                    width="medium",
                ),
            },
            hide_index=True,
        )
        
        # Add popover for snippets
        st.markdown("""
        <style>
        .snippet-popover {
            position: relative;
            display: inline-block;
        }
        .snippet-popover .snippet-content {
            visibility: hidden;
            width: 300px;
            background-color: #f9f9f9;
            color: #333;
            text-align: left;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -150px;
            opacity: 0;
            transition: opacity 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .snippet-popover:hover .snippet-content {
            visibility: visible;
            opacity: 1;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display snippets with popover
        st.subheader("📝 Snippets")
        for i, result in enumerate(results):
            snippet = result.get('summary', '')
            if snippet:
                st.markdown(f"""
                <div class="snippet-popover">
                    <strong>{result.get('title', '')}</strong>
                    <div class="snippet-content">
                        {snippet}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No detailed results available.")
    
    # Add a collapsible section for the raw JSON data
    with st.expander("Research Results (JSON)", expanded=False):
        st.json(metaphor_response)


def metaphor_news_summarizer(news_keywords):
    """ build a LLM-based news summarizer app with the Exa API to keep us up-to-date 
    with the latest news on a given topic.
    """
    exa = get_metaphor_client()

    # FIXME: Needs to be user defined.
    one_week_ago = (datetime.now() - timedelta(days=7))
    date_cutoff = one_week_ago.strftime("%Y-%m-%d")

    search_response = exa.search_and_contents(
        news_keywords, use_autoprompt=True, start_published_date=date_cutoff
    )

    urls = [result.url for result in search_response.results]
    print("URLs:")
    for url in urls:
        print(url)


def print_search_result(contents_response):
    # Define the Result namedtuple
    Result = namedtuple("Result", ["url", "title", "text"])
    # Tabulate the data
    table_headers = ["URL", "Title", "Summary"]
    table_data = [(result.url, result.title, result.text) for result in contents_response]

    table = tabulate(table_data,
        headers=table_headers,
        tablefmt="fancy_grid",
        colalign=["left", "left", "left"],
        maxcolwidths=[20, 20, 70])

    # Convert table_data to DataFrame
    import pandas as pd
    df = pd.DataFrame(table_data, columns=["URL", "Title", "Summary"])
    import streamlit as st
    st.table(df)
    print(table)
    # Save the combined table to a file
    try:
        save_in_file(table)
    except Exception as save_results_err:
        logger.error(f"Failed to save search results: {save_results_err}")


def metaphor_scholar_search(query, include_domains=None, time_range="anytime"):
    """
    Search for papers using the Metaphor API.

    Args:
        query (str): The search query.
        include_domains (list): List of domains to include.
        time_range (str): Time range for published articles ("day", "week", "month", "year", "anytime").

    Returns:
        MetaphorResponse: The response from the Metaphor API.
    """
    client = get_metaphor_client()
    try:
        if time_range == "day":
            start_published_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        elif time_range == "week":
            start_published_date = (datetime.utcnow() - timedelta(weeks=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        elif time_range == "month":
            start_published_date = (datetime.utcnow() - timedelta(weeks=4)).strftime('%Y-%m-%dT%H:%M:%SZ')
        elif time_range == "year":
            start_published_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            start_published_date = None

        response = client.search(query, include_domains=include_domains, start_published_date=start_published_date, use_autoprompt=True)
        return response
    except Exception as e:
        logger.error(f"Error in searching papers: {e}")

def get_exa_answer(query: str, system_prompt: str = None) -> dict:
    """
    Get an AI-generated answer for a query using Exa's answer endpoint.
    
    Args:
        query (str): The search query to get an answer for
        system_prompt (str, optional): Custom system prompt for the LLM. If None, uses default prompt.
        
    Returns:
        dict: Response containing answer, citations, and cost information
            {
                "answer": str,
                "citations": list[dict],
                "costDollars": dict
            }
    """
    exa = get_metaphor_client()
    try:
        # Use default system prompt if none provided
        if system_prompt is None:
            system_prompt = (
                "I am doing research to write factual content. "
                "Help me find answers for content generation task. "
                "Provide detailed, well-structured answers with clear citations."
            )

        logger.info(f"Getting Exa answer for query: {query}")
        logger.debug(f"Using system prompt: {system_prompt}")

        # Make API call to get answer with system_prompt parameter
        result = exa.answer(
            query,
            model="exa",
            text=True  # Include full text in citations
        )

        if not result or not result.get('answer'):
            logger.warning("No answer received from Exa")
            return None

        # Format response to match expected structure
        response = {
            "answer": result.get('answer'),
            "citations": result.get('citations', []),
            "costDollars": result.get('costDollars', {"total": 0})
        }

        return response

    except Exception as e:
        logger.error(f"Error getting Exa answer: {e}")
        return None
