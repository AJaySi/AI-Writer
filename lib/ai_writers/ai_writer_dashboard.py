import streamlit as st
from lib.utils.alwrity_utils import (essay_writer, ai_news_writer, ai_finance_ta_writer)

from lib.ai_writers.ai_story_writer.story_writer import story_input_section
from lib.ai_writers.ai_product_description_writer import write_ai_prod_desc
from lib.ai_writers.ai_copywriter.copywriter_dashboard import copywriter_dashboard
from lib.ai_writers.linkedin_writer import LinkedInAIWriter
from lib.ai_writers.blog_rewriter_updater.ai_blog_rewriter import write_blog_rewriter
#from lib.content_planning_calender.content_planning_agents_alwrity_crew import ai_agents_content_planner
from lib.ai_writers.ai_blog_writer.ai_blog_generator import ai_blog_writer_page
from loguru import logger

def list_ai_writers():
    """Return a list of available AI writers with their metadata (no UI rendering)."""
    return [
        {
            "name": "AI Blog Writer",
            "icon": "📝",
            "description": "Generate comprehensive blog posts from keywords, URLs, or uploaded content",
            "category": "Content Creation",
            "function": ai_blog_writer_page,
            "path": "ai_blog_writer"
        },
        {
            "name": "AI Blog Rewriter",
            "icon": "🔄",
            "description": "Rewrite and update existing blog content with improved quality and SEO optimization",
            "category": "Content Creation",
            "function": write_blog_rewriter,
            "path": "blog_rewriter"
        },
        {
            "name": "Story Writer",
            "icon": "📚",
            "description": "Create engaging stories and narratives with AI assistance",
            "category": "Creative Writing",
            "function": story_input_section,
            "path": "story_writer"
        },
        {
            "name": "Essay writer",
            "icon": "✍️",
            "description": "Generate well-structured essays on any topic",
            "category": "Academic",
            "function": essay_writer,
            "path": "essay_writer"
        },
        {
            "name": "Write News reports",
            "icon": "📰",
            "description": "Create professional news articles and reports",
            "category": "Journalism",
            "function": ai_news_writer,
            "path": "news_writer"
        },
        {
            "name": "Write Financial TA report",
            "icon": "📊",
            "description": "Generate technical analysis reports for financial markets",
            "category": "Finance",
            "function": ai_finance_ta_writer,
            "path": "financial_writer"
        },
        {
            "name": "AI Product Description Writer",
            "icon": "🛍️",
            "description": "Create compelling product descriptions that drive sales",
            "category": "E-commerce",
            "function": write_ai_prod_desc,
            "path": "product_writer"
        },
        {
            "name": "AI Copywriter",
            "icon": "✒️",
            "description": "Generate persuasive copy for marketing and advertising",
            "category": "Marketing",
            "function": copywriter_dashboard,
            "path": "copywriter"
        },
        {
            "name": "LinkedIn AI Writer",
            "icon": "💼",
            "description": "Create professional LinkedIn content that engages your network",
            "category": "Professional",
            "function": lambda: LinkedInAIWriter().run(),
            "path": "linkedin_writer"
        }
    ]

def get_ai_writers():
    """Render the AI Writers dashboard UI with a professional, clickable card layout."""
    logger.info("Initializing AI Writers Dashboard")
    writers = list_ai_writers()
    logger.info(f"Found {len(writers)} AI writers")

    # Add custom CSS for a professional dashboard with VIBRANT clickable cards
    st.markdown("""
        <style>
            /* Base UI improvements */
            body, .main .block-container {
                background: linear-gradient(135deg, #f0f4f8 0%, #e6eef7 100%) !important;
                min-height: 100vh;
                color: #2c3e50;
                font-family: 'Helvetica Neue', sans-serif;
            }
            
            /* Main layout improvements */
            .main .block-container {
                padding: 1.5rem 2rem 2rem 2rem !important;
                max-width: 1200px;
                margin: 0 auto;
            }

            /* Dashboard header */
            .dashboard-header {
                text-align: center;
                margin-bottom: 2.5rem;
                padding: 2rem 1.5rem;
                background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
                border: 1px solid rgba(0, 0, 0, 0.04);
            }
            .dashboard-header h1 {
                font-size: 2.6em;
                font-family: 'Helvetica Neue', sans-serif;
                font-weight: 700;
                color: #1976d2;
                margin-bottom: 0.5rem;
            }
            .dashboard-header p {
                font-size: 1.15em;
                color: #546e7a;
                max-width: 700px;
                margin: 0 auto;
                line-height: 1.6;
            }

            /* Styling st.button to look like a clickable card - PREMIUM VIBRANT */
            [data-testid="stVerticalBlock"] [data-testid="stButton"] > button {
                /* Vivid Gradient Background - More saturated blue-purple */
                background: linear-gradient(135deg, #8a2be2 0%, #4169e1 100%); 
                color: #ffffff;
                border: none;
                padding: 1.8rem 1.5rem;
                border-radius: 18px;
                font-weight: 500;
                font-size: 1rem;
                font-family: 'Helvetica Neue', sans-serif;
                transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1); /* Smoother, more premium transition */
                box-shadow: 0 8px 20px rgba(77, 5, 232, 0.25), 0 2px 6px rgba(0, 0, 0, 0.15); /* Layered shadow for depth */
                width: 100%;
                height: 100%; 
                min-height: 190px;
                margin-bottom: 0;
                text-align: left;
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                justify-content: flex-start;
                line-height: 1.5;
                overflow: hidden;
                transform: translateY(0); /* Starting position for hover animation */
                position: relative; /* For pseudo-element effects */
            }
            
            /* Subtle shine effect on cards */
            [data-testid="stVerticalBlock"] [data-testid="stButton"] > button::after {
                content: '';
                position: absolute;
                top: 0;
                left: -50%;
                width: 150%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                transform: skewX(-20deg);
                transition: 0.5s;
                opacity: 0;
            }
            
            /* Dynamic hover effects with gradient shift */
            [data-testid="stVerticalBlock"] [data-testid="stButton"] > button:hover {
                background: linear-gradient(135deg, #4169e1 0%, #8a2be2 100%); /* Reverse gradient on hover */
                transform: translateY(-8px) scale(1.05); /* More dramatic lift */
                box-shadow: 0 15px 30px rgba(77, 5, 232, 0.4), 0 5px 15px rgba(0, 0, 0, 0.2); /* Deeper shadow */
                color: #ffffff;
            }
            
            /* Animate shine on hover */
            [data-testid="stVerticalBlock"] [data-testid="stButton"] > button:hover::after {
                left: 100%;
                opacity: 1;
            }
            
            [data-testid="stVerticalBlock"] [data-testid="stButton"] > button:hover > div > p strong {
                color: #ffffff; /* Bright white on hover */
                text-shadow: 0 0 15px rgba(255,255,255,0.5); /* Glow effect on hover */
            }

            /* Target the paragraph generated by Streamlit inside the button */
            [data-testid="stVerticalBlock"] [data-testid="stButton"] > button > div > p {
                margin: 0;
                line-height: 1.5;
                color: rgba(255, 255, 255, 0.9); /* Slightly dimmed base text */
            }

            /* Icon (first line/element) - MORE PROMINENT */
            [data-testid="stVerticalBlock"] [data-testid="stButton"] > button > div > p::first-line {
                font-size: 2.3em; /* Larger icon */
                line-height: 1.2;
                display: block;
                margin-bottom: 1rem;
                color: #ffffff;
                text-shadow: 0 0 10px rgba(255,255,255,0.4); /* Light glow effect */
            }

            /* Title (strong tag from markdown) - ENHANCED CONTRAST */
            [data-testid="stVerticalBlock"] [data-testid="stButton"] > button > div > p strong {
                font-size: 1.4em; /* Larger title */
                font-weight: 700; /* Bolder */
                color: #ffffff;
                display: block;
                margin: 0.7rem 0;
                text-shadow: 1px 1px 4px rgba(0,0,0,0.3); /* Stronger shadow for better contrast */
                letter-spacing: 0.5px; /* Slight letter spacing for premium feel */
            }

             /* Description - IMPROVED CONTRAST */
             [data-testid="stVerticalBlock"] [data-testid="stButton"] > button > div > p {
                font-size: 1rem; /* Slightly larger for readability */
                color: rgba(255, 255, 255, 0.95); /* Better contrast */
                text-shadow: 0 1px 2px rgba(0,0,0,0.1); /* Subtle shadow for text */
             }

            /* Column adjustments for consistent card height */
            [data-testid="column"] {
                 display: flex;
                 flex-direction: column;
                 gap: 1.5rem; /* Consistent gap */
            }

            /* Hide Streamlit default title */
            .stApp > header {
                visibility: hidden;
            }
        </style>
    """, unsafe_allow_html=True)

    # Dashboard header
    st.markdown("""
        <div class="dashboard-header">
            <h1>🚀 AI Content Creation Suite</h1>
            <p>Welcome! Select the perfect AI writer tool from the options below to start creating amazing content.</p>
        </div>
    """, unsafe_allow_html=True)

    # Create columns for the grid layout
    cols = st.columns(3)
    
    # Render buttons styled as cards for each writer
    for idx, writer in enumerate(writers):
        with cols[idx % 3]:
            # Prepare the button label using simple Markdown with newlines
            button_label = f"{writer['icon']}\n**{writer['name']}**\n{writer['description']}" 
            
            if st.button(
                button_label, 
                key=f"writer_{writer['path']}",
                help=f"Click to use the {writer['name']}", # More specific help text
                use_container_width=True,
            ):
                logger.info(f"Selected writer: {writer['name']} with path: {writer['path']}")
                st.session_state.selected_writer = writer
                st.query_params["writer"] = writer['path']
                logger.info(f"Updated query params with writer: {writer['path']}")
                st.rerun()

    logger.info("Finished rendering AI Writers Dashboard")
    # Return writers list, though it's not strictly needed if only rendering UI
    return writers

# Remove the old ai_writers function since it's now integrated into get_ai_writers