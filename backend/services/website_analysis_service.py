"""
Website Analysis Service for Onboarding Step 2
Handles storage and retrieval of website analysis results.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json
from loguru import logger

from models.onboarding import WebsiteAnalysis, OnboardingSession


class WebsiteAnalysisService:
    """Service for managing website analysis data during onboarding."""
    
    def __init__(self, db_session: Session):
        """Initialize the service with database session."""
        self.db = db_session
    
    def save_analysis(self, session_id: int, website_url: str, analysis_data: Dict[str, Any]) -> Optional[int]:
        """
        Save website analysis results to database.
        
        Args:
            session_id: Onboarding session ID
            website_url: The analyzed website URL
            analysis_data: Complete analysis results from style detection
            
        Returns:
            Analysis ID if successful, None otherwise
        """
        try:
            # Check if analysis already exists for this URL and session
            existing_analysis = self.db.query(WebsiteAnalysis).filter_by(
                session_id=session_id,
                website_url=website_url
            ).first()
            
            if existing_analysis:
                # Update existing analysis
                existing_analysis.writing_style = analysis_data.get('style_analysis', {}).get('writing_style')
                existing_analysis.content_characteristics = analysis_data.get('style_analysis', {}).get('content_characteristics')
                existing_analysis.target_audience = analysis_data.get('style_analysis', {}).get('target_audience')
                existing_analysis.content_type = analysis_data.get('style_analysis', {}).get('content_type')
                existing_analysis.recommended_settings = analysis_data.get('style_analysis', {}).get('recommended_settings')
                existing_analysis.crawl_result = analysis_data.get('crawl_result')
                existing_analysis.style_patterns = analysis_data.get('style_patterns')
                existing_analysis.style_guidelines = analysis_data.get('style_guidelines')
                existing_analysis.status = 'completed'
                existing_analysis.error_message = None
                existing_analysis.warning_message = analysis_data.get('warning')
                existing_analysis.updated_at = datetime.utcnow()
                
                self.db.commit()
                logger.info(f"Updated existing analysis for URL: {website_url}")
                return existing_analysis.id
            else:
                # Create new analysis
                analysis = WebsiteAnalysis(
                    session_id=session_id,
                    website_url=website_url,
                    writing_style=analysis_data.get('style_analysis', {}).get('writing_style'),
                    content_characteristics=analysis_data.get('style_analysis', {}).get('content_characteristics'),
                    target_audience=analysis_data.get('style_analysis', {}).get('target_audience'),
                    content_type=analysis_data.get('style_analysis', {}).get('content_type'),
                    recommended_settings=analysis_data.get('style_analysis', {}).get('recommended_settings'),
                    crawl_result=analysis_data.get('crawl_result'),
                    style_patterns=analysis_data.get('style_patterns'),
                    style_guidelines=analysis_data.get('style_guidelines'),
                    status='completed',
                    warning_message=analysis_data.get('warning')
                )
                
                self.db.add(analysis)
                self.db.commit()
                logger.info(f"Saved new analysis for URL: {website_url}")
                return analysis.id
                
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error saving website analysis: {str(e)}")
            return None
    
    def get_analysis(self, analysis_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve website analysis by ID.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Analysis data dictionary or None if not found
        """
        try:
            analysis = self.db.query(WebsiteAnalysis).get(analysis_id)
            if analysis:
                return analysis.to_dict()
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving analysis {analysis_id}: {str(e)}")
            return None
    
    def get_analysis_by_url(self, session_id: int, website_url: str) -> Optional[Dict[str, Any]]:
        """
        Get analysis for a specific URL in a session.
        
        Args:
            session_id: Onboarding session ID
            website_url: Website URL
            
        Returns:
            Analysis data dictionary or None if not found
        """
        try:
            analysis = self.db.query(WebsiteAnalysis).filter_by(
                session_id=session_id,
                website_url=website_url
            ).first()
            
            if analysis:
                return analysis.to_dict()
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving analysis for URL {website_url}: {str(e)}")
            return None
    
    def get_session_analyses(self, session_id: int) -> List[Dict[str, Any]]:
        """
        Get all analyses for a session.
        
        Args:
            session_id: Onboarding session ID
            
        Returns:
            List of analysis summaries
        """
        try:
            analyses = self.db.query(WebsiteAnalysis).filter_by(
                session_id=session_id
            ).order_by(WebsiteAnalysis.created_at.desc()).all()
            
            return [analysis.to_dict() for analysis in analyses]
            
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving analyses for session {session_id}: {str(e)}")
            return []
    
    def get_analysis_by_session(self, session_id: int) -> Optional[Dict[str, Any]]:
        """
        Get the latest analysis for a session.
        
        Args:
            session_id: Onboarding session ID
            
        Returns:
            Latest analysis data or None if not found
        """
        try:
            analysis = self.db.query(WebsiteAnalysis).filter_by(
                session_id=session_id
            ).order_by(WebsiteAnalysis.created_at.desc()).first()
            
            if analysis:
                return analysis.to_dict()
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving latest analysis for session {session_id}: {str(e)}")
            return None
    
    def check_existing_analysis(self, session_id: int, website_url: str) -> Optional[Dict[str, Any]]:
        """
        Check if analysis exists for a URL and return it if found.
        Used for confirmation dialog in frontend.
        
        Args:
            session_id: Onboarding session ID
            website_url: Website URL
            
        Returns:
            Analysis data if found, None otherwise
        """
        try:
            analysis = self.db.query(WebsiteAnalysis).filter_by(
                session_id=session_id,
                website_url=website_url
            ).first()
            
            if analysis and analysis.status == 'completed':
                return {
                    'exists': True,
                    'analysis_date': analysis.analysis_date.isoformat() if analysis.analysis_date else None,
                    'analysis_id': analysis.id,
                    'summary': {
                        'writing_style': analysis.writing_style,
                        'target_audience': analysis.target_audience,
                        'content_type': analysis.content_type
                    }
                }
            return {'exists': False}
            
        except SQLAlchemyError as e:
            logger.error(f"Error checking existing analysis for URL {website_url}: {str(e)}")
            return {'exists': False, 'error': str(e)}
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """
        Delete a website analysis.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            analysis = self.db.query(WebsiteAnalysis).get(analysis_id)
            if analysis:
                self.db.delete(analysis)
                self.db.commit()
                logger.info(f"Deleted analysis {analysis_id}")
                return True
            return False
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting analysis {analysis_id}: {str(e)}")
            return False
    
    def save_error_analysis(self, session_id: int, website_url: str, error_message: str) -> Optional[int]:
        """
        Save analysis record with error status.
        
        Args:
            session_id: Onboarding session ID
            website_url: Website URL
            error_message: Error message
            
        Returns:
            Analysis ID if successful, None otherwise
        """
        try:
            analysis = WebsiteAnalysis(
                session_id=session_id,
                website_url=website_url,
                status='failed',
                error_message=error_message
            )
            
            self.db.add(analysis)
            self.db.commit()
            logger.info(f"Saved error analysis for URL: {website_url}")
            return analysis.id
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error saving error analysis: {str(e)}")
            return None 