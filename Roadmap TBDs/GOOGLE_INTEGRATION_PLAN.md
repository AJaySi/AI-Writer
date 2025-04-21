# Google Integration Implementation Plan

This document outlines the step-by-step implementation plan for integrating Google login and Google Search Console (GSC) with AI-Writer to enhance content creation with real user insights.

## Overview

The integration will allow users to:

1. Sign in with their Google account
2. Connect to Google Search Console
3. Access search analytics data for content optimization
4. Use real keyword data for content creation
5. Track content performance over time

## Implementation Steps

### Phase 1: Google OAuth Integration

#### Step 1: Set Up Google Cloud Project

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project named "AI-Writer"
   - Note the Project ID for configuration

2. **Configure OAuth Consent Screen**
   - Navigate to "APIs & Services" > "OAuth consent screen"
   - Select "External" user type
   - Fill in application information:
     - App name: "AI-Writer"
     - User support email: support@alwrity.com
     - Developer contact information
   - Add scopes:
     - `https://www.googleapis.com/auth/userinfo.email`
     - `https://www.googleapis.com/auth/userinfo.profile`
     - `https://www.googleapis.com/auth/webmasters.readonly`
   - Add test users for development

3. **Create OAuth Credentials**
   - Navigate to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Web application" as application type
   - Set name to "AI-Writer Web Client"
   - Add authorized JavaScript origins:
     - `http://localhost:8501` (for development)
     - `https://your-production-domain.com` (for production)
   - Add authorized redirect URIs:
     - `http://localhost:8501/oauth/callback` (for development)
     - `https://your-production-domain.com/oauth/callback` (for production)
   - Save and note the Client ID and Client Secret

4. **Enable Required APIs**
   - Navigate to "APIs & Services" > "Library"
   - Search for and enable:
     - Google Search Console API
     - Google OAuth2 API
     - Google People API

#### Step 2: Implement Backend Authentication

1. **Install Required Packages**

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

2. **Create Authentication Module**

Create a new file at `/workspace/AI-Writer/lib/integrations/google/auth.py`:

```python
"""Google authentication module for AI-Writer."""

import os
import json
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from loguru import logger

# Define scopes needed for the application
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/webmasters.readonly'
]

# Configuration directory
CONFIG_DIR = Path(__file__).parent.parent.parent.parent / 'config'
CREDENTIALS_FILE = CONFIG_DIR / 'google_credentials.json'
TOKENS_DIR = CONFIG_DIR / 'tokens'

def get_google_auth_url() -> str:
    """Generate Google OAuth authorization URL.
    
    Returns:
        str: Authorization URL for Google OAuth
    """
    try:
        # Ensure config directory exists
        CONFIG_DIR.mkdir(exist_ok=True)
        TOKENS_DIR.mkdir(exist_ok=True)
        
        # Load client configuration
        client_config = st.secrets.get("google_oauth", None)
        
        if not client_config:
            logger.error("Google OAuth client configuration not found in secrets")
            return ""
        
        # Create OAuth flow instance
        flow = Flow.from_client_config(
            client_config=client_config,
            scopes=SCOPES,
            redirect_uri=client_config["web"]["redirect_uris"][0]
        )
        
        # Generate authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store flow in session state for later use
        st.session_state.google_auth_flow = flow
        
        return auth_url
    except Exception as e:
        logger.error(f"Error generating Google auth URL: {str(e)}")
        return ""

def handle_auth_callback(code: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Handle OAuth callback and exchange code for tokens.
    
    Args:
        code: Authorization code from Google
        
    Returns:
        Tuple[bool, Optional[Dict]]: Success status and user info if successful
    """
    try:
        # Get flow from session state
        flow = st.session_state.get("google_auth_flow")
        if not flow:
            logger.error("Auth flow not found in session state")
            return False, None
        
        # Exchange code for tokens
        flow.fetch_token(code=code)
        
        # Get credentials
        credentials = flow.credentials
        
        # Save credentials
        save_credentials(credentials)
        
        # Get user info
        user_info = get_user_info(credentials)
        
        # Store in session state
        st.session_state.google_credentials = credentials_to_dict(credentials)
        st.session_state.google_user_info = user_info
        
        return True, user_info
    except Exception as e:
        logger.error(f"Error handling auth callback: {str(e)}")
        return False, None

def save_credentials(credentials: Credentials) -> bool:
    """Save Google credentials to file.
    
    Args:
        credentials: Google OAuth credentials
        
    Returns:
        bool: Success status
    """
    try:
        # Convert credentials to dict
        creds_dict = credentials_to_dict(credentials)
        
        # Get user email from credentials
        user_info = get_user_info(credentials)
        user_email = user_info.get("email", "unknown")
        
        # Create user-specific token file
        token_file = TOKENS_DIR / f"{user_email}.json"
        
        # Save credentials to file
        with open(token_file, 'w') as f:
            json.dump(creds_dict, f)
        
        logger.info(f"Saved credentials for {user_email}")
        return True
    except Exception as e:
        logger.error(f"Error saving credentials: {str(e)}")
        return False

def load_credentials(user_email: str) -> Optional[Credentials]:
    """Load Google credentials from file.
    
    Args:
        user_email: Email of the user
        
    Returns:
        Optional[Credentials]: Google credentials if found
    """
    try:
        # Get user-specific token file
        token_file = TOKENS_DIR / f"{user_email}.json"
        
        # Check if file exists
        if not token_file.exists():
            logger.warning(f"No credentials found for {user_email}")
            return None
        
        # Load credentials from file
        with open(token_file, 'r') as f:
            creds_dict = json.load(f)
        
        # Create credentials object
        credentials = Credentials.from_authorized_user_info(creds_dict, SCOPES)
        
        # Check if credentials are valid
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            save_credentials(credentials)
        
        return credentials
    except Exception as e:
        logger.error(f"Error loading credentials: {str(e)}")
        return None

def get_user_info(credentials: Credentials) -> Dict[str, Any]:
    """Get user information from Google.
    
    Args:
        credentials: Google OAuth credentials
        
    Returns:
        Dict[str, Any]: User information
    """
    try:
        # Build people API service
        service = build('people', 'v1', credentials=credentials)
        
        # Get user profile
        profile = service.people().get(
            resourceName='people/me',
            personFields='names,emailAddresses,photos'
        ).execute()
        
        # Extract relevant information
        user_info = {
            "email": profile.get("emailAddresses", [{}])[0].get("value", ""),
            "name": profile.get("names", [{}])[0].get("displayName", ""),
            "picture": profile.get("photos", [{}])[0].get("url", "")
        }
        
        return user_info
    except Exception as e:
        logger.error(f"Error getting user info: {str(e)}")
        return {}

def credentials_to_dict(credentials: Credentials) -> Dict[str, Any]:
    """Convert Google credentials to dictionary.
    
    Args:
        credentials: Google OAuth credentials
        
    Returns:
        Dict[str, Any]: Credentials as dictionary
    """
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def is_authenticated() -> bool:
    """Check if user is authenticated with Google.
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    return 'google_credentials' in st.session_state and 'google_user_info' in st.session_state

def logout() -> None:
    """Log out user from Google."""
    if 'google_credentials' in st.session_state:
        del st.session_state.google_credentials
    if 'google_user_info' in st.session_state:
        del st.session_state.google_user_info
    if 'google_auth_flow' in st.session_state:
        del st.session_state.google_auth_flow
```

3. **Create OAuth Callback Handler**

Create a new file at `/workspace/AI-Writer/lib/integrations/google/callback_handler.py`:

```python
"""Google OAuth callback handler for Streamlit."""

import streamlit as st
from urllib.parse import parse_qs, urlparse
from .auth import handle_auth_callback

def handle_oauth_callback():
    """Handle OAuth callback in Streamlit."""
    # Get current URL
    query_params = st.experimental_get_query_params()
    
    # Check if this is a callback
    if 'code' in query_params:
        code = query_params['code'][0]
        
        # Exchange code for tokens
        success, user_info = handle_auth_callback(code)
        
        if success:
            # Clear query parameters to avoid reprocessing
            st.experimental_set_query_params()
            
            # Show success message
            st.success(f"Successfully logged in as {user_info.get('name', 'User')}")
            
            # Redirect to main page
            st.experimental_rerun()
        else:
            st.error("Failed to authenticate with Google. Please try again.")
    
    # Check for error
    if 'error' in query_params:
        error = query_params['error'][0]
        st.error(f"Authentication error: {error}")
        st.experimental_set_query_params()
```

#### Step 3: Implement Google Search Console API

1. **Create GSC API Module**

Create a new file at `/workspace/AI-Writer/lib/integrations/google/search_console.py`:

```python
"""Google Search Console API integration for AI-Writer."""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from loguru import logger

def get_search_console_service(credentials: Dict[str, Any]) -> Any:
    """Build Google Search Console API service.
    
    Args:
        credentials: Google OAuth credentials dictionary
        
    Returns:
        Any: Search Console API service
    """
    try:
        # Convert dict to credentials object
        creds = Credentials.from_authorized_user_info(credentials)
        
        # Build service
        service = build('searchconsole', 'v1', credentials=creds)
        
        return service
    except Exception as e:
        logger.error(f"Error building Search Console service: {str(e)}")
        return None

def get_site_list() -> List[Dict[str, Any]]:
    """Get list of sites from Search Console.
    
    Returns:
        List[Dict[str, Any]]: List of sites
    """
    try:
        # Check if user is authenticated
        if 'google_credentials' not in st.session_state:
            logger.warning("User not authenticated with Google")
            return []
        
        # Get credentials
        credentials = st.session_state.google_credentials
        
        # Build service
        service = get_search_console_service(credentials)
        if not service:
            return []
        
        # Get site list
        sites = service.sites().list().execute()
        
        # Extract site entries
        site_entries = sites.get('siteEntry', [])
        
        # Filter for verified sites
        verified_sites = [
            {
                'site_url': site.get('siteUrl', ''),
                'permission_level': site.get('permissionLevel', ''),
                'site_type': 'Web' if site.get('siteUrl', '').startswith('http') else 'Domain Property'
            }
            for site in site_entries
            if site.get('permissionLevel') in ['siteOwner', 'siteFullUser']
        ]
        
        return verified_sites
    except Exception as e:
        logger.error(f"Error getting site list: {str(e)}")
        return []

def get_search_analytics(
    site_url: str,
    start_date: datetime,
    end_date: datetime,
    dimensions: List[str] = ['query'],
    row_limit: int = 1000
) -> Dict[str, Any]:
    """Get search analytics data from Search Console.
    
    Args:
        site_url: URL of the site
        start_date: Start date for data
        end_date: End date for data
        dimensions: Dimensions to include (query, page, device, country, date)
        row_limit: Maximum number of rows to return
        
    Returns:
        Dict[str, Any]: Search analytics data
    """
    try:
        # Check if user is authenticated
        if 'google_credentials' not in st.session_state:
            logger.warning("User not authenticated with Google")
            return {'rows': []}
        
        # Get credentials
        credentials = st.session_state.google_credentials
        
        # Build service
        service = get_search_console_service(credentials)
        if not service:
            return {'rows': []}
        
        # Format dates
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        # Prepare request body
        request_body = {
            'startDate': start_date_str,
            'endDate': end_date_str,
            'dimensions': dimensions,
            'rowLimit': row_limit,
            'startRow': 0,
            'searchType': 'web'
        }
        
        # Execute request
        response = service.searchanalytics().query(
            siteUrl=site_url,
            body=request_body
        ).execute()
        
        return response
    except Exception as e:
        logger.error(f"Error getting search analytics: {str(e)}")
        return {'rows': []}

def get_top_keywords(site_url: str, days: int = 30, limit: int = 100) -> List[Dict[str, Any]]:
    """Get top keywords for a site.
    
    Args:
        site_url: URL of the site
        days: Number of days to include
        limit: Maximum number of keywords to return
        
    Returns:
        List[Dict[str, Any]]: List of top keywords with metrics
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get search analytics data
        analytics = get_search_analytics(
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            dimensions=['query'],
            row_limit=limit
        )
        
        # Process rows
        rows = analytics.get('rows', [])
        
        # Format results
        keywords = []
        for row in rows:
            keywords.append({
                'keyword': row.get('keys', [''])[0],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': row.get('ctr', 0) * 100,  # Convert to percentage
                'position': row.get('position', 0)
            })
        
        # Sort by clicks (descending)
        keywords.sort(key=lambda x: x['clicks'], reverse=True)
        
        return keywords
    except Exception as e:
        logger.error(f"Error getting top keywords: {str(e)}")
        return []

def get_top_pages(site_url: str, days: int = 30, limit: int = 100) -> List[Dict[str, Any]]:
    """Get top pages for a site.
    
    Args:
        site_url: URL of the site
        days: Number of days to include
        limit: Maximum number of pages to return
        
    Returns:
        List[Dict[str, Any]]: List of top pages with metrics
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get search analytics data
        analytics = get_search_analytics(
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            dimensions=['page'],
            row_limit=limit
        )
        
        # Process rows
        rows = analytics.get('rows', [])
        
        # Format results
        pages = []
        for row in rows:
            pages.append({
                'page': row.get('keys', [''])[0],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': row.get('ctr', 0) * 100,  # Convert to percentage
                'position': row.get('position', 0)
            })
        
        # Sort by clicks (descending)
        pages.sort(key=lambda x: x['clicks'], reverse=True)
        
        return pages
    except Exception as e:
        logger.error(f"Error getting top pages: {str(e)}")
        return []

def get_keyword_insights(keyword: str, site_url: str, days: int = 90) -> Dict[str, Any]:
    """Get detailed insights for a specific keyword.
    
    Args:
        keyword: Keyword to analyze
        site_url: URL of the site
        days: Number of days to include
        
    Returns:
        Dict[str, Any]: Keyword insights
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get search analytics data with date dimension
        analytics = get_search_analytics(
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            dimensions=['query', 'date'],
            row_limit=1000
        )
        
        # Process rows
        rows = analytics.get('rows', [])
        
        # Filter for the specific keyword
        keyword_rows = [
            row for row in rows
            if row.get('keys', ['', ''])[0].lower() == keyword.lower()
        ]
        
        # Prepare time series data
        time_series = []
        for row in keyword_rows:
            date_str = row.get('keys', ['', ''])[1]
            time_series.append({
                'date': date_str,
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': row.get('ctr', 0) * 100,
                'position': row.get('position', 0)
            })
        
        # Sort by date
        time_series.sort(key=lambda x: x['date'])
        
        # Get pages ranking for this keyword
        page_analytics = get_search_analytics(
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            dimensions=['query', 'page'],
            row_limit=100
        )
        
        # Filter for the specific keyword
        keyword_pages = [
            {
                'page': row.get('keys', ['', ''])[1],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': row.get('ctr', 0) * 100,
                'position': row.get('position', 0)
            }
            for row in page_analytics.get('rows', [])
            if row.get('keys', ['', ''])[0].lower() == keyword.lower()
        ]
        
        # Sort by position (ascending)
        keyword_pages.sort(key=lambda x: x['position'])
        
        # Calculate totals
        total_clicks = sum(row.get('clicks', 0) for row in keyword_rows)
        total_impressions = sum(row.get('impressions', 0) for row in keyword_rows)
        avg_ctr = (sum(row.get('ctr', 0) for row in keyword_rows) / len(keyword_rows)) * 100 if keyword_rows else 0
        avg_position = sum(row.get('position', 0) for row in keyword_rows) / len(keyword_rows) if keyword_rows else 0
        
        # Compile insights
        insights = {
            'keyword': keyword,
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'avg_ctr': avg_ctr,
            'avg_position': avg_position,
            'time_series': time_series,
            'pages': keyword_pages
        }
        
        return insights
    except Exception as e:
        logger.error(f"Error getting keyword insights: {str(e)}")
        return {
            'keyword': keyword,
            'total_clicks': 0,
            'total_impressions': 0,
            'avg_ctr': 0,
            'avg_position': 0,
            'time_series': [],
            'pages': []
        }
```

#### Step 4: Create UI Components

1. **Create Login Component**

Create a new file at `/workspace/AI-Writer/lib/integrations/google/components.py`:

```python
"""UI components for Google integration."""

import streamlit as st
from .auth import get_google_auth_url, is_authenticated, logout
from .search_console import get_site_list, get_top_keywords, get_top_pages, get_keyword_insights

def render_google_login_button():
    """Render Google login button."""
    if not is_authenticated():
        auth_url = get_google_auth_url()
        
        st.markdown("""
            <style>
            .google-button {
                display: inline-flex;
                align-items: center;
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0;
                cursor: pointer;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
                font-weight: 500;
                height: 40px;
                transition: background-color 0.3s;
            }
            .google-button:hover {
                background-color: #357AE8;
            }
            .google-button:active {
                background-color: #2A67D4;
            }
            .google-icon-wrapper {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                background-color: white;
                border-radius: 2px;
                margin-right: 1px;
            }
            .google-icon {
                width: 18px;
                height: 18px;
            }
            .google-text {
                padding: 0 16px;
            }
            </style>
            
            <a href="{auth_url}" class="google-button">
                <div class="google-icon-wrapper">
                    <img class="google-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"/>
                </div>
                <span class="google-text">Sign in with Google</span>
            </a>
        """.format(auth_url=auth_url), unsafe_allow_html=True)
    else:
        user_info = st.session_state.google_user_info
        
        # Display user info
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(user_info.get('picture', ''), width=50)
        
        with col2:
            st.markdown(f"**{user_info.get('name', 'User')}**")
            st.markdown(f"{user_info.get('email', '')}")
        
        # Logout button
        if st.button("Sign Out"):
            logout()
            st.experimental_rerun()

def render_site_selector():
    """Render Google Search Console site selector."""
    if not is_authenticated():
        st.warning("Please sign in with Google to access Search Console data.")
        return None
    
    # Get site list
    sites = get_site_list()
    
    if not sites:
        st.warning("No verified sites found in your Search Console account.")
        return None
    
    # Create site options
    site_options = [site['site_url'] for site in sites]
    
    # Select site
    selected_site = st.selectbox(
        "Select a website",
        options=site_options,
        index=0 if site_options else None,
        format_func=lambda x: x.replace("sc-domain:", "")
    )
    
    return selected_site

def render_search_console_dashboard(site_url):
    """Render Google Search Console dashboard.
    
    Args:
        site_url: URL of the selected site
    """
    if not site_url:
        return
    
    st.markdown("## Search Console Insights")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Top Keywords", "Top Pages", "Keyword Research"])
    
    with tab1:
        st.markdown("### Top Keywords")
        
        # Date range selector
        days = st.slider("Time period (days)", min_value=7, max_value=90, value=30, step=1)
        
        # Get top keywords
        with st.spinner("Loading keyword data..."):
            keywords = get_top_keywords(site_url, days=days, limit=100)
        
        if not keywords:
            st.info("No keyword data available for this site.")
            return
        
        # Display keywords table
        st.dataframe(
            keywords,
            column_config={
                "keyword": "Keyword",
                "clicks": st.column_config.NumberColumn("Clicks", format="%d"),
                "impressions": st.column_config.NumberColumn("Impressions", format="%d"),
                "ctr": st.column_config.NumberColumn("CTR", format="%.2f%%"),
                "position": st.column_config.NumberColumn("Position", format="%.1f")
            },
            hide_index=True
        )
    
    with tab2:
        st.markdown("### Top Pages")
        
        # Date range selector
        days = st.slider("Time period (days)", min_value=7, max_value=90, value=30, step=1, key="pages_days")
        
        # Get top pages
        with st.spinner("Loading page data..."):
            pages = get_top_pages(site_url, days=days, limit=100)
        
        if not pages:
            st.info("No page data available for this site.")
            return
        
        # Display pages table
        st.dataframe(
            pages,
            column_config={
                "page": "Page URL",
                "clicks": st.column_config.NumberColumn("Clicks", format="%d"),
                "impressions": st.column_config.NumberColumn("Impressions", format="%d"),
                "ctr": st.column_config.NumberColumn("CTR", format="%.2f%%"),
                "position": st.column_config.NumberColumn("Position", format="%.1f")
            },
            hide_index=True
        )
    
    with tab3:
        st.markdown("### Keyword Research")
        
        # Keyword input
        keyword = st.text_input("Enter a keyword to analyze")
        
        if keyword:
            # Get keyword insights
            with st.spinner(f"Analyzing '{keyword}'..."):
                insights = get_keyword_insights(keyword, site_url, days=90)
            
            # Display insights
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Clicks", f"{insights['total_clicks']:,}")
            
            with col2:
                st.metric("Impressions", f"{insights['total_impressions']:,}")
            
            with col3:
                st.metric("Avg. CTR", f"{insights['avg_ctr']:.2f}%")
            
            with col4:
                st.metric("Avg. Position", f"{insights['avg_position']:.1f}")
            
            # Time series chart
            if insights['time_series']:
                st.markdown("#### Performance Over Time")
                
                # Prepare data for chart
                chart_data = {
                    'date': [item['date'] for item in insights['time_series']],
                    'clicks': [item['clicks'] for item in insights['time_series']],
                    'impressions': [item['impressions'] for item in insights['time_series']],
                    'position': [item['position'] for item in insights['time_series']]
                }
                
                # Create tabs for different metrics
                chart_tab1, chart_tab2, chart_tab3 = st.tabs(["Clicks", "Impressions", "Position"])
                
                with chart_tab1:
                    st.line_chart(chart_data, x='date', y='clicks')
                
                with chart_tab2:
                    st.line_chart(chart_data, x='date', y='impressions')
                
                with chart_tab3:
                    # Invert position axis (lower is better)
                    position_chart = {
                        'date': chart_data['date'],
                        'position': [-pos for pos in chart_data['position']]  # Invert values
                    }
                    st.line_chart(position_chart, x='date', y='position')
                    st.caption("Note: Position axis is inverted (higher is better)")
            
            # Ranking pages
            if insights['pages']:
                st.markdown("#### Pages Ranking for this Keyword")
                
                st.dataframe(
                    insights['pages'],
                    column_config={
                        "page": "Page URL",
                        "clicks": st.column_config.NumberColumn("Clicks", format="%d"),
                        "impressions": st.column_config.NumberColumn("Impressions", format="%d"),
                        "ctr": st.column_config.NumberColumn("CTR", format="%.2f%%"),
                        "position": st.column_config.NumberColumn("Position", format="%.1f")
                    },
                    hide_index=True
                )
            
            # Content suggestions
            st.markdown("#### Content Suggestions")
            
            if st.button("Generate Content Ideas"):
                with st.spinner("Generating content ideas..."):
                    # This would connect to your AI content generation system
                    # For now, we'll just show a placeholder
                    st.info("This would connect to your AI content generation system to create content ideas based on this keyword's performance data.")
```

2. **Create Main Integration Page**

Create a new file at `/workspace/AI-Writer/lib/integrations/google/page.py`:

```python
"""Google integration page for AI-Writer."""

import streamlit as st
from .components import render_google_login_button, render_site_selector, render_search_console_dashboard
from .callback_handler import handle_oauth_callback

def render_google_integration_page():
    """Render the Google integration page."""
    st.title("Google Integration")
    
    # Handle OAuth callback if present
    handle_oauth_callback()
    
    # Display login/user info
    st.markdown("### Google Account")
    render_google_login_button()
    
    # Separator
    st.markdown("---")
    
    # Search Console section
    st.markdown("### Google Search Console")
    st.markdown("""
        Connect to Google Search Console to access search analytics data for your websites.
        This data will help you optimize your content for better search visibility.
    """)
    
    # Site selector
    selected_site = render_site_selector()
    
    # Display dashboard if site is selected
    if selected_site:
        render_search_console_dashboard(selected_site)
```

#### Step 5: Update Main Application

1. **Add Google Integration to Sidebar**

Update the sidebar in the main application file (`alwrity.py`):

```python
# Add to imports
from lib.integrations.google.page import render_google_integration_page

# Add to sidebar menu
with st.sidebar:
    st.title("AI-Writer")
    
    # Existing menu items...
    
    # Add Google Integration option
    if st.sidebar.selectbox("Integrations", ["None", "Google"]) == "Google":
        page = "google_integration"
    
    # Existing sidebar code...

# Add to page router
if page == "google_integration":
    render_google_integration_page()
```

2. **Add Google Credentials to Streamlit Secrets**

Create a file at `/.streamlit/secrets.toml`:

```toml
[google_oauth]
web = {
  "client_id": "YOUR_CLIENT_ID",
  "project_id": "ai-writer",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_secret": "YOUR_CLIENT_SECRET",
  "redirect_uris": ["http://localhost:8501/oauth/callback"],
  "javascript_origins": ["http://localhost:8501"]
}
```

### Phase 2: Content Enhancement with GSC Data

#### Step 1: Create Keyword Research Module

Create a new file at `/workspace/AI-Writer/lib/integrations/google/keyword_research.py`:

```python
"""Keyword research module using Google Search Console data."""

from typing import Dict, List, Any, Optional
import streamlit as st
from loguru import logger
from .search_console import get_top_keywords, get_keyword_insights

def get_content_opportunities(site_url: str, min_impressions: int = 100, max_position: float = 20.0) -> List[Dict[str, Any]]:
    """Find content opportunities based on GSC data.
    
    Args:
        site_url: URL of the site
        min_impressions: Minimum impressions threshold
        max_position: Maximum position threshold
        
    Returns:
        List[Dict[str, Any]]: List of content opportunities
    """
    try:
        # Get top keywords
        keywords = get_top_keywords(site_url, days=90, limit=1000)
        
        # Filter for opportunities
        opportunities = [
            keyword for keyword in keywords
            if keyword['impressions'] >= min_impressions
            and keyword['position'] <= max_position
            and keyword['position'] > 3  # Not already in top 3
        ]
        
        # Sort by potential (impressions * (11 - position)/10)
        # This prioritizes keywords with high impressions and positions 4-10
        for opp in opportunities:
            opp['potential'] = opp['impressions'] * (11 - min(opp['position'], 10)) / 10
        
        opportunities.sort(key=lambda x: x['potential'], reverse=True)
        
        return opportunities[:100]  # Return top 100 opportunities
    except Exception as e:
        logger.error(f"Error finding content opportunities: {str(e)}")
        return []

def get_keyword_clusters(keywords: List[Dict[str, Any]], threshold: int = 3) -> List[Dict[str, Any]]:
    """Group keywords into clusters based on common words.
    
    Args:
        keywords: List of keywords with metrics
        threshold: Minimum number of keywords to form a cluster
        
    Returns:
        List[Dict[str, Any]]: List of keyword clusters
    """
    try:
        # Extract keyword strings
        keyword_strings = [k['keyword'].lower() for k in keywords]
        
        # Create word frequency map
        word_map = {}
        for kw in keyword_strings:
            words = kw.split()
            for word in words:
                if len(word) > 3:  # Ignore short words
                    if word not in word_map:
                        word_map[word] = []
                    word_map[word].append(kw)
        
        # Find clusters
        clusters = []
        for word, kws in word_map.items():
            if len(kws) >= threshold:
                # Get full keyword data for each keyword in cluster
                cluster_data = [
                    k for k in keywords
                    if k['keyword'].lower() in kws
                ]
                
                # Calculate cluster metrics
                total_impressions = sum(k['impressions'] for k in cluster_data)
                total_clicks = sum(k['clicks'] for k in cluster_data)
                avg_position = sum(k['position'] for k in cluster_data) / len(cluster_data)
                
                clusters.append({
                    'topic': word,
                    'keywords': cluster_data,
                    'keyword_count': len(cluster_data),
                    'total_impressions': total_impressions,
                    'total_clicks': total_clicks,
                    'avg_position': avg_position
                })
        
        # Sort clusters by total impressions
        clusters.sort(key=lambda x: x['total_impressions'], reverse=True)
        
        return clusters
    except Exception as e:
        logger.error(f"Error creating keyword clusters: {str(e)}")
        return []

def generate_content_brief(keyword: str, site_url: str) -> Dict[str, Any]:
    """Generate a content brief for a keyword based on GSC data.
    
    Args:
        keyword: Target keyword
        site_url: URL of the site
        
    Returns:
        Dict[str, Any]: Content brief
    """
    try:
        # Get keyword insights
        insights = get_keyword_insights(keyword, site_url, days=90)
        
        # Get top keywords (for related keywords)
        all_keywords = get_top_keywords(site_url, days=90, limit=1000)
        
        # Find related keywords
        related_keywords = [
            k for k in all_keywords
            if keyword.lower() in k['keyword'].lower() and k['keyword'].lower() != keyword.lower()
        ]
        
        # Sort related keywords by impressions
        related_keywords.sort(key=lambda x: x['impressions'], reverse=True)
        
        # Create content brief
        brief = {
            'primary_keyword': keyword,
            'search_metrics': {
                'monthly_impressions': insights['total_impressions'] // 3,  # Approximate monthly
                'monthly_clicks': insights['total_clicks'] // 3,
                'avg_position': insights['avg_position'],
                'avg_ctr': insights['avg_ctr']
            },
            'related_keywords': related_keywords[:20],  # Top 20 related keywords
            'competing_pages': insights['pages'],
            'recommended_headings': [],  # Will be filled by AI
            'content_suggestions': []  # Will be filled by AI
        }
        
        return brief
    except Exception as e:
        logger.error(f"Error generating content brief: {str(e)}")
        return {
            'primary_keyword': keyword,
            'search_metrics': {
                'monthly_impressions': 0,
                'monthly_clicks': 0,
                'avg_position': 0,
                'avg_ctr': 0
            },
            'related_keywords': [],
            'competing_pages': [],
            'recommended_headings': [],
            'content_suggestions': []
        }
```

#### Step 2: Integrate with Content Generation

1. **Create GSC-Enhanced Content Generator**

Create a new file at `/workspace/AI-Writer/lib/integrations/google/content_generator.py`:

```python
"""Content generator enhanced with Google Search Console data."""

from typing import Dict, List, Any, Optional
import streamlit as st
from loguru import logger
from .keyword_research import generate_content_brief
from ...ai_writers.blog_writer import generate_blog_post

def generate_seo_optimized_content(
    keyword: str,
    site_url: str,
    content_type: str = "blog",
    length: str = "medium"
) -> Dict[str, Any]:
    """Generate SEO-optimized content using GSC data.
    
    Args:
        keyword: Target keyword
        site_url: URL of the site
        content_type: Type of content to generate
        length: Content length
        
    Returns:
        Dict[str, Any]: Generated content
    """
    try:
        # Generate content brief
        brief = generate_content_brief(keyword, site_url)
        
        # Extract related keywords
        related_keywords = [k['keyword'] for k in brief['related_keywords']]
        
        # Prepare prompt enhancements
        prompt_enhancements = {
            'primary_keyword': brief['primary_keyword'],
            'related_keywords': related_keywords,
            'search_position': brief['search_metrics']['avg_position'],
            'monthly_impressions': brief['search_metrics']['monthly_impressions'],
            'competing_urls': [p['page'] for p in brief['competing_pages'][:5]]
        }
        
        # Generate content with enhanced prompt
        content = generate_blog_post(
            keyword=keyword,
            content_type=content_type,
            length=length,
            prompt_enhancements=prompt_enhancements
        )
        
        # Add brief data to the result
        content['brief'] = brief
        
        return content
    except Exception as e:
        logger.error(f"Error generating SEO-optimized content: {str(e)}")
        return {
            'title': f"Error generating content for '{keyword}'",
            'content': f"An error occurred: {str(e)}",
            'brief': {}
        }
```

2. **Create Content Optimization Component**

Create a new file at `/workspace/AI-Writer/lib/integrations/google/content_optimizer.py`:

```python
"""Content optimization using Google Search Console data."""

from typing import Dict, List, Any, Optional
import streamlit as st
from loguru import logger
from .search_console import get_keyword_insights
from ...seo_tools.analyzer import analyze_content_for_seo

def optimize_existing_content(
    content: str,
    keyword: str,
    site_url: str
) -> Dict[str, Any]:
    """Optimize existing content using GSC data.
    
    Args:
        content: Existing content
        keyword: Target keyword
        site_url: URL of the site
        
    Returns:
        Dict[str, Any]: Optimization suggestions
    """
    try:
        # Get keyword insights
        insights = get_keyword_insights(keyword, site_url, days=90)
        
        # Analyze content for SEO
        seo_analysis = analyze_content_for_seo(content, keyword)
        
        # Generate optimization suggestions
        suggestions = []
        
        # Check keyword density
        if seo_analysis['keyword_density'] < 0.5:
            suggestions.append({
                'type': 'keyword_density',
                'severity': 'high',
                'message': f"Keyword density is too low ({seo_analysis['keyword_density']:.2f}%). Aim for 1-2%.",
                'action': "Add more instances of the keyword in a natural way."
            })
        elif seo_analysis['keyword_density'] > 3:
            suggestions.append({
                'type': 'keyword_density',
                'severity': 'medium',
                'message': f"Keyword density is too high ({seo_analysis['keyword_density']:.2f}%). Aim for 1-2%.",
                'action': "Reduce keyword usage to avoid keyword stuffing."
            })
        
        # Check title
        if keyword.lower() not in seo_analysis['title'].lower():
            suggestions.append({
                'type': 'title',
                'severity': 'high',
                'message': "Primary keyword is missing from the title.",
                'action': f"Add '{keyword}' to the title in a natural way."
            })
        
        # Check headings
        if not any(keyword.lower() in h.lower() for h in seo_analysis['headings']):
            suggestions.append({
                'type': 'headings',
                'severity': 'medium',
                'message': "Primary keyword is missing from all headings.",
                'action': f"Add '{keyword}' to at least one heading (preferably H2)."
            })
        
        # Check content length
        if seo_analysis['word_count'] < 300:
            suggestions.append({
                'type': 'content_length',
                'severity': 'high',
                'message': f"Content is too short ({seo_analysis['word_count']} words). Aim for at least 800 words.",
                'action': "Expand the content with more valuable information."
            })
        elif seo_analysis['word_count'] < 800:
            suggestions.append({
                'type': 'content_length',
                'severity': 'medium',
                'message': f"Content is relatively short ({seo_analysis['word_count']} words). Aim for 1000+ words for competitive keywords.",
                'action': "Consider adding more depth to the content."
            })
        
        # Check readability
        if seo_analysis['readability_score'] < 50:
            suggestions.append({
                'type': 'readability',
                'severity': 'medium',
                'message': f"Content readability is low ({seo_analysis['readability_score']}/100).",
                'action': "Simplify sentences, use shorter paragraphs, and avoid jargon."
            })
        
        # Check competing pages
        competing_pages = insights['pages']
        if competing_pages:
            top_competing_page = competing_pages[0]
            suggestions.append({
                'type': 'competition',
                'severity': 'info',
                'message': f"Your top competing page ranks at position {top_competing_page['position']:.1f}.",
                'action': f"Review the content at {top_competing_page['page']} for insights."
            })
        
        # Compile results
        result = {
            'keyword': keyword,
            'search_metrics': {
                'monthly_impressions': insights['total_impressions'] // 3,
                'monthly_clicks': insights['total_clicks'] // 3,
                'avg_position': insights['avg_position'],
                'avg_ctr': insights['avg_ctr']
            },
            'seo_analysis': seo_analysis,
            'suggestions': suggestions
        }
        
        return result
    except Exception as e:
        logger.error(f"Error optimizing content: {str(e)}")
        return {
            'keyword': keyword,
            'search_metrics': {},
            'seo_analysis': {},
            'suggestions': [{
                'type': 'error',
                'severity': 'high',
                'message': f"Error analyzing content: {str(e)}",
                'action': "Please try again or contact support."
            }]
        }
```

#### Step 3: Create Content Planning Component

Create a new file at `/workspace/AI-Writer/lib/integrations/google/content_planner.py`:

```python
"""Content planning using Google Search Console data."""

import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
from .keyword_research import get_content_opportunities, get_keyword_clusters
from .search_console import get_top_keywords

def render_content_planner(site_url: str):
    """Render content planning interface using GSC data.
    
    Args:
        site_url: URL of the site
    """
    st.markdown("## Content Planning")
    st.markdown("""
        Use your Google Search Console data to plan your content strategy.
        Identify opportunities, organize topics, and create a content calendar.
    """)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Content Opportunities", "Topic Clusters", "Content Calendar"])
    
    with tab1:
        st.markdown("### Content Opportunities")
        st.markdown("""
            Find keywords where you're ranking on page 1-2 but not in the top 3.
            These are opportunities to improve existing content or create new content.
        """)
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            min_impressions = st.slider(
                "Minimum monthly impressions",
                min_value=10,
                max_value=1000,
                value=100,
                step=10
            )
        
        with col2:
            max_position = st.slider(
                "Maximum position",
                min_value=5.0,
                max_value=30.0,
                value=20.0,
                step=1.0
            )
        
        # Get opportunities
        if st.button("Find Opportunities"):
            with st.spinner("Analyzing search data..."):
                opportunities = get_content_opportunities(
                    site_url=site_url,
                    min_impressions=min_impressions,
                    max_position=max_position
                )
            
            if not opportunities:
                st.info("No content opportunities found with the current filters.")
            else:
                # Display opportunities
                st.markdown(f"Found {len(opportunities)} content opportunities:")
                
                # Create dataframe
                st.dataframe(
                    opportunities,
                    column_config={
                        "keyword": "Keyword",
                        "clicks": st.column_config.NumberColumn("Clicks", format="%d"),
                        "impressions": st.column_config.NumberColumn("Impressions", format="%d"),
                        "ctr": st.column_config.NumberColumn("CTR", format="%.2f%%"),
                        "position": st.column_config.NumberColumn("Position", format="%.1f"),
                        "potential": st.column_config.NumberColumn("Potential", format="%.1f")
                    },
                    hide_index=True
                )
                
                # Action buttons for selected opportunity
                st.markdown("### Take Action")
                selected_keyword = st.selectbox(
                    "Select a keyword to take action on",
                    options=[o['keyword'] for o in opportunities]
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Create New Content", key="create_new"):
                        st.session_state.selected_keyword = selected_keyword
                        st.session_state.action = "create_content"
                        st.experimental_rerun()
                
                with col2:
                    if st.button("Optimize Existing Content", key="optimize"):
                        st.session_state.selected_keyword = selected_keyword
                        st.session_state.action = "optimize_content"
                        st.experimental_rerun()
    
    with tab2:
        st.markdown("### Topic Clusters")
        st.markdown("""
            Group your keywords into topic clusters to organize your content strategy.
            This helps identify themes and create comprehensive content around topics.
        """)
        
        # Cluster settings
        min_cluster_size = st.slider(
            "Minimum cluster size",
            min_value=2,
            max_value=10,
            value=3,
            step=1
        )
        
        # Get clusters
        if st.button("Generate Topic Clusters"):
            with st.spinner("Analyzing keywords..."):
                # Get top keywords
                keywords = get_top_keywords(site_url, days=90, limit=1000)
                
                # Generate clusters
                clusters = get_keyword_clusters(
                    keywords=keywords,
                    threshold=min_cluster_size
                )
            
            if not clusters:
                st.info("No topic clusters found with the current settings.")
            else:
                # Display clusters
                st.markdown(f"Found {len(clusters)} topic clusters:")
                
                for i, cluster in enumerate(clusters):
                    with st.expander(f"Cluster: {cluster['topic']} ({cluster['keyword_count']} keywords)"):
                        st.markdown(f"**Total Impressions:** {cluster['total_impressions']:,}")
                        st.markdown(f"**Total Clicks:** {cluster['total_clicks']:,}")
                        st.markdown(f"**Average Position:** {cluster['avg_position']:.1f}")
                        
                        # Display keywords in cluster
                        st.dataframe(
                            cluster['keywords'],
                            column_config={
                                "keyword": "Keyword",
                                "clicks": st.column_config.NumberColumn("Clicks", format="%d"),
                                "impressions": st.column_config.NumberColumn("Impressions", format="%d"),
                                "position": st.column_config.NumberColumn("Position", format="%.1f")
                            },
                            hide_index=True
                        )
                        
                        # Action button
                        if st.button("Create Cluster Content", key=f"cluster_{i}"):
                            st.session_state.selected_cluster = cluster
                            st.session_state.action = "create_cluster_content"
                            st.experimental_rerun()
    
    with tab3:
        st.markdown("### Content Calendar")
        st.markdown("""
            Create a content calendar based on your search data and opportunities.
            Plan your content strategy for the coming weeks or months.
        """)
        
        # Calendar settings
        num_weeks = st.slider(
            "Number of weeks to plan",
            min_value=1,
            max_value=12,
            value=4,
            step=1
        )
        
        posts_per_week = st.slider(
            "Posts per week",
            min_value=1,
            max_value=7,
            value=2,
            step=1
        )
        
        # Generate calendar
        if st.button("Generate Content Calendar"):
            with st.spinner("Creating content calendar..."):
                # Get opportunities
                opportunities = get_content_opportunities(
                    site_url=site_url,
                    min_impressions=50,
                    max_position=30.0
                )
                
                # Sort by potential
                opportunities.sort(key=lambda x: x['potential'], reverse=True)
                
                # Calculate total posts needed
                total_posts = num_weeks * posts_per_week
                
                # Limit opportunities to needed posts
                selected_opportunities = opportunities[:total_posts]
                
                # Create calendar
                calendar = []
                start_date = datetime.now() + timedelta(days=7)  # Start next week
                
                for week in range(num_weeks):
                    week_start = start_date + timedelta(weeks=week)
                    
                    for day in range(posts_per_week):
                        opp_index = week * posts_per_week + day
                        
                        if opp_index < len(selected_opportunities):
                            post_date = week_start + timedelta(days=day)
                            
                            calendar.append({
                                'date': post_date.strftime('%Y-%m-%d'),
                                'keyword': selected_opportunities[opp_index]['keyword'],
                                'impressions': selected_opportunities[opp_index]['impressions'],
                                'position': selected_opportunities[opp_index]['position'],
                                'potential': selected_opportunities[opp_index]['potential']
                            })
            
            if not calendar:
                st.info("Could not generate content calendar. Try adjusting your filters.")
            else:
                # Display calendar
                st.markdown(f"Generated content calendar with {len(calendar)} posts:")
                
                # Group by week
                weeks = {}
                for post in calendar:
                    post_date = datetime.strptime(post['date'], '%Y-%m-%d')
                    week_num = post_date.isocalendar()[1]
                    week_start = post_date - timedelta(days=post_date.weekday())
                    week_key = f"Week {week_num} ({week_start.strftime('%b %d')})"
                    
                    if week_key not in weeks:
                        weeks[week_key] = []
                    
                    weeks[week_key].append(post)
                
                # Display by week
                for week_key, posts in weeks.items():
                    with st.expander(week_key, expanded=True):
                        for post in posts:
                            st.markdown(f"**{post['date']}:** {post['keyword']}")
                            st.markdown(f"Impressions: {post['impressions']:,} | Position: {post['position']:.1f}")
                            st.markdown("---")
                
                # Export button
                if st.download_button(
                    label="Export Calendar (CSV)",
                    data="\n".join([
                        "date,keyword,impressions,position,potential",
                        *[f"{post['date']},{post['keyword']},{post['impressions']},{post['position']},{post['potential']}" for post in calendar]
                    ]),
                    file_name="content_calendar.csv",
                    mime="text/csv"
                ):
                    st.success("Calendar exported successfully!")
```

#### Step 4: Integrate with Content Writers

1. **Update Blog Writer**

Modify the existing blog writer to accept GSC data:

```python
# Add to blog_writer.py

def generate_blog_post(
    keyword: str,
    content_type: str = "blog",
    length: str = "medium",
    prompt_enhancements: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Generate a blog post with optional GSC data enhancement.
    
    Args:
        keyword: Target keyword
        content_type: Type of content to generate
        length: Content length
        prompt_enhancements: Optional GSC data for prompt enhancement
        
    Returns:
        Dict[str, Any]: Generated content
    """
    # Existing code...
    
    # Enhance prompt with GSC data if available
    if prompt_enhancements:
        # Add related keywords to prompt
        if 'related_keywords' in prompt_enhancements:
            related_kw_str = ", ".join(prompt_enhancements['related_keywords'][:5])
            prompt += f"\nInclude these related keywords naturally: {related_kw_str}"
        
        # Add search position context
        if 'search_position' in prompt_enhancements:
            position = prompt_enhancements['search_position']
            if position > 10:
                prompt += f"\nThis keyword currently ranks at position {position:.1f}, which is on page 2. Create comprehensive content to improve ranking."
            else:
                prompt += f"\nThis keyword currently ranks at position {position:.1f}. Enhance the content to improve ranking further."
        
        # Add impression data
        if 'monthly_impressions' in prompt_enhancements:
            impressions = prompt_enhancements['monthly_impressions']
            prompt += f"\nThis keyword gets approximately {impressions} monthly impressions."
        
        # Add competing URLs
        if 'competing_urls' in prompt_enhancements:
            prompt += "\nMake sure your content is more comprehensive than competing pages."
    
    # Continue with existing code...
```

2. **Add GSC Data to SEO Tools**

Update the SEO analyzer to incorporate GSC data:

```python
# Add to seo_tools/analyzer.py

def analyze_content_with_gsc(
    content: str,
    keyword: str,
    gsc_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze content with GSC data enhancement.
    
    Args:
        content: Content to analyze
        keyword: Target keyword
        gsc_data: Google Search Console data
        
    Returns:
        Dict[str, Any]: Enhanced analysis
    """
    # Get basic SEO analysis
    analysis = analyze_content_for_seo(content, keyword)
    
    # Enhance with GSC data
    if gsc_data:
        # Add search metrics
        analysis['search_metrics'] = {
            'impressions': gsc_data.get('impressions', 0),
            'clicks': gsc_data.get('clicks', 0),
            'position': gsc_data.get('position', 0),
            'ctr': gsc_data.get('ctr', 0)
        }
        
        # Add competition analysis
        if 'competing_pages' in gsc_data:
            analysis['competition'] = {
                'competing_pages': gsc_data['competing_pages'],
                'ranking_gap': analysis['word_count'] - gsc_data.get('avg_competitor_length', 0)
            }
        
        # Add keyword opportunity score
        if 'position' in gsc_data and 'impressions' in gsc_data:
            position = gsc_data['position']
            impressions = gsc_data['impressions']
            
            # Calculate opportunity score (higher for keywords with good impressions but not yet in top 3)
            if position <= 3:
                opportunity_score = 30  # Already ranking well
            elif position <= 10:
                opportunity_score = 70  # On first page but not top 3
            elif position <= 20:
                opportunity_score = 50  # On second page
            else:
                opportunity_score = 30  # Beyond second page
            
            # Adjust for impressions
            if impressions > 1000:
                opportunity_score += 30
            elif impressions > 500:
                opportunity_score += 20
            elif impressions > 100:
                opportunity_score += 10
            
            # Cap at 100
            opportunity_score = min(opportunity_score, 100)
            
            analysis['opportunity_score'] = opportunity_score
    
    return analysis
```

### Phase 3: Testing Plan

#### Step 1: Unit Testing

1. **Create Test Files**

Create a new file at `/workspace/AI-Writer/tests/integrations/google/test_auth.py`:

```python
"""Unit tests for Google authentication module."""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from lib.integrations.google.auth import (
    get_google_auth_url,
    handle_auth_callback,
    save_credentials,
    load_credentials,
    get_user_info,
    credentials_to_dict,
    is_authenticated
)

class TestGoogleAuth(unittest.TestCase):
    """Test cases for Google authentication module."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock session state
        self.session_state_patch = patch('streamlit.session_state', {})
        self.mock_session_state = self.session_state_patch.start()
        
        # Mock secrets
        self.secrets_patch = patch('streamlit.secrets', {
            'google_oauth': {
                'web': {
                    'client_id': 'test_client_id',
                    'client_secret': 'test_client_secret',
                    'redirect_uris': ['http://localhost:8501/oauth/callback']
                }
            }
        })
        self.mock_secrets = self.secrets_patch.start()
    
    def tearDown(self):
        """Clean up after tests."""
        self.session_state_patch.stop()
        self.secrets_patch.stop()
    
    @patch('lib.integrations.google.auth.Flow')
    def test_get_google_auth_url(self, mock_flow):
        """Test generating Google auth URL."""
        # Mock flow instance
        mock_flow_instance = MagicMock()
        mock_flow_instance.authorization_url.return_value = ('https://test-auth-url.com', None)
        mock_flow.from_client_config.return_value = mock_flow_instance
        
        # Call function
        url = get_google_auth_url()
        
        # Assertions
        self.assertEqual(url, 'https://test-auth-url.com')
        mock_flow.from_client_config.assert_called_once()
        mock_flow_instance.authorization_url.assert_called_once()
    
    @patch('lib.integrations.google.auth.get_user_info')
    def test_handle_auth_callback(self, mock_get_user_info):
        """Test handling auth callback."""
        # Mock flow in session state
        mock_flow = MagicMock()
        mock_flow.credentials = MagicMock()
        self.mock_session_state['google_auth_flow'] = mock_flow
        
        # Mock user info
        mock_get_user_info.return_value = {'email': 'test@example.com', 'name': 'Test User'}
        
        # Call function
        success, user_info = handle_auth_callback('test_code')
        
        # Assertions
        self.assertTrue(success)
        self.assertEqual(user_info['email'], 'test@example.com')
        mock_flow.fetch_token.assert_called_once_with(code='test_code')
        mock_get_user_info.assert_called_once()
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    @patch('lib.integrations.google.auth.get_user_info')
    def test_save_credentials(self, mock_get_user_info, mock_json_dump, mock_open):
        """Test saving credentials."""
        # Mock credentials
        mock_credentials = MagicMock()
        mock_credentials.token = 'test_token'
        mock_credentials.refresh_token = 'test_refresh_token'
        
        # Mock user info
        mock_get_user_info.return_value = {'email': 'test@example.com'}
        
        # Call function
        result = save_credentials(mock_credentials)
        
        # Assertions
        self.assertTrue(result)
        mock_get_user_info.assert_called_once()
        mock_open.assert_called_once()
        mock_json_dump.assert_called_once()
    
    def test_credentials_to_dict(self):
        """Test converting credentials to dictionary."""
        # Mock credentials
        mock_credentials = MagicMock()
        mock_credentials.token = 'test_token'
        mock_credentials.refresh_token = 'test_refresh_token'
        mock_credentials.token_uri = 'test_token_uri'
        mock_credentials.client_id = 'test_client_id'
        mock_credentials.client_secret = 'test_client_secret'
        mock_credentials.scopes = ['test_scope']
        
        # Call function
        result = credentials_to_dict(mock_credentials)
        
        # Assertions
        self.assertEqual(result['token'], 'test_token')
        self.assertEqual(result['refresh_token'], 'test_refresh_token')
        self.assertEqual(result['client_id'], 'test_client_id')
        self.assertEqual(result['scopes'], ['test_scope'])
    
    def test_is_authenticated(self):
        """Test authentication check."""
        # Test not authenticated
        self.assertFalse(is_authenticated())
        
        # Test authenticated
        self.mock_session_state['google_credentials'] = {'token': 'test'}
        self.mock_session_state['google_user_info'] = {'email': 'test@example.com'}
        self.assertTrue(is_authenticated())

if __name__ == '__main__':
    unittest.main()
```

2. **Create Test for Search Console API**

Create a new file at `/workspace/AI-Writer/tests/integrations/google/test_search_console.py`:

```python
"""Unit tests for Google Search Console API module."""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from lib.integrations.google.search_console import (
    get_search_console_service,
    get_site_list,
    get_search_analytics,
    get_top_keywords,
    get_top_pages,
    get_keyword_insights
)

class TestSearchConsole(unittest.TestCase):
    """Test cases for Google Search Console API module."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock session state
        self.session_state_patch = patch('streamlit.session_state', {
            'google_credentials': {
                'token': 'test_token',
                'refresh_token': 'test_refresh_token',
                'token_uri': 'test_token_uri',
                'client_id': 'test_client_id',
                'client_secret': 'test_client_secret',
                'scopes': ['test_scope']
            }
        })
        self.mock_session_state = self.session_state_patch.start()
    
    def tearDown(self):
        """Clean up after tests."""
        self.session_state_patch.stop()
    
    @patch('lib.integrations.google.search_console.build')
    @patch('lib.integrations.google.search_console.Credentials')
    def test_get_search_console_service(self, mock_credentials, mock_build):
        """Test building Search Console service."""
        # Mock credentials
        mock_credentials_instance = MagicMock()
        mock_credentials.from_authorized_user_info.return_value = mock_credentials_instance
        
        # Mock service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Call function
        service = get_search_console_service(self.mock_session_state['google_credentials'])
        
        # Assertions
        self.assertEqual(service, mock_service)
        mock_credentials.from_authorized_user_info.assert_called_once()
        mock_build.assert_called_once_with('searchconsole', 'v1', credentials=mock_credentials_instance)
    
    @patch('lib.integrations.google.search_console.get_search_console_service')
    def test_get_site_list(self, mock_get_service):
        """Test getting site list."""
        # Mock service
        mock_service = MagicMock()
        mock_sites = MagicMock()
        mock_sites.list().execute.return_value = {
            'siteEntry': [
                {
                    'siteUrl': 'https://example.com/',
                    'permissionLevel': 'siteOwner'
                },
                {
                    'siteUrl': 'sc-domain:example.org',
                    'permissionLevel': 'siteFullUser'
                },
                {
                    'siteUrl': 'https://example.net/',
                    'permissionLevel': 'siteRestrictedUser'  # Should be filtered out
                }
            ]
        }
        mock_service.sites.return_value = mock_sites
        mock_get_service.return_value = mock_service
        
        # Call function
        sites = get_site_list()
        
        # Assertions
        self.assertEqual(len(sites), 2)  # Only 2 sites with sufficient permissions
        self.assertEqual(sites[0]['site_url'], 'https://example.com/')
        self.assertEqual(sites[0]['permission_level'], 'siteOwner')
        self.assertEqual(sites[0]['site_type'], 'Web')
        self.assertEqual(sites[1]['site_url'], 'sc-domain:example.org')
        self.assertEqual(sites[1]['site_type'], 'Domain Property')
    
    @patch('lib.integrations.google.search_console.get_search_console_service')
    def test_get_search_analytics(self, mock_get_service):
        """Test getting search analytics data."""
        # Mock service
        mock_service = MagicMock()
        mock_analytics = MagicMock()
        mock_analytics.query().execute.return_value = {
            'rows': [
                {
                    'keys': ['test keyword'],
                    'clicks': 100,
                    'impressions': 1000,
                    'ctr': 0.1,
                    'position': 5.5
                }
            ]
        }
        mock_service.searchanalytics.return_value = mock_analytics
        mock_get_service.return_value = mock_service
        
        # Call function
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        result = get_search_analytics(
            site_url='https://example.com/',
            start_date=start_date,
            end_date=end_date,
            dimensions=['query'],
            row_limit=100
        )
        
        # Assertions
        self.assertEqual(len(result['rows']), 1)
        mock_analytics.query.assert_called_once()
        call_args = mock_analytics.query.call_args[1]
        self.assertEqual(call_args['siteUrl'], 'https://example.com/')
        self.assertEqual(call_args['body']['dimensions'], ['query'])
        self.assertEqual(call_args['body']['rowLimit'], 100)
    
    @patch('lib.integrations.google.search_console.get_search_analytics')
    def test_get_top_keywords(self, mock_get_analytics):
        """Test getting top keywords."""
        # Mock analytics response
        mock_get_analytics.return_value = {
            'rows': [
                {
                    'keys': ['keyword1'],
                    'clicks': 100,
                    'impressions': 1000,
                    'ctr': 0.1,
                    'position': 5.5
                },
                {
                    'keys': ['keyword2'],
                    'clicks': 200,
                    'impressions': 2000,
                    'ctr': 0.1,
                    'position': 3.2
                }
            ]
        }
        
        # Call function
        keywords = get_top_keywords(
            site_url='https://example.com/',
            days=30,
            limit=100
        )
        
        # Assertions
        self.assertEqual(len(keywords), 2)
        self.assertEqual(keywords[0]['keyword'], 'keyword1')
        self.assertEqual(keywords[0]['clicks'], 100)
        self.assertEqual(keywords[0]['impressions'], 1000)
        self.assertEqual(keywords[0]['ctr'], 10.0)  # Converted to percentage
        self.assertEqual(keywords[0]['position'], 5.5)
        mock_get_analytics.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```

#### Step 2: Integration Testing

1. **Create Integration Test Script**

Create a new file at `/workspace/AI-Writer/tests/integrations/google/test_integration.py`:

```python
"""Integration tests for Google integration."""

import unittest
import os
import sys
from pathlib import Path
import streamlit as st
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from lib.integrations.google.auth import get_google_auth_url, handle_auth_callback
from lib.integrations.google.search_console import get_site_list, get_top_keywords
from lib.integrations.google.keyword_research import get_content_opportunities
from lib.integrations.google.content_generator import generate_seo_optimized_content

class TestGoogleIntegration(unittest.TestCase):
    """Integration tests for Google integration."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Check if we have real credentials for testing
        cls.has_real_credentials = os.environ.get('GOOGLE_TEST_CREDENTIALS') is not None
        
        if cls.has_real_credentials:
            # Load real credentials from environment
            import json
            credentials_json = os.environ.get('GOOGLE_TEST_CREDENTIALS')
            cls.test_credentials = json.loads(credentials_json)
            
            # Set up session state with real credentials
            st.session_state['google_credentials'] = cls.test_credentials
            st.session_state['google_user_info'] = {
                'email': os.environ.get('GOOGLE_TEST_EMAIL', 'test@example.com'),
                'name': 'Test User'
            }
    
    def test_auth_flow(self):
        """Test authentication flow."""
        # Skip if no real credentials
        if not self.has_real_credentials:
            self.skipTest("No real credentials available for testing")
        
        # Get auth URL
        auth_url = get_google_auth_url()
        
        # Verify URL format
        self.assertTrue(auth_url.startswith('https://accounts.google.com/o/oauth2/auth'))
        self.assertIn('client_id=', auth_url)
        self.assertIn('redirect_uri=', auth_url)
        self.assertIn('scope=', auth_url)
    
    def test_search_console_access(self):
        """Test Search Console API access."""
        # Skip if no real credentials
        if not self.has_real_credentials:
            self.skipTest("No real credentials available for testing")
        
        # Get site list
        sites = get_site_list()
        
        # Verify we got some sites
        self.assertIsInstance(sites, list)
        
        # If we have sites, test keyword data
        if sites:
            site_url = sites[0]['site_url']
            
            # Get top keywords
            keywords = get_top_keywords(site_url, days=30, limit=10)
            
            # Verify we got keyword data
            self.assertIsInstance(keywords, list)
            
            # If we have keywords, test content opportunities
            if keywords:
                # Get content opportunities
                opportunities = get_content_opportunities(site_url, min_impressions=10, max_position=50.0)
                
                # Verify we got opportunities
                self.assertIsInstance(opportunities, list)
    
    @patch('lib.integrations.google.content_generator.generate_blog_post')
    def test_content_generation(self, mock_generate_blog_post):
        """Test content generation with GSC data."""
        # Mock blog post generation
        mock_generate_blog_post.return_value = {
            'title': 'Test Blog Post',
            'content': 'This is a test blog post.'
        }
        
        # Generate content
        content = generate_seo_optimized_content(
            keyword='test keyword',
            site_url='https://example.com/',
            content_type='blog',
            length='medium'
        )
        
        # Verify content was generated
        self.assertEqual(content['title'], 'Test Blog Post')
        self.assertEqual(content['content'], 'This is a test blog post.')
        
        # Verify prompt enhancements were passed
        mock_generate_blog_post.assert_called_once()
        call_args = mock_generate_blog_post.call_args[1]
        self.assertEqual(call_args['keyword'], 'test keyword')
        self.assertEqual(call_args['content_type'], 'blog')
        self.assertEqual(call_args['length'], 'medium')
        self.assertIn('prompt_enhancements', call_args)

if __name__ == '__main__':
    unittest.main()
```

#### Step 3: End-to-End Testing

1. **Create Manual Test Plan**

Create a new file at `/workspace/AI-Writer/tests/integrations/google/manual_test_plan.md`:

```markdown
# Google Integration Manual Test Plan

This document outlines the manual testing procedures for the Google integration in AI-Writer.

## Prerequisites

- Google account with access to Search Console
- Website verified in Google Search Console
- AI-Writer development environment set up

## Test Cases

### 1. Authentication Flow

#### 1.1 Google Login

1. Navigate to the Google Integration page
2. Click "Sign in with Google"
3. Complete Google authentication flow
4. Verify user is redirected back to AI-Writer
5. Verify user info is displayed correctly

**Expected Result:** User is successfully authenticated and user info is displayed.

#### 1.2 Logout

1. Click "Sign Out" button
2. Verify user is logged out
3. Verify login button is displayed again

**Expected Result:** User is successfully logged out.

### 2. Search Console Access

#### 2.1 Site Selection

1. Authenticate with Google
2. Verify site selector displays user's verified sites
3. Select a site from the dropdown
4. Verify Search Console dashboard loads

**Expected Result:** User's verified sites are displayed and can be selected.

#### 2.2 Top Keywords

1. Select a site
2. Navigate to "Top Keywords" tab
3. Adjust time period slider
4. Verify keyword data loads and updates

**Expected Result:** Keyword data is displayed and updates when time period changes.

#### 2.3 Top Pages

1. Select a site
2. Navigate to "Top Pages" tab
3. Adjust time period slider
4. Verify page data loads and updates

**Expected Result:** Page data is displayed and updates when time period changes.

#### 2.4 Keyword Research

1. Select a site
2. Navigate to "Keyword Research" tab
3. Enter a keyword
4. Verify keyword insights are displayed
5. Verify performance charts are displayed
6. Verify ranking pages are displayed

**Expected Result:** Keyword insights and related data are displayed correctly.

### 3. Content Planning

#### 3.1 Content Opportunities

1. Navigate to Content Planning
2. Select "Content Opportunities" tab
3. Adjust filters
4. Click "Find Opportunities"
5. Verify opportunities are displayed
6. Select a keyword and click "Create New Content"
7. Verify redirection to content creation

**Expected Result:** Content opportunities are found and can be used for content creation.

#### 3.2 Topic Clusters

1. Navigate to Content Planning
2. Select "Topic Clusters" tab
3. Adjust cluster settings
4. Click "Generate Topic Clusters"
5. Verify clusters are displayed
6. Expand a cluster to view keywords
7. Click "Create Cluster Content"
8. Verify redirection to content creation

**Expected Result:** Topic clusters are generated and can be used for content creation.

#### 3.3 Content Calendar

1. Navigate to Content Planning
2. Select "Content Calendar" tab
3. Adjust calendar settings
4. Click "Generate Content Calendar"
5. Verify calendar is displayed
6. Verify export functionality works

**Expected Result:** Content calendar is generated and can be exported.

### 4. Content Creation

#### 4.1 SEO-Optimized Content

1. Select a keyword from opportunities
2. Click "Create New Content"
3. Verify GSC data is incorporated in the prompt
4. Generate content
5. Verify content includes related keywords
6. Verify content addresses search intent

**Expected Result:** Generated content is optimized based on GSC data.

#### 4.2 Content Optimization

1. Select a keyword
2. Click "Optimize Existing Content"
3. Enter or paste existing content
4. Click "Analyze Content"
5. Verify optimization suggestions are displayed
6. Apply suggestions
7. Verify content improvements

**Expected Result:** Content optimization suggestions are provided and can be applied.

## Test Execution Checklist

| Test Case | Status | Notes |
|-----------|--------|-------|
| 1.1 Google Login | | |
| 1.2 Logout | | |
| 2.1 Site Selection | | |
| 2.2 Top Keywords | | |
| 2.3 Top Pages | | |
| 2.4 Keyword Research | | |
| 3.1 Content Opportunities | | |
| 3.2 Topic Clusters | | |
| 3.3 Content Calendar | | |
| 4.1 SEO-Optimized Content | | |
| 4.2 Content Optimization | | |
```

#### Step 4: Automated Testing Setup

1. **Create GitHub Actions Workflow**

Create a new file at `/.github/workflows/google_integration_tests.yml`:

```yaml
name: Google Integration Tests

on:
  push:
    branches: [ main ]
    paths:
      - 'lib/integrations/google/**'
      - 'tests/integrations/google/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'lib/integrations/google/**'
      - 'tests/integrations/google/**'
  workflow_dispatch:

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest pytest-cov
    
    - name: Run unit tests
      run: |
        pytest tests/integrations/google/test_auth.py tests/integrations/google/test_search_console.py -v
    
    - name: Generate coverage report
      run: |
        pytest --cov=lib.integrations.google tests/integrations/google/ --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: google-integration
        fail_ci_if_error: false

  integration-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest
    
    - name: Run integration tests
      env:
        GOOGLE_TEST_CREDENTIALS: ${{ secrets.GOOGLE_TEST_CREDENTIALS }}
        GOOGLE_TEST_EMAIL: ${{ secrets.GOOGLE_TEST_EMAIL }}
      run: |
        pytest tests/integrations/google/test_integration.py -v
```

## Deployment Plan

### Phase 1: Development Environment

1. **Initial Setup**
   - Set up Google Cloud Project
   - Configure OAuth consent screen
   - Create OAuth credentials
   - Enable required APIs
   - Implement authentication module

2. **Local Testing**
   - Test authentication flow
   - Test Search Console API access
   - Test content generation with GSC data
   - Run unit tests

### Phase 2: Staging Environment

1. **Configuration**
   - Create staging Google Cloud Project
   - Configure OAuth for staging domain
   - Update redirect URIs
   - Set up staging environment variables

2. **Integration Testing**
   - Deploy to staging environment
   - Test end-to-end flow
   - Verify data accuracy
   - Test with multiple users and sites

3. **Performance Testing**
   - Test with large datasets
   - Optimize API calls
   - Implement caching if needed
   - Monitor API usage limits

### Phase 3: Production Deployment

1. **Final Configuration**
   - Create production Google Cloud Project
   - Configure OAuth for production domain
   - Set up production environment variables
   - Verify API quotas and limits

2. **Deployment**
   - Deploy to production
   - Monitor for errors
   - Verify authentication flow
   - Test with real user accounts

3. **Post-Deployment**
   - Monitor API usage
   - Collect user feedback
   - Address any issues
   - Document the integration

## User Documentation

### User Guide

Create a user guide that explains:

1. How to connect Google account
2. How to access Search Console data
3. How to use content opportunities
4. How to create SEO-optimized content
5. How to use the content calendar

### Video Tutorial

Create a video tutorial demonstrating:

1. Initial setup process
2. Finding content opportunities
3. Creating content with GSC data
4. Optimizing existing content
5. Planning content with the calendar

## Conclusion

This implementation plan provides a comprehensive approach to integrating Google login and Google Search Console with AI-Writer. By following these steps, you'll enhance the platform with real user insights for content creation, improving the relevance and effectiveness of generated content.

The integration will provide significant value to users by:

1. Leveraging real search data for content creation
2. Identifying content opportunities based on actual performance
3. Optimizing content for keywords that matter to the user's audience
4. Creating a data-driven content strategy
5. Measuring content performance over time

This feature will differentiate AI-Writer from competitors by providing a closed-loop system for content creation, optimization, and performance tracking.