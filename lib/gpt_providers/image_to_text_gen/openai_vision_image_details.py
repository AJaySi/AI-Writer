"""
This module provides functionality to analyze images using OpenAI's Vision API. 
It encodes an image to a base64 string and sends a request to the OpenAI API 
to interpret the contents of the image, returning a textual description.
"""

import requests
import sys
import re
import base64

def analyze_and_extract_details_from_image(image_path, api_key):
    """
    Analyzes an image using OpenAI's Vision API and extracts Alt Text, Description, Title, and Caption.

    Args:
        image_path (str): Path to the image file.
        api_key (str): Your OpenAI API key.

    Returns:
        dict: Extracted details including Alt Text, Description, Title, and Caption.
    """
    def encode_image(path):
        """ Encodes an image to a base64 string. """
        with open(path, "rb", encoding="utf-8") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "The given image is used in blog content. Analyze the given image and suggest alternative(alt) test, description, title, caption."
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

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        assistant_message = response.json()['choices'][0]['message']['content']

        # Extracting details using regular expressions
        alt_text_match = re.search(r'Alt Text: "(.*?)"', assistant_message)
        description_match = re.search(r'Description: (.*?)\n\n', assistant_message)
        title_match = re.search(r'Title: "(.*?)"', assistant_message)
        caption_match = re.search(r'Caption: "(.*?)"', assistant_message)

        return {
            'alt_text': alt_text_match.group(1) if alt_text_match else None,
            'description': description_match.group(1) if description_match else None,
            'title': title_match.group(1) if title_match else None,
            'caption': caption_match.group(1) if caption_match else None
        }

    except requests.RequestException as e:
        sys.exit(f"Error: Failed to communicate with OpenAI API. Error: {e}")
    except Exception as e:
        sys.exit(f"Error occurred: {e}")
