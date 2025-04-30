"""
AI Blog Rewriter Module

This module provides functionality to rewrite and update existing blog content
with improved quality, factual accuracy, and SEO optimization.
"""

import streamlit as st
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
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen
from ..gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
from ..web_research.exa_search import exa_search
from ..web_research.tavily_search import tavily_search

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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
            
            # Extract main content - this is a simplified approach
            # In a real implementation, you'd want more sophisticated content extraction
            content = ""
            article_tag = soup.find("article")
            if article_tag:
                content = article_tag.get_text(separator="\\n\\n")
            else:
                # Try to find main content by looking for common content containers
                main_content = soup.find(["main", "div", "section"], class_=re.compile(r"content|article|post|entry"))
                if main_content:
                    # Remove navigation, sidebars, comments, etc.
                    for elem in main_content.find_all(["nav", "aside", "footer", "comments", "script", "style"]):
                        elem.decompose()
                    content = main_content.get_text(separator="\\n\\n")
                else:
                    # Fallback to body content
                    body = soup.find("body")
                    if body:
                        content = body.get_text(separator="\\n\\n")
            
            # Clean up the content
            content = re.sub(r'\\n{3,}', '\\n\\n', content)  # Remove excessive newlines
            content = re.sub(r'\s{2,}', ' ', content)     # Remove excessive spaces
            
            # Extract headings for structure analysis
            headings = []
            for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
                headings.append({
                    "level": int(h.name[1]),
                    "text": h.get_text().strip()
                })
            
            # Extract images
            images = []
            for img in soup.find_all("img"):
                if img.get("src") and not img.get("src").startswith("data:"):
                    image_url = img.get("src")
                    if not image_url.startswith(("http://", "https://")):
                        # Convert relative URL to absolute
                        base_url = "/".join(url.split("/")[:3])  # Get domain
                        image_url = f"{base_url}/{image_url.lstrip('/')}"
                    
                    alt_text = img.get("alt", "")
                    images.append({
                        "url": image_url,
                        "alt_text": alt_text
                    })
            
            # Extract publish date if available
            publish_date = None
            date_meta = soup.find("meta", attrs={"property": "article:published_time"})
            if date_meta and "content" in date_meta.attrs:
                publish_date = date_meta["content"]
            else:
                # Try common date patterns in the HTML
                date_elem = soup.find(["time", "span", "div"], class_=re.compile(r"date|time|publish"))
                if date_elem and date_elem.get_text():
                    publish_date = date_elem.get_text().strip()
            
            # Extract author if available
            author = None
            author_meta = soup.find("meta", attrs={"name": "author"})
            if author_meta and "content" in author_meta.attrs:
                author = author_meta["content"]
            else:
                # Try common author patterns in the HTML
                author_elem = soup.find(["a", "span", "div"], class_=re.compile(r"author|byline"))
                if author_elem and author_elem.get_text():
                    author = author_elem.get_text().strip()
            
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
        paragraph_count = len(re.split(r'\\n\\n+', text_content))
        
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
                # Try to parse the date in various formats
                if "T" in publish_date:
                    # ISO format
                    pub_date = datetime.fromisoformat(publish_date.replace("Z", "+00:00"))
                else:
                    # Try common date formats
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
                
                # Calculate content age
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
            # Extract JSON from the response
            topics_json = re.search(r'\[.*\]', topics_json, re.DOTALL)
            if topics_json:
                topics = json.loads(topics_json.group(0))
            else:
                # Fallback if JSON extraction fails
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
        for topic in topics[:3]:  # Limit to 3 topics to avoid excessive API calls
            topic_results = {"topic": topic["topic"], "sources": []}
            
            # Try Exa search first
            try:
                exa_results = exa_search(topic["query"], num_results=num_results)
                if exa_results:
                    topic_results["sources"].extend(exa_results)
            except Exception as e:
                logger.warning(f"Exa search failed: {e}")
            
            # If Exa didn't return enough results, try Tavily
            if len(topic_results["sources"]) < num_results:
                try:
                    tavily_results = tavily_search(topic["query"], num_results=num_results)
                    if tavily_results:
                        # Avoid duplicates
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
        max_content_length = 6000  # Adjust based on your LLM's context window
        if len(content) > max_content_length:
            content_preview = content[:max_content_length] + "...\\n[Content truncated due to length]"
        else:
            content_preview = content
        
        # Format research results
        research_summary = ""
        for topic in research_results.get("topics", []):
            research_summary += f"\\n## {topic['topic']}\\n"
            for i, source in enumerate(topic.get("sources", [])[:3]):  # Limit to 3 sources per topic
                research_summary += f"Source {i+1}: {source.get('title', 'Untitled')}\\n"
                research_summary += f"URL: {source.get('url', 'No URL')}\\n"
                research_summary += f"Content: {source.get('content', 'No content')[:300]}...\\n\\n"
        
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
            
            # Extract JSON from the response
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response
            
            # Clean up the JSON string
            json_str = re.sub(r'```(json)?', '', json_str).strip()
            
            # Parse the JSON
            rewritten_content = json.loads(json_str)
            
            # Validate the response structure
            required_fields = ["title", "meta_description", "content"]
            for field in required_fields:
                if field not in rewritten_content:
                    rewritten_content[field] = original_content.get(field, "")
            
            # Ensure suggested_images exists
            if "suggested_images" not in rewritten_content:
                rewritten_content["suggested_images"] = []
            
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


def write_blog_rewriter():
    """Main function to display the blog rewriter UI."""
    st.title("AI Blog Rewriter & Updater")
    
    # Create a container for the header section
    with st.container():
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-top: 0;">Revitalize Your Content</h3>
            <p>Update, fact-check, and enhance your existing blog posts with AI assistance. 
            Our tool analyzes your content, researches the latest information, and rewrites your blog 
            to be more engaging, accurate, and SEO-friendly.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize the BlogRewriter class
    if "blog_rewriter" not in st.session_state:
        st.session_state.blog_rewriter = BlogRewriter()
    
    # Initialize session state variables
    if "original_content" not in st.session_state:
        st.session_state.original_content = {}
    if "content_analysis" not in st.session_state:
        st.session_state.content_analysis = {}
    if "research_results" not in st.session_state:
        st.session_state.research_results = {}
    if "rewritten_content" not in st.session_state:
        st.session_state.rewritten_content = {}
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = {}
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    
    # Create tabs for the workflow
    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ Import Content", 
        "2️⃣ Analyze & Research", 
        "3️⃣ Rewrite Settings", 
        "4️⃣ Results & Export"
    ])
    
    # Tab 1: Import Content
    with tab1:
        st.header("Import Your Blog Content")
        
        import_method = st.radio(
            "Choose import method:",
            ["Import from URL", "Paste content manually"],
            horizontal=True
        )
        
        if import_method == "Import from URL":
            url = st.text_input(
                "Enter blog URL:",
                placeholder="https://example.com/blog-post",
                help="Enter the full URL of the blog post you want to rewrite"
            )
            
            if st.button("Import Content", type="primary"):
                if not url:
                    st.error("Please enter a valid URL")
                else:
                    with st.spinner("Extracting content from URL..."):
                        # Extract content from URL
                        st.session_state.original_content = st.session_state.blog_rewriter.extract_content_from_url(url)
                        
                        if "error" in st.session_state.original_content:
                            st.error(f"Error extracting content: {st.session_state.original_content['error']}")
                        else:
                            st.success("Content extracted successfully!")
                            st.session_state.current_step = 2
                            # Auto-click the next tab
                            st.experimental_rerun()
        else:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                title = st.text_input(
                    "Blog Title:",
                    placeholder="Enter the title of your blog post"
                )
            
            with col2:
                author = st.text_input(
                    "Author (optional):",
                    placeholder="Author name"
                )
            
            meta_description = st.text_area(
                "Meta Description (optional):",
                placeholder="Enter the meta description of your blog post",
                max_chars=MAX_META_DESCRIPTION_LENGTH,
                height=80
            )
            
            content = st.text_area(
                "Blog Content:",
                placeholder="Paste your blog content here...",
                height=300
            )
            
            if st.button("Import Content", type="primary"):
                if not title or not content:
                    st.error("Please enter both title and content")
                else:
                    # Store the manually entered content
                    st.session_state.original_content = {
                        "title": title,
                        "meta_description": meta_description,
                        "content": content,
                        "author": author,
                        "headings": [],
                        "images": [],
                        "publish_date": None,
                        "url": None
                    }
                    
                    st.success("Content imported successfully!")
                    st.session_state.current_step = 2
                    # Auto-click the next tab
                    st.experimental_rerun()
        
        # Display the imported content if available
        if st.session_state.original_content and "title" in st.session_state.original_content:
            with st.expander("View Imported Content", expanded=False):
                st.subheader(st.session_state.original_content["title"])
                
                if st.session_state.original_content.get("meta_description"):
                    st.markdown(f"**Meta Description:** {st.session_state.original_content['meta_description']}")
                
                if st.session_state.original_content.get("author"):
                    st.markdown(f"**Author:** {st.session_state.original_content['author']}")
                
                if st.session_state.original_content.get("publish_date"):
                    st.markdown(f"**Published:** {st.session_state.original_content['publish_date']}")
                
                st.markdown("**Content Preview:**")
                content_preview = st.session_state.original_content["content"]
                if len(content_preview) > 1000:
                    content_preview = content_preview[:1000] + "..."
                st.text_area("", content_preview, height=200, disabled=True)
                
                # Display images if available
                if st.session_state.original_content.get("images"):
                    st.markdown(f"**Images:** {len(st.session_state.original_content['images'])} images found")
    
    # Tab 2: Analyze & Research
    with tab2:
        st.header("Analyze & Research")
        
        if not st.session_state.original_content or "title" not in st.session_state.original_content:
            st.info("Please import your blog content first")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Analyze Content", type="primary"):
                    with st.spinner("Analyzing content..."):
                        # Analyze the content
                        st.session_state.content_analysis = st.session_state.blog_rewriter.analyze_content(
                            st.session_state.original_content
                        )
                        st.success("Content analysis complete!")
            
            with col2:
                research_depth = st.selectbox(
                    "Research Depth:",
                    ["low", "medium", "high"],
                    index=1,
                    format_func=lambda x: {"low": "Basic", "medium": "Standard", "high": "Comprehensive"}[x],
                    help="Choose the depth of research to update your content"
                )
                
                if st.button("Conduct Research", type="primary"):
                    with st.spinner("Researching latest information..."):
                        # Conduct research
                        st.session_state.research_results = st.session_state.blog_rewriter.conduct_research(
                            st.session_state.original_content["title"],
                            st.session_state.original_content["content"],
                            research_depth
                        )
                        st.success("Research complete!")
            
            # Display content analysis if available
            if st.session_state.content_analysis:
                st.subheader("Content Analysis")
                
                metrics = st.session_state.content_analysis.get("metrics", {})
                
                # Create metrics display
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Word Count", metrics.get("word_count", 0))
                with col2:
                    st.metric("Paragraphs", metrics.get("paragraph_count", 0))
                with col3:
                    st.metric("Sentences", metrics.get("sentence_count", 0))
                with col4:
                    content_age = st.session_state.content_analysis.get("content_age", {})
                    if "months" in content_age:
                        st.metric("Content Age", f"{content_age['months']} months")
                    elif "error" in content_age:
                        st.metric("Content Age", "Unknown")
                
                # Heading structure
                heading_structure = st.session_state.content_analysis.get("heading_structure", {})
                if heading_structure:
                    st.markdown("**Heading Structure:**")
                    for level, count in sorted(heading_structure.items()):
                        st.markdown(f"H{level}: {count} headings")
                
                # Image analysis
                images = st.session_state.content_analysis.get("images", {})
                if images:
                    st.markdown(f"**Images:** {images.get('count', 0)} images found, {images.get('with_alt_text', 0)} with alt text")
            
            # Display research results if available
            if st.session_state.research_results:
                st.subheader("Research Results")
                
                topics = st.session_state.research_results.get("topics", [])
                if topics:
                    for topic in topics:
                        with st.expander(f"Topic: {topic['topic']}", expanded=False):
                            for i, source in enumerate(topic.get("sources", [])):
                                st.markdown(f"**Source {i+1}:** {source.get('title', 'Untitled')}")
                                st.markdown(f"**URL:** {source.get('url', 'No URL')}")
                                st.markdown(f"**Content Preview:** {source.get('content', 'No content')[:200]}...")
                                st.markdown("---")
                else:
                    st.info("No research results available")
            
            # Enable proceeding to the next step if both analysis and research are done
            if st.session_state.content_analysis and st.session_state.research_results:
                if st.button("Proceed to Rewrite Settings", type="primary"):
                    st.session_state.current_step = 3
                    st.experimental_rerun()
    
    # Tab 3: Rewrite Settings
    with tab3:
        st.header("Rewrite Settings")
        
        if not st.session_state.original_content or "title" not in st.session_state.original_content:
            st.info("Please import your blog content first")
        elif not st.session_state.content_analysis or not st.session_state.research_results:
            st.info("Please complete content analysis and research first")
        else:
            # Create a form for rewrite settings
            with st.form("rewrite_settings_form"):
                st.subheader("Content Transformation")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    rewrite_mode = st.selectbox(
                        "Rewrite Mode:",
                        list(REWRITE_MODES.keys()),
                        format_func=lambda x: x.replace("_", " ").title(),
                        help="Choose how you want to transform your content"
                    )
                    
                    st.info(REWRITE_MODES[rewrite_mode])
                
                with col2:
                    tone = st.selectbox(
                        "Target Tone:",
                        TONE_OPTIONS,
                        index=0,
                        help="Choose the tone for your rewritten content"
                    )
                
                st.subheader("Content Length")
                
                original_word_count = st.session_state.content_analysis.get("metrics", {}).get("word_count", 0)
                
                length_option = st.radio(
                    "Target Length:",
                    ["same", "shorter", "longer", "custom"],
                    format_func=lambda x: {
                        "same": f"Same as original ({original_word_count} words)",
                        "shorter": f"Shorter (about {int(original_word_count * 0.7)} words)",
                        "longer": f"Longer (about {int(original_word_count * 1.3)} words)",
                        "custom": "Custom word count"
                    }[x],
                    horizontal=True
                )
                
                if length_option == "custom":
                    target_word_count = st.number_input(
                        "Custom Word Count:",
                        min_value=100,
                        max_value=10000,
                        value=original_word_count,
                        step=100
                    )
                else:
                    target_word_count = {
                        "same": original_word_count,
                        "shorter": int(original_word_count * 0.7),
                        "longer": int(original_word_count * 1.3)
                    }[length_option]
                
                st.subheader("SEO Optimization")
                
                keywords = st.text_input(
                    "Focus Keywords (comma-separated):",
                    placeholder="e.g., digital marketing, SEO, content strategy",
                    help="Enter keywords to optimize your content for"
                )
                
                st.subheader("Additional Instructions")
                
                special_instructions = st.text_area(
                    "Special Instructions (optional):",
                    placeholder="Add any specific instructions for rewriting your content...",
                    help="Provide any additional instructions for the AI"
                )
                
                # Submit button
                submitted = st.form_submit_button("Rewrite Blog", type="primary")
                
                if submitted:
                    # Process the form data
                    user_preferences = {
                        "rewrite_mode": rewrite_mode,
                        "tone": tone,
                        "target_word_count": target_word_count,
                        "keywords": [k.strip() for k in keywords.split(",")] if keywords else [],
                        "special_instructions": special_instructions
                    }
                    
                    with st.spinner("Rewriting your blog..."):
                        # Rewrite the blog
                        st.session_state.rewritten_content = st.session_state.blog_rewriter.rewrite_blog(
                            st.session_state.original_content,
                            user_preferences,
                            st.session_state.research_results,
                            st.session_state.content_analysis
                        )
                        
                        if "error" in st.session_state.rewritten_content:
                            st.error(f"Error rewriting blog: {st.session_state.rewritten_content['error']}")
                        else:
                            st.success("Blog rewritten successfully!")
                            st.session_state.current_step = 4
                            st.experimental_rerun()
    
    # Tab 4: Results & Export
    with tab4:
        st.header("Results & Export")
        
        if not st.session_state.rewritten_content or "title" not in st.session_state.rewritten_content:
            st.info("Please complete the rewriting process first")
        else:
            # Display the rewritten content
            st.subheader("Rewritten Blog")
            
            # Title and meta description
            st.markdown(f"## {st.session_state.rewritten_content['title']}")
            
            if st.session_state.rewritten_content.get("meta_description"):
                with st.expander("Meta Description", expanded=True):
                    st.text_area(
                        "",
                        st.session_state.rewritten_content["meta_description"],
                        height=80,
                        disabled=True
                    )
            
            # Create tabs for different views
            content_tab1, content_tab2 = st.tabs(["Preview", "Markdown"])
            
            with content_tab1:
                st.markdown(st.session_state.rewritten_content["content"])
            
            with content_tab2:
                st.text_area(
                    "",
                    st.session_state.rewritten_content["content"],
                    height=400
                )
            
            # Image generation section
            st.subheader("Generate Images")
            
            suggested_images = st.session_state.rewritten_content.get("suggested_images", [])
            if suggested_images:
                st.markdown("**Suggested Images:**")
                
                for i, img in enumerate(suggested_images):
                    with st.expander(f"Image {i+1}: {img.get('description', 'No description')}", expanded=False):
                        st.markdown(f"**Description:** {img.get('description', 'No description')}")
                        st.markdown(f"**Caption:** {img.get('caption', 'No caption')}")
                        st.markdown(f"**Placement:** {img.get('placement', 'No placement specified')}")
                        
                        # Generate image button
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            image_prompt = st.text_area(
                                "Image Prompt:",
                                value=img.get('description', ''),
                                key=f"image_prompt_{i}"
                            )
                        
                        with col2:
                            style = st.selectbox(
                                "Style:",
                                ["realistic", "artistic", "cartoon", "3d_render"],
                                key=f"style_{i}"
                            )
                            
                            if st.button("Generate Image", key=f"gen_img_{i}"):
                                with st.spinner("Generating image..."):
                                    image_path = st.session_state.blog_rewriter.generate_image(image_prompt, style)
                                    
                                    if image_path:
                                        # Store the generated image
                                        if "generated_images" not in st.session_state:
                                            st.session_state.generated_images = {}
                                        
                                        st.session_state.generated_images[f"image_{i}"] = {
                                            "path": image_path,
                                            "caption": img.get('caption', ''),
                                            "placement": img.get('placement', '')
                                        }
                                        
                                        st.success("Image generated successfully!")
                                        st.experimental_rerun()
                        
                        # Display the generated image if available
                        if f"image_{i}" in st.session_state.generated_images:
                            st.image(
                                st.session_state.generated_images[f"image_{i}"]["path"],
                                caption=st.session_state.generated_images[f"image_{i}"]["caption"],
                                use_column_width=True
                            )
            else:
                st.info("No image suggestions available")
                
                # Custom image generation
                with st.expander("Generate Custom Image", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        custom_image_prompt = st.text_area(
                            "Image Prompt:",
                            placeholder="Describe the image you want to generate..."
                        )
                    
                    with col2:
                        custom_style = st.selectbox(
                            "Style:",
                            ["realistic", "artistic", "cartoon", "3d_render"]
                        )
                        
                        if st.button("Generate Custom Image"):
                            if not custom_image_prompt:
                                st.error("Please enter an image prompt")
                            else:
                                with st.spinner("Generating image..."):
                                    image_path = st.session_state.blog_rewriter.generate_image(custom_image_prompt, custom_style)
                                    
                                    if image_path:
                                        # Store the generated image
                                        if "generated_images" not in st.session_state:
                                            st.session_state.generated_images = {}
                                        
                                        st.session_state.generated_images["custom_image"] = {
                                            "path": image_path,
                                            "caption": "Custom generated image",
                                            "placement": "Custom placement"
                                        }
                                        
                                        st.success("Image generated successfully!")
                                        st.experimental_rerun()
                    
                    # Display the generated custom image if available
                    if "custom_image" in st.session_state.generated_images:
                        st.image(
                            st.session_state.generated_images["custom_image"]["path"],
                            caption=st.session_state.generated_images["custom_image"]["caption"],
                            use_column_width=True
                        )
            
            # Export options
            st.subheader("Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "Download as Markdown",
                    data=st.session_state.rewritten_content["content"],
                    file_name=f"{st.session_state.rewritten_content['title'].replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            
            with col2:
                # Create HTML version
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{st.session_state.rewritten_content['title']}</title>
                    <meta name="description" content="{st.session_state.rewritten_content.get('meta_description', '')}">
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                        h1, h2, h3, h4, h5, h6 {{ color: #333; }}
                        img {{ max-width: 100%; height: auto; }}
                        pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                        blockquote {{ border-left: 5px solid #eee; padding-left: 15px; margin-left: 0; }}
                    </style>
                </head>
                <body>
                    <h1>{st.session_state.rewritten_content['title']}</h1>
                    {st.session_state.rewritten_content['content']}
                </body>
                </html>
                """
                
                st.download_button(
                    "Download as HTML",
                    data=html_content,
                    file_name=f"{st.session_state.rewritten_content['title'].replace(' ', '_')}.html",
                    mime="text/html"
                )
            
            with col3:
                # Create JSON version with all content and metadata
                json_content = {
                    "title": st.session_state.rewritten_content["title"],
                    "meta_description": st.session_state.rewritten_content.get("meta_description", ""),
                    "content": st.session_state.rewritten_content["content"],
                    "suggested_images": st.session_state.rewritten_content.get("suggested_images", []),
                    "generated_images": [
                        {
                            "caption": img_data["caption"],
                            "placement": img_data["placement"],
                            "path": img_data["path"]
                        }
                        for img_key, img_data in st.session_state.generated_images.items()
                    ] if hasattr(st.session_state, "generated_images") else [],
                    "original_title": st.session_state.original_content.get("title", ""),
                    "original_url": st.session_state.original_content.get("url", ""),
                    "rewrite_date": datetime.now().isoformat()
                }
                
                st.download_button(
                    "Download as JSON",
                    data=json.dumps(json_content, indent=2),
                    file_name=f"{st.session_state.rewritten_content['title'].replace(' ', '_')}.json",
                    mime="application/json"
                )
            
            # Copy to clipboard buttons
            st.subheader("Quick Copy")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Copy Title", key="copy_title"):
                    st.code(st.session_state.rewritten_content["title"])
                    st.success("Title copied to clipboard!")
            
            with col2:
                if st.button("Copy Meta Description", key="copy_meta"):
                    st.code(st.session_state.rewritten_content.get("meta_description", ""))
                    st.success("Meta description copied to clipboard!")
            
            with col3:
                if st.button("Copy Full Content", key="copy_content"):
                    st.success("Content copied to clipboard!")
            
            # Comparison with original
            with st.expander("Compare with Original", expanded=False):
                comp_col1, comp_col2 = st.columns(2)
                
                with comp_col1:
                    st.subheader("Original")
                    st.markdown(f"**Title:** {st.session_state.original_content.get('title', '')}")
                    if st.session_state.original_content.get("meta_description"):
                        st.markdown(f"**Meta Description:** {st.session_state.original_content['meta_description']}")
                    st.text_area(
                        "Original Content",
                        st.session_state.original_content.get("content", ""),
                        height=300,
                        disabled=True
                    )
                
                with comp_col2:
                    st.subheader("Rewritten")
                    st.markdown(f"**Title:** {st.session_state.rewritten_content['title']}")
                    if st.session_state.rewritten_content.get("meta_description"):
                        st.markdown(f"**Meta Description:** {st.session_state.rewritten_content['meta_description']}")
                    st.text_area(
                        "Rewritten Content",
                        st.session_state.rewritten_content["content"],
                        height=300,
                        disabled=True
                    )
            
            # Start over button
            if st.button("Start Over", type="primary"):
                # Reset session state
                for key in ["original_content", "content_analysis", "research_results", 
                           "rewritten_content", "generated_images", "current_step"]:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.experimental_rerun()

if __name__ == "__main__":
    write_blog_rewriter()