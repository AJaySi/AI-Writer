"""Pydantic models for Facebook Engagement Analysis functionality."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ContentType(str, Enum):
    """Content type options for analysis."""
    POST = "Post"
    STORY = "Story"
    REEL = "Reel"
    CAROUSEL = "Carousel"
    VIDEO = "Video"
    IMAGE = "Image"
    LINK = "Link"


class AnalysisType(str, Enum):
    """Analysis type options."""
    CONTENT_ANALYSIS = "Content analysis"
    PERFORMANCE_PREDICTION = "Performance prediction"
    OPTIMIZATION_SUGGESTIONS = "Optimization suggestions"
    COMPETITOR_COMPARISON = "Competitor comparison"
    TREND_ANALYSIS = "Trend analysis"


class FacebookEngagementRequest(BaseModel):
    """Request model for Facebook engagement analysis."""
    content: str = Field(..., description="Content to analyze")
    content_type: ContentType = Field(..., description="Type of content being analyzed")
    analysis_type: AnalysisType = Field(..., description="Type of analysis to perform")
    business_type: str = Field(..., description="Type of business")
    target_audience: str = Field(..., description="Target audience description")
    post_timing: Optional[str] = Field(None, description="When the content was/will be posted")
    hashtags: Optional[List[str]] = Field(None, description="Hashtags used with the content")
    competitor_content: Optional[str] = Field(None, description="Competitor content for comparison")
    historical_performance: Optional[Dict[str, Any]] = Field(None, description="Historical performance data")


class EngagementMetrics(BaseModel):
    """Engagement metrics and predictions."""
    predicted_reach: str = Field(..., description="Predicted reach")
    predicted_engagement_rate: str = Field(..., description="Predicted engagement rate")
    predicted_likes: str = Field(..., description="Predicted likes")
    predicted_comments: str = Field(..., description="Predicted comments")
    predicted_shares: str = Field(..., description="Predicted shares")
    virality_score: str = Field(..., description="Virality potential score")


class OptimizationSuggestions(BaseModel):
    """Content optimization suggestions."""
    content_improvements: List[str] = Field(..., description="Content improvement suggestions")
    timing_suggestions: List[str] = Field(..., description="Posting time optimization")
    hashtag_improvements: List[str] = Field(..., description="Hashtag optimization suggestions")
    visual_suggestions: List[str] = Field(..., description="Visual element suggestions")
    engagement_tactics: List[str] = Field(..., description="Engagement boosting tactics")


class FacebookEngagementResponse(BaseModel):
    """Response model for Facebook engagement analysis."""
    success: bool = Field(..., description="Whether the analysis was successful")
    content_score: Optional[float] = Field(None, description="Overall content quality score (0-100)")
    engagement_metrics: Optional[EngagementMetrics] = Field(None, description="Predicted engagement metrics")
    optimization_suggestions: Optional[OptimizationSuggestions] = Field(None, description="Optimization recommendations")
    sentiment_analysis: Optional[Dict[str, Any]] = Field(None, description="Content sentiment analysis")
    trend_alignment: Optional[Dict[str, Any]] = Field(None, description="Alignment with current trends")
    competitor_insights: Optional[Dict[str, Any]] = Field(None, description="Competitor comparison insights")
    error: Optional[str] = Field(None, description="Error message if analysis failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the analysis")