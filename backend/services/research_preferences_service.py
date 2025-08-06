"""
Research Preferences Service for Onboarding Step 3
Handles storage and retrieval of research preferences and style detection data.
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json
from loguru import logger

from models.onboarding import ResearchPreferences, OnboardingSession, WebsiteAnalysis


class ResearchPreferencesService:
    """Service for managing research preferences data during onboarding."""
    
    def __init__(self, db_session: Session):
        """Initialize the service with database session."""
        self.db = db_session
    
    def save_research_preferences(self, session_id: int, preferences_data: Dict[str, Any], style_data: Optional[Dict[str, Any]] = None) -> Optional[int]:
        """
        Save research preferences to database.
        
        Args:
            session_id: Onboarding session ID
            preferences_data: Research preferences from step 3
            style_data: Style detection data from step 2 (optional)
            
        Returns:
            Preferences ID if successful, None otherwise
        """
        try:
            # Check if preferences already exist for this session
            existing_preferences = self.db.query(ResearchPreferences).filter_by(session_id=session_id).first()
            
            if existing_preferences:
                # Update existing preferences
                existing_preferences.research_depth = preferences_data.get('research_depth', 'Comprehensive')
                existing_preferences.content_types = preferences_data.get('content_types', [])
                existing_preferences.auto_research = preferences_data.get('auto_research', True)
                existing_preferences.factual_content = preferences_data.get('factual_content', True)
                
                # Update style data if provided
                if style_data:
                    existing_preferences.writing_style = style_data.get('writing_style')
                    existing_preferences.content_characteristics = style_data.get('content_characteristics')
                    existing_preferences.target_audience = style_data.get('target_audience')
                    existing_preferences.recommended_settings = style_data.get('recommended_settings')
                
                existing_preferences.updated_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"Updated research preferences for session {session_id}")
                return existing_preferences.id
            else:
                # Create new preferences
                preferences = ResearchPreferences(
                    session_id=session_id,
                    research_depth=preferences_data.get('research_depth', 'Comprehensive'),
                    content_types=preferences_data.get('content_types', []),
                    auto_research=preferences_data.get('auto_research', True),
                    factual_content=preferences_data.get('factual_content', True),
                    writing_style=style_data.get('writing_style') if style_data else None,
                    content_characteristics=style_data.get('content_characteristics') if style_data else None,
                    target_audience=style_data.get('target_audience') if style_data else None,
                    recommended_settings=style_data.get('recommended_settings') if style_data else None
                )
                
                self.db.add(preferences)
                self.db.commit()
                logger.info(f"Created research preferences for session {session_id}")
                return preferences.id
                
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error saving research preferences: {e}")
            return None
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error saving research preferences: {e}")
            return None
    
    def get_research_preferences(self, session_id: int) -> Optional[Dict[str, Any]]:
        """
        Get research preferences for a session.
        
        Args:
            session_id: Onboarding session ID
            
        Returns:
            Research preferences data or None if not found
        """
        try:
            preferences = self.db.query(ResearchPreferences).filter_by(session_id=session_id).first()
            if preferences:
                return preferences.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error getting research preferences: {e}")
            return None
    
    def get_style_data_from_analysis(self, session_id: int) -> Optional[Dict[str, Any]]:
        """
        Get style detection data from website analysis for a session.
        
        Args:
            session_id: Onboarding session ID
            
        Returns:
            Style data from website analysis or None if not found
        """
        try:
            analysis = self.db.query(WebsiteAnalysis).filter_by(session_id=session_id).first()
            if analysis:
                return {
                    'writing_style': analysis.writing_style,
                    'content_characteristics': analysis.content_characteristics,
                    'target_audience': analysis.target_audience,
                    'recommended_settings': analysis.recommended_settings
                }
            return None
        except Exception as e:
            logger.error(f"Error getting style data from analysis: {e}")
            return None
    
    def save_preferences_with_style_data(self, session_id: int, preferences_data: Dict[str, Any]) -> Optional[int]:
        """
        Save research preferences with style data from website analysis.
        
        Args:
            session_id: Onboarding session ID
            preferences_data: Research preferences from step 3
            
        Returns:
            Preferences ID if successful, None otherwise
        """
        # Get style data from website analysis
        style_data = self.get_style_data_from_analysis(session_id)
        
        # Save preferences with style data
        return self.save_research_preferences(session_id, preferences_data, style_data)
    
    def update_preferences(self, preferences_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update existing research preferences.
        
        Args:
            preferences_id: Research preferences ID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            preferences = self.db.query(ResearchPreferences).filter_by(id=preferences_id).first()
            if not preferences:
                logger.warning(f"Research preferences {preferences_id} not found")
                return False
            
            # Update fields
            for field, value in updates.items():
                if hasattr(preferences, field):
                    setattr(preferences, field, value)
            
            preferences.updated_at = datetime.utcnow()
            self.db.commit()
            logger.info(f"Updated research preferences {preferences_id}")
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error updating research preferences: {e}")
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating research preferences: {e}")
            return False
    
    def delete_preferences(self, session_id: int) -> bool:
        """
        Delete research preferences for a session.
        
        Args:
            session_id: Onboarding session ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            preferences = self.db.query(ResearchPreferences).filter_by(session_id=session_id).first()
            if preferences:
                self.db.delete(preferences)
                self.db.commit()
                logger.info(f"Deleted research preferences for session {session_id}")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting research preferences: {e}")
            return False 