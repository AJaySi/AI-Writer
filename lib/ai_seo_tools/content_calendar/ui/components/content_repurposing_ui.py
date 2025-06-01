import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from pathlib import Path
import sys

# Add parent directory to path to import existing tools
parent_dir = str(Path(__file__).parent.parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from lib.database.models import ContentItem, ContentType, Platform, SEOData
from lib.ai_seo_tools.content_calendar.core.content_repurposer import SmartContentRepurposingEngine
from lib.ai_seo_tools.content_calendar.core.content_generator import ContentGenerator

logger = logging.getLogger(__name__)

class ContentRepurposingUI:
    """
    Streamlit UI component for the Smart Content Repurposing Engine.
    """
    
    def __init__(self):
        self.repurposing_engine = SmartContentRepurposingEngine()
        self.content_generator = ContentGenerator()
        self.logger = logging.getLogger('content_calendar.repurposing_ui')
    
    def render_repurposing_interface(self):
        """Render the main repurposing interface."""
        st.header("🔄 Smart Content Repurposing Engine")
        st.markdown("Transform your content into multiple platform-optimized pieces with AI-powered repurposing.")
        
        # Create tabs for different repurposing functions
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Single Content Repurposing",
            "📚 Content Series Creation", 
            "🔍 Content Analysis",
            "📊 Repurposing Dashboard"
        ])
        
        with tab1:
            self._render_single_content_repurposing()
        
        with tab2:
            self._render_content_series_creation()
        
        with tab3:
            self._render_content_analysis()
        
        with tab4:
            self._render_repurposing_dashboard()
    
    def _render_single_content_repurposing(self):
        """Render the single content repurposing interface."""
        st.subheader("Repurpose Single Content")
        st.markdown("Transform one piece of content into multiple platform-optimized variations.")
        
        # Content input section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📄 Source Content")
            
            # Content input options
            input_method = st.radio(
                "How would you like to provide content?",
                ["Manual Input", "Upload File", "Select from Calendar"],
                horizontal=True
            )
            
            source_content = None
            
            if input_method == "Manual Input":
                source_content = self._render_manual_content_input()
            elif input_method == "Upload File":
                source_content = self._render_file_upload_input()
            else:  # Select from Calendar
                source_content = self._render_calendar_selection()
        
        with col2:
            st.markdown("### 🎯 Target Platforms")
            
            # Platform selection
            available_platforms = [
                Platform.TWITTER,
                Platform.LINKEDIN,
                Platform.INSTAGRAM,
                Platform.FACEBOOK,
                Platform.WEBSITE
            ]
            
            selected_platforms = st.multiselect(
                "Select target platforms:",
                options=available_platforms,
                default=[Platform.TWITTER, Platform.LINKEDIN],
                format_func=lambda x: x.name.title()
            )
            
            # Repurposing strategy
            strategy = st.selectbox(
                "Repurposing Strategy:",
                ["adaptive", "atomic", "series"],
                help="Adaptive: AI chooses best approach, Atomic: Break into small pieces, Series: Create connected content"
            )
        
        # Generate repurposed content
        if st.button("🚀 Generate Repurposed Content", type="primary"):
            if source_content and selected_platforms:
                with st.spinner("Repurposing content..."):
                    try:
                        repurposed_content = self.content_generator.repurpose_content_for_platforms(
                            content_item=source_content,
                            target_platforms=selected_platforms,
                            strategy=strategy
                        )
                        
                        if repurposed_content:
                            self._display_repurposed_content(repurposed_content)
                        else:
                            st.error("Failed to generate repurposed content. Please try again.")
                    
                    except Exception as e:
                        st.error(f"Error during repurposing: {str(e)}")
            else:
                st.warning("Please provide source content and select at least one target platform.")
    
    def _render_content_series_creation(self):
        """Render the content series creation interface."""
        st.subheader("Create Cross-Platform Content Series")
        st.markdown("Generate a strategic content series that progressively reveals information across platforms.")
        
        # Source content input
        source_content = self._render_manual_content_input(key_suffix="_series")
        
        if source_content:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🌐 Platform Strategy")
                
                # Platform selection with strategy
                platforms = st.multiselect(
                    "Select platforms for series:",
                    options=[Platform.TWITTER, Platform.LINKEDIN, Platform.INSTAGRAM, Platform.FACEBOOK, Platform.WEBSITE],
                    default=[Platform.TWITTER, Platform.LINKEDIN, Platform.WEBSITE],
                    format_func=lambda x: x.name.title(),
                    key="series_platforms"
                )
                
                series_type = st.selectbox(
                    "Series Strategy:",
                    ["progressive_disclosure", "platform_native"],
                    help="Progressive: Gradually reveal info across platforms, Native: Optimize for each platform's strengths"
                )
            
            with col2:
                st.markdown("### 📅 Timeline Preview")
                
                if platforms:
                    # Show timeline preview
                    timeline_df = self._create_series_timeline_preview(source_content, platforms)
                    st.dataframe(timeline_df, use_container_width=True)
            
            # Generate series
            if st.button("📚 Create Content Series", type="primary", key="create_series"):
                if platforms:
                    with st.spinner("Creating content series..."):
                        try:
                            series_content = self.content_generator.create_content_series_across_platforms(
                                source_content=source_content,
                                platforms=platforms,
                                series_type=series_type
                            )
                            
                            if series_content:
                                self._display_content_series(series_content)
                            else:
                                st.error("Failed to create content series. Please try again.")
                        
                        except Exception as e:
                            st.error(f"Error creating series: {str(e)}")
                else:
                    st.warning("Please select at least one platform for the series.")
    
    def _render_content_analysis(self):
        """Render the content analysis interface."""
        st.subheader("Content Repurposing Analysis")
        st.markdown("Analyze your content's repurposing potential and get AI-powered recommendations.")
        
        # Content input
        content_to_analyze = self._render_manual_content_input(key_suffix="_analysis")
        
        if content_to_analyze:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                available_platforms = st.multiselect(
                    "Available platforms for analysis:",
                    options=[Platform.TWITTER, Platform.LINKEDIN, Platform.INSTAGRAM, Platform.FACEBOOK, Platform.WEBSITE],
                    default=[Platform.TWITTER, Platform.LINKEDIN, Platform.INSTAGRAM, Platform.FACEBOOK, Platform.WEBSITE],
                    format_func=lambda x: x.name.title(),
                    key="analysis_platforms"
                )
            
            with col2:
                if st.button("🔍 Analyze Content", type="primary"):
                    if available_platforms:
                        with st.spinner("Analyzing content..."):
                            try:
                                analysis = self.content_generator.analyze_content_for_repurposing(
                                    content_item=content_to_analyze,
                                    available_platforms=available_platforms
                                )
                                
                                if analysis:
                                    self._display_content_analysis(analysis)
                                else:
                                    st.error("Failed to analyze content. Please try again.")
                            
                            except Exception as e:
                                st.error(f"Error during analysis: {str(e)}")
                    else:
                        st.warning("Please select at least one platform for analysis.")
    
    def _render_repurposing_dashboard(self):
        """Render the repurposing dashboard with metrics and insights."""
        st.subheader("Repurposing Dashboard")
        st.markdown("Track your content repurposing performance and insights.")
        
        # Mock data for demonstration
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Content Pieces Created", "156", "+23")
        
        with col2:
            st.metric("Time Saved", "312 hours", "+45 hours")
        
        with col3:
            st.metric("Platform Coverage", "85%", "+12%")
        
        with col4:
            st.metric("Engagement Boost", "34%", "+8%")
        
        # Recent repurposing activity
        st.markdown("### 📈 Recent Repurposing Activity")
        
        # Mock data for recent activity
        recent_activity = pd.DataFrame({
            'Date': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12'],
            'Source Content': ['AI Writing Tips', 'SEO Best Practices', 'Content Strategy Guide', 'Social Media Trends'],
            'Platforms': ['Twitter, LinkedIn', 'LinkedIn, Instagram', 'All Platforms', 'Twitter, Facebook'],
            'Pieces Created': [3, 2, 5, 2],
            'Status': ['Published', 'Scheduled', 'Draft', 'Published']
        })
        
        st.dataframe(recent_activity, use_container_width=True)
        
        # Performance insights
        st.markdown("### 💡 Performance Insights")
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.info("🎯 **Best Performing Platform**: LinkedIn posts show 45% higher engagement when repurposed from blog content.")
        
        with insights_col2:
            st.success("📊 **Optimization Tip**: Twitter threads perform 60% better when created from long-form content with statistics.")
    
    def _render_manual_content_input(self, key_suffix: str = "") -> Optional[ContentItem]:
        """Render manual content input form."""
        with st.form(f"content_input_form{key_suffix}"):
            title = st.text_input("Content Title:", key=f"title{key_suffix}")
            content_type = st.selectbox(
                "Content Type:",
                options=[ContentType.BLOG_POST, ContentType.SOCIAL_MEDIA, ContentType.VIDEO, ContentType.NEWSLETTER],
                format_func=lambda x: x.name.replace('_', ' ').title(),
                key=f"content_type{key_suffix}"
            )
            
            description = st.text_area(
                "Content Description/Body:",
                height=200,
                help="Paste your content here. This will be analyzed and repurposed.",
                key=f"description{key_suffix}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                author = st.text_input("Author:", value="Content Creator", key=f"author{key_suffix}")
            with col2:
                tags = st.text_input("Tags (comma-separated):", key=f"tags{key_suffix}")
            
            submitted = st.form_submit_button("📝 Use This Content")
            
            if submitted and title and description:
                # Create ContentItem
                content_item = ContentItem(
                    title=title,
                    description=description,
                    content_type=content_type,
                    platforms=[],
                    publish_date=datetime.now(),
                    status="draft",
                    author=author,
                    tags=tags.split(',') if tags else [],
                    notes="",
                    seo_data=SEOData(title=title, meta_description="", keywords=[], structured_data={})
                )
                return content_item
        
        return None
    
    def _render_file_upload_input(self) -> Optional[ContentItem]:
        """Render file upload input."""
        uploaded_file = st.file_uploader(
            "Upload content file:",
            type=['txt', 'md', 'docx'],
            help="Upload a text file, markdown file, or Word document"
        )
        
        if uploaded_file:
            try:
                # Read file content
                if uploaded_file.type == "text/plain":
                    content = str(uploaded_file.read(), "utf-8")
                else:
                    content = str(uploaded_file.read(), "utf-8")  # Simplified for demo
                
                # Extract title from filename
                title = uploaded_file.name.split('.')[0].replace('_', ' ').title()
                
                # Create ContentItem
                content_item = ContentItem(
                    title=title,
                    description=content,
                    content_type=ContentType.BLOG_POST,
                    platforms=[],
                    publish_date=datetime.now(),
                    status="draft",
                    author="Uploaded Content",
                    tags=[],
                    notes=f"Uploaded from file: {uploaded_file.name}",
                    seo_data=SEOData(title=title, meta_description="", keywords=[], structured_data={})
                )
                
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                return content_item
                
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        
        return None
    
    def _render_calendar_selection(self) -> Optional[ContentItem]:
        """Render calendar content selection."""
        st.info("📅 Calendar integration coming soon! For now, please use manual input or file upload.")
        return None
    
    def _display_repurposed_content(self, repurposed_content: List[ContentItem]):
        """Display the repurposed content results."""
        st.success(f"✅ Successfully created {len(repurposed_content)} repurposed content pieces!")
        
        for i, content in enumerate(repurposed_content):
            with st.expander(f"📱 {content.platforms[0].name.title()} - {content.title}"):
                st.markdown(f"**Platform:** {content.platforms[0].name.title()}")
                st.markdown(f"**Content Type:** {content.content_type.name.replace('_', ' ').title()}")
                st.markdown(f"**Scheduled for:** {content.publish_date.strftime('%Y-%m-%d')}")
                
                st.markdown("**Content:**")
                st.write(content.description)
                
                if content.tags:
                    st.markdown(f"**Tags:** {', '.join(content.tags)}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📝 Edit", key=f"edit_{i}"):
                        st.info("Edit functionality coming soon!")
                with col2:
                    if st.button(f"📅 Schedule", key=f"schedule_{i}"):
                        st.info("Scheduling functionality coming soon!")
                with col3:
                    if st.button(f"📋 Copy", key=f"copy_{i}"):
                        st.code(content.description)
    
    def _display_content_series(self, series_content: Dict[str, List[ContentItem]]):
        """Display the content series results."""
        total_pieces = sum(len(pieces) for pieces in series_content.values())
        st.success(f"✅ Successfully created content series with {total_pieces} pieces across {len(series_content)} platforms!")
        
        for platform, content_pieces in series_content.items():
            st.markdown(f"### 📱 {platform.title()} Series ({len(content_pieces)} pieces)")
            
            for i, content in enumerate(content_pieces):
                with st.expander(f"Part {i+1}: {content.title}"):
                    st.markdown(f"**Scheduled for:** {content.publish_date.strftime('%Y-%m-%d')}")
                    st.markdown("**Content:**")
                    st.write(content.description)
                    
                    if content.tags:
                        st.markdown(f"**Tags:** {', '.join(content.tags)}")
    
    def _display_content_analysis(self, analysis: Dict[str, Any]):
        """Display content analysis results."""
        st.markdown("### 📊 Content Analysis Results")
        
        # Content metrics
        col1, col2, col3 = st.columns(3)
        
        content_analysis = analysis.get('content_analysis', {})
        
        with col1:
            st.metric("Word Count", content_analysis.get('word_count', 0))
        
        with col2:
            richness = content_analysis.get('content_richness', 'Unknown')
            st.metric("Content Richness", richness)
        
        with col3:
            potential = content_analysis.get('repurposing_potential', 'Unknown')
            st.metric("Repurposing Potential", potential)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Recommended Platforms:**")
            platforms = analysis.get('platform_suggestions', [])
            for platform in platforms:
                st.write(f"• {platform.name.title()}")
        
        with col2:
            st.markdown("**Suggested Strategies:**")
            strategies = analysis.get('strategy_suggestions', [])
            for strategy in strategies:
                st.write(f"• {strategy.replace('_', ' ').title()}")
        
        # Content atoms
        st.markdown("### 🔬 Content Atoms Analysis")
        
        atoms = content_analysis.get('content_atoms', {})
        
        for atom_type, atom_list in atoms.items():
            if atom_list:
                with st.expander(f"{atom_type.title()} ({len(atom_list)} found)"):
                    for atom in atom_list:
                        st.write(f"• {atom}")
        
        # Estimated output
        estimated = analysis.get('estimated_output', {})
        if estimated:
            st.markdown("### 📈 Estimated Output")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Pieces", estimated.get('total_pieces', 0))
            
            with col2:
                st.metric("Time Savings", estimated.get('time_savings', '0 hours'))
            
            with col3:
                st.metric("Content Multiplication", estimated.get('content_multiplication', '1x'))
    
    def _create_series_timeline_preview(self, content: ContentItem, platforms: List[Platform]) -> pd.DataFrame:
        """Create a preview timeline for content series."""
        timeline_data = []
        base_date = datetime.now()
        
        for i, platform in enumerate(platforms):
            release_date = base_date + timedelta(days=i)
            timeline_data.append({
                'Platform': platform.name.title(),
                'Release Date': release_date.strftime('%Y-%m-%d'),
                'Content Type': self._get_platform_content_type(platform),
                'Strategy': self._get_platform_strategy(platform)
            })
        
        return pd.DataFrame(timeline_data)
    
    def _get_platform_content_type(self, platform: Platform) -> str:
        """Get content type for platform."""
        types = {
            Platform.TWITTER: "Thread/Tweet",
            Platform.LINKEDIN: "Professional Post",
            Platform.INSTAGRAM: "Visual Post",
            Platform.FACEBOOK: "Engaging Post",
            Platform.WEBSITE: "Blog Article"
        }
        return types.get(platform, "Standard Post")
    
    def _get_platform_strategy(self, platform: Platform) -> str:
        """Get strategy for platform."""
        strategies = {
            Platform.TWITTER: "Hook & Engage",
            Platform.LINKEDIN: "Authority Building",
            Platform.INSTAGRAM: "Visual Storytelling",
            Platform.FACEBOOK: "Community Discussion",
            Platform.WEBSITE: "Complete Information"
        }
        return strategies.get(platform, "Standard Approach")

# Main function to render the UI
def render_content_repurposing_ui():
    """Main function to render the content repurposing UI."""
    ui = ContentRepurposingUI()
    ui.render_repurposing_interface()

# For testing
if __name__ == "__main__":
    render_content_repurposing_ui() 