"""
Card components for Twitter UI.
Provides consistent card layouts for features and tweets.
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from ..styles.theme import Theme

class BaseCard:
    """Base class for all card components."""
    
    def __init__(
        self,
        title: str,
        description: str,
        icon: Optional[str] = None,
        status: Optional[str] = None,
        actions: Optional[List[Dict[str, Any]]] = None
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.status = status
        self.actions = actions or []
    
    def render(self) -> None:
        """Render the card with consistent styling."""
        with st.container():
            st.markdown(f"""
                <div class="card">
                    <div style="display: flex; align-items: center; margin-bottom: {Theme.SPACING["sm"]};">
                        {f'<span style="font-size: 1.5em; margin-right: {Theme.SPACING["sm"]};">{self.icon}</span>' if self.icon else ''}
                        <h3 style="margin: 0;">{self.title}</h3>
                    </div>
                    <p style="color: {Theme.COLORS["text_secondary"]}; margin: {Theme.SPACING["sm"]} 0;">
                        {self.description}
                    </p>
                    {f'<span class="status-badge status-{self.status}">{self.status.title()}</span>' if self.status else ''}
                </div>
            """, unsafe_allow_html=True)
            
            if self.actions:
                cols = st.columns(len(self.actions))
                for i, action in enumerate(self.actions):
                    with cols[i]:
                        if st.button(
                            action["label"],
                            key=f"action_{i}",
                            help=action.get("help"),
                            use_container_width=True
                        ):
                            action["callback"]()

class FeatureCard(BaseCard):
    """Card component for displaying features."""
    
    def __init__(
        self,
        title: str,
        description: str,
        icon: str,
        status: str = "active",
        features: Optional[List[Dict[str, Any]]] = None,
        on_click: Optional[callable] = None
    ):
        super().__init__(title, description, icon, status)
        self.features = features or []
        self.on_click = on_click
    
    def render(self) -> None:
        """Render the feature card with enhanced styling."""
        with st.container():
            st.markdown(f"""
                <div class="card feature-card">
                    <div style="display: flex; align-items: center; margin-bottom: {Theme.SPACING["sm"]};">
                        <span style="font-size: 1.5em; margin-right: {Theme.SPACING["sm"]};">{self.icon}</span>
                        <h3 style="margin: 0;">{self.title}</h3>
                    </div>
                    <p style="color: {Theme.COLORS["text_secondary"]}; margin: {Theme.SPACING["sm"]} 0;">
                        {self.description}
                    </p>
                    <span class="status-badge status-{self.status}">{self.status.title()}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if self.features:
                for feature in self.features:
                    st.markdown(f"""
                        <div style="margin-left: {Theme.SPACING["lg"]}; margin-top: {Theme.SPACING["sm"]};">
                            <p style="margin: 0;">
                                <strong>{feature["name"]}</strong>: {feature["description"]}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
            
            if self.on_click:
                if st.button(
                    f"Launch {self.title}",
                    key=f"launch_{self.title.lower().replace(' ', '_')}",
                    use_container_width=True
                ):
                    self.on_click()

class TweetCard(BaseCard):
    """Card component for displaying tweets."""
    
    def __init__(
        self,
        content: str,
        engagement_score: float,
        hashtags: List[str],
        emojis: List[str],
        metrics: Optional[Dict[str, Any]] = None,
        on_copy: Optional[callable] = None,
        on_save: Optional[callable] = None
    ):
        super().__init__(
            title="Tweet",
            description=content,
            icon="🐦",
            actions=[
                {
                    "label": "Copy",
                    "callback": on_copy or (lambda: None),
                    "help": "Copy tweet to clipboard"
                },
                {
                    "label": "Save",
                    "callback": on_save or (lambda: None),
                    "help": "Save tweet for later"
                }
            ]
        )
        self.engagement_score = engagement_score
        self.hashtags = hashtags
        self.emojis = emojis
        self.metrics = metrics or {}
    
    def render(self) -> None:
        """Render the tweet card with metrics and actions."""
        with st.container():
            st.markdown(f"""
                <div class="card tweet-card">
                    <div style="display: flex; align-items: center; margin-bottom: {Theme.SPACING["sm"]};">
                        <span style="font-size: 1.5em; margin-right: {Theme.SPACING["sm"]};">{self.icon}</span>
                        <h3 style="margin: 0;">Tweet</h3>
                    </div>
                    <p style="color: {Theme.COLORS["text"]}; margin: {Theme.SPACING["sm"]} 0;">
                        {self.description}
                    </p>
                    <div style="display: flex; gap: {Theme.SPACING["sm"]}; margin: {Theme.SPACING["sm"]} 0;">
                        {''.join(f'<span style="color: {Theme.COLORS["primary"]};">{tag}</span>' for tag in self.hashtags)}
                    </div>
                    <div style="display: flex; gap: {Theme.SPACING["sm"]}; margin: {Theme.SPACING["sm"]} 0;">
                        {''.join(f'<span>{emoji}</span>' for emoji in self.emojis)}
                    </div>
                    <div style="margin-top: {Theme.SPACING["md"]};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span>Engagement Score: {self.engagement_score}%</span>
                            <div style="display: flex; gap: {Theme.SPACING["sm"]};">
                                <button class="stButton" onclick="copyTweet()">Copy</button>
                                <button class="stButton" onclick="saveTweet()">Save</button>
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if self.metrics:
                cols = st.columns(len(self.metrics))
                for i, (metric, value) in enumerate(self.metrics.items()):
                    with cols[i]:
                        st.metric(metric, f"{value}%") 