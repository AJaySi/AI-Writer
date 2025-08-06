# AI Blog Metadata Generator

The AI Blog Metadata Generator module is designed to assist in creating SEO-optimized metadata for blog articles. Utilizing artificial intelligence, this module generates high-quality metadata to enhance the visibility and engagement of blog posts.

## Prerequisites

To use this module, ensure that the following prerequisites are met:

- Python 3.6 or higher
- Streamlit
- Loguru
- Asyncio
- A GPT provider (e.g., OpenAI, Gemini)

## Installation

Install the required packages using the Python package installer, pip:

```bash
pip install -r requirements.txt
```

## Usage

Follow these steps to utilize the AI Blog Metadata Generator module:

### Generate Blog Title

The module provides a function to create a blog title that is both SEO-optimized and engaging. This function ensures the title adheres to SEO best practices and avoids negative keywords.

### Generate Meta Description

This functionality creates a compelling meta description for the blog content. The description is kept between 150-160 characters to ensure it meets SEO standards.

### Generate Blog Tags

The module suggests relevant and specific tags for the blog content. This helps in categorizing and improving the discoverability of the blog post.

### Generate Blog Categories

The module identifies the main topics and suggests the most relevant categories for the blog content. This function ensures that the blog is categorized appropriately for the target audience and taxonomy.

## Helper Functions

The module includes helper functions to run the asyncio event loop within Streamlit, ensuring smooth and efficient operation of asynchronous tasks such as generating metadata.

By leveraging this module, users can enhance their blog posts with well-crafted metadata, improving their visibility and engagement in search engines.
