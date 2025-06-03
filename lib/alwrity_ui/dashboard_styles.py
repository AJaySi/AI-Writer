import streamlit as st

def apply_dashboard_style():
    """Apply common glassmorphic styling for all dashboards (AI Writers, SEO Tools, Social Media)."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Global styling with glassmorphic background */
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            .main .block-container {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 2rem 2.5rem 3rem 2.5rem !important;
                max-width: 1400px;
                margin: 2rem auto;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
            }

            /* Modern dashboard header with glassmorphic effect */
            .dashboard-header {
                text-align: center;
                margin-bottom: 3rem;
                padding: 3rem 2rem;
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                position: relative;
                overflow: hidden;
            }
            
            .dashboard-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
                animation: shimmer 3s ease-in-out infinite;
            }
            
            @keyframes shimmer {
                0%, 100% { opacity: 0; }
                50% { opacity: 1; }
            }
            
            .dashboard-header h1 {
                font-size: 3.2em;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 1rem;
                text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                letter-spacing: -0.02em;
                line-height: 1.1;
            }
            
            .dashboard-header p {
                font-size: 1.2em;
                color: rgba(255, 255, 255, 0.85);
                max-width: 600px;
                margin: 0 auto;
                line-height: 1.6;
                font-weight: 400;
            }

            /* Category headers with modern styling */
            .stMarkdown h2 {
                color: #ffffff;
                font-size: 1.8em;
                font-weight: 600;
                margin: 2.5rem 0 1.5rem 0;
                padding-left: 1rem;
                border-left: 4px solid rgba(255, 255, 255, 0.6);
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
                letter-spacing: -0.01em;
            }

            /* Custom category headers */
            .category-header {
                margin: 3rem 0 2rem 0;
                position: relative;
            }
            
            .category-header h2 {
                color: #ffffff;
                font-size: 1.8em;
                font-weight: 600;
                margin: 0 0 0.5rem 0;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                letter-spacing: -0.01em;
            }
            
            .category-line {
                height: 2px;
                background: linear-gradient(90deg, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0.2) 50%, transparent 100%);
                border-radius: 1px;
                margin-bottom: 1.5rem;
            }

            /* Cards container with grid layout */
            .cards-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            /* Card container */
            .card-container {
                position: relative;
                margin-bottom: 1.5rem;
            }

            /* Premium cards (works for both writer and tool cards) */
            .premium-card {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 20px;
                padding: 0;
                cursor: pointer;
                transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
                position: relative;
                overflow: hidden;
                min-height: 200px;
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
                transform: translateY(0) scale(1);
                margin-bottom: 1rem;
            }

            /* Style all Streamlit buttons to match the glassmorphic design */
            .card-container + div[data-testid="stButton"] > button,
            .stButton > button {
                background: rgba(255, 255, 255, 0.08) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                border-radius: 20px !important;
                color: #ffffff !important;
                font-family: 'Inter', sans-serif !important;
                font-weight: 500 !important;
                font-size: 1rem !important;
                padding: 1rem 1.5rem !important;
                min-height: 60px !important;
                margin: 0 !important;
                box-shadow: 
                    0 8px 25px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
                transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
                position: relative !important;
                overflow: hidden !important;
                width: 100% !important;
            }

            /* Button hover effects */
            .card-container + div[data-testid="stButton"] > button:hover,
            .stButton > button:hover {
                background: rgba(255, 255, 255, 0.12) !important;
                backdrop-filter: blur(25px) !important;
                transform: translateY(-4px) scale(1.02) !important;
                box-shadow: 
                    0 15px 35px rgba(0, 0, 0, 0.25),
                    0 0 0 1px rgba(255, 255, 255, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
                border-color: rgba(255, 255, 255, 0.3) !important;
                color: #ffffff !important;
            }

            /* Button focus state */
            .card-container + div[data-testid="stButton"] > button:focus,
            .stButton > button:focus {
                outline: 2px solid rgba(255, 255, 255, 0.5) !important;
                outline-offset: 2px !important;
                background: rgba(255, 255, 255, 0.12) !important;
            }

            /* Button active state */
            .card-container + div[data-testid="stButton"] > button:active,
            .stButton > button:active {
                transform: translateY(-2px) scale(1.01) !important;
                transition: all 0.1s ease !important;
            }

            /* Add shine effect to buttons */
            .card-container + div[data-testid="stButton"] > button::before,
            .stButton > button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                transform: skewX(-20deg);
                transition: left 0.6s ease;
                pointer-events: none;
            }

            .card-container + div[data-testid="stButton"] > button:hover::before,
            .stButton > button:hover::before {
                left: 100%;
            }

            /* Card hover effects when hovering over the container */
            .card-container:hover .premium-card {
                background: rgba(255, 255, 255, 0.12);
                backdrop-filter: blur(25px);
                transform: translateY(-4px) scale(1.02);
                box-shadow: 
                    0 15px 35px rgba(0, 0, 0, 0.25),
                    0 0 0 1px rgba(255, 255, 255, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.3);
            }

            .card-container:hover .card-glow {
                opacity: 1;
            }

            .card-container:hover .card-arrow {
                transform: translateX(5px);
                color: #ffffff;
            }

            .card-container:hover .card-shine {
                left: 100%;
            }

            .card-container:hover .card-icon {
                filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.5));
                transform: scale(1.05);
            }

            .card-container:hover .card-category {
                background: rgba(255, 255, 255, 0.2);
                color: #ffffff;
            }

            /* Active/pressed state */
            .card-container:active .premium-card {
                transform: translateY(-2px) scale(1.01);
                transition: all 0.1s ease;
            }

            /* Card glow effect */
            .card-glow {
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
                border-radius: 22px;
                opacity: 0;
                transition: opacity 0.3s ease;
                z-index: -1;
            }

            /* Card content wrapper */
            .card-content {
                padding: 2rem 1.8rem;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                position: relative;
                z-index: 2;
            }

            /* Card icon */
            .card-icon {
                font-size: 2.8em;
                margin-bottom: 1rem;
                color: #ffffff;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
                line-height: 1;
                transition: all 0.3s ease;
            }

            /* Card title */
            .card-title {
                font-size: 1.3em;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 0.8rem;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                letter-spacing: -0.01em;
                line-height: 1.3;
            }

            /* Card description */
            .card-description {
                font-size: 0.95em;
                color: rgba(255, 255, 255, 0.85);
                line-height: 1.5;
                margin-bottom: 1.5rem;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
                flex-grow: 1;
            }

            /* Card footer */
            .card-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: auto;
            }

            /* Card category badge */
            .card-category {
                background: rgba(255, 255, 255, 0.15);
                color: rgba(255, 255, 255, 0.9);
                padding: 0.3rem 0.8rem;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: 500;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
            }

            /* Card arrow */
            .card-arrow {
                font-size: 1.2em;
                color: rgba(255, 255, 255, 0.7);
                transition: all 0.3s ease;
                transform: translateX(0);
            }

            /* Card shine effect */
            .card-shine {
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                transform: skewX(-20deg);
                transition: left 0.6s ease;
                pointer-events: none;
            }

            /* Category spacer */
            .category-spacer {
                height: 2rem;
            }

            /* Responsive adjustments for cards */
            @media (max-width: 768px) {
                .cards-container {
                    grid-template-columns: 1fr;
                    gap: 1rem;
                }
                
                .card-content {
                    padding: 1.5rem;
                }
                
                .premium-card {
                    min-height: 180px;
                }
                
                .category-header {
                    margin: 2rem 0 1.5rem 0;
                }
                
                .main .block-container {
                    padding: 1.5rem !important;
                    margin: 1rem;
                }
                
                .dashboard-header {
                    padding: 2rem 1.5rem;
                    margin-bottom: 2rem;
                }
                
                .dashboard-header h1 {
                    font-size: 2.4em;
                }
                
                .dashboard-header p {
                    font-size: 1.1em;
                }
            }

            /* Card entrance animations */
            .premium-card {
                animation: cardSlideIn 0.6s ease-out forwards;
                opacity: 0;
            }

            @keyframes cardSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(30px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            /* Stagger animation delays */
            .premium-card:nth-child(1) { animation-delay: 0.1s; }
            .premium-card:nth-child(2) { animation-delay: 0.2s; }
            .premium-card:nth-child(3) { animation-delay: 0.3s; }
            .premium-card:nth-child(4) { animation-delay: 0.4s; }
            .premium-card:nth-child(5) { animation-delay: 0.5s; }
            .premium-card:nth-child(6) { animation-delay: 0.6s; }

            /* Hide Streamlit elements */
            .stApp > header {
                visibility: hidden;
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(255, 255, 255, 0.5);
            }

            /* Page entrance animation */
            .main .block-container {
                animation: fadeInUp 0.8s ease-out;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        </style>
    """, unsafe_allow_html=True)

def render_dashboard_header(title, description):
    """Render a standardized dashboard header."""
    st.markdown(f"""
        <div class="dashboard-header">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)

def render_category_header(category_name):
    """Render a standardized category header."""
    st.markdown(f"""
        <div class="category-header">
            <h2>{category_name}</h2>
            <div class="category-line"></div>
        </div>
    """, unsafe_allow_html=True)

def render_card(icon, title, description, category, key_suffix="", help_text=""):
    """Render a standardized premium card with button."""
    st.markdown(f"""
        <div class="card-container">
            <div class="premium-card">
                <div class="card-glow"></div>
                <div class="card-content">
                    <div class="card-icon">{icon}</div>
                    <div class="card-title">{title}</div>
                    <div class="card-description">{description}</div>
                    <div class="card-footer">
                        <span class="card-category">{category}</span>
                        <div class="card-arrow">→</div>
                    </div>
                </div>
                <div class="card-shine"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Return button for functionality
    return st.button(
        f"Select {title}", 
        key=f"card_{key_suffix}",
        help=help_text or f"Launch {title} - {description}",
        use_container_width=True
    ) 