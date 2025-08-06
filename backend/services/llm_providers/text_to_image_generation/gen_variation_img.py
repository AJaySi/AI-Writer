from loguru import logger
import sys
from PIL import Image
from openai import OpenAI

def gen_new_from_given_img(img_path, image_dir, num_img=1, img_size="1024x1024", response_format="url"):
    """
    Generates variations of a given image using OpenAI's image variation API.

    This function takes an existing image, processes it, and generates a specified number of new images based on it. 
    These generated images are variations of the original, providing creative flexibility.

    Args:
        img_path (str): Path to the original image file.
        image_dir (str): Directory where the generated images will be saved.
        num_img (int, optional): Number of image variations to generate. Defaults to 1.
        img_size (str, optional): Size of the generated images. Defaults to "1024x1024".
        response_format (str, optional): Format in which the generated images are returned. Defaults to "url".

    Returns:
        str: Path to the saved image variation.

    Raises:
        SystemExit: If a critical error occurs that prevents successful execution.
    """
    try:
        logger.info(f"Starting image variation generation for: {img_path}")

        # Convert and prepare the image
        png = Image.open(img_path).convert('RGBA')
        background = Image.new('RGBA', png.size, (255, 255, 255))
        alpha_composite = Image.alpha_composite(background, png)
        alpha_composite.save(img_path, 'PNG', quality=80)
        logger.info("Image prepared for variation generation.")

        client = OpenAI()
        variation_response = client.images.create_variation(
            image=open(img_path, "rb", encoding="utf-8"),
            n=num_img,
            size=img_size,
            response_format=response_format
        )

        # Saving the generated image
        generated_image_path = save_generated_image(variation_response, image_dir)
        logger.info(f"Image variation generated and saved to: {generated_image_path}")
        return generated_image_path

    except Exception as e:
        logger.error(f"Error occurred during image variation generation: {e}")
        sys.exit(f"Exiting due to critical error: {e}")
