# ALwrity Social Media Integration - Comprehensive Guide

## 🚀 Overview

ALwrity's social media integration is a comprehensive, secure, and scalable solution that enables users to connect their social media accounts and Google Search Console for automated content posting and analytics retrieval. This guide covers the complete implementation with all security features, testing capabilities, and debugging tools.

## 🏗️ Architecture Overview

### Core Components

1. **OAuth Service** - Handles authentication for all platforms
2. **Connection Testing Service** - Validates and tests connections
3. **Security Service** - Implements security measures and best practices
4. **Social Posting Service** - Manages content posting across platforms
5. **GSC Analytics Service** - Handles Google Search Console data
6. **Logging Service** - Comprehensive debugging and monitoring

### Supported Platforms

| Platform | Status | Features | OAuth Type |
|----------|--------|----------|------------|
| Google Search Console | ✅ Full | Analytics, Site Management | OAuth2 |
| YouTube | ✅ Full | Channel Management, Analytics | OAuth2 |
| Facebook | ✅ Full | Page Posting, Analytics | OAuth2 |
| Instagram | ✅ Full | Photo/Video Posting, Analytics | OAuth2 (via Facebook) |
| Twitter/X | ✅ Full | Tweet Posting, Analytics | OAuth2 |
| LinkedIn | ✅ Full | Professional Posting, Analytics | OAuth2 |
| TikTok | ✅ Beta | Video Management, Analytics | OAuth2 |
| Pinterest | ✅ Beta | Pin Management, Analytics | OAuth2 |
| Snapchat | ✅ Beta | Ad Management, Analytics | OAuth2 |
| Reddit | ✅ Beta | Community Posting, Analytics | OAuth2 |
| Discord | ✅ Beta | Server Management, Analytics | OAuth2 |

## 🛡️ Security Features

### 1. OAuth Security
- **CSRF Protection**: State parameter validation
- **Token Encryption**: Fernet encryption for stored tokens
- **Automatic Token Refresh**: Seamless token renewal
- **Scope Validation**: Minimal required permissions
- **Redirect URI Validation**: Prevents open redirect attacks

### 2. Rate Limiting
- **IP-based Rate Limiting**: Per-IP request limits
- **Endpoint-specific Limits**: Different limits for different endpoints
- **OAuth-specific Limits**: Stricter limits for authentication endpoints
- **Sliding Window**: Time-based rate limiting

### 3. Security Middleware
- **Input Sanitization**: Automatic input cleaning
- **IP Blocking**: Automatic blocking of malicious IPs
- **Security Headers**: Comprehensive security headers
- **Webhook Validation**: Signature validation for webhooks

### 4. Logging & Monitoring
- **Structured Logging**: JSON-formatted logs
- **Security Event Logging**: Track all security events
- **Performance Monitoring**: Track API performance
- **Error Tracking**: Comprehensive error logging

## 🧪 Testing & Validation

### Connection Testing Features

Each connected platform undergoes comprehensive testing:

1. **Basic Connection Test**
   - Token validity check
   - Expiration status
   - Refresh token availability

2. **Platform-specific Tests**
   - API endpoint accessibility
   - Permission validation
   - Data retrieval capability

3. **Performance Testing**
   - Response time measurement
   - Error rate tracking
   - Success rate monitoring

### Frontend Testing Interface

- **Real-time Status Updates**: Live connection status
- **Error Display**: Detailed error messages
- **Test Results**: Comprehensive test reports
- **Benefits Messaging**: Platform-specific benefits

## 📊 Analytics & Insights

### Google Search Console Integration
- **Site Management**: View and manage verified sites
- **Search Performance**: Clicks, impressions, CTR, position
- **Query Analysis**: Top performing search queries
- **Page Performance**: Best performing pages
- **Index Status**: Page indexing information

### Social Media Analytics
- **Engagement Metrics**: Likes, shares, comments
- **Reach Analysis**: Post reach and impressions
- **Audience Insights**: Demographics and behavior
- **Performance Trends**: Historical performance data

## 🔧 Configuration

### Environment Variables

```bash
# Core OAuth Settings
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/social/oauth/callback/google

FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/social/oauth/callback/facebook

TWITTER_CLIENT_ID=your_twitter_client_id
TWITTER_CLIENT_SECRET=your_twitter_client_secret
TWITTER_REDIRECT_URI=http://localhost:8000/api/social/oauth/callback/twitter

LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8000/api/social/oauth/callback/linkedin

# Security Settings
ENCRYPTION_KEY=your_32_byte_base64_key
WEBHOOK_SECRET=your_webhook_secret
MAX_CONNECTIONS_PER_USER=20
RATE_LIMIT_WINDOW=300
MAX_REQUESTS_PER_WINDOW=10
MAX_FAILED_ATTEMPTS=5
LOCKOUT_DURATION=3600

# Logging Settings
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_DIR=logs

# Frontend Settings
FRONTEND_DOMAIN=localhost:3000
```

### Platform Setup Instructions

#### Google (GSC + YouTube)

1. **Create Google Cloud Project**
   ```bash
   # Visit Google Cloud Console
   https://console.cloud.google.com/
   ```

2. **Enable APIs**
   - Google Search Console API
   - YouTube Data API v3

3. **Configure OAuth Consent Screen**
   - Add your domain
   - Set up privacy policy
   - Add test users (for development)

4. **Create OAuth 2.0 Credentials**
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/social/oauth/callback/google`

#### Facebook (Facebook + Instagram)

1. **Create Facebook App**
   ```bash
   # Visit Facebook Developers
   https://developers.facebook.com/
   ```

2. **Add Products**
   - Facebook Login
   - Instagram Basic Display (for Instagram)

3. **Configure OAuth Settings**
   - Valid OAuth Redirect URIs: `http://localhost:8000/api/social/oauth/callback/facebook`

#### Twitter/X

1. **Create Twitter App**
   ```bash
   # Visit Twitter Developer Portal
   https://developer.twitter.com/
   ```

2. **Configure OAuth 2.0**
   - Type of App: Web App
   - Callback URL: `http://localhost:8000/api/social/oauth/callback/twitter`

#### LinkedIn

1. **Create LinkedIn App**
   ```bash
   # Visit LinkedIn Developer Portal
   https://developer.linkedin.com/
   ```

2. **Add Products**
   - Sign In with LinkedIn
   - Share on LinkedIn

3. **Configure OAuth**
   - Redirect URLs: `http://localhost:8000/api/social/oauth/callback/linkedin`

## 🚀 Quick Start

### 1. Installation

```bash
# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your OAuth credentials
nano .env
```

### 3. Database Migration

```bash
# Initialize database with social media tables
python -c "from services.database import init_database; init_database()"
```

### 4. Start Services

```bash
# Backend (Terminal 1)
cd backend
uvicorn app:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend
npm start
```

### 5. Test Connection

1. Navigate to `http://localhost:3000`
2. Go through onboarding to the "Social Media" step
3. Connect a platform (start with Google Search Console)
4. Test the connection using the test button
5. View benefits and analytics

## 📡 API Reference

### Authentication Endpoints

#### Initiate OAuth Flow
```bash
GET /api/social/auth/{platform}?user_id=1
```

**Response:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/auth?...",
  "state": "encoded_state_token"
}
```

#### OAuth Callback
```bash
GET /api/social/oauth/callback/{platform}?code=auth_code&state=state_token
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully connected google_search_console",
  "connection": {
    "id": 1,
    "platform": "google_search_console",
    "platform_username": "user@example.com",
    "connection_status": "active"
  },
  "test_result": {
    "status": "passed",
    "tests_performed": ["basic_connection", "gsc_specific"],
    "errors": [],
    "warnings": [],
    "recommendations": []
  }
}
```

### Connection Management

#### List Connections
```bash
GET /api/social/connections?user_id=1
```

#### Test Connection
```bash
POST /api/social/connections/{connection_id}/test
```

#### Disconnect Platform
```bash
DELETE /api/social/connections/{connection_id}
```

### Content Posting

#### Post Content
```bash
POST /api/social/connections/{connection_id}/post
Content-Type: application/json

{
  "content": "Your content here",
  "media_urls": ["https://example.com/image.jpg"],
  "scheduled_at": "2024-01-01T12:00:00Z"
}
```

### Analytics

#### Get GSC Performance
```bash
GET /api/social/gsc/{connection_id}/analytics/performance?start_date=2024-01-01&end_date=2024-01-31
```

#### Get Social Analytics
```bash
GET /api/social/posts/{post_id}/analytics
```

## 🐛 Debugging & Troubleshooting

### Enable Debug Logging

```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or in .env file
LOG_LEVEL=DEBUG
LOG_TO_FILE=true
```

### Common Issues & Solutions

#### 1. OAuth Connection Fails

**Symptoms:**
- "Invalid redirect URI" error
- "Client ID not found" error

**Solutions:**
```bash
# Check OAuth configuration
curl -X GET "http://localhost:8000/api/social/test/platforms"

# Verify environment variables
echo $GOOGLE_CLIENT_ID
echo $GOOGLE_REDIRECT_URI

# Check platform app settings
# Ensure redirect URI matches exactly
```

#### 2. Token Refresh Fails

**Symptoms:**
- "Token expired" errors
- Intermittent connection failures

**Solutions:**
```bash
# Test connection manually
curl -X POST "http://localhost:8000/api/social/connections/1/test"

# Check token status in database
# Look for expires_at and refresh_token fields

# Force token refresh
# Connection testing will automatically attempt refresh
```

#### 3. Rate Limiting Issues

**Symptoms:**
- "Rate limit exceeded" errors
- 429 HTTP status codes

**Solutions:**
```bash
# Check current rate limits
curl -I "http://localhost:8000/api/social/connections"
# Look for X-RateLimit-* headers

# Adjust rate limits in environment
MAX_REQUESTS_PER_WINDOW=20
RATE_LIMIT_WINDOW=300
```

#### 4. Security Blocks

**Symptoms:**
- "Access denied" errors
- "IP blocked" messages

**Solutions:**
```bash
# Check security logs
tail -f logs/social_media_*.log | grep "Security Event"

# Whitelist IP if needed
# Add to security service allowed IPs

# Clear failed attempts
# Restart application to reset rate limits
```

### Log Analysis

#### Key Log Patterns

```bash
# OAuth flow tracking
grep "OAuth.*google" logs/social_media_*.log

# Connection testing
grep "Connection test" logs/social_media_*.log

# Security events
grep "Security Event" logs/social_media_*.log

# Performance monitoring
grep "Performance:" logs/social_media_*.log

# API errors
grep "Platform API Error" logs/social_media_*.log
```

#### Performance Monitoring

```bash
# Average response times
grep "Performance:" logs/social_media_*.log | jq '.duration_seconds' | awk '{sum+=$1; count++} END {print "Avg:", sum/count}'

# Error rates
grep "ERROR" logs/social_media_*.log | wc -l

# Top failing platforms
grep "Platform API Error" logs/social_media_*.log | jq '.platform' | sort | uniq -c | sort -nr
```

## 📈 Monitoring & Maintenance

### Health Checks

```bash
# System health
curl http://localhost:8000/health

# Social connections health
curl http://localhost:8000/api/social/connections/health

# Platform status
curl http://localhost:8000/api/social/test/platforms
```

### Regular Maintenance Tasks

1. **Token Cleanup**
   - Remove expired connections
   - Clean up failed OAuth attempts

2. **Log Rotation**
   - Archive old log files
   - Monitor disk usage

3. **Security Monitoring**
   - Review security events
   - Update blocked IP lists

4. **Performance Optimization**
   - Monitor response times
   - Optimize slow endpoints

## 🔜 Future Enhancements

### Planned Features

1. **Advanced Analytics**
   - Predictive analytics
   - Content performance recommendations
   - Audience segment analysis

2. **Automation**
   - Smart scheduling
   - Content optimization
   - Auto-hashtag generation

3. **Additional Platforms**
   - Mastodon
   - Threads
   - BeReal
   - Clubhouse

4. **Enterprise Features**
   - Team management
   - Role-based access
   - Audit logging
   - Advanced security

### Contributing

To contribute to the social media integration:

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

## 📞 Support

For support with the social media integration:

- **Documentation**: This comprehensive guide
- **API Reference**: `/api/docs` endpoint
- **Logs**: Check `logs/social_media_*.log`
- **Testing**: Use built-in connection testing
- **Security**: Review security event logs

## 🎉 Conclusion

ALwrity's social media integration provides a robust, secure, and comprehensive solution for connecting and managing multiple social media platforms. With built-in testing, security measures, and detailed debugging capabilities, it's designed to scale with your needs while maintaining the highest standards of security and reliability.

The integration supports all major social media platforms and Google Search Console, providing users with powerful analytics and automated posting capabilities that enhance their content strategy and social media presence.