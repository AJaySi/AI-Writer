import os
import  sys
import datetime
import subprocess

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

from selenium import webdriver
from PIL import Image
import shutil
from screenshotone import Client, TakeOptions
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path('../.env'))

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


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
        with open(generated_image_filepath, 'wb', encoding="utf-8") as result_file:
            shutil.copyfileobj(image, result_file)

        # Display the screenshot using Image.show
        image = Image.open(generated_image_filepath)
        image.show()
        # Wait for 2 seconds (adjust the delay as needed)
        sleep(2)
        # Close the image window
        image.close()

    except Exception as err:
        print(f"Failed in screenshotone api: {err}")
        generated_image_filepath = take_screenshot(url, generated_image_filepath)

    return generated_image_filepath


def take_screenshot(url, generated_image_filepath):
    # Create a webdriver instance in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    logger.debug(f"Taking screenshot of url: {url}")

    try:
        # Navigate to the given url
        driver.get(url)

        # Optionally, increase the delay to ensure all content is loaded
        sleep(2)

        # Explicitly wait for the page to load (adjust timeout as needed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Set a larger window size
        driver.set_window_size(1200, 800)

        # Take a screenshot of the webpage
        screenshot = driver.get_screenshot_as_png()

        # Save the screenshot to a file
        with open(generated_image_filepath, "wb", encoding="utf-8") as f:
            f.write(screenshot)

        # Display the screenshot using Image.show
        image = Image.open(generated_image_filepath)
        image.show()
        # Wait for 2 seconds (adjust the delay as needed)
        sleep(2)

        # Close the image window using subprocess (platform-dependent)
        subprocess.run(["pkill", "-f", "display"])  # Adjust based on your platform and viewer

        # If using macOS, you can use the following:
        # subprocess.run(["osascript", "-e", 'tell application "Preview" to close every window'])
        # If using Windows, you can use the following:
        # subprocess.run(["taskkill", "/F", "/IM", "Microsoft.Photos.exe"])

        logger.debug(f"Screenshot successfully stored at: {generated_image_filepath}")
        return generated_image_filepath
    finally:
        # Close the webdriver instance
        driver.quit()
