#####################################################
#
# Alwrity, AI Long form writer - Writing_with_Prompt_Chaining
# and generative AI.
#
#####################################################

import os
import re
import time #iwish
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv
from configparser import ConfigParser
import streamlit as st

from pprint import pprint
from textwrap import dedent

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..utils.read_main_config_params import read_return_config_section
from ..ai_web_researcher.gpt_online_researcher import do_metaphor_ai_research
from ..ai_web_researcher.gpt_online_researcher import do_google_serp_search, do_tavily_ai_search
from ..blog_metadata.get_blog_metadata import get_blog_metadata_longform
from ..blog_postprocessing.save_blog_to_file import save_blog_to_file
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def generate_with_retry(prompt, system_prompt=None):
    """
    Generates content from the model with retry handling for errors.

    Parameters:
        prompt (str): The prompt to generate content from.
        system_prompt (str, optional): Custom system prompt to use instead of the default one.

    Returns:
        str: The generated content.
    """
    try:
        # FIXME: Need a progress bar here.
        return llm_text_gen(prompt, system_prompt)
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        st.error(f"Error generating content: {e}")
        return False


def long_form_generator(keywords, search_params=None, blog_params=None):
    """
    Generate a long-form blog post based on the given keywords
    
    Args:
        keywords (str): Topic or keywords for the blog post
        search_params (dict, optional): Search parameters for research
        blog_params (dict, optional): Blog content characteristics
    """
    
    # Initialize default parameters if not provided
    if blog_params is None:
        blog_params = {
            "blog_length": 3000,  # Default longer for long-form content
            "blog_tone": "Professional",
            "blog_demographic": "Professional",
            "blog_type": "Informational",
            "blog_language": "English"
        }
    else:
        # Ensure we have a higher word count for long-form content
        if blog_params.get("blog_length", 0) < 2500:
            blog_params["blog_length"] = max(3000, blog_params.get("blog_length", 0))
    
    # Extract parameters with defaults
    blog_length = blog_params.get("blog_length", 3000)
    blog_tone = blog_params.get("blog_tone", "Professional")
    blog_demographic = blog_params.get("blog_demographic", "Professional")
    blog_type = blog_params.get("blog_type", "Informational")
    blog_language = blog_params.get("blog_language", "English")
    
    st.subheader(f"Long-form {blog_type} Blog ({blog_length}+ words)")
    
    with st.status("Generating comprehensive long-form content...", expanded=True) as status:
        # Step 1: Generate outline
        status.update(label="Creating detailed content outline...")
        
        # Use a customized prompt based on the blog parameters
        outline_prompt = f"""
        As an expert content strategist writing in a {blog_tone} tone for {blog_demographic} audience,
        create a detailed outline for a comprehensive {blog_type} blog post about "{keywords}" 
        that will be approximately {blog_length} words in {blog_language}.
        
        The outline should include:
        1. An engaging headline
        2. 5-7 main sections with descriptive headings
        3. 2-3 subsections under each main section
        4. Key points to cover in each section
        5. Ideas for relevant examples or case studies
        6. Suggestions for data points or statistics to include
        
        Format the outline in markdown with proper headings and bullet points.
        """
        
        try:
            outline = llm_text_gen(outline_prompt)
            st.markdown("### Content Outline")
            st.markdown(outline)
            status.update(label="Outline created successfully ✓")
            
            # Step 2: Research the topic using the search parameters
            status.update(label="Researching topic details...")
            research_results = research_topic(keywords, search_params)
            status.update(label="Research completed ✓")
            
            # Step 3: Generate the full content
            status.update(label=f"Writing {blog_length}+ word {blog_tone} {blog_type} content...")
            
            full_content_prompt = f"""
            You are a professional content writer who specializes in {blog_type} content with a {blog_tone} tone 
            for {blog_demographic} audiences. Write a comprehensive, in-depth blog post in {blog_language} about:
            
            "{keywords}"
            
            Use this outline as your structure:
            {outline}
            
            And incorporate these research findings where relevant:
            {research_results}
            
            The blog post should:
            - Be approximately {blog_length} words
            - Include an engaging introduction and strong conclusion
            - Use appropriate subheadings for all sections in the outline
            - Include examples, data points, and actionable insights
            - Be formatted in markdown with proper headings, bullet points, and emphasis
            - Maintain a {blog_tone} tone throughout
            - Address the needs and interests of a {blog_demographic} audience
            
            Do not include phrases like "according to research" or "based on the outline" in your content.
            """
            
            full_content = llm_text_gen(full_content_prompt)
            status.update(label="Long-form content generated successfully! ✓", state="complete")
            
            # Display the full content
            st.markdown("### Your Complete Long-form Blog Post")
            st.markdown(full_content)
            
            return full_content
            
        except Exception as e:
            status.update(label=f"Error generating long-form content: {str(e)}", state="error")
            st.error(f"Failed to generate long-form content: {str(e)}")
            return None
    
def research_topic(keywords, search_params=None):
    """
    Research a topic using search parameters and return a summary
    
    Args:
        keywords (str): Topic to research
        search_params (dict, optional): Search parameters
        
    Returns:
        str: Research summary
    """
    # Display a placeholder for research results
    placeholder = st.empty()
    placeholder.info("Researching topic... Please wait.")
    
    try:
        from .ai_blog_writer.keywords_to_blog_streamlit import do_tavily_ai_search
        
        # Use provided search params or defaults
        if search_params is None:
            search_params = {
                "max_results": 10, 
                "search_depth": "advanced",
                "time_range": "year"
            }
        
        # Conduct research using Tavily
        tavily_results = do_tavily_ai_search(
            keywords,
            max_results=search_params.get("max_results", 10),
            search_depth=search_params.get("search_depth", "advanced"),
            include_domains=search_params.get("include_domains", []),
            time_range=search_params.get("time_range", "year")
        )
        
        # Extract research data
        research_data = ""
        if tavily_results and len(tavily_results) == 3:
            results, titles, answer = tavily_results
            
            if answer and len(answer) > 50:
                research_data += f"Summary: {answer}\n\n"
            
            if results and 'results' in results and len(results['results']) > 0:
                research_data += "Key Sources:\n"
                for i, result in enumerate(results['results'][:7], 1):
                    title = result.get('title', 'Untitled Source')
                    content_snippet = result.get('content', '')[:300] + "..."
                    research_data += f"{i}. {title}\n{content_snippet}\n\n"
        
        # If research data is empty or too short, provide a generic response
        if not research_data or len(research_data) < 100:
            research_data = f"No specific research data found for '{keywords}'. Please provide more specific information in your content."
        
        placeholder.success("Research completed successfully!")
        return research_data
        
    except Exception as e:
        placeholder.error(f"Research failed: {str(e)}")
        return f"Unable to gather research for '{keywords}'. Please continue with the content based on your knowledge."
    finally:
        # Remove the placeholder after a short delay
        import time
        time.sleep(1)
        placeholder.empty()


def generate_long_form_content(content_keywords):
    """
    Main function to generate long-form content based on the provided keywords.
    
    Parameters:
        content_keywords (str): The main keywords or topic for the long-form content.
        
    Returns:
        str: The generated long-form content.
    """
    return long_form_generator(content_keywords)


# Example usage
if __name__ == "__main__":
    # Example usage of the function
    content_keywords = "artificial intelligence in healthcare"
    generated_content = generate_long_form_content(content_keywords)
    print(f"Generated content: {generated_content[:100]}...")
