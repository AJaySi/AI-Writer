"""
Google Search Console Analytics Service
Fetches and processes GSC data for connected websites.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sqlalchemy.orm import Session
from models.social_connections import SocialConnection, SocialAnalytics
from services.oauth_service import oauth_service

class GSCAnalyticsService:
    def __init__(self):
        self.service_name = 'searchconsole'
        self.api_version = 'v1'

    def get_gsc_service(self, connection: SocialConnection, db: Session):
        """Get authenticated GSC service instance."""
        access_token = oauth_service.get_valid_token(connection, db)
        if not access_token:
            raise ValueError("No valid access token for GSC connection")
        
        # Create credentials object
        credentials = Credentials(
            token=access_token,
            refresh_token=oauth_service.decrypt_token(connection.refresh_token) if connection.refresh_token else None,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
        )
        
        return build(self.service_name, self.api_version, credentials=credentials)

    async def fetch_site_list(self, connection: SocialConnection, db: Session) -> List[Dict]:
        """Fetch list of verified sites from GSC."""
        try:
            service = self.get_gsc_service(connection, db)
            sites_response = service.sites().list().execute()
            
            sites = []
            for site in sites_response.get('siteEntry', []):
                site_data = {
                    'siteUrl': site['siteUrl'],
                    'permissionLevel': site['permissionLevel']
                }
                sites.append(site_data)
            
            # Update connection profile data with latest sites
            profile_data = connection.profile_data or {}
            profile_data['sites'] = sites
            profile_data['last_site_fetch'] = datetime.utcnow().isoformat()
            connection.profile_data = profile_data
            db.commit()
            
            return sites
        except HttpError as e:
            raise ValueError(f"Failed to fetch GSC sites: {e}")

    async def fetch_search_analytics(
        self, 
        connection: SocialConnection, 
        db: Session,
        site_url: str,
        start_date: str = None,
        end_date: str = None,
        dimensions: List[str] = None,
        row_limit: int = 25000
    ) -> Dict[str, Any]:
        """
        Fetch search analytics data from GSC.
        
        Args:
            connection: SocialConnection instance
            db: Database session
            site_url: The site URL to fetch data for
            start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            end_date: End date in YYYY-MM-DD format (default: 3 days ago)
            dimensions: List of dimensions (query, page, country, device, date)
            row_limit: Maximum number of rows to return
        """
        try:
            service = self.get_gsc_service(connection, db)
            
            # Set default dates if not provided
            if not end_date:
                end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=33)).strftime('%Y-%m-%d')
            
            # Set default dimensions
            if not dimensions:
                dimensions = ['query', 'page']
            
            request_body = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': dimensions,
                'rowLimit': row_limit,
                'startRow': 0
            }
            
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            # Process and save analytics data
            analytics_data = {
                'site_url': site_url,
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'dimensions': dimensions,
                'rows': response.get('rows', []),
                'row_count': len(response.get('rows', [])),
                'fetched_at': datetime.utcnow().isoformat()
            }
            
            # Save to database
            self._save_analytics_data(connection.id, 'search_analytics', analytics_data, db, start_date, end_date)
            
            return analytics_data
            
        except HttpError as e:
            raise ValueError(f"Failed to fetch GSC search analytics: {e}")

    async def fetch_performance_summary(
        self,
        connection: SocialConnection,
        db: Session,
        site_url: str,
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, Any]:
        """Fetch performance summary data (clicks, impressions, CTR, position)."""
        try:
            service = self.get_gsc_service(connection, db)
            
            # Set default dates
            if not end_date:
                end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=33)).strftime('%Y-%m-%d')
            
            # Fetch overall performance
            request_body = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['date'],
                'rowLimit': 1000
            }
            
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            # Calculate totals and averages
            total_clicks = 0
            total_impressions = 0
            total_ctr = 0
            total_position = 0
            row_count = len(response.get('rows', []))
            
            daily_data = []
            for row in response.get('rows', []):
                total_clicks += row.get('clicks', 0)
                total_impressions += row.get('impressions', 0)
                total_ctr += row.get('ctr', 0)
                total_position += row.get('position', 0)
                
                daily_data.append({
                    'date': row.get('keys', [''])[0],
                    'clicks': row.get('clicks', 0),
                    'impressions': row.get('impressions', 0),
                    'ctr': row.get('ctr', 0),
                    'position': row.get('position', 0)
                })
            
            summary_data = {
                'site_url': site_url,
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'totals': {
                    'clicks': total_clicks,
                    'impressions': total_impressions,
                    'ctr': total_ctr / row_count if row_count > 0 else 0,
                    'position': total_position / row_count if row_count > 0 else 0
                },
                'daily_data': daily_data,
                'fetched_at': datetime.utcnow().isoformat()
            }
            
            # Save to database
            self._save_analytics_data(connection.id, 'performance_summary', summary_data, db, start_date, end_date)
            
            return summary_data
            
        except HttpError as e:
            raise ValueError(f"Failed to fetch GSC performance summary: {e}")

    async def fetch_top_queries(
        self,
        connection: SocialConnection,
        db: Session,
        site_url: str,
        start_date: str = None,
        end_date: str = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Fetch top performing search queries."""
        try:
            service = self.get_gsc_service(connection, db)
            
            # Set default dates
            if not end_date:
                end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=33)).strftime('%Y-%m-%d')
            
            request_body = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['query'],
                'rowLimit': limit,
                'dataState': 'final'
            }
            
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            queries_data = {
                'site_url': site_url,
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'queries': [
                    {
                        'query': row.get('keys', [''])[0],
                        'clicks': row.get('clicks', 0),
                        'impressions': row.get('impressions', 0),
                        'ctr': row.get('ctr', 0),
                        'position': row.get('position', 0)
                    }
                    for row in response.get('rows', [])
                ],
                'fetched_at': datetime.utcnow().isoformat()
            }
            
            # Save to database
            self._save_analytics_data(connection.id, 'top_queries', queries_data, db, start_date, end_date)
            
            return queries_data
            
        except HttpError as e:
            raise ValueError(f"Failed to fetch GSC top queries: {e}")

    async def fetch_top_pages(
        self,
        connection: SocialConnection,
        db: Session,
        site_url: str,
        start_date: str = None,
        end_date: str = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Fetch top performing pages."""
        try:
            service = self.get_gsc_service(connection, db)
            
            # Set default dates
            if not end_date:
                end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=33)).strftime('%Y-%m-%d')
            
            request_body = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['page'],
                'rowLimit': limit,
                'dataState': 'final'
            }
            
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            pages_data = {
                'site_url': site_url,
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'pages': [
                    {
                        'page': row.get('keys', [''])[0],
                        'clicks': row.get('clicks', 0),
                        'impressions': row.get('impressions', 0),
                        'ctr': row.get('ctr', 0),
                        'position': row.get('position', 0)
                    }
                    for row in response.get('rows', [])
                ],
                'fetched_at': datetime.utcnow().isoformat()
            }
            
            # Save to database
            self._save_analytics_data(connection.id, 'top_pages', pages_data, db, start_date, end_date)
            
            return pages_data
            
        except HttpError as e:
            raise ValueError(f"Failed to fetch GSC top pages: {e}")

    async def fetch_index_status(
        self,
        connection: SocialConnection,
        db: Session,
        site_url: str
    ) -> Dict[str, Any]:
        """Fetch indexing status information (requires URL Inspection API)."""
        try:
            service = self.get_gsc_service(connection, db)
            
            # Get URL inspection data for the main site
            request_body = {
                'inspectionUrl': site_url,
                'siteUrl': site_url
            }
            
            response = service.urlInspection().index().inspect(body=request_body).execute()
            
            index_data = {
                'site_url': site_url,
                'inspection_result': response.get('inspectionResult', {}),
                'fetched_at': datetime.utcnow().isoformat()
            }
            
            # Save to database
            self._save_analytics_data(connection.id, 'index_status', index_data, db)
            
            return index_data
            
        except HttpError as e:
            raise ValueError(f"Failed to fetch GSC index status: {e}")

    def _save_analytics_data(
        self,
        connection_id: int,
        metric_name: str,
        metric_value: Dict,
        db: Session,
        start_date: str = None,
        end_date: str = None
    ):
        """Save analytics data to the database."""
        try:
            # Convert date strings to datetime objects
            date_start = None
            date_end = None
            if start_date:
                date_start = datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                date_end = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Check if analytics record already exists for this metric and date range
            existing = db.query(SocialAnalytics).filter(
                SocialAnalytics.connection_id == connection_id,
                SocialAnalytics.metric_name == metric_name,
                SocialAnalytics.date_range_start == date_start,
                SocialAnalytics.date_range_end == date_end
            ).first()
            
            if existing:
                # Update existing record
                existing.metric_value = metric_value
                existing.fetched_at = datetime.utcnow()
            else:
                # Create new record
                analytics = SocialAnalytics(
                    connection_id=connection_id,
                    metric_name=metric_name,
                    metric_value=metric_value,
                    date_range_start=date_start,
                    date_range_end=date_end
                )
                db.add(analytics)
            
            db.commit()
            
        except Exception as e:
            print(f"Failed to save analytics data: {e}")
            db.rollback()

    def get_cached_analytics(
        self,
        connection_id: int,
        metric_name: str,
        db: Session,
        max_age_hours: int = 6
    ) -> Optional[Dict]:
        """Get cached analytics data if it's recent enough."""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        analytics = db.query(SocialAnalytics).filter(
            SocialAnalytics.connection_id == connection_id,
            SocialAnalytics.metric_name == metric_name,
            SocialAnalytics.fetched_at >= cutoff_time
        ).order_by(SocialAnalytics.fetched_at.desc()).first()
        
        if analytics:
            return analytics.metric_value
        return None

# Global instance
gsc_analytics_service = GSCAnalyticsService()