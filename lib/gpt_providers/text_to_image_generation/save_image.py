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

    generated_image_name = f"generated_image_{datetime.datetime.now():%Y-%m-%d-%H-%M-%S}.webp"
    generated_image_filepath = os.path.join(os.getenv('IMG_SAVE_DIR'), generated_image_name)

    try:
        for i, image in enumerate(img_generation_response["artifacts"]):
            with open(generated_image_filepath, "wb") as f:
                f.write(base64.b64decode(image["base64"]))
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get generated image content: {e}")
        return None

    logger.info(f"Saved image at path: {generated_image_filepath}")

    return generated_image_filepath
