import streamlit as st
import base64
import requests
from PIL import Image
import os


def encode_image(image_path):
    """
    Encodes an image to base64 format.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Base64 encoded string of the image.

    Raises:
        ValueError: If the image path is invalid.
    """
    safe_root = os.getenv('SAFE_ROOT_DIRECTORY', '/safe/root/directory')  # Use an environment variable for the safe root directory
    normalized_path = os.path.normpath(image_path)
    if not normalized_path.startswith(safe_root):
        raise ValueError("Invalid image path")
    with open(normalized_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_image_description(image_path):
    """
    Generates a description for the given image using an external API.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Description of the image.

    Raises:
        ValueError: If the image path is invalid.
    """
    safe_root = os.getenv('SAFE_ROOT_DIRECTORY', '/safe/root/directory')  # Use an environment variable for the safe root directory
    normalized_path = os.path.normpath(image_path)
    if not normalized_path.startswith(safe_root):
        raise ValueError("Invalid image path")
    base64_image = encode_image(normalized_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """You are an SEO expert specializing in writing optimized Alt text for images. 
            Your goal is to create clear, descriptive, and concise Alt text that accurately represents 
            the content and context of the given image. Make sure your response is optimized for search engines and accessibility."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    # Extract the content field from the response
    content = response_data['choices'][0]['message']['content']
    return content


def alt_text_gen():
    """
    Streamlit app function to generate Alt text for an uploaded image.
    """
    st.title("Image Description Generator")

    image_path = st.text_input("Enter the full path of the image file", help="Provide the full path to a .jpg, .jpeg, or .png image file")

    if image_path:
        if os.path.exists(image_path) and image_path.lower().endswith(('jpg', 'jpeg', 'png')):
            try:
                image = Image.open(image_path)
                st.image(image, caption='Uploaded Image', use_column_width=True)

                if st.button("Get Image Alt Text"):
                    with st.spinner("Generating Alt Text..."):
                        try:
                            description = get_image_description(image_path)
                            st.success("Alt Text generated successfully!")
                            st.write("Alt Text:", description)
                        except Exception as e:
                            st.error(f"Error generating description: {e}")
            except Exception as e:
                st.error(f"Error processing image: {e}")
        else:
            st.error("Please enter a valid image file path ending with .jpg, .jpeg, or .png")
    else:
        st.info("Please enter the full path of an image file.")
