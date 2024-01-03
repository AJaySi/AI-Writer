import os
import datetime

from selenium import webdriver
from PIL import Image
import shutil
from screenshotone import Client, TakeOptions
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path('../.env'))


def screenshot_api(url, generated_image_filepath):
    """ Use screenshotone API to take company webpage screenshots """
    try:
        # create API client
        client = Client(os.getenv('SCREENSHOTONE_ACCESS_KEY'), os.getenv('SCREENSHOTONE_SECRET_KEY'))

        # set up options
        options = (TakeOptions.url(url)
            .format("png")
            .viewport_width(1024)
            .viewport_height(768)
            .block_cookie_banners(True)
            .block_chats(True))

        # generate the screenshot URL and share it with a user
        #url = client.generate_take_url(options)
        # or render a screenshot and download the image as stream
        image = client.take(options)

        # store the screenshot the example.png file
        with open(generated_image_filepath, 'wb') as result_file:
            shutil.copyfileobj(image, result_file)

        # Display the screenshot using Image.show
        image = Image.open(generated_image_filepath)
        image.show()

    except Exception as err:
        print(f"Failed in screenshotone api: {err}")
        generated_image_filepath = take_screenshot(url, generated_image_filepath)

    return generated_image_filepath


def take_screenshot(url, generated_image_filepath, full_screenshot):
    # Create a webdriver instance
    driver = webdriver.Chrome()

    # Navigate to the given url
    driver.get(url)

    # Get the height of the webpage
    page_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to the bottom of the webpage
    for i in range(0, page_height, 100):
        driver.execute_script(f"window.scrollTo(0, {i})")

    # Get the total height of the webpage
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Resize the webdriver window to the height of the webpage
    if full_screenshot:
        driver.set_window_size(800, total_height)

    # Take a screenshot of the webpage
    screenshot = driver.get_screenshot_as_png()

    # Close the webdriver instance
    driver.quit()

    # Save the screenshot to a file
    with open(generated_image_filepath, "wb") as f:
        f.write(screenshot)

    # Display the screenshot using Image.show
    image = Image.open(generated_image_filepath)
    image.show()

    return generated_image_filepath
