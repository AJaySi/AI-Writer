from PIL import Image
import requests

# Ensure you sign up for an account to obtain an API key:
# https://platform.stability.ai/
# Your API key can be found here after account creation:
# https://platform.stability.ai/account/keys


def generate_stable_diffusion_image(prompt):
    """
    Generate images using Stable Diffusion API based on a given prompt.

    Args:
        prompt (str): The prompt to generate the image.
        image_dir (str): The directory where the image will be saved.

    Raises:
        Warning: If the adult content classifier is triggered.
        Exception: For any issues during image generation or saving.
    """
    api_key = os.getenv('STABILITY_API_KEY')

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "webp",
        },
    )

    if response.status_code == 200:
        with open("./dog-wearing-glasses.jpeg", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
