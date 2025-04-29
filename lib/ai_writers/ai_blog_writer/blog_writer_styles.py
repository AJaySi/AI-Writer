import streamlit as st

def apply_blog_writer_styles():
    st.markdown("""
    <style>
        /* Base UI improvements */
        body, .main .block-container {
            background: linear-gradient(135deg, #f0f4f8 0%, #d7e1ec 100%) !important;
            min-height: 100vh;
            color: #2c3e50;
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        /* Main layout improvements */
        .main .block-container {
            padding: 1rem 2rem 2rem 2rem !important;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Back button styling */
        [data-testid="stButton"] > button:first-of-type {
            background: #1976d2;
            color: white;
            border: none;
            border-radius: 30px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            box-shadow: 0 2px 10px rgba(25, 118, 210, 0.2);
            margin-bottom: 1.5rem;
        }
        
        [data-testid="stButton"] > button:first-of-type:hover {
            background: #1565c0;
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
        }
        
        /* Header styling */
        .blog-header, .page-header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem 1.5rem;
            background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .blog-header h1, .page-header h1 {
            font-size: 2.5em;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            color: #1976d2;
            margin-bottom: 0.5rem;
        }
        
        .blog-header p, .page-header p {
            font-size: 1.1em;
            color: #546e7a;
            max-width: 700px;
            margin: 0 auto;
            line-height: 1.6;
        }
        
        /* Input section styling */
        .stTextArea textarea, .stTextInput input {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: #2c3e50;
            font-size: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }
        
        .stTextArea textarea:focus, .stTextInput input:focus {
            border: 1.5px solid #1976d2;
            box-shadow: 0 2px 10px rgba(25, 118, 210, 0.12);
        }
        
        /* File uploader styling */
        .stFileUploader > div {
            background: #ffffff;
            border: 2px dashed #cfd8dc;
            border-radius: 10px;
            padding: 1.5rem 1rem;
            text-align: center;
            transition: all 0.2s ease;
        }
        
        .stFileUploader > div:hover {
            border-color: #1976d2;
            background: rgba(25, 118, 210, 0.03);
        }
        
        /* Options expander styling */
        .stExpander {
            border-radius: 10px;
            overflow: hidden;
            margin: 1.5rem 0;
            border: 1px solid #e0e0e0;
        }
        
        .stExpander > details {
            background: #ffffff;
            padding: 0.5rem;
        }
        
        .stExpander > details > summary {
            padding: 0.75rem 1rem;
            font-weight: 600;
            color: #1976d2;
        }
        
        .stExpander > details > summary:hover {
            color: #1565c0;
        }
        
        /* Checkbox styling */
        .stCheckbox > div {
            background: #ffffff;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            border: 1px solid #f0f0f0;
        }
        
        .stCheckbox > div:hover {
            background: rgba(25, 118, 210, 0.03);
        }
        
        .stCheckbox label {
            font-weight: 500;
            color: #455a64;
        }
        
        /* Radio button styling */
        .stRadio > div {
            background: #ffffff;
            border-radius: 10px;
            padding: 0.5rem;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            border: 1px solid #f0f0f0;
        }
        
        .stRadio > div > div {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .stRadio > div > div > label {
            background: #f5f7fa;
            padding: 0.6rem 1.2rem;
            border-radius: 30px;
            transition: all 0.2s ease;
            text-align: center;
            font-weight: 500;
            color: #546e7a;
            border: 1px solid #e0e0e0;
        }
        
        .stRadio > div > div > label:hover {
            background: #e3f2fd;
            color: #1976d2;
            border-color: #bbdefb;
        }
        
        .stRadio > div > div > label[data-baseweb="radio"] input:checked + div {
            background: #1976d2;
            color: white;
            border-color: #1976d2;
        }
        
        /* Generate button styling */
        button[data-testid="baseButton-secondary"], 
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(45deg, #1976d2, #2196f3);
            color: white;
            border: none;
            border-radius: 30px;
            padding: 0.85rem 1.5rem;
            font-weight: 600;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.25);
            text-transform: uppercase;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        button[data-testid="baseButton-secondary"]:hover, 
        button[data-testid="baseButton-primary"]:hover {
            background: linear-gradient(45deg, #1565c0, #1976d2);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(25, 118, 210, 0.35);
        }
        
        /* Input labels */
        .stTextArea label, .stTextInput label, .stFileUploader label {
            font-weight: 600;
            color: #455a64;
            font-size: 1.05rem;
            margin-bottom: 0.5rem;
        }
        
        /* Section headers */
        .stMarkdown h3 {
            color: #1976d2;
            font-weight: 600;
            font-size: 1.3rem;
            margin: 1.5rem 0 0.75rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(25, 118, 210, 0.1);
        }
        
        .stMarkdown h4 {
            color: #455a64;
            font-weight: 600;
            font-size: 1.1rem;
            margin: 1rem 0 0.5rem 0;
        }
        
        /* Column layout improvements */
        [data-testid="column"] {
            background: #ffffff;
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.04);
            border: 1px solid rgba(0, 0, 0, 0.05);
            margin: 0 0.5rem;
        }
        
        /* Success and error messages */
        .stSuccess, .stInfo, .stError {
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True) 