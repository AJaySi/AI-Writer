import os
import sys
import tinify
from PIL import Image
from loguru import logger
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Set Tinyfy API key from environment variable
tinify_key = os.getenv('TINIFY_API_KEY')
if tinify_key:
    tinify.key = tinify_key

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
)

def compress_image(image, quality=45, resize=None, preserve_exif=False):
    """
    Compress and optionally resize an image.
    
    Args:
        image (PIL.Image): Image object to compress.
        quality (int): Quality of the output image (1-100).
        resize (tuple): Tuple (width, height) to resize the image.
        preserve_exif (bool): Preserve EXIF data if True.
    
    Returns:
        PIL.Image: The compressed and resized image object.
    """
    try:
        # Ensure image is in a compatible mode for JPEG/WebP
        if image.mode == 'RGBA':
            logger.info("Converting RGBA image to RGB.")
            image = image.convert('RGB')

        exif = image.info.get('exif') if preserve_exif and 'exif' in image.info else None

        # Resize image if needed
        if resize:
            image = image.resize(resize, Image.LANCZOS)
            logger.info(f"Resized image to {resize}")

        # Save compressed image
        try:
            logger.info("Attempting to save the compressed image with EXIF data (if any).")
            image.save("temp.jpg", optimize=True, quality=quality, exif=exif)
        except Exception as exif_error:
            logger.warning(f"Error saving image with EXIF: {exif_error}. Saving without EXIF.")
            image.save("temp.jpg", optimize=True, quality=quality)

        logger.info("Image compression successful.")
        return Image.open("temp.jpg")
    
    except Exception as e:
        logger.error(f"Error compressing image: {e}")
        st.error("Failed to compress the image. Please try again.")
        return None

def convert_to_webp(image, image_path):
    """
    Convert an image to WebP format.
    
    Args:
        image (PIL.Image): Image object to convert.
        image_path (str): Path to save the WebP image.
    
    Returns:
        str: Path to the WebP image.
    """
    try:
        webp_path = os.path.splitext(image_path)[0] + '.webp'
        image.save(webp_path, 'WEBP', quality=80, method=6)
        return webp_path
    except Exception as e:
        logger.error(f"Error converting image to WebP: {e}")
        st.error("Failed to convert the image to WebP format. Please try again.")
        return None

def compress_image_tinyfy(image_path):
    """
    Compress an image using Tinyfy API.
    
    Args:
        image_path (str): Path to the image to be compressed.
    
    Returns:
        None
    """
    try:
        if not tinify.key:
            logger.warning("Tinyfy API key is not set. Skipping Tinyfy compression.")
            return
        
        source = tinify.from_file(image_path)
        source.to_file(image_path)
        logger.info("Tinyfy compression successful.")
    except Exception as e:
        logger.error(f"Error during Tinyfy compression: {e}")
        st.warning("Tinyfy compression failed. Ensure the API key is set.")

def optimize_image(image, image_path, quality, resize, preserve_exif):
    """
    Optimize the image by compressing and converting it to WebP, with optional Tinyfy compression.

    Args:
        image (PIL.Image): The original image.
        image_path (str): The path to the image file.
        quality (int): Quality level for compression.
        resize (tuple): Dimensions to resize the image.
        preserve_exif (bool): Whether to preserve EXIF data.

    Returns:
        str: Path to the optimized WebP image, or None if failed.
    """
    logger.info("Starting image optimization process...")

    # Compress the image using Pillow
    compressed_image = compress_image(image, quality, resize, preserve_exif)
    if compressed_image is None:
        return None

    # Convert image to WebP format
    webp_path = convert_to_webp(compressed_image, image_path)
    if webp_path is None:
        return None

    # Optionally compress the WebP image using Tinyfy API
    if tinify.key:
        compress_image_tinyfy(webp_path)
    else:
        logger.info("Tinyfy key not provided, skipping Tinyfy compression.")

    return webp_path

def main_img_optimizer():
    st.title("ALwrity Image Optimizer")
    st.markdown("## Upload an image to optimize its size and format.")

    # API Key Input (Optional)
    input_tinify_key = st.text_input("Optional: Enter your Tinyfy API Key")
    if input_tinify_key:
        tinify.key = input_tinify_key

    # File Upload
    uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)

        # Image Compression Options
        quality = st.slider("Compression Quality", 1, 100, 45)
        preserve_exif = st.checkbox("Preserve EXIF Data", value=False)
        resize = st.checkbox("Resize Image")

        if resize:
            width = st.number_input("Width", value=image.width)
            height = st.number_input("Height", value=image.height)
            resize_dims = (width, height)
        else:
            resize_dims = None

        # Optimize Image
        if st.button("Optimize Image"):
            with st.spinner("Optimizing..."):
                if tinify.key:
                    st.info("Tinyfy compression will be applied.")
                
                webp_path = optimize_image(image, uploaded_file.name, quality, resize_dims, preserve_exif)

                if webp_path:
                    st.image(webp_path, caption="Optimized Image (WebP)", use_column_width=True)
                    st.success("Image optimization completed!")

                    # Provide download link
                    with open(webp_path, "rb") as file:
                        st.download_button(
                            label="Download Optimized Image",
                            data=file,
                            file_name=os.path.basename(webp_path),
                            mime="image/webp"
                        )
