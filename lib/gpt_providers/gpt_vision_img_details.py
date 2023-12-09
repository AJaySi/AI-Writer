import requests
import re
import base64
import os
import sys
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
 
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def analyze_and_extract_details_from_image(image_path):
    """
    Analyzes an image using OpenAI's Vision API to extract Alt Text, Description, Title, and Caption.
    
    This function encodes an image to a base64 string and sends a request to the OpenAI API.
    It interprets the contents of the image, returning a textual description.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: A dictionary with extracted details including Alt Text, Description, Title, and Caption.
        None: If an error occurs during processing.

    Raises:
        SystemExit: If a critical error occurs that prevents the function from executing successfully.
    """
    try:
        logger.info("Starting image analysis using OpenAI's Vision API.")

        def encode_image(path):
            """ Encodes an image to a base64 string. """
            with open(path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_image = encode_image(image_path)
        logger.info("Image encoded to base64 successfully.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze the given image and suggest the following: Alternative text(Alt Text), description, title, caption."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        assistant_message = response.json()['choices'][0]['message']['content']
        logger.info("Received response from OpenAI API.")

        # Extracting details using regular expressions
        alt_text_match = re.search(r'Alt Text: "(.*?)"', assistant_message)
        description_match = re.search(r'Description: (.*?)\n\n', assistant_message)
        title_match = re.search(r'Title: "(.*?)"', assistant_message)
        caption_match = re.search(r'Caption: "(.*?)"', assistant_message)

        image_details = {
            'alt_text': alt_text_match.group(1) if alt_text_match else "N/A",
            'description': description_match.group(1) if description_match else "N/A",
            'title': title_match.group(1) if title_match else "N/A",
            'caption': caption_match.group(1) if caption_match else "N/A"
        }

        logger.info("Image analysis completed successfully.")
        return image_details

    except requests.RequestException as e:
        logger.error(f"GPT-Vision API communication failure. Error: {e}")
        sys.exit(f"Exiting due to GPT-Vision API communication failure: {e}")

    except Exception as e:
        logger.error(f"Unexpected error occurred during image analysis: {e}")
        sys.exit(f"Exiting due to an unexpected error: {e}")

# Example usage
if __name__ == "__main__":
    image_path = "path/to/your/image.jpg"
    try:
        details = analyze_and_extract_details_from_image(image_path)
        if details:
            print(f"Extracted image details: {details}")
        else:
            print("No details extracted from the image.")
    except SystemExit as e:
        print(f"Terminated: {e}")
