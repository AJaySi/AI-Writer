import streamlit as st
import base64
import requests
from PIL import Image
import os


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(image_path):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
 
#  Understand which images are informative, decorative, functional, or complex.
#  Identify informative images, then write the text alternative for images using the essential information, describing it in detail. 
#  Don’t forget to include the emotional implications of the image.
#  Filter out decorative images, like a flourish or stylistic elements that lack meaningful context. 
#  Then, write the alt text as “null” as in, <img alt=””> so that screen readers won’t waste users’ time by announcing it.
#  Take your functional images, which describe what happens when you click an image, like the ‘download’ icon. 
#  Then, make sure your alt text doesn’t describe those images but instead, denotes their functionality.
#  Grab your complex infographics or diagrams, then compose alt text describing the information laid out in the images.
#    
#  Less is more: Ensure the length of alternative text is under 125 characters when possible, spaces included.
#  Don’t skimp on quality: Pay close attention to the accuracy of the information and insight the image provides in that short amount of words.
#  Don’t use images of text, whenever possible, except in logos. If used, the image alt text should include the same words as in the image.
#  For image maps, with multiple clickable areas, a group alt text gives the overall context of the map. 
#  Any clickable area should also have its own individual alternative text, describing the link’s destination and purpose.
#  Don’t ever assign a random, vague, or ambiguous alternative text description to an image simply to increase your accessibility score.
#  This could lead to confusion and frustration for a screen reader user. 
#  Alt text accessibility is rooted in providing meaningful and functional alternative means of usability.
#  Poor or random alt text descriptions can arguably be worse than having no alt text at all.

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """You are an SEO expert specializing in writing optimized Alt text for images. 
            Your goal is to create clear, descriptive, and concise Alt text that accurately represents 
            the content and context of the given image. Make sure your response is optimized for search engines and accessibility."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    # Extract the content field from the response
    content = response_data['choices'][0]['message']['content']
    return content


def alt_text_gen():
    st.title("Image Description Generator")

    image_path = st.text_input("Enter the full path of the image file")

    if image_path:
        if os.path.exists(image_path) and image_path.lower().endswith(('jpg', 'jpeg', 'png')):
            try:
                image = Image.open(image_path)
                st.image(image, caption='Uploaded Image', use_column_width=True)

                if st.button("Get Image Alt Text"):
                    with st.spinner("Generating Alt Text..."):
                        try:
                            description = get_image_description(image_path)
                            st.success("Alt Text generated successfully!")
                            st.write("ALt Text:", description)
                        except Exception as e:
                            st.error(f"Error generating description: {e}")
            except Exception as e:
                st.error(f"Error processing image: {e}")
        else:
            st.error("Please enter a valid image file path ending with .jpg, .jpeg, or .png")
    else:
        st.info("Please enter the full path of an image file.")
