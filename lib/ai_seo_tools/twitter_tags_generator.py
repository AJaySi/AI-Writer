import streamlit as st
import openai
import os
from bs4 import BeautifulSoup
import requests

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def scrape_url_content(url):
    """
    Scrapes the content from the provided URL.
    
    Args:
        url (str): The URL to scrape content from.

    Returns:
        str: The extracted text content from the webpage.
    """
    # FIXME: Use firecrawl metadata option for this.
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ' '.join([p.text for p in soup.find_all('p')])
        return text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL content: {e}")
        return ""
    except Exception as e:
        st.error(f"Error parsing the HTML content: {e}")
        return ""

def generate_twitter_tags(topic, scraped_content=""):
    """
    Generates a list of relevant Twitter hashtags based on the topic and optional scraped content.

    Args:
        topic (str): The main topic or key phrase.
        scraped_content (str): Optional scraped content to add more context.

    Returns:
        str: A list of Twitter hashtags as a string.
    """
    prompt = f"Generate a list of highly relevant and trending Twitter hashtags based on the topic '{topic}'"
    
    if scraped_content:
        prompt += f" and the following content: {scraped_content[:700]}..."  # Limit content to keep prompt manageable.

    prompt += " Make sure the hashtags are popular and relevant to the topic. Follow Latest best practices for twitter tags."

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Failed to generate Open Graph tags: {err}")
        return None


def display_app():
    """
    Displays the Streamlit app UI and handles user interactions.
    """
    st.title("AI Twitter Tag Generator")

    st.write(
        "Generate trending and highly relevant Twitter tags with minimal input. "
        "Optionally, provide a URL to make the tags even more targeted."
    )

    # User Inputs
    topic = st.text_input(
        "Enter the topic or key phrase for Twitter tags",
        placeholder="e.g., AI in marketing"
    )

    url = st.text_input(
        "Optional: Enter a URL to scrape for more targeted tags",
        placeholder="e.g., https://example.com/article"
    )

    if topic:
        if url:
            with st.spinner("Scraping content from the provided URL..."):
                scraped_content = scrape_url_content(url)
                if not scraped_content:
                    st.info("No content could be extracted from the provided URL.")
        else:
            scraped_content = ""

        if st.button("Generate Twitter Tags"):
            with st.spinner("Generating Twitter tags..."):
                tags = generate_twitter_tags(topic, scraped_content)
                if tags:
                    st.success("Twitter tags generated successfully!")
                    st.write(tags)
    else:
        st.info("Please enter a topic or key phrase to generate Twitter tags.")
