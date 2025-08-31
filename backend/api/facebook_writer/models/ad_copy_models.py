"""Pydantic models for Facebook Ad Copy functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class AdObjective(str, Enum):
    """Ad objective options."""
    BRAND_AWARENESS = "Brand awareness"
    REACH = "Reach"
    TRAFFIC = "Traffic"
    ENGAGEMENT = "Engagement"
    APP_INSTALLS = "App installs"
    VIDEO_VIEWS = "Video views"
    LEAD_GENERATION = "Lead generation"
    MESSAGES = "Messages"
    CONVERSIONS = "Conversions"
    CATALOG_SALES = "Catalog sales"
    STORE_TRAFFIC = "Store traffic"
    CUSTOM = "Custom"


class AdFormat(str, Enum):
    """Ad format options."""
    SINGLE_IMAGE = "Single image"
    SINGLE_VIDEO = "Single video"
    CAROUSEL = "Carousel"
    SLIDESHOW = "Slideshow"
    COLLECTION = "Collection"
    INSTANT_EXPERIENCE = "Instant experience"


class TargetAge(str, Enum):
    """Target age groups."""
    TEENS = "13-17"
    YOUNG_ADULTS = "18-24"
    MILLENNIALS = "25-34"
    GEN_X = "35-44"
    MIDDLE_AGED = "45-54"
    SENIORS = "55-64"
    ELDERLY = "65+"
    CUSTOM = "Custom"


class AdBudget(str, Enum):
    """Ad budget ranges."""
    SMALL = "$10-50/day"
    MEDIUM = "$50-200/day"
    LARGE = "$200-1000/day"
    ENTERPRISE = "$1000+/day"
    CUSTOM = "Custom"


class TargetingOptions(BaseModel):
    """Targeting options for the ad."""
    age_group: TargetAge = Field(..., description="Target age group")
    custom_age: Optional[str] = Field(None, description="Custom age range if 'Custom' is selected")
    gender: Optional[str] = Field(None, description="Gender targeting")
    location: Optional[str] = Field(None, description="Geographic targeting")
    interests: Optional[str] = Field(None, description="Interest-based targeting")
    behaviors: Optional[str] = Field(None, description="Behavior-based targeting")
    lookalike_audience: Optional[str] = Field(None, description="Lookalike audience description")


class FacebookAdCopyRequest(BaseModel):
    """Request model for Facebook ad copy generation."""
    business_type: str = Field(..., description="Type of business")
    product_service: str = Field(..., description="Product or service being advertised")
    ad_objective: AdObjective = Field(..., description="Main objective of the ad campaign")
    custom_objective: Optional[str] = Field(None, description="Custom objective if 'Custom' is selected")
    ad_format: AdFormat = Field(..., description="Format of the ad")
    target_audience: str = Field(..., description="Target audience description")
    targeting_options: TargetingOptions = Field(..., description="Detailed targeting options")
    unique_selling_proposition: str = Field(..., description="What makes your offer unique")
    offer_details: Optional[str] = Field(None, description="Special offers, discounts, or promotions")
    budget_range: AdBudget = Field(..., description="Ad budget range")
    custom_budget: Optional[str] = Field(None, description="Custom budget if 'Custom' is selected")
    campaign_duration: Optional[str] = Field(None, description="How long the campaign will run")
    competitor_analysis: Optional[str] = Field(None, description="Information about competitor ads")
    brand_voice: Optional[str] = Field(None, description="Brand voice and tone guidelines")
    compliance_requirements: Optional[str] = Field(None, description="Any compliance or regulatory requirements")


class AdCopyVariations(BaseModel):
    """Different variations of ad copy."""
    headline_variations: List[str] = Field(..., description="Multiple headline options")
    primary_text_variations: List[str] = Field(..., description="Multiple primary text options")
    description_variations: List[str] = Field(..., description="Multiple description options")
    cta_variations: List[str] = Field(..., description="Multiple call-to-action options")


class AdPerformancePredictions(BaseModel):
    """Predicted ad performance metrics."""
    estimated_reach: str = Field(..., description="Estimated reach")
    estimated_ctr: str = Field(..., description="Estimated click-through rate")
    estimated_cpc: str = Field(..., description="Estimated cost per click")
    estimated_conversions: str = Field(..., description="Estimated conversions")
    optimization_score: str = Field(..., description="Overall optimization score")


class FacebookAdCopyResponse(BaseModel):
    """Response model for Facebook ad copy generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    primary_ad_copy: Optional[Dict[str, str]] = Field(None, description="Primary ad copy with headline, text, description")
    ad_variations: Optional[AdCopyVariations] = Field(None, description="Multiple variations for A/B testing")
    targeting_suggestions: Optional[List[str]] = Field(None, description="Additional targeting suggestions")
    creative_suggestions: Optional[List[str]] = Field(None, description="Creative and visual suggestions")
    performance_predictions: Optional[AdPerformancePredictions] = Field(None, description="Performance predictions")
    optimization_tips: Optional[List[str]] = Field(None, description="Optimization tips for better performance")
    compliance_notes: Optional[List[str]] = Field(None, description="Compliance and policy considerations")
    budget_recommendations: Optional[List[str]] = Field(None, description="Budget allocation recommendations")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")