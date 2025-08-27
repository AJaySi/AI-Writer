"""Pydantic models for Facebook Group Post functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class GroupType(str, Enum):
    """Group type options."""
    INDUSTRY = "Industry/Professional"
    HOBBY = "Hobby/Interest"
    LOCAL = "Local community"
    SUPPORT = "Support group"
    EDUCATIONAL = "Educational"
    BUSINESS = "Business networking"
    LIFESTYLE = "Lifestyle"
    CUSTOM = "Custom"


class PostPurpose(str, Enum):
    """Post purpose in group."""
    SHARE_KNOWLEDGE = "Share knowledge"
    ASK_QUESTION = "Ask question"
    PROMOTE_BUSINESS = "Promote business"
    BUILD_RELATIONSHIPS = "Build relationships"
    PROVIDE_VALUE = "Provide value"
    SEEK_ADVICE = "Seek advice"
    ANNOUNCE_NEWS = "Announce news"
    CUSTOM = "Custom"


class GroupRules(BaseModel):
    """Group rules and guidelines."""
    no_promotion: bool = Field(default=False, description="No promotion allowed")
    value_first: bool = Field(default=True, description="Must provide value first")
    no_links: bool = Field(default=False, description="No external links allowed")
    community_focused: bool = Field(default=True, description="Must be community-focused")
    relevant_only: bool = Field(default=True, description="Only relevant content allowed")


class FacebookGroupPostRequest(BaseModel):
    """Request model for Facebook group post generation."""
    group_name: str = Field(..., description="Name of the Facebook group")
    group_type: GroupType = Field(..., description="Type of group")
    custom_group_type: Optional[str] = Field(None, description="Custom group type if 'Custom' is selected")
    post_purpose: PostPurpose = Field(..., description="Purpose of the post")
    custom_purpose: Optional[str] = Field(None, description="Custom purpose if 'Custom' is selected")
    business_type: str = Field(..., description="Your business type")
    topic: str = Field(..., description="Main topic or subject of the post")
    target_audience: str = Field(..., description="Target audience within the group")
    value_proposition: str = Field(..., description="What value are you providing to the group")
    group_rules: GroupRules = Field(default_factory=GroupRules, description="Group rules to follow")
    include: Optional[str] = Field(None, description="Elements to include")
    avoid: Optional[str] = Field(None, description="Elements to avoid")
    call_to_action: Optional[str] = Field(None, description="Desired call-to-action")


class FacebookGroupPostResponse(BaseModel):
    """Response model for Facebook group post generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    content: Optional[str] = Field(None, description="Generated group post content")
    engagement_starters: Optional[List[str]] = Field(None, description="Questions or prompts to encourage engagement")
    value_highlights: Optional[List[str]] = Field(None, description="Key value points highlighted in the post")
    community_guidelines: Optional[List[str]] = Field(None, description="How the post follows community guidelines")
    follow_up_suggestions: Optional[List[str]] = Field(None, description="Suggestions for follow-up engagement")
    relationship_building_tips: Optional[List[str]] = Field(None, description="Tips for building relationships in the group")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the generation")