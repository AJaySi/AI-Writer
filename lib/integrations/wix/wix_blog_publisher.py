"""
Wix Blog Publisher for Alwrity

This module integrates the Wix API with the Alwrity AI Writer platform,
allowing users to publish generated blog content directly to their Wix site.
"""

import os
import logging
import tempfile
import streamlit as st
from typing import Dict, List, Optional, Union, Any, Tuple
from pathlib import Path

from .wix_integration import WixIntegration

# Configure logging
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('wix_blog_publisher')

def publish_to_wix(
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
update_if_exists: bool = True,
api_key: Optional[str] = None,
refresh_token: Optional[str] = None,
site_id: Optional[str] = None
) -> Dict:
"""
Publish a blog post to Wix.

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
api_key: Wix API key (optional if using refresh token)
refresh_token: Wix refresh token for OAuth authentication
site_id: Wix site ID

Returns:
Published blog post data
"""
# Initialize Wix integration
wix = WixIntegration(api_key, refresh_token, site_id)

# Publish the blog post
return wix.publish_blog_post(
title=title,
content=content,
is_markdown=is_markdown,
featured_image_path=featured_image_path,
featured_image_url=featured_image_url,
excerpt=excerpt,
tags=tags,
categories=categories,
seo_title=seo_title,
seo_description=seo_description,
seo_keywords=seo_keywords,
author_name=author_name,
publisher_name=publisher_name,
publisher_logo_url=publisher_logo_url,
publish=publish,
update_if_exists=update_if_exists
)

def wix_blog_publisher_ui():
"""
Streamlit UI for publishing blog posts to Wix.
"""
st.title("Publish to Wix")
st.write("Publish your blog content directly to your Wix site.")

# Authentication settings
st.header("Wix Authentication")

# Check for saved credentials
if "wix_refresh_token" in st.session_state and "wix_site_id" in st.session_state:
st.success("✅ Wix credentials are saved in this session.")
show_saved = st.checkbox("Show saved credentials")
if show_saved:
st.text_input("Refresh Token", value=st.session_state.wix_refresh_token, type="password", disabled=True)
st.text_input("Site ID", value=st.session_state.wix_site_id, disabled=True)

clear_creds = st.button("Clear saved credentials")
if clear_creds:
if "wix_refresh_token" in st.session_state:
del st.session_state.wix_refresh_token
if "wix_site_id" in st.session_state:
del st.session_state.wix_site_id
st.rerun()
else:
col1, col2 = st.columns(2)

with col1:
refresh_token = st.text_input("Wix Refresh Token", type="password", help="Your Wix refresh token for API authentication")

with col2:
site_id = st.text_input("Wix Site ID", help="Your Wix site ID")

save_creds = st.checkbox("Save credentials for this session", value=True)

if st.button("Validate Credentials"):
if not refresh_token:
st.error("Refresh token is required.")
return

if not site_id:
st.error("Site ID is required.")
return

# Try to initialize Wix integration to validate credentials
try:
wix = WixIntegration(refresh_token=refresh_token, site_id=site_id)
# Test API call
site_info = wix.get_site_info()
if site_info.get("status") == "connected":
st.success(f"✅ Credentials validated successfully! Found {site_info.get('post_count', 0)} posts and {site_info.get('category_count', 0)} categories.")

# Save credentials if requested
if save_creds:
st.session_state.wix_refresh_token = refresh_token
st.session_state.wix_site_id = site_id
st.rerun()
else:
st.error(f"❌ Failed to validate credentials: {site_info.get('error', 'Unknown error')}")
except Exception as e:
st.error(f"❌ Failed to validate credentials: {str(e)}")
return

# Blog content section
st.header("Blog Content")

# Check if we have content in session state (from other parts of the app)
blog_title = st.text_input(
"Blog Title", 
value=st.session_state.get("blog_title", ""),
help="The title of your blog post"
)

content_type = st.radio(
"Content Format",
["Markdown", "HTML"],
horizontal=True,
help="The format of your blog content"
)
is_markdown = content_type == "Markdown"

blog_content = st.text_area(
"Blog Content", 
value=st.session_state.get("blog_content", ""),
height=300,
help="The content of your blog post"
)

# Featured image
st.subheader("Featured Image")
image_source = st.radio(
"Image Source",
["None", "Upload", "URL"],
horizontal=True,
help="How to provide the featured image"
)

featured_image_path = None
featured_image_url = None

if image_source == "Upload":
uploaded_file = st.file_uploader("Upload Featured Image", type=["jpg", "jpeg", "png", "gif"])
if uploaded_file:
# Save the uploaded file to a temporary location
with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
tmp.write(uploaded_file.getvalue())
featured_image_path = tmp.name
elif image_source == "URL":
featured_image_url = st.text_input("Featured Image URL", help="URL of the featured image")

# Blog metadata
st.header("Blog Metadata")

col1, col2 = st.columns(2)

with col1:
excerpt = st.text_area(
"Excerpt", 
value=st.session_state.get("blog_excerpt", ""),
help="A short summary of your blog post"
)

tags_input = st.text_input(
"Tags (comma-separated)", 
value=", ".join(st.session_state.get("blog_tags", [])) if isinstance(st.session_state.get("blog_tags", []), list) else st.session_state.get("blog_tags", ""),
help="Tags for your blog post, separated by commas"
)
tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else None

categories_input = st.text_input(
"Categories (comma-separated)", 
value=", ".join(st.session_state.get("blog_categories", [])) if isinstance(st.session_state.get("blog_categories", []), list) else st.session_state.get("blog_categories", ""),
help="Categories for your blog post, separated by commas"
)
categories = [cat.strip() for cat in categories_input.split(",")] if categories_input else None

with col2:
author_name = st.text_input("Author Name", help="Name of the blog post author")
publisher_name = st.text_input("Publisher Name", help="Name of the blog publisher (usually your site name)")
publisher_logo_url = st.text_input("Publisher Logo URL", help="URL of the publisher's logo")

# SEO settings
with st.expander("SEO Settings"):
seo_title = st.text_input("SEO Title", value=blog_title, help="Title for search engines (defaults to blog title)")
seo_description = st.text_area("SEO Description", value=excerpt, help="Description for search engines (defaults to excerpt)")
seo_keywords_input = st.text_input("SEO Keywords (comma-separated)", value=tags_input, help="Keywords for search engines (defaults to tags)")
seo_keywords = [kw.strip() for kw in seo_keywords_input.split(",")] if seo_keywords_input else None

# Publishing options
st.header("Publishing Options")

col1, col2 = st.columns(2)

with col1:
publish = not st.checkbox("Save as draft", help="If checked, the post will be saved as a draft instead of being published")

with col2:
update_if_exists = st.checkbox("Update if exists", value=True, help="If checked, an existing post with the same title will be updated")

# Publish button
if st.button("Publish to Wix", type="primary"):
if not blog_title:
st.error("Blog title is required.")
return

if not blog_content:
st.error("Blog content is required.")
return

# Get credentials
refresh_token = st.session_state.get("wix_refresh_token")
site_id = st.session_state.get("wix_site_id")

if not refresh_token or not site_id:
st.error("Wix credentials are required. Please enter them in the authentication section.")
return

# Show progress
with st.spinner("Publishing to Wix..."):
try:
# Publish to Wix
result = publish_to_wix(
title=blog_title,
content=blog_content,
is_markdown=is_markdown,
featured_image_path=featured_image_path,
featured_image_url=featured_image_url,
excerpt=excerpt,
tags=tags,
categories=categories,
seo_title=seo_title,
seo_description=seo_description,
seo_keywords=seo_keywords,
author_name=author_name,
publisher_name=publisher_name,
publisher_logo_url=publisher_logo_url,
publish=publish,
update_if_exists=update_if_exists,
refresh_token=refresh_token,
site_id=site_id
)

# Clean up temporary file if created
if featured_image_path and os.path.exists(featured_image_path) and featured_image_path.startswith(tempfile.gettempdir()):
try:
os.remove(featured_image_path)
except:
pass

# Show success message
st.success("✅ Blog post published successfully!")

# Show post details
post = result.get("post", {})
st.subheader("Published Post Details")

col1, col2 = st.columns(2)

with col1:
st.write(f"**Title:** {post.get('title', 'N/A')}")
st.write(f"**Status:** {post.get('status', 'N/A')}")
st.write(f"**ID:** {post.get('id', 'N/A')}")

with col2:
st.write(f"**Published Date:** {post.get('publishedDate', 'N/A')}")
st.write(f"**URL:** {post.get('url', 'N/A')}")
st.write(f"**Tags:** {', '.join(post.get('tags', []))}")

# Add a view button if URL is available
if post.get("url"):
st.markdown(f"[View Post]({post.get('url')})")

# Add SEO report button
if st.button("Generate SEO Report"):
with st.spinner("Generating SEO report..."):
try:
wix = WixIntegration(refresh_token=refresh_token, site_id=site_id)
seo_report = wix.get_seo_report(post.get("id"), seo_keywords or tags or [])

st.subheader("SEO Report")
st.write(f"**SEO Score:** {seo_report.get('seo_score', 0):.1f}/100")

st.write("**Recommendations:**")
for i, rec in enumerate(seo_report.get("recommendations", [])):
st.write(f"{i+1}. {rec}")
except Exception as e:
st.error(f"Failed to generate SEO report: {str(e)}")

except Exception as e:
st.error(f"❌ Failed to publish blog post: {str(e)}")
logger.error(f"Failed to publish blog post: {str(e)}")

# For testing the UI directly
if __name__ == "__main__":
wix_blog_publisher_ui()