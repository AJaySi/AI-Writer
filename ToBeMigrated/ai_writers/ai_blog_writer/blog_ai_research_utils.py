import sys
import os
import streamlit as st
from loguru import logger
from dotenv import load_dotenv
from pathlib import Path
import time

# Load environment variables
load_dotenv(Path('../../../.env'))

# Import necessary modules
from ...ai_web_researcher.gpt_online_researcher import (
    do_google_serp_search as gpt_do_google_serp_search, 
    do_tavily_ai_search as gpt_do_tavily_ai_search
)
from ...ai_web_researcher.tavily_ai_search import do_tavily_ai_search as tavily_direct_search


def initialize_parameters(search_params=None, blog_params=None):
    """
    Initialize and validate search and blog parameters with defaults.
    
    Args:
        search_params (dict, optional): Search parameters
        blog_params (dict, optional): Blog parameters
        
    Returns:
        tuple: (search_params, blog_params) with defaults applied
    """
    # Initialize search params if not provided
    if search_params is None:
        search_params = {}
    
    # Initialize blog params if not provided
    if blog_params is None:
        blog_params = {}
    
    # Provide default values only for missing keys
    # This ensures we don't override values that were intentionally set to 0 or other falsy values
    if "max_results" not in search_params:
        search_params["max_results"] = 10
    if "search_depth" not in search_params:
        search_params["search_depth"] = "basic"
    if "time_range" not in search_params:
        search_params["time_range"] = "year"
    if "include_domains" not in search_params:
        search_params["include_domains"] = []
    
    # Provide default values only for missing blog parameter keys
    if "blog_length" not in blog_params:
        blog_params["blog_length"] = 2000
    if "blog_tone" not in blog_params:
        blog_params["blog_tone"] = "Professional"
    if "blog_demographic" not in blog_params:
        blog_params["blog_demographic"] = "Professional"
    if "blog_type" not in blog_params:
        blog_params["blog_type"] = "Informational"
    if "blog_language" not in blog_params:
        blog_params["blog_language"] = "English"
    if "blog_output_format" not in blog_params:
        blog_params["blog_output_format"] = "markdown"
    
    # Log the parameters for debugging
    logger.info(f"Using search parameters: {search_params}")
    logger.info(f"Using blog parameters: {blog_params}")
    
    return search_params, blog_params


def perform_google_search(search_keywords, search_params, status, status_container, progress_bar):
    """
    Perform Google SERP search for the given keywords.
    
    Args:
        search_keywords (str): Keywords to search for
        search_params (dict): Search parameters
        status: Streamlit status object
        status_container: Streamlit container for status messages
        progress_bar: Streamlit progress bar
        
    Returns:
        tuple: (google_search_result, g_titles, success_flag)
    """
    def update_progress(message, progress=None, level="info"):
        """Helper function to update progress in Streamlit UI"""
        if progress is not None:
            progress_bar.progress(progress)
        
        if level == "error":
            status_container.error(f"🚫 {message}")
        elif level == "warning":
            status_container.warning(f"⚠️ {message}")
        elif level == "success":
            status_container.success(f"✅ {message}")
        else:
            status_container.info(f"🔄 {message}")
        logger.debug(f"Progress update [{level}]: {message}")
        
    try:
        # Update the function call to include the required parameters and search_params
        status.update(label=f"Starting Google SERP search for: {search_keywords}")
        
        # Add search params to the Google SERP search
        google_search_params = {
            "max_results": search_params.get("max_results", 10)
        }
        
        # Include domains if provided
        if search_params.get("include_domains"):
            google_search_params["include_domains"] = search_params.get("include_domains")
        
        google_search_result = do_google_serp_search(
            search_keywords, 
            status_container=status_container,
            update_progress=update_progress,
            **google_search_params
        )
        
        if google_search_result and google_search_result.get('titles') and len(google_search_result.get('titles', [])) > 0:
            status.update(label=f"✅ Finished with Google web for Search: {search_keywords}")
            g_titles = google_search_result.get('titles', [])
            return google_search_result, g_titles, True
        else:
            # Check if there's an error message in the result
            if google_search_result and 'summary' in google_search_result and 'Error' in google_search_result['summary']:
                error_msg = google_search_result['summary']
                status.update(label=f"❌ Google search failed: {error_msg}", state="error")
                st.error(f"Google SERP search failed: {error_msg}")
            else:
                status.update(label="❌ Failed to get Google SERP results. No valid data returned.", state="error")
                st.error("Google SERP search failed to return valid results.")
            return google_search_result, [], False
    except Exception as err:
        status.update(label=f"❌ Google search error: {str(err)}", state="error")
        st.error(f"Google web research failed: {err}")
        logger.error(f"Failed in Google web research: {err}")
        return None, [], False


def perform_tavily_search(search_keywords, search_params, status):
    """
    Perform Tavily AI search for the given keywords.
    
    Args:
        search_keywords (str): Keywords to search for
        search_params (dict): Search parameters
        status: Streamlit status object
        
    Returns:
        tuple: (tavily_search_result, success_flag)
    """
    try:
        status.update(label=f"🔍 Starting Tavily AI research: {search_keywords}")
        
        # Pass the search parameters to Tavily
        tavily_result_tuple = do_tavily_ai_search(
            search_keywords,
            max_results=search_params.get("max_results", 10),
            search_depth=search_params.get("search_depth", "basic"),
            include_domains=search_params.get("include_domains", []),
            time_range=search_params.get("time_range", "year")
        )
        
        if tavily_result_tuple and len(tavily_result_tuple) == 3:
            tavily_search_result, t_titles, t_answer = tavily_result_tuple
            # If we have either titles or an answer, consider it a success
            if (t_titles and len(t_titles) > 0) or (t_answer and len(t_answer) > 10):
                status.update(label=f"✅ Finished Tavily AI Search on: {search_keywords}", state="complete")
                return tavily_search_result, True
            else:
                status.update(label="❌ Tavily search returned empty results", state="error")
                st.warning("Tavily search didn't find relevant information.")
                return tavily_search_result, False
        else:
            status.update(label="❌ Tavily search returned incomplete results", state="error")
            st.error("Tavily search failed to return valid results.")
            return None, False
            
    except Exception as err:
        status.update(label=f"❌ Tavily search error: {str(err)}", state="error")
        st.error(f"Failed in Tavily web research: {err}")
        logger.error(f"Failed in Tavily web research: {err}")
        return None, False


def do_google_serp_search(search_keywords, status_container=None, update_progress=None, **kwargs):
    """
    Wrapper function to handle the parameter mismatch with the original function.
    """
    try:
        if status_container is None:
            status_container = st.empty()
        
        if update_progress is None:
            def update_progress(message, progress=None, level="info"):
                if level == "error":
                    status_container.error(message)
                elif level == "warning":
                    status_container.warning(message)
                else:
                    status_container.info(message)
        
        # Create a fixed update_progress function that handles any progress type
        def safe_update_progress(message, progress=None, level="info"):
            try:
                # Handle progress value of different types
                if progress is not None:
                    if isinstance(progress, str):
                        # Try to convert string to float if it represents a number
                        try:
                            progress = float(progress)
                        except ValueError:
                            # If conversion fails, just log the message without updating progress
                            progress = None
                
                # Call the original update_progress with sanitized values
                update_progress(message, progress, level)
            except Exception as err:
                # If there's an error in the progress function, just log to console
                logger.error(f"Error in progress update: {err}")
                # Try one more time with just the message
                try:
                    update_progress(message, None, level)
                except:
                    pass
        
        # Set default search parameters - fix the parameter to use 'max_results' not 'num_results'
        search_params = {
            "max_results": kwargs.get("max_results", 10),
            "include_domains": kwargs.get("include_domains", []),
            "search_depth": kwargs.get("search_depth", "basic")
        }
        
        # Update status to indicate we're checking API keys
        status_container.info("🔑 Checking required API keys...")
        
        # Call the original function with the required parameters
        result = gpt_do_google_serp_search(search_keywords, status_container, safe_update_progress, **search_params)
        return result
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in do_google_serp_search wrapper: {error_msg}")
        
        # Check for common error patterns and display user-friendly messages
        if "SERPER_API_KEY is missing" in error_msg:
            status_container.error("🔑 Google search API key (SERPER_API_KEY) is missing. Please check your environment settings.")
            st.error("Google SERP search failed: API key is missing. Using alternative methods.")
        elif "Progress Value has invalid type" in error_msg:
            # This is an internal error, log it but show a more user-friendly message
            status_container.warning("⚠️ Internal progress tracking error. Continuing with search.")
        else:
            # For unknown errors, show the full error message
            status_container.error(f"🚫 Google search error: {error_msg}")
            st.error(f"Google SERP search failed: {error_msg}")
        
        # Return a minimal result structure to prevent downstream errors
        return {
            'results': {},
            'titles': [],
            'summary': f"Error occurred during search: {error_msg}",
            'stats': {
                'organic_count': 0,
                'questions_count': 0,
                'related_count': 0
            }
        }


def do_tavily_ai_search(keywords, max_results=10, search_depth="basic", include_domains=None, time_range="year"):
    """
    Wrapper function for Tavily search to handle parameter differences.
    
    Args:
        keywords (str): Keywords to search for
        max_results (int): Maximum number of search results to return
        search_depth (str): "basic" or "advanced" search depth
        include_domains (list): List of domains to prioritize in search
        time_range (str): Time range for results ("day", "week", "month", "year", "all")
    """
    status_container = st.empty()
    
    if include_domains is None:
        include_domains = []
    
    try:
        # Show status message
        status_container.info(f"🔍 Preparing Tavily AI search with {search_depth} depth...")
        
        # FIXED: Ensure all parameters have correct types to prevent comparison errors
        tavily_params = {
            'max_results': int(max_results),  # Explicitly convert to int
            'search_depth': str(search_depth),  # Ensure this is a string
            'include_domains': include_domains,
            'time_range': str(time_range)
        }
        
        # Log the parameters for debugging
        logger.info(f"Tavily search parameters: {tavily_params}")
        
        # Check for API key before making the request
        tavily_api_key = os.environ.get("TAVILY_API_KEY")
        if not tavily_api_key:
            status_container.error("🔑 Tavily API key (TAVILY_API_KEY) is missing. Please check your environment settings.")
            st.error("Tavily search failed: API key is missing. Using alternative methods.")
            return None, [], "API key missing"
        
        status_container.info(f"🔍 Searching with Tavily AI using {search_depth} depth for: {keywords}")
        
        # Direct implementation without calling gpt_do_tavily_ai_search to avoid type issues
        try:
            # Call the function directly with correct parameter types
            tavily_raw_results = tavily_direct_search(
                keywords,
                max_results=tavily_params['max_results'],
                search_depth=tavily_params['search_depth'],
                include_domains=tavily_params['include_domains'],
                time_range=tavily_params['time_range']
            )
            
            # Extract the needed information
            if isinstance(tavily_raw_results, tuple) and len(tavily_raw_results) == 3:
                # If already in the right format, use it directly
                return tavily_raw_results
                
            # Process the results to extract titles and answer
            t_results = tavily_raw_results
            t_titles = []
            t_answer = ""
            
            # Extract titles from results if available
            if isinstance(t_results, dict):
                if 'results' in t_results and isinstance(t_results['results'], list):
                    t_titles = [r.get('title', '') for r in t_results['results']]
                    status_container.success(f"✅ Found {len(t_titles)} relevant articles")
                if 'answer' in t_results:
                    t_answer = t_results['answer']
                    status_container.success("✅ Generated a summary answer")
            
            return t_results, t_titles, t_answer
            
        except ImportError:
            # Fall back to the original function if direct import fails
            status_container.warning("⚠️ Using fallback Tavily search method...")
            logger.warning("Using fallback Tavily search method")
            
            # FIXED: Alternative approach - wrap the call in try/except to handle type errors
            try:
                tavily_result = gpt_do_tavily_ai_search(keywords, **tavily_params)
                
                # Format the result to match what the blog writer expects
                if isinstance(tavily_result, tuple) and len(tavily_result) == 3:
                    status_container.success("✅ Tavily search completed successfully")
                    return tavily_result
                
                # If not a tuple with expected values, try to extract what we need
                t_results = tavily_result
                
                # Extract titles and answer if available
                t_titles = []
                t_answer = ""
                
                if isinstance(t_results, dict):
                    if 'results' in t_results and isinstance(t_results['results'], list):
                        t_titles = [r.get('title', '') for r in t_results['results']]
                        status_container.success(f"✅ Found {len(t_titles)} relevant articles")
                    if 'answer' in t_results:
                        t_answer = t_results['answer']
                        status_container.success("✅ Generated a summary answer")
                
                return t_results, t_titles, t_answer
                
            except TypeError as type_err:
                # Handle the specific type error more gracefully
                error_msg = str(type_err)
                logger.error(f"Type error in Tavily search: {error_msg}")
                
                if "'>' not supported" in error_msg:
                    status_container.error("🚫 Tavily search parameter type error. Trying alternative approach...")
                    
                    # Try a simpler approach with minimal parameters
                    try:
                        # Call with only the keyword and fixed max_results
                        tavily_result = gpt_do_tavily_ai_search(keywords, max_results=10)
                        
                        # Minimal processing to extract titles and answer
                        t_results = tavily_result
                        t_titles = []
                        t_answer = ""
                        
                        if isinstance(t_results, dict):
                            if 'results' in t_results and isinstance(t_results['results'], list):
                                t_titles = [r.get('title', '') for r in t_results['results']]
                            if 'answer' in t_results:
                                t_answer = t_results['answer']
                        
                        return t_results, t_titles, t_answer
                    except Exception as inner_err:
                        logger.error(f"Alternative Tavily approach also failed: {inner_err}")
                        raise
                else:
                    # Re-raise other type errors
                    raise
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in do_tavily_ai_search wrapper: {error_msg}")
        
        # Display user-friendly error message
        status_container.error(f"🚫 Tavily search error: {error_msg}")
        st.error(f"Tavily AI search failed: {error_msg}")
        
        # Return empty results to prevent downstream errors
        return None, [], f"Error: {error_msg}"
    
    finally:
        # Clear the status container after a delay
        time.sleep(2)
        status_container.empty() 