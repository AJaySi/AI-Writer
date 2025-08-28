"""Pydantic models for Facebook Reel functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ReelType(str, Enum):
    """Reel type options."""
    PRODUCT_DEMO = "Product demonstration"
    TUTORIAL = "Tutorial/How-to"
    ENTERTAINMENT = "Entertainment"
    EDUCATIONAL = "Educational"
    TREND_BASED = "Trend-based"
    BEHIND_SCENES = "Behind the scenes"
    USER_GENERATED = "User-generated content"
    CUSTOM = "Custom"


class ReelLength(str, Enum):
    """Reel length options."""
    SHORT = "15-30 seconds"
    MEDIUM = "30-60 seconds"
    LONG = "60-90 seconds"


class ReelStyle(str, Enum):
    """Reel style options."""
    FAST_PACED = "Fast-paced"
    RELAXED = "Relaxed"
    DRAMATIC = "Dramatic"
    MINIMALIST = "Minimalist"
    VIBRANT = "Vibrant"
    CUSTOM = "Custom"


class FacebookReelRequest(BaseModel):
    """Request model for Facebook reel generation."""
    business_type: str = Field(..., description="Type of business")
    target_audience: str = Field(..., description="Target audience description")
    reel_type: ReelType = Field(..., description="Type of reel to create")
    custom_reel_type: Optional[str] = Field(None, description="Custom reel type if 'Custom' is selected")
    reel_length: ReelLength = Field(..., description="Desired length of the reel")
    reel_style: ReelStyle = Field(..., description="Style of the reel")
    custom_style: Optional[str] = Field(None, description="Custom style if 'Custom' is selected")
    topic: str = Field(..., description="Main topic or focus of the reel")
    include: Optional[str] = Field(None, description="Elements to include in the reel")
    avoid: Optional[str] = Field(None, description="Elements to avoid in the reel")
    music_preference: Optional[str] = Field(None, description="Music style preference")


class FacebookReelResponse(BaseModel):
    """Response model for Facebook reel generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    script: Optional[str] = Field(None, description="Generated reel script")
    scene_breakdown: Optional[List[str]] = Field(None, description="Scene-by-scene breakdown")
    music_suggestions: Optional[List[str]] = Field(None, description="Music suggestions")
    hashtag_suggestions: Optional[List[str]] = Field(None, description="Hashtag suggestions")
    engagement_tips: Optional[List[str]] = Field(None, description="Engagement optimization tips")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")