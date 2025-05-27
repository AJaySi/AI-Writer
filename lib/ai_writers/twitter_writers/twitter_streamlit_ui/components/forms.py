"""
Form components for Twitter UI.
Provides consistent form layouts and input validation.
"""

import streamlit as st
from typing import Dict, Any, Optional, List, Callable
from ..styles.theme import Theme

class BaseForm:
    """Base class for all form components."""
    
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        on_submit: Optional[Callable] = None
    ):
        self.title = title
        self.description = description
        self.on_submit = on_submit
        self.fields: Dict[str, Any] = {}
    
    def add_field(
        self,
        key: str,
        label: str,
        field_type: str = "text",
        required: bool = False,
        help_text: Optional[str] = None,
        options: Optional[List[str]] = None,
        default: Any = None,
        validation: Optional[Callable] = None
    ) -> None:
        """Add a field to the form."""
        self.fields[key] = {
            "label": label,
            "type": field_type,
            "required": required,
            "help_text": help_text,
            "options": options,
            "default": default,
            "validation": validation
        }
    
    def validate(self) -> bool:
        """Validate all form fields."""
        for key, field in self.fields.items():
            if field["required"] and not st.session_state.get(key):
                st.error(f"{field['label']} is required")
                return False
            if field["validation"] and not field["validation"](st.session_state.get(key)):
                return False
        return True
    
    def render(self) -> None:
        """Render the form with consistent styling."""
        with st.container():
            st.markdown(f"""
                <div class="form-container">
                    <h3 style="margin-bottom: {Theme.SPACING['sm']};">{self.title}</h3>
                    {f'<p style="color: {Theme.COLORS["text_secondary"]}; margin-bottom: {Theme.SPACING["md"]};">{self.description}</p>' if self.description else ''}
                </div>
            """, unsafe_allow_html=True)
            
            for key, field in self.fields.items():
                if field["type"] == "text":
                    st.text_input(
                        field["label"],
                        key=key,
                        help=field["help_text"],
                        value=field["default"]
                    )
                elif field["type"] == "textarea":
                    st.text_area(
                        field["label"],
                        key=key,
                        help=field["help_text"],
                        value=field["default"]
                    )
                elif field["type"] == "select":
                    st.selectbox(
                        field["label"],
                        options=field["options"],
                        key=key,
                        help=field["help_text"],
                        index=field["options"].index(field["default"]) if field["default"] in field["options"] else 0
                    )
                elif field["type"] == "multiselect":
                    st.multiselect(
                        field["label"],
                        options=field["options"],
                        key=key,
                        help=field["help_text"],
                        default=field["default"]
                    )
                elif field["type"] == "number":
                    st.number_input(
                        field["label"],
                        key=key,
                        help=field["help_text"],
                        value=field["default"]
                    )
                elif field["type"] == "slider":
                    st.slider(
                        field["label"],
                        key=key,
                        help=field["help_text"],
                        value=field["default"]
                    )
                elif field["type"] == "checkbox":
                    st.checkbox(
                        field["label"],
                        key=key,
                        help=field["help_text"],
                        value=field["default"]
                    )
            
            if st.button("Submit", use_container_width=True):
                if self.validate() and self.on_submit:
                    self.on_submit()

class TweetForm(BaseForm):
    """Form component for tweet generation."""
    
    def __init__(
        self,
        on_submit: Optional[Callable] = None,
        default_tone: str = "professional",
        default_length: str = "medium"
    ):
        super().__init__(
            title="Generate Tweet",
            description="Create engaging tweets with AI assistance",
            on_submit=on_submit
        )
        
        # Add tweet content field
        self.add_field(
            "tweet_content",
            "Tweet Content",
            field_type="textarea",
            required=True,
            help_text="Enter your tweet content or topic"
        )
        
        # Add tone selection
        self.add_field(
            "tone",
            "Tweet Tone",
            field_type="select",
            options=["professional", "casual", "humorous", "informative", "inspirational"],
            default=default_tone,
            help_text="Select the tone for your tweet"
        )
        
        # Add length selection
        self.add_field(
            "length",
            "Tweet Length",
            field_type="select",
            options=["short", "medium", "long"],
            default=default_length,
            help_text="Select the desired length of your tweet"
        )
        
        # Add hashtag options
        self.add_field(
            "hashtags",
            "Hashtags",
            field_type="multiselect",
            options=["#AI", "#Tech", "#Innovation", "#Business", "#Marketing"],
            help_text="Select relevant hashtags"
        )
        
        # Add emoji options
        self.add_field(
            "emojis",
            "Emojis",
            field_type="multiselect",
            options=["🚀", "💡", "🎯", "🔥", "✨"],
            help_text="Select emojis to include"
        )
        
        # Add engagement settings
        self.add_field(
            "engagement_boost",
            "Engagement Boost",
            field_type="slider",
            default=50,
            help_text="Adjust the engagement optimization level"
        )

class SettingsForm(BaseForm):
    """Form component for user settings."""
    
    def __init__(
        self,
        on_submit: Optional[Callable] = None,
        default_settings: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            title="User Settings",
            description="Customize your Twitter experience",
            on_submit=on_submit
        )
        
        settings = default_settings or {}
        
        # Add API settings
        self.add_field(
            "api_key",
            "Twitter API Key",
            field_type="text",
            help_text="Enter your Twitter API key",
            default=settings.get("api_key", "")
        )
        
        # Add theme settings
        self.add_field(
            "theme",
            "Theme",
            field_type="select",
            options=["light", "dark", "system"],
            default=settings.get("theme", "system"),
            help_text="Select your preferred theme"
        )
        
        # Add notification settings
        self.add_field(
            "notifications",
            "Enable Notifications",
            field_type="checkbox",
            default=settings.get("notifications", True),
            help_text="Receive notifications for important updates"
        )
        
        # Add auto-save settings
        self.add_field(
            "auto_save",
            "Auto-save Drafts",
            field_type="checkbox",
            default=settings.get("auto_save", True),
            help_text="Automatically save tweet drafts"
        )
        
        # Add language settings
        self.add_field(
            "language",
            "Language",
            field_type="select",
            options=["English", "Spanish", "French", "German", "Japanese"],
            default=settings.get("language", "English"),
            help_text="Select your preferred language"
        ) 