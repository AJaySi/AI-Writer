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
    # Background layer
    background_type: str = Field(default="Solid color", description="Background type (Solid color, Gradient, Image, Video)")
    background_image_prompt: Optional[str] = Field(None, description="If background_type is Image/Video, describe desired visual")
    gradient_style: Optional[str] = Field(None, description="Gradient style if gradient background is chosen")

    # Text overlay styling
    text_overlay: bool = Field(default=True, description="Include text overlay")
    text_style: Optional[str] = Field(None, description="Headline/Subtext style, e.g., Bold, Minimal, Handwritten")
    text_color: Optional[str] = Field(None, description="Preferred text color or palette")
    text_position: Optional[str] = Field(None, description="Top/Center/Bottom; Left/Center/Right")

    # Embellishments and interactivity
    stickers: bool = Field(default=True, description="Use stickers/emojis")
    interactive_elements: bool = Field(default=True, description="Include polls/questions")
    interactive_types: Optional[List[str]] = Field(
        default=None,
        description="List of interactive types like ['poll','quiz','slider','countdown']"
    )

    # CTA overlay
    call_to_action: Optional[str] = Field(None, description="Optional CTA copy to place on story")


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
    # Advanced text generation options (parity with original Streamlit module)
    use_hook: bool = Field(default=True, description="Start with a hook to grab attention")
    use_story: bool = Field(default=True, description="Use a short narrative arc")
    use_cta: bool = Field(default=True, description="Include a call to action")
    use_question: bool = Field(default=True, description="Ask a question to spur interaction")
    use_emoji: bool = Field(default=True, description="Use emojis where appropriate")
    use_hashtags: bool = Field(default=True, description="Include relevant hashtags in copy")


class FacebookStoryResponse(BaseModel):
    """Response model for Facebook story generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    content: Optional[str] = Field(None, description="Generated story content")
    images_base64: Optional[List[str]] = Field(None, description="List of base64-encoded story images (PNG)")
    visual_suggestions: Optional[List[str]] = Field(None, description="Visual element suggestions")
    engagement_tips: Optional[List[str]] = Field(None, description="Engagement optimization tips")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")