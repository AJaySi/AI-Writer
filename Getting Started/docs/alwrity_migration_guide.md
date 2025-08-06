# Alwrity Migration Guide: From Streamlit to React + FastAPI

## Overview
This guide explains how to migrate from the current Streamlit-based `alwrity.py` to the new React + FastAPI architecture while maintaining all present functionality.

---

## Architecture Changes

### Before (Streamlit)
```
alwrity.py (Streamlit app)
├── Onboarding (API key setup)
├── Main UI (sidebar navigation)
└── All features (AI writers, SEO tools, etc.)
```

### After (React + FastAPI)
```
Backend (FastAPI)
├── backend/main.py (replaces alwrity.py)
├── backend/api/onboarding.py (onboarding endpoints)
├── backend/services/api_key_manager.py (API key management)
└── backend/models/onboarding.py (database models)

Frontend (React)
├── frontend/src/App.tsx (main app with onboarding check)
├── frontend/src/components/OnboardingWizard/ (onboarding flow)
└── frontend/src/components/MainApp.tsx (main application)
```

---

## Key Changes

### 1. **alwrity.py → backend/main.py**
- **Before**: Single Streamlit file handling everything
- **After**: FastAPI backend with separate React frontend
- **Maintained**: All environment setup, API key checking, logging

### 2. **Onboarding Flow**
- **Before**: Streamlit-based onboarding in `alwrity.py`
- **After**: React wizard with FastAPI backend
- **Maintained**: Same onboarding steps and validation logic

### 3. **Application Flow**
- **Before**: Direct access to all features after onboarding
- **After**: Onboarding check → React wizard (first-time) → Main app (returning users)
- **Maintained**: All existing functionality preserved

---

## How to Run the New Architecture

### Option 1: Development Mode
```bash
# Terminal 1: Start FastAPI backend
cd backend
python main.py
# Backend runs on http://localhost:8000

# Terminal 2: Start React frontend
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

### Option 2: Production Mode
```bash
# Build React app
cd frontend
npm run build

# Serve with FastAPI
cd backend
python main.py
# Both frontend and backend served from http://localhost:8000
```

---

## Migration Steps

### Phase 1: Backend Setup ✅
1. ✅ Extract API key management to `backend/services/api_key_manager.py`
2. ✅ Create FastAPI onboarding endpoints in `backend/api/onboarding.py`
3. ✅ Set up database models in `backend/models/onboarding.py`
4. ✅ Create main FastAPI app in `backend/main.py`

### Phase 2: Frontend Setup ✅
1. ✅ Create React onboarding wizard
2. ✅ Implement API integration
3. ✅ Create main app structure
4. ✅ Set up onboarding flow

### Phase 3: Feature Migration (Next Steps)
1. **Migrate AI Writers**: Wrap existing AI writer modules as FastAPI endpoints
2. **Migrate SEO Tools**: Create API endpoints for SEO functionality
3. **Migrate UI Components**: Convert Streamlit UI to React components
4. **Add Authentication**: Implement user management and sessions

---

## Maintaining Present Functionality

### ✅ Preserved Features
- **API Key Management**: Same validation and storage logic
- **Onboarding Flow**: Same steps, improved UI
- **Environment Setup**: All paths and configurations preserved
- **Logging**: Same logging configuration
- **Error Handling**: Enhanced with better user feedback

### 🔄 Enhanced Features
- **UI/UX**: Modern React interface with Material-UI
- **Performance**: Faster loading and better responsiveness
- **Scalability**: Backend can handle multiple users
- **Maintainability**: Separated concerns, easier to extend

---

## API Endpoints

### Onboarding Endpoints
- `GET /api/check-onboarding` - Check if onboarding is required
- `POST /api/onboarding/start` - Start onboarding session
- `GET /api/onboarding/step` - Get current step
- `POST /api/onboarding/step` - Set current step
- `GET /api/onboarding/api-keys` - Get saved API keys
- `POST /api/onboarding/api-keys` - Save API key
- `GET /api/onboarding/progress` - Get onboarding progress
- `POST /api/onboarding/progress` - Set onboarding progress

### Application Endpoints
- `GET /api/status` - Get application status
- `GET /health` - Health check

---

## Development Workflow

### For First-Time Users
1. User visits application
2. `App.tsx` checks onboarding status via `/api/check-onboarding`
3. If onboarding required → Show `Wizard.tsx`
4. User completes 6-step onboarding process
5. On completion → Switch to `MainApp.tsx`

### For Returning Users
1. User visits application
2. `App.tsx` checks onboarding status
3. If onboarding complete → Show `MainApp.tsx` directly
4. User accesses all features

---

## Next Steps

### Immediate
1. **Test the onboarding flow** end-to-end
2. **Install dependencies** for React and FastAPI
3. **Configure development environment**

### Short-term
1. **Migrate AI Writers** to FastAPI endpoints
2. **Create React components** for main features
3. **Add authentication** and user management

### Long-term
1. **Add enterprise features** (SSO, multi-user, audit)
2. **Optimize performance** and scalability
3. **Add advanced features** (real-time collaboration, etc.)

---

## Troubleshooting

### Common Issues
1. **CORS errors**: Ensure CORS middleware is configured
2. **API connection errors**: Check backend is running on correct port
3. **Database errors**: Ensure SQLite database is created
4. **React build errors**: Install all required dependencies

### Dependencies Required
```bash
# Backend
pip install fastapi uvicorn sqlalchemy python-dotenv

# Frontend
npm install react @mui/material @mui/icons-material axios
```

---

**The migration maintains all present functionality while providing a modern, scalable foundation for enterprise features.** 