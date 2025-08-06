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
import pandas as pd
import random
import numpy as np

from lib.alwrity_ui.display_google_serp_results import (
    process_research_results,
    process_search_results,
    display_research_results
)
from lib.alwrity_ui.google_trends_ui import display_google_trends_data, process_trends_data

from .tavily_ai_search import do_tavily_ai_search
from .metaphor_basic_neural_web_search import metaphor_search_articles, streamlit_display_metaphor_results
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
        # Reset session state variables for this research operation
        if 'metaphor_results_displayed' in st.session_state:
            del st.session_state.metaphor_results_displayed
        
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
                
                # Pass the parameters to do_tavily_ai_search
                t_results = do_tavily_ai_search(
                    search_keywords,  # Pass as positional argument
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
                    # Add debug logging to check the structure of metaphor_results
                    logger.debug(f"Metaphor results structure: {type(metaphor_results)}")
                    if isinstance(metaphor_results, dict):
                        logger.debug(f"Metaphor results keys: {metaphor_results.keys()}")
                        if 'data' in metaphor_results:
                            logger.debug(f"Metaphor data keys: {metaphor_results['data'].keys()}")
                            if 'results' in metaphor_results['data']:
                                logger.debug(f"Number of results: {len(metaphor_results['data']['results'])}")
                    
                    # Display Metaphor results only if not already displayed
                    if 'metaphor_results_displayed' not in st.session_state:
                        st.session_state.metaphor_results_displayed = True
                        # Make sure to pass the correct parameters to streamlit_display_metaphor_results
                        streamlit_display_metaphor_results(metaphor_results, search_keywords)
                
                # Add Google Trends Analysis
                update_progress("Initiating Google Trends analysis...", progress=80)
                try:
                    # Add an informative message about Google Trends
                    with st.expander("ℹ️ About Google Trends Analysis", expanded=False):
                        st.markdown("""
                        **What is Google Trends Analysis?**
                        
                        Google Trends Analysis provides insights into how often a particular search-term is entered relative to the total search-volume across various regions of the world, and in various languages.
                        
                        **What data will be shown?**
                        
                        - **Related Keywords**: Terms that are frequently searched together with your keyword
                        - **Interest Over Time**: How interest in your keyword has changed over the past 12 months
                        - **Regional Interest**: Where in the world your keyword is most popular
                        - **Related Queries**: What people search for before and after searching for your keyword
                        - **Related Topics**: Topics that are closely related to your keyword
                        
                        **How to use this data:**
                        
                        - Identify trending topics in your industry
                        - Understand seasonal patterns in search behavior
                        - Discover related keywords for content planning
                        - Target content to specific regions with high interest
                        """)
                    
                    trends_results = do_google_pytrends_analysis(search_keywords)
                    if trends_results:
                        update_progress("Google Trends analysis completed successfully", progress=90)
                        # Store trends results in the research_results
                        if metaphor_results:
                            metaphor_results['trends_data'] = trends_results
                        else:
                            # If metaphor_results is None, create a new container for results
                            metaphor_results = {'trends_data': trends_results}
                        
                        # Display Google Trends data using the new UI module
                        display_google_trends_data(trends_results, search_keywords)
                    else:
                        update_progress("Google Trends analysis returned no results", level="warning")
                except Exception as trends_err:
                    logger.error(f"Google Trends analysis failed: {trends_err}")
                    update_progress("Google Trends analysis failed", level="warning")
                    st.error(f"Error in Google Trends analysis: {str(trends_err)}")
                
                # Return the combined results
                update_progress("Research completed!", progress=100, level="success")
                return metaphor_results or t_results
                    
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
        update_progress("Validating search parameters", progress=0.1)
        status_container.info("📝 Validating parameters...")
        
        if not search_keywords or not isinstance(search_keywords, str):
            logger.error(f"Invalid search keywords: {search_keywords}")
            raise ValueError("Search keywords must be a non-empty string")
        
        # Update search initiation
        update_progress(f"Initiating search for: '{search_keywords}'", progress=0.2)
        status_container.info("🌐 Querying search API...")
        logger.info(f"Search params: {kwargs}")
        
        # Execute search
        g_results = google_search(search_keywords)
        
        if g_results:
            # Log success
            update_progress("Search completed successfully", progress=0.8, level="success")
            
            # Update statistics
            stats = f"""Found:
                - {len(g_results.get('organic', []))} organic results
                - {len(g_results.get('peopleAlsoAsk', []))} related questions
                - {len(g_results.get('relatedSearches', []))} related searches"""
            update_progress(stats, progress=0.9)
            
            # Process results
            update_progress("Processing search results", progress=0.95)
            status_container.info("⚡ Processing results...")
            processed_results = process_search_results(g_results)
            
            # Extract titles
            update_progress("Extracting information", progress=0.98)
            g_titles = extract_info(g_results, 'titles')
            
            # Final success
            update_progress("Analysis completed successfully", progress=1.0, level="success")
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
            update_progress("No results found", progress=0.5, level="warning")
            status_container.warning("⚠️ No results found")
            return None
            
    except Exception as err:
        error_msg = f"Search failed: {str(err)}"
        update_progress(error_msg, progress=0.5, level="error")
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
        
        # Import the Tavily search function directly
        from .tavily_ai_search import do_tavily_ai_search as tavily_search
        
        # Call the actual Tavily search function
        t_results = tavily_search(
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


def do_google_pytrends_analysis(keywords):
    """
    Perform Google Trends analysis for the given keywords.
    
    Args:
        keywords (str): The search keywords to analyze
        
    Returns:
        dict: A dictionary containing formatted Google Trends data with the following keys:
            - related_keywords: List of related keywords
            - interest_over_time: DataFrame with date and interest columns
            - regional_interest: DataFrame with country_code, country, and interest columns
            - related_queries: DataFrame with query and value columns
            - related_topics: DataFrame with topic and value columns
    """
    logger.info(f"Performing Google Trends analysis for keywords: {keywords}")
    
    # Create a progress container for Streamlit
    progress_container = st.empty()
    progress_bar = st.progress(0)
    
    def update_progress(message, progress=None, level="info"):
        """Helper function to update progress in Streamlit UI"""
        if progress is not None:
            progress_bar.progress(progress)
        
        if level == "error":
            progress_container.error(f"🚫 {message}")
        elif level == "warning":
            progress_container.warning(f"⚠️ {message}")
        else:
            progress_container.info(f"🔄 {message}")
        logger.debug(f"Progress update [{level}]: {message}")
    
    try:
        # Initialize the formatted data dictionary
        formatted_data = {
            'related_keywords': [],
            'interest_over_time': pd.DataFrame(),
            'regional_interest': pd.DataFrame(),
            'related_queries': pd.DataFrame(),
            'related_topics': pd.DataFrame()
        }
        
        # Get raw trends data from google_trends_researcher
        update_progress("Fetching Google Trends data...", progress=10)
        raw_trends_data = do_google_trends_analysis(keywords)
        
        if not raw_trends_data:
            logger.warning("No Google Trends data returned")
            update_progress("No Google Trends data returned", level="warning", progress=20)
            return formatted_data
        
        # Process related keywords from the raw data
        update_progress("Processing related keywords...", progress=30)
        if isinstance(raw_trends_data, list):
            formatted_data['related_keywords'] = raw_trends_data
        elif isinstance(raw_trends_data, dict):
            if 'keywords' in raw_trends_data:
                formatted_data['related_keywords'] = raw_trends_data['keywords']
            if 'interest_over_time' in raw_trends_data:
                formatted_data['interest_over_time'] = raw_trends_data['interest_over_time']
            if 'regional_interest' in raw_trends_data:
                formatted_data['regional_interest'] = raw_trends_data['regional_interest']
            if 'related_queries' in raw_trends_data:
                formatted_data['related_queries'] = raw_trends_data['related_queries']
            if 'related_topics' in raw_trends_data:
                formatted_data['related_topics'] = raw_trends_data['related_topics']
        
        # If we have keywords but missing other data, try to fetch them using pytrends directly
        if formatted_data['related_keywords'] and (
            formatted_data['interest_over_time'].empty or 
            formatted_data['regional_interest'].empty or 
            formatted_data['related_queries'].empty or 
            formatted_data['related_topics'].empty
        ):
            try:
                update_progress("Fetching additional data from Google Trends API...", progress=40)
                from pytrends.request import TrendReq
                pytrends = TrendReq(hl='en-US', tz=360)
                
                # Build payload with the main keyword
                update_progress("Building search payload...", progress=45)
                pytrends.build_payload([keywords], timeframe='today 12-m', geo='')
                
                # Get interest over time if missing
                if formatted_data['interest_over_time'].empty:
                    try:
                        update_progress("Fetching interest over time data...", progress=50)
                        interest_df = pytrends.interest_over_time()
                        if not interest_df.empty:
                            formatted_data['interest_over_time'] = interest_df.reset_index()
                            update_progress(f"Successfully fetched interest over time data with {len(formatted_data['interest_over_time'])} data points", progress=55)
                        else:
                            update_progress("No interest over time data available", level="warning", progress=55)
                    except Exception as e:
                        logger.error(f"Error fetching interest over time: {e}")
                        update_progress(f"Error fetching interest over time: {str(e)}", level="warning", progress=55)
                
                # Get regional interest if missing
                if formatted_data['regional_interest'].empty:
                    try:
                        update_progress("Fetching regional interest data...", progress=60)
                        regional_df = pytrends.interest_by_region()
                        if not regional_df.empty:
                            formatted_data['regional_interest'] = regional_df.reset_index()
                            update_progress(f"Successfully fetched regional interest data for {len(formatted_data['regional_interest'])} regions", progress=65)
                        else:
                            update_progress("No regional interest data available", level="warning", progress=65)
                    except Exception as e:
                        logger.error(f"Error fetching regional interest: {e}")
                        update_progress(f"Error fetching regional interest: {str(e)}", level="warning", progress=65)
                
                # Get related queries if missing
                if formatted_data['related_queries'].empty:
                    try:
                        update_progress("Fetching related queries data...", progress=70)
                        # Get related queries data
                        related_queries = pytrends.related_queries()
                        
                        # Create empty DataFrame as fallback
                        formatted_data['related_queries'] = pd.DataFrame(columns=['query', 'value'])
                        
                        # Simple direct approach to avoid list index errors
                        if related_queries and isinstance(related_queries, dict):
                            # Check if our keyword exists in the results
                            if keywords in related_queries:
                                keyword_data = related_queries[keywords]
                                
                                # Process top queries if available
                                if 'top' in keyword_data and keyword_data['top'] is not None:
                                    try:
                                        update_progress("Processing top related queries...", progress=75)
                                        # Convert to DataFrame if it's not already
                                        if isinstance(keyword_data['top'], pd.DataFrame):
                                            top_df = keyword_data['top']
                                        else:
                                            # Try to convert to DataFrame
                                            top_df = pd.DataFrame(keyword_data['top'])
                                        
                                        # Ensure it has the right columns
                                        if not top_df.empty:
                                            # Rename columns if needed
                                            if 'query' in top_df.columns:
                                                # Already has the right column name
                                                pass
                                            elif len(top_df.columns) > 0:
                                                # Use first column as query
                                                top_df = top_df.rename(columns={top_df.columns[0]: 'query'})
                                            
                                            # Add to our results
                                            formatted_data['related_queries'] = top_df
                                            update_progress(f"Successfully processed {len(top_df)} top related queries", progress=80)
                                    except Exception as e:
                                        logger.warning(f"Error processing top queries: {e}")
                                        update_progress(f"Error processing top queries: {str(e)}", level="warning", progress=80)
                                
                                # Process rising queries if available
                                if 'rising' in keyword_data and keyword_data['rising'] is not None:
                                    try:
                                        update_progress("Processing rising related queries...", progress=85)
                                        # Convert to DataFrame if it's not already
                                        if isinstance(keyword_data['rising'], pd.DataFrame):
                                            rising_df = keyword_data['rising']
                                        else:
                                            # Try to convert to DataFrame
                                            rising_df = pd.DataFrame(keyword_data['rising'])
                                        
                                        # Ensure it has the right columns
                                        if not rising_df.empty:
                                            # Rename columns if needed
                                            if 'query' in rising_df.columns:
                                                # Already has the right column name
                                                pass
                                            elif len(rising_df.columns) > 0:
                                                # Use first column as query
                                                rising_df = rising_df.rename(columns={rising_df.columns[0]: 'query'})
                                            
                                            # Combine with existing data if we have any
                                            if not formatted_data['related_queries'].empty:
                                                formatted_data['related_queries'] = pd.concat([formatted_data['related_queries'], rising_df])
                                                update_progress(f"Successfully processed {len(rising_df)} rising related queries", progress=90)
                                            else:
                                                formatted_data['related_queries'] = rising_df
                                                update_progress(f"Successfully processed {len(rising_df)} rising related queries", progress=90)
                                    except Exception as e:
                                        logger.warning(f"Error processing rising queries: {e}")
                                        update_progress(f"Error processing rising queries: {str(e)}", level="warning", progress=90)
                    except Exception as e:
                        logger.error(f"Error fetching related queries: {e}")
                        update_progress(f"Error fetching related queries: {str(e)}", level="warning", progress=90)
                        # Ensure we have an empty DataFrame with the right columns
                        formatted_data['related_queries'] = pd.DataFrame(columns=['query', 'value'])
                
                # Get related topics if missing
                if formatted_data['related_topics'].empty:
                    try:
                        update_progress("Fetching related topics data...", progress=95)
                        # Get related topics data
                        related_topics = pytrends.related_topics()
                        
                        # Create empty DataFrame as fallback
                        formatted_data['related_topics'] = pd.DataFrame(columns=['topic', 'value'])
                        
                        # Simple direct approach to avoid list index errors
                        if related_topics and isinstance(related_topics, dict):
                            # Check if our keyword exists in the results
                            if keywords in related_topics:
                                keyword_data = related_topics[keywords]
                                
                                # Process top topics if available
                                if 'top' in keyword_data and keyword_data['top'] is not None:
                                    try:
                                        update_progress("Processing top related topics...", progress=97)
                                        # Convert to DataFrame if it's not already
                                        if isinstance(keyword_data['top'], pd.DataFrame):
                                            top_df = keyword_data['top']
                                        else:
                                            # Try to convert to DataFrame
                                            top_df = pd.DataFrame(keyword_data['top'])
                                        
                                        # Ensure it has the right columns
                                        if not top_df.empty:
                                            # Rename columns if needed
                                            if 'topic_title' in top_df.columns:
                                                top_df = top_df.rename(columns={'topic_title': 'topic'})
                                            elif len(top_df.columns) > 0 and 'topic' not in top_df.columns:
                                                # Use first column as topic
                                                top_df = top_df.rename(columns={top_df.columns[0]: 'topic'})
                                            
                                            # Add to our results
                                            formatted_data['related_topics'] = top_df
                                            update_progress(f"Successfully processed {len(top_df)} top related topics", progress=98)
                                    except Exception as e:
                                        logger.warning(f"Error processing top topics: {e}")
                                        update_progress(f"Error processing top topics: {str(e)}", level="warning", progress=98)
                                
                                # Process rising topics if available
                                if 'rising' in keyword_data and keyword_data['rising'] is not None:
                                    try:
                                        update_progress("Processing rising related topics...", progress=99)
                                        # Convert to DataFrame if it's not already
                                        if isinstance(keyword_data['rising'], pd.DataFrame):
                                            rising_df = keyword_data['rising']
                                        else:
                                            # Try to convert to DataFrame
                                            rising_df = pd.DataFrame(keyword_data['rising'])
                                        
                                        # Ensure it has the right columns
                                        if not rising_df.empty:
                                            # Rename columns if needed
                                            if 'topic_title' in rising_df.columns:
                                                rising_df = rising_df.rename(columns={'topic_title': 'topic'})
                                            elif len(rising_df.columns) > 0 and 'topic' not in rising_df.columns:
                                                # Use first column as topic
                                                rising_df = rising_df.rename(columns={rising_df.columns[0]: 'topic'})
                                            
                                            # Combine with existing data if we have any
                                            if not formatted_data['related_topics'].empty:
                                                formatted_data['related_topics'] = pd.concat([formatted_data['related_topics'], rising_df])
                                                update_progress(f"Successfully processed {len(rising_df)} rising related topics", progress=100)
                                            else:
                                                formatted_data['related_topics'] = rising_df
                                                update_progress(f"Successfully processed {len(rising_df)} rising related topics", progress=100)
                                    except Exception as e:
                                        logger.warning(f"Error processing rising topics: {e}")
                                        update_progress(f"Error processing rising topics: {str(e)}", level="warning", progress=100)
                    except Exception as e:
                        logger.error(f"Error fetching related topics: {e}")
                        update_progress(f"Error fetching related topics: {str(e)}", level="warning", progress=100)
                        # Ensure we have an empty DataFrame with the right columns
                        formatted_data['related_topics'] = pd.DataFrame(columns=['topic', 'value'])
                
            except Exception as e:
                logger.error(f"Error fetching additional trends data: {e}")
                update_progress(f"Error fetching additional trends data: {str(e)}", level="warning", progress=100)
        
        # Ensure all DataFrames have the correct column names for the UI
        update_progress("Finalizing data formatting...", progress=100)
        
        if not formatted_data['interest_over_time'].empty:
            if 'date' not in formatted_data['interest_over_time'].columns:
                formatted_data['interest_over_time'] = formatted_data['interest_over_time'].reset_index()
            if 'interest' not in formatted_data['interest_over_time'].columns and keywords in formatted_data['interest_over_time'].columns:
                formatted_data['interest_over_time'] = formatted_data['interest_over_time'].rename(columns={keywords: 'interest'})
        
        if not formatted_data['regional_interest'].empty:
            if 'country_code' not in formatted_data['regional_interest'].columns and 'geoName' in formatted_data['regional_interest'].columns:
                formatted_data['regional_interest'] = formatted_data['regional_interest'].rename(columns={'geoName': 'country_code'})
            if 'interest' not in formatted_data['regional_interest'].columns and keywords in formatted_data['regional_interest'].columns:
                formatted_data['regional_interest'] = formatted_data['regional_interest'].rename(columns={keywords: 'interest'})
        
        if not formatted_data['related_queries'].empty:
            # Handle different column names that might be present in the related queries DataFrame
            if 'query' not in formatted_data['related_queries'].columns:
                if 'Top query' in formatted_data['related_queries'].columns:
                    formatted_data['related_queries'] = formatted_data['related_queries'].rename(columns={'Top query': 'query'})
                elif 'Rising query' in formatted_data['related_queries'].columns:
                    formatted_data['related_queries'] = formatted_data['related_queries'].rename(columns={'Rising query': 'query'})
                elif 'query' not in formatted_data['related_queries'].columns and len(formatted_data['related_queries'].columns) > 0:
                    # If we have a DataFrame but no 'query' column, use the first column as 'query'
                    first_col = formatted_data['related_queries'].columns[0]
                    formatted_data['related_queries'] = formatted_data['related_queries'].rename(columns={first_col: 'query'})
            
            if 'value' not in formatted_data['related_queries'].columns and len(formatted_data['related_queries'].columns) > 1:
                # If we have a second column, use it as 'value'
                second_col = formatted_data['related_queries'].columns[1]
                formatted_data['related_queries'] = formatted_data['related_queries'].rename(columns={second_col: 'value'})
            elif 'value' not in formatted_data['related_queries'].columns:
                # If no 'value' column exists, add one with default values
                formatted_data['related_queries']['value'] = 0
        
        if not formatted_data['related_topics'].empty:
            # Handle different column names that might be present in the related topics DataFrame
            if 'topic' not in formatted_data['related_topics'].columns:
                if 'topic_title' in formatted_data['related_topics'].columns:
                    formatted_data['related_topics'] = formatted_data['related_topics'].rename(columns={'topic_title': 'topic'})
                elif 'topic' not in formatted_data['related_topics'].columns and len(formatted_data['related_topics'].columns) > 0:
                    # If we have a DataFrame but no 'topic' column, use the first column as 'topic'
                    first_col = formatted_data['related_topics'].columns[0]
                    formatted_data['related_topics'] = formatted_data['related_topics'].rename(columns={first_col: 'topic'})
            
            if 'value' not in formatted_data['related_topics'].columns and len(formatted_data['related_topics'].columns) > 1:
                # If we have a second column, use it as 'value'
                second_col = formatted_data['related_topics'].columns[1]
                formatted_data['related_topics'] = formatted_data['related_topics'].rename(columns={second_col: 'value'})
            elif 'value' not in formatted_data['related_topics'].columns:
                # If no 'value' column exists, add one with default values
                formatted_data['related_topics']['value'] = 0
        
        # Clear the progress container after completion
        progress_container.empty()
        progress_bar.empty()
        
        return formatted_data
        
    except Exception as e:
        logger.error(f"Error in Google Trends analysis: {e}")
        update_progress(f"Error in Google Trends analysis: {str(e)}", level="error", progress=100)
        # Clear the progress container after error
        progress_container.empty()
        progress_bar.empty()
        return {
            'related_keywords': [],
            'interest_over_time': pd.DataFrame(),
            'regional_interest': pd.DataFrame(),
            'related_queries': pd.DataFrame(),
            'related_topics': pd.DataFrame()
        }


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