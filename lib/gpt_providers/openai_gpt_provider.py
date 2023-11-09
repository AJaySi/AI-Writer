########################################################
#
# openai chatgpt integration for blog generation.
# Choosing a model from openai and fine tuning its various paramters. 
#
########################################################

import os
import sys

from tqdm import tqdm, trange
import time # I wish
import openai
from openai import OpenAI
from pytube import YouTube
import tempfile
from html2image import Html2Image
import datetime
from PIL import Image
import requests

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )



def openai_chatgpt(prompt, model="gpt-3.5-turbo-16k", temperature=0.2, max_tokens=8192, top_p=0.9, n=1):
    """
    Wrapper function for openai chat Completion
    """
    # Error in generating topic content: Rate limit reached for default-global-with-image-limits
    # in free account on requests per min. Limit: 3 / min. Please try again in 20s.
    for i in trange(10):
        time.sleep(1)

    try:
        client = OpenAI()
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


def speech_to_text(video_url):
    """ Common openai function for speech to text. """
    client = OpenAI()
    try:
        # Download YouTube video
        logger.info(f"Download YouTube video: {video_url}")
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()

        # Save the video in a temporary file
        logger.info(f"Finished Downloading, Saving video for transcription.")
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            temp_file_name = temp_file.name

        stream.download(output_path=os.path.dirname(temp_file_name), filename=os.path.basename(temp_file_name))
        try:
            # Transcribe the video using OpenAI's Whisper API
            logger.info(f"Transcribe the video using OpenAI's Whisper API")
            with open(temp_file_name, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file
                        )
        except Exception as err:
            logger.error(f"Failed to transcribe using whisper model: {err}")
        
        logger.info("Finished Transcribing. Creating a blog from the transcript.")
        # Remove the temporary file after transcription
        os.remove(temp_file_name)
        return(transcript)

    except Exception as e:
        logger.error(f"Error: speech-to-text, Failed to transcribe url: {video_url} with error: {e}")


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
