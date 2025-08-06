"""
Wix Blog Manager

This module provides high-level functions for managing blog content on Wix,
including content creation, SEO optimization, and media management.
"""

import os
import re
import logging
import tempfile
import requests
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
from pathlib import Path
import markdown
import html2text
from bs4 import BeautifulSoup

from .wix_api_client import WixAPIClient

# Configure logging
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('wix_blog_manager')

class WixBlogManager:
"""
High-level manager for Wix blog content.

This class provides convenient methods for common blog management tasks,
building on the lower-level WixAPIClient.
"""

def __init__(
self, 
api_key: Optional[str] = None, 
refresh_token: Optional[str] = None,
site_id: Optional[str] = None
):
"""
Initialize the Wix Blog Manager.

Args:
api_key: Wix API key (optional if using refresh token)
refresh_token: Wix refresh token for OAuth authentication
site_id: Wix site ID
"""
self.client = WixAPIClient(api_key, refresh_token, site_id)

def publish_markdown_post(
self,
title: str,
markdown_content: str,
featured_image_path: Optional[str] = None,
featured_image_url: Optional[str] = None,
excerpt: Optional[str] = None,
tags: Optional[List[str]] = None,
categories: Optional[List[str]] = None,
seo_title: Optional[str] = None,
seo_description: Optional[str] = None,
seo_keywords: Optional[List[str]] = None,
publish: bool = False
) -> Dict:
"""
Publish a blog post from markdown content.

Args:
title: Post title
markdown_content: Post content in markdown format
featured_image_path: Local path to featured image (optional)
featured_image_url: URL of featured image to download (optional)
excerpt: Post excerpt/summary (optional)
tags: List of tags (optional)
categories: List of category names (optional)
seo_title: SEO title (optional)
seo_description: SEO description (optional)
seo_keywords: SEO keywords (optional)
publish: Whether to publish the post immediately (optional)

Returns:
Published blog post data
"""
# Convert markdown to HTML
html_content = self._markdown_to_html(markdown_content)

# Process images in the content
html_content, embedded_images = self._process_content_images(html_content)

# Handle featured image
featured_image_id = None
temp_image_path = None

if featured_image_url and not featured_image_path:
# Download the image from URL
try:
temp_image_path = self._download_image(featured_image_url)
featured_image_path = temp_image_path
except Exception as e:
logger.error(f"Failed to download featured image: {str(e)}")

if featured_image_path:
try:
image_response = self.client.upload_image(
file_path=featured_image_path,
title=title,
alt_text=title
)
featured_image_id = image_response.get("file", {}).get("id")
logger.info(f"Uploaded featured image with ID: {featured_image_id}")
except Exception as e:
logger.error(f"Failed to upload featured image: {str(e)}")

# Clean up temporary file if created
if temp_image_path and os.path.exists(temp_image_path):
try:
os.remove(temp_image_path)
except:
pass

# Process categories - convert names to IDs
category_ids = []
if categories:
for category_name in categories:
try:
category_id = self.client.get_or_create_category(category_name)
if category_id:
category_ids.append(category_id)
except Exception as e:
logger.error(f"Failed to process category '{category_name}': {str(e)}")

# Generate excerpt if not provided
if not excerpt:
excerpt = self._generate_excerpt(markdown_content)

# Prepare SEO data
seo_data = None
if seo_title or seo_description or seo_keywords:
seo_data = {
"title": seo_title or title,
"description": seo_description or excerpt or "",
"keywords": seo_keywords or tags or []
}

# Create the blog post
response = self.client.create_post(
title=title,
content=html_content,
excerpt=excerpt,
featured_image_id=featured_image_id,
tags=tags,
categories=category_ids,
seo_data=seo_data,
publish=publish
)

# Update SEO settings if the post was published
if publish and response.get("post", {}).get("id"):
post_id = response["post"]["id"]
post_url = self.client.get_post_url(post_id)

try:
self.client.update_seo_settings(
page_url=post_url,
title=seo_title or title,
description=seo_description or excerpt or "",
keywords=seo_keywords or tags,
og_image_url=featured_image_url
)
except Exception as e:
logger.error(f"Failed to update SEO settings: {str(e)}")

return response

def update_markdown_post(
self,
post_id: str,
title: Optional[str] = None,
markdown_content: Optional[str] = None,
featured_image_path: Optional[str] = None,
featured_image_url: Optional[str] = None,
excerpt: Optional[str] = None,
tags: Optional[List[str]] = None,
categories: Optional[List[str]] = None,
seo_title: Optional[str] = None,
seo_description: Optional[str] = None,
seo_keywords: Optional[List[str]] = None,
publish: bool = False
) -> Dict:
"""
Update an existing blog post with markdown content.

Args:
post_id: ID of the post to update
title: New post title (optional)
markdown_content: New post content in markdown format (optional)
featured_image_path: Local path to new featured image (optional)
featured_image_url: URL of new featured image to download (optional)
excerpt: New post excerpt/summary (optional)
tags: New list of tags (optional)
categories: New list of category names (optional)
seo_title: New SEO title (optional)
seo_description: New SEO description (optional)
seo_keywords: New SEO keywords (optional)
publish: Whether to publish the post after updating (optional)

Returns:
Updated blog post data
"""
# Get current post data
current_post = self.client.get_post(post_id)
if "post" not in current_post:
raise ValueError(f"Post with ID {post_id} not found")

# Convert markdown to HTML if provided
html_content = None
if markdown_content:
html_content = self._markdown_to_html(markdown_content)
# Process images in the content
html_content, embedded_images = self._process_content_images(html_content)

# Handle featured image
featured_image_id = None
temp_image_path = None

if featured_image_url and not featured_image_path:
# Download the image from URL
try:
temp_image_path = self._download_image(featured_image_url)
featured_image_path = temp_image_path
except Exception as e:
logger.error(f"Failed to download featured image: {str(e)}")

if featured_image_path:
try:
image_response = self.client.upload_image(
file_path=featured_image_path,
title=title or current_post["post"].get("title", ""),
alt_text=title or current_post["post"].get("title", "")
)
featured_image_id = image_response.get("file", {}).get("id")
logger.info(f"Uploaded featured image with ID: {featured_image_id}")
except Exception as e:
logger.error(f"Failed to upload featured image: {str(e)}")

# Clean up temporary file if created
if temp_image_path and os.path.exists(temp_image_path):
try:
os.remove(temp_image_path)
except:
pass

# Process categories - convert names to IDs
category_ids = None
if categories:
category_ids = []
for category_name in categories:
try:
category_id = self.client.get_or_create_category(category_name)
if category_id:
category_ids.append(category_id)
except Exception as e:
logger.error(f"Failed to process category '{category_name}': {str(e)}")

# Generate excerpt if not provided but markdown is
if not excerpt and markdown_content:
excerpt = self._generate_excerpt(markdown_content)

# Prepare SEO data
seo_data = None
if seo_title or seo_description or seo_keywords:
seo_data = {
"title": seo_title or title or current_post["post"].get("title", ""),
"description": seo_description or excerpt or current_post["post"].get("excerpt", ""),
"keywords": seo_keywords or tags or current_post["post"].get("tags", [])
}

# Update the blog post
response = self.client.update_post(
post_id=post_id,
title=title,
content=html_content,
excerpt=excerpt,
featured_image_id=featured_image_id,
tags=tags,
categories=category_ids,
seo_data=seo_data,
publish=publish
)

# Update SEO settings if needed
if (seo_title or seo_description or seo_keywords or featured_image_url):
post_url = self.client.get_post_url(post_id)

try:
self.client.update_seo_settings(
page_url=post_url,
title=seo_title or title,
description=seo_description or excerpt,
keywords=seo_keywords or tags,
og_image_url=featured_image_url
)
except Exception as e:
logger.error(f"Failed to update SEO settings: {str(e)}")

return response

def find_post_by_title(self, title: str) -> Optional[Dict]:
"""
Find a post by its title (exact match).

Args:
title: Post title to search for

Returns:
Post data or None if not found
"""
# List all posts (this is inefficient but Wix API doesn't support filtering by title)
# In a production environment, you might want to implement pagination
response = self.client.list_posts(limit=100)
posts = response.get("posts", [])

for post in posts:
if post.get("title") == title:
return post

return None

def publish_or_update_markdown_post(
self,
title: str,
markdown_content: str,
featured_image_path: Optional[str] = None,
featured_image_url: Optional[str] = None,
excerpt: Optional[str] = None,
tags: Optional[List[str]] = None,
categories: Optional[List[str]] = None,
seo_title: Optional[str] = None,
seo_description: Optional[str] = None,
seo_keywords: Optional[List[str]] = None,
publish: bool = False,
update_if_exists: bool = True
) -> Dict:
"""
Publish a new post or update an existing one with the same title.

Args:
title: Post title
markdown_content: Post content in markdown format
featured_image_path: Local path to featured image (optional)
featured_image_url: URL of featured image to download (optional)
excerpt: Post excerpt/summary (optional)
tags: List of tags (optional)
categories: List of category names (optional)
seo_title: SEO title (optional)
seo_description: SEO description (optional)
seo_keywords: SEO keywords (optional)
publish: Whether to publish the post immediately (optional)
update_if_exists: Whether to update an existing post with the same title (optional)

Returns:
Published or updated blog post data
"""
# Check if a post with this title already exists
existing_post = self.find_post_by_title(title)

if existing_post and update_if_exists:
# Update existing post
logger.info(f"Updating existing post with title: {title}")
return self.update_markdown_post(
post_id=existing_post["id"],
title=title,
markdown_content=markdown_content,
featured_image_path=featured_image_path,
featured_image_url=featured_image_url,
excerpt=excerpt,
tags=tags,
categories=categories,
seo_title=seo_title,
seo_description=seo_description,
seo_keywords=seo_keywords,
publish=publish
)
else:
# Create new post
logger.info(f"Creating new post with title: {title}")
return self.publish_markdown_post(
title=title,
markdown_content=markdown_content,
featured_image_path=featured_image_path,
featured_image_url=featured_image_url,
excerpt=excerpt,
tags=tags,
categories=categories,
seo_title=seo_title,
seo_description=seo_description,
seo_keywords=seo_keywords,
publish=publish
)

def optimize_seo_for_post(
self,
post_id: str,
seo_title: Optional[str] = None,
seo_description: Optional[str] = None,
seo_keywords: Optional[List[str]] = None,
og_image_url: Optional[str] = None,
structured_data: Optional[Dict] = None
) -> Dict:
"""
Optimize SEO settings for an existing blog post.

Args:
post_id: ID of the blog post
seo_title: SEO title (optional)
seo_description: SEO description (optional)
seo_keywords: SEO keywords (optional)
og_image_url: Open Graph image URL (optional)
structured_data: Structured data (JSON-LD) (optional)

Returns:
Updated SEO settings data
"""
# Get the post URL
post_url = self.client.get_post_url(post_id)

# Update SEO settings
return self.client.update_seo_settings(
page_url=post_url,
title=seo_title,
description=seo_description,
keywords=seo_keywords,
og_image_url=og_image_url,
structured_data=structured_data
)

def generate_structured_data(
self,
post_id: str,
author_name: str,
publisher_name: str,
publisher_logo_url: str
) -> Dict:
"""
Generate structured data (JSON-LD) for a blog post.

Args:
post_id: ID of the blog post
author_name: Name of the author
publisher_name: Name of the publisher
publisher_logo_url: URL of the publisher's logo

Returns:
Structured data as a dictionary
"""
# Get post data
post_data = self.client.get_post(post_id)
post = post_data.get("post", {})

# Get post URL
post_url = self.client.get_post_url(post_id)

# Create structured data
structured_data = {
"@context": "https://schema.org",
"@type": "BlogPosting",
"headline": post.get("title", ""),
"description": post.get("excerpt", ""),
"author": {
"@type": "Person",
"name": author_name
},
"publisher": {
"@type": "Organization",
"name": publisher_name,
"logo": {
"@type": "ImageObject",
"url": publisher_logo_url
}
},
"datePublished": post.get("publishedDate", ""),
"dateModified": post.get("lastPublishedDate", "")
}

# Add featured image if available
if post.get("featuredImageId"):
try:
media_item = self.client.get_media_item(post["featuredImageId"])
image_url = media_item.get("file", {}).get("url", "")
if image_url:
structured_data["image"] = image_url
except:
pass

return structured_data

def apply_structured_data_to_post(
self,
post_id: str,
author_name: str,
publisher_name: str,
publisher_logo_url: str
) -> Dict:
"""
Generate and apply structured data to a blog post.

Args:
post_id: ID of the blog post
author_name: Name of the author
publisher_name: Name of the publisher
publisher_logo_url: URL of the publisher's logo

Returns:
Updated SEO settings data
"""
# Generate structured data
structured_data = self.generate_structured_data(
post_id=post_id,
author_name=author_name,
publisher_name=publisher_name,
publisher_logo_url=publisher_logo_url
)

# Get the post URL
post_url = self.client.get_post_url(post_id)

# Update SEO settings with structured data
return self.client.update_seo_settings(
page_url=post_url,
structured_data=structured_data
)

# Helper methods

def _markdown_to_html(self, markdown_content: str) -> str:
"""
Convert markdown content to HTML.

Args:
markdown_content: Content in markdown format

Returns:
HTML content
"""
# Use the markdown library to convert to HTML
html = markdown.markdown(
markdown_content,
extensions=['extra', 'codehilite', 'tables', 'toc']
)

return html

def _html_to_markdown(self, html_content: str) -> str:
"""
Convert HTML content to markdown.

Args:
html_content: Content in HTML format

Returns:
Markdown content
"""
# Use html2text to convert HTML to markdown
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
h.ignore_tables = False
h.ignore_emphasis = False

return h.handle(html_content)

def _process_content_images(self, html_content: str) -> Tuple[str, List[Dict]]:
"""
Process images in HTML content, uploading them to Wix and replacing URLs.

Args:
html_content: HTML content with image tags

Returns:
Tuple of (updated HTML content, list of uploaded image data)
"""
soup = BeautifulSoup(html_content, 'html.parser')
img_tags = soup.find_all('img')
uploaded_images = []

for img in img_tags:
src = img.get('src', '')
alt = img.get('alt', '')

# Skip images that are already hosted on Wix
if 'wixstatic.com' in src:
continue

# Handle images with data URLs
if src.startswith('data:image'):
logger.info("Skipping data URL image - not supported in this implementation")
continue

# Handle remote images
if src.startswith('http://') or src.startswith('https://'):
try:
# Download the image
temp_path = self._download_image(src)

# Upload to Wix
image_response = self.client.upload_image(
file_path=temp_path,
title=alt or "Blog image",
alt_text=alt or "Blog image"
)

# Get the new URL
new_url = image_response.get("file", {}).get("url", "")

if new_url:
# Replace the src attribute
img['src'] = new_url
uploaded_images.append({
'original_url': src,
'wix_url': new_url,
'wix_id': image_response.get("file", {}).get("id", "")
})

# Clean up temp file
if os.path.exists(temp_path):
os.remove(temp_path)

except Exception as e:
logger.error(f"Failed to process image {src}: {str(e)}")

# Handle local images (not implemented in this version)
else:
logger.info(f"Skipping local image {src} - not supported in this implementation")

# Return the updated HTML
return str(soup), uploaded_images

def _download_image(self, url: str) -> str:
"""
Download an image from a URL to a temporary file.

Args:
url: URL of the image

Returns:
Path to the downloaded temporary file
"""
response = requests.get(url, stream=True)
response.raise_for_status()

# Determine file extension
content_type = response.headers.get('content-type', '')
extension = '.jpg'  # Default

if 'image/jpeg' in content_type:
extension = '.jpg'
elif 'image/png' in content_type:
extension = '.png'
elif 'image/gif' in content_type:
extension = '.gif'
elif 'image/webp' in content_type:
extension = '.webp'

# Create a temporary file
fd, temp_path = tempfile.mkstemp(suffix=extension)
os.close(fd)

# Write the image data to the file
with open(temp_path, 'wb') as f:
for chunk in response.iter_content(chunk_size=8192):
f.write(chunk)

return temp_path

def _generate_excerpt(self, markdown_content: str, max_length: int = 160) -> str:
"""
Generate an excerpt from markdown content.

Args:
markdown_content: Content in markdown format
max_length: Maximum length of the excerpt

Returns:
Generated excerpt
"""
# Convert markdown to plain text
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.ignore_tables = True
h.ignore_emphasis = True

# First convert markdown to HTML, then HTML to plain text
html = markdown.markdown(markdown_content)
plain_text = h.handle(html)

# Clean up the text
plain_text = re.sub(r'\s+', ' ', plain_text).strip()

# Truncate to max_length
if len(plain_text) <= max_length:
return plain_text

# Try to truncate at a sentence boundary
sentences = re.split(r'(?<=[.!?])\s+', plain_text)
excerpt = ""

for sentence in sentences:
if len(excerpt + sentence) <= max_length:
excerpt += sentence + " "
else:
break

# If we couldn't get a full sentence, just truncate
if not excerpt:
excerpt = plain_text[:max_length-3] + "..."

return excerpt.strip()
