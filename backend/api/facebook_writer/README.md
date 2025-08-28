# Facebook Writer API

A comprehensive FastAPI-based backend for generating Facebook content using AI. This is a complete migration of the original Streamlit-based Facebook writer to a modern REST API architecture.

## Overview

The Facebook Writer API provides 10 different tools for creating, optimizing, and analyzing Facebook content:

### Content Creation Tools
- **FB Post Generator** - Create engaging Facebook posts with optimization features
- **FB Story Generator** - Generate creative Facebook Stories with visual suggestions  
- **FB Reel Generator** - Create Reels scripts with music and hashtag suggestions
- **Carousel Generator** - Generate multi-slide carousel posts

### Business Tools  
- **Event Description Generator** - Create compelling event descriptions
- **Group Post Generator** - Generate community-focused group posts
- **Page About Generator** - Create professional page About sections

### Marketing Tools
- **Ad Copy Generator** - Generate high-converting ad copy with targeting suggestions
- **Hashtag Generator** - Create relevant and trending hashtags
- **Engagement Analyzer** - Analyze content performance and get optimization tips

## API Architecture

### Directory Structure
```
backend/api/facebook_writer/
├── models/           # Pydantic models for request/response
├── services/         # Business logic and AI integration
├── routers/          # FastAPI route definitions
└── README.md        # This file
```

### Key Components

#### Models (`models/`)
- **Request Models**: Strongly typed input validation using Pydantic
- **Response Models**: Structured output with success/error handling
- **Enum Classes**: Predefined options for dropdowns and selections

#### Services (`services/`)
- **Base Service**: Common functionality and Gemini AI integration
- **Specialized Services**: Individual services for each content type
- **Error Handling**: Consistent error responses across all services

#### Routers (`routers/`)
- **FastAPI Routes**: RESTful endpoints with automatic documentation
- **Request Validation**: Automatic validation using Pydantic models
- **Response Formatting**: Consistent JSON responses

## API Endpoints

### Health & Discovery
- `GET /api/facebook-writer/health` - Health check
- `GET /api/facebook-writer/tools` - List available tools
- `GET /api/facebook-writer/post/templates` - Get post templates
- `GET /api/facebook-writer/analytics/benchmarks` - Get industry benchmarks
- `GET /api/facebook-writer/compliance/guidelines` - Get compliance guidelines

### Content Generation
- `POST /api/facebook-writer/post/generate` - Generate Facebook post
- `POST /api/facebook-writer/story/generate` - Generate Facebook story
- `POST /api/facebook-writer/reel/generate` - Generate Facebook reel
- `POST /api/facebook-writer/carousel/generate` - Generate carousel post
- `POST /api/facebook-writer/event/generate` - Generate event description
- `POST /api/facebook-writer/group-post/generate` - Generate group post
- `POST /api/facebook-writer/page-about/generate` - Generate page about
- `POST /api/facebook-writer/ad-copy/generate` - Generate ad copy
- `POST /api/facebook-writer/hashtags/generate` - Generate hashtags
- `POST /api/facebook-writer/engagement/analyze` - Analyze engagement

## Usage Examples

### Generate a Facebook Post
```python
import requests

payload = {
    "business_type": "Fitness coach",
    "target_audience": "Fitness enthusiasts aged 25-35", 
    "post_goal": "Increase engagement",
    "post_tone": "Inspirational",
    "include": "Success story, workout tips",
    "avoid": "Generic advice",
    "media_type": "Image",
    "advanced_options": {
        "use_hook": True,
        "use_story": True,
        "use_cta": True,
        "use_question": True,
        "use_emoji": True,
        "use_hashtags": True
    }
}

response = requests.post(
    "http://localhost:8000/api/facebook-writer/post/generate",
    json=payload
)

if response.status_code == 200:
    data = response.json()
    print(f"Generated post: {data['content']}")
    print(f"Expected reach: {data['analytics']['expected_reach']}")
```

### Generate Ad Copy
```python
payload = {
    "business_type": "E-commerce store",
    "product_service": "Wireless headphones",
    "ad_objective": "Conversions",
    "ad_format": "Single image",
    "target_audience": "Tech enthusiasts and music lovers",
    "targeting_options": {
        "age_group": "25-34",
        "interests": "Technology, Music",
        "location": "United States"
    },
    "unique_selling_proposition": "Premium sound at affordable prices",
    "budget_range": "Medium"
}

response = requests.post(
    "http://localhost:8000/api/facebook-writer/ad-copy/generate", 
    json=payload
)
```

## Setup & Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Running the Server
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Testing
```bash
python test_facebook_writer.py
```

## AI Integration

The API uses Google's Gemini AI through the existing `gemini_provider` service:

- **Text Generation**: For creating content
- **Structured Output**: For complex responses with multiple fields
- **Error Handling**: Robust retry logic and fallbacks
- **Temperature Control**: Optimized for different content types

## Migration Notes

This FastAPI backend replaces the original Streamlit interface while maintaining all functionality:

### ✅ Migrated Features
- All 10 Facebook writer tools
- AI content generation using Gemini
- Advanced options and customization
- Analytics predictions
- Optimization suggestions
- Error handling and validation

### 🔄 Architecture Changes
- **UI Framework**: Streamlit → FastAPI REST API
- **Input Handling**: Streamlit widgets → Pydantic models
- **Output Format**: Streamlit display → JSON responses
- **State Management**: Session state → Stateless API
- **Integration**: Direct function calls → HTTP endpoints

### 🎯 Benefits
- **Scalability**: Can handle multiple concurrent requests
- **Integration**: Easy to integrate with React frontend
- **Documentation**: Automatic OpenAPI/Swagger docs
- **Testing**: Comprehensive test coverage
- **Deployment**: Standard FastAPI deployment options

## API Documentation

When the server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Error Handling

All endpoints return consistent error responses:
```json
{
    "success": false,
    "error": "Detailed error message",
    "content": null,
    "metadata": {
        "operation": "operation_name",
        "error_type": "ValueError"
    }
}
```

## Performance

- **Response Time**: ~2-5 seconds for content generation
- **Concurrency**: Supports multiple simultaneous requests
- **Rate Limiting**: Handled by Gemini API quotas
- **Caching**: Consider implementing for repeated requests

## Next Steps

1. **Frontend Integration**: Connect React UI to these endpoints
2. **Authentication**: Add user authentication and authorization  
3. **Rate Limiting**: Implement API rate limiting
4. **Caching**: Add Redis for caching generated content
5. **Monitoring**: Add logging and metrics collection
6. **Testing**: Expand test coverage for edge cases