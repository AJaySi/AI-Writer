"""AI-powered blog rewriter tool."""

import streamlit as st
from bs4 import BeautifulSoup
import requests
from transformers import pipeline
import time
from exa_py import Exa

# Load the LLM
generator = pipeline('text-generation', model='gpt-3')  # Example, adjust based on your model

def main():
    st.markdown("<h1 style='text-align: center; color: #1565C0;'>AI Blog Content Refresher</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Keep your blog fresh and engaging with AI!</h3>", unsafe_allow_html=True)

    # User Inputs
    with st.form("content_refresh_form"):
        url = st.text_input("Enter Blog Post URL", placeholder="https://www.example.com/blog-post")
        keywords = st.text_area("Enter Relevant Keywords", placeholder="Example: 'SEO best practices', 'digital marketing tips'")
        tone = st.selectbox("Choose Desired Tone", ["Formal", "Informal", "Engaging", "Informative"])
        target_audience = st.text_input("Target Audience", placeholder="e.g., tech enthusiasts, business owners")
        desired_length = st.slider("Desired Content Length (words)", min_value=300, max_value=1500, value=600, step=100)

        submitted = st.form_submit_button("Refresh Content")

    if submitted:
        st.markdown("<h2 style='text-align: center; color: #1565C0;'>Content Refresh for: <span style='color: blue;'>"+url+"</span></h2>", unsafe_allow_html=True)
        st.info(f"Refreshing your blog post...")

        # Fetch the existing content
        website_data = collect_website_data(url)

        # Get additional context from web research (using Metaphor API)
        web_research_context = get_web_research_context(keywords)

        # Generate the updated content
        updated_content = generate_updated_content(
            website_data, keywords, tone, target_audience, desired_length, web_research_context
        )

        # Display Results
        st.subheader("Updated Blog Content")
        st.write(updated_content)

def collect_website_data(url):
    # ... (Your web scraping function remains the same)

def get_web_research_context(keywords):
    """Fetches web research context using Metaphor API."""
    METAPHOR_API_KEY = os.getenv('METAPHOR_API_KEY')
    if not METAPHOR_API_KEY:
        st.error("METAPHOR_API_KEY environment variable not set!")
        return None

    metaphor = Exa(METAPHOR_API_KEY)
    try:
        search_response = metaphor.search_and_contents(
            keywords,
            use_autoprompt=True,
            num_results=5
        )
        return search_response.results
    except Exception as err:
        st.error(f"Error fetching web research context: {err}")
        return None

def generate_updated_content(website_data, keywords, tone, target_audience, desired_length, web_research_context):
    prompt = f"""
    You are an expert blog content writer. 
    Analyze the following existing blog post content:

    ```
    {website_data['content']}
    ```

    Here is some additional context from web research:

    ```
    {web_research_context}
    ```

    Generate an updated version of this content, keeping the core message but making it more engaging and relevant for a {target_audience} audience. 

    Consider the following:

    * Use the provided keywords: {keywords}
    * Adopt a {tone} writing style.
    * Keep the content around {desired_length} words.
    * Make sure the content is fresh, up-to-date, and provides value to the reader.
    * Incorporate insights from the web research context to make the content more comprehensive and insightful.

    Format your response as Markdown.
    """

    response = generator(prompt, max_length=2000, num_return_sequences=1, do_sample=True)
    return response[0]['generated_text']

if __name__ == "__main__":
    main()
