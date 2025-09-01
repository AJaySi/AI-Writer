# ALwrity Story Generators API

This module provides FastAPI endpoints for AI-powered story generation, illustration, and video creation functionality. It replaces the original Streamlit-based implementations with a modern, scalable REST API.

## Features

- **AI Story Writer**: Generate complete stories using prompt chaining and iterative generation
- **AI Story Illustrator**: Create illustrations for stories from text, URLs, or uploaded files
- **AI Story Video Generator**: Generate video scenes with illustrations (scene generation only, full video compilation requires additional libraries)
- **Enhanced Gemini Integration**: Updated Gemini image generation with latest API capabilities
- **Intelligent Logging**: Comprehensive logging with structured output
- **Exception Handling**: Robust error handling with custom exceptions
- **Async Support**: Fully asynchronous operations with progress tracking
- **Job Management**: Background job processing with real-time status updates

## Architecture

```
backend/api/story_generators/
├── __init__.py                 # Main module exports
├── main.py                     # FastAPI app integration
├── README.md                   # This documentation
├── core/                       # Core functionality
│   ├── __init__.py
│   ├── exceptions.py           # Custom exceptions and handlers
│   └── logging.py              # Enhanced logging system
├── schemas/                    # Pydantic models
│   ├── __init__.py
│   ├── story_writer_schemas.py
│   ├── story_illustrator_schemas.py
│   └── story_video_schemas.py
├── services/                   # Business logic
│   ├── __init__.py
│   ├── story_writer_service.py
│   ├── story_illustrator_service.py
│   ├── story_video_service.py
│   └── gemini_image_service.py
└── routers/                    # FastAPI routers
    ├── __init__.py
    ├── story_writer.py
    ├── story_illustrator.py
    └── story_video_generator.py
```

## API Endpoints

### Story Writer

- `POST /api/story-writer/generate` - Generate a story (async with job tracking)
- `GET /api/story-writer/generate-sync` - Generate a story synchronously
- `GET /api/story-writer/status/{job_id}` - Get generation status
- `GET /api/story-writer/stream/{job_id}` - Stream progress updates (SSE)
- `DELETE /api/story-writer/jobs/{job_id}` - Cancel generation job
- `GET /api/story-writer/jobs` - List all jobs
- `GET /api/story-writer/health` - Health check

### Story Illustrator

- `POST /api/story-illustrator/generate` - Generate illustrations (async)
- `POST /api/story-illustrator/upload-file` - Upload file and generate illustrations
- `GET /api/story-illustrator/generate-from-url` - Generate from URL
- `GET /api/story-illustrator/status/{job_id}` - Get generation status
- `GET /api/story-illustrator/stream/{job_id}` - Stream progress updates
- `GET /api/story-illustrator/download/{job_id}` - Download illustrations ZIP
- `GET /api/story-illustrator/illustration/{job_id}/{index}` - Get single illustration
- `DELETE /api/story-illustrator/jobs/{job_id}` - Cancel job
- `GET /api/story-illustrator/jobs` - List all jobs
- `GET /api/story-illustrator/health` - Health check

### Story Video Generator

- `POST /api/story-video-generator/generate` - Generate video scenes (async)
- `GET /api/story-video-generator/generate-scenes-only` - Generate only scenes
- `GET /api/story-video-generator/status/{job_id}` - Get generation status
- `GET /api/story-video-generator/stream/{job_id}` - Stream progress updates
- `GET /api/story-video-generator/scene/{job_id}/{scene_index}` - Get specific scene
- `DELETE /api/story-video-generator/jobs/{job_id}` - Cancel job
- `GET /api/story-video-generator/jobs` - List all jobs
- `GET /api/story-video-generator/health` - Health check

## Usage Examples

### Story Writer

```python
import requests

# Generate a story asynchronously
response = requests.post("http://localhost:8000/api/story-writer/generate", json={
    "persona": "Award-Winning Science Fiction Author",
    "story_setting": "A futuristic city in the year 2150",
    "character_input": "John is a tall, muscular man with a kind heart",
    "plot_elements": "Theme: Good vs. evil. Conflict: Save the world",
    "writing_style": "😎 Casual",
    "story_tone": "⏳ Suspenseful",
    "narrative_pov": "👤 First Person",
    "audience_age_group": "👨‍👩‍👧‍👦 Adults (18+ years)",
    "content_rating": "🌟 G - General Audiences",
    "ending_preference": "😊 Happy Ending"
})

job_id = response.json()["job_id"]

# Check status
status_response = requests.get(f"http://localhost:8000/api/story-writer/status/{job_id}")
print(status_response.json())
```

### Story Illustrator

```python
# Generate illustrations from text
response = requests.post("http://localhost:8000/api/story-illustrator/generate", json={
    "story_input": {
        "text": "Once upon a time in a magical forest..."
    },
    "settings": {
        "style": "fantasy",
        "aspect_ratio": "16:9",
        "quality": "high",
        "max_illustrations": 5
    }
})

# Upload file for illustration
with open("story.txt", "rb") as f:
    files = {"file": f}
    data = {
        "style": "digital art",
        "max_illustrations": 10
    }
    response = requests.post(
        "http://localhost:8000/api/story-illustrator/upload-file",
        files=files,
        data=data
    )
```

### Story Video Generator

```python
# Generate video scenes
response = requests.get("http://localhost:8000/api/story-video-generator/generate-scenes-only", params={
    "story_text": "A brave knight embarked on a quest...",
    "title": "The Knight's Quest",
    "illustration_style": "fantasy",
    "max_scenes": 8,
    "duration_per_scene": 5.0
})

scenes = response.json()["scenes"]
print(f"Generated {len(scenes)} scenes")
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY` - Google Gemini API key (required)
- `OPENAI_API_KEY` - OpenAI API key (optional, for fallback)
- `LOG_LEVEL` - Logging level (default: INFO)

### Gemini Image Generation

The enhanced Gemini image service supports:
- Latest Gemini 2.0 Flash Experimental model
- Multiple art styles and quality levels
- Batch illustration generation
- Automatic prompt enhancement
- Rate limiting and error handling

### Logging

Structured logging with:
- JSON format for machine processing
- Console output for development
- File output for production
- Request/response tracking
- Performance metrics
- Error context

## Migration from Streamlit

The original Streamlit implementations have been migrated to FastAPI with the following improvements:

1. **Scalability**: Async operations with background job processing
2. **API-First**: RESTful endpoints for easy integration
3. **Job Management**: Track long-running operations
4. **Error Handling**: Comprehensive exception handling
5. **Logging**: Enhanced logging with structured output
6. **Documentation**: Auto-generated OpenAPI documentation
7. **Testing**: Built for testability with dependency injection

## Limitations

### Current Implementation

- **Video Compilation**: Full video compilation requires additional libraries (moviepy, ffmpeg)
- **File Formats**: Limited file format support (PDF/Word processing requires additional libraries)
- **Audio Generation**: TTS/narration generation not yet implemented
- **Storage**: Uses local file storage (cloud storage integration recommended for production)

### Future Enhancements

- Full video compilation with transitions and effects
- Advanced file format support
- Text-to-speech integration
- Cloud storage integration
- Batch processing capabilities
- Advanced scene detection and segmentation

## Error Handling

The API uses custom exception types:

- `StoryGenerationError` - Story generation failures
- `IllustrationGenerationError` - Illustration generation failures
- `VideoGenerationError` - Video generation failures
- `InvalidInputError` - Invalid input data
- `ModelConnectionError` - AI model connection issues
- `FileProcessingError` - File processing failures
- `RateLimitError` - API rate limit exceeded

All exceptions are automatically mapped to appropriate HTTP status codes and include detailed error information.

## Performance

### Optimization Features

- Async/await for non-blocking operations
- Connection pooling for AI model APIs
- Rate limiting to prevent API quota exhaustion
- Caching for repeated operations
- Background job processing
- Progress tracking and streaming

### Monitoring

- Request/response logging
- Performance metrics
- Error tracking
- Health check endpoints
- Service status monitoring

## Testing

Run tests with:

```bash
cd backend
python -m pytest api/story_generators/tests/
```

## Deployment

The API is integrated into the main ALwrity backend application. To deploy:

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables
3. Start the application: `python start_alwrity_backend.py`
4. Access documentation at: `http://localhost:8000/docs`

## Support

For issues or questions:
1. Check the logs in `backend/logs/story_generators.jsonl`
2. Use the health check endpoints to verify service status
3. Review the OpenAPI documentation at `/docs`