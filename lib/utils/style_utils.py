"""CSS styles and utilities for ALwrity pages."""

def get_base_styles() -> str:
    """
    Get the base CSS styles for ALwrity.
    
    Returns:
        str: CSS styles as a string
    """
    return """
    <style>
    /* Hide main menu */
    #MainMenu {
        visibility: hidden !important;
    }
    
    /* Hide footer */
    footer {
        visibility: hidden !important;
    }
    
    /* Hide deploy button */
    .stDeployButton {
        display: none !important;
    }
    
    /* Hide sidebar in both states */
    [data-testid="stSidebar"][aria-expanded="true"],
    [data-testid="stSidebar"][aria-expanded="false"] {
        visibility: hidden !important;
        width: 0px !important;
        position: fixed !important;
    }
    
    /* Hide hamburger menu */
    .st-emotion-cache-1rs6os {
        visibility: hidden !important;
    }
    
    /* Ensure main content takes full width */
    .main .block-container {
        max-width: 100% !important;
        padding-top: 1rem !important;
    }
    </style>
    """

def get_glassmorphic_styles() -> str:
    """
    Get the glassmorphic CSS styles for ALwrity.
    
    Returns:
        str: CSS styles as a string
    """
    return """
    <style>
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .glass-container:hover {
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.47);
    }

    .info-section {
        background: linear-gradient(135deg, rgba(31,119,180,0.1), rgba(31,119,180,0.05));
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }

    .info-section h4 {
        color: #1f77b4;
        margin-bottom: 8px;
    }

    .info-section p {
        margin: 4px 0;
        line-height: 1.5;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #00ff00;
    }

    .metric-label {
        font-size: 14px;
        color: #888;
    }

    .progress-bar {
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff00, #00ccff);
        transition: width 0.3s ease;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        padding: 10px 20px;
        margin: 0 2px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    .stExpander {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        margin: 10px 0;
    }

    .stExpander:hover {
        border-color: rgba(255, 255, 255, 0.2);
    }

    .stExpander .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px 8px 0 0;
        padding: 10px 15px;
    }

    .stExpander .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 0 0 8px 8px;
        padding: 15px;
    }

    .example-box {
        background: rgba(31,119,180,0.05);
        border-left: 3px solid #1f77b4;
        padding: 12px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 4px rgba(31,119,180,0.1);
    }

    .example-box p {
        margin: 4px 0;
        font-style: italic;
    }

    .example-box code {
        color: #00ff00;
        font-family: monospace;
    }

    .analysis-section {
        background: rgba(31,119,180,0.05);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }

    .analysis-section h3 {
        color: #1f77b4;
        margin-bottom: 12px;
    }

    .analysis-section ul {
        margin: 8px 0;
        padding-left: 20px;
    }

    .analysis-section li {
        margin: 4px 0;
    }

    .insight-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }

    .insight-card h4 {
        color: #00ff00;
        margin-bottom: 10px;
    }

    .insight-card ul {
        margin: 0;
        padding-left: 20px;
    }

    .insight-card li {
        margin: 5px 0;
    }

    .recommendation-box {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid rgba(0, 255, 0, 0.2);
        border-radius: 6px;
        padding: 10px;
        margin: 5px 0;
    }

    .recommendation-box h5 {
        color: #00ff00;
        margin-bottom: 5px;
    }

    .recommendation-box p {
        margin: 0;
        font-size: 14px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #00ff00, #00ccff);
        border: none;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #00ccff, #00ff00);
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stProgress .st-bo {
        background-color: rgba(255, 255, 255, 0.1);
    }

    .stProgress .st-bo > div {
        background: linear-gradient(90deg, #00ff00, #00ccff);
    }
    </style>
    """

def get_test_config_styles():
    """Returns CSS styles for the test configuration page."""
    return """
        <style>
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .stTextInput > div > div > input {
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                padding: 0.5rem 1rem;
            }
            
            .stSelectbox > div > div > select {
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                padding: 0.5rem 1rem;
            }
            
            .stTextArea > div > div > textarea {
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                padding: 0.5rem 1rem;
            }
            
            .stMarkdown {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            h1, h2, h3 {
                color: #2c3e50;
                font-weight: 600;
            }
            
            .stSuccess {
                background: linear-gradient(135deg, #43c6ac 0%, #191654 100%);
                padding: 1rem;
                border-radius: 8px;
                color: white;
            }
            
            .stError {
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
                padding: 1rem;
                border-radius: 8px;
                color: white;
            }
            
            .stWarning {
                background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%);
                padding: 1rem;
                border-radius: 8px;
                color: #2c3e50;
            }
        </style>
    """

def get_glass_container(content: str) -> str:
    """Returns HTML for a glass-morphism container."""
    return f"""
        <div style='
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        '>
            {content}
        </div>
    """

def get_info_section(content: str) -> str:
    """Returns HTML for an info section."""
    return f"""
        <div style='
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        '>
            {content}
        </div>
    """

def get_example_box(content: str) -> str:
    """Returns HTML for an example box."""
    return f"""
        <div style='
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        '>
            {content}
        </div>
    """

def get_analysis_section(title: str, content: str) -> str:
    """Returns HTML for an analysis section."""
    return f"""
        <div style='
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        '>
            <h3>{title}</h3>
            {content}
        </div>
    """

def get_style_guide_html() -> str:
    """Returns HTML for the style guide section."""
    return """
        <div style='
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        '>
            <h3>Style Guide</h3>
            <p>This section will contain your style guide and brand guidelines.</p>
        </div>
    """

def get_test_config_styles() -> str:
    """
    Get all CSS styles for test configuration settings page.
    
    Returns:
        str: Combined CSS styles as a string
    """
    return f"{get_base_styles()}{get_glassmorphic_styles()}" 