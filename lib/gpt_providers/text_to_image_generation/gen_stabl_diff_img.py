# Ensure you sign up for an account to obtain an API key:
# https://platform.stability.ai/
# Your API key can be found here after account creation:
# https://platform.stability.ai/account/keys

import base64
import os
import requests
from PIL import Image
from io import BytesIO
import streamlit as st

from .save_image import save_generated_image


def generate_stable_diffusion_image(prompt):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_API_KEY")
    
    if api_key is None:
        st.warning("Missing Stability API key.")
    
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )
    
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    
    data = response.json()
    img_path = save_generated_image(data)

    for i, image in enumerate(data["artifacts"]):
        # Decode base64 image data
        img_data = base64.b64decode(image["base64"])
        # Open image using PIL
        img = Image.open(BytesIO(img_data))
        # Display the image
        img.show()

    return img_path
