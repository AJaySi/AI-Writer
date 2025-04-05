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
        raise ValueError("METAPHOR_API_KEY environment variable not set!")
    return Exa(METAPHOR_API_KEY)


def metaphor_rag_search():
    """ Mainly used for researching blog sections. """
    metaphor = get_metaphor_client()



def metaphor_find_similar(similar_url):
    """
    Find similar content using the Metaphor API.

    Args:
        url (str): The URL to find similar content.

    Returns:
        MetaphorResponse: The response from the Metaphor API.
    """
    metaphor = get_metaphor_client()
    try:
        logger.info(f"Doing similar web search for url: {similar_url}")
        search_response = metaphor.find_similar_and_contents(
            similar_url,
            highlights=True,
            num_results=10)
    except Exception as e:
        logger.error(f"Metaphor: Error in finding similar content: {e}")
        raise

    competitors = search_response.results
    # Initialize lists to store titles and URLs
    titles = []
    urls = []

    # Initialize lists to store titles, URLs, and contents
    titles = []
    urls = []
    contents = []
    
    # Extract titles, URLs, and contents from the competitors
    for c in competitors:
        titles.append(c.title)
        urls.append(c.url)
        # Simulate web content fetching and summarization (replace with actual logic)
        all_contents = ""
        try:
            search_response = metaphor.search_and_contents(
                c.url,
                type="keyword",
                num_results=1
            )
            research_response = search_response.results
            for r in research_response:
                all_contents += r.text
            c.text = summarize_competitor_content(all_contents)  # Replace with actual summarization function
        except Exception as err:
            c.text = f"Failed to summarize content: {err}"
        contents.append(c.text)
    
    # Create a DataFrame from the titles, URLs, and contents
    df = pd.DataFrame({
        "Title": titles,
        "URL": urls,
        "Content Summary": contents
    })
    # Display the DataFrame as a table
    if not df.empty:
        st.write("### Competitor Analysis Results")
        st.table(df)
 
    print_search_result(competitors)
    return search_response


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
        
        # Display results in Streamlit
        streamlit_display_metaphor_results(formatted_response)
        return formatted_response

    except Exception as e:
        logger.error(f"Error in Exa searching articles: {e}")
        return None

def streamlit_display_metaphor_results(metaphor_response: dict):
    """
    Display Metaphor search results in Streamlit with enhanced metrics and popovers
    
    Args:
        metaphor_response (dict): Response from Metaphor search
    """
    if not metaphor_response or 'data' not in metaphor_response:
        st.error("No valid Metaphor search results to display")
        return

    # Initialize session state variables if they don't exist
    if 'search_insights' not in st.session_state:
        st.session_state.search_insights = None
    
    if 'metaphor_response' not in st.session_state:
        st.session_state.metaphor_response = metaphor_response
    
    if 'insights_generated' not in st.session_state:
        st.session_state.insights_generated = False
    
    # Update the stored metaphor_response with the latest data
    st.session_state.metaphor_response = metaphor_response

    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    # Calculate metrics
    results = metaphor_response['data']['results']
    total_results = len(results)
    avg_score = sum(r['score'] for r in results if r['score']) / total_results if total_results > 0 else 0
    
    with col1:
        st.metric(
            label="Total Results",
            value=total_results
        )
    with col2:
        if metaphor_response['data'].get('costDollars'):
            cost = metaphor_response['data']['costDollars']
            st.metric(
                label="Search Cost",
                value=f"${cost['total']:.3f}"
            )
    with col3:
        st.metric(
            label="Average Relevance Score",
            value=f"{avg_score:.2f}"
        )

    # Display AI-generated answers side by side
    if 'answer' in metaphor_response or 'tavily_answer' in metaphor_response:
        st.markdown("### 🤖 AI-Generated Research Answers")
        
        # Create two columns for side-by-side display
        tavily_col, metaphor_col = st.columns(2)
        
        # Display Tavily answer if available
        with tavily_col:
            if 'tavily_answer' in metaphor_response:
                st.markdown("#### 🔍 Tavily AI Answer")
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B;">
                    {metaphor_response['tavily_answer']}
                </div>
                """, unsafe_allow_html=True)
                
                if metaphor_response.get('tavily_cost_dollars'):
                    st.caption(f"Tavily Answer Cost: ${metaphor_response['tavily_cost_dollars']['total']:.3f}")
                
                if metaphor_response.get('tavily_citations'):
                    with st.expander("📚 Tavily Sources"):
                        for idx, citation in enumerate(metaphor_response['tavily_citations'], 1):
                            st.markdown(f"**Source {idx}:** [{citation.get('title', 'Untitled')}]({citation.get('url')})")
            else:
                st.markdown("#### 🔍 Tavily AI Answer")
                st.info("No Tavily answer available for this query.")
        
        # Display Metaphor answer if available
        with metaphor_col:
            if 'answer' in metaphor_response:
                st.markdown("#### 🔍 Metaphor AI Answer")
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;">
                    {metaphor_response['answer']}
                </div>
                """, unsafe_allow_html=True)
                
                if metaphor_response.get('answerCostDollars'):
                    st.caption(f"Metaphor Answer Cost: ${metaphor_response['answerCostDollars']['total']:.3f}")
                
                if metaphor_response.get('citations'):
                    with st.expander("📚 Metaphor Sources"):
                        for idx, citation in enumerate(metaphor_response['citations'], 1):
                            st.markdown(f"**Source {idx}:** [{citation.get('title', 'Untitled')}]({citation.get('url')})")
            else:
                st.markdown("#### 🔍 Metaphor AI Answer")
                st.info("No Metaphor answer available for this query.")
    
    # Add "Get Search Insights" button - moved outside the AI answers conditional
    st.markdown("### 🔍 Search Insights")
    
    # Create a container for the insights
    insights_container = st.container()
    
    # Use a button with a callback function
    if st.button("Generate Search Insights", type="primary"):
        # Set a flag in session state to indicate that insights should be generated
        st.session_state.insights_generated = True
        
        # Store the current metaphor_response in session state
        st.session_state.metaphor_response = metaphor_response
        
        # Redirect to the same page with a query parameter to trigger insights generation
        st.experimental_rerun()
    
    # If insights should be generated, do it in a separate container
    if st.session_state.insights_generated:
        with insights_container:
            with st.spinner("Analyzing search results to generate insights..."):
                # Get the stored metaphor_response from session state
                stored_response = st.session_state.metaphor_response
                stored_results = stored_response['data']['results']
                
                # Prepare data for analysis
                analysis_data = {
                    "metaphor_results": stored_results,
                    "metaphor_answer": stored_response.get("answer", ""),
                    "tavily_answer": stored_response.get("tavily_answer", ""),
                    "metaphor_citations": stored_response.get("citations", []),
                    "tavily_citations": stored_response.get("tavily_citations", [])
                }
                
                # Create the analysis prompt
                analysis_prompt = f"""
                **Search Intent & User Needs Analysis**
                
                I have conducted research using both Tavily and Metaphor AI search engines. 
                Below is the data from both sources:
                
                **Metaphor AI Answer:**
                {analysis_data["metaphor_answer"]}
                
                **Tavily AI Answer:**
                {analysis_data["tavily_answer"]}
                
                **Search Results:**
                {[f"{i+1}. {r['title']} - {r['summary']}" for i, r in enumerate(analysis_data["metaphor_results"])]}
                
                **Citations:**
                {[f"{i+1}. {c.get('title', 'Untitled')} - {c.get('url', 'No URL')}" for i, c in enumerate(analysis_data["metaphor_citations"] + analysis_data["tavily_citations"])]}
                
                Based on this research data, please provide the following insights:
                
                **Search Intent & User Needs**
                ```
                Review the research data and identify:
                1. The distribution of search intent (categorize as Informational/Commercial/Navigational/Transactional)
                2. Most common user questions and their patterns
                3. Frequently mentioned pain points or challenges
                4. Recurring solutions or approaches to addressing these challenges
                5. Gaps between user questions and available answers
                
                Present findings in a structured format with percentages and specific examples.
                ```
                
                Format your response as a comprehensive analysis with clear sections, bullet points, and examples from the research data.
                """
                
                try:
                    # Import the llm_text_gen function
                    import importlib
                    text_gen_module = importlib.import_module('lib.gpt_providers.text_generation.main_text_generation')
                    if hasattr(text_gen_module, 'llm_text_gen'):
                        # Generate insights using llm_text_gen
                        insights = text_gen_module.llm_text_gen(analysis_prompt)
                        
                        # Store insights in session state
                        st.session_state.search_insights = insights
                        
                        # Reset the flag to prevent regeneration on next rerun
                        st.session_state.insights_generated = False
                    else:
                        st.error("Could not find llm_text_gen function in the text generation module.")
                except Exception as e:
                    st.error(f"Error generating insights: {str(e)}")
                    logger.error(f"Error generating insights: {e}")
    
    # Display insights if they exist in session state
    if st.session_state.search_insights:
        with insights_container:
            st.markdown("### 🔍 Search Intent & User Needs Analysis")
            st.markdown(st.session_state.search_insights)

    # Create DataFrame from results
    df = pd.DataFrame(results)
    
    # Prepare data for display
    display_df = df.copy()
    display_df['Visit Site'] = display_df['url']
    
    # Format publishedDate as string if it exists
    if 'publishedDate' in display_df.columns:
        display_df['publishedDate'] = display_df['publishedDate'].apply(
            lambda x: x[:10] if isinstance(x, str) else 'N/A'
        )

    # Configure columns for data editor
    columns = {
        'title': st.column_config.TextColumn(
            'Title',
            width='large',
            required=True,
        ),
        'author': st.column_config.TextColumn(
            'Author',
            width='medium',
        ),
        'publishedDate': st.column_config.TextColumn(
            'Published Date',
            width='medium',
        ),
        'score': st.column_config.NumberColumn(
            'Relevance Score',
            width='small',
            format="%.2f"
        ),
        'Visit Site': st.column_config.LinkColumn(
            'Link',
            width='small',
            display_text='Visit Site',
        ),
        'summary': st.column_config.TextColumn(
            'Summary',
            width='large',
            required=True,
        )
    }

    # Display results in data editor
    st.data_editor(
        display_df,
        column_config=columns,
        hide_index=True,
        num_rows='dynamic',
        disabled=True,
        column_order=['title', 'author', 'publishedDate', 'score', 'summary', 'Visit Site']
    )

    # Display detailed summaries with popovers
    st.write("### Detailed Summaries")
    for idx, result in enumerate(results, 1):
        with st.expander(f"📄 {result['title']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Summary**")
                st.markdown(result['summary'])
            with col2:
                st.markdown("**Details**")
                st.markdown(f"**Author:** {result['author'] if result['author'] else 'N/A'}")
                st.markdown(f"**Published:** {result['publishedDate'][:10] if result['publishedDate'] else 'N/A'}")
                st.markdown(f"**Score:** {result['score']:.2f}")
                st.markdown(f"[Visit Site]({result['url']})")

    # Display search metadata
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"Search Type: {metaphor_response['data']['resolvedSearchType']}")
    with col2:
        st.caption(f"Request ID: {metaphor_response['data']['requestId']}")


def metaphor_news_summarizer(news_keywords):
    """ build a LLM-based news summarizer app with the Exa API to keep us up-to-date 
    with the latest news on a given topic.
    """
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
