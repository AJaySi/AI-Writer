"""
Story Generators API Module

This module provides FastAPI endpoints for AI-powered story generation,
illustration, and video creation functionality.
"""

from .routers.story_writer import router as story_writer_router
from .routers.story_illustrator import router as story_illustrator_router
from .routers.story_video_generator import router as story_video_generator_router

__all__ = [
    'story_writer_router',
    'story_illustrator_router', 
    'story_video_generator_router'
]