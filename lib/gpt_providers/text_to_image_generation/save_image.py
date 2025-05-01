import base64
import datetime
import os
import requests
from PIL import Image
import logging

def save_generated_image(img_generation_response):
    """
    Save generated images for blog, ensuring unique names for SEO.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Get image save directory with fallback to a local directory
    image_save_dir = os.getenv('IMG_SAVE_DIR', 'generated_images')
    
    # Create the directory if it doesn't exist
    if not os.path.exists(image_save_dir):
        logger.info(f"Creating image save directory: {image_save_dir}")
        os.makedirs(image_save_dir, exist_ok=True)

    generated_image_name = f"generated_image_{datetime.datetime.now():%Y-%m-%d-%H-%M-%S}.webp"
    generated_image_filepath = os.path.join(image_save_dir, generated_image_name)

    try:
        for i, image in enumerate(img_generation_response["artifacts"]):
            with open(generated_image_filepath, "wb") as f:
                f.write(base64.b64decode(image["base64"]))
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get generated image content: {e}")
        return None
    except Exception as e:
        logger.error(f"Error saving image: {e}")
        return None

    logger.info(f"Saved image at path: {generated_image_filepath}")

    return generated_image_filepath
