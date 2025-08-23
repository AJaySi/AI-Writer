# ALwrity Social Media Integration Setup Guide

This guide explains how to set up and configure the social media integration system in ALwrity, allowing users to connect their social media accounts and Google Search Console for analytics and automated posting.

## Overview

The social media integration system provides:

- **OAuth2 Authentication** for secure platform connections
- **Google Search Console Integration** for SEO analytics and insights
- **Social Media Posting** to Facebook, Twitter, LinkedIn, and YouTube
- **Analytics Fetching** from connected platforms
- **Secure Token Management** with encryption
- **User-Friendly Onboarding** step in the wizard

## Architecture

### Backend Components

1. **Models** (`/backend/models/social_connections.py`)
   - `SocialConnection`: Stores OAuth tokens and connection metadata
   - `SocialPost`: Tracks posted content and analytics
   - `SocialAnalytics`: Stores fetched analytics data

2. **Services**
   - `oauth_service.py`: Handles OAuth flows for all platforms
   - `gsc_analytics_service.py`: Google Search Console data fetching
   - `social_posting_service.py`: Content posting to social platforms

3. **API Endpoints** (`/backend/api/social_connections.py`)
   - OAuth initiation and callback handling
   - Connection management
   - Analytics retrieval
   - Content posting

### Frontend Components

1. **Social Connections Step** (`/frontend/src/components/OnboardingWizard/SocialConnectionsStep.tsx`)
   - Platform connection interface
   - OAuth popup handling
   - Live GSC data demonstration

## Setup Instructions

### 1. Install Dependencies

Add the required packages to your backend:

```bash
pip install authlib httpx google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client cryptography
```

### 2. Environment Variables

Add the following environment variables to your `.env` file:

```env
# OAuth Encryption Key (generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
OAUTH_ENCRYPTION_KEY=your_encryption_key_here

# Google OAuth (for GSC and YouTube)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/oauth/callback/google

# Facebook OAuth
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/oauth/callback/facebook

# Twitter OAuth
TWITTER_CLIENT_ID=your_twitter_client_id
TWITTER_CLIENT_SECRET=your_twitter_client_secret
TWITTER_REDIRECT_URI=http://localhost:8000/api/oauth/callback/twitter

# LinkedIn OAuth
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8000/api/oauth/callback/linkedin
```

### 3. Platform-Specific Setup

#### Google Search Console & YouTube

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Search Console API
   - YouTube Data API v3
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/oauth/callback/google`
5. Copy Client ID and Client Secret to your `.env` file

**Required Scopes:**
- Google Search Console: `https://www.googleapis.com/auth/webmasters`
- YouTube: `https://www.googleapis.com/auth/youtube`

#### Facebook

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or use existing one
3. Add Facebook Login product
4. Configure OAuth redirect URIs: `http://localhost:8000/api/oauth/callback/facebook`
5. Request the following permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
   - `business_management`
   - `read_insights`

#### Twitter/X

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Set up OAuth 2.0 with PKCE
4. Configure callback URL: `http://localhost:8000/api/oauth/callback/twitter`
5. Request the following scopes:
   - `tweet.read`
   - `tweet.write`
   - `users.read`
   - `offline.access`

#### LinkedIn

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create a new app
3. Add Sign In with LinkedIn product
4. Configure redirect URL: `http://localhost:8000/api/oauth/callback/linkedin`
5. Request the following scopes:
   - `w_member_social`
   - `r_liteprofile`
   - `r_emailaddress`

### 4. Database Migration

The social media tables will be created automatically when you run the application. The models include:

- `social_connections`: OAuth tokens and connection metadata
- `social_posts`: Posted content tracking
- `social_analytics`: Analytics data storage

### 5. Update Main Application

The social connections router is already integrated into the main FastAPI application (`app.py`).

## Usage

### 1. User Onboarding

Users will see a new "Social Media" step in the onboarding wizard where they can:

- Connect Google Search Console for SEO analytics
- Connect social media platforms for posting and analytics
- View live data from connected platforms

### 2. API Endpoints

#### Connect Platform
```bash
GET /api/social/auth/{platform}?user_id=1
```

#### Get Connections
```bash
GET /api/social/connections?user_id=1
```

#### Post Content
```bash
POST /api/social/connections/{connection_id}/post
{
  "content": "Your post content here",
  "media_urls": ["optional_image_url"],
  "scheduled_at": "2024-01-01T12:00:00"
}
```

#### Get GSC Analytics
```bash
GET /api/social/gsc/{connection_id}/analytics/performance?site_url=https://example.com
```

### 3. Security Features

- **Token Encryption**: All OAuth tokens are encrypted before database storage
- **Scope Validation**: Only requested permissions are granted
- **Token Refresh**: Automatic token refresh for expired credentials
- **Secure State Management**: CSRF protection for OAuth flows

## Troubleshooting

### Common Issues

1. **OAuth Errors**
   - Verify redirect URIs match exactly in platform settings
   - Check that all required scopes are requested
   - Ensure client credentials are correct

2. **GSC Connection Issues**
   - User must have Search Console access to the website
   - Website must be verified in Search Console
   - API must be enabled in Google Cloud Console

3. **Token Expiration**
   - System automatically refreshes tokens when possible
   - Users may need to reconnect if refresh tokens expire

### Development Testing

1. Use ngrok for local HTTPS testing:
   ```bash
   ngrok http 8000
   ```

2. Update redirect URIs to use ngrok URL

3. Test OAuth flows with different platforms

## Future Enhancements

- **Scheduled Posting**: Implement job queue for scheduled posts
- **Analytics Dashboard**: Create comprehensive analytics visualization
- **Content Templates**: Platform-specific content optimization
- **Batch Operations**: Multiple platform posting in one action
- **Advanced Permissions**: Granular permission management

## API Reference

### Social Connection Model
```python
{
  "id": 1,
  "platform": "google_search_console",
  "platform_username": "GSC User (2 sites)",
  "connection_status": "active",
  "auto_post_enabled": false,
  "analytics_enabled": true,
  "connected_at": "2024-01-01T12:00:00Z",
  "profile_data": {
    "sites": [...]
  }
}
```

### Post Content Model
```python
{
  "content": "Your content here",
  "media_urls": ["url1", "url2"],
  "scheduled_at": "2024-01-01T12:00:00Z"
}
```

### Analytics Response Model
```python
{
  "success": true,
  "data": {
    "site_url": "https://example.com",
    "totals": {
      "clicks": 1000,
      "impressions": 5000,
      "ctr": 0.2,
      "position": 15.5
    },
    "daily_data": [...]
  }
}
```

## Support

For issues or questions about the social media integration:

1. Check the logs for specific error messages
2. Verify platform API credentials and permissions
3. Ensure all required environment variables are set
4. Test with individual platforms to isolate issues

The integration is designed to be robust and handle various error conditions gracefully, providing clear feedback to users when issues occur.