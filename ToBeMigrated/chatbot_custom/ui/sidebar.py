"""
Sidebar Manager for Enhanced ALwrity Chatbot.

Manages the intelligent sidebar with dashboard, quick tools, and user analytics.
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime


class SidebarManager:
    """Manages the enhanced sidebar interface."""
    
    def __init__(self, context_manager, workflow_engine, tool_router):
        self.context_manager = context_manager
        self.workflow_engine = workflow_engine
        self.tool_router = tool_router
    
    def render_sidebar(self) -> Dict[str, Any]:
        """Render the complete sidebar interface."""
        sidebar_data = {}
        
        with st.sidebar:
            # Header
            st.markdown("# 🚀 ALwrity Hub")
            st.markdown("---")
            
            # Dashboard section
            sidebar_data.update(self._render_dashboard())
            
            # Quick tools section
            sidebar_data.update(self._render_quick_tools())
            
            # Active workflows section
            sidebar_data.update(self._render_active_workflows())
            
            # User preferences section
            sidebar_data.update(self._render_user_preferences())
            
            # Analytics section
            sidebar_data.update(self._render_analytics())
            
            # Export/Import section
            sidebar_data.update(self._render_export_import())
            
        return sidebar_data
    
    def _render_dashboard(self) -> Dict[str, Any]:
        """Render the dashboard section."""
        st.markdown("## 📊 Dashboard")
        
        # Get user analytics
        analytics = self.context_manager.get_user_analytics()
        
        # Key metrics in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Total Interactions",
                value=analytics.get("total_interactions", 0)
            )
            st.metric(
                label="Active Workflows",
                value=analytics.get("active_workflows_count", 0)
            )
        
        with col2:
            st.metric(
                label="Workflows Completed",
                value=analytics.get("workflows_completed", 0)
            )
            st.metric(
                label="Conversation Turns",
                value=analytics.get("conversation_turns", 0)
            )
        
        # Most used tools
        most_used_tools = analytics.get("most_used_tools", [])
        if most_used_tools:
            st.markdown("**🔧 Most Used Tools:**")
            for tool, count in most_used_tools[:3]:
                st.markdown(f"• {tool}: {count} times")
        
        st.markdown("---")
        
        return {"dashboard_rendered": True}
    
    def _render_quick_tools(self) -> Dict[str, Any]:
        """Render the quick tools section."""
        st.markdown("## ⚡ Quick Tools")
        
        quick_actions = {}
        
        # Content creation tools
        st.markdown("**✍️ Content Creation**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Blog Writer", key="quick_blog"):
                quick_actions["action"] = "blog_writer"
            if st.button("📱 Social Post", key="quick_social"):
                quick_actions["action"] = "social_post"
        
        with col2:
            if st.button("📧 Email Writer", key="quick_email"):
                quick_actions["action"] = "email_writer"
            if st.button("📖 Story Writer", key="quick_story"):
                quick_actions["action"] = "story_writer"
        
        # SEO tools
        st.markdown("**🔍 SEO Tools**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔧 Technical SEO", key="quick_tech_seo"):
                quick_actions["action"] = "technical_seo"
            if st.button("📊 Content Gap", key="quick_content_gap"):
                quick_actions["action"] = "content_gap"
        
        with col2:
            if st.button("🎯 Keyword Research", key="quick_keywords"):
                quick_actions["action"] = "keyword_research"
            if st.button("🏆 Competitor Analysis", key="quick_competitor"):
                quick_actions["action"] = "competitor_analysis"
        
        # Analysis tools
        st.markdown("**📈 Analysis**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌐 Website Analyzer", key="quick_website"):
                quick_actions["action"] = "website_analyzer"
            if st.button("📋 On-Page SEO", key="quick_onpage"):
                quick_actions["action"] = "onpage_seo"
        
        with col2:
            if st.button("🔗 URL SEO Check", key="quick_url_seo"):
                quick_actions["action"] = "url_seo_check"
            if st.button("📱 Social Analyzer", key="quick_social_analyzer"):
                quick_actions["action"] = "social_analyzer"
        
        st.markdown("---")
        
        return {"quick_actions": quick_actions}
    
    def _render_active_workflows(self) -> Dict[str, Any]:
        """Render the active workflows section."""
        st.markdown("## 🔄 Active Workflows")
        
        workflow_actions = {}
        active_workflows = self.context_manager.get_active_workflows()
        paused_workflows = self.context_manager.get_paused_workflows()
        
        if active_workflows:
            for workflow in active_workflows:
                with st.expander(f"🟢 {workflow.workflow_name}"):
                    # Progress bar
                    progress = workflow.current_step / workflow.total_steps
                    st.progress(progress)
                    st.markdown(f"Step {workflow.current_step}/{workflow.total_steps}")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("⏸️ Pause", key=f"pause_{workflow.workflow_id}"):
                            workflow_actions["pause"] = workflow.workflow_id
                    with col2:
                        if st.button("▶️ Continue", key=f"continue_{workflow.workflow_id}"):
                            workflow_actions["continue"] = workflow.workflow_id
        
        if paused_workflows:
            st.markdown("**⏸️ Paused Workflows:**")
            for workflow in paused_workflows:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"• {workflow.workflow_name}")
                with col2:
                    if st.button("▶️", key=f"resume_{workflow.workflow_id}"):
                        workflow_actions["resume"] = workflow.workflow_id
        
        # Start new workflow
        st.markdown("**🆕 Start New Workflow:**")
        available_workflows = list(self.workflow_engine.workflows.keys())
        selected_workflow = st.selectbox(
            "Choose workflow:",
            [""] + available_workflows,
            key="new_workflow_select"
        )
        
        if selected_workflow and st.button("🚀 Start Workflow", key="start_new_workflow"):
            workflow_actions["start"] = selected_workflow
        
        st.markdown("---")
        
        return {"workflow_actions": workflow_actions}
    
    def _render_user_preferences(self) -> Dict[str, Any]:
        """Render the user preferences section."""
        st.markdown("## ⚙️ Preferences")
        
        preferences_updated = {}
        current_prefs = self.context_manager.user_preferences
        
        with st.expander("🎨 Content Preferences"):
            # Tone preference
            tone = st.selectbox(
                "Preferred Tone:",
                ["professional", "casual", "friendly", "formal", "creative"],
                index=["professional", "casual", "friendly", "formal", "creative"].index(
                    current_prefs.preferred_tone
                ),
                key="pref_tone"
            )
            
            # Length preference
            length = st.selectbox(
                "Preferred Length:",
                ["short", "medium", "long", "comprehensive"],
                index=["short", "medium", "long", "comprehensive"].index(
                    current_prefs.preferred_length
                ),
                key="pref_length"
            )
            
            # Industry focus
            industry_focus = st.multiselect(
                "Industry Focus:",
                ["Technology", "Healthcare", "Finance", "Education", "Marketing", 
                 "E-commerce", "Travel", "Food", "Fashion", "Real Estate"],
                default=current_prefs.industry_focus,
                key="pref_industry"
            )
            
            # Content preferences
            content_prefs = st.multiselect(
                "Content Types:",
                ["Blog Posts", "Social Media", "Email Marketing", "Technical Writing",
                 "Creative Writing", "SEO Content", "Product Descriptions", "News Articles"],
                default=current_prefs.content_preferences,
                key="pref_content_types"
            )
            
            if st.button("💾 Save Preferences", key="save_preferences"):
                preferences_updated = {
                    "preferred_tone": tone,
                    "preferred_length": length,
                    "industry_focus": industry_focus,
                    "content_preferences": content_prefs
                }
        
        st.markdown("---")
        
        return {"preferences_updated": preferences_updated}
    
    def _render_analytics(self) -> Dict[str, Any]:
        """Render the analytics section."""
        st.markdown("## 📈 Analytics")
        
        analytics = self.context_manager.get_user_analytics()
        
        with st.expander("📊 Usage Statistics"):
            # Recent activity pattern
            recent_activity = analytics.get("recent_activity_pattern", {})
            if recent_activity:
                st.markdown("**Recent Activity:**")
                for date, count in list(recent_activity.items())[-7:]:  # Last 7 days
                    st.markdown(f"• {date}: {count} interactions")
            
            # Tool usage breakdown
            most_used_tools = analytics.get("most_used_tools", [])
            if most_used_tools:
                st.markdown("**Tool Usage Breakdown:**")
                for tool, count in most_used_tools:
                    percentage = (count / analytics.get("total_interactions", 1)) * 100
                    st.markdown(f"• {tool}: {count} ({percentage:.1f}%)")
        
        # Context summary
        with st.expander("🧠 Context Summary"):
            context_summary = self.context_manager.get_context_summary()
            st.text(context_summary)
        
        st.markdown("---")
        
        return {"analytics_viewed": True}
    
    def _render_export_import(self) -> Dict[str, Any]:
        """Render the export/import section."""
        st.markdown("## 💾 Data Management")
        
        export_actions = {}
        
        with st.expander("📤 Export Data"):
            export_format = st.selectbox(
                "Export Format:",
                ["JSON", "TXT"],
                key="export_format"
            )
            
            if st.button("📥 Export Conversation History", key="export_history"):
                export_actions["export"] = {
                    "type": "conversation_history",
                    "format": export_format.lower()
                }
            
            if st.button("📊 Export Analytics", key="export_analytics"):
                export_actions["export"] = {
                    "type": "analytics",
                    "format": export_format.lower()
                }
        
        with st.expander("🗑️ Data Cleanup"):
            cleanup_days = st.number_input(
                "Keep data for (days):",
                min_value=1,
                max_value=365,
                value=30,
                key="cleanup_days"
            )
            
            if st.button("🧹 Cleanup Old Data", key="cleanup_data"):
                export_actions["cleanup"] = cleanup_days
            
            if st.button("⚠️ Reset All Data", key="reset_data"):
                if st.checkbox("I understand this will delete all data", key="confirm_reset"):
                    export_actions["reset"] = True
        
        return {"export_actions": export_actions}
    
    def render_workflow_suggestions(self, intent_analysis: Dict[str, Any]) -> Optional[str]:
        """Render workflow suggestions based on intent analysis."""
        suggested_workflows = intent_analysis.get("suggested_workflows", [])
        
        if suggested_workflows:
            st.sidebar.markdown("## 💡 Suggested Workflows")
            
            for workflow in suggested_workflows[:3]:  # Show top 3 suggestions
                workflow_info = self.workflow_engine.get_workflow(workflow)
                if workflow_info:
                    with st.sidebar.expander(f"🔄 {workflow_info['name']}"):
                        st.markdown(f"**Description:** {workflow_info['description']}")
                        st.markdown(f"**Steps:** {len(workflow_info['steps'])}")
                        
                        if st.button(f"Start {workflow_info['name']}", 
                                   key=f"suggest_{workflow}"):
                            return workflow
        
        return None
    
    def render_tool_suggestions(self, intent_analysis: Dict[str, Any]) -> Optional[str]:
        """Render tool suggestions based on intent analysis."""
        suggested_tools = intent_analysis.get("suggested_tools", [])
        
        if suggested_tools:
            st.sidebar.markdown("## 🛠️ Suggested Tools")
            
            # Group tools by category
            tool_categories = self.tool_router.tool_categories
            categorized_tools = {}
            
            for tool in suggested_tools[:6]:  # Show top 6 suggestions
                for category, tools in tool_categories.items():
                    if tool in tools:
                        if category not in categorized_tools:
                            categorized_tools[category] = []
                        categorized_tools[category].append(tool)
                        break
            
            for category, tools in categorized_tools.items():
                st.sidebar.markdown(f"**{category.title()}:**")
                for tool in tools:
                    if st.sidebar.button(f"🚀 {tool.replace('_', ' ').title()}", 
                                       key=f"suggest_tool_{tool}"):
                        return tool
        
        return None
    
    def show_notification(self, message: str, type: str = "info"):
        """Show a notification in the sidebar."""
        if type == "success":
            st.sidebar.success(message)
        elif type == "error":
            st.sidebar.error(message)
        elif type == "warning":
            st.sidebar.warning(message)
        else:
            st.sidebar.info(message)
    
    def get_sidebar_state(self) -> Dict[str, Any]:
        """Get current sidebar state for persistence."""
        return {
            "last_updated": datetime.now().isoformat(),
            "active_sections": st.session_state.get("sidebar_sections", []),
            "user_preferences": self.context_manager.user_preferences.__dict__
        } 