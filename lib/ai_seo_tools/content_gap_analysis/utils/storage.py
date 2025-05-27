"""
Storage module for content gap analysis results.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

class ContentGapAnalysisStorage:
    """Handles storage and retrieval of content gap analysis results."""
    
    def __init__(self, db_session: Session):
        """Initialize the storage handler."""
        self.db = db_session
    
    def save_analysis(self, user_id: int, website_url: str, industry: str, results: Dict[str, Any]) -> Optional[int]:
        """
        Save content gap analysis results.
        
        Args:
            user_id: User ID
            website_url: Target website URL
            industry: Industry category
            results: Analysis results dictionary
            
        Returns:
            Analysis ID if successful, None otherwise
        """
        try:
            # Create main analysis record
            analysis = ContentGapAnalysis(
                user_id=user_id,
                website_url=website_url,
                industry=industry,
                status='completed',
                metadata={'version': '1.0'}
            )
            self.db.add(analysis)
            self.db.flush()  # Get the ID without committing
            
            # Save website analysis
            website_analysis = WebsiteAnalysis(
                content_gap_analysis_id=analysis.id,
                content_score=results.get('website', {}).get('content_score', 0),
                seo_score=results.get('website', {}).get('seo_score', 0),
                structure_score=results.get('website', {}).get('structure_score', 0),
                content_metrics=results.get('website', {}).get('content_metrics', {}),
                seo_metrics=results.get('website', {}).get('seo_metrics', {}),
                technical_metrics=results.get('website', {}).get('technical_metrics', {}),
                ai_insights=results.get('website', {}).get('ai_insights', {})
            )
            self.db.add(website_analysis)
            
            # Save competitor analysis if available
            if 'competitors' in results:
                for competitor in results['competitors']:
                    competitor_analysis = CompetitorAnalysis(
                        content_gap_analysis_id=analysis.id,
                        competitor_url=competitor.get('url'),
                        market_position=competitor.get('market_position', {}),
                        content_gaps=competitor.get('content_gaps', []),
                        competitive_advantages=competitor.get('competitive_advantages', []),
                        trend_analysis=competitor.get('trend_analysis', {})
                    )
                    self.db.add(competitor_analysis)
            
            # Save keyword analysis
            keyword_analysis = KeywordAnalysis(
                content_gap_analysis_id=analysis.id,
                top_keywords=results.get('keywords', {}).get('top_keywords', []),
                search_intent=results.get('keywords', {}).get('search_intent', {}),
                opportunities=results.get('keywords', {}).get('opportunities', []),
                trend_analysis=results.get('keywords', {}).get('trend_analysis', {})
            )
            self.db.add(keyword_analysis)
            
            # Save recommendations
            for recommendation in results.get('recommendations', []):
                content_recommendation = ContentRecommendation(
                    content_gap_analysis_id=analysis.id,
                    recommendation_type=recommendation.get('type'),
                    priority_score=recommendation.get('priority_score', 0),
                    recommendation=recommendation.get('recommendation', ''),
                    implementation_steps=recommendation.get('implementation_steps', []),
                    expected_impact=recommendation.get('expected_impact', {}),
                    status='pending'
                )
                self.db.add(content_recommendation)
            
            # Save analysis history
            history = AnalysisHistory(
                content_gap_analysis_id=analysis.id,
                status='completed',
                metrics={'duration': results.get('duration', 0)}
            )
            self.db.add(history)
            
            # Commit all changes
            self.db.commit()
            return analysis.id
            
        except SQLAlchemyError as e:
            self.db.rollback()
            st.error(f"Error saving analysis results: {str(e)}")
            return None
    
    def get_analysis(self, analysis_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve content gap analysis results.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Dictionary containing analysis results if found, None otherwise
        """
        try:
            analysis = self.db.query(ContentGapAnalysis).get(analysis_id)
            if not analysis:
                return None
            
            # Get website analysis
            website_analysis = self.db.query(WebsiteAnalysis).filter_by(
                content_gap_analysis_id=analysis_id
            ).first()
            
            # Get competitor analysis
            competitor_analyses = self.db.query(CompetitorAnalysis).filter_by(
                content_gap_analysis_id=analysis_id
            ).all()
            
            # Get keyword analysis
            keyword_analysis = self.db.query(KeywordAnalysis).filter_by(
                content_gap_analysis_id=analysis_id
            ).first()
            
            # Get recommendations
            recommendations = self.db.query(ContentRecommendation).filter_by(
                content_gap_analysis_id=analysis_id
            ).all()
            
            # Get analysis history
            history = self.db.query(AnalysisHistory).filter_by(
                content_gap_analysis_id=analysis_id
            ).order_by(AnalysisHistory.run_date.desc()).all()
            
            return {
                'id': analysis.id,
                'website_url': analysis.website_url,
                'industry': analysis.industry,
                'analysis_date': analysis.analysis_date,
                'status': analysis.status,
                'website': {
                    'content_score': website_analysis.content_score,
                    'seo_score': website_analysis.seo_score,
                    'structure_score': website_analysis.structure_score,
                    'content_metrics': website_analysis.content_metrics,
                    'seo_metrics': website_analysis.seo_metrics,
                    'technical_metrics': website_analysis.technical_metrics,
                    'ai_insights': website_analysis.ai_insights
                } if website_analysis else {},
                'competitors': [{
                    'url': ca.competitor_url,
                    'market_position': ca.market_position,
                    'content_gaps': ca.content_gaps,
                    'competitive_advantages': ca.competitive_advantages,
                    'trend_analysis': ca.trend_analysis
                } for ca in competitor_analyses],
                'keywords': {
                    'top_keywords': keyword_analysis.top_keywords,
                    'search_intent': keyword_analysis.search_intent,
                    'opportunities': keyword_analysis.opportunities,
                    'trend_analysis': keyword_analysis.trend_analysis
                } if keyword_analysis else {},
                'recommendations': [{
                    'type': r.recommendation_type,
                    'priority_score': r.priority_score,
                    'recommendation': r.recommendation,
                    'implementation_steps': r.implementation_steps,
                    'expected_impact': r.expected_impact,
                    'status': r.status
                } for r in recommendations],
                'history': [{
                    'run_date': h.run_date,
                    'status': h.status,
                    'metrics': h.metrics,
                    'error_log': h.error_log
                } for h in history]
            }
            
        except SQLAlchemyError as e:
            st.error(f"Error retrieving analysis results: {str(e)}")
            return None
    
    def get_user_analyses(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all analyses for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of analysis summaries
        """
        try:
            analyses = self.db.query(ContentGapAnalysis).filter_by(
                user_id=user_id
            ).order_by(ContentGapAnalysis.analysis_date.desc()).all()
            
            return [{
                'id': analysis.id,
                'website_url': analysis.website_url,
                'industry': analysis.industry,
                'analysis_date': analysis.analysis_date,
                'status': analysis.status
            } for analysis in analyses]
            
        except SQLAlchemyError as e:
            st.error(f"Error retrieving user analyses: {str(e)}")
            return []
    
    def update_recommendation_status(self, recommendation_id: int, status: str) -> bool:
        """
        Update the status of a recommendation.
        
        Args:
            recommendation_id: Recommendation ID
            status: New status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            recommendation = self.db.query(ContentRecommendation).get(recommendation_id)
            if recommendation:
                recommendation.status = status
                recommendation.updated_at = datetime.utcnow()
                self.db.commit()
                return True
            return False
            
        except SQLAlchemyError as e:
            self.db.rollback()
            st.error(f"Error updating recommendation status: {str(e)}")
            return False
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """
        Delete an analysis and all related data.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            analysis = self.db.query(ContentGapAnalysis).get(analysis_id)
            if analysis:
                self.db.delete(analysis)
                self.db.commit()
                return True
            return False
            
        except SQLAlchemyError as e:
            self.db.rollback()
            st.error(f"Error deleting analysis: {str(e)}")
            return False 