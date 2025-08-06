# ALwrity Backend

Welcome to the ALwrity Backend! This is the FastAPI-powered backend that provides RESTful APIs for the ALwrity AI content creation platform.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- pip (Python package manager)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
python start_alwrity_backend.py
```

### 3. Verify It's Working
- Open your browser to: http://localhost:8000/api/docs
- You should see the interactive API documentation
- Health check: http://localhost:8000/health

## 📁 Project Structure

```
backend/
├── app.py                          # FastAPI application definition
├── start_alwrity_backend.py        # Server startup script
├── requirements.txt                 # Python dependencies
├── api/
│   ├── __init__.py
│   └── onboarding.py              # Onboarding API endpoints
├── services/
│   ├── __init__.py
│   ├── api_key_manager.py         # API key management
│   └── validation.py              # Validation services
├── models/
│   ├── __init__.py
│   └── onboarding.py              # Data models
└── README.md                      # This file
```

## 🔧 File Descriptions

### Core Files

#### `app.py` - FastAPI Application
- **What it does**: Defines all API endpoints and middleware
- **Contains**: 
  - FastAPI app initialization
  - All API routes (onboarding, health, etc.)
  - CORS middleware for frontend integration
  - Static file serving for React frontend
- **When to edit**: When adding new API endpoints or modifying existing ones

#### `start_alwrity_backend.py` - Server Startup
- **What it does**: Enhanced startup script with dependency checking
- **Contains**:
  - Dependency validation
  - Environment setup (creates directories)
  - User-friendly logging and error messages
  - Server startup with uvicorn
- **When to use**: This is your main entry point to start the server

### Supporting Directories

#### `api/` - API Endpoints
- Contains modular API endpoint definitions
- Organized by feature (onboarding, etc.)
- Each file handles a specific domain of functionality

#### `services/` - Business Logic
- Contains service layer functions
- Handles database operations, API key management, etc.
- Separates business logic from API endpoints

#### `models/` - Data Models
- Contains Pydantic models and database schemas
- Defines data structures for API requests/responses
- Ensures type safety and validation

## 🎯 How to Start the Backend

### Option 1: Recommended (Using the startup script)
```bash
cd backend
python start_alwrity_backend.py
```

### Option 2: Direct uvicorn (For development)
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Production mode
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 🌐 What You'll See

When you start the backend successfully, you'll see:

```
🎯 ALwrity Backend Server
========================================
✅ All dependencies are installed
🔧 Setting up environment...
   ✅ Created directory: lib/workspace/alwrity_content
   ✅ Created directory: lib/workspace/alwrity_web_research
   ✅ Created directory: lib/workspace/alwrity_prompts
   ✅ Created directory: lib/workspace/alwrity_config
   ℹ️  No .env file found. API keys will need to be configured.
✅ Environment setup complete
🚀 Starting ALwrity Backend...
   📍 Host: 0.0.0.0
   🔌 Port: 8000
   🔄 Reload: true

🌐 Backend is starting...
   📖 API Documentation: http://localhost:8000/api/docs
   🔍 Health Check: http://localhost:8000/health
   📊 ReDoc: http://localhost:8000/api/redoc

⏹️  Press Ctrl+C to stop the server
============================================================
```

## 📚 API Documentation

Once the server is running, you can access:

- **📖 Interactive API Docs (Swagger)**: http://localhost:8000/api/docs
- **📊 ReDoc Documentation**: http://localhost:8000/api/redoc
- **🔍 Health Check**: http://localhost:8000/health

## 🔑 Available Endpoints

### Health & Status
- `GET /health` - Health check endpoint

### Onboarding System
- `GET /api/onboarding/status` - Get current onboarding status
- `GET /api/onboarding/progress` - Get full progress data
- `GET /api/onboarding/config` - Get onboarding configuration

### Step Management
- `GET /api/onboarding/step/{step_number}` - Get step data
- `POST /api/onboarding/step/{step_number}/complete` - Complete a step
- `POST /api/onboarding/step/{step_number}/skip` - Skip a step
- `GET /api/onboarding/step/{step_number}/validate` - Validate step access

### API Key Management
- `GET /api/onboarding/api-keys` - Get configured API keys
- `POST /api/onboarding/api-keys` - Save an API key
- `POST /api/onboarding/api-keys/validate` - Validate API keys

### Onboarding Control
- `POST /api/onboarding/start` - Start onboarding
- `POST /api/onboarding/complete` - Complete onboarding
- `POST /api/onboarding/reset` - Reset progress
- `GET /api/onboarding/resume` - Get resume information

## 🧪 Testing the Backend

### Quick Test with curl
```bash
# Health check
curl http://localhost:8000/health

# Get onboarding status
curl http://localhost:8000/api/onboarding/status

# Complete step 1
curl -X POST http://localhost:8000/api/onboarding/step/1/complete \
  -H "Content-Type: application/json" \
  -d '{"data": {"api_keys": ["openai"]}}'
```

### Using the Swagger UI
1. Open http://localhost:8000/api/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

## ⚙️ Configuration

### Environment Variables
You can customize the server behavior with these environment variables:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload (default: true)

Example:
```bash
HOST=127.0.0.1 PORT=8080 python start_alwrity_backend.py
```

### CORS Configuration
The backend is configured to allow requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:8000` (Backend dev server)
- `http://localhost:3001` (Alternative React port)

## 🔄 Development Workflow

### 1. Start Development Server
```bash
cd backend
python start_alwrity_backend.py
```

### 2. Make Changes
- Edit `app.py` for API changes
- Edit files in `api/` for endpoint modifications
- Edit files in `services/` for business logic changes

### 3. Auto-reload
The server automatically reloads when you save changes to Python files.

### 4. Test Changes
- Use the Swagger UI at http://localhost:8000/api/docs
- Or use curl commands for quick testing

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Make sure you're in the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
```

#### 2. "Port already in use" error
```bash
# Use a different port
PORT=8080 python start_alwrity_backend.py
```

#### 3. "Permission denied" errors
```bash
# On Windows, run PowerShell as Administrator
# On Linux/Mac, check file permissions
ls -la
```

#### 4. CORS errors from frontend
- Make sure the frontend is running on http://localhost:3000
- Check that CORS is properly configured in `app.py`

### Getting Help

1. **Check the logs**: The startup script provides detailed information
2. **API Documentation**: Use http://localhost:8000/api/docs to test endpoints
3. **Health Check**: Visit http://localhost:8000/health to verify the server is running

## 🚀 Production Deployment

### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Gunicorn (Recommended for production)
```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔗 Integration with Frontend

This backend is designed to work seamlessly with the React frontend:

1. **API Client**: Frontend uses axios to communicate with these endpoints
2. **Real-time Updates**: Frontend polls status endpoints for live updates
3. **Error Handling**: Comprehensive error responses for frontend handling
4. **CORS**: Configured for cross-origin requests from React

## 📈 Features

- **✅ Onboarding Progress Tracking**: Complete 6-step onboarding flow with persistence
- **🔑 API Key Management**: Secure storage and validation of AI provider API keys
- **🔄 Resume Functionality**: Users can resume onboarding from where they left off
- **✅ Validation**: Comprehensive validation for API keys and step completion
- **🌐 CORS Support**: Configured for React frontend integration
- **📚 Auto-generated Documentation**: Swagger UI and ReDoc
- **🔍 Health Monitoring**: Built-in health check endpoint

## 🤝 Contributing

When adding new features:

1. **Add API endpoints** in `api/` directory
2. **Add business logic** in `services/` directory
3. **Add data models** in `models/` directory
4. **Update this README** with new information
5. **Test thoroughly** using the Swagger UI

## 📞 Support

If you encounter issues:

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Test individual endpoints using the Swagger UI
4. Check the health endpoint: http://localhost:8000/health

---

**Happy coding! 🎉** 