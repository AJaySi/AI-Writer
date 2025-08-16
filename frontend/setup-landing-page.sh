#!/bin/bash

# Alwrity Landing Page Setup Script
echo "🚀 Setting up Alwrity Landing Page with Clerk Authentication..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are installed"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create environment file if it doesn't exist
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local file..."
    cp env.example .env.local
    echo "⚠️  Please update .env.local with your Clerk publishable key"
else
    echo "✅ .env.local already exists"
fi

# Check if Clerk key is configured
if grep -q "pk_test_your_clerk_key_here" .env.local; then
    echo "⚠️  Please update your Clerk publishable key in .env.local"
    echo "   Get your key from: https://dashboard.clerk.com/"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env.local with your Clerk publishable key"
echo "2. Configure Clerk dashboard with redirect URLs:"
echo "   - http://localhost:3000/auth/signin"
echo "   - http://localhost:3000/auth/signup"
echo "   - http://localhost:3000/dashboard"
echo "   - http://localhost:3000/onboarding"
echo "3. Run 'npm start' to start the development server"
echo "4. Visit http://localhost:3000 to see the landing page"
echo ""
echo "📚 For detailed instructions, see: LANDING_PAGE_IMPLEMENTATION_GUIDE.md"
