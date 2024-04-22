import datetime
import os
import requests
from PIL import Image
import logging

def save_generated_image(img_generation_response, image_dir):
    """
    Save generated images for blog, ensuring unique names for SEO.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    generated_image_name = f"generated_image_{datetime.datetime.now():%Y-%m-%d-%H-%M-%S}.png"
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    generated_image_url = img_generation_response.data[0].url

    logger.info(f"Fetch the image from url: {generated_image_url}")
    try:
        response = requests.get(generated_image_url, stream=True)
        response.raise_for_status()
        with open(generated_image_filepath, "wb", encoding="utf-8") as image_file:
            image_file.write(response.content)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get generated image content: {e}")
        return None

    logger.info(f"Saved image at path: {generated_image_filepath}")

    if os.environ.get('DISPLAY', ''):  # Check if display is supported
        img = Image.open(generated_image_filepath)
        img.show()

    return generated_image_filepath

