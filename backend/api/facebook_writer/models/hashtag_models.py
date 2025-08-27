"""Pydantic models for Facebook Hashtag functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class HashtagPurpose(str, Enum):
    """Hashtag purpose options."""
    BRAND_AWARENESS = "Brand awareness"
    ENGAGEMENT = "Engagement"
    REACH = "Reach expansion"
    COMMUNITY = "Community building"
    TREND = "Trend participation"
    PRODUCT_PROMOTION = "Product promotion"
    EVENT_PROMOTION = "Event promotion"
    CUSTOM = "Custom"


class HashtagCategory(str, Enum):
    """Hashtag category options."""
    BRANDED = "Branded hashtags"
    TRENDING = "Trending hashtags"
    INDUSTRY = "Industry-specific"
    LOCATION = "Location-based"
    LIFESTYLE = "Lifestyle"
    COMMUNITY = "Community hashtags"


class FacebookHashtagRequest(BaseModel):
    """Request model for Facebook hashtag generation."""
    business_type: str = Field(..., description="Type of business")
    industry: str = Field(..., description="Industry or niche")
    target_audience: str = Field(..., description="Target audience description")
    purpose: HashtagPurpose = Field(..., description="Purpose of the hashtags")
    custom_purpose: Optional[str] = Field(None, description="Custom purpose if 'Custom' is selected")
    content_topic: str = Field(..., description="Topic or theme of the content")
    location: Optional[str] = Field(None, description="Location if relevant for local hashtags")
    brand_name: Optional[str] = Field(None, description="Brand name for branded hashtags")
    campaign_name: Optional[str] = Field(None, description="Campaign name if applicable")
    hashtag_count: int = Field(default=10, ge=5, le=30, description="Number of hashtags to generate")
    include_categories: List[HashtagCategory] = Field(default_factory=list, description="Categories to include")


class FacebookHashtagResponse(BaseModel):
    """Response model for Facebook hashtag generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    hashtags: Optional[List[str]] = Field(None, description="Generated hashtags")
    categorized_hashtags: Optional[Dict[str, List[str]]] = Field(None, description="Hashtags organized by category")
    trending_hashtags: Optional[List[str]] = Field(None, description="Currently trending relevant hashtags")
    usage_tips: Optional[List[str]] = Field(None, description="Tips for using hashtags effectively")
    performance_predictions: Optional[Dict[str, str]] = Field(None, description="Predicted performance for different hashtag sets")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")