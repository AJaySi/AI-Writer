import requests
import json
import os

class WixAPI:
    def __init__(self, api_key, site_id):
        self.api_key = api_key
        self.site_id = site_id
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def upload_blog(self, blog_title, blog_content, blog_image=None):
        """Uploads a blog to a Wix website.

        Args:
            blog_title: The title of the blog.
            blog_content: The content of the blog.
            blog_image: The image for the blog (optional).

        Returns:
            The ID of the uploaded blog.
        """

        response = requests.post(
            f"https://www.wix.com/api/v1/sites/{self.site_id}/blogs",
            headers=self.headers,
            json={
                "title": blog_title,
                "content": blog_content,
                "image": blog_image
            }
        )

        if response.status_code == 201:
            return json.loads(response.content)["id"]
        else:
            raise Exception(f"Failed to upload blog: {response.status_code}")

def upload_blogs(wix_api, local_directory):
    """Uploads all blogs from a local directory to a Wix website.

    Args:
        wix_api: A WixAPI object.
        local_directory: The local directory containing the blogs.
    """

    for blog_file in os.listdir(local_directory):
        blog_path = os.path.join(local_directory, blog_file)

        # Read the blog content from the file.
        with open(blog_path, "r") as f:
            blog_content = f.read()

        # Get the blog title from the file name.
        blog_title = blog_file.split(".")[0]

        # Upload the blog to the Wix website.
        blog_id = wix_api.upload_blog(blog_title, blog_content)

        print(f"Uploaded blog {blog_title} with ID {blog_id}")

if __name__ == "__main__":
    # Get the Wix API key.
    wix_api_key = "IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjk3MDFlNTlhLTJlNmEtNDVhMy1hYmU2LWQ0ZWMxMWI4YWFhY1wiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNjYmI5OWQxLTk1ZmYtNGRmZC1iNGIxLTYwOWRmNWExNmUwN1wifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCJhNTZiYTM1Zi02NDUzLTQxMDAtYWM1ZC1lM2M4OGU4YTdjN2RcIn19IiwiaWF0IjoxNjk2NjY4MDE1fQ.XhR3cBfxXhjRIeRL28Y7x0lG7o3pN6Cibpe50rN2saJRxFGyVcQGpWt6R_RnyMaBXQrxyKQcLjpTTSxmdnC6Myby1oCFAHuOpmUoGnYz634J_Epfc2BdwnA2SbnvAEktbOoFhIlMf7is2Xt89bE-h7LUPIejGHdCUucv_F1n6gBY6Bl0KxQhA_9k7M92bKr_mvoncDwTPVoeI_CL6fsQZ19tWzSDfe-DvornEIPId-Pp8Gh-lx9LmyhWepQDxpDDXEtlCEEeWvTB8_6ohOC_Jc2gSp8pw7uEawmoAaaqRKsLPBHFjrdgddKJ9jesWWMXxUGWcvJtBtoB3bZypgJSkQ"

    # Get the Wix site ID.
    wix_site_id = "a56ba35f-6453-4100-ac5d-e3c88e8a7c7d"

    # Create a WixAPI object.
    wix_api = WixAPI(wix_api_key, wix_site_id)

    # Get the local directory containing the blogs.
    local_directory = "/home/ajsingh/pseo_experiments/lib/webhosting_integrations"

    # Upload all blogs from the local directory to the Wix website.
    upload_blogs(wix_api, local_directory)

