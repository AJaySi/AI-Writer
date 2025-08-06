"""
Blog Rewriter Utilities Module

This module contains the core functionality for rewriting and updating blog content,
including content extraction, analysis, research, and rewriting capabilities.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import logging
from typing import Dict, List, Tuple, Optional, Any
import json
import os
from datetime import datetime

# Import required modules from the project
from ...gpt_providers.text_generation.main_text_generation import llm_text_gen
from ...gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
from ...ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles
from ...ai_web_researcher.tavily_ai_search import do_tavily_ai_search

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define constants
MAX_TITLE_LENGTH = 70
MAX_META_DESCRIPTION_LENGTH = 160
REWRITE_MODES = {
    "standard": "Standard rewrite with improved clarity and flow",
    "seo_optimization": "Optimize for search engines with targeted keywords",
    "simplification": "Simplify complex content for broader audience",
    "expansion": "Expand with additional details and examples",
    "fact_check": "Focus on fact-checking and updating information",
    "tone_shift": "Change the tone while preserving content",
    "modernization": "Update outdated content with current information"
}

# Define tone options
TONE_OPTIONS = [
    "Professional", "Conversational", "Academic", "Enthusiastic", 
    "Authoritative", "Friendly", "Technical", "Inspirational"
]

class BlogRewriter:
    """Class to handle blog rewriting functionality."""
    
    def __init__(self):
        """Initialize the BlogRewriter class."""
        self.original_content = {}
        self.rewritten_content = {}
        self.research_results = {}
        self.content_analysis = {}
        self.image_suggestions = []
    
    def extract_content_from_url(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a given URL.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            Dictionary containing extracted content
        """
        logger.info(f"Extracting content from URL: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else ""
            
            # Extract meta description
            meta_desc = ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag and "content" in meta_tag.attrs:
                meta_desc = meta_tag["content"]
            
            # Extract main content - try multiple strategies
            content = ""
            
            # Strategy 1: Look for article tag
            article_tag = soup.find("article")
            if article_tag:
                content = article_tag.get_text(separator="\n\n")
            
            # Strategy 2: Look for main content areas
            if not content:
                main_content = soup.find(["main", "div", "section"], class_=re.compile(r"content|article|post|entry|main|body"))
                if main_content:
                    for elem in main_content.find_all(["nav", "aside", "footer", "comments", "script", "style", "header"]):
                        elem.decompose()
                    content = main_content.get_text(separator="\n\n")
            
            # Strategy 3: Look for specific content classes
            if not content:
                content_classes = ["post-content", "entry-content", "article-content", "blog-content", "content-area"]
                for class_name in content_classes:
                    content_div = soup.find("div", class_=class_name)
                    if content_div:
                        for elem in content_div.find_all(["nav", "aside", "footer", "comments", "script", "style", "header"]):
                            elem.decompose()
                        content = content_div.get_text(separator="\n\n")
                        break
            
            # Strategy 4: Look for content within body
            if not content:
                body = soup.find("body")
                if body:
                    # Remove unwanted elements
                    for elem in body.find_all(["nav", "aside", "footer", "comments", "script", "style", "header"]):
                        elem.decompose()
                    content = body.get_text(separator="\n\n")
            
            # Clean up the content
            content = re.sub(r'\n{3,}', '\n\n', content)
            content = re.sub(r'\s{2,}', ' ', content)
            content = content.strip()
            
            # Extract headings with their hierarchy
            headings = []
            for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
                headings.append({
                    "level": int(h.name[1]),
                    "text": h.get_text().strip()
                })
            
            # Extract images with more metadata
            images = []
            for img in soup.find_all("img"):
                if img.get("src") and not img.get("src").startswith("data:"):
                    image_url = img.get("src")
                    if not image_url.startswith(("http://", "https://")):
                        base_url = "/".join(url.split("/")[:3])
                        image_url = f"{base_url}/{image_url.lstrip('/')}"
                    
                    images.append({
                        "url": image_url,
                        "alt_text": img.get("alt", ""),
                        "title": img.get("title", ""),
                        "class": img.get("class", []),
                        "width": img.get("width"),
                        "height": img.get("height")
                    })
            
            # Extract publish date with multiple strategies
            publish_date = None
            # Try meta tags first
            date_meta = soup.find("meta", attrs={"property": "article:published_time"})
            if date_meta and "content" in date_meta.attrs:
                publish_date = date_meta["content"]
            else:
                # Try other meta tags
                for prop in ["datePublished", "dateCreated", "dateModified"]:
                    date_meta = soup.find("meta", attrs={"property": prop})
                    if date_meta and "content" in date_meta.attrs:
                        publish_date = date_meta["content"]
                        break
            
            # Try HTML elements if meta tags failed
            if not publish_date:
                date_elem = soup.find(["time", "span", "div"], class_=re.compile(r"date|time|publish|posted|created"))
                if date_elem and date_elem.get_text():
                    publish_date = date_elem.get_text().strip()
            
            # Extract author with multiple strategies
            author = None
            # Try meta tags first
            author_meta = soup.find("meta", attrs={"name": "author"})
            if author_meta and "content" in author_meta.attrs:
                author = author_meta["content"]
            else:
                # Try other meta tags
                for prop in ["article:author", "author"]:
                    author_meta = soup.find("meta", attrs={"property": prop})
                    if author_meta and "content" in author_meta.attrs:
                        author = author_meta["content"]
                        break
            
            # Try HTML elements if meta tags failed
            if not author:
                author_elem = soup.find(["a", "span", "div"], class_=re.compile(r"author|byline|writer|posted-by"))
                if author_elem and author_elem.get_text():
                    author = author_elem.get_text().strip()
            
            # Log content extraction results
            logger.info(f"Extracted content length: {len(content)} characters")
            logger.info(f"Found {len(headings)} headings")
            logger.info(f"Found {len(images)} images")
            logger.info(f"Publish date: {publish_date}")
            logger.info(f"Author: {author}")
            
            return {
                "title": title,
                "meta_description": meta_desc,
                "content": content,
                "headings": headings,
                "images": images,
                "publish_date": publish_date,
                "author": author,
                "url": url
            }
            
        except Exception as e:
            logger.error(f"Error extracting content from URL: {e}")
            return {
                "title": "",
                "meta_description": "",
                "content": "",
                "headings": [],
                "images": [],
                "publish_date": None,
                "author": None,
                "url": url,
                "error": str(e)
            }
    
    def analyze_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the extracted content to provide insights.
        
        Args:
            content: Dictionary containing extracted content
            
        Returns:
            Dictionary containing content analysis
        """
        logger.info("Analyzing content")
        
        analysis = {}
        
        # Basic metrics
        text_content = content.get("content", "")
        word_count = len(text_content.split())
        sentence_count = len(re.split(r'[.!?]+', text_content))
        paragraph_count = len(re.split(r'\n\n+', text_content))
        
        analysis["metrics"] = {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "avg_words_per_sentence": round(word_count / max(sentence_count, 1), 1),
            "avg_sentences_per_paragraph": round(sentence_count / max(paragraph_count, 1), 1)
        }
        
        # Heading structure analysis
        headings = content.get("headings", [])
        heading_structure = {}
        for h in headings:
            level = h["level"]
            if level not in heading_structure:
                heading_structure[level] = 0
            heading_structure[level] += 1
        
        analysis["heading_structure"] = heading_structure
        
        # Content age analysis
        publish_date = content.get("publish_date")
        if publish_date:
            try:
                if "T" in publish_date:
                    pub_date = datetime.fromisoformat(publish_date.replace("Z", "+00:00"))
                else:
                    date_formats = [
                        "%Y-%m-%d", "%d-%m-%Y", "%B %d, %Y", "%b %d, %Y",
                        "%d %B %Y", "%d %b %Y", "%Y/%m/%d", "%d/%m/%Y"
                    ]
                    for fmt in date_formats:
                        try:
                            pub_date = datetime.strptime(publish_date, fmt)
                            break
                        except ValueError:
                            continue
                
                now = datetime.now()
                age_days = (now - pub_date).days
                analysis["content_age"] = {
                    "days": age_days,
                    "months": round(age_days / 30, 1),
                    "years": round(age_days / 365, 1)
                }
            except Exception as e:
                logger.warning(f"Could not parse publish date: {e}")
                analysis["content_age"] = {"error": "Could not determine content age"}
        else:
            analysis["content_age"] = {"error": "No publish date found"}
        
        # Image analysis
        images = content.get("images", [])
        analysis["images"] = {
            "count": len(images),
            "with_alt_text": sum(1 for img in images if img.get("alt_text"))
        }
        
        return analysis
    
    def conduct_research(self, title: str, content: str, research_depth: str = "medium") -> Dict[str, Any]:
        """
        Conduct web research to find updated information related to the blog content.
        
        Args:
            title: Blog title
            content: Blog content
            research_depth: Depth of research (low, medium, high)
            
        Returns:
            Dictionary containing research results
        """
        logger.info(f"Conducting research with depth: {research_depth}")
        
        # Extract key topics from the content
        prompt = f"""
        Extract 3-5 key topics or claims from this blog content that might need fact-checking or updating.
        For each topic, provide a concise search query that would help find the most recent information.
        
        Blog title: {title}
        
        First 1000 characters of content:
        {content[:1000]}...
        
        Format your response as a JSON array of objects with 'topic' and 'query' fields.
        """
        
        try:
            topics_json = llm_text_gen(prompt)
            topics_json = re.search(r'\[.*\]', topics_json, re.DOTALL)
            if topics_json:
                topics = json.loads(topics_json.group(0))
            else:
                topics = [
                    {"topic": title, "query": title + " latest information"},
                    {"topic": "Updates on " + title, "query": title + " recent developments"}
                ]
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            topics = [
                {"topic": title, "query": title + " latest information"},
                {"topic": "Updates on " + title, "query": title + " recent developments"}
            ]
        
        # Determine number of results based on research depth
        num_results = {"low": 2, "medium": 3, "high": 5}.get(research_depth, 3)
        
        research_results = {"topics": []}
        
        # Conduct research for each topic
        for topic in topics[:3]:  # Limit to 3 topics
            topic_results = {"topic": topic["topic"], "sources": []}
            
            # Try Exa search first
            try:
                exa_results = metaphor_search_articles(topic["query"], num_results=num_results)
                if exa_results:
                    topic_results["sources"].extend(exa_results)
            except Exception as e:
                logger.warning(f"Exa search failed: {e}")
            
            # If Exa didn't return enough results, try Tavily
            if len(topic_results["sources"]) < num_results:
                try:
                    tavily_results = do_tavily_ai_search(topic["query"], num_results=num_results)
                    if tavily_results:
                        existing_urls = [s["url"] for s in topic_results["sources"]]
                        for result in tavily_results:
                            if result["url"] not in existing_urls:
                                topic_results["sources"].append(result)
                                existing_urls.append(result["url"])
                except Exception as e:
                    logger.warning(f"Tavily search failed: {e}")
            
            research_results["topics"].append(topic_results)
        
        return research_results
    
    def generate_rewrite_prompt(self, original_content: Dict[str, Any], 
                               user_preferences: Dict[str, Any],
                               research_results: Dict[str, Any],
                               content_analysis: Dict[str, Any]) -> str:
        """
        Generate a prompt for the LLM to rewrite the blog.
        
        Args:
            original_content: Original blog content
            user_preferences: User preferences for rewriting
            research_results: Research results for updating content
            content_analysis: Analysis of the original content
            
        Returns:
            Prompt string for the LLM
        """
        logger.info("Generating rewrite prompt")
        
        # Extract key information
        title = original_content.get("title", "")
        content = original_content.get("content", "")
        
        # Truncate content if it's too long
        max_content_length = 6000
        if len(content) > max_content_length:
            content_preview = content[:max_content_length] + "...\n[Content truncated due to length]"
        else:
            content_preview = content
        
        # Format research results
        research_summary = ""
        for topic in research_results.get("topics", []):
            research_summary += f"\n## {topic['topic']}\n"
            for i, source in enumerate(topic.get("sources", [])[:3]):
                research_summary += f"Source {i+1}: {source.get('title', 'Untitled')}\n"
                research_summary += f"URL: {source.get('url', 'No URL')}\n"
                research_summary += f"Content: {source.get('content', 'No content')[:300]}...\n\n"
        
        # Build the prompt
        prompt = f"""
        # Blog Rewriting Task
        
        ## Original Blog Information
        Title: {title}
        Word Count: {content_analysis.get('metrics', {}).get('word_count', 'Unknown')}
        Estimated Age: {content_analysis.get('content_age', {}).get('months', 'Unknown')} months
        
        ## Rewriting Instructions
        Mode: {user_preferences.get('rewrite_mode', 'standard')}
        Target Tone: {user_preferences.get('tone', 'Professional')}
        Target Word Count: {user_preferences.get('target_word_count', 'Same as original')}
        Focus Keywords: {', '.join(user_preferences.get('keywords', []))}
        
        ## Special Instructions
        {user_preferences.get('special_instructions', 'No special instructions')}
        
        ## Recent Research Findings
        {research_summary if research_summary else "No research results available."}
        
        ## Original Content
        {content_preview}
        
        ## Your Task
        Please rewrite this blog post according to the instructions above. The rewritten blog should:
        
        1. Maintain the core message and value of the original content
        2. Update any outdated information based on the research findings
        3. Adopt the requested tone and style
        4. Incorporate the focus keywords naturally
        5. Improve readability and engagement
        6. Maintain a logical structure with appropriate headings
        7. Include a compelling introduction and conclusion
        
        ## Output Format
        Please provide your response in the following JSON format:
        ```json
        {{
            "title": "Rewritten title",
            "meta_description": "SEO-optimized meta description (max 160 characters)",
            "content": "Full rewritten content with proper markdown formatting",
            "suggested_images": [
                {{
                    "description": "Brief description of a suggested image",
                    "caption": "Suggested caption for the image",
                    "placement": "Where this image should be placed (e.g., 'After introduction', 'Before conclusion')"
                }}
            ]
        }}
        ```
        
        Ensure the JSON is properly formatted and valid.
        """
        
        return prompt
    
    def rewrite_blog(self, original_content: Dict[str, Any], 
                    user_preferences: Dict[str, Any],
                    research_results: Dict[str, Any],
                    content_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rewrite the blog based on original content, user preferences, and research.
        
        Args:
            original_content: Original blog content
            user_preferences: User preferences for rewriting
            research_results: Research results for updating content
            content_analysis: Analysis of the original content
            
        Returns:
            Dictionary containing rewritten content
        """
        logger.info("Rewriting blog content")
        
        # Generate the prompt
        prompt = self.generate_rewrite_prompt(
            original_content, user_preferences, research_results, content_analysis
        )
        
        # Call the LLM to rewrite the content
        try:
            response = llm_text_gen(prompt)
            
            # Clean the response of any invalid control characters
            response = ''.join(char for char in response if ord(char) >= 32 or char in '\n\r\t')
            
            # Extract JSON from the response
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # If no JSON block found, try to find JSON-like content
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    json_str = response
            
            # Clean up the JSON string
            json_str = re.sub(r'```(json)?', '', json_str).strip()
            
            # Remove any remaining invalid control characters
            json_str = ''.join(char for char in json_str if ord(char) >= 32 or char in '\n\r\t')
            
            # Parse the JSON with error handling
            try:
                rewritten_content = json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                # Try to fix common JSON issues
                json_str = json_str.replace('\\n', '\\\\n')  # Fix escaped newlines
                json_str = json_str.replace('\\"', '"')      # Fix escaped quotes
                json_str = json_str.replace('\\t', '\\\\t')  # Fix escaped tabs
                rewritten_content = json.loads(json_str)
            
            # Validate the response structure
            required_fields = ["title", "meta_description", "content"]
            for field in required_fields:
                if field not in rewritten_content:
                    rewritten_content[field] = original_content.get(field, "")
                    logger.warning(f"Missing required field '{field}' in rewritten content")
            
            # Ensure suggested_images exists
            if "suggested_images" not in rewritten_content:
                rewritten_content["suggested_images"] = []
            
            # Clean up the content field
            if "content" in rewritten_content:
                # Remove any remaining invalid control characters
                rewritten_content["content"] = ''.join(
                    char for char in rewritten_content["content"] 
                    if ord(char) >= 32 or char in '\n\r\t'
                )
                # Normalize whitespace
                rewritten_content["content"] = re.sub(r'\s+', ' ', rewritten_content["content"])
                rewritten_content["content"] = re.sub(r'\n{3,}', '\n\n', rewritten_content["content"])
            
            return rewritten_content
            
        except Exception as e:
            logger.error(f"Error rewriting blog: {e}")
            return {
                "title": original_content.get("title", ""),
                "meta_description": original_content.get("meta_description", ""),
                "content": original_content.get("content", ""),
                "suggested_images": [],
                "error": str(e)
            }
    
    def generate_image(self, image_prompt: str, style: str = "realistic") -> str:
        """
        Generate an image based on the prompt.
        
        Args:
            image_prompt: Prompt for image generation
            style: Style of the image
            
        Returns:
            Path to the generated image
        """
        logger.info(f"Generating image with prompt: {image_prompt}")
        
        try:
            image_path = generate_image(image_prompt, style=style)
            return image_path
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return "" 