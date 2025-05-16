import os
from PIL import Image
from io import BytesIO
import PIL
import streamlit as st
from google import genai
from google.genai import types
import logging
import datetime
import base64
import random
import time


from .save_image import save_generated_image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('gemini_image_generator')

# With image generation in Gemini, your imagination is the limit. 
# If what you see doesn't quite match what you had in mind, try adding more details to the prompt. 
# The more specific you are, the better Gemini can create images that reflect your vision.

# Generate images using Gemini
# Gemini 2.0 Flash Experimental supports the ability to output text and inline images. 
# This lets you use Gemini to conversationally edit images or generate outputs with interwoven text (for example, generating a blog post with text and images in a single turn).
# Note: Make sure to include responseModalities: ["Text", "Image"] in your generation configuration for text and image output with gemini-2.0-flash-exp-image-generation. Image only is not allowed.


class AIPromptGenerator:
    """
    Generates enhanced AI image prompts based on user keywords,
    following the guidelines of the Imagen documentation.
    """

    def __init__(self):
        self.photography_styles = ["photo", "photograph"]
        self.art_styles = ["painting", "sketch", "drawing", "illustration", "digital art", "render"]
        self.art_techniques = ["technical pencil drawing", "charcoal drawing", "color pencil drawing", "pastel painting", "digital art", "art deco (poster)", "impressionist painting", "renaissance painting", "pop art"]
        self.camera_proximity = ["close-up", "zoomed out", "taken from far away"]
        self.camera_position = ["aerial", "from below"]
        self.lighting = ["natural lighting", "dramatic lighting", "warm lighting", "cold lighting", "studio lighting", "golden hour lighting"]
        self.camera_settings = ["motion blur", "soft focus", "bokeh", "portrait"]
        self.lens_types = ["35mm lens", "50mm lens", "fisheye lens", "wide angle lens", "macro lens", "telephoto lens"]
        self.film_types = ["black and white film", "polaroid"]
        self.materials = ["made of cheese", "made of paper", "made of neon tubes", "metallic", "glass", "wooden", "stone"]
        self.shapes = ["in the shape of a bird", "angular", "curved", "geometric"]
        self.quality_modifiers_general = ["high-quality", "beautiful", "stylized", "detailed", "epic", "grand"]
        self.quality_modifiers_photo = ["4K", "HDR", "studio photo", "professional photo", "photorealistic"]
        self.quality_modifiers_art = ["by a professional artist", "intricate details", "masterpiece"]
        self.aspect_ratios = ["1:1 aspect ratio", "4:3 aspect ratio", "3:4 aspect ratio", "16:9 aspect ratio", "9:16 aspect ratio"]
        self.photorealistic_modifiers = {
            "portraits": ["prime lens", "zoom lens", "24-35mm", "black and white film", "film noir", "shallow depth of field", "duotone (mention two colors)"],
            "objects": ["macro lens", "60-105mm", "high detail", "precise focusing", "controlled lighting"],
            "motion": ["telephoto zoom lens", "100-400mm", "fast shutter speed", "action shot", "movement tracking"],
            "wide-angle": ["wide-angle lens", "10-24mm", "long exposure", "sharp focus", "smooth water or clouds", "astro photography"]
        }

    def generate_prompt(self, keywords):
        """
        Generates an enhanced AI image prompt based on user-provided keywords.

        Args:
            keywords (list): A list of keywords describing the desired image.

        Returns:
            str: An enhanced AI image prompt.
        """
        if not keywords:
            return "A beautiful image."

        prompt_parts = []
        subject = " ".join(keywords)
        prompt_parts.append(subject)

        # Add context and background (optional)
        context_options = ["in a detailed background", "outdoors", "indoors", "in a studio", "with a blurred background"]
        if random.random() < 0.6:  # Add context with a probability
            prompt_parts.append(random.choice(context_options))

        # Add style (optional)
        style_options = self.photography_styles + [f"{art} of" for art in self.art_styles]
        if random.random() < 0.7:
            prompt_parts.insert(0, random.choice(style_options))
            if prompt_parts[0].startswith("painting of") or prompt_parts[0].startswith("sketch of") or prompt_parts[0].startswith("drawing of"):
                if random.random() < 0.5:
                    prompt_parts.append(f"in the style of {random.choice(self.art_techniques)}")

        # Add photography modifiers (if photography style is chosen)
        if any(style in prompt_parts[0] for style in self.photography_styles):
            if random.random() < 0.4:
                prompt_parts.append(random.choice(self.camera_proximity))
            if random.random() < 0.3:
                prompt_parts.append(random.choice(self.camera_position))
            if random.random() < 0.5:
                prompt_parts.append(random.choice(self.lighting))
            if random.random() < 0.3:
                prompt_parts.append(random.choice(self.camera_settings))
            if random.random() < 0.2:
                prompt_parts.append(random.choice(self.lens_types))
            if random.random() < 0.1:
                prompt_parts.append(random.choice(self.film_types))

        # Add shapes and materials (optional)
        if random.random() < 0.3:
            prompt_parts.append(random.choice(self.materials))
        if random.random() < 0.2:
            prompt_parts.append(random.choice(self.shapes))

        # Add quality modifiers (optional)
        if random.random() < 0.6:
            quality_options = self.quality_modifiers_general
            if any(style in prompt_parts[0] for style in self.photography_styles):
                quality_options += self.quality_modifiers_photo
            else:
                quality_options += self.quality_modifiers_art
            prompt_parts.append(random.choice(list(set(quality_options)))) # Avoid duplicates

        # Add aspect ratio (optional)
        if random.random() < 0.2:
            prompt_parts.append(random.choice(self.aspect_ratios))

        return ", ".join(prompt_parts)

    def generate_photorealistic_prompt(self, keywords, focus=""):
        """
        Generates an enhanced AI image prompt specifically for photorealistic images.

        Args:
            keywords (list): A list of keywords describing the desired image.
            focus (str, optional): The focus of the photorealistic image (e.g., "portraits", "objects", "motion", "wide-angle"). Defaults to "".

        Returns:
            str: An enhanced photorealistic AI image prompt.
        """
        if not keywords:
            return "A photorealistic image."

        prompt_parts = ["A photo of", "photorealistic"]
        prompt_parts.append(" ".join(keywords))

        if focus and focus in self.photorealistic_modifiers:
            modifiers = self.photorealistic_modifiers[focus]
            if modifiers:
                num_modifiers = random.randint(1, min(3, len(modifiers)))
                selected_modifiers = random.sample(modifiers, num_modifiers)
                prompt_parts.extend(selected_modifiers)

        # Add general quality modifiers
        if random.random() < 0.5:
            prompt_parts.append(random.choice(self.quality_modifiers_photo))

        # Add lighting
        if random.random() < 0.4:
            prompt_parts.append(random.choice(self.lighting))

        return ", ".join(prompt_parts)


def generate_gemini_image(prompt, keywords=None, style=None, focus=None, enhance_prompt=True, max_retries=3, initial_retry_delay=2, aspect_ratio="16:9"):
    """
    Generate images using Gemini
    Depending on the prompt and context, Gemini will generate content in different modes (text to image, text to image and text, etc.). 
    Here are some examples:

    1). Text to image
    Example prompt: "Generate an image of the Eiffel tower with fireworks in the background."
    2). Text to image(s) and text (interleaved)
    Example prompt: "Generate an illustrated recipe for a paella."

    Image generation may not always trigger:
    - The model may output text only. Try asking for image outputs explicitly (e.g. "generate an image", "provide images as you go along", "update the image").
    - The model may stop generating partway through. Try again or try a different prompt.

    Args:
        prompt (str): The prompt to generate the image from.
        keywords (list, optional): Keywords to enhance the prompt. Defaults to None.
        style (str, optional): The style of the image. Defaults to None.
        focus (str, optional): The focus of the image (e.g., "portraits", "objects", "motion", "wide-angle"). Defaults to None.
        enhance_prompt (bool, optional): Whether to enhance the prompt using AIPromptGenerator. Defaults to True.
        max_retries (int, optional): Maximum number of retry attempts for handling 503 errors. Defaults to 3.
        initial_retry_delay (int, optional): Initial delay in seconds before retrying. Defaults to 2.
        aspect_ratio (str, optional): The aspect ratio for the generated image. Must be one of "16:9", "9:16", "4:3", "3:4", or "1:1". Defaults to "16:9".

    Returns:
        str: The path to the generated image.
    """
    logger.info(f"Generating image with prompt: '{prompt[:100]}...'")
    
    # Check if the GEMINI_API_KEY is available
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        error_msg = "GEMINI_API_KEY is missing. Please set it in your environment variables."
        logger.error(error_msg)
        st.error(f"🔑 {error_msg}")
        return None
    
    # Enhance the prompt if requested
    if enhance_prompt and keywords:
        prompt_generator = AIPromptGenerator()
        if style == "photorealistic" and focus:
            logger.info(f"Generating photorealistic prompt with focus: {focus}")
            enhanced_prompt = prompt_generator.generate_photorealistic_prompt(keywords, focus)
        else:
            logger.info("Generating enhanced prompt")
            enhanced_prompt = prompt_generator.generate_prompt(keywords)
        
        # Combine the enhanced prompt with the original prompt
        prompt = f"{prompt}\n\nEnhanced prompt: {enhanced_prompt}"
        logger.info(f"Final prompt: '{prompt[:100]}...'")
    
    # Add aspect ratio to the prompt
    if aspect_ratio:
        prompt += f"\n\nPlease generate the image with {aspect_ratio} aspect ratio."
    
    retry_count = 0
    retry_delay = initial_retry_delay
    
    while retry_count <= max_retries:
        try:
            client = genai.Client(api_key=api_key)
            contents = (prompt)

            logger.info("Sending request to Gemini API")
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )
            logger.info("Received response from Gemini API")

            img_name = None
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    logger.info(f"Received text response: '{part.text[:100]}...'")
                    print(part.text)
                elif part.inline_data is not None:
                    logger.info("Received image data from Gemini")
                    image = Image.open(BytesIO((part.inline_data.data)))
                    
                    # Resize image to match aspect ratio if needed
                    if aspect_ratio:
                        current_width, current_height = image.size
                        target_width = current_width
                        target_height = current_height
                        
                        # Calculate target dimensions based on aspect ratio
                        if aspect_ratio == "16:9":
                            target_height = int(current_width * 9/16)
                        elif aspect_ratio == "9:16":
                            target_width = int(current_height * 9/16)
                        elif aspect_ratio == "4:3":
                            target_height = int(current_width * 3/4)
                        elif aspect_ratio == "3:4":
                            target_width = int(current_height * 3/4)
                        elif aspect_ratio == "1:1":
                            target_size = min(current_width, current_height)
                            target_width = target_size
                            target_height = target_size
                        
                        logger.info(f"Resizing image from {current_width}x{current_height} to {target_width}x{target_height}")
                        
                        # Create a new image with the target dimensions
                        resized_image = Image.new('RGB', (target_width, target_height), (255, 255, 255))
                        
                        # Calculate position to paste the original image
                        paste_x = (target_width - current_width) // 2
                        paste_y = (target_height - current_height) // 2
                        
                        # Paste the original image onto the new canvas
                        resized_image.paste(image, (paste_x, paste_y))
                        image = resized_image
                    
                    if part.text is not None:
                        img_name = f'{part.text}-gemini-native-image.png'
                    else:
                        img_name = f'gemini-native-image-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.png'
                    try:
                        logger.info(f"Saving image to: {img_name}")
                        image.save(img_name)
                        
                        # Create a dictionary with the expected format for save_generated_image
                        img_response = {
                            "artifacts": [
                                {
                                    "base64": base64.b64encode(open(img_name, "rb").read()).decode('utf-8')
                                }
                            ]
                        }
                        
                        # Call save_generated_image with the correct format
                        save_generated_image(img_response)
                    except Exception as err:
                        logger.error(f"Failed to save image: {err}")
                        st.error(f"Failed to save image: {err}")
            
            logger.info(f"Image generation completed. Image name: {img_name}")
            return img_name
        except Exception as err:
            error_message = str(err)
            logger.error(f"Error in generate_gemini_image: {err}")
            
            # Check if this is a 503 UNAVAILABLE error
            if "503 UNAVAILABLE" in error_message and retry_count < max_retries:
                retry_count += 1
                logger.info(f"Model is overloaded. Retrying in {retry_delay} seconds (attempt {retry_count}/{max_retries})")
                st.warning(f"The image generation service is currently busy. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Exponential backoff
                retry_delay *= 2
            else:
                st.error(f"Error generating image: {err}")
                return None
    
    # If we've exhausted all retries
    st.error("The image generation service is currently unavailable. Please try again later.")
    return None


def edit_image(image_path, prompt, max_retries=3, initial_retry_delay=2):
    """
    - Image editing (text and image to image)
    Example prompt: "Edit this image to make it look like a cartoon"
    Example prompt: [image of a cat] + [image of a pillow] + "Create a cross stitch of my cat on this pillow."
    
    - Multi-turn image editing (chat)
    Example prompts: [upload an image of a blue car.] "Turn this car into a convertible." "Now change the color to yellow."
    
    Image editing with Gemini
    To perform image editing, add an image as input. 
    The following example demonstrats uploading base64 encoded images. 
    For multiple images and larger payloads, check the image input section.

    Args:
        image_path (str): The path to the image to edit.
        prompt (str): The prompt to edit the image with.
        max_retries (int, optional): Maximum number of retry attempts for handling 503 errors. Defaults to 3.
        initial_retry_delay (int, optional): Initial delay in seconds before retrying. Defaults to 2.

    Returns:
        str: The path to the edited image.
    """
    import PIL.Image
    image = PIL.Image.open(image_path)

    retry_count = 0
    retry_delay = initial_retry_delay
    
    while retry_count <= max_retries:
        try:
            client = genai.Client()
            text_input = (prompt)

            logger.info("Sending request to Gemini API for image editing")
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=[text_input, image],
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )
            logger.info("Received response from Gemini API for image editing")

            edited_img_name = None
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    logger.info(f"Received text response: '{part.text[:100]}...'")
                    st.write(part.text)
                elif part.inline_data is not None:
                    logger.info("Received edited image data from Gemini")
                    edited_image = Image.open(BytesIO(part.inline_data.data))
                    edited_image.show()
                    
                    # Save the edited image
                    edited_img_name = f'edited-{os.path.basename(image_path)}'
                    try:
                        logger.info(f"Saving edited image to: {edited_img_name}")
                        edited_image.save(edited_img_name)
                        
                        # Create a dictionary with the expected format for save_generated_image
                        img_response = {
                            "artifacts": [
                                {
                                    "base64": base64.b64encode(open(edited_img_name, "rb").read()).decode('utf-8')
                                }
                            ]
                        }
                        
                        # Call save_generated_image with the correct format
                        save_generated_image(img_response)
                    except Exception as err:
                        logger.error(f"Failed to save edited image: {err}")
                        st.error(f"Failed to save edited image: {err}")
            
            logger.info(f"Image editing completed. Edited image name: {edited_img_name}")
            return edited_img_name
        except Exception as err:
            error_message = str(err)
            logger.error(f"Error in edit_image: {err}")
            
            # Check if this is a 503 UNAVAILABLE error
            if "503 UNAVAILABLE" in error_message and retry_count < max_retries:
                retry_count += 1
                logger.info(f"Model is overloaded. Retrying in {retry_delay} seconds (attempt {retry_count}/{max_retries})")
                st.warning(f"The image editing service is currently busy. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Exponential backoff
                retry_delay *= 2
            else:
                st.error(f"Error editing image: {err}")
                return None
    
    # If we've exhausted all retries
    st.error("The image editing service is currently unavailable. Please try again later.")
    return None


