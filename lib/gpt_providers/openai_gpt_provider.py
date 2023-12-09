########################################################
#
# openai chatgpt integration for blog generation.
# Choosing a model from openai and fine tuning its various paramters. 
#
########################################################

import os
import sys

import requests
import re
import base64
from tqdm import tqdm, trange
import time # I wish
import openai
from openai import OpenAI
from pytube import YouTube
import tempfile
from html2image import Html2Image
import datetime
from PIL import Image
import moviepy.editor as mp
import requests
from moviepy.editor import AudioFileClip
from concurrent.futures import ThreadPoolExecutor

from ..gpt_online_researcher import do_online_research

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

def analyze_and_extract_details_from_image(image_path):
    """
    Analyzes an image using OpenAI's Vision API and extracts Alt Text, Description, Title, and Caption.
    This module provides functionality to analyze images using OpenAI's Vision API.
    It encodes an image to a base64 string and sends a request to the OpenAI API
    to interpret the contents of the image, returning a textual description.

    Args:
        image_path (str): Path to the image file.
        api_key (str): Your OpenAI API key.

    Returns:
        dict: Extracted details including Alt Text, Description, Title, and Caption.
    """
    logger.info(f"analyze_and_extract_details_from_image: Encoding image to base64")
    def encode_image(path):
        """ Encodes an image to a base64 string. """
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_image = encode_image(image_path)
    logger.info("Using GPT-4 Vision to get generated image details and tags.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "The given image is used in blog content. Analyze the given image and suggest the following: Alternative text(Alt Text), description, title, caption."
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

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        assistant_message = response.json()['choices'][0]['message']['content']

        # Extracting details using regular expressions
        alt_text_match = re.search(r'Alt Text: "(.*?)"', assistant_message)
        description_match = re.search(r'Description: (.*?)\n\n', assistant_message)
        title_match = re.search(r'Title: "(.*?)"', assistant_message)
        caption_match = re.search(r'Caption: "(.*?)"', assistant_message)
        image_details = {
            'alt_text': alt_text_match.group(1) if alt_text_match else None,
            'description': description_match.group(1) if description_match else None,
            'title': title_match.group(1) if title_match else None,
            'caption': caption_match.group(1) if caption_match else None
        }

        logger.info(f"analyze_and_extract_details_from_image: {image_details}")
        return image_details

    except requests.RequestException as e:
        #sys.exit(f"Error: GPT-Vision: Failed to communicate with OpenAI API. Error: {e}")
        logger.error(f"Error: GPT-Vision: Failed to communicate with OpenAI API. Error: {e}")
    except Exception as e:
        #sys.exit(f"Error occurred- GPT-Vision: {e}")
        logger.error(f"Error occurred- GPT-Vision: {e}")


def openai_chatgpt(prompt, model="gpt-4-1106-preview", temperature=0.2, max_tokens=4096, top_p=0.9, n=1):
    """
    Wrapper function for openai chat Completion
    """
    # Error in generating topic content: Rate limit reached for default-global-with-image-limits
    # in free account on requests per min. Limit: 3 / min. Please try again in 20s.
    for i in trange(10):
        time.sleep(1)

    try:
        client = OpenAI()
    except Exception as err:
        print("Error: OpenAI Client.")
        exit(1)
    try:
        # using OpenAI's Completion module that helps execute any tasks involving text
        response = client.chat.completions.create(
            # model name used, there are many other models available under the umbrella of GPT-3
            model=model,
            # passing the user input
            messages=[{"role": "user", "content": prompt}],
            # generated output can have "max_tokens" number of tokens
            max_tokens=max_tokens,
            # number of outputs generated in one call
            n=n,
            top_p=top_p,
            #frequency_penalty=0,
            #presence_penalty=0
            )
    except openai.APIError as e:
        #Handle API error here, e.g. retry or log
        SystemError(f"OpenAI API returned an API Error: {e}")
    except openai.APIConnectionError as e:
        #Handle connection error here
        SystemError(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        SystemError(f"OpenAI API request exceeded rate limit: {e}")
    except Exception as err:
        SystemError(f"OpenAI client Error: {err}")

    return response.choices[0].message.content


def openai_chatgpt_streaming_text(user_prompt):
    """
    Function to use stream=True for real time output from openai
    """
    client = OpenAI()
    response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "user", "content": f"{user_prompt}"}],
            max_tokens = 8192,
            temperature = 0.9,
            n=1,
            stream=True
        )
    
    # Create variables to collect the stream of events, iterate through the stream of events
    collected_events = []
    completion_text = ''
    print("\n\n.....COME ONE...\n\n")
    for chunk in response:
        collected_events.append(chunk)  # save the event response
        event_text = chunk.choices[0].delta.content  # extract the text
        completion_text += event_text  # append the text
        sys.stdout.write(chunk.choices[0].delta.content)
        sys.stdout.flush()
    print(f"COMLETION: {completion_text}")
    return completion_text


def generate_dalle2_images(user_prompt, image_dir, num_images=1, img_size="512x512", response_format="url"):
    """
    The generation API endpoint creates an image based on a text prompt.

    Required inputs:
    prompt (str): A text description of the desired image(s). The maximum length is 1000 characters.

    Optional inputs:
    --> num_images (int): The number of images to generate. Must be between 1 and 10. Defaults to 1.
    --> size (str): The size of the generated images. Must be one of "256x256", "512x512", or "1024x1024". 
    Smaller images are faster. Defaults to "1024x1024".
    -->response_format (str): The format in which the generated images are returned. 
    Must be one of "url" or "b64_json". Defaults to "url".
    --> user (str): A unique identifier representing your end-user, which will help OpenAI to monitor and detect abuse.
    """
    logger.info(f"Generated Dall-e-2 blog images will be stored at: {image_dir=}")
    try:
        client = OpenAI()
        img_generation_response = client.images.generate(
            model="dall-e-2",
            prompt=user_prompt,
            n=num_images,
            size=img_size
        )
    except openai.OpenAIError as e:
        logger.error(f"Dalle-2 image generate error: {e.http_status}")
        logger.error(f"{e.error}")
    except Exception as aerr:
        logger.info(f"Failed to generate Image with Dalle2, Error: {aerr}")
    else:
        img_path = save_generated_image(img_generation_response, image_dir)
        return img_path


def generate_dalle3_images(img_prompt, image_dir, size="1024x1024", quality="hd", n=1):
    """ Function to create images using Dalle3 """
    client = OpenAI()
    logger.info("Generating Dall-e-3 image for the blog.")
    try:
        img_generation_response = client.images.generate(
            model="dall-e-3",
            prompt=f"{img_prompt}",
            size=size,
            quality=quality,
            n=1,
        )
    except openai.OpenAIError as e:
        logger.error(f"Dalle-3 image generate error: {e.http_status}")
        logger.error(f"{e.error}")
    except Exception as e:
        SystemError("Failed to Generate images with Dalle3.")
    else:
        #image_url = response.data[0].url
        img_path = save_generated_image(img_generation_response, image_dir)
        return img_path



def speech_to_text(video_url, output_path='.'):
    """ Transcribes speech to text from a YouTube video URL. """
    try:
        # Create a YouTube object
        print(f"Accessing YouTube URL: {video_url}")
        yt = YouTube(video_url)

        # Select the highest quality audio stream
        print("Fetching audio stream. Select the highest quality audio stream")
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream is None:
            print("No audio stream found for this video.")
            return
        else:
            # Download the audio stream
            print(f"Downloading audio for: {yt.title}")
            audio_file = audio_stream.download(output_path)
            print(f"Downloaded: {yt.title} to {output_path}")

            try:
                # Check if the audio file size is less than 24MB
                max_file_size = 24 * 1024 * 1024  # 24MB in bytes
                file_size = os.path.getsize(audio_file)
                if file_size > max_file_size:
                    print("Error: File size exceeds 24MB limit.")
                    exit(1)

                # File uploads are currently limited to 25 MB and the following input 
                # file types are supported: mp3, mp4, mpeg, mpga, m4a, wav, and webm.
                try:
                    client = OpenAI()
                except Exception as err:
                    SystemExit("Unable to get openai client object: {err}")

                print("Transcribing using Openai whisper.")
                transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=open(audio_file, "rb"),
                        response_format="text"
                        )
                return transcript
            except Exception as err:
                print(f"Failed in whisper transcription: {err}")
                exit(1)

    except Exception as e:
        print(f"YT video download, An error occurred: {e}")
        exit(1)
    os.remove(audio_file)


# The idea is to download images from other blogs and recreate from it.
# This helps us generate images very close to the topic and also not worry about prompt message.
def gen_new_from_given_img(img_path, image_dir, num_img=1, img_size="1024x1024", response_format="url"):
    """
    This function will take an image and produce a variant of it.
    Required inputs:
    image (str): The image to use as the basis for the variation(s). Must be a valid PNG file, less than 4MB, and square.

    Optional inputs:
    n (int): The number of images to generate. Must be between 1 and 10. Defaults to 1.
    size (str): The size of the generated images. Must be one of "256x256", "512x512", or "1024x1024". 
    Smaller images are faster. Defaults to "1024x1024".
    response_format (str): The format in which the generated images are returned. Must be one of "url" or "b64_json". Defaults to "url".
    user (str): A unique identifier representing your end-user, which will help OpenAI to monitor and detect abuse.
    """
    logger.info(f"Generating a variation of the image at: {img_path}")
    try:
        client = OpenAI()
        png = Image.open(img_path).convert('RGBA')
        background = Image.new('RGBA', png.size, (255, 255, 255))

        alpha_composite = Image.alpha_composite(background, png)
        alpha_composite.save(img_path, 'PNG', quality=80)
        variation_response = client.images.create_variation(
            image=open(img_path, "rb"),
            n=num_img,
            size=img_size,
            response_format=response_format,
        )
    except Exception as err:
        logger.error(f"An error occured in Image.create_variation::: {err}")
        SystemExit(1)
    try:
        img_path = save_generated_image(variation_response, image_dir)
    except Exception as err:
        logger.error(f"An error in Saving Image.create_variation::: {err}")
        SystemExit(1)
    else:
        return img_path


def save_generated_image(img_generation_response, image_dir):
    """
       Common util function to save the generated images for blog.  
    """
    # save the image
    # We need to change the image name to unique, overwrite and for SEO considerations.
    # Note: filetype should be *.png
    generated_image_name = f"generated_image_{datetime.datetime.now():%Y-%m-%d-%H-%M-%S}.png"
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    # extract image URL from response
    generated_image_url = img_generation_response.data[0].url
    # We use the requests library to fetch the image from URL
    logger.info(f"Fetch the image from url: {generated_image_url}")
    response = requests.get(generated_image_url, stream=True)
    # We use the Image Class from PIL library to open the image
    Image.open(response.raw)
    # Download the image.
    try:
        generated_image = requests.get(generated_image_url).content
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Failed to get generted image content: {e}")
    else:
        logger.info(f"Saving image at path: {generated_image_filepath}")
        with open(generated_image_filepath, "wb") as image_file:
            # Write the image to a file and store.
            image_file.write(generated_image)

    #logger.info(generated_image_filepath)
    logger.info("Display the generated image.")
    img = Image.open(generated_image_filepath)
    img.show()
    return generated_image_filepath
