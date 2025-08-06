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
import json

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
        
    def generate_outline(self, topic: str) -> Dict[str, List[str]]:
        """Generate a blog outline based on the topic and configuration."""
        try:
            # Create a focused prompt for outline generation
            prompt = f"""Generate a blog outline for topic: {topic}

Content Type: {self.config.content_type.value}
Target Audience: {self.config.target_audience}
Content Depth: {self.config.content_depth.value}
Style: {self.config.outline_style.value}
Word Count Target: {self.config.target_word_count}
Main Sections: {self.config.num_main_sections}
Subsections per Section: {self.config.num_subsections_per_section}

Requirements:
- Create exactly {self.config.num_main_sections} main sections
- Each section should have exactly {self.config.num_subsections_per_section} subsections
- Focus on {self.config.content_type.value} content style
- Target {self.config.target_audience} audience
- Maintain {self.config.content_depth.value} depth
- Follow {self.config.outline_style.value} style
- Optimize for {self.config.target_word_count} words total

IMPORTANT: You must return a valid JSON object with main sections as keys and lists of subsections as values.
Example format: {{"Section 1": ["Subsection 1.1", "Subsection 1.2"], "Section 2": ["Subsection 2.1", "Subsection 2.2"]}}
Do not include any additional text or explanations, only the JSON object."""

            # Get outline from LLM
            outline_json = llm_text_gen(prompt)
            
            # Clean the response to ensure it's valid JSON
            outline_json = outline_json.strip()
            if not outline_json.startswith('{'):
                outline_json = outline_json[outline_json.find('{'):]
            if not outline_json.endswith('}'):
                outline_json = outline_json[:outline_json.rfind('}')+1]
            
            # Parse the outline
            try:
                outline = json.loads(outline_json)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
                logger.error(f"Raw response: {outline_json}")
                # Fallback to a basic outline structure
                outline = {
                    f"Section {i+1}": [f"Subsection {i+1}.{j+1}" for j in range(self.config.num_subsections_per_section)]
                    for i in range(self.config.num_main_sections)
                }
            
            # Add introduction and conclusion if configured
            if self.config.include_introduction:
                outline = {"Introduction": ["Overview", "Importance", "What to Expect"]} | outline
            
            if self.config.include_conclusion:
                outline["Conclusion"] = ["Summary", "Key Takeaways", "Next Steps"]
            
            # Add FAQs if configured
            if self.config.include_faqs:
                # Generate topic-specific FAQs
                faq_prompt = f"""Generate 3 specific and relevant FAQ questions for a blog post about: {topic}

Content Type: {self.config.content_type.value}
Target Audience: {self.config.target_audience}
Content Depth: {self.config.content_depth.value}

Requirements:
- Questions should be specific to the topic
- Cover common concerns and important aspects
- Be relevant to the target audience
- Include both basic and advanced questions

Format: Return only a JSON array of 3 questions.
Example format: ["Question 1?", "Question 2?", "Question 3?"]"""

                try:
                    faq_json = llm_text_gen(faq_prompt)
                    faq_json = faq_json.strip()
                    if not faq_json.startswith('['):
                        faq_json = faq_json[faq_json.find('['):]
                    if not faq_json.endswith(']'):
                        faq_json = faq_json[:faq_json.rfind(']')+1]
                    
                    faqs = json.loads(faq_json)
                    outline["Frequently Asked Questions"] = faqs
                except Exception as e:
                    logger.error(f"Error generating FAQs: {str(e)}")
                    outline["Frequently Asked Questions"] = [
                        f"Common Question about {topic} 1",
                        f"Common Question about {topic} 2",
                        f"Common Question about {topic} 3"
                    ]
            
            # Add resources if configured
            if self.config.include_resources:
                outline["Additional Resources"] = [
                    "Further Reading",
                    "Tools and References",
                    "Related Topics"
                ]
            
            return outline
            
        except Exception as e:
            logger.error(f"Error generating outline: {str(e)}")
            return {}

    def generate_section_content(self, section: str, subsections: List[str]) -> Optional[SectionContent]:
        """Generate content for a section."""
        try:
            # Create a focused prompt for content generation
            prompt = f"""Generate content for section: {section}

Subsections: {', '.join(subsections)}
Content Type: {self.config.content_type.value}
Target Audience: {self.config.target_audience}
Content Depth: {self.config.content_depth.value}
Style: {self.config.outline_style.value}
Word Count Target: {self.config.target_word_count // self.config.num_main_sections}

Requirements:
- Write content for each subsection
- Maintain {self.config.content_depth.value} depth
- Target {self.config.target_audience} audience
- Follow {self.config.outline_style.value} style
- Optimize for {self.config.target_word_count // self.config.num_main_sections} words
- Include relevant examples and data points
- Use clear, engaging language

Format: Return only a JSON object with 'content' and 'image_prompt' fields.
Example format: {{"content": "Section content here...", "image_prompt": "Image description here..."}}"""

            # Get content from LLM
            content_json = llm_text_gen(prompt)
            content_data = json.loads(content_json)
            
            # Generate image if configured
            image_path = None
            if self.config.include_images:
                image_path = self.generate_section_image(section)
            
            return SectionContent(
                title=section,
                content=content_data["content"],
                image_prompt=content_data.get("image_prompt"),
                image_path=image_path
            )
            
        except Exception as e:
            logger.error(f"Error generating content for section {section}: {str(e)}")
            return None

    def generate_section_image(self, section: str) -> Optional[str]:
        """Generate an image for a section."""
        try:
            # Create a focused prompt for image generation
            prompt = f"""Generate an image prompt for section: {section}

Style: {self.config.image_style}
Engine: {self.config.image_engine}
Content Type: {self.config.content_type.value}
Target Audience: {self.config.target_audience}

Requirements:
- Create a {self.config.image_style} style image
- Optimize for {self.config.image_engine} engine
- Match {self.config.content_type.value} content type
- Appeal to {self.config.target_audience} audience
- Be visually engaging and relevant

Format: Return only a JSON object with an 'image_prompt' field.
Example format: {{"image_prompt": "Detailed image description here..."}}"""

            # Get image prompt from LLM
            prompt_json = llm_text_gen(prompt)
            prompt_data = json.loads(prompt_json)
            
            # Generate image using the specified engine
            if self.config.image_engine == "Gemini-AI":
                image_path = generate_gemini_image(prompt_data["image_prompt"])
            elif self.config.image_engine == "Dalle3":
                image_path = generate_dalle_image(prompt_data["image_prompt"])
            else:  # Stability-AI
                image_path = generate_stability_image(prompt_data["image_prompt"])
            
            return image_path
            
        except Exception as e:
            logger.error(f"Error generating image for section {section}: {str(e)}")
            return None

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
