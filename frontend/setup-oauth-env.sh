#!/bin/bash

# OAuth Environment Setup Script for Alwrity
# This script helps you create the .env.local file with OAuth configuration

echo "🔐 Alwrity OAuth Environment Setup"
echo "=================================="
echo ""

# Check if .env.local already exists
if [ -f ".env.local" ]; then
    echo "⚠️  .env.local already exists. Backing up to .env.local.backup"
    cp .env.local .env.local.backup
fi

# Create .env.local file
echo "Creating .env.local file..."

cat > .env.local << 'EOF'
# Clerk Authentication Configuration
VITE_CLERK_PUBLISHABLE_KEY=pk_test_bGl2aW5nLWhhbXN0ZXItNTkuY2xlcmsuYWNjb3VudHMuZGV2JA

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
EOF

echo "✅ .env.local file created successfully!"
echo ""
echo "📝 Next Steps:"
echo "1. Update VITE_CLERK_PUBLISHABLE_KEY with your actual Clerk key"
echo "2. Configure OAuth providers in Clerk dashboard"
echo "3. Follow the CLERK_OAUTH_SETUP_GUIDE.md for detailed instructions"
echo ""
echo "🔗 Useful Links:"
echo "- Clerk Dashboard: https://dashboard.clerk.com"
echo "- Google Cloud Console: https://console.cloud.google.com"
echo "- GitHub Developer Settings: https://github.com/settings/developers"
echo "- Facebook Developers: https://developers.facebook.com"
echo ""
echo "📚 Documentation: CLERK_OAUTH_SETUP_GUIDE.md"
