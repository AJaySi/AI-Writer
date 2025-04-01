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

def get_glass_container(content: str) -> str:
    """Wrap content in a glass container."""
    return f"""
        <div class="glass-container">
            {content}
        </div>
    """

def get_info_section(content: str) -> str:
    """Wrap content in an info section."""
    return f"""
        <div class="info-section">
            {content}
        </div>
    """

def get_example_box(content: str) -> str:
    """Wrap content in an example box."""
    return f"""
        <div class="example-box">
            {content}
        </div>
    """

def get_analysis_section(title: str, content: str) -> str:
    """Create an analysis section with title and content."""
    return f"""
        <div class="analysis-section">
            <h3>{title}</h3>
            {content}
        </div>
    """

def get_style_guide_html() -> str:
    """
    Get the style guide HTML content.
    
    Returns:
        str: HTML content for the style guide section
    """
    return """
        ### How ALwrity Discovers Your Style
        
        **AI-Powered Style Analysis**
        
        ALwrity AI analyzes your existing content to understand your unique writing style and preferences. This helps us generate content that matches your voice perfectly.
        
        **Step 1: Content Analysis**
        
        We'll analyze your website content or written samples to understand:
        
        - Writing tone and voice
        - Vocabulary and language style
        - Content structure and formatting
        - Target audience and engagement style
        
        **Step 2: Style Recommendations**
        
        Based on the analysis, we'll provide:
        
        - Personalized writing guidelines
        - Content structure templates
        - Tone and voice recommendations
        - Audience engagement strategies
        
        **Step 3: Content Generation**
        
        Finally, we'll use these insights to:
        
        - Generate content that matches your style
        - Maintain consistency across all content
        - Optimize for your target audience
        - Ensure brand voice alignment
    """

def get_test_config_styles() -> str:
    """
    Get all CSS styles for test configuration settings page.
    
    Returns:
        str: Combined CSS styles as a string
    """
    return f"{get_base_styles()}{get_glassmorphic_styles()}" 