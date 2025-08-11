# ALwrity Setup Guide

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.10+
- Node.js 18+
- npm or yarn
- Git

---

## 📋 **Complete Setup Steps**

### **1. Clone and Setup Repository**

```bash
# Clone the repository
git clone https://github.com/AJaySi/AI-Writer.git
cd AI-Writer

# Install Python dependencies
pip install -r requirements.txt
```

### **2. Backend Setup (FastAPI)**

#### **Option A: Using the start_alwrity_backend script (Recommended)**
```bash
# From project root
python start_alwrity_backend.py
```

#### **Option B: Manual backend startup**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:** http://localhost:8000

### **3. Frontend Setup (React)**

```bash
cd frontend
npm install
npm start
```

**Frontend will be available at:** http://localhost:3000

---

## 🏗️ **Current Architecture Overview**

### **Project Structure**
```
alwrity/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main FastAPI application
│   ├── api/
│   │   ├── content_planning/  # Content planning endpoints
│   │   │   ├── api/
│   │   │   │   ├── enhanced_strategy_routes.py
│   │   │   │   └── router.py
│   │   │   └── services/
│   │   │       ├── content_strategy/  # Modular services
│   │   │       │   ├── core/
│   │   │       │   ├── ai_analysis/
│   │   │       │   ├── onboarding/
│   │   │       │   ├── performance/
│   │   │       │   ├── utils/
│   │   │       │   └── autofill/
│   │   │       └── enhanced_strategy_service.py
│   │   └── onboarding.py      # Onboarding endpoints
│   ├── models/
│   │   ├── enhanced_strategy_models.py
│   │   └── onboarding.py
│   ├── services/
│   │   ├── ai_service_manager.py
│   │   └── llm_providers/
│   └── requirements.txt
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── App.tsx            # Main app component
│   │   ├── components/
│   │   │   ├── ContentPlanningDashboard/
│   │   │   │   ├── components/
│   │   │   │   │   ├── ContentStrategyBuilder.tsx
│   │   │   │   │   ├── ProgressTracker.tsx
│   │   │   │   │   └── StrategicInputField.tsx
│   │   │   │   └── stores/
│   │   │   │       └── enhancedStrategyStore.ts
│   │   │   └── OnboardingWizard/
│   │   ├── services/
│   │   │   └── contentPlanningApi.ts
│   │   └── utils/
│   └── package.json
│
├── start_alwrity_backend.py   # Backend startup script
├── requirements.txt           # Python dependencies
└── README.md
```

---

## 🔧 **Development Mode**

### **Terminal 1: Backend (Recommended)**
```bash
# From project root - uses the startup script
python start_alwrity_backend.py
```

### **Terminal 2: Frontend**
```bash
cd frontend
npm start
```

---

## 🧪 **Testing the Setup**

### **1. Test Backend Health**
```bash
curl http://localhost:8000/health
```
**Expected Response:**
```json
{"status":"healthy","timestamp":"2025-08-10T12:55:16.132"}
```

### **2. Test Content Planning API**
```bash
# Test enhanced strategy endpoints
curl http://localhost:8000/api/content-planning/enhanced-strategies/health

# Test autofill functionality
curl -X POST http://localhost:8000/api/content-planning/enhanced-strategies/autofill/refresh \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "use_ai": true, "ai_only": true}'
```

### **3. Test Onboarding Endpoints**
```bash
# Test onboarding status
curl http://localhost:8000/api/onboarding/status

# Test API key validation
curl -X POST http://localhost:8000/api/onboarding/providers/openai/validate \
  -H "Content-Type: application/json" \
  -d '{"api_key": "sk-your-openai-key"}'
```

### **4. Test Frontend**
- Open http://localhost:3000 in your browser
- You should see the ALwrity application with modern React interface
- Navigate to Content Planning Dashboard to test the new features

---

## 📊 **API Endpoints Overview**

### **Content Planning Endpoints**
```python
# Enhanced Strategy Endpoints
GET /api/content-planning/enhanced-strategies/health
GET /api/content-planning/enhanced-strategies/
POST /api/content-planning/enhanced-strategies/
GET /api/content-planning/enhanced-strategies/{strategy_id}
PUT /api/content-planning/enhanced-strategies/{strategy_id}
DELETE /api/content-planning/enhanced-strategies/{strategy_id}

# Autofill Endpoints
GET /api/content-planning/enhanced-strategies/autofill/refresh/stream
POST /api/content-planning/enhanced-strategies/autofill/refresh
POST /api/content-planning/enhanced-strategies/{strategy_id}/autofill/accept

# AI Analytics Endpoints
GET /api/content-planning/ai-analytics/
POST /api/content-planning/ai-analytics/regenerate
```

### **Onboarding Endpoints**
```python
# Core Onboarding
GET /api/onboarding/status
GET /api/onboarding/progress
GET /api/onboarding/step/{n}
POST /api/onboarding/step/{n}/complete
POST /api/onboarding/step/{n}/skip

# API Key Management
GET /api/onboarding/api-keys
POST /api/onboarding/api-keys
GET /api/onboarding/providers
GET /api/onboarding/providers/{provider}/setup
POST /api/onboarding/providers/{provider}/validate
```

### **API Documentation**
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 🎯 **Application Flow**

### **First-Time Users**
1. Visit http://localhost:3000
2. System checks onboarding status
3. Shows React onboarding wizard with 6 steps:
   - **Step 1**: API Key Management
   - **Step 2**: Website Setup
   - **Step 3**: Research Configuration
   - **Step 4**: Personalization Settings
   - **Step 5**: Integrations
   - **Step 6**: Final Setup
4. Complete setup with modern UI
5. Redirects to main application

### **Returning Users**
1. Visit http://localhost:3000
2. System checks onboarding status
3. Shows main application directly
4. Access Content Planning Dashboard for AI-powered strategy generation

---

## 🐛 **Troubleshooting**

### **Backend Issues**

#### **Import Errors**
```bash
# If you get import errors, ensure you're in the correct directory
cd backend
python -c "from api.content_planning.api.router import router; print('✅ Backend imports working')"
```

#### **Missing Dependencies**
```bash
# Install all Python dependencies
pip install -r requirements.txt

# If specific modules are missing
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart
```

#### **Port Already in Use**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python start_alwrity_backend.py --port 8001
```

#### **Database Issues**
```bash
# The system uses SQLite by default
# Database files are created automatically in the backend directory
# Check for database files:
ls backend/*.db
```

### **Frontend Issues**

#### **Build Errors**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### **Port Conflicts**
```bash
# Change port in package.json or use different port
npm start -- --port 3001
```

#### **CORS Issues**
- Ensure backend CORS is configured correctly
- Check that frontend is making requests to correct backend URL
- Verify proxy configuration in package.json

### **Content Planning Issues**

#### **AI Autofill Not Working**
```bash
# Test the autofill endpoint directly
curl -X POST http://localhost:8000/api/content-planning/enhanced-strategies/autofill/refresh \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "use_ai": true, "ai_only": true}'

# Check backend logs for AI service errors
# Ensure API keys are configured correctly
```

#### **Strategy Generation Issues**
```bash
# Test strategy creation
curl -X POST http://localhost:8000/api/content-planning/enhanced-strategies/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Strategy", "user_id": 1}'
```

---

## 🔍 **Monitoring & Debugging**

### **Backend Logs**
- Check terminal where backend is running
- FastAPI provides detailed error messages and request logs
- Look for AI service integration logs

### **Frontend Logs**
- Check browser developer console
- React development server logs
- Network tab for API requests

### **Database**
- SQLite database files in backend directory
- Created automatically on first run
- Can be inspected with SQLite browser

### **API Documentation**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- Interactive testing of all endpoints

---

## 🚀 **Production Deployment**

### **Backend**
```bash
# Build and run with gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### **Frontend**
```bash
cd frontend
npm run build
# Serve build/ folder with nginx or similar
```

### **Environment Variables**
```bash
# Backend environment variables
export DATABASE_URL="postgresql://user:password@localhost/alwrity"
export CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
export LOG_LEVEL="INFO"
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"

# Frontend environment variables
export REACT_APP_API_URL="http://localhost:8000"
export REACT_APP_ENVIRONMENT="production"
```

---

## 📚 **Key Features Available**

### **✅ Content Strategy Generation**
- AI-powered content strategy generation with 100% success rate
- 30+ strategic input fields with intelligent auto-fill
- Real-time AI analysis and recommendations
- Multi-category strategy organization

### **✅ Advanced AI Integration**
- Multiple AI providers (OpenAI, Google Gemini, Anthropic)
- Structured JSON output with retry mechanisms
- Field type normalization and validation
- Predictive analytics and optimization

### **✅ Modern Architecture**
- FastAPI backend with modular services
- React frontend with Material-UI
- Multi-tenant authentication system
- Comprehensive API documentation

### **✅ Development Tools**
- Hot reload for both frontend and backend
- Comprehensive error handling and logging
- Interactive API documentation
- Modular service architecture

---

## 📚 **Additional Documentation**

- **[API Documentation](API_DOCUMENTATION.md)** - Complete FastAPI backend documentation
- **[Enhanced Strategy Refactoring Plan](docs/enhanced_strategy_refactoring_plan.md)** - Module breakdown strategy
- **[ALwrity Vision](ALwrity_vision.md)** - Comprehensive platform vision and roadmap
- **[README.md](README.md)** - Main project documentation

---

## 🎉 **Setup Complete!**

**✅ The new ALwrity FastAPI + React architecture is ready for development and testing.**

**Key Features Available:**
- **AI-Powered Content Strategy Generation** with 100% success rate
- **Modular Backend Services** for maintainability and scalability
- **Modern React Frontend** with Material-UI components
- **Comprehensive API Documentation** with interactive testing
- **Multi-tenant Authentication** system
- **Advanced AI Integration** with multiple providers

**Next Steps:**
1. **Test the content strategy generation** using the AI autofill feature
2. **Explore the modular backend services** and API endpoints
3. **Configure API keys** for different AI providers
4. **Start developing** new features using the established patterns
5. **Review the refactoring plan** for future module breakdown

**🚀 Ready to build the ultimate AI-powered digital marketing platform!** 