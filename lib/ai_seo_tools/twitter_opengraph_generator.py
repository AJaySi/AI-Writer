import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests
import os

from ..ai_web_researcher.firecrawl_web_crawler import scrape_url
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


# Placeholder function for web scraping the URL (to be replaced with your mechanism)
def scrape_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title
        title = soup.find('title').text.strip() if soup.find('title') else None

        # Extract the description 
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None

        # Extract the image URL
        image_url = soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else None

        return title, description, image_url

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while scraping the webpage: {e}")
        return None, None, None 

# Function to generate OpenGraph meta tags
def generate_opengraph_meta_tags(url, html_content=None, title=None, description=None, image_url=None):
    ai_prompt = f"""
    Generate OpenGraph meta tags for a Twitter Card for the following webpage: {url}

    Here is the HTML content of the page: 
    ```html
    {html_content}
    ```

    Optional Customizations:
    * Title: {title if title else "Infer from the page content"}
    * Description: {description if description else "Infer from the page content"}
    * Image URL: {image_url if image_url else "Infer from the page content"}

    Best practices:
    - Title: Should be concise and informative.
    - Description: Provide a brief summary of the content.
    - Image URL: Use a high-quality image.
    - URL: Ensure the URL is correct.
    - Type: Specify the content type (e.g., article, website).
    - Site Name: Provide the name of the site.

    Output the generated OpenGraph meta tags as a series of HTML meta tags in the following format:

    <meta property="og:title" content="Extracted or provided title" />
    <meta property="og:description" content="Extracted or provided description" />
    <meta property="og:image" content="Extracted or provided image URL" />
    <meta property="og:url" content="{url}" />
    <meta property="og:type" content="Infer from the URL" />
    <meta property="og:site_name" content="Extract site name from the URL" />
    """
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=ai_prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()

# Function to display the Streamlit UI
def display_ui():
    st.title('OpenGraph Meta Tags Generator for Twitter 🐦')
    st.write('Generate OpenGraph meta tags for Twitter cards with ease. Just provide a URL and let our tool do the rest!')

    # User inputs
    url = st.text_input('Content URL', help="🔗 Paste the URL of the page you want to share on Twitter.", placeholder="e.g., https://example.com")
    title = st.text_input('Title (optional)', help="📝 Optionally, provide a custom title for your Twitter card.", placeholder="e.g., Amazing Blog Post")
    description = st.text_area('Description (optional)', help="✍️ Optionally, provide a custom description for your Twitter card.", placeholder="e.g., This blog post covers...")
    image_url = st.text_input('Image URL (optional)', help="📸 Optionally, provide a URL to an image for your Twitter card.", placeholder="e.g., https://example.com/image.jpg")

    if st.button('Generate Meta Tags'):
        if url:
            # Scrape the webpage for missing information if not provided
            if not title or not description or not image_url:
                scraped_title, scraped_description, scraped_image_url = scrape_webpage(url)
                title = title or scraped_title
                description = description or scraped_description
                image_url = image_url or scraped_image_url
            
            # Fetch HTML content
            html_content = requests.get(url).text

            # Generate OpenGraph meta tags
            meta_tags = generate_opengraph_meta_tags(url, html_content=html_content, title=title, description=description, image_url=image_url)
            
            st.subheader('Generated OpenGraph Meta Tags')
            st.code(meta_tags, language='html')
        else:
            st.error('Please provide a content URL.')

    # Instructions and preview
    st.write('### Instructions')
    st.write('1. Enter the URL of the content you want to share on Twitter.')
    st.write('2. Optionally, provide a custom title, description, and image URL.')
    st.write('3. Click "Generate Meta Tags" to see the generated OpenGraph meta tags.')

    st.write('### Preview')
    st.write('A preview of how the Twitter card will look with the generated meta tags will be shown here (Feature to be implemented).')

# Run the Streamlit UI
if __name__ == '__main__':
    display_ui()
