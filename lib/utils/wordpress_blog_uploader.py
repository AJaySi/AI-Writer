import os
import sys

import mimetypes
import requests
from requests.auth import HTTPBasicAuth
import base64
import json
from clint.textui import progress

from PIL import Image
import tempfile
import os

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

## Check if blog needs to be posted on wordpress.
#if wordpress:
## Fixme: Fetch all tags and categories to check, if present ones are present and
## use them else create new ones. Its better to use chatgpt than string comparison.
## Similar tags and categories will be missed.
## blog_categories = 
## blog_tags = 
#logger.info("Uploading the blog to wordpress.\n")
#main_img_path = compress_image(main_img_path, quality=85)
#try:
#    img_details = analyze_and_extract_details_from_image(main_img_path)
#    alt_text = img_details.get('alt_text')
#    img_description = img_details.get('description')
#    img_title = img_details.get('title')
#    caption = img_details.get('caption')
#    try:
#        media = upload_media(wordpress_url, wordpress_username, wordpress_password,
#                main_img_path, alt_text, img_description, img_title, caption)
#    except Exception as err:
#        sys.exit(f"Error occurred in upload_media: {err}")
#except Exception as e:
#    sys.exit(f"Error occurred in analyze_and_extract_details_from_image: {e}")
#
## Then create the post with the uploaded media as the featured image
#media_id = media['id']
#blog_markdown_str = convert_markdown_to_html(blog_markdown_str)
#try:
#   upload_blog_post(wordpress_url, wordpress_username, wordpress_password, a_blog_topic,
#       blog_markdown_str, media_id, blog_meta_desc, blog_categories, blog_tags, status='publish')
#except Exception as err:
#    sys.exit(f"Failed to upload blog to wordpress.Error: {err}")


def compress_image(image_path, quality=85):
    """
    Compress the image by reducing its quality and logger.info size information.

    :param image_path: Path to the original image
    :param quality: Quality of the output image (1-100), lower means more compression
    :return: Path to the compressed image
    """
    if not os.path.exists(image_path):
        raise ValueError(f"Provided image path does not exist: {image_path}")

    # Get the size of the original image
    original_size = os.path.getsize(image_path)

    # Open the image
    with Image.open(image_path) as img:
        # Define the format based on the original image format
        img_format = img.format

        # Create a temporary file to save the compressed image
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.' + img_format.lower())

        # Save the image with reduced quality
        img.save(temp_file, format=img_format, quality=quality, optimize=True)

        # Get the size of the compressed image
        compressed_size = os.path.getsize(temp_file.name)

        # Calculate the percentage reduction
        reduction = (1 - (compressed_size / original_size)) * 100
        logger.info("########### Image Compression ###############")
        logger.info(f"Compressing the image, Original size: {original_size / 1024:.2f} KB")
        logger.info(f"Compressed size: {compressed_size / 1024:.2f} KB")
        logger.info(f"Reduction in image size: {reduction:.2f}%")
        # TBD: https://tinypng.com/developers/reference/python
        logger.info(f"Note: Consider converting images to JPEG/WebP format.\n\n")

        return temp_file.name


def create_wordpress_tag(url, username, app_password, tag_name):
    """
    Create a new tag in WordPress using the REST API and return its ID.

    :param url: URL of the WordPress site (e.g., 'https://example.com')
    :param username: WordPress username
    :param app_password: WordPress application password
    :param tag_name: Name of the tag to be created
    :return: ID of the created tag or error message
    """
    api_endpoint = f"{url}/wp-json/wp/v2/tags"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'name': tag_name,
    }
    response = requests.post(api_endpoint, json=data, auth=HTTPBasicAuth(username, app_password), headers=headers)
    
    if response.status_code == 201:
        return response.json().get('id')  # Return the ID of the created tag
    else:
        return response.text


def create_wordpress_category(url, username, app_password, category_name):
    """
    Create a new category in WordPress using the REST API and return its ID.

    :param url: URL of the WordPress site (e.g., 'https://example.com')
    :param username: WordPress username
    :param app_password: WordPress application password
    :param category_name: Name of the category to be created
    :return: ID of the created category or error message
    """
    api_endpoint = f"{url}/wp-json/wp/v2/categories"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'name': category_name,
    }
    response = requests.post(api_endpoint, json=data, auth=HTTPBasicAuth(username, app_password), headers=headers)
    
    if response.status_code == 201:
        return response.json().get('id')  # Return the ID of the created category
    else:
        return response.text


def get_all_wordpress_categories(url, username, password):
    """
    Get all categories from WordPress.

    :param url: URL of the WordPress site
    :param username: WordPress username
    :param password: WordPress application password
    :return: Dictionary of category names and their IDs
    """
    logger.info("Fetching all wordpress categories to create Or use exsiting.")
    categories = {}
    api_endpoint = f"{url}/wp-json/wp/v2/categories"
    response = requests.get(api_endpoint, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        for category in response.json():
            categories[category['name']] = category['id']
        return categories
    else:
        return "Error: " + response.text


def get_all_wordpress_tags(url, username, password):
    """
    Get all tags from WordPress.

    :param url: URL of the WordPress site
    :param username: WordPress username
    :param password: WordPress application password
    :return: Dictionary of tag names and their IDs
    """
    logger.info("Fetching all tags from wordpress to create or use existing tag.")
    tags = {}
    api_endpoint = f"{url}/wp-json/wp/v2/tags"
    response = requests.get(api_endpoint, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        for tag in response.json():
            tags[tag['name']] = tag['id']
        return tags
    else:
        return "Error: " + response.text


def create_or_get_wordpress_category(url, username, password, category_name):
    """
    Create a new category or get existing one from WordPress.

    :param url: URL of the WordPress site
    :param username: WordPress username
    :param password: WordPress application password
    :param category_name: Name of the category
    :return: ID of the category
    """
    existing_categories = get_all_wordpress_categories(url, username, password)
    if category_name in existing_categories:
        return existing_categories[category_name]
    else:
        return create_wordpress_category(url, username, password, category_name)


def create_or_get_wordpress_tag(url, username, password, tag_name):
    """
    Create a new tag or get existing one from WordPress.

    :param url: URL of the WordPress site
    :param username: WordPress username
    :param password: WordPress application password
    :param tag_name: Name of the tag
    :return: ID of the tag
    """
    existing_tags = get_all_wordpress_tags(url, username, password)
    if tag_name in existing_tags:
        return existing_tags[tag_name]
    else:
        return create_wordpress_tag(url, username, password, tag_name)


def upload_media(url, username, password, media_path, alt_text, description, title, caption):
    """
    Upload media to WordPress site with alt text, description, title, and caption.

    :param url: URL of your WordPress site
    :param username: Your WordPress username
    :param password: Your WordPress password
    :param media_path: Path to the media file
    :param alt_text: Alternative text for the image
    :param description: Description of the media
    :param title: Title of the media
    :param caption: Caption for the media
    """
    if not os.path.exists(media_path):
        logger.info(f"File not found: {media_path}")
        return None

    mime_type, _ = mimetypes.guess_type(media_path)
    if mime_type is None:
        logger.info(f"Unable to determine MIME type for the file: {media_path}")
        return None

    credentials = username + ':' + password
    token = base64.b64encode(credentials.encode())
    header = {
        'Authorization': 'Basic ' + token.decode('utf-8'),
        'Content-Disposition': 'attachment; filename={}'.format(os.path.basename(media_path))
    }

    with open(media_path, 'rb', encoding="utf-8") as media:
        media_name = os.path.basename(media_path)
        files = {'file': (media_name, media, mime_type)}

        # Upload the media file
        response = requests.post(url + '/wp-json/wp/v2/media', headers=header, files=files)

        if response.status_code == 201:
            logger.info("Media uploaded successfully.")
            media_id = response.json()['id']

            # Update media with alt text, description, title, and caption
            media_data = {
                'alt_text': alt_text,
                'description': description,
                'title': title,
                'caption': caption
            }

            media_update_response = requests.post(f"{url}/wp-json/wp/v2/media/{media_id}", headers=header, json=media_data)

            if media_update_response.status_code == 200:
                logger.info("Media updated with alt text, description, title, and caption successfully.")
                return media_update_response.json()
            else:
                logger.error("Failed to update media.")
                logger.error(f"Response:{media_update_response.content}")
                return None
        else:
            logger.error("Failed to upload media.")
            logger.error("Response:{response.content}")
            return None



def upload_blog_post(url, username, password, title, content, media_id, meta_desc, categories=None, tags=None, status='draft'):
    """
    Upload a blog post to a WordPress site.
    https://developer.wordpress.org/rest-api/reference/posts/#create-a-post

    :param url: URL of your WordPress site
    :param username: Your WordPress username
    :param password: Your WordPress password
    :param title: Title of the blog post
    :param content: Content of the blog post
    :param media_id: ID of the uploaded media to be set as the featured image
    :param categories: List of category IDs
    :param tags: List of tag IDs
    :param status: Status of the post ('draft', 'publish', etc.)
    """
    credentials = username + ':' + password
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    # Prepare the data for the post
    # https://developer.wordpress.org/rest-api/reference/posts/#schema-meta
    post = {
        'title': title,
        'content': content,
        # One of: publish, future, draft, pending, private
        'status': status,
        'excerpt': meta_desc,
        'featured_media': media_id,
        #'categories': categories,
        #'tags': tags,

        'meta': {
            'description': meta_desc  # This depends on your WordPress setup
        }
    }
    #if categories:
    #    post['categories'] = categories

    # Make the request
    response = requests.post(url + '/wp-json/wp/v2/posts', headers=header, json=post)
    
    # Check response
    if response.status_code == 201:
        logger.info("Blog to wordpress, uploaded successfully.")
        return json.loads(response.content)
    else:
        logger.error("Blog upload to wordpress Failed.")
        logger.error(f"Response: {response.content}")  # Print response content for debugging
        return None
