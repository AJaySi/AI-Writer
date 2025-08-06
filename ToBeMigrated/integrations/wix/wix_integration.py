"""
Wix Integration for Alwrity

This module provides a high-level interface for integrating Wix blog functionality
with the Alwrity AI Writer platform.
"""

import os
import logging
import json
from typing import Dict, List, Optional, Union, Any, Tuple
from pathlib import Path

from .wix_api_client import WixAPIClient
from .wix_blog_manager import WixBlogManager
from .wix_seo_optimizer import WixSEOOptimizer

# Configure logging
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('wix_integration')

class WixIntegration:
"""
Main integration class for Wix blog functionality.

This class provides a simplified interface for common operations,
combining the functionality of the API client, blog manager, and SEO optimizer.
"""

def __init__(
self, 
api_key: Optional[str] = None, 
refresh_token: Optional[str] = None,
site_id: Optional[str] = None
):
"""
Initialize the Wix Integration.

Args:
api_key: Wix API key (optional if using refresh token)
refresh_token: Wix refresh token for OAuth authentication
site_id: Wix site ID
"""
self.api_client = WixAPIClient(api_key, refresh_token, site_id)
self.blog_manager = WixBlogManager(api_key, refresh_token, site_id)
self.seo_optimizer = WixSEOOptimizer(api_key, refresh_token, site_id)

def publish_blog_post(
self,
title: str,
content: str,
is_markdown: bool = True,
featured_image_path: Optional[str] = None,
featured_image_url: Optional[str] = None,
excerpt: Optional[str] = None,
tags: Optional[List[str]] = None,
categories: Optional[List[str]] = None,
seo_title: Optional[str] = None,
seo_description: Optional[str] = None,
seo_keywords: Optional[List[str]] = None,
author_name: Optional[str] = None,
publisher_name: Optional[str] = None,
publisher_logo_url: Optional[str] = None,
publish: bool = True,
update_if_exists: bool = True
) -> Dict:
"""
Publish a blog post with comprehensive SEO optimization.

Args:
title: Post title
content: Post content (markdown or HTML)
is_markdown: Whether the content is in markdown format
featured_image_path: Local path to featured image (optional)
featured_image_url: URL of featured image to download (optional)
excerpt: Post excerpt/summary (optional)
tags: List of tags (optional)
categories: List of category names (optional)
seo_title: SEO title (optional)
seo_description: SEO description (optional)
seo_keywords: SEO keywords (optional)
author_name: Name of the author (optional)
publisher_name: Name of the publisher (optional)
publisher_logo_url: URL of the publisher's logo (optional)
publish: Whether to publish the post immediately (optional)
update_if_exists: Whether to update an existing post with the same title (optional)

Returns:
Published blog post data
"""
# Generate SEO data if not provided
if not seo_keywords and tags:
seo_keywords = tags

if not seo_title:
seo_title = title

if not seo_description and not excerpt:
if is_markdown:
# Generate description from markdown content
seo_description = self.blog_manager._generate_excerpt(content)
else:
# Generate description from HTML content
seo_description = self.seo_optimizer.generate_meta_description(content)
elif not seo_description:
seo_description = excerpt

# Publish or update the post
if is_markdown:
response = self.blog_manager.publish_or_update_markdown_post(
title=title,
markdown_content=content,
featured_image_path=featured_image_path,
featured_image_url=featured_image_url,
excerpt=excerpt,
tags=tags,
categories=categories,
seo_title=seo_title,
seo_description=seo_description,
seo_keywords=seo_keywords,
publish=publish,
update_if_exists=update_if_exists
)
else:
# Find existing post or create new one
existing_post = self.blog_manager.find_post_by_title(title)

if existing_post and update_if_exists:
# Update existing post
response = self.api_client.update_post(
post_id=existing_post["id"],
title=title,
content=content,
excerpt=excerpt,
tags=tags,
categories=[self.api_client.get_or_create_category(cat) for cat in categories] if categories else None,
seo_data={
"title": seo_title,
"description": seo_description,
"keywords": seo_keywords or []
},
publish=publish
)
else:
# Create new post
response = self.api_client.create_post(
title=title,
content=content,
excerpt=excerpt,
tags=tags,
categories=[self.api_client.get_or_create_category(cat) for cat in categories] if categories else None,
seo_data={
"title": seo_title,
"description": seo_description,
"keywords": seo_keywords or []
},
publish=publish
)

# Apply additional SEO optimization if the post was published
if publish and response.get("post", {}).get("id"):
post_id = response["post"]["id"]

# Apply structured data if author and publisher info is provided
if author_name and publisher_name and publisher_logo_url:
try:
self.seo_optimizer.apply_structured_data_to_post(
post_id=post_id,
author_name=author_name,
publisher_name=publisher_name,
publisher_logo_url=publisher_logo_url
)
except Exception as e:
logger.error(f"Failed to apply structured data: {str(e)}")

# Apply comprehensive SEO optimization
try:
self.seo_optimizer.apply_seo_optimization(
post_id=post_id,
title=seo_title,
description=seo_description,
keywords=seo_keywords,
author_name=author_name,
publisher_name=publisher_name,
publisher_logo_url=publisher_logo_url,
og_image_url=featured_image_url
)
except Exception as e:
logger.error(f"Failed to apply SEO optimization: {str(e)}")

return response

def upload_media(
self,
file_path: str,
title: Optional[str] = None,
alt_text: Optional[str] = None,
description: Optional[str] = None
) -> Dict:
"""
Upload a media file to Wix.

Args:
file_path: Path to the media file
title: Media title (optional)
alt_text: Media alt text (optional)
description: Media description (optional)

Returns:
Uploaded media data
"""
return self.api_client.upload_image(
file_path=file_path,
title=title,
alt_text=alt_text,
description=description
)

def get_seo_report(self, post_id: str, target_keywords: List[str]) -> Dict:
"""
Generate a comprehensive SEO report for a blog post.

Args:
post_id: ID of the blog post
target_keywords: List of target keywords

Returns:
Dictionary with SEO report data
"""
return self.seo_optimizer.generate_seo_report(post_id, target_keywords)

def list_blog_posts(
self,
limit: int = 50,
offset: int = 0,
sort_field: str = "lastPublishedDate",
sort_order: str = "desc"
) -> Dict:
"""
List blog posts with pagination and sorting.

Args:
limit: Maximum number of posts to return (default: 50)
offset: Pagination offset (default: 0)
sort_field: Field to sort by (default: lastPublishedDate)
sort_order: Sort order, 'asc' or 'desc' (default: desc)

Returns:
Dictionary containing blog posts and pagination info
"""
return self.api_client.list_posts(
limit=limit,
offset=offset,
sort_field=sort_field,
sort_order=sort_order
)

def list_categories(self) -> Dict:
"""
List all blog categories.

Returns:
Dictionary containing blog categories
"""
return self.api_client.list_categories()

def create_category(self, name: str, description: Optional[str] = None) -> str:
"""
Create a new blog category.

Args:
name: Category name
description: Category description (optional)

Returns:
ID of the created category
"""
response = self.api_client.create_category(
label=name,
description=description
)
return response.get("category", {}).get("id", "")

def get_post_by_id(self, post_id: str) -> Dict:
"""
Get a blog post by ID.

Args:
post_id: ID of the blog post

Returns:
Blog post data
"""
return self.api_client.get_post(post_id)

def get_post_by_title(self, title: str) -> Optional[Dict]:
"""
Get a blog post by title.

Args:
title: Title of the blog post

Returns:
Blog post data or None if not found
"""
return self.blog_manager.find_post_by_title(title)

def delete_post(self, post_id: str) -> Dict:
"""
Delete a blog post.

Args:
post_id: ID of the blog post

Returns:
Response data
"""
return self.api_client.delete_post(post_id)

def update_post_status(self, post_id: str, publish: bool = True) -> Dict:
"""
Update the publication status of a blog post.

Args:
post_id: ID of the blog post
publish: Whether to publish (True) or unpublish (False) the post

Returns:
Updated blog post data
"""
if publish:
return self.api_client.publish_post(post_id)
else:
return self.api_client.unpublish_post(post_id)

def search_posts(self, query: str, limit: int = 10) -> List[Dict]:
"""
Search for blog posts by content or title.

Args:
query: Search query
limit: Maximum number of results to return

Returns:
List of matching blog posts
"""
# First try to find by title
title_matches = []
try:
all_posts = self.list_blog_posts(limit=100)["posts"]
for post in all_posts:
if query.lower() in post.get("title", "").lower():
title_matches.append(post)
if len(title_matches) >= limit:
break
except Exception as e:
logger.error(f"Error searching posts by title: {str(e)}")

return title_matches[:limit]

def get_site_info(self) -> Dict:
"""
Get information about the Wix site.

Returns:
Dictionary with site information
"""
try:
# Make a simple API call to verify credentials and get site info
posts = self.list_blog_posts(limit=1)
categories = self.list_categories()

return {
"site_id": self.api_client.site_id,
"post_count": posts.get("totalCount", 0),
"category_count": len(categories.get("categories", [])),
"status": "connected"
}
except Exception as e:
logger.error(f"Error getting site info: {str(e)}")
return {
"site_id": self.api_client.site_id,
"status": "error",
"error": str(e)
}