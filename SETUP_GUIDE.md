# ALwrity Setup Guide

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- npm or yarn

---

## 📋 **Complete Setup Steps**

### **1. Backend Setup**


#### **Option B: Run from backend directory**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Backend will be available at:** http://localhost:8000

### **2. Frontend Setup**

```bash
cd frontend
npm install
npm start
```

**Frontend will be available at:** http://localhost:3000

---

## 🏗️ **New Architecture Overview**

### **Project Structure**
```
alwrity/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main FastAPI application
│   ├── api/
│   │   ├── onboarding.py      # Core onboarding endpoints
│   │   └── component_logic.py # Advanced component endpoints
│   ├── services/
│   │   ├── api_key_manager.py # API key management service
│   │   ├── validation.py      # Validation services
│   │   └── component_logic/   # Component logic services
│   │       ├── ai_research_logic.py
│   │       ├── personalization_logic.py
│   │       └── research_utilities.py
│   ├── models/
│   │   ├── onboarding.py      # Database models
│   │   └── component_logic.py # Component logic models
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── App.tsx            # Main app with onboarding check
│   │   ├── components/
│   │   │   ├── OnboardingWizard/  # Complete onboarding flow
│   │   │   │   ├── common/        # Design system components
│   │   │   │   │   ├── useOnboardingStyles.ts
│   │   │   │   │   ├── onboardingUtils.ts
│   │   │   │   │   ├── OnboardingStepLayout.tsx
│   │   │   │   │   ├── OnboardingCard.tsx
│   │   │   │   │   └── OnboardingButton.tsx
│   │   │   │   ├── ApiKeyStep.tsx
│   │   │   │   ├── WebsiteStep.tsx
│   │   │   │   ├── ResearchStep.tsx
│   │   │   │   ├── PersonalizationStep.tsx
│   │   │   │   ├── IntegrationsStep.tsx
│   │   │   │   ├── FinalStep.tsx
│   │   │   │   └── ResearchTestStep.tsx
│   │   │   └── MainApp.tsx        # Main application
│   │   └── api/
│   │       ├── onboarding.ts      # Onboarding API integration
│   │       └── componentLogic.ts  # Component logic API integration
│   └── package.json           # Node.js dependencies
│
└── lib/utils/api_key_manager/ # Legacy Streamlit (reference only)
    ├── onboarding_progress.py # Migrated to backend
    ├── components/            # Migrated to React
    └── ...
```

---

## 🔧 **Development Mode**

### **Terminal 1: Backend**
```bash
# From project root
python run_backend.py
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
{"status":"healthy","timestamp":"2025-07-28T18:14:35.749581"}
```

### **2. Test Onboarding Check**
```bash
curl http://localhost:8000/api/check-onboarding
```
**Expected Response:**
```json
{"onboarding_required":false,"onboarding_complete":true}
```

### **3. Test Component Logic Endpoints**
```bash
# Test AI Research endpoint
curl -X POST http://localhost:8000/api/onboarding/ai-research/validate-user \
  -H "Content-Type: application/json" \
  -d '{"full_name": "John Doe", "email": "john@example.com", "company": "Test Corp", "role": "Developer"}'

# Test Personalization endpoint
curl -X POST http://localhost:8000/api/onboarding/personalization/validate-style \
  -H "Content-Type: application/json" \
  -d '{"writing_style": "Professional", "tone": "Formal", "content_length": "Standard"}'
```

### **4. Test Frontend**
- Open http://localhost:3000 in your browser
- You should see the ALwrity application with modern React interface

---

## 📊 **API Endpoints Overview**

### **Core Endpoints (12 Total)**
```python
# Health and Status
GET /health                    # Health check
GET /api/status               # Application status

# Onboarding Endpoints
GET /api/onboarding/status    # Get onboarding status
GET /api/onboarding/progress  # Get full progress data
GET /api/onboarding/step/{n}  # Get step data
POST /api/onboarding/step/{n}/complete  # Complete step
POST /api/onboarding/step/{n}/skip      # Skip step
GET /api/onboarding/api-keys  # Get API keys
POST /api/onboarding/api-keys # Save API key
GET /api/onboarding/resume    # Get resume info

# Provider Information
GET /api/onboarding/providers                    # Get all providers
GET /api/onboarding/providers/{provider}/setup   # Get setup info
POST /api/onboarding/providers/{provider}/validate # Validate key
GET /api/onboarding/validation/enhanced          # Enhanced validation
```

### **Component Logic Endpoints (15 Total)**
```python
# AI Research Endpoints (4)
POST /api/onboarding/ai-research/validate-user
POST /api/onboarding/ai-research/configure-preferences
POST /api/onboarding/ai-research/process-research
GET /api/onboarding/ai-research/configuration-options

# Personalization Endpoints (6)
POST /api/onboarding/personalization/validate-style
POST /api/onboarding/personalization/configure-brand
POST /api/onboarding/personalization/process-settings
GET /api/onboarding/personalization/configuration-options
POST /api/onboarding/personalization/generate-guidelines

# Research Utilities Endpoints (5)
POST /api/onboarding/research/process-topic
POST /api/onboarding/research/process-results
POST /api/onboarding/research/validate-request
GET /api/onboarding/research/providers-info
POST /api/onboarding/research/generate-report
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

---

## 🐛 **Troubleshooting**

### **Backend Issues**

#### **Import Errors**
```bash
# If you get "No module named 'backend'" error:
# Use the run_backend.py script from project root
python run_backend.py
```

#### **Missing Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

#### **Port Already in Use**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

#### **Database Issues**
```bash
# Remove and recreate database
rm backend/onboarding.db
# Restart backend - database will be recreated automatically
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

### **Component Logic Issues**

#### **API Key Validation**
```bash
# Test API key validation
curl -X POST http://localhost:8000/api/onboarding/providers/openai/validate \
  -H "Content-Type: application/json" \
  -d '{"api_key": "sk-your-openai-key"}'
```

#### **Research Utilities**
```bash
# Test research topic processing
curl -X POST http://localhost:8000/api/onboarding/research/process-topic \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI writing tools", "providers": ["tavily"], "depth": "standard"}'
```

---

## 🔍 **Monitoring & Debugging**

### **Backend Logs**
- Check terminal where backend is running
- Logs show API requests and errors
- FastAPI provides detailed error messages

### **Frontend Logs**
- Check browser developer console
- React development server logs
- Network tab for API requests

### **Database**
- SQLite database: `backend/onboarding.db`
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
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
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
export DATABASE_URL="sqlite:///./onboarding.db"
export CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
export LOG_LEVEL="INFO"

# Frontend environment variables
export REACT_APP_API_URL="http://localhost:8000"
export REACT_APP_ENVIRONMENT="development"
```

---

## 📚 **Additional Documentation**

- **[API Documentation](API_DOCUMENTATION.md)** - Complete FastAPI backend documentation
- **[Migration Guide](ALWRITY_MIGRATION_FINAL.md)** - Complete migration documentation
- **[README.md](README.md)** - Main project documentation

---

## 🎉 **Setup Complete!**

**✅ The new ALwrity architecture is ready for development and testing.**

**Key Features Available:**
- **27 API Endpoints** with comprehensive functionality
- **Modern React Frontend** with Material-UI components
- **Component Logic Services** for advanced features
- **Design System** for consistent UI/UX
- **Real-time Validation** and error handling
- **Complete Onboarding Flow** with 6 steps

**Next Steps:**
1. **Test all endpoints** using the API documentation
2. **Explore the React components** and design system
3. **Configure API keys** for different providers
4. **Start developing** new features using the established patterns 