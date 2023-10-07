import requests
import json

def upload_blog_post(wix_site_id, wix_api_key, blog_post_title, blog_post_content):
    """ Uploads a blog post to a Wix website.

    Args:
        wix_site_id: The ID of the Wix website.
        wix_api_key: The API key for the Wix website.
        blog_post_title: The title of the blog post.
        blog_post_content: The content of the blog post.

    Returns:
        None.
    """

    # Create the request body.
    request_body = {
        "title": blog_post_title,
        "content": blog_post_content
    }

    # Make the request to the Wix API.
    response = requests.post(
        f"https://{wix_site_id}.wixsite.com/api/v1/blog/posts",
        headers={"Authorization": f"Bearer {wix_api_key}"},
        json=request_body
    )

    # Check the response status code.
    if response.status_code != 200:
        raise Exception(f"Failed to upload blog post: {response.status_code}")

    # Print a success message.
    print("Blog post uploaded successfully!")



###########################################################################################
# Example usage:
wix_site_id = "1234567890"
wix_api_key = "YOUR_WIX_API_KEY"
blog_post_title = "My first blog post"
blog_post_content = "This is my first blog post."


upload_blog_post(wix_site_id, wix_api_key, blog_post_title, blog_post_content)

