"""
LinkedIn Content Generation Models for ALwrity

This module defines the data models for LinkedIn content generation endpoints.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class LinkedInPostType(str, Enum):
    """Types of LinkedIn posts."""
    PROFESSIONAL = "professional"
    THOUGHT_LEADERSHIP = "thought_leadership"
    INDUSTRY_NEWS = "industry_news"
    PERSONAL_STORY = "personal_story"
    COMPANY_UPDATE = "company_update"
    POLL = "poll"


class LinkedInTone(str, Enum):
    """LinkedIn content tone options."""
    PROFESSIONAL = "professional"
    CONVERSATIONAL = "conversational"
    AUTHORITATIVE = "authoritative"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"
    FRIENDLY = "friendly"


class SearchEngine(str, Enum):
    """Available search engines for research."""
    METAPHOR = "metaphor"
    GOOGLE = "google"
    TAVILY = "tavily"


class LinkedInPostRequest(BaseModel):
    """Request model for LinkedIn post generation."""
    topic: str = Field(..., description="Main topic for the post", min_length=3, max_length=200)
    industry: str = Field(..., description="Target industry context", min_length=2, max_length=100)
    post_type: LinkedInPostType = Field(default=LinkedInPostType.PROFESSIONAL, description="Type of LinkedIn post")
    tone: LinkedInTone = Field(default=LinkedInTone.PROFESSIONAL, description="Tone of the post")
    target_audience: Optional[str] = Field(None, description="Specific target audience", max_length=200)
    key_points: Optional[List[str]] = Field(None, description="Key points to include", max_items=10)
    include_hashtags: bool = Field(default=True, description="Whether to include hashtags")
    include_call_to_action: bool = Field(default=True, description="Whether to include call to action")
    research_enabled: bool = Field(default=True, description="Whether to include research-backed content")
    search_engine: SearchEngine = Field(default=SearchEngine.METAPHOR, description="Search engine for research")
    max_length: int = Field(default=3000, description="Maximum character count", ge=100, le=3000)
    
    class Config:
        schema_extra = {
            "example": {
                "topic": "AI in healthcare transformation",
                "industry": "Healthcare",
                "post_type": "thought_leadership",
                "tone": "professional",
                "target_audience": "Healthcare executives and professionals",
                "key_points": ["AI diagnostics", "Patient outcomes", "Cost reduction"],
                "include_hashtags": True,
                "include_call_to_action": True,
                "research_enabled": True,
                "search_engine": "metaphor",
                "max_length": 2000
            }
        }


class LinkedInArticleRequest(BaseModel):
    """Request model for LinkedIn article generation."""
    topic: str = Field(..., description="Main topic for the article", min_length=3, max_length=200)
    industry: str = Field(..., description="Target industry context", min_length=2, max_length=100)
    tone: LinkedInTone = Field(default=LinkedInTone.PROFESSIONAL, description="Tone of the article")
    target_audience: Optional[str] = Field(None, description="Specific target audience", max_length=200)
    key_sections: Optional[List[str]] = Field(None, description="Key sections to include", max_items=10)
    include_images: bool = Field(default=True, description="Whether to generate image suggestions")
    seo_optimization: bool = Field(default=True, description="Whether to include SEO optimization")
    research_enabled: bool = Field(default=True, description="Whether to include research-backed content")
    search_engine: SearchEngine = Field(default=SearchEngine.METAPHOR, description="Search engine for research")
    word_count: int = Field(default=1500, description="Target word count", ge=500, le=5000)
    
    class Config:
        schema_extra = {
            "example": {
                "topic": "Digital transformation in manufacturing",
                "industry": "Manufacturing",
                "tone": "professional",
                "target_audience": "Manufacturing leaders and technology professionals",
                "key_sections": ["Current challenges", "Technology solutions", "Implementation strategies"],
                "include_images": True,
                "seo_optimization": True,
                "research_enabled": True,
                "search_engine": "metaphor",
                "word_count": 2000
            }
        }


class LinkedInCarouselRequest(BaseModel):
    """Request model for LinkedIn carousel post generation."""
    topic: str = Field(..., description="Main topic for the carousel", min_length=3, max_length=200)
    industry: str = Field(..., description="Target industry context", min_length=2, max_length=100)
    slide_count: int = Field(default=8, description="Number of slides", ge=3, le=15)
    tone: LinkedInTone = Field(default=LinkedInTone.PROFESSIONAL, description="Tone of the carousel")
    target_audience: Optional[str] = Field(None, description="Specific target audience", max_length=200)
    key_takeaways: Optional[List[str]] = Field(None, description="Key takeaways to include", max_items=10)
    include_cover_slide: bool = Field(default=True, description="Whether to include a cover slide")
    include_cta_slide: bool = Field(default=True, description="Whether to include a call-to-action slide")
    visual_style: Optional[str] = Field("modern", description="Visual style preference")
    
    class Config:
        schema_extra = {
            "example": {
                "topic": "5 Ways to Improve Team Productivity",
                "industry": "Business Management",
                "slide_count": 8,
                "tone": "professional",
                "target_audience": "Team leaders and managers",
                "key_takeaways": ["Clear communication", "Goal setting", "Tool optimization"],
                "include_cover_slide": True,
                "include_cta_slide": True,
                "visual_style": "modern"
            }
        }


class LinkedInVideoScriptRequest(BaseModel):
    """Request model for LinkedIn video script generation."""
    topic: str = Field(..., description="Main topic for the video", min_length=3, max_length=200)
    industry: str = Field(..., description="Target industry context", min_length=2, max_length=100)
    video_length: int = Field(default=60, description="Target video length in seconds", ge=15, le=300)
    tone: LinkedInTone = Field(default=LinkedInTone.PROFESSIONAL, description="Tone of the video")
    target_audience: Optional[str] = Field(None, description="Specific target audience", max_length=200)
    key_messages: Optional[List[str]] = Field(None, description="Key messages to include", max_items=5)
    include_hook: bool = Field(default=True, description="Whether to include an attention-grabbing hook")
    include_captions: bool = Field(default=True, description="Whether to include caption suggestions")
    
    class Config:
        schema_extra = {
            "example": {
                "topic": "Quick tips for remote team management",
                "industry": "Human Resources",
                "video_length": 90,
                "tone": "conversational",
                "target_audience": "Remote team managers",
                "key_messages": ["Communication tools", "Regular check-ins", "Team building"],
                "include_hook": True,
                "include_captions": True
            }
        }


class LinkedInCommentResponseRequest(BaseModel):
    """Request model for LinkedIn comment response generation."""
    original_post: str = Field(..., description="Content of the original post", min_length=10, max_length=3000)
    comment: str = Field(..., description="Comment to respond to", min_length=1, max_length=1000)
    response_type: Literal["professional", "appreciative", "clarifying", "disagreement", "value_add"] = Field(
        default="professional", description="Type of response"
    )
    tone: LinkedInTone = Field(default=LinkedInTone.PROFESSIONAL, description="Tone of the response")
    include_question: bool = Field(default=False, description="Whether to include a follow-up question")
    brand_voice: Optional[str] = Field(None, description="Specific brand voice guidelines", max_length=500)
    
    class Config:
        schema_extra = {
            "example": {
                "original_post": "Just published an article about AI transformation in healthcare...",
                "comment": "Great insights! How do you see this affecting smaller healthcare providers?",
                "response_type": "value_add",
                "tone": "professional",
                "include_question": True,
                "brand_voice": "Expert but approachable, data-driven"
            }
        }


class ResearchSource(BaseModel):
    """Model for research source information."""
    title: str
    url: str
    content: str
    relevance_score: Optional[float] = None


class HashtagSuggestion(BaseModel):
    """Model for hashtag suggestions."""
    hashtag: str
    category: str
    popularity_score: Optional[float] = None


class ImageSuggestion(BaseModel):
    """Model for image suggestions."""
    description: str
    alt_text: str
    style: Optional[str] = None
    placement: Optional[str] = None


class PostContent(BaseModel):
    """Model for generated post content."""
    content: str
    character_count: int
    hashtags: List[HashtagSuggestion]
    call_to_action: Optional[str] = None
    engagement_prediction: Optional[Dict[str, Any]] = None


class ArticleContent(BaseModel):
    """Model for generated article content."""
    title: str
    content: str
    word_count: int
    sections: List[Dict[str, str]]
    seo_metadata: Optional[Dict[str, Any]] = None
    image_suggestions: List[ImageSuggestion]
    reading_time: Optional[int] = None


class CarouselSlide(BaseModel):
    """Model for carousel slide content."""
    slide_number: int
    title: str
    content: str
    visual_elements: List[str]
    design_notes: Optional[str] = None


class CarouselContent(BaseModel):
    """Model for generated carousel content."""
    title: str
    slides: List[CarouselSlide]
    cover_slide: Optional[CarouselSlide] = None
    cta_slide: Optional[CarouselSlide] = None
    design_guidelines: Dict[str, str]


class VideoScript(BaseModel):
    """Model for video script content."""
    hook: str
    main_content: List[Dict[str, str]]  # scene_number, content, duration, visual_notes
    conclusion: str
    captions: Optional[List[str]] = None
    thumbnail_suggestions: List[str]
    video_description: str


class LinkedInPostResponse(BaseModel):
    """Response model for LinkedIn post generation."""
    success: bool = True
    data: Optional[PostContent] = None
    research_sources: List[ResearchSource] = []
    generation_metadata: Dict[str, Any] = {}
    error: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "content": "🚀 AI is revolutionizing healthcare...",
                    "character_count": 1250,
                    "hashtags": [
                        {"hashtag": "#AIinHealthcare", "category": "industry", "popularity_score": 0.9},
                        {"hashtag": "#DigitalTransformation", "category": "general", "popularity_score": 0.8}
                    ],
                    "call_to_action": "What's your experience with AI in healthcare? Share in the comments!",
                    "engagement_prediction": {"estimated_likes": 120, "estimated_comments": 15}
                },
                "research_sources": [
                    {
                        "title": "AI in Healthcare: Current Trends",
                        "url": "https://example.com/ai-healthcare",
                        "content": "Summary of AI healthcare trends...",
                        "relevance_score": 0.95
                    }
                ],
                "generation_metadata": {
                    "model_used": "gemini-2.0-flash-001",
                    "generation_time": 3.2,
                    "research_time": 5.1
                }
            }
        }


class LinkedInArticleResponse(BaseModel):
    """Response model for LinkedIn article generation."""
    success: bool = True
    data: Optional[ArticleContent] = None
    research_sources: List[ResearchSource] = []
    generation_metadata: Dict[str, Any] = {}
    error: Optional[str] = None


class LinkedInCarouselResponse(BaseModel):
    """Response model for LinkedIn carousel generation."""
    success: bool = True
    data: Optional[CarouselContent] = None
    generation_metadata: Dict[str, Any] = {}
    error: Optional[str] = None


class LinkedInVideoScriptResponse(BaseModel):
    """Response model for LinkedIn video script generation."""
    success: bool = True
    data: Optional[VideoScript] = None
    generation_metadata: Dict[str, Any] = {}
    error: Optional[str] = None


class LinkedInCommentResponseResult(BaseModel):
    """Response model for LinkedIn comment response generation."""
    success: bool = True
    response: Optional[str] = None
    alternative_responses: List[str] = []
    tone_analysis: Optional[Dict[str, Any]] = None
    generation_metadata: Dict[str, Any] = {}
    error: Optional[str] = None