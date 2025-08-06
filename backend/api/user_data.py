"""User Data API endpoints for ALwrity."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from loguru import logger

from services.user_data_service import UserDataService
from services.database import get_db_session

router = APIRouter(prefix="/api/user-data", tags=["user-data"])

@router.get("/")
async def get_user_data():
    """Get comprehensive user data from onboarding."""
    try:
        db_session = get_db_session()
        if not db_session:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        user_data_service = UserDataService(db_session)
        user_data = user_data_service.get_user_onboarding_data()
        
        if not user_data:
            return {"message": "No user data found"}
        
        return user_data
        
    except Exception as e:
        logger.error(f"Error getting user data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting user data: {str(e)}")
    finally:
        if db_session:
            db_session.close()

@router.get("/website-url")
async def get_website_url():
    """Get the user's website URL from onboarding data."""
    try:
        db_session = get_db_session()
        if not db_session:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        user_data_service = UserDataService(db_session)
        website_url = user_data_service.get_user_website_url()
        
        if not website_url:
            return {"website_url": None, "message": "No website URL found"}
        
        return {"website_url": website_url}
        
    except Exception as e:
        logger.error(f"Error getting website URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting website URL: {str(e)}")
    finally:
        if db_session:
            db_session.close()

@router.get("/onboarding")
async def get_onboarding_data():
    """Get onboarding data for the user."""
    try:
        db_session = get_db_session()
        if not db_session:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        user_data_service = UserDataService(db_session)
        onboarding_data = user_data_service.get_user_onboarding_data()
        
        if not onboarding_data:
            return {"message": "No onboarding data found"}
        
        return onboarding_data
        
    except Exception as e:
        logger.error(f"Error getting onboarding data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting onboarding data: {str(e)}")
    finally:
        if db_session:
            db_session.close() 