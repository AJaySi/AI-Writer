"""
Gemini Image Description Module

This module provides functionality to generate text descriptions of images using Google's Gemini API.
"""

import os
import sys
from typing import Optional, Union, List

from google import genai
from PIL import Image
from dotenv import load_dotenv

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def describe_image(image_path: str, prompt: str = "Describe this image in detail:") -> Optional[str]:
    """
    Generate a text description of an image using Google's Gemini API.
    
    Parameters:
        image_path (str): Path to the image file.
        prompt (str, optional): Custom prompt to guide the image description. 
                              Defaults to "Describe this image in detail:".
    
    Returns:
        Optional[str]: The generated description of the image, or None if an error occurs.
    
    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the API key is not set.
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Check if API key is set
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            error_message = "GEMINI_API_KEY environment variable is not set"
            logger.error(error_message)
            raise ValueError(error_message)
        
        # Check if image file exists
        if not os.path.exists(image_path):
            error_message = f"Image file not found: {image_path}"
            logger.error(error_message)
            raise FileNotFoundError(error_message)
        
        # Initialize the Gemini client
        client = genai.Client(api_key=api_key)
        
        # Open and process the image
        try:
            image = Image.open(image_path)
            logger.info(f"Successfully opened image: {image_path}")
        except Exception as e:
            error_message = f"Failed to open image: {e}"
            logger.error(error_message)
            return None
        
        # Generate content description
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    prompt,
                    image
                ]
            )
            
            # Extract and return the text
            description = response.text
            logger.info(f"Successfully generated description for image: {image_path}")
            return description
            
        except Exception as e:
            error_message = f"Failed to generate content: {e}"
            logger.error(error_message)
            return None
            
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logger.error(error_message)
        return None


def analyze_image_with_prompt(image_path: str, prompt: str) -> Optional[str]:
    """
    Analyze an image with a custom prompt using Google's Gemini API.
    
    Parameters:
        image_path (str): Path to the image file.
        prompt (str): Custom prompt for analyzing the image.
    
    Returns:
        Optional[str]: The generated analysis of the image, or None if an error occurs.
    """
    return describe_image(image_path, prompt)


# Example usage
if __name__ == "__main__":
    # Example usage of the function
    image_path = "path/to/your/image.jpg"
    description = describe_image(image_path)
    if description:
        print(f"Image description: {description}")
    else:
        print("Failed to generate image description")