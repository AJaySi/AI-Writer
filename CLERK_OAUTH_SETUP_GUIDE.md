# 🔐 Clerk OAuth Setup Guide for Alwrity

## 📋 Overview
This guide walks you through configuring multiple OAuth providers (Google, GitHub, Facebook) and email/password authentication in your Clerk dashboard for Alwrity.

## 🎯 Prerequisites
- Clerk account with an Alwrity application
- Access to Google Cloud Console
- Access to GitHub Developer Settings
- Domain or localhost for development

## 🔧 Step-by-Step Configuration

### 1. Access Clerk Dashboard
1. Go to https://dashboard.clerk.com
2. Sign in to your account
3. Select your Alwrity application

### 2. Navigate to Social Connections
1. In the left sidebar, click "User & Authentication"
2. Click "Social Connections"
3. You'll see a list of available OAuth providers

### 3. Configure Google OAuth

#### 3.1 Get Google OAuth Credentials
1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create/Select Project**:
   - Create a new project or select existing one
   - Note down the Project ID
3. **Enable APIs**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API" and enable it
   - Search for "Google Identity" and enable it
4. **Create OAuth Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"
   - Set Application Type to "Web application"
   - Add Authorized redirect URIs:
     ```
     https://your-clerk-domain.com/sign-in/callback
     http://localhost:3000/sign-in/callback
     ```
5. **Copy Credentials**:
   - Client ID: `your-google-client-id`
   - Client Secret: `your-google-client-secret`

#### 3.2 Configure in Clerk
1. In Clerk dashboard, click on "Google" in Social Connections
2. Enable Google OAuth
3. Paste your Google Client ID and Client Secret
4. Save configuration

### 4. Configure GitHub OAuth

#### 4.1 Get GitHub OAuth Credentials
1. **Go to GitHub Developer Settings**: https://github.com/settings/developers
2. **Create New OAuth App**:
   - Click "New OAuth App"
   - Fill in the details:
     - **Application name**: `Alwrity`
     - **Homepage URL**: `https://your-domain.com` or `http://localhost:3000`
     - **Application description**: `AI-powered content creation platform`
     - **Authorization callback URL**: `https://your-clerk-domain.com/sign-in/callback`
   - Click "Register application"
3. **Copy Credentials**:
   - Client ID: `your-github-client-id`
   - Client Secret: Click "Generate a new client secret"

#### 4.2 Configure in Clerk
1. In Clerk dashboard, click on "GitHub" in Social Connections
2. Enable GitHub OAuth
3. Paste your GitHub Client ID and Client Secret
4. Save configuration

### 5. Configure Facebook OAuth (if not already done)

#### 5.1 Get Facebook OAuth Credentials
1. **Go to Facebook Developers**: https://developers.facebook.com/
2. **Create App**:
   - Click "Create App"
   - Choose "Consumer" app type
   - Fill in app details
3. **Add Facebook Login**:
   - Go to "Add Product" → "Facebook Login"
   - Configure OAuth redirect URIs:
     ```
     https://your-clerk-domain.com/sign-in/callback
     http://localhost:3000/sign-in/callback
     ```
4. **Copy Credentials**:
   - App ID: `your-facebook-app-id`
   - App Secret: `your-facebook-app-secret`

#### 5.2 Configure in Clerk
1. In Clerk dashboard, click on "Facebook" in Social Connections
2. Enable Facebook OAuth
3. Paste your Facebook App ID and App Secret
4. Save configuration

### 6. Configure Email/Password Authentication

1. **In Clerk dashboard**, click on "Email/Password" in Social Connections
2. **Enable Email/Password authentication**
3. **Configure settings**:
   - ✅ Enable "Allow sign up"
   - ✅ Enable "Allow sign in"
   - ✅ Enable "Email verification"
   - Set password requirements (minimum 8 characters)
   - Configure email templates if needed

### 7. Update Environment Variables

Create or update your `.env.local` file in the frontend directory:

```bash
# Clerk Authentication Configuration
VITE_CLERK_PUBLISHABLE_KEY=pk_test_your-clerk-key

# Backend API Configuration
VITE_API_BASE_URL=http://localhost:8000

# Environment
VITE_ENV=development

# Authentication Provider Flags
VITE_ENABLE_EMAIL_AUTH=true
VITE_ENABLE_GITHUB_AUTH=true
VITE_ENABLE_GOOGLE_AUTH=true
VITE_ENABLE_FACEBOOK_AUTH=true

# OAuth Redirect URLs (for reference)
VITE_GOOGLE_REDIRECT_URI=http://localhost:3000/sign-in/callback
VITE_GITHUB_REDIRECT_URI=http://localhost:3000/sign-in/callback
```

## 🔍 Verification Steps

### 1. Test OAuth Providers
1. Start your development server
2. Navigate to the sign-in page
3. Test each OAuth provider:
   - Google: Should redirect to Google consent screen
   - GitHub: Should redirect to GitHub authorization
   - Facebook: Should redirect to Facebook login
   - Email/Password: Should show email/password form

### 2. Check Clerk Dashboard
1. Go to "Users" in Clerk dashboard
2. Verify that users can sign up through all providers
3. Check that user profiles contain provider information

### 3. Verify Redirect URIs
1. Ensure all redirect URIs are correctly configured
2. Test both development and production URLs
3. Check for any CORS or redirect errors

## 🚨 Common Issues & Solutions

### Issue: "Invalid redirect URI"
**Solution**: 
- Double-check redirect URIs in both OAuth provider and Clerk
- Ensure exact match including protocol (http vs https)
- Add both development and production URLs

### Issue: "OAuth provider not found"
**Solution**:
- Verify OAuth provider is enabled in Clerk
- Check Client ID and Secret are correct
- Ensure required APIs are enabled in provider dashboard

### Issue: "Email verification not working"
**Solution**:
- Check email templates in Clerk dashboard
- Verify email provider settings
- Test with different email addresses

## 📞 Support Resources

- **Clerk Documentation**: https://clerk.com/docs
- **Google OAuth Guide**: https://developers.google.com/identity/protocols/oauth2
- **GitHub OAuth Guide**: https://docs.github.com/en/developers/apps/building-oauth-apps
- **Facebook OAuth Guide**: https://developers.facebook.com/docs/facebook-login

## ✅ Checklist

- [ ] Google OAuth configured in Google Cloud Console
- [ ] Google OAuth enabled in Clerk dashboard
- [ ] GitHub OAuth configured in GitHub Developer Settings
- [ ] GitHub OAuth enabled in Clerk dashboard
- [ ] Facebook OAuth configured in Facebook Developers
- [ ] Facebook OAuth enabled in Clerk dashboard
- [ ] Email/Password authentication enabled in Clerk
- [ ] Environment variables updated
- [ ] All OAuth providers tested
- [ ] Redirect URIs verified
- [ ] User registration tested for all providers

---

**Next Steps**: After completing this configuration, proceed to Phase 2: Frontend Implementation to create the authentication components.
