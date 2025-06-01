"""
Wix API Client for Blog Management

This module provides a comprehensive client for interacting with the Wix API
to manage blog posts, SEO settings, and media uploads.

Documentation: https://dev.wix.com/api/rest/getting-started
"""

import os
import json
import time
import logging
import requests
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
import mimetypes
from pathlib import Path
from io import BytesIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('wix_api_client')

class WixAPIClient:
    """
    Client for interacting with the Wix API for blog management.

    This client handles authentication, blog post creation/updating,
    media uploads, and SEO settings.
    """

    # Base URLs for different Wix API endpoints
    BASE_URL = "https://www.wixapis.com"
    OAUTH_URL = "https://www.wix.com/oauth"

    # API Endpoints
    BLOG_API = "/blog/v3"
    MEDIA_API = "/site-media/v1"
    SEO_API = "/site-properties/v4/seo"

    def __init__(
        self, 
        api_key: Optional[str] = None, 
        refresh_token: Optional[str] = None,
        site_id: Optional[str] = None
    ):
        """
        Initialize the Wix API Client.

        Args:
            api_key: Wix API key (optional if using refresh token)
            refresh_token: Wix refresh token for OAuth authentication
            site_id: Wix site ID
        """
        self.api_key = api_key or os.environ.get('WIX_API_KEY')
        self.refresh_token = refresh_token or os.environ.get('WIX_REFRESH_TOKEN')
        self.site_id = site_id or os.environ.get('WIX_SITE_ID')
        self.access_token = None
        self.token_expiry = 0

        if not self.refresh_token:
            logger.warning("No refresh token provided. Authentication will fail.")

        if not self.site_id:
            logger.warning("No site ID provided. API calls will fail.")

    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers required for API requests.

        Returns:
            Dict containing the necessary headers for Wix API requests
        """
        # Ensure we have a valid access token
        self._ensure_valid_token()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "wix-site-id": self.site_id,
            "Content-Type": "application/json"
        }

        return headers

    def _ensure_valid_token(self) -> None:
        """
        Ensure we have a valid access token, refreshing if necessary.
        """
        current_time = time.time()

        # If token is expired or doesn't exist, refresh it
        if not self.access_token or current_time >= self.token_expiry:
            self._refresh_access_token()

    def _refresh_access_token(self) -> None:
        """
        Refresh the access token using the refresh token.
        """
        if not self.refresh_token:
            raise ValueError("Refresh token is required for authentication")

        url = f"{self.OAUTH_URL}/access"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.api_key if self.api_key else ""
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()

            data = response.json()
            self.access_token = data.get("access_token")

            # Set token expiry (subtract 5 minutes for safety margin)
            expires_in = data.get("expires_in", 3600)  # Default to 1 hour if not specified
            self.token_expiry = time.time() + expires_in - 300

            logger.info("Successfully refreshed access token")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to refresh access token: {str(e)}")
            if response.text:
                logger.error(f"Response: {response.text}")
            raise

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None, 
        params: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> Dict:
        """
        Make a request to the Wix API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request payload
            params: Query parameters
            files: Files to upload

        Returns:
            Response data as dictionary
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()

        # If we're uploading files, remove the Content-Type header
        if files:
            headers.pop("Content-Type", None)

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                files=files
            )

            # Log request details for debugging
            logger.debug(f"Request: {method} {url}")
            logger.debug(f"Headers: {headers}")
            if data:
                logger.debug(f"Data: {json.dumps(data)}")
            if params:
                logger.debug(f"Params: {params}")

            # Handle response
            response.raise_for_status()

            if response.content:
                return response.json()
            return {}

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {str(e)}")
            if response.text:
                logger.error(f"Response: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise

    def list_posts(
        self, 
        limit: int = 50, 
        offset: int = 0, 
        sort_field: str = "lastPublishedDate", 
        sort_order: str = "desc",
        filter_by: Optional[Dict] = None
    ) -> Dict:
        """
        List blog posts with pagination and sorting.

        Args:
            limit: Maximum number of posts to return (default: 50)
            offset: Pagination offset (default: 0)
            sort_field: Field to sort by (default: lastPublishedDate)
            sort_order: Sort order, 'asc' or 'desc' (default: desc)
            filter_by: Optional filter criteria

        Returns:
            Dictionary containing blog posts and pagination info
        """
        endpoint = f"{self.BLOG_API}/posts/query"

        payload = {
            "limit": limit,
            "offset": offset,
            "sort": [
                {
                    "fieldName": sort_field,
                    "order": sort_order
                }
            ]
        }

        if filter_by:
            payload["filter"] = filter_by

        return self._make_request("POST", endpoint, data=payload)

    def get_post(self, post_id: str) -> Dict:
        """
        Get a specific blog post by ID.

        Args:
            post_id: ID of the blog post

        Returns:
            Blog post data
        """
        endpoint = f"{self.BLOG_API}/posts/{post_id}"
        return self._make_request("GET", endpoint)

    def create_post(
        self, 
        title: str, 
        content: str, 
        excerpt: Optional[str] = None,
        featured_image_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        seo_data: Optional[Dict] = None,
        publish: bool = False
    ) -> Dict:
        """
        Create a new blog post.

        Args:
            title: Post title
            content: Post content (HTML)
            excerpt: Post excerpt/summary
            featured_image_id: ID of the featured image (from media manager)
            tags: List of tags
            categories: List of category IDs
            seo_data: SEO settings for the post
            publish: Whether to publish the post immediately

        Returns:
            Created blog post data
        """
        endpoint = f"{self.BLOG_API}/posts"

        # Prepare the post data
        post_data = {
            "post": {
                "title": title,
                "content": content,
                "excerpt": excerpt or "",
                "featured_image_id": featured_image_id,
                "tags": tags or [],
                "categoryIds": categories or []
            }
        }

        # Add SEO data if provided
        if seo_data:
            post_data["post"]["seoData"] = seo_data

        # Create the post
        response = self._make_request("POST", endpoint, data=post_data)

        # Publish the post if requested
        if publish and response.get("post", {}).get("id"):
            post_id = response["post"]["id"]
            self.publish_post(post_id)
            # Refresh the post data to get the published version
            response = self.get_post(post_id)

        return response

    def update_post(
        self, 
        post_id: str, 
        title: Optional[str] = None, 
        content: Optional[str] = None,
        excerpt: Optional[str] = None,
        featured_image_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        seo_data: Optional[Dict] = None,
        publish: bool = False
    ) -> Dict:
        """
        Update an existing blog post.

        Args:
            post_id: ID of the post to update
            title: New post title (optional)
            content: New post content (HTML) (optional)
            excerpt: New post excerpt/summary (optional)
            featured_image_id: New featured image ID (optional)
            tags: New list of tags (optional)
            categories: New list of category IDs (optional)
            seo_data: New SEO settings (optional)
            publish: Whether to publish the post after updating

        Returns:
            Updated blog post data
        """
        # First, get the current post data
        current_post = self.get_post(post_id)

        if "post" not in current_post:
            raise ValueError(f"Post with ID {post_id} not found")

        current_post_data = current_post["post"]

        # Update only the fields that were provided
        update_data = {
            "post": {
                "id": post_id,
                "title": title if title is not None else current_post_data.get("title", ""),
                "content": content if content is not None else current_post_data.get("content", ""),
                "excerpt": excerpt if excerpt is not None else current_post_data.get("excerpt", ""),
                "featured_image_id": featured_image_id if featured_image_id is not None else current_post_data.get("featuredImageId"),
                "tags": tags if tags is not None else current_post_data.get("tags", []),
                "categoryIds": categories if categories is not None else current_post_data.get("categoryIds", [])
            }
        }

        # Add SEO data if provided
        if seo_data:
            update_data["post"]["seoData"] = seo_data
        elif "seoData" in current_post_data:
            update_data["post"]["seoData"] = current_post_data["seoData"]

        # Update the post
        endpoint = f"{self.BLOG_API}/posts/{post_id}"
        response = self._make_request("PATCH", endpoint, data=update_data)

        # Publish the post if requested
        if publish:
            self.publish_post(post_id)
            # Refresh the post data to get the published version
            response = self.get_post(post_id)

        return response

    def delete_post(self, post_id: str) -> Dict:
        """
        Delete a blog post.

        Args:
            post_id: ID of the post to delete

        Returns:
            Response data
        """
        endpoint = f"{self.BLOG_API}/posts/{post_id}"
        return self._make_request("DELETE", endpoint)

    def publish_post(self, post_id: str) -> Dict:
        """
        Publish a draft blog post.

        Args:
            post_id: ID of the post to publish

        Returns:
            Published post data
        """
        endpoint = f"{self.BLOG_API}/posts/{post_id}/publish"
        return self._make_request("POST", endpoint)

    def unpublish_post(self, post_id: str) -> Dict:
        """
        Unpublish a published blog post (revert to draft).

        Args:
            post_id: ID of the post to unpublish

        Returns:
            Unpublished post data
        """
        endpoint = f"{self.BLOG_API}/posts/{post_id}/unpublish"
        return self._make_request("POST", endpoint)

    def list_categories(self) -> Dict:
        """
        List all blog categories.

        Returns:
            Dictionary containing blog categories
        """
        endpoint = f"{self.BLOG_API}/categories"
        return self._make_request("GET", endpoint)

    def create_category(self, label: str, description: Optional[str] = None) -> Dict:
        """
        Create a new blog category.

        Args:
            label: Category name
            description: Category description (optional)

        Returns:
            Created category data
        """
        endpoint = f"{self.BLOG_API}/categories"

        payload = {
            "category": {
                "label": label,
                "description": description or ""
            }
        }

        return self._make_request("POST", endpoint, data=payload)

    def update_category(
        self, 
        category_id: str, 
        label: Optional[str] = None, 
        description: Optional[str] = None
    ) -> Dict:
        """
        Update an existing blog category.

        Args:
            category_id: ID of the category to update
            label: New category name (optional)
            description: New category description (optional)

        Returns:
            Updated category data
        """
        # First, get the current category data
        current_categories = self.list_categories()

        current_category = None
        for category in current_categories.get("categories", []):
            if category.get("id") == category_id:
                current_category = category
                break

        if not current_category:
            raise ValueError(f"Category with ID {category_id} not found")

        # Update only the fields that were provided
        update_data = {
            "category": {
                "id": category_id,
                "label": label if label is not None else current_category.get("label", ""),
                "description": description if description is not None else current_category.get("description", "")
            }
        }

        endpoint = f"{self.BLOG_API}/categories/{category_id}"
        return self._make_request("PATCH", endpoint, data=update_data)

    def delete_category(self, category_id: str) -> Dict:
        """
        Delete a blog category.

        Args:
            category_id: ID of the category to delete

        Returns:
            Response data
        """
        endpoint = f"{self.BLOG_API}/categories/{category_id}"
        return self._make_request("DELETE", endpoint)

    def upload_image(
        self, 
        file_path: str, 
        title: Optional[str] = None, 
        alt_text: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict:
        """
        Upload an image to the Wix media manager.

        Args:
            file_path: Path to the image file
            title: Image title (optional)
            alt_text: Image alt text for accessibility (optional)
            description: Image description (optional)

        Returns:
            Uploaded image data
        """
        # Check if file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Get file name and mime type
        file_name = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)

        if not mime_type or not mime_type.startswith('image/'):
            raise ValueError(f"File does not appear to be an image: {file_path}")

        # Prepare metadata
        metadata = {
            "title": title or file_name,
            "altText": alt_text or "",
            "description": description or ""
        }

        # First, get an upload URL
        endpoint = f"{self.MEDIA_API}/files/upload/url"
        upload_url_response = self._make_request("POST", endpoint, data={
            "mimeType": mime_type,
            "fileName": file_name
        })

        if "uploadUrl" not in upload_url_response:
            raise ValueError("Failed to get upload URL")

        upload_url = upload_url_response["uploadUrl"]

        # Upload the file to the provided URL
        with open(file_path, 'rb') as file:
            upload_response = requests.post(
                upload_url,
                files={'file': (file_name, file, mime_type)},
                headers={"Content-Type": mime_type}
            )

        upload_response.raise_for_status()

        # Complete the upload with metadata
        endpoint = f"{self.MEDIA_API}/files"
        complete_data = {
            "uploadToken": upload_url_response.get("uploadToken"),
            "mediaOptions": {
                "mimeType": mime_type,
                "fileName": file_name,
                "mediaType": "IMAGE",
                "title": metadata["title"],
                "description": metadata["description"],
                "alt": metadata["altText"]
            }
        }

        return self._make_request("POST", endpoint, data=complete_data)

    def get_media_item(self, media_id: str) -> Dict:
        """
        Get details of a specific media item.

        Args:
            media_id: ID of the media item

        Returns:
            Media item data
        """
        endpoint = f"{self.MEDIA_API}/files/{media_id}"
        return self._make_request("GET", endpoint)

    def list_media_items(
        self, 
        media_type: str = "IMAGE", 
        limit: int = 50, 
        offset: int = 0
    ) -> Dict:
        """
        List media items with pagination.

        Args:
            media_type: Type of media to list (IMAGE, VIDEO, AUDIO, DOCUMENT)
            limit: Maximum number of items to return
            offset: Pagination offset

        Returns:
            Dictionary containing media items and pagination info
        """
        endpoint = f"{self.MEDIA_API}/files/query"

        payload = {
            "query": {
                "paging": {
                    "limit": limit,
                    "offset": offset
                },
                "filter": {
                    "mediaType": media_type
                }
            }
        }

        return self._make_request("POST", endpoint, data=payload)

    def delete_media_item(self, media_id: str) -> Dict:
        """
        Delete a media item.

        Args:
            media_id: ID of the media item to delete

        Returns:
            Response data
        """
        endpoint = f"{self.MEDIA_API}/files/{media_id}"
        return self._make_request("DELETE", endpoint)

    def get_seo_settings(self, page_url: str) -> Dict:
        """
        Get SEO settings for a specific page.

        Args:
            page_url: URL path of the page (e.g., "/blog/my-post")

        Returns:
            SEO settings data
        """
        endpoint = f"{self.SEO_API}/sites/{self.site_id}/url/{page_url}"
        return self._make_request("GET", endpoint)

    def update_seo_settings(
        self, 
        page_url: str, 
        title: Optional[str] = None,
        description: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        og_image_url: Optional[str] = None,
        structured_data: Optional[Dict] = None,
        no_index: Optional[bool] = None
    ) -> Dict:
        """
        Update SEO settings for a specific page.

        Args:
            page_url: URL path of the page (e.g., "/blog/my-post")
            title: SEO title
            description: SEO description
            keywords: SEO keywords
            og_image_url: Open Graph image URL
            structured_data: Structured data (JSON-LD)
            no_index: Whether to prevent indexing by search engines

        Returns:
            Updated SEO settings data
        """
        # First, get current SEO settings
        try:
            current_settings = self.get_seo_settings(page_url)
        except:
            # If the page doesn't exist yet, start with empty settings
            current_settings = {"tags": {}}

        # Prepare the update data
        seo_data = {
            "tags": {}
        }

        # Update only the fields that were provided
        if title is not None:
            seo_data["tags"]["title"] = title
        elif "title" in current_settings.get("tags", {}):
            seo_data["tags"]["title"] = current_settings["tags"]["title"]

        if description is not None:
            seo_data["tags"]["description"] = description
        elif "description" in current_settings.get("tags", {}):
            seo_data["tags"]["description"] = current_settings["tags"]["description"]

        if keywords is not None:
            seo_data["tags"]["keywords"] = ", ".join(keywords)
        elif "keywords" in current_settings.get("tags", {}):
            seo_data["tags"]["keywords"] = current_settings["tags"]["keywords"]

        if og_image_url is not None:
            seo_data["tags"]["og:image"] = og_image_url
        elif "og:image" in current_settings.get("tags", {}):
            seo_data["tags"]["og:image"] = current_settings["tags"]["og:image"]

        if structured_data is not None:
            seo_data["tags"]["jsonld"] = json.dumps(structured_data)
        elif "jsonld" in current_settings.get("tags", {}):
            seo_data["tags"]["jsonld"] = current_settings["tags"]["jsonld"]

        if no_index is not None:
            seo_data["tags"]["robots"] = "noindex" if no_index else "index"
        elif "robots" in current_settings.get("tags", {}):
            seo_data["tags"]["robots"] = current_settings["tags"]["robots"]

        endpoint = f"{self.SEO_API}/sites/{self.site_id}/url/{page_url}"
        return self._make_request("PUT", endpoint, data=seo_data)

    def create_blog_post_with_image(
        self, 
        title: str, 
        content: str, 
        image_path: Optional[str] = None,
        excerpt: Optional[str] = None,
        tags: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        seo_title: Optional[str] = None,
        seo_description: Optional[str] = None,
        seo_keywords: Optional[List[str]] = None,
        publish: bool = False
    ) -> Dict:
        """
        Create a blog post with an optional featured image in one operation.

        Args:
            title: Post title
            content: Post content (HTML)
            image_path: Path to featured image (optional)
            excerpt: Post excerpt/summary (optional)
            tags: List of tags (optional)
            categories: List of category IDs (optional)
            seo_title: SEO title (optional)
            seo_description: SEO description (optional)
            seo_keywords: SEO keywords (optional)
            publish: Whether to publish the post immediately (optional)

        Returns:
            Created blog post data
        """
        # Upload image if provided
        featured_image_id = None
        if image_path and os.path.isfile(image_path):
            try:
                image_response = self.upload_image(
                    file_path=image_path,
                    title=title,
                    alt_text=title
                )
                featured_image_id = image_response.get("file", {}).get("id")
                logger.info(f"Uploaded image with ID: {featured_image_id}")
            except Exception as e:
                logger.error(f"Failed to upload image: {str(e)}")

        # Prepare SEO data
        seo_data = None
        if seo_title or seo_description or seo_keywords:
            seo_data = {
                "title": seo_title or title,
                "description": seo_description or excerpt or "",
                "keywords": seo_keywords or tags or []
            }

        # Create the blog post
        return self.create_post(
            title=title,
            content=content,
            excerpt=excerpt,
            featured_image_id=featured_image_id,
            tags=tags,
            categories=categories,
            seo_data=seo_data,
            publish=publish
        )

    def get_or_create_category(self, category_name: str) -> str:
        """
        Get a category ID by name, creating it if it doesn't exist.

        Args:
            category_name: Name of the category

        Returns:
            Category ID
        """
        # List all categories
        categories_response = self.list_categories()
        categories = categories_response.get("categories", [])

        # Check if category exists
        for category in categories:
            if category.get("label", "").lower() == category_name.lower():
                return category.get("id")

        # Create category if it doesn't exist
        create_response = self.create_category(label=category_name)
        return create_response.get("category", {}).get("id")

    def get_post_by_slug(self, slug: str) -> Optional[Dict]:
        """
        Find a post by its slug.

        Args:
            slug: Post slug

        Returns:
            Post data or None if not found
        """
        # List posts with a filter for the slug
        filter_by = {
            "slug": {
                "$eq": slug
            }
        }

        response = self.list_posts(limit=1, filter_by=filter_by)
        posts = response.get("posts", [])

        if posts:
            return posts[0]
        return None

    def get_post_url(self, post_id: str) -> str:
        """
        Get the full URL for a blog post.

        Args:
            post_id: ID of the blog post

        Returns:
            Full URL to the blog post
        """
        post_data = self.get_post(post_id)
        slug = post_data.get("post", {}).get("slug", "")

        # Get the blog URL prefix
        # This is a simplification - in reality, you might need to get this from site settings
        return f"/blog/{slug}"