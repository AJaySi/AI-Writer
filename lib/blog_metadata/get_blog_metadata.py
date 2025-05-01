import os
import time
import datetime
import sys
import streamlit as st
from loguru import logger
import random
import asyncio
import re

logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


async def blog_metadata(blog_article):
    """ 
    Generate comprehensive SEO metadata for a blog article.
    
    Args:
        blog_article (str): The content of the blog article
        
    Returns:
        tuple: (blog_title, blog_meta_desc, blog_tags, blog_categories, blog_hashtags, blog_slug)
    """
    logger.info("Generating comprehensive blog metadata")
    
    progress_bar = st.progress(0)
    total_steps = 6  # Increased steps for new metadata types
    status_container = st.empty()

    try:
        # Step 1: Generate blog title
        status_container.info("Generating SEO-optimized blog title...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        blog_title = generate_blog_title(blog_article)
        progress_bar.progress(1 / total_steps)

        # Step 2: Generate blog meta description
        status_container.info("Creating compelling meta description...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        blog_meta_desc = generate_blog_description(blog_article)
        progress_bar.progress(2 / total_steps)

        # Step 3: Generate blog tags
        status_container.info("Extracting relevant blog tags...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        blog_tags = get_blog_tags(blog_article)
        progress_bar.progress(3 / total_steps)

        # Step 4: Generate blog categories
        status_container.info("Identifying primary blog categories...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        blog_categories = get_blog_categories(blog_article)
        progress_bar.progress(4 / total_steps)
        
        # Step 5: Generate social media hashtags
        status_container.info("Creating social media hashtags...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        blog_hashtags = generate_blog_hashtags(blog_article)
        progress_bar.progress(5 / total_steps)
        
        # Step 6: Generate SEO URL slug
        status_container.info("Generating SEO-friendly URL slug...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        blog_slug = generate_blog_slug(blog_title)
        progress_bar.progress(6 / total_steps)

        # Present the result in a table format
        status_container.success("✅ Blog SEO Metadata generation complete")
        #st.table({
        #    "Metadata": ["Blog Title", "Meta Description", "Tags", "Categories", "Social Hashtags", "URL Slug"],
        #    "Value": [blog_title, blog_meta_desc, blog_tags, blog_categories, blog_hashtags, blog_slug]
        #})

        return blog_title, blog_meta_desc, blog_tags, blog_categories, blog_hashtags, blog_slug
    
    except Exception as e:
        status_container.error(f"Error generating metadata: {str(e)}")
        logger.error(f"Failed to generate metadata: {str(e)}")
        # Return default values to ensure the blog generation process can continue
        return f"Blog Article", "An informative blog post", "content, blog", "General, Information", "#content #blog", "blog-article"


def generate_blog_title(blog_article):
    """
    Generate an SEO-optimized and engaging title for a blog article.
    
    Args:
        blog_article (str): The content of the blog article
        
    Returns:
        str: An SEO-optimized title
    """
    logger.info("Generating SEO-optimized blog title")
    
    # Extract the first 3000 characters for title generation
    snippet = blog_article[:3000] if len(blog_article) > 3000 else blog_article
    
    prompt = f"""As an expert SEO copywriter, create the perfect blog title based on this content.

REQUIREMENTS:
1. Make it compelling, specific, and actionable
2. Include primary keywords naturally near the beginning
3. Keep it between 50-60 characters (10-12 words maximum)
4. Make it promise clear value to the reader
5. Use power words that evoke emotion where appropriate

AVOID:
- Clickbait tactics or false promises
- Generic titles that could apply to any article
- Using words like "unveiling", "unleash", "power of", "ultimate guide", or "complete"
- ALL CAPS or excessive punctuation!!!!

EXAMPLES OF GREAT TITLES:
- "7 Proven Strategies to Improve Your Email Marketing ROI"
- "Why Remote Work Improves Productivity: New Research Findings"
- "How to Build a Personal Budget That Actually Works"

CONTENT TO ANALYZE:
"{snippet}"

Reply with ONLY the title and no other text or explanation.
"""
    try:
        title = llm_text_gen(prompt)
        # Clean up any quotes or extra spaces
        title = title.strip('"\'').strip()
        logger.info(f"Generated title: {title}")
        return title
    except Exception as err:
        logger.error(f"Failed to generate blog title: {err}")
        return "Blog Article"  # Fallback title


def generate_blog_description(blog_content):
    """
    Generate an SEO-optimized meta description for the blog.
    
    Args:
        blog_content (str): The content of the blog article
        
    Returns:
        str: An SEO-optimized meta description
    """
    logger.info("Generating SEO-optimized meta description")
    
    # Extract the first 2000 characters for description generation
    snippet = blog_content[:2000] if len(blog_content) > 2000 else blog_content
    
    prompt = f"""As an SEO expert, write the perfect meta description for this blog content.

REQUIREMENTS:
1. Exactly 150-160 characters (this is critical for SEO)
2. Include primary keywords naturally
3. Compelling value proposition that makes readers want to click
4. Clear indication of what the reader will learn/gain
5. End with an implicit call-to-action when possible

EXAMPLES OF EXCELLENT META DESCRIPTIONS:
- "Learn how to increase email open rates by 43% with these 5 proven strategies from industry experts. Implement today for immediate results."
- "Discover why 67% of professionals struggle with work-life balance and explore research-backed techniques to reclaim your time and energy."

CONTENT TO SUMMARIZE:
"{snippet}"

Reply with ONLY the meta description and no other text. Keep it between 150-160 characters exactly.
"""
    try:
        description = llm_text_gen(prompt)
        # Clean up any quotes or extra spaces
        description = description.strip('"\'').strip()
        logger.info(f"Generated meta description: {description}")
        return description
    except Exception as err:
        logger.error(f"Failed to generate blog description: {err}")
        return "An informative blog post about this topic."  # Fallback description


def get_blog_tags(blog_article):
    """
    Generate relevant SEO tags for a blog article.
    
    Args:
        blog_article (str): The content of the blog article
        
    Returns:
        str: Comma-separated list of relevant tags
    """
    logger.info("Generating SEO-optimized blog tags")
    
    # Extract the first 3000 characters for tag generation
    snippet = blog_article[:3000] if len(blog_article) > 3000 else blog_article
    
    prompt = f"""As an SEO specialist, extract the 4-6 most relevant tags for this blog post.

REQUIREMENTS:
1. Choose specific, targeted keywords that accurately represent the content
2. Include a mix of broad and specific tags
3. Focus on terms users would actually search for
4. Include at least one long-tail keyword phrase
5. Ensure all tags are directly addressed in the content

CONTENT TO ANALYZE:
"{snippet}"

Reply with ONLY the tags as a comma-separated list (e.g., "keyword1, keyword2, keyword3, keyword phrase"). Provide 4-6 tags total.
"""
    try:
        tags = llm_text_gen(prompt)
        # Clean up any quotes or extra commas
        tags = tags.strip('"\'').strip()
        if tags.endswith(','):
            tags = tags[:-1]
        logger.info(f"Generated tags: {tags}")
        return tags
    except Exception as err:
        logger.error(f"Failed to generate blog tags: {err}")
        return "content, blog"  # Fallback tags


def get_blog_categories(blog_article):
    """
    Identify the most appropriate blog categories for the article.
    
    Args:
        blog_article (str): The content of the blog article
        
    Returns:
        str: Comma-separated list of relevant categories
    """
    logger.info("Generating blog categories")
    
    # Extract the first 2000 characters for category generation
    snippet = blog_article[:2000] if len(blog_article) > 2000 else blog_article
    
    prompt = f"""As a content strategist, identify the 2-3 most appropriate high-level categories for this blog.

REQUIREMENTS:
1. Choose broad, established categories used in content organization
2. Select categories that best represent the main themes of the article
3. Consider the target audience and their interests
4. Focus on categories that would help with site navigation
5. Aim for a primary category and 1-2 supporting categories

EXAMPLES OF GOOD CATEGORIES:
- Marketing, Social Media, Strategy
- Finance, Personal Budgeting, Money Management
- Productivity, Remote Work, Business

CONTENT TO ANALYZE:
"{snippet}"

Reply with ONLY the categories as a comma-separated list (e.g., "Category1, Category2, Category3"). Provide 2-3 categories total.
"""
    try:
        categories = llm_text_gen(prompt)
        # Clean up any quotes or extra commas
        categories = categories.strip('"\'').strip()
        if categories.endswith(','):
            categories = categories[:-1]
        logger.info(f"Generated categories: {categories}")
        return categories
    except Exception as err:
        logger.error(f"Failed to generate blog categories: {err}")
        return "General, Information"  # Fallback categories


def generate_blog_hashtags(blog_article):
    """
    Generate social media hashtags for promoting the blog article.
    
    Args:
        blog_article (str): The content of the blog article
        
    Returns:
        str: Space-separated list of hashtags starting with #
    """
    logger.info("Generating social media hashtags")
    
    # Extract the first 2000 characters for hashtag generation
    snippet = blog_article[:2000] if len(blog_article) > 2000 else blog_article
    
    prompt = f"""As a social media strategist, create 5-7 effective hashtags for this blog content.

REQUIREMENTS:
1. Mix of popular and niche hashtags for better visibility
2. Include industry-specific and trending hashtags where relevant
3. Avoid overly generic hashtags (like #content or #blog)
4. Format each hashtag with # symbol and camelCase or separate words
5. Include at least one branded or campaign-style hashtag

EXAMPLES OF EFFECTIVE HASHTAG SETS:
- #EmailMarketing #ROITips #DigitalStrategy #MarketingTips #GrowthHacking #EmailROI
- #RemoteWork #ProductivityTips #FutureOfWork #WorkFromHome #RemoteProductivity #HRInsights

CONTENT TO ANALYZE:
"{snippet}"

Reply with ONLY the hashtags, each starting with # and separated by spaces. Provide 5-7 hashtags total.
"""
    try:
        hashtags = llm_text_gen(prompt)
        # Clean up any quotes or extra spaces
        hashtags = hashtags.strip('"\'').strip()
        # Ensure all hashtags start with #
        if not hashtags.startswith('#'):
            hashtags = ' '.join([f"#{tag.strip('#')}" for tag in hashtags.split()])
        logger.info(f"Generated hashtags: {hashtags}")
        return hashtags
    except Exception as err:
        logger.error(f"Failed to generate blog hashtags: {err}")
        return "#content #blog"  # Fallback hashtags


def generate_blog_slug(blog_title):
    """
    Generate an SEO-friendly URL slug from the blog title.
    
    Args:
        blog_title (str): The title of the blog article
        
    Returns:
        str: An SEO-friendly URL slug
    """
    logger.info("Generating SEO-friendly URL slug")
    
    try:
        # Use a prompt to generate a customized slug
        prompt = f"""As an SEO specialist, create an SEO-friendly URL slug for this blog title: "{blog_title}"

REQUIREMENTS:
1. Keep it under 60 characters
2. Use only lowercase letters, numbers, and hyphens
3. Include primary keywords near the beginning
4. Remove all unnecessary words (a, the, and, or, but, etc.)
5. Ensure it's human-readable and descriptive

EXAMPLES:
- Title: "10 Effective Ways to Improve Your Email Marketing ROI This Quarter"
  Slug: "improve-email-marketing-roi"
  
- Title: "Why Most Remote Workers Are More Productive According to New Research"
  Slug: "remote-workers-productivity-research"

Reply with ONLY the slug and no other text or explanation.
"""
        slug = llm_text_gen(prompt)
        
        # Clean up and normalize the slug
        slug = slug.strip('"\'').strip()
        
        # If the LLM didn't create a proper slug, do it programmatically
        if not re.match(r'^[a-z0-9-]+$', slug):
            # Fallback to simple programmatic slug creation
            slug = blog_title.lower()
            # Remove special characters
            slug = re.sub(r'[^a-z0-9\s-]', '', slug)
            # Replace spaces with hyphens
            slug = re.sub(r'\s+', '-', slug)
            # Remove redundant hyphens
            slug = re.sub(r'-+', '-', slug)
            # Limit length to 60 characters
            slug = slug[:60].strip('-')
        
        logger.info(f"Generated slug: {slug}")
        return slug
    except Exception as err:
        logger.error(f"Failed to generate blog slug: {err}")
        # Create a simple slug programmatically as fallback
        slug = blog_title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug) 
        slug = re.sub(r'-+', '-', slug)
        slug = slug[:60].strip('-')
        return slug


# Helper function to run the asyncio event loop within Streamlit
def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coro)
    loop.close()
    return result


def get_blog_metadata_longform(longform_content):
    """ Function for caching long-form content """
    # Open the file in write mode ("w") to overwrite existing content.
    filepath = os.path.join(os.getenv("CONTENT_SAVE_DIR"), "lognform_metadata_file")
    with open(filepath, "w") as file:
        # Write the text to the file
        file.write(longform_content)
        print(f"String saved successfully to: {filepath}")

    #genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    #file_path = genai.upload_file(path=filepath)
    
    # Wait for the file to finish processing
    #while file_path.state.name == 'PROCESSING':
    #    print('Waiting for video to be processed.')
    #    time.sleep(2)
    #    file_path = genai.get_file(video_file.name)

    #print(f'Video processing complete: {file_path.uri}')

    # Create a cache with a 5 minute TTL
    #cache = caching.CachedContent.create(
    #    model='models/gemini-1.5-flash-001',
    #    display_name='Alwrity Longform content', # used to identify the cache
    #    system_instruction=(
    #        'You are an expert file analyzer , and your job is to answer '
    #        'the user\'s query based on the file you have access to.'
    #    ),
    #    contents=[file_path],
    #    ttl=datetime.timedelta(minutes=15),
    #)

    # Construct a GenerativeModel which uses the created cache.
    #model = genai.GenerativeModel.from_cached_content(cached_content=cache)

    # Query the model
    #response = model.generate_content([(
    #    'SUmmarize the given file '
    #    'in 10 lines '
    #    'list main points')])

    #print(response.usage_metadata)
    #return(response.text)
    return("TBD: Not implemented")
