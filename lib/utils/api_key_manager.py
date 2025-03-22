import os
import streamlit as st
from dotenv import load_dotenv
from functools import lru_cache
from .alwrity_ui_styling import get_base_styles, get_provider_selection_styles, get_api_form_styles

@st.cache_data
def get_api_keys_config():
    """Cache API keys configuration"""
    return {
        "METAPHOR_API_KEY": "https://dashboard.exa.ai/login",
        "TAVILY_API_KEY": "https://tavily.com/#api",
        "SERPER_API_KEY": "https://serper.dev/signup",
        "STABILITY_API_KEY": "https://platform.stability.ai/",
        "FIRECRAWL_API_KEY": "https://www.firecrawl.dev/account"
    }

@st.cache_data
def get_supported_providers():
    """Cache supported providers configuration"""
    return {
        'google': "GEMINI_API_KEY",
        'openai': "OPENAI_API_KEY",
        'mistral': "MISTRAL_API_KEY"
    }

@lru_cache(maxsize=32)
def check_env_var(key):
    """Cache environment variable checks"""
    return os.getenv(key) is not None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_missing_keys(api_keys):
    """Cache missing keys check results"""
    return {
        key: url for key, url in api_keys.items() 
        if not check_env_var(key)
    }

def display_provider_selection():
    """Display a styled provider selection section"""
    # Apply cached styles
    st.markdown(f"<style>{get_provider_selection_styles()}</style>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    .provider-card {
        background: linear-gradient(135deg, #f9f9f9, #e0e0e0);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #dcdcdc;
    }
    .provider-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
    }
    .provider-description {
        font-size: 1rem;
        color: #555;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='provider-card'>", unsafe_allow_html=True)
    st.markdown("<div class='provider-header'>🤖 Select Your AI Provider</div>", unsafe_allow_html=True)
    st.markdown("<div class='provider-description'>Choose your preferred AI provider to proceed with the configuration.</div>", unsafe_allow_html=True)
    provider = st.selectbox(
        "AI Provider",
        options=["google", "openai", "mistral"],
        help="Select the AI provider you have an API key for"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    return provider

def get_grouped_api_keys(missing_keys):
    """Organize API keys into functional groups"""
    groups = {
        "All": missing_keys,
        "Blog & Social": {k: v for k, v in missing_keys.items() 
                         if k in ["GEMINI_API_KEY", "OPENAI_API_KEY", "MISTRAL_API_KEY", "SERPER_API_KEY"]},
        "Deep Research": {k: v for k, v in missing_keys.items() 
                         if k in ["GEMINI_API_KEY", "OPENAI_API_KEY", "MISTRAL_API_KEY", 
                                "FIRECRAWL_API_KEY", "METAPHOR_API_KEY", "TAVILY_API_KEY"]}
    }
    return groups

def validate_tab_inputs(group_name, keys):
    """Validate if all required keys for a tab are provided"""
    missing = []
    for key in keys:
        value = st.session_state.get(key, "")
        if not value:
            missing.append(key)
    return missing

def display_api_key_form(missing_keys):
    """Display a styled form for API key input with grouped tabs"""
    st.markdown(f"<style>{get_api_form_styles()}</style>", unsafe_allow_html=True)

    # Define group information messages
    group_info = {
        "All": """
        ### 🔐 Complete API Configuration
        Configure all available API keys to unlock the full potential of ALwrity:
        - **AI Models**: For advanced text generation and analysis
        - **Search APIs**: For comprehensive web research
        - **Research Tools**: For deep content analysis
        
        > **Note**: You can start with minimal configuration and add more keys later.
        """,
        
        "Blog & Social": """
        ### ✍️ Content Creation Essentials
        Required keys for basic content creation:
        - **AI Model API** (Google/OpenAI/Mistral): Text generation
        - **SERP API**: Web search integration
        
        #### Features Available:
        - Blog post generation
        - Social media content
        - Basic web research
        
        > **Tip**: Start with these keys for basic content creation workflow.
        """,
        
        "Deep Research": """
        ### 🔍 Advanced Research Tools
        For in-depth content research and analysis:
        - **AI Model API**: Content analysis
        - **Firecrawl**: Advanced web scraping
        - **Metaphor**: Semantic search
        - **Tavily**: AI-powered research
        
        #### Enhanced Capabilities:
        - Comprehensive research
        - Fact verification
        - Citation support
        - Deep content analysis
        
        > **Pro Tip**: Configure all keys for maximum research capabilities.
        """
    }

    st.markdown("<div class='api-interface'>", unsafe_allow_html=True)
        
    # Initialize grouped keys using the helper function
    grouped_keys = get_grouped_api_keys(missing_keys)
    
    # Create tabs for different groups
    tabs = st.tabs(list(grouped_keys.keys()))
    
    # Add get key links to information messages
    api_key_links = {
        "METAPHOR_API_KEY": "https://dashboard.exa.ai/login",
        "TAVILY_API_KEY": "https://tavily.com/#api",
        "SERPER_API_KEY": "https://serper.dev/signup",
        "STABILITY_API_KEY": "https://platform.stability.ai/",
        "FIRECRAWL_API_KEY": "https://www.firecrawl.dev/account",
        "GEMINI_API_KEY": "https://makersuite.google.com/app/apikey",
        "OPENAI_API_KEY": "https://platform.openai.com/api-keys",
        "MISTRAL_API_KEY": "https://console.mistral.ai/api-keys/"
    }

    with st.form(key='api_keys_form', clear_on_submit=False):
        # Add validation state
        validation_state = {}
        active_tab = None
        
        for tab_idx, (group_name, keys) in enumerate(grouped_keys.items()):
            with tabs[tab_idx]:
                # Track active tab
                if tab_idx == st.session_state.get("active_tab_index", 0):
                    active_tab = group_name

                # Display group information
                st.markdown(group_info[group_name])
                st.divider()

                if not keys:
                    st.success("✅ All required keys for this group are configured!")
                    validation_state[group_name] = True
                    continue

                # Display keys in columns
                col1, col2 = st.columns(2)
                for idx, (key, _) in enumerate(keys.items()):
                    with col1 if idx % 2 == 0 else col2:
                        get_key_link = api_key_links.get(key, "#")
                        st.markdown(f"""
                            <div class='api-input-container'>
                                <div class='api-input-header'>
                                    <label class='api-input-label'>
                                        {key}<span class='api-required'>*</span>
                                    </label>
                                    <div class='api-actions'>
                                        <div class='api-tooltip' data-tooltip='Required for {group_name} features'>ℹ️</div>
                                        <a href='{get_key_link}' target='_blank' class='api-get-key' 
                                           title='Get your API key'>
                                            🔑 Get Key
                                        </a>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Create unique key for each input
                        input_key = f"{group_name}_{key}"
                        
                        # If value exists in session state for any tab, use it
                        if key in st.session_state:
                            value = st.session_state[key]
                        else:
                            value = st.session_state.get(input_key, "")
                        
                        input_value = st.text_input(
                            label=f"Enter {key}",
                            type="password",
                            key=input_key,
                            value=value,
                            help=f"Enter your {key} here",
                            placeholder="Enter API key here...",
                            label_visibility="collapsed"
                        )
                        
                        # Sync the value across tabs
                        if input_value:
                            st.session_state[key] = input_value

                # Validate current tab inputs
                missing_inputs = validate_tab_inputs(group_name, keys)
                validation_state[group_name] = len(missing_inputs) == 0

                if missing_inputs:
                    st.warning(f"""
                    ⚠️ Required API keys missing for {group_name}:
                    - {', '.join(missing_inputs)}
                    
                    Please provide all required keys before saving.
                    """)

        # Centered submit button with dynamic state
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            submit_disabled = not validation_state.get(active_tab, False)
            
            st.markdown("""
            <style>
            .save-button-enabled {
                background: linear-gradient(135deg, #3182CE, #4299E1) !important;
                color: white !important;
                border: none !important;
                padding: 14px 28px !important;
                font-weight: 600 !important;
                font-size: 16px !important;
                box-shadow: 0 4px 6px rgba(49, 130, 206, 0.2) !important;
                transition: all 0.3s ease !important;
            }
            .save-button-enabled:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 12px rgba(49, 130, 206, 0.25) !important;
                background: linear-gradient(135deg, #2B6CB0, #3182CE) !important;
            }
            .save-button-disabled {
                background: #E2E8F0 !important;
                color: #718096 !important;
                cursor: not-allowed !important;
            }
            .api-input-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }

            .api-actions {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .api-get-key {
                display: inline-flex;
                align-items: center;
                padding: 4px 8px;
                font-size: 12px;
                color: #3182CE;
                background: rgba(49, 130, 206, 0.1);
                border-radius: 4px;
                text-decoration: none;
                transition: all 0.2s ease;
            }

            .api-get-key:hover {
                background: rgba(49, 130, 206, 0.2);
                transform: translateY(-1px);
                text-decoration: none;
                color: #2B6CB0;
            }

            .api-tooltip {
                cursor: help;
                position: relative;
            }

            .api-tooltip::after {
                content: attr(data-tooltip) '\\A Click 🔑 Get Key to obtain your API key';
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                padding: 8px 12px;
                background: #2D3748;
                color: white;
                font-size: 12px;
                border-radius: 4px;
                white-space: pre;
                opacity: 0;
                visibility: hidden;
                transition: all 0.2s ease;
                width: max-content;
                max-width: 250px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                z-index: 1000;
            }

            .api-tooltip:hover::after {
                opacity: 1;
                visibility: visible;
                bottom: calc(100% + 5px);
            }
            </style>
            """, unsafe_allow_html=True)

            submit = st.form_submit_button(
                "💾 Save API Keys", 
                disabled=submit_disabled,
                use_container_width=True,
                type="primary" if not submit_disabled else "secondary",
                help="Please provide all required API keys for the current tab"
            )

    st.markdown("</div>", unsafe_allow_html=True)
    return submit, validation_state

def check_all_api_keys():
    """Enhanced API key management with improved UI/UX"""
    load_dotenv()
    
    # Apply cached base styles
    st.markdown(f"<style>{get_base_styles()}</style>", unsafe_allow_html=True)
    st.markdown(f'<style>{open("lib/workspace/alwrity_ui_styling.css").read()}</style>', unsafe_allow_html=True)

    # Use cached configurations
    api_keys = get_api_keys_config()
    supported_providers = get_supported_providers()
    missing_keys = get_missing_keys(api_keys)

    @st.cache_resource
    def get_gpt_provider():
        """Cache GPT provider selection"""
        return os.getenv("GPT_PROVIDER")

    gpt_provider = get_gpt_provider()
    if not gpt_provider:
        gpt_provider = display_provider_selection()
        try:
            with open(".env", "a") as env_file:
                env_file.write(f"GPT_PROVIDER={gpt_provider}\n")
            os.environ["GPT_PROVIDER"] = gpt_provider
            st.success(f"✅ Successfully set {gpt_provider.upper()} as your AI provider")
            # Clear cache to reflect new provider
            get_gpt_provider.clear()
        except IOError as e:
            st.error(f"❌ Configuration Error: {str(e)}")


    # Check for provider API key
    api_key_var = supported_providers[gpt_provider.lower()]
    if not check_env_var(api_key_var):
        missing_keys[api_key_var] = ''
        
        submit, validation_state = display_api_key_form(missing_keys)
        if submit:
            try:
                valid_keys = {}
                for key in missing_keys:
                    key_value = st.session_state.get(key, "").strip()
                    if key_value:
                        valid_keys[key] = key_value
                
                if not valid_keys:
                    st.error("❌ No API keys provided. Please enter at least one API key.")
                    return False

                with open(".env", "a") as env_file:
                    for key, value in valid_keys.items():
                        env_file.write(f"{key}={value}\n")
                
                st.success(f"""✨ Successfully saved {len(valid_keys)} API key(s):
                - {', '.join(valid_keys.keys())}""")
                st.info("🔄 Please restart the application to apply changes")
                st.balloons()
                
                # Clear caches to reflect new configuration
                get_missing_keys.clear()
                check_env_var.cache_clear()
                st.stop()
            except Exception as e:
                st.error(f"""❌ Error saving API keys: 
                Please make sure you have:
                1. Provided all required keys for the current tab
                2. Entered valid API key values
                3. Have write permissions for the .env file
                
                Technical details: {str(e)}
                """)
        return False

    return True
