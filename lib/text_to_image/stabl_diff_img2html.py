import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Set the host URL environment variable. Ensure it doesn't have 'https' or a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# Ensure you sign up for an account to obtain an API key:
# https://platform.stability.ai/
# Your API key can be found here after account creation:
# https://platform.stability.ai/account/keys


def generate_stable_diffusion_image(prompt, image_dir):
    """
    Generate images using Stable Diffusion API based on a given prompt.

    Args:
        prompt (str): The prompt to generate the image.
        image_dir (str): The directory where the image will be saved.

    Raises:
        Warning: If the adult content classifier is triggered.
        Exception: For any issues during image generation or saving.
    """
    try:
        # Initialize the StabilityInference client with the API key and other settings.
        stability_api = client.StabilityInference(
            key=os.environ['STABILITY_KEY'],  # Reference to the API key.
            verbose=True,  # Enable verbose mode for debug messages.
            engine="stable-diffusion-xl-1024-v1-0",  # Engine used for generation.
        )

        # Generating the image with specified parameters.
        answers = stability_api.generate(
            prompt=prompt,
            seed=4253978046,  # Deterministic seed for reproducible results.
            steps=50,  # Number of inference steps.
            cfg_scale=7.0,  # Strength of prompt matching.
            width=1024, height=1024,  # Image dimensions.
            samples=1,  # Number of images to generate.
            sampler=generation.SAMPLER_K_DPMPP_2M  # Denoising sampler selection.
        )

        # Process responses and save images.
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Request activated safety filters. Modify the prompt and retry."
                    )
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    img_name = os.path.join(image_dir, f"{artifact.seed}.png")
                    img.show()
                    img.save(img_name)  # Save the image with the seed in the filename.

    except Exception as e:
        raise Exception(f"Error during image generation or saving: {e}")

# Example usage:
# generate_stable_diffusion_image("A futuristic cityscape", "/path/to/save/images/")

