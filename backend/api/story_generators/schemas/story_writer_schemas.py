"""
Pydantic schemas for AI Story Writer endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class WritingStyle(str, Enum):
    FORMAL = "🧐 Formal"
    CASUAL = "😎 Casual" 
    POETIC = "🎼 Poetic"
    HUMOROUS = "😂 Humorous"


class StoryTone(str, Enum):
    DARK = "🌑 Dark"
    UPLIFTING = "☀️ Uplifting"
    SUSPENSEFUL = "⏳ Suspenseful"
    WHIMSICAL = "🎈 Whimsical"


class NarrativePOV(str, Enum):
    FIRST_PERSON = "👤 First Person"
    THIRD_PERSON_LIMITED = "👥 Third Person Limited"
    THIRD_PERSON_OMNISCIENT = "👁️ Third Person Omniscient"


class AudienceAgeGroup(str, Enum):
    CHILDREN = "👶 Children (5-10 years)"
    YOUNG_ADULTS = "🧒 Young Adults (11-17 years)"
    ADULTS = "👨‍👩‍👧‍👦 Adults (18+ years)"
    ALL_AGES = "🌍 All Ages"


class ContentRating(str, Enum):
    G = "🌟 G - General Audiences"
    PG = "👨‍👩‍👧‍👦 PG - Parental Guidance"
    PG13 = "🔞 PG-13 - Parents Strongly Cautioned"
    R = "⚠️ R - Restricted"


class EndingPreference(str, Enum):
    HAPPY = "😊 Happy Ending"
    TRAGIC = "😢 Tragic Ending"
    OPEN = "🤔 Open Ending"
    TWIST = "🌀 Twist Ending"


class StoryWriterRequest(BaseModel):
    """Request schema for story writing."""
    
    persona: str = Field(
        ...,
        description="The writing persona/author type to use",
        example="Award-Winning Science Fiction Author"
    )
    story_setting: str = Field(
        ...,
        description="The setting where the story takes place",
        example="A bustling futuristic city with towering skyscrapers and flying cars, set in the year 2150"
    )
    character_input: str = Field(
        ...,
        description="Information about the main characters",
        example="John is a tall, muscular man with a kind heart. Xishan is a clever and resourceful woman. Amol is a mischievous and energetic young boy."
    )
    plot_elements: str = Field(
        ...,
        description="Plot elements including theme, key events, and main conflict",
        example="Theme: Good vs. evil. Key Events: The hero meets the villain, faces challenges. Main Conflict: Save the world from a powerful enemy."
    )
    writing_style: WritingStyle = Field(
        ...,
        description="The writing style for the story"
    )
    story_tone: StoryTone = Field(
        ...,
        description="The overall tone or mood of the story"
    )
    narrative_pov: NarrativePOV = Field(
        ...,
        description="The narrative point of view"
    )
    audience_age_group: AudienceAgeGroup = Field(
        ...,
        description="Target audience age group"
    )
    content_rating: ContentRating = Field(
        ...,
        description="Content rating for the story"
    )
    ending_preference: EndingPreference = Field(
        ...,
        description="Preferred type of ending"
    )


class StoryWriterResponse(BaseModel):
    """Response schema for story writing."""
    
    success: bool = Field(..., description="Whether the story generation was successful")
    story: Optional[str] = Field(None, description="The generated story text")
    premise: Optional[str] = Field(None, description="The story premise")
    outline: Optional[str] = Field(None, description="The story outline")
    word_count: Optional[int] = Field(None, description="Word count of the generated story")
    character_count: Optional[int] = Field(None, description="Character count of the generated story")
    error_message: Optional[str] = Field(None, description="Error message if generation failed")


class StoryGenerationStatus(BaseModel):
    """Schema for story generation status updates."""
    
    status: str = Field(..., description="Current status of story generation")
    progress: float = Field(..., description="Progress percentage (0-100)")
    current_step: str = Field(..., description="Current step in the generation process")
    draft_length: Optional[int] = Field(None, description="Current draft length in characters")
    estimated_completion_time: Optional[int] = Field(None, description="Estimated completion time in seconds")