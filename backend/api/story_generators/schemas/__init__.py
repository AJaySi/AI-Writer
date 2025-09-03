"""
Story Generators Schemas

Pydantic models for request/response validation.
"""

from .story_writer_schemas import (
    StoryWriterRequest,
    StoryWriterResponse,
    StoryGenerationStatus,
    WritingStyle,
    StoryTone,
    NarrativePOV,
    AudienceAgeGroup,
    ContentRating,
    EndingPreference
)

from .story_illustrator_schemas import (
    StoryIllustratorRequest,
    StoryIllustratorResponse,
    IllustrationProgress,
    StoryInput,
    IllustrationSettings,
    IllustrationData,
    IllustrationStyle,
    AspectRatio,
    ImageQuality
)

from .story_video_schemas import (
    StoryVideoRequest,
    StoryVideoResponse,
    VideoGenerationProgress,
    VideoGenerationJob,
    SceneData,
    VideoSettings,
    AudioSettings,
    VideoFormat,
    VideoQuality,
    TransitionType
)

__all__ = [
    # Story Writer
    'StoryWriterRequest',
    'StoryWriterResponse', 
    'StoryGenerationStatus',
    'WritingStyle',
    'StoryTone',
    'NarrativePOV',
    'AudienceAgeGroup',
    'ContentRating',
    'EndingPreference',
    
    # Story Illustrator
    'StoryIllustratorRequest',
    'StoryIllustratorResponse',
    'IllustrationProgress',
    'StoryInput',
    'IllustrationSettings',
    'IllustrationData',
    'IllustrationStyle',
    'AspectRatio',
    'ImageQuality',
    
    # Story Video Generator
    'StoryVideoRequest',
    'StoryVideoResponse',
    'VideoGenerationProgress',
    'VideoGenerationJob',
    'SceneData',
    'VideoSettings',
    'AudioSettings',
    'VideoFormat',
    'VideoQuality',
    'TransitionType'
]