"""Pydantic models for Facebook Story functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class StoryType(str, Enum):
    """Story type options."""
    PRODUCT_SHOWCASE = "Product showcase"
    BEHIND_SCENES = "Behind the scenes"
    USER_TESTIMONIAL = "User testimonial"
    EVENT_PROMOTION = "Event promotion"
    TUTORIAL = "Tutorial/How-to"
    QUESTION_POLL = "Question/Poll"
    ANNOUNCEMENT = "Announcement"
    CUSTOM = "Custom"


class StoryTone(str, Enum):
    """Story tone options."""
    CASUAL = "Casual"
    FUN = "Fun"
    PROFESSIONAL = "Professional"
    INSPIRATIONAL = "Inspirational"
    EDUCATIONAL = "Educational"
    ENTERTAINING = "Entertaining"
    CUSTOM = "Custom"


class StoryVisualOptions(BaseModel):
    """Visual options for story."""
    background_type: str = Field(default="Solid color", description="Background type")
    text_overlay: bool = Field(default=True, description="Include text overlay")
    stickers: bool = Field(default=True, description="Use stickers/emojis")
    interactive_elements: bool = Field(default=True, description="Include polls/questions")


class FacebookStoryRequest(BaseModel):
    """Request model for Facebook story generation."""
    business_type: str = Field(..., description="Type of business")
    target_audience: str = Field(..., description="Target audience description")
    story_type: StoryType = Field(..., description="Type of story to create")
    custom_story_type: Optional[str] = Field(None, description="Custom story type if 'Custom' is selected")
    story_tone: StoryTone = Field(..., description="Tone of the story")
    custom_tone: Optional[str] = Field(None, description="Custom tone if 'Custom' is selected")
    include: Optional[str] = Field(None, description="Elements to include in the story")
    avoid: Optional[str] = Field(None, description="Elements to avoid in the story")
    visual_options: StoryVisualOptions = Field(default_factory=StoryVisualOptions, description="Visual customization options")


class FacebookStoryResponse(BaseModel):
    """Response model for Facebook story generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    content: Optional[str] = Field(None, description="Generated story content")
    visual_suggestions: Optional[List[str]] = Field(None, description="Visual element suggestions")
    engagement_tips: Optional[List[str]] = Field(None, description="Engagement optimization tips")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")