#########################################################
#
# This module will generate images for the blogs using APIs
# from Dall-E and other free resources. Given a prompt, the
# images will be stored in local directory.
# Required: openai API key.
#
#########################################################

# imports

import openai  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to logger.info and edit images

# set API key
# Taking from env is safer than hardcoding here. But, not all have shell to export.
# Better to take it from a config file and pass it as a parameter.
# variable OPENAI_API_KEY=<API-KEY>
openai.api_key = os.environ.get("OPENAI_API_KEY")
# set a directory to save DALL·E images to
image_dir_name = "blog_images"

image_dir = os.path.join(os.curdir, image_dir_name)
# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)


def generate_image(logger, num_images=1, img_size="1024x1024", response_format="url"):
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
    # logger.info the directory to save to. TBD: Need to log these.
    logger.info(f"Generated blog images will be stored at: {image_dir=}")

    # TBD: Ask gpt for prompt for AI generated images as:
    # I want you to act as an artist advisor providing advice on various art styles such tips on utilizing 
    # light & shadow effects effectively in painting, shading techniques while sculpting etc.
    # Develop prompts for an AI-generated art piece inspired by [concept], using [symbolism] and [metaphor].
    # Provide prompts for an AI-generated art piece inspired by [era] art, incorporating [medium] and [subject matter].
    # Develop a set of prompts that could be used to generate AI-generated art focused on the theme of “urban decay.”
    # I want you to act as a prompt generator for Science Fiction Art and 
    # give me five prompts that transport me to a futuristic world.
    # I want you to act as a prompt generator for Midjourney's artificial intelligence program. 
    # Your job is to provide detailed and creative descriptions that will inspire unique and interesting images from the AI. 
    # Keep in mind that the AI is capable of understanding a wide range of language and can interpret abstract concepts, 
    # so feel free to be as imaginative and descriptive as possible. For example, 
    # you could describe a scene from a futuristic city, or a surreal landscape filled with strange creatures. 
    # The more detailed and imaginative your description, the more interesting the resulting image will be. 
    # Here is your first prompt: ""
    
    prompt = "An illustration of AI teaching human to speak"
    
    # call the OpenAI API to generate image from prompt.
    logger.info(f"Calling openai.image.generate with prompt: {prompt}")
    try:
        img_generation_response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url",
        )
    except AttributeError as aerr:
        logger.info(f"Failed to generate Image, Try: pip install openai --upgrade in your terminal.Error: {aerr}")
    else:
        # logger.info response/result. dbg.
        print(f"{img_generation_response}")
        save_generated_image(logger, img_generation_response)


def save_generated_image(logger, img_generation_response):
    """
         
    """
    # save the image
    # We need to change the image name to unique, overwrite and for SEO considerations.
    # Note: filetype should be *.png
    generated_image_name = "generated_image.png"

    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    # extract image URL from response
    generated_image_url = img_generation_response["data"][0]["url"]
    print(f"Extracted URL: {generated_image_url}")
    
    # We use the requests library to fetch the image from URL
    response = requests.get(generated_image_url, stream=True)
    # We use the Image Class from PIL library to open the image
    Image.open(response.raw)
    # Download the image.
    try:
        generated_image = requests.get(generated_image_url).content
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Failed to get generted image content: {e}")
    else:
        with open(generated_image_filepath, "wb") as image_file:
            # Write the image to a file and store.
            image_file.write(generated_image)

    # Optional, dbg.
    # logger.info the image
    #logger.info(generated_image_filepath)
    print("Display the generated image.")
    img = Image.open(generated_image_filepath)
    img.show()

    # Close image window.
    #for proc in psutil.process_iter():
    #    if proc.name() == "Image Viewer":
    #        proc.kill()


# WIP
# The idea is to download images from other blogs and recreate from it.
# This helps us generate images very close to the topic and also not worry about prompt message.
def gen_new_from_given_img(logger, num_img=1, img_size="1024x1024", response_format="url"):
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
    img_path = "/home/ajsingh/pseo_experiments_V0.0.1/blog_images/variation_example.png"
    try:
        png = Image.open(img_path).convert('RGBA')
        background = Image.new('RGBA', png.size, (255, 255, 255))

        alpha_composite = Image.alpha_composite(background, png)
        alpha_composite.save('foo.png', 'PNG', quality=80)
        variation_response = openai.Image.create_variation(
            image=open('foo.jpg', "rb"),
            n=num_img,
            size=img_size,
            response_format=response_format,
        )
    except Exception as err:
        logger.error(f"An error occured in Image.create_variation::: {err}")
        SystemExit(1)

    # logger.info response
    logger.info(variation_response)

    # save the images
    variation_urls = [datum["url"] for datum in variation_response["data"]]  # extract URLs
    variation_images = [requests.get(url).content for url in variation_urls]  # download images
    variation_image_names = [f"variation_image_{i}.png" for i in range(len(variation_images))]  # create names
    variation_image_filepaths = [os.path.join(image_dir, name) for name in variation_image_names]  # create filepaths
    for image, filepath in zip(variation_images, variation_image_filepaths):  # loop through the variations
        with open(filepath, "wb") as image_file:  # open the file
            image_file.write(image)  # write the image to the file

    # logger.info the original image
    logger.info(generated_image_filepath)
    orig_img = Image.open(generated_image_filepath)
    orig_img.show()

    # logger.info the new variations
    for variation_image_filepaths in variation_image_filepaths:
        logger.info(variation_image_filepaths)
        var_img = Image.open(variation_image_filepaths)
        var_img.show()
