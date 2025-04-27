# AI Writer

A comprehensive suite of AI-powered tools for content creation and optimization.

## Features

- **Twitter AI Writer**: Generate tweets, threads, and optimize Twitter content
- **LinkedIn AI Writer**: Create engaging LinkedIn posts, articles, and more
- **Blog Writer**: Generate blog posts from keywords, URLs, or other content
- **Multi-provider Authentication**: Sign in with Google or Twitter
- And many more AI writing tools!

## Setup

### Prerequisites

- Node.js (v14 or higher)
- PostgreSQL database
- Google Developer account (for OAuth)
- Twitter Developer account (for OAuth)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AJaySi/AI-Writer.git
cd AI-Writer
```

2. Install dependencies:
```bash
npm install
```

3. Copy the environment variables template:
```bash
cp .env.example .env
```

4. Update the `.env` file with your credentials:
- Database connection string
- Google OAuth credentials
- Twitter OAuth credentials
- Session secret
- App URL

5. Set up the database:
```bash
psql -U your_username -d your_database -a -f lib/db/schema.sql
```

6. Start the development server:
```bash
npm run dev
```

## Authentication Setup

### Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Navigate to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth client ID"
5. Set the application type to "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:3000/api/auth/callback/google` (for development)
   - `https://your-production-url.com/api/auth/callback/google` (for production)
7. Copy the Client ID and Client Secret to your `.env` file

### Twitter OAuth Setup

1. Go to the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project and app
3. Enable OAuth 2.0
4. Set the callback URL:
   - `http://localhost:3000/api/auth/callback/twitter` (for development)
   - `https://your-production-url.com/api/auth/callback/twitter` (for production)
5. Request the required scopes: `tweet.read`, `users.read`
6. Copy the Client ID and Client Secret to your `.env` file

## Usage

1. Navigate to the application in your browser
2. Sign in with your Google or Twitter account
3. Access the various AI writing tools from the dashboard

## License

This project is licensed under the MIT License - see the LICENSE file for details.