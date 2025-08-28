"""Pydantic models for Facebook Carousel functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class CarouselType(str, Enum):
    """Carousel type options."""
    PRODUCT_SHOWCASE = "Product showcase"
    STEP_BY_STEP = "Step-by-step guide"
    BEFORE_AFTER = "Before/After"
    TESTIMONIALS = "Customer testimonials"
    FEATURES_BENEFITS = "Features & Benefits"
    PORTFOLIO = "Portfolio showcase"
    EDUCATIONAL = "Educational content"
    CUSTOM = "Custom"


class CarouselSlide(BaseModel):
    """Individual carousel slide content."""
    title: str = Field(..., description="Slide title")
    content: str = Field(..., description="Slide content/description")
    image_description: Optional[str] = Field(None, description="Description of the image for this slide")


class FacebookCarouselRequest(BaseModel):
    """Request model for Facebook carousel generation."""
    business_type: str = Field(..., description="Type of business")
    target_audience: str = Field(..., description="Target audience description")
    carousel_type: CarouselType = Field(..., description="Type of carousel to create")
    custom_carousel_type: Optional[str] = Field(None, description="Custom carousel type if 'Custom' is selected")
    topic: str = Field(..., description="Main topic or theme of the carousel")
    num_slides: int = Field(default=5, ge=3, le=10, description="Number of slides (3-10)")
    include_cta: bool = Field(default=True, description="Include call-to-action in final slide")
    cta_text: Optional[str] = Field(None, description="Custom call-to-action text")
    brand_colors: Optional[str] = Field(None, description="Brand colors to mention for design")
    include: Optional[str] = Field(None, description="Elements to include")
    avoid: Optional[str] = Field(None, description="Elements to avoid")


class FacebookCarouselResponse(BaseModel):
    """Response model for Facebook carousel generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    main_caption: Optional[str] = Field(None, description="Main caption for the carousel post")
    slides: Optional[List[CarouselSlide]] = Field(None, description="Generated carousel slides")
    design_suggestions: Optional[List[str]] = Field(None, description="Design and layout suggestions")
    hashtag_suggestions: Optional[List[str]] = Field(None, description="Hashtag suggestions")
    engagement_tips: Optional[List[str]] = Field(None, description="Engagement optimization tips")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")