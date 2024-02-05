import sys
import os
import tinify
from PIL import Image
from loguru import logger
from tqdm import tqdm
from dotenv import load_dotenv 

#default directory for .env file is the current directory
#if you set .env in different directory, put the directory address load_dotenv("directory_of_.env)
load_dotenv()

# Retrieve Tinyfy API key from environment variable
tinify.key = os.getenv('TINIFY_API_KEY')

# Configure logger
logger.remove()
logger.add(sys.stdout, colorize=True, format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

def compress_image(image_path, quality=45, resize=None, preserve_exif=False):
    """
    Compress and optionally resize an image, and overwrite the original image.
    
    Args:
        image_path (str): Path to the original image.
        quality (int): Quality of the output image (1-100).
        resize (tuple): Tuple (width, height) to resize image.
        preserve_exif (bool): Preserve EXIF data if True.
    """
    if not os.path.exists(image_path):
        logger.error(f"Image path does not exist: {image_path}")
        return

    original_size = os.path.getsize(image_path)
    try:
        with Image.open(image_path) as img:
            img_format = img.format
            exif = img.info['exif'] if preserve_exif and 'exif' in img.info else None

            if resize:
                img = img.resize(resize, Image.ANTIALIAS)

            img.save(image_path, format=img_format, quality=quality, optimize=True, exif=exif)

            compressed_size = os.path.getsize(image_path)
            reduction = (1 - (compressed_size / original_size)) * 100
            logger.info(f"Compressed {image_path}, Reduction: {reduction:.2f}%")
    except Exception as e:
        logger.error(f"Error compressing image {image_path}: {e}")

def is_image_file(filename):
    """
    Check if a file is an image based on its extension.
    
    Args:
        filename (str): Name of the file to check.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)


def convert_to_webp(image_path):
    """
    Convert an image to WebP format.

    Args:
        image_path (str): Path to the original image.

    Returns:
        str: Path to the WebP image.
    """
    if not os.path.exists(image_path):
        logger.error(f"Image path does not exist: {image_path}")
        return

    try:
        with Image.open(image_path) as img:
            webp_path = os.path.splitext(image_path)[0] + '.webp'
            img.save(webp_path, 'WEBP')
            logger.info(f"Converted {image_path} to WebP")
            return webp_path
    except Exception as e:
        logger.error(f"Error converting image to WebP: {e}")


def compress_image_tinyfy(image_path):
    """
    Compress the image using Tinyfy API.

    Args:
        image_path (str): Path to the original image.
    """
    if not os.path.exists(image_path):
        logger.error(f"Image path does not exist: {image_path}")
        return

    try:
        source = tinify.from_file(image_path)
        source.to_file(image_path)
        logger.info(f"Compressed {image_path} using Tinyfy API")
    except tinify.Error as e:
        logger.error(f"Tinyfy API error: {e}")


def optimize_image(image_path):
    image_path = convert_to_webp(image_path)
    compress_image_tinyfy(image_path)
    compress_image(image_path)
    return image_path
