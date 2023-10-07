import requests
import json


def upload_blog_post(wordpress_site_url, wordpress_username, wordpress_password, blog_post_title, blog_post_content, blog_post_image_url=None):
    """
    Uploads a blog post to a WordPress website.

    Args:
        wordpress_site_url: The URL of the WordPress website.
        wordpress_username: The username for the WordPress website.
        wordpress_password: The password for the WordPress website.
        blog_post_title: The title of the blog post.
        blog_post_content: The content of the blog post.
        blog_post_image_url: The URL of the blog post image.

    Returns:
        None.
    """

    # Get the WordPress authentication token.
    wordpress_auth_token = get_wordpress_auth_token(wordpress_site_url, wordpress_username, wordpress_password)

    # Create the request body.
    request_body = {
        "title": blog_post_title,
        "content": blog_post_content
    }

    # If a blog post image URL is provided, add it to the request body.
    if blog_post_image_url:
        request_body["featured_media"] = blog_post_image_url

    # Make the request to the WordPress API.
    try:
        response = requests.post(
            f"{wordpress_site_url}/wp-json/wp/v2/posts",
            headers={"Authorization": f"Bearer {wordpress_auth_token}"},
            json=request_body
        )
    except Exception as e:
        raise e

    # Check the response status code.
    if response.status_code != 201:
        raise Exception(f"Failed to upload blog post: {response.status_code}")

    # Print a success message.
    print("Blog post uploaded successfully!")


def get_wordpress_auth_token(wordpress_site_url, wordpress_username, wordpress_password):
    """
    Gets the WordPress authentication token.

    Args:
        wordpress_site_url: The URL of the WordPress website.
        wordpress_username: The username for the WordPress website.
        wordpress_password: The password for the WordPress website.

    Returns:
        A string containing the WordPress authentication token.
    """

    # Create the request body.
    request_body = {
        "username": wordpress_username,
        "password": wordpress_password
    }

    # Make the request to the WordPress API.
    try:
        response = requests.post(
            f"{wordpress_site_url}/wp-json/jwt-auth/v1/token",
            json=request_body
        )
    except Exception as e:
        raise e

    # Check the response status code.
    if response.status_code != 200:
        raise Exception(f"Failed to get WordPress authentication token: {response.status_code}")

    # Return the WordPress authentication token.
    return response.json()["token"]


# Sample usage:

# Get the WordPress site URL, username, and password.
wordpress_site_url = "https://example.com"
wordpress_username = "YOUR_WORDPRESS_USERNAME"
wordpress_password = "YOUR_WORDPRESS_PASSWORD"

# Upload the blog post.
try:
    upload_blog_post(wordpress_site_url, wordpress_username, wordpress_password,
                     "My first blog post", "This is my first blog post.")
except Exception as e:
    print(e)

