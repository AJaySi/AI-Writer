"""Pydantic models for Facebook Post functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class PostGoal(str, Enum):
    """Post goal options."""
    PROMOTE_PRODUCT = "Promote a product/service"
    SHARE_CONTENT = "Share valuable content"
    INCREASE_ENGAGEMENT = "Increase engagement"
    BUILD_AWARENESS = "Build brand awareness"
    DRIVE_TRAFFIC = "Drive website traffic"
    GENERATE_LEADS = "Generate leads"
    ANNOUNCE_NEWS = "Announce news/updates"
    CUSTOM = "Custom"


class PostTone(str, Enum):
    """Post tone options."""
    INFORMATIVE = "Informative"
    HUMOROUS = "Humorous"
    INSPIRATIONAL = "Inspirational"
    UPBEAT = "Upbeat"
    CASUAL = "Casual"
    PROFESSIONAL = "Professional"
    CONVERSATIONAL = "Conversational"
    CUSTOM = "Custom"


class MediaType(str, Enum):
    """Media type options."""
    NONE = "None"
    IMAGE = "Image"
    VIDEO = "Video"
    CAROUSEL = "Carousel"
    LINK_PREVIEW = "Link Preview"


class AdvancedOptions(BaseModel):
    """Advanced post generation options."""
    use_hook: bool = Field(default=True, description="Use attention-grabbing hook")
    use_story: bool = Field(default=True, description="Include storytelling elements")
    use_cta: bool = Field(default=True, description="Add clear call-to-action")
    use_question: bool = Field(default=True, description="Include engagement question")
    use_emoji: bool = Field(default=True, description="Use relevant emojis")
    use_hashtags: bool = Field(default=True, description="Add relevant hashtags")


class FacebookPostRequest(BaseModel):
    """Request model for Facebook post generation."""
    business_type: str = Field(..., description="Type of business (e.g., 'Fitness coach')")
    target_audience: str = Field(..., description="Target audience description (e.g., 'Fitness enthusiasts aged 25-35')")
    post_goal: PostGoal = Field(..., description="Main goal of the post")
    custom_goal: Optional[str] = Field(None, description="Custom goal if 'Custom' is selected")
    post_tone: PostTone = Field(..., description="Tone of the post")
    custom_tone: Optional[str] = Field(None, description="Custom tone if 'Custom' is selected")
    include: Optional[str] = Field(None, description="Elements to include in the post")
    avoid: Optional[str] = Field(None, description="Elements to avoid in the post")
    media_type: MediaType = Field(default=MediaType.NONE, description="Type of media to include")
    advanced_options: AdvancedOptions = Field(default_factory=AdvancedOptions, description="Advanced generation options")


class FacebookPostAnalytics(BaseModel):
    """Analytics predictions for the generated post."""
    expected_reach: str = Field(..., description="Expected reach range")
    expected_engagement: str = Field(..., description="Expected engagement percentage")
    best_time_to_post: str = Field(..., description="Optimal posting time")


class FacebookPostOptimization(BaseModel):
    """Optimization suggestions for the post."""
    suggestions: List[str] = Field(..., description="List of optimization suggestions")


class FacebookPostResponse(BaseModel):
    """Response model for Facebook post generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    content: Optional[str] = Field(None, description="Generated post content")
    analytics: Optional[FacebookPostAnalytics] = Field(None, description="Analytics predictions")
    optimization: Optional[FacebookPostOptimization] = Field(None, description="Optimization suggestions")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")