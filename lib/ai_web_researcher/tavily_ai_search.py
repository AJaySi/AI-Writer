"""
This Python script uses the Tavily AI service to perform advanced searches based on specified keywords and options. It retrieves Tavily AI search results, pretty-prints them using Rich and Tabulate, and provides additional information such as the answer to the search query and follow-up questions.

Features:
- Utilizes the Tavily AI service for advanced searches.
- Retrieves API keys from the environment variables loaded from a .env file.
- Configures logging with Loguru for informative messages.
- Implements a retry mechanism using Tenacity to handle transient failures during Tavily searches.
- Displays search results, including titles, snippets, and links, in a visually appealing table using Tabulate and Rich.

Usage:
- Ensure the necessary API keys are set in the .env file.
- Run the script to perform a Tavily AI search with specified keywords and options.
- The search results, including titles, snippets, and links, are displayed in a formatted table.
- Additional information, such as the answer to the search query and follow-up questions, is presented in separate tables.

Modifications:
- To modify the script, update the environment variables in the .env file with the required API keys.
- Adjust the search parameters, such as keywords and search depth, in the `do_tavily_ai_search` function as needed.
- Customize logging configurations and table formatting according to preferences.

To-Do (TBD):
- Consider adding further enhancements or customization based on specific use cases.

"""


import os
from pathlib import Path
import sys
from dotenv import load_dotenv
from loguru import logger
from tavily import TavilyClient
from rich import print
from tabulate import tabulate
# Load environment variables from .env file
load_dotenv(Path('../../.env'))
from rich import print
import streamlit as st
# Configure logger
logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )

from .common_utils import save_in_file, cfg_search_param
from tenacity import retry, stop_after_attempt, wait_random_exponential


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def do_tavily_ai_search(keywords, max_results=5, include_domains=None, search_depth="advanced", **kwargs):
    """
    Get Tavily AI search results based on specified keywords and options.
    """
    # Run Tavily search
    logger.info(f"Running Tavily search on: {keywords}")

    # Retrieve API keys
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        raise ValueError("API keys for Tavily is Not set.")

    # Initialize Tavily client
    try:
        client = TavilyClient(api_key=api_key)
    except Exception as err:
        logger.error(f"Failed to create Tavily client. Check TAVILY_API_KEY: {err}")
        raise

    try:
        # Create search parameters exactly matching Tavily's API format
        tavily_search_result = client.search(
            query=keywords,
            search_depth="advanced",
            time_range="year",
            include_answer="advanced",
            include_domains=[""] if not include_domains else include_domains,
            max_results=max_results
        )

        if tavily_search_result:
            print_result_table(tavily_search_result)
            streamlit_display_results(tavily_search_result)
            return tavily_search_result
        return None

    except Exception as err:
        logger.error(f"Failed to do Tavily Research: {err}")
        raise


def streamlit_display_results(output_data):
    """Display Tavily AI search results in Streamlit UI with enhanced visualization."""

    # Display the 'answer' in Streamlit with enhanced styling
    answer = output_data.get("answer", "No answer available")
    st.markdown("### 🤖 AI-Generated Answer")
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;">
        {answer}
    </div>
    """, unsafe_allow_html=True)
    
    # Display follow-up questions if available
    follow_up_questions = output_data.get("follow_up_questions", [])
    if follow_up_questions:
        st.markdown("### ❓ Follow-up Questions")
        for i, question in enumerate(follow_up_questions, 1):
            st.markdown(f"**{i}.** {question}")
    
    # Prepare data for display with dataeditor
    st.markdown("### 📊 Search Results")
    
    # Create a DataFrame for the results
    import pandas as pd
    results_data = []
    
    for item in output_data.get("results", []):
        title = item.get("title", "")
        snippet = item.get("content", "")
        link = item.get("url", "")
        results_data.append({
            "Title": title,
            "Content": snippet,
            "Link": link
        })
    
    if results_data:
        df = pd.DataFrame(results_data)
        
        # Display the data editor
        st.data_editor(
            df,
            column_config={
                "Title": st.column_config.TextColumn(
                    "Title",
                    help="Article title",
                    width="medium",
                ),
                "Content": st.column_config.TextColumn(
                    "Content",
                    help="Click the button below to view full content",
                    width="large",
                ),
                "Link": st.column_config.LinkColumn(
                    "Link",
                    help="Click to visit the website",
                    width="small",
                    display_text="Visit Site"
                ),
            },
            hide_index=True,
            use_container_width=True,
        )

        # Add popovers for full content display
        for item in output_data.get("results", []):
            with st.popover(f"View content: {item.get('title', '')[:50]}..."):
                st.markdown(item.get("content", ""))
    else:
        st.info("No results found for your search query.")


def print_result_table(output_data):
    """ Pretty print the tavily AI search result. """
    # Prepare data for tabulate
    table_data = []
    for item in output_data.get("results"):
        title = item.get("title", "")
        snippet = item.get("content", "")
        link = item.get("url", "")
        table_data.append([title, snippet, link])
    
    # Define table headers
    table_headers = ["Title", "Snippet", "Link"] 
    # Display the table using tabulate
    table = tabulate(table_data, 
            headers=table_headers, 
            tablefmt="fancy_grid", 
            colalign=["left", "left", "left"], 
            maxcolwidths=[30, 60, 30])
    # Print the table
    print(table)

    # Save the combined table to a file
    try:
        save_in_file(table)
    except Exception as save_results_err:
        logger.error(f"Failed to save search results: {save_results_err}")
    
    # Display the 'answer' in a table
    table_headers = [f"The answer to search query: {output_data.get('query')}"]
    table_data = [[output_data.get("answer")]]
    table = tabulate(table_data, 
            headers=table_headers, 
            tablefmt="fancy_grid", 
            maxcolwidths=[80])
    print(table)
    # Save the combined table to a file
    try:
        save_in_file(table)
    except Exception as save_results_err:
        logger.error(f"Failed to save search results: {save_results_err}")
    
    # Display the 'follow_up_questions' in a table
    if output_data.get("follow_up_questions"):
        table_headers = [f"Search Engine follow up questions for query: {output_data.get('query')}"]
        table_data = [[output_data.get("follow_up_questions")]]
        table = tabulate(table_data, 
            headers=table_headers, 
            tablefmt="fancy_grid",
            maxcolwidths=[80])
        print(table)
        try:
            save_in_file(table)
        except Exception as save_results_err:
            logger.error(f"Failed to save search results: {save_results_err}")
