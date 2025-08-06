import streamlit as st
import requests
from bs4 import BeautifulSoup
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def generate_og_tags(url, title_hint, description_hint, platform="General"):
    """
    Generate Open Graph tags based on the provided URL, title hint, description hint, and platform.

    Args:
        url (str): The URL of the webpage.
        title_hint (str): A hint for the title.
        description_hint (str): A hint for the description.
        platform (str): The platform for which to generate the tags (General, Facebook, or Twitter).

    Returns:
        str: The generated Open Graph tags or an error message.
    """
    # Create a prompt for the text generation model
    prompt = (
        f"Generate Open Graph tags for the following page:\nURL: {url}\n"
        f"Title hint: {title_hint}\nDescription hint: {description_hint}"
    )
    if platform == "Facebook":
        prompt += "\nSpecifically for Facebook"
    elif platform == "Twitter":
        prompt += "\nSpecifically for Twitter"

    try:
        # Generate Open Graph tags using the text generation model
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Failed to generate Open Graph tags: {err}")
        return None


def extract_default_og_tags(url):
    """
    Extract default Open Graph tags from the provided URL.

    Args:
        url (str): The URL of the webpage.

    Returns:
        tuple: A tuple containing the title, description, and image URL, or None in case of an error.
    """
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title, description, and image URL
        title = soup.find('title').text if soup.find('title') else None
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None
        image_url = soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else None

        return title, description, image_url

    except requests.exceptions.RequestException as req_err:
        st.error(f"Error fetching the URL: {req_err}")
        return None, None, None

    except Exception as err:
        st.error(f"Error parsing the HTML content: {err}")
        return None, None, None


def og_tag_generator():
    """Main function to run the Streamlit app."""
    st.title("AI Open Graph Tag Generator")

    # Platform selection
    platform = st.selectbox(
        "**Select the platform**",
        ["General", "Facebook", "Twitter"],
        help="Choose the platform for which you want to generate Open Graph tags."
    )

    # URL input
    url = st.text_input(
        "**Enter the URL of the page to generate Open Graph tags for:**",
        placeholder="e.g., https://example.com",
        help="Provide the URL of the page you want to generate Open Graph tags for."
    )

    if url:
        # Extract default Open Graph tags
        title, description, image_url = extract_default_og_tags(url)

        # Title hint input
        title_hint = st.text_input(
            "**Modify existing title or suggest a new one (optional):**",
            value=title if title else "",
            placeholder="e.g., Amazing Blog Post Title"
        )

        # Description hint input
        description_hint = st.text_area(
            "**Modify existing description or suggest a new one (optional):**",
            value=description if description else "",
            placeholder="e.g., This is a detailed description of the content."
        )

        # Image URL hint input
        image_hint = st.text_input(
            "**Use this image or suggest a new URL (optional):**",
            value=image_url if image_url else "",
            placeholder="e.g., https://example.com/image.jpg"
        )

        # Generate Open Graph tags
        if st.button("Generate Open Graph Tags"):
            with st.spinner("Generating Open Graph tags..."):
                try:
                    og_tags = generate_og_tags(url, title_hint, description_hint, platform)
                    if og_tags:
                        st.success("Open Graph tags generated successfully!")
                        st.markdown(og_tags)
                    else:
                        st.error("Failed to generate Open Graph tags.")
                except Exception as e:
                    st.error(f"Failed to generate Open Graph tags: {e}")
    else:
        st.info("Please enter a URL to generate Open Graph tags.")
