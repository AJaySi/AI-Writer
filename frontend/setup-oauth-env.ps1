# OAuth Environment Setup Script for Alwrity (PowerShell)
# This script helps you create the .env.local file with OAuth configuration

Write-Host "🔐 Alwrity OAuth Environment Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env.local already exists
if (Test-Path ".env.local") {
    Write-Host "⚠️  .env.local already exists. Backing up to .env.local.backup" -ForegroundColor Yellow
    Copy-Item ".env.local" ".env.local.backup"
}

# Create .env.local file
Write-Host "Creating .env.local file..." -ForegroundColor Green

$envContent = @"
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
"@

$envContent | Out-File -FilePath ".env.local" -Encoding UTF8

Write-Host "✅ .env.local file created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Update VITE_CLERK_PUBLISHABLE_KEY with your actual Clerk key" -ForegroundColor White
Write-Host "2. Configure OAuth providers in Clerk dashboard" -ForegroundColor White
Write-Host "3. Follow the CLERK_OAUTH_SETUP_GUIDE.md for detailed instructions" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Useful Links:" -ForegroundColor Yellow
Write-Host "- Clerk Dashboard: https://dashboard.clerk.com" -ForegroundColor Blue
Write-Host "- Google Cloud Console: https://console.cloud.google.com" -ForegroundColor Blue
Write-Host "- GitHub Developer Settings: https://github.com/settings/developers" -ForegroundColor Blue
Write-Host "- Facebook Developers: https://developers.facebook.com" -ForegroundColor Blue
Write-Host ""
Write-Host "📚 Documentation: CLERK_OAUTH_SETUP_GUIDE.md" -ForegroundColor Cyan
