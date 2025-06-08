"""
Navigation components for Twitter UI.
Provides consistent navigation and layout structure.
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from ..styles.theme import Theme

class Sidebar:
    """Sidebar navigation component."""
    
    def __init__(
        self,
        title: str = "Twitter Tools",
        logo: Optional[str] = None,
        menu_items: Optional[List[Dict[str, Any]]] = None
    ):
        self.title = title
        self.logo = logo
        self.menu_items = menu_items or []
    
    def add_menu_item(
        self,
        label: str,
        icon: str,
        page: str,
        badge: Optional[str] = None
    ) -> None:
        """Add a menu item to the sidebar."""
        self.menu_items.append({
            "label": label,
            "icon": icon,
            "page": page,
            "badge": badge
        })
    
    def render(self) -> None:
        """Render the sidebar with consistent styling."""
        with st.sidebar:
            # Logo and title
            if self.logo:
                try:
                    import os
                    if os.path.exists(self.logo):
                        st.image(self.logo, width=50)
                    else:
                        # Show a placeholder or just skip the logo
                        st.markdown("🐦", help="Twitter Tools Logo")
                except Exception as e:
                    # If there's any error loading the image, show an emoji instead
                    st.markdown("🐦", help="Twitter Tools Logo")
            
            st.markdown(f"""
                <h2 style="margin: {Theme.SPACING["sm"]} 0;">{self.title}</h2>
            """, unsafe_allow_html=True)
            
            # Menu items
            for item in self.menu_items:
                st.markdown(f"""
                    <div class="menu-item">
                        <span style="font-size: 1.2em; margin-right: {Theme.SPACING["sm"]};">{item["icon"]}</span>
                        <span>{item["label"]}</span>
                        {f'<span class="badge">{item["badge"]}</span>' if item.get("badge") else ""}
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(
                    item["label"],
                    key=f"nav_{item['page']}",
                    use_container_width=True
                ):
                    st.session_state["current_page"] = item["page"]

class Header:
    """Header navigation component."""
    
    def __init__(
        self,
        title: str,
        subtitle: Optional[str] = None,
        actions: Optional[List[Dict[str, Any]]] = None
    ):
        self.title = title
        self.subtitle = subtitle
        self.actions = actions or []
    
    def add_action(
        self,
        label: str,
        icon: str,
        callback: callable,
        help_text: Optional[str] = None
    ) -> None:
        """Add an action button to the header."""
        self.actions.append({
            "label": label,
            "icon": icon,
            "callback": callback,
            "help_text": help_text
        })
    
    def render(self) -> None:
        """Render the header with consistent styling."""
        # Build action buttons HTML
        action_buttons = []
        for action in self.actions:
            help_text = action.get("help_text", "")
            action_buttons.append(f"""
                <button class="header-action" title="{help_text}">
                    <span style="font-size: 1.2em; margin-right: {Theme.SPACING["xs"]};">{action["icon"]}</span>
                    {action["label"]}
                </button>
            """)
        
        st.markdown(f"""
            <div class="header">
                <div>
                    <h1 style="margin: 0;">{self.title}</h1>
                    {f'<p style="color: {Theme.COLORS["text_secondary"]}; margin: {Theme.SPACING["xs"]} 0;">{self.subtitle}</p>' if self.subtitle else ""}
                </div>
                <div style="display: flex; gap: {Theme.SPACING["sm"]};">
                    {''.join(action_buttons)}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Add action button callbacks
        for i, action in enumerate(self.actions):
            if st.button(
                action["label"],
                key=f"header_action_{i}",
                help=action.get("help_text")
            ):
                action["callback"]()

class Tabs:
    """Tab navigation component."""
    
    def __init__(
        self,
        tabs: Optional[List[Dict[str, Any]]] = None,
        default_tab: Optional[str] = None
    ):
        self.tabs = tabs or []
        self.default_tab = default_tab
    
    def add_tab(
        self,
        label: str,
        icon: Optional[str] = None,
        content: Optional[callable] = None
    ) -> None:
        """Add a tab to the navigation."""
        self.tabs.append({
            "label": label,
            "icon": icon,
            "content": content
        })
    
    def render(self) -> None:
        """Render the tabs with consistent styling."""
        if not self.tabs:
            return
        
        # Create tab labels with icons
        tab_labels = [
            f"{tab['icon']} {tab['label']}" if tab.get('icon') else tab['label']
            for tab in self.tabs
        ]
        
        # Get current tab from session state or use default
        current_tab = st.session_state.get("current_tab", self.default_tab or self.tabs[0]["label"])
        
        # Render tabs
        selected_tab = st.tabs(tab_labels)[tab_labels.index(current_tab)]
        
        # Update session state
        st.session_state["current_tab"] = current_tab
        
        # Render tab content
        with selected_tab:
            for tab in self.tabs:
                if tab["label"] == current_tab and tab.get("content"):
                    tab["content"]()

class Breadcrumbs:
    """Breadcrumb navigation component."""
    
    def __init__(
        self,
        items: Optional[List[Dict[str, Any]]] = None
    ):
        self.items = items or []
    
    def add_item(
        self,
        label: str,
        page: Optional[str] = None,
        icon: Optional[str] = None
    ) -> None:
        """Add a breadcrumb item."""
        self.items.append({
            "label": label,
            "page": page,
            "icon": icon
        })
    
    def render(self) -> None:
        """Render the breadcrumbs with consistent styling."""
        if not self.items:
            return
        
        breadcrumb_items = []
        for i, item in enumerate(self.items):
            icon_html = f'<span style="font-size: 1.2em; margin-right: {Theme.SPACING["xs"]};">{item["icon"]}</span>' if item.get("icon") else ""
            link_html = f'<a href="#" onclick="setPage(\'{item["page"]}\')">{item["label"]}</a>' if item.get("page") else f'<span>{item["label"]}</span>'
            separator = f'<span style="margin: 0 {Theme.SPACING["xs"]};">/</span>' if i < len(self.items) - 1 else ""
            
            breadcrumb_items.append(f"""
                <span class="breadcrumb-item">
                    {icon_html}
                    {link_html}
                </span>
                {separator}
            """)
        
        st.markdown(f"""
            <div class="breadcrumbs">
                {''.join(breadcrumb_items)}
            </div>
        """, unsafe_allow_html=True) 