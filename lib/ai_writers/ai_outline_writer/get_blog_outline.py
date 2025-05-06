"""
Enhanced Blog Outline Generator

This module provides a sophisticated outline generation system that creates detailed,
well-structured outlines for blog posts based on user preferences and content requirements.
"""

import sys
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from loguru import logger

from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

logger.remove()
logger.add(sys.stdout,
          colorize=True,
          format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

class ContentType(Enum):
    """Types of content that can be generated."""
    HOW_TO = "how-to"
    TUTORIAL = "tutorial"
    LISTICLE = "listicle"
    COMPARISON = "comparison"
    CASE_STUDY = "case-study"
    OPINION = "opinion"
    NEWS = "news"
    REVIEW = "review"
    GUIDE = "guide"

class ContentDepth(Enum):
    """Depth levels for content coverage."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class OutlineStyle(Enum):
    """Styles for outline structure."""
    TRADITIONAL = "traditional"
    MODERN = "modern"
    CONVERSATIONAL = "conversational"
    ACADEMIC = "academic"
    SEO_OPTIMIZED = "seo-optimized"

@dataclass
class OutlineConfig:
    """Configuration for outline generation."""
    content_type: ContentType = ContentType.GUIDE
    content_depth: ContentDepth = ContentDepth.INTERMEDIATE
    outline_style: OutlineStyle = OutlineStyle.MODERN
    target_word_count: int = 2000
    num_main_sections: int = 5
    num_subsections_per_section: int = 3
    include_introduction: bool = True
    include_conclusion: bool = True
    include_faqs: bool = True
    include_resources: bool = True
    target_audience: str = "general"
    language: str = "English"
    keywords: List[str] = None
    exclude_topics: List[str] = None
    include_images: bool = True
    image_style: str = "realistic"
    image_engine: str = "Gemini-AI"

@dataclass
class SectionContent:
    """Content for a section including text and image."""
    title: str
    content: str
    image_prompt: Optional[str] = None
    image_path: Optional[str] = None

class BlogOutlineGenerator:
    """Enhanced blog outline generator with comprehensive controls."""
    
    def __init__(self, config: Optional[OutlineConfig] = None):
        """Initialize the outline generator with optional configuration."""
        self.config = config or OutlineConfig()
        self.outline = {}
        self.section_contents = {}
        
    async def generate_outline(self, topic: str) -> Dict:
        """Generate a comprehensive outline based on the topic and configuration."""
        try:
            # Step 1: Generate main sections
            main_sections = await self._generate_main_sections(topic)
            
            # Step 2: Generate subsections for each main section
            detailed_sections = await self._generate_subsections(main_sections)
            
            # Step 3: Add introduction and conclusion if requested
            if self.config.include_introduction:
                detailed_sections["Introduction"] = await self._generate_introduction(topic)
            
            if self.config.include_conclusion:
                detailed_sections["Conclusion"] = await self._generate_conclusion(topic)
            
            # Step 4: Add FAQs if requested
            if self.config.include_faqs:
                detailed_sections["FAQs"] = await self._generate_faqs(topic)
            
            # Step 5: Add resources if requested
            if self.config.include_resources:
                detailed_sections["Additional Resources"] = await self._generate_resources(topic)
            
            self.outline = detailed_sections
            
            # Step 6: Generate content for each section
            await self._generate_section_contents(topic)
            
            return self.outline
            
        except Exception as err:
            logger.error(f"Failed to generate outline: {err}")
            raise
    
    async def _generate_main_sections(self, topic: str) -> List[str]:
        """Generate main sections for the outline."""
        prompt = f"""Generate {self.config.num_main_sections} main sections for a {self.config.content_type.value} 
        article about {topic} with the following characteristics:
        
        Content Type: {self.config.content_type.value}
        Content Depth: {self.config.content_depth.value}
        Target Word Count: {self.config.target_word_count}
        Target Audience: {self.config.target_audience}
        Style: {self.config.outline_style.value}
        
        Additional Requirements:
        - Each section should contribute to the overall word count goal
        - Sections should flow logically
        - Include key concepts and important points
        - Consider SEO optimization
        - Keywords to include: {', '.join(self.config.keywords or [])}
        - Topics to exclude: {', '.join(self.config.exclude_topics or [])}
        
        Please provide only the section titles, one per line."""
        
        response = await llm_text_gen(prompt)
        return [section.strip() for section in response.split('\n') if section.strip()]
    
    async def _generate_subsections(self, main_sections: List[str]) -> Dict[str, List[str]]:
        """Generate subsections for each main section."""
        detailed_sections = {}
        
        for section in main_sections:
            prompt = f"""Generate {self.config.num_subsections_per_section} subsections for the following section:
            {section}
            
            Content Type: {self.config.content_type.value}
            Content Depth: {self.config.content_depth.value}
            Style: {self.config.outline_style.value}
            
            Each subsection should:
            - Be specific and focused
            - Support the main section's topic
            - Include key points to cover
            - Consider SEO optimization
            
            Please provide only the subsection titles, one per line."""
            
            response = await llm_text_gen(prompt)
            detailed_sections[section] = [sub.strip() for sub in response.split('\n') if sub.strip()]
        
        return detailed_sections
    
    async def _generate_introduction(self, topic: str) -> List[str]:
        """Generate introduction subsections."""
        prompt = f"""Generate introduction subsections for an article about {topic}.
        
        Content Type: {self.config.content_type.value}
        Content Depth: {self.config.content_depth.value}
        Style: {self.config.outline_style.value}
        
        The introduction should:
        - Hook the reader
        - Present the main topic
        - Outline what's to come
        - Set the tone for the article
        
        Please provide only the subsection titles, one per line."""
        
        response = await llm_text_gen(prompt)
        return [sub.strip() for sub in response.split('\n') if sub.strip()]
    
    async def _generate_conclusion(self, topic: str) -> List[str]:
        """Generate conclusion subsections."""
        prompt = f"""Generate conclusion subsections for an article about {topic}.
        
        Content Type: {self.config.content_type.value}
        Content Depth: {self.config.content_depth.value}
        Style: {self.config.outline_style.value}
        
        The conclusion should:
        - Summarize key points
        - Provide final thoughts
        - Include a call to action
        - Leave a lasting impression
        
        Please provide only the subsection titles, one per line."""
        
        response = await llm_text_gen(prompt)
        return [sub.strip() for sub in response.split('\n') if sub.strip()]
    
    async def _generate_faqs(self, topic: str) -> List[str]:
        """Generate FAQ subsections."""
        prompt = f"""Generate FAQ subsections for an article about {topic}.
        
        Content Type: {self.config.content_type.value}
        Content Depth: {self.config.content_depth.value}
        Style: {self.config.outline_style.value}
        
        The FAQs should:
        - Address common questions
        - Cover important aspects
        - Be relevant to the target audience
        - Include both basic and advanced questions
        
        Please provide only the FAQ questions, one per line."""
        
        response = await llm_text_gen(prompt)
        return [sub.strip() for sub in response.split('\n') if sub.strip()]
    
    async def _generate_resources(self, topic: str) -> List[str]:
        """Generate resource subsections."""
        prompt = f"""Generate resource subsections for an article about {topic}.
        
        Content Type: {self.config.content_type.value}
        Content Depth: {self.config.content_depth.value}
        Style: {self.config.outline_style.value}
        
        The resources should:
        - Include relevant links
        - Suggest further reading
        - Provide tools or references
        - Include related materials
        
        Please provide only the resource categories, one per line."""
        
        response = await llm_text_gen(prompt)
        return [sub.strip() for sub in response.split('\n') if sub.strip()]
    
    async def _generate_section_contents(self, topic: str):
        """Generate content and images for each section."""
        for section, subsections in self.outline.items():
            if section not in ["Introduction", "Conclusion", "FAQs", "Additional Resources"]:
                # Generate content for the main section
                content_prompt = f"""Write a detailed section for a blog post about {topic}.
                Section Title: {section}
                Content Type: {self.config.content_type.value}
                Content Depth: {self.config.content_depth.value}
                Style: {self.config.outline_style.value}
                Target Word Count: {self.config.target_word_count // self.config.num_main_sections}
                
                Include:
                - Clear explanation of the main points
                - Examples and illustrations
                - Key takeaways
                - Relevant data or statistics
                """
                
                content = await llm_text_gen(content_prompt)
                
                # Generate image prompt if images are enabled
                image_prompt = None
                image_path = None
                
                if self.config.include_images:
                    image_prompt = f"""Create a detailed image prompt for a blog section about {topic}.
                    Section: {section}
                    Content: {content[:200]}...
                    Style: {self.config.image_style}
                    """
                    
                    image_prompt = await llm_text_gen(image_prompt)
                    try:
                        image_path = generate_image(
                            image_prompt,
                            title=section,
                            description=content[:100],
                            tags=self.config.keywords
                        )
                    except Exception as err:
                        logger.warning(f"Failed to generate image for section {section}: {err}")
                
                self.section_contents[section] = SectionContent(
                    title=section,
                    content=content,
                    image_prompt=image_prompt,
                    image_path=image_path
                )
    
    def to_markdown(self) -> str:
        """Convert outline to markdown format with content and images."""
        markdown = f"# {self.outline.get('Introduction', [''])[0]}\n\n"
        
        for section, subsections in self.outline.items():
            if section not in ["Introduction", "Conclusion", "FAQs", "Additional Resources"]:
                markdown += f"## {section}\n\n"
                
                # Add section content if available
                if section in self.section_contents:
                    content = self.section_contents[section]
                    markdown += f"{content.content}\n\n"
                    
                    # Add image if available
                    if content.image_path:
                        markdown += f"![{section}]({content.image_path})\n\n"
                
                # Add subsections
                for subsection in subsections:
                    markdown += f"- {subsection}\n"
                markdown += "\n"
        
        if "Conclusion" in self.outline:
            markdown += "## Conclusion\n\n"
            for subsection in self.outline["Conclusion"]:
                markdown += f"- {subsection}\n"
            markdown += "\n"
        
        if "FAQs" in self.outline:
            markdown += "## Frequently Asked Questions\n\n"
            for faq in self.outline["FAQs"]:
                markdown += f"- {faq}\n"
            markdown += "\n"
        
        if "Additional Resources" in self.outline:
            markdown += "## Additional Resources\n\n"
            for resource in self.outline["Additional Resources"]:
                markdown += f"- {resource}\n"
        
        return markdown
