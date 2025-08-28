"""Pydantic models for Facebook Event functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class EventType(str, Enum):
    """Event type options."""
    WORKSHOP = "Workshop"
    WEBINAR = "Webinar"
    CONFERENCE = "Conference"
    NETWORKING = "Networking event"
    PRODUCT_LAUNCH = "Product launch"
    SALE_PROMOTION = "Sale/Promotion"
    COMMUNITY = "Community event"
    EDUCATION = "Educational event"
    CUSTOM = "Custom"


class EventFormat(str, Enum):
    """Event format options."""
    IN_PERSON = "In-person"
    VIRTUAL = "Virtual"
    HYBRID = "Hybrid"


class FacebookEventRequest(BaseModel):
    """Request model for Facebook event generation."""
    event_name: str = Field(..., description="Name of the event")
    event_type: EventType = Field(..., description="Type of event")
    custom_event_type: Optional[str] = Field(None, description="Custom event type if 'Custom' is selected")
    event_format: EventFormat = Field(..., description="Format of the event")
    business_type: str = Field(..., description="Type of business hosting the event")
    target_audience: str = Field(..., description="Target audience for the event")
    event_date: Optional[str] = Field(None, description="Event date (YYYY-MM-DD format)")
    event_time: Optional[str] = Field(None, description="Event time")
    location: Optional[str] = Field(None, description="Event location (physical address or virtual platform)")
    duration: Optional[str] = Field(None, description="Event duration")
    key_benefits: Optional[str] = Field(None, description="Key benefits or highlights of attending")
    speakers: Optional[str] = Field(None, description="Key speakers or presenters")
    agenda: Optional[str] = Field(None, description="Brief agenda or schedule")
    ticket_info: Optional[str] = Field(None, description="Ticket pricing and availability")
    special_offers: Optional[str] = Field(None, description="Special offers or early bird discounts")
    include: Optional[str] = Field(None, description="Additional elements to include")
    avoid: Optional[str] = Field(None, description="Elements to avoid")


class FacebookEventResponse(BaseModel):
    """Response model for Facebook event generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    event_title: Optional[str] = Field(None, description="Generated event title")
    event_description: Optional[str] = Field(None, description="Generated event description")
    short_description: Optional[str] = Field(None, description="Short version for social media")
    key_highlights: Optional[List[str]] = Field(None, description="Key event highlights")
    call_to_action: Optional[str] = Field(None, description="Call-to-action text")
    hashtag_suggestions: Optional[List[str]] = Field(None, description="Hashtag suggestions")
    promotion_tips: Optional[List[str]] = Field(None, description="Event promotion tips")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")