import streamlit as st
import json
from datetime import date
from dotenv import load_dotenv

from ..ai_web_researcher.firecrawl_web_crawler import scrape_url
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen

# Load environment variables
load_dotenv()

# Define a dictionary for schema types
schema_types = {
    "Article": {
        "fields": ["Headline", "Author", "Date Published", "Keywords"],
        "schema_type": "Article",
    },
    "Product": {
        "fields": ["Name", "Description", "Price", "Brand", "Image URL"],
        "schema_type": "Product",
    },
    "Recipe": {
        "fields": ["Name", "Ingredients", "Cooking Time", "Serving Size", "Image URL"],
        "schema_type": "Recipe",
    },
    "Event": {
        "fields": ["Name", "Start Date", "End Date", "Location", "Description"],
        "schema_type": "Event",
    },
    "LocalBusiness": {
        "fields": ["Name", "Address", "Phone Number", "Opening Hours", "Image URL"],
        "schema_type": "LocalBusiness",
    },
    # ... (add more schema types as needed)
}

def generate_json_data(content_type, details, url):
    """Generates structured data (JSON-LD) based on user input."""
    try:
        scraped_text = scrape_url(url)
    except Exception as err:
        st.error(f"Failed to scrape web page from URL: {url} - Error: {err}")
        return

    schema = schema_types.get(content_type)
    if not schema:
        st.error(f"Invalid content type: {content_type}")
        return

    data = {
        "@context": "https://schema.org",
        "@type": schema["schema_type"],
    }
    for field in schema["fields"]:
        value = details.get(field)
        if isinstance(value, date):
            value = value.isoformat()
        data[field] = value if value else "N/A"  # Use placeholder values if input is missing

    if url:
        data['url'] = url

    llm_structured_data = get_llm_structured_data(content_type, data, scraped_text)
    return llm_structured_data

def get_llm_structured_data(content_type, data, scraped_text):
    """Function to get structured data from LLM."""
    prompt = f"""Given the following information:

        HTML Content: <<<HTML>>> {scraped_text} <<<END_HTML>>>
        Content Type: <<<CONTENT_TYPE>>> {content_type} <<<END_CONTENT_TYPE>>>
        Additional Relevant Data: <<<ADDITIONAL_DATA>>> {data} <<<END_ADDITIONAL_DATA>>>

        Create a detailed structured data (JSON-LD) script for SEO purposes. 
        The structured data should help search engines understand the content and features of the webpage, enhancing its visibility and potential for rich snippets in search results.
        
        Detailed Steps:
        Parse the HTML content to extract relevant information like the title, main heading, and body content.
        Use the contentType to determine the structured data type (e.g., Article, Product, Recipe).
        Integrate the additional relevant data (e.g., author, datePublished, keywords) into the structured data.
        Ensure all URLs, images, and other attributes are correctly formatted and included.
        Validate the generated JSON-LD to ensure it meets schema.org standards and is free of errors.

        Expected Output:
        Generate a JSON-LD structured data snippet based on the provided inputs."""

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Failed to get response from LLM: {err}")
        return

def ai_structured_data():
    st.title("📝 Generate Structured Data for SEO 🚀")
    st.markdown("**Make your content more discoverable with rich snippets.**")

    content_type = st.selectbox("**Select Content Type**", list(schema_types.keys()))

    details = {}
    schema_fields = schema_types[content_type]["fields"]
    num_fields = len(schema_fields)

    url = st.text_input("**URL :**", placeholder="Enter the URL of your webpage")
    for i in range(0, num_fields, 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < num_fields:
                field = schema_fields[i + j]
                if "Date" in field:
                    details[field] = cols[j].date_input(field)
                else:
                    details[field] = cols[j].text_input(field, placeholder=f"Enter {field.lower()}")

    if st.button("Generate Structured Data"):
        if not url:
            st.error("URL is required to generate structured data.")
            return

        structured_data = generate_json_data(content_type, details, url)
        if structured_data:
            st.subheader("Generated Structured Data (JSON-LD):")
            st.markdown(structured_data)

            st.download_button(
                label="Download JSON-LD",
                data=structured_data,
                file_name=f"{content_type}_structured_data.json",
                mime="application/json",
            )
