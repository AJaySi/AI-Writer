# Wix Blog Integration for Alwrity

This integration allows you to publish blog content from Alwrity directly to your Wix site using the Wix REST API.

## Features

- **Blog Post Management**: Create, update, and delete blog posts
- **Media Management**: Upload images and other media files
- **SEO Optimization**: Comprehensive SEO settings and analysis
- **Category Management**: Create and manage blog categories
- **Markdown Support**: Write in markdown and publish as HTML
- **Streamlit UI**: User-friendly interface for publishing

## Prerequisites

Before using this integration, you'll need:

1. A Wix site with the Blog feature enabled
2. Wix API credentials (refresh token and site ID)
3. Python 3.7+ with required dependencies

## Getting Wix API Credentials

To use this integration, you need to obtain a refresh token and site ID from Wix:

1. **Create a Wix Developer Account**:
- Go to [Wix Developers](https://dev.wix.com/) and sign up or log in
- Create a new OAuth app

2. **Configure OAuth App**:
- Set a name and description for your app
- Add redirect URLs (e.g., `https://localhost:3000/oauth/callback`)
- Save the app and note the App ID and App Secret

3. **Get a Refresh Token**:
- Follow the OAuth flow to get an authorization code
- Exchange the code for an access token and refresh token
- Detailed instructions: [Wix OAuth Documentation](https://dev.wix.com/api/rest/getting-started/authentication)

4. **Get Your Site ID**:
- Log in to your Wix account
- Go to your site's dashboard
- The site ID is in the URL: `https://manage.wix.com/dashboard/{SITE_ID}/home`

## Installation

The Wix integration is included with Alwrity. No additional installation is required.

## Usage

### Using the Streamlit UI

1. Navigate to the Wix integration in the Alwrity UI
2. Enter your Wix refresh token and site ID
3. Fill in the blog details and content
4. Click "Publish to Wix"

### Using the Python API

```python
from lib.integrations.wix_integration import WixIntegration

# Initialize the integration
wix = WixIntegration(
refresh_token="YOUR_REFRESH_TOKEN",
site_id="YOUR_SITE_ID"
)

# Publish a blog post
result = wix.publish_blog_post(
title="My Blog Post",
content="# Hello World\n\nThis is my blog post.",
is_markdown=True,
tags=["example", "blog"],
categories=["Technology"],
publish=True
)

# Get the published post URL
post_url = result.get("post", {}).get("url")
print(f"Published at: {post_url}")
```

### Using the Command-Line Interface

```bash
# Set environment variables
export WIX_REFRESH_TOKEN="YOUR_REFRESH_TOKEN"
export WIX_SITE_ID="YOUR_SITE_ID"

# List blog posts
python -m lib.integrations.wix_cli list-posts

# Publish a blog post
python -m lib.integrations.wix_cli publish-post \
--title "My Blog Post" \
--content-file blog.md \
--is-markdown \
--tags "example,blog" \
--categories "Technology"

# Generate an SEO report
python -m lib.integrations.wix_cli seo-report \
--title "My Blog Post" \
--keywords "example,blog,technology"
```

## API Reference

### WixIntegration

The main integration class that provides high-level methods for working with Wix blogs.

#### Methods

- `publish_blog_post(title, content, ...)`: Publish a blog post
- `upload_media(file_path, ...)`: Upload a media file
- `get_seo_report(post_id, target_keywords)`: Generate an SEO report
- `list_blog_posts(limit, offset, ...)`: List blog posts
- `list_categories()`: List blog categories
- `create_category(name, description)`: Create a blog category
- `get_post_by_id(post_id)`: Get a blog post by ID
- `get_post_by_title(title)`: Get a blog post by title
- `delete_post(post_id)`: Delete a blog post

### WixAPIClient

Low-level client for interacting with the Wix API.

### WixBlogManager

Handles blog content management, including markdown processing and image handling.

### WixSEOOptimizer

Provides SEO analysis and optimization for blog posts.

## Error Handling

The integration includes comprehensive error handling:

- API errors are logged with detailed information
- Authentication errors provide clear guidance
- File handling errors include path information
- Network errors include retry logic

## Best Practices

1. **Store credentials securely**:
- Use environment variables or a secure credential store
- Don't hardcode credentials in your code

2. **Optimize images before upload**:
- Compress images to reduce file size
- Use appropriate image formats (JPEG for photos, PNG for graphics)

3. **SEO optimization**:
- Use the SEO report to improve your content
- Include relevant keywords in titles and headings
- Add alt text to all images

4. **Content management**:
- Use categories and tags consistently
- Include featured images for better visual appeal
- Write clear, concise meta descriptions

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
- Ensure your refresh token is valid
- Check that your site ID is correct
- Verify that your app has the necessary permissions

2. **API Rate Limits**:
- The Wix API has rate limits that may affect bulk operations
- Add delays between requests if you're publishing many posts

3. **Image Upload Issues**:
- Check that the image file exists and is readable
- Verify that the image format is supported (JPEG, PNG, GIF)
- Ensure the image file size is within Wix limits

4. **Content Formatting Issues**:
- If using markdown, ensure it's valid
- Check for special characters that might cause issues
- Verify that HTML content is properly formatted

### Getting Help

If you encounter issues not covered here:

1. Check the logs for detailed error messages
2. Consult the [Wix API Documentation](https://dev.wix.com/api/rest/getting-started)
3. Contact Alwrity support for assistance

## License

This integration is part of the Alwrity platform and is subject to the same license terms.

## Acknowledgements

- [Wix REST API](https://dev.wix.com/api/rest) for providing the API endpoints
- [Requests](https://docs.python-requests.org/) for HTTP functionality
- [Markdown](https://python-markdown.github.io/) for markdown processing
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Streamlit](https://streamlit.io/) for the user interface
