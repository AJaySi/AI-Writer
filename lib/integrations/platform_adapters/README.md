# Platform Adapters

A flexible and extensible system for managing content across different social media platforms and content management systems.

## Overview

The platform adapters system provides a unified interface for publishing, managing, and analyzing content across multiple platforms. It follows a modular architecture where each platform has its own adapter implementation while maintaining a consistent interface.

## Architecture

### Core Components

1. **Base Platform Adapter (`base.py`)**
   - Abstract base class defining the interface for all platform adapters
   - Common functionality and error handling
   - Standardized response formatting

2. **Platform Manager (`manager.py`)**
   - Central manager for handling multiple platform adapters
   - Platform initialization and configuration
   - Unified content publishing and management

3. **Unified Platform Adapter (`unified.py`)**
   - Content adaptation across different platforms
   - Platform-specific content generation
   - Performance analytics and recommendations

### Current Implementations

#### Twitter Adapter (`twitter.py`)
- Full implementation of Twitter API integration
- Features:
  - Tweet publishing with media support
  - Content validation
  - Analytics and engagement metrics
  - Media upload handling
  - Rate limit management

#### WordPress Adapter (TBD)
- Planned implementation of WordPress REST API integration
- Features:
  - ⏳ Post creation and management
  - ⏳ Page management
  - ⏳ Media library integration
  - ⏳ Category and tag management
  - ⏳ Custom post type support
  - ⏳ SEO metadata management
  - ⏳ Comment moderation
  - ⏳ User management

#### Wix Adapter (TBD)
- Planned implementation of Wix API integration
- Features:
  - ⏳ Blog post management
  - ⏳ Page content management
  - ⏳ Media upload and management
  - ⏳ SEO settings
  - ⏳ Collection management
  - ⏳ Form submissions handling
  - ⏳ Site settings management
  - ⏳ Analytics integration

## Features

### Core Features
- ✅ Multi-platform content publishing
- ✅ Content validation and optimization
- ✅ Analytics and performance tracking
- ✅ Media handling
- ✅ Error handling and logging
- ✅ Platform-specific content adaptation

### Platform-Specific Features

#### Twitter
- ✅ Tweet publishing
- ✅ Media attachments
- ✅ Analytics tracking
- ✅ Content validation
- ✅ Rate limit handling

#### Instagram (TBD)
- ⏳ Post creation
- ⏳ Story publishing
- ⏳ Hashtag optimization
- ⏳ Media handling

#### LinkedIn (TBD)
- ⏳ Post creation
- ⏳ Article publishing
- ⏳ Professional content optimization
- ⏳ Company page integration

#### Facebook (TBD)
- ⏳ Post creation
- ⏳ Page management
- ⏳ Audience targeting
- ⏳ Analytics integration

#### WordPress (TBD)
- ⏳ REST API integration
- ⏳ Content synchronization
- ⏳ Media management
- ⏳ SEO optimization
- ⏳ Custom post types
- ⏳ Plugin integration

#### Wix (TBD)
- ⏳ API integration
- ⏳ Content management
- ⏳ Media handling
- ⏳ SEO settings
- ⏳ Collection management
- ⏳ Analytics integration

## Configuration

Each platform adapter requires specific configuration parameters:

### Twitter Configuration
```python
{
    'api_key': 'your_api_key',
    'api_secret': 'your_api_secret',
    'access_token': 'your_access_token',
    'access_token_secret': 'your_access_token_secret'
}
```

### WordPress Configuration
```python
{
    'site_url': 'https://your-wordpress-site.com',
    'username': 'your_username',
    'application_password': 'your_application_password',
    'api_version': 'v2'
}
```

### Wix Configuration
```python
{
    'site_id': 'your_site_id',
    'api_key': 'your_api_key',
    'access_token': 'your_access_token'
}
```

## Usage

### Basic Usage
```python
from lib.integrations.platform_adapters.manager import PlatformManager

# Initialize platform manager
config = {
    'platforms': {
        'twitter': {
            'api_key': 'your_api_key',
            'api_secret': 'your_api_secret',
            'access_token': 'your_access_token',
            'access_token_secret': 'your_access_token_secret'
        },
        'wordpress': {
            'site_url': 'https://your-wordpress-site.com',
            'username': 'your_username',
            'application_password': 'your_application_password'
        },
        'wix': {
            'site_id': 'your_site_id',
            'api_key': 'your_api_key',
            'access_token': 'your_access_token'
        }
    }
}

manager = PlatformManager(config)

# Publish content
content = {
    'text': 'Hello, World!',
    'media': [
        {
            'url': 'https://example.com/image.jpg',
            'type': 'image'
        }
    ]
}

result = await manager.publish_content(content, platforms=['twitter', 'wordpress', 'wix'])
```

## TBD Features

### Platform Support
- [ ] Instagram adapter implementation
- [ ] LinkedIn adapter implementation
- [ ] Facebook adapter implementation
- [ ] YouTube adapter implementation
- [ ] TikTok adapter implementation
- [ ] WordPress adapter implementation
- [ ] Wix adapter implementation

### Content Management
- [ ] Bulk content publishing
- [ ] Content scheduling
- [ ] Content templates
- [ ] A/B testing support
- [ ] Content versioning
- [ ] Cross-platform content synchronization
- [ ] CMS-specific content optimization

### Analytics
- [ ] Cross-platform analytics
- [ ] Custom metric tracking
- [ ] Automated reporting
- [ ] Performance optimization suggestions
- [ ] ROI tracking
- [ ] CMS-specific analytics integration

### Media Handling
- [ ] Advanced media optimization
- [ ] Media library management
- [ ] Automatic media resizing
- [ ] Media format conversion
- [ ] Media metadata management
- [ ] Cross-platform media synchronization

### Security
- [ ] OAuth2 implementation
- [ ] API key rotation
- [ ] Rate limit handling
- [ ] Error recovery
- [ ] Audit logging
- [ ] CMS-specific security features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## Testing

Each platform adapter should include:
- Unit tests
- Integration tests
- Mock API responses
- Error handling tests
- Rate limit tests
- CMS-specific test cases

## Error Handling

The system implements standardized error handling:
- Platform-specific error mapping
- Retry mechanisms
- Error logging
- User-friendly error messages
- CMS-specific error handling

## Logging

Comprehensive logging system:
- Platform operations
- API calls
- Error tracking
- Performance metrics
- Debug information
- CMS-specific logging

## Dependencies

- Python 3.11+
- tweepy (for Twitter integration)
- requests
- loguru
- typing
- datetime
- wordpress-xmlrpc (for WordPress integration)
- wix-api-client (for Wix integration)