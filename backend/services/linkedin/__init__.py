"""
LinkedIn Services Package

This package provides comprehensive LinkedIn content generation and management services
including content generation, image generation, and various LinkedIn-specific utilities.
"""

# Import existing services
from .content_generator import ContentGenerator
from .content_generator_prompts import (
    PostPromptBuilder,
    ArticlePromptBuilder,
    CarouselPromptBuilder,
    VideoScriptPromptBuilder,
    CommentResponsePromptBuilder,
    CarouselGenerator,
    VideoScriptGenerator
)

# Import new image generation services
from .image_generation import (
    LinkedInImageGenerator,
    LinkedInImageEditor,
    LinkedInImageStorage
)
from .image_prompts import LinkedInPromptGenerator

__all__ = [
    # Content Generation
    'ContentGenerator',
    
    # Prompt Builders
    'PostPromptBuilder',
    'ArticlePromptBuilder', 
    'CarouselPromptBuilder',
    'VideoScriptPromptBuilder',
    'CommentResponsePromptBuilder',
    
    # Specialized Generators
    'CarouselGenerator',
    'VideoScriptGenerator',
    
    # Image Generation Services
    'LinkedInImageGenerator',
    'LinkedInImageEditor',
    'LinkedInImageStorage',
    'LinkedInPromptGenerator'
]

# Version information
__version__ = "2.0.0"
__author__ = "Alwrity Team"
__description__ = "LinkedIn Content and Image Generation Services"
