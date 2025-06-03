import streamlit as st

def apply_navigation_styles():
    """Apply navigation and UI setup specific styling."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            /* Main app styling for navigation */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Compact layout styling with zero top padding when sub-tab selected */
            .main .block-container {
                padding-top: 0 !important;  /* Remove all top padding */
                padding-bottom: 0;
                max-width: 100%;
            }
            
            /* Remove extra padding and margins */
            .stMarkdown {
                margin: 0;
                padding: 0;
            }
            
            /* Header styling with zero margins when in sub-tab */
            .sub-tab-active h1, .sub-tab-active h2, .sub-tab-active h3 {
                display: none;  /* Hide headers in sub-tab mode */
            }
            
            /* Remove extra padding in containers */
            .stMarkdown {
                margin-bottom: 0;
            }
            
            /* Header styling */
            h1, h2, h3 {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-weight: 600;
                margin-top: 0;
                margin-bottom: 0.5rem;  /* Reduced from 1rem */
                padding-top: 0;
            }
            
            /* Reduce spacing between elements */
            .element-container {
                margin-bottom: 0.5rem;  /* Reduced from 1rem */
            }
            
            /* Button styling */
            .stButton > button {
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
                margin-bottom: 0.25rem;  /* Reduced from 0.5rem */
                font-family: 'Inter', sans-serif;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            /* Input field styling */
            .stTextInput > div > div > input {
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                padding: 0.5rem 1rem;
                font-family: 'Inter', sans-serif;
            }
            
            /* Checkbox styling */
            .stCheckbox > label {
                font-weight: 500;
                font-family: 'Inter', sans-serif;
            }
            
            /* Expander styling */
            .streamlit-expanderHeader {
                font-weight: 500;
                color: #2c3e50;
                margin-bottom: 0.5rem;
                font-family: 'Inter', sans-serif;
            }
            
            /* Success message styling */
            .stSuccess {
                background: linear-gradient(135deg, #43c6ac 0%, #191654 100%);
                padding: 0.75rem;
                border-radius: 8px;
                color: white;
                margin-bottom: 1rem;
                font-family: 'Inter', sans-serif;
            }
            
            /* Error message styling */
            .stError {
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
                padding: 0.75rem;
                border-radius: 8px;
                color: white;
                margin-bottom: 1rem;
                font-family: 'Inter', sans-serif;
            }
            
            /* Info message styling */
            .stInfo {
                padding: 0.75rem;
                margin-bottom: 1rem;
                font-family: 'Inter', sans-serif;
            }

            /* Sidebar navigation styling */
            .sidebar-nav {
                padding: 0.5rem 0;
            }
            
            .nav-button {
                width: 100%;
                text-align: left;
                padding: 0.5rem 1rem;
                background: transparent;
                border: none;
                color: #2c3e50;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 0.2rem 0;
                border-radius: 4px;
                font-family: 'Inter', sans-serif;
            }
            
            .nav-button:hover {
                background: rgba(0,0,0,0.05);
                padding-left: 0.5rem;
            }
            
            .nav-button.active {
                background: #1565C0;
                color: white;
            }
            
            /* Enhanced Sub-menu styling with minimal spacing */
            .sub-menu {
                padding-left: 1rem;
                margin: 0;
                border-left: 2px solid rgba(21, 101, 192, 0.3);
                background: rgba(255, 255, 255, 0.05);
                border-radius: 0 8px 8px 0;
                padding-top: 0;
                padding-bottom: 0;
            }
            
            /* Sub-menu button styling with minimal gaps */
            .sub-menu .stButton > button {
                font-size: 0.9rem;
                text-align: left;
                padding: 0.4rem 0.8rem;
                background: transparent;
                border: none;
                color: #2c3e50;
                font-weight: 500;
                transition: all 0.2s ease;
                margin: 0;
                border-radius: 4px;
                min-height: 0;
                height: auto;
                line-height: 1.2;
                width: 100%;
                font-family: 'Inter', sans-serif;
            }
            
            /* Platform-specific button styles */
            .facebook-button .stButton > button {
                color: #4267B2;
                background: rgba(66, 103, 178, 0.1);
            }
            
            .linkedin-button .stButton > button {
                color: #0077B5;
                background: rgba(0, 119, 181, 0.1);
            }
            
            .twitter-button .stButton > button {
                color: #1DA1F2;
                background: rgba(29, 161, 242, 0.1);
            }
            
            .instagram-button .stButton > button {
                color: #E1306C;
                background: rgba(225, 48, 108, 0.1);
            }
            
            .youtube-button .stButton > button {
                color: #FF0000;
                background: rgba(255, 0, 0, 0.1);
            }
            
            /* Platform-specific hover states */
            .facebook-button .stButton > button:hover {
                background: rgba(66, 103, 178, 0.2) !important;
                color: #4267B2 !important;
            }
            
            .linkedin-button .stButton > button:hover {
                background: rgba(0, 119, 181, 0.2) !important;
                color: #0077B5 !important;
            }
            
            .twitter-button .stButton > button:hover {
                background: rgba(29, 161, 242, 0.2) !important;
                color: #1DA1F2 !important;
            }
            
            .instagram-button .stButton > button:hover {
                background: rgba(225, 48, 108, 0.2) !important;
                color: #E1306C !important;
            }
            
            .youtube-button .stButton > button:hover {
                background: rgba(255, 0, 0, 0.2) !important;
                color: #FF0000 !important;
            }
            
            /* Platform-specific active states */
            .facebook-button.active .stButton > button {
                background: #4267B2 !important;
                color: white !important;
            }
            
            .linkedin-button.active .stButton > button {
                background: #0077B5 !important;
                color: white !important;
            }
            
            .twitter-button.active .stButton > button {
                background: #1DA1F2 !important;
                color: white !important;
            }
            
            .instagram-button.active .stButton > button {
                background: #E1306C !important;
                color: white !important;
            }
            
            .youtube-button.active .stButton > button {
                background: #FF0000 !important;
                color: white !important;
            }

            /* Remove any extra spacing from button containers */
            .sub-menu .stButton {
                margin: 0;
                padding: 0;
            }
            
            .sub-menu > div {
                margin: 0;
                padding: 0;
            }
            
            .sub-menu .element-container {
                margin: 0;
                padding: 0;
            }
            
            /* Ensure minimal gaps between elements */
            .sub-menu > div:not(:last-child) {
                margin-bottom: 1px;
            }

            /* Sidebar icon styling */
            .sidebar-icon {
                padding: 1rem;
                text-align: center;
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
            }
            
            .sidebar-icon img {
                width: 80px !important;
                height: auto !important;
                margin: 0 auto;
            }
            
            /* Additional compact layout overrides for specific pages */
            .compact-layout .main .block-container {
                padding-top: 0.25rem !important;
                padding-bottom: 0;
            }
            
            /* Hide Streamlit elements for cleaner navigation */
            .stApp > header {
                visibility: hidden;
            }
            
            /* Custom scrollbar for navigation */
            .sidebar .stMarkdown::-webkit-scrollbar {
                width: 6px;
            }
            
            .sidebar .stMarkdown::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 3px;
            }
            
            .sidebar .stMarkdown::-webkit-scrollbar-thumb {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 3px;
            }
            
            .sidebar .stMarkdown::-webkit-scrollbar-thumb:hover {
                background: rgba(0, 0, 0, 0.5);
            }
        </style>
    """, unsafe_allow_html=True)

def apply_compact_layout():
    """Apply compact layout styling for specific pages."""
    st.markdown("""
        <style>
            .main .block-container {
                padding-top: 0.25rem !important;
                padding-bottom: 0;
            }
        </style>
    """, unsafe_allow_html=True) 