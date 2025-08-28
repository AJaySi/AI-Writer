"""Pydantic models for Facebook Page About functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class BusinessCategory(str, Enum):
    """Business category options."""
    RETAIL = "Retail"
    RESTAURANT = "Restaurant/Food"
    HEALTH_FITNESS = "Health & Fitness"
    EDUCATION = "Education"
    TECHNOLOGY = "Technology"
    CONSULTING = "Consulting"
    CREATIVE = "Creative Services"
    NONPROFIT = "Non-profit"
    ENTERTAINMENT = "Entertainment"
    REAL_ESTATE = "Real Estate"
    AUTOMOTIVE = "Automotive"
    BEAUTY = "Beauty & Personal Care"
    FINANCE = "Finance"
    TRAVEL = "Travel & Tourism"
    CUSTOM = "Custom"


class PageTone(str, Enum):
    """Page tone options."""
    PROFESSIONAL = "Professional"
    FRIENDLY = "Friendly"
    INNOVATIVE = "Innovative"
    TRUSTWORTHY = "Trustworthy"
    CREATIVE = "Creative"
    APPROACHABLE = "Approachable"
    AUTHORITATIVE = "Authoritative"
    CUSTOM = "Custom"


class ContactInfo(BaseModel):
    """Contact information for the page."""
    website: Optional[str] = Field(None, description="Website URL")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    address: Optional[str] = Field(None, description="Physical address")
    hours: Optional[str] = Field(None, description="Business hours")


class FacebookPageAboutRequest(BaseModel):
    """Request model for Facebook page about generation."""
    business_name: str = Field(..., description="Name of the business")
    business_category: BusinessCategory = Field(..., description="Category of business")
    custom_category: Optional[str] = Field(None, description="Custom category if 'Custom' is selected")
    business_description: str = Field(..., description="Brief description of what the business does")
    target_audience: str = Field(..., description="Target audience description")
    unique_value_proposition: str = Field(..., description="What makes the business unique")
    services_products: str = Field(..., description="Main services or products offered")
    company_history: Optional[str] = Field(None, description="Brief company history or founding story")
    mission_vision: Optional[str] = Field(None, description="Mission statement or vision")
    achievements: Optional[str] = Field(None, description="Key achievements or awards")
    page_tone: PageTone = Field(..., description="Desired tone for the page")
    custom_tone: Optional[str] = Field(None, description="Custom tone if 'Custom' is selected")
    contact_info: ContactInfo = Field(default_factory=ContactInfo, description="Contact information")
    keywords: Optional[str] = Field(None, description="Important keywords to include")
    call_to_action: Optional[str] = Field(None, description="Primary call-to-action")


class FacebookPageAboutResponse(BaseModel):
    """Response model for Facebook page about generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    short_description: Optional[str] = Field(None, description="Short description (under 155 characters)")
    long_description: Optional[str] = Field(None, description="Detailed about section")
    company_overview: Optional[str] = Field(None, description="Company overview section")
    mission_statement: Optional[str] = Field(None, description="Mission statement")
    story_section: Optional[str] = Field(None, description="Company story/history section")
    services_section: Optional[str] = Field(None, description="Services/products section")
    cta_suggestions: Optional[List[str]] = Field(None, description="Call-to-action suggestions")
    keyword_optimization: Optional[List[str]] = Field(None, description="SEO keyword suggestions")
    completion_tips: Optional[List[str]] = Field(None, description="Tips for completing the page")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")