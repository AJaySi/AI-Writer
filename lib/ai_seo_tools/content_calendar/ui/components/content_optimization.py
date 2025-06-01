import streamlit as st
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd
from lib.ai_seo_tools.content_calendar.core.content_generator import ContentGenerator
from lib.ai_seo_tools.content_calendar.core.ai_generator import AIGenerator
from lib.ai_seo_tools.content_calendar.integrations.seo_optimizer import SEOOptimizer
from lib.database.models import ContentItem, ContentType, Platform, SEOData
import logging
from lib.database.models import get_engine, get_session, init_db

logger = logging.getLogger('content_calendar.optimization')

engine = get_engine()
init_db(engine)
session = get_session(engine)

class OptimizationManager:
    def __init__(self):
        if 'optimization_history' not in st.session_state:
            st.session_state.optimization_history = {}
        if 'optimization_previews' not in st.session_state:
            st.session_state.optimization_previews = {}
        if 'optimization_metrics' not in st.session_state:
            st.session_state.optimization_metrics = {}

    def track_optimization(self, content_id: str, optimization_data: Dict[str, Any]) -> bool:
        """Track optimization changes for content with detailed metrics."""
        try:
            if content_id not in st.session_state.optimization_history:
                st.session_state.optimization_history[content_id] = []
            
            optimization_data['timestamp'] = datetime.now()
            optimization_data['metrics'] = self._calculate_optimization_metrics(optimization_data)
            st.session_state.optimization_history[content_id].append(optimization_data)
            
            # Update metrics
            if content_id not in st.session_state.optimization_metrics:
                st.session_state.optimization_metrics[content_id] = []
            st.session_state.optimization_metrics[content_id].append(optimization_data['metrics'])
            
            return True
        except Exception as e:
            logger.error(f"Error tracking optimization: {str(e)}")
            return False

    def _calculate_optimization_metrics(self, optimization_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed optimization metrics."""
        try:
            metrics = {
                'readability_score': 0,
                'seo_score': 0,
                'engagement_potential': 0,
                'keyword_density': 0,
                'content_quality': 0
            }
            
            # Calculate readability score
            if 'content' in optimization_data:
                content = optimization_data['content']
                metrics['readability_score'] = self._calculate_readability(content)
            
            # Calculate SEO score
            if 'seo_data' in optimization_data:
                seo_data = optimization_data['seo_data']
                metrics['seo_score'] = self._calculate_seo_score(seo_data)
                metrics['keyword_density'] = self._calculate_keyword_density(seo_data)
            
            # Calculate engagement potential
            if 'engagement_metrics' in optimization_data:
                engagement = optimization_data['engagement_metrics']
                metrics['engagement_potential'] = self._calculate_engagement_potential(engagement)
            
            # Calculate overall content quality
            metrics['content_quality'] = (
                metrics['readability_score'] * 0.3 +
                metrics['seo_score'] * 0.3 +
                metrics['engagement_potential'] * 0.4
            )
            
            return metrics
        except Exception as e:
            logger.error(f"Error calculating optimization metrics: {str(e)}")
            return {}

    def _calculate_readability(self, content: str) -> float:
        """Calculate content readability score."""
        try:
            # Implement readability calculation logic
            # This is a placeholder implementation
            return 0.8
        except Exception as e:
            logger.error(f"Error calculating readability: {str(e)}")
            return 0.0

    def _calculate_seo_score(self, seo_data: SEOData) -> float:
        """Calculate SEO optimization score."""
        try:
            # Implement SEO score calculation logic
            # This is a placeholder implementation
            return 0.85
        except Exception as e:
            logger.error(f"Error calculating SEO score: {str(e)}")
            return 0.0

    def _calculate_keyword_density(self, seo_data: SEOData) -> float:
        """Calculate keyword density."""
        try:
            # Implement keyword density calculation logic
            # This is a placeholder implementation
            return 2.5
        except Exception as e:
            logger.error(f"Error calculating keyword density: {str(e)}")
            return 0.0

    def _calculate_engagement_potential(self, engagement: Dict[str, Any]) -> float:
        """Calculate content engagement potential."""
        try:
            # Implement engagement potential calculation logic
            # This is a placeholder implementation
            return 0.75
        except Exception as e:
            logger.error(f"Error calculating engagement potential: {str(e)}")
            return 0.0

    def get_optimization_history(self, content_id: str) -> List[Dict[str, Any]]:
        """Get detailed optimization history for content."""
        return st.session_state.optimization_history.get(content_id, [])

    def get_optimization_metrics(self, content_id: str) -> List[Dict[str, Any]]:
        """Get optimization metrics history."""
        return st.session_state.optimization_metrics.get(content_id, [])

    def save_preview(self, content_id: str, preview_data: Dict[str, Any]) -> bool:
        """Save optimization preview with versioning."""
        try:
            if content_id not in st.session_state.optimization_previews:
                st.session_state.optimization_previews[content_id] = []
            
            preview_data['version'] = len(st.session_state.optimization_previews[content_id]) + 1
            preview_data['timestamp'] = datetime.now()
            st.session_state.optimization_previews[content_id].append(preview_data)
            return True
        except Exception as e:
            logger.error(f"Error saving preview: {str(e)}")
            return False

    def get_preview(self, content_id: str, version: int = None) -> Dict[str, Any]:
        """Get optimization preview with optional versioning."""
        try:
            previews = st.session_state.optimization_previews.get(content_id, [])
            if not previews:
                return {}
            
            if version is None:
                return previews[-1]
            
            for preview in previews:
                if preview['version'] == version:
                    return preview
            
            return {}
        except Exception as e:
            logger.error(f"Error getting preview: {str(e)}")
            return {}

def render_content_optimization(
    content_generator: ContentGenerator,
    ai_generator: AIGenerator,
    seo_optimizer: SEOOptimizer
):
    """Render the content optimization interface with advanced features."""
    st.title("Content Calendar")
    
    # Initialize optimization manager
    optimization_manager = OptimizationManager()
    
    # Check if calendar manager is available
    if 'calendar_manager' not in st.session_state:
        st.error("Calendar manager not initialized. Please refresh the page.")
        return

    # Create main tabs
    main_tabs = st.tabs(["Content Planning", "Content Optimization"])
    
    with main_tabs[0]:
        # Create two columns for the layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("Quick Calendar Generation")
            st.markdown("""
            Generate a content calendar in three simple steps:
            1. Enter your keywords
            2. Select target platforms
            3. Choose time period
            """)
            
            # Step 1: Keywords Input
            st.subheader("Step 1: Enter Keywords")
            keywords = st.text_area(
                "Enter keywords or topics (one per line)",
                help="Enter the main topics or keywords you want to create content about"
            )
            
            # Step 2: Platform Selection
            st.subheader("Step 2: Select Target Platforms")
            platform_categories = {
                "Website": ["WEBSITE"],
                "Social Media": ["INSTAGRAM", "FACEBOOK", "TWITTER", "LINKEDIN"],
                "Video": ["YOUTUBE"],
                "Newsletter": ["NEWSLETTER"]
            }
            
            selected_platforms = []
            for category, platforms in platform_categories.items():
                st.markdown(f"**{category}**")
                for platform in platforms:
                    if st.checkbox(platform.replace("_", " ").title(), key=f"platform_{platform}"):
                        selected_platforms.append(platform)
            
            # Step 3: Time Period
            st.subheader("Step 3: Choose Time Period")
            time_period = st.selectbox(
                "Select time period",
                ["1 Week", "2 Weeks", "1 Month", "3 Months", "6 Months"],
                help="Choose how far ahead you want to plan your content"
            )
            
            # Generate Calendar Button
            if st.button("Generate with AI", type="primary"):
                if not keywords or not selected_platforms:
                    st.error("Please enter keywords and select at least one platform.")
                else:
                    with st.spinner("Generating content calendar..."):
                        try:
                            # Generate content ideas based on keywords
                            content_ideas = []
                            for keyword in keywords.split('\n'):
                                if keyword.strip():
                                    # Generate content ideas for each platform
                                    for platform in selected_platforms:
                                        try:
                                            # Create a content item for the AI generator
                                            content_item = ContentItem(
                                                title=keyword.strip(),
                                                description=f"Content about {keyword.strip()}",
                                                content_type=ContentType.BLOG_POST if platform == "WEBSITE" else ContentType.SOCIAL_MEDIA,
                                                platforms=[Platform[platform]],
                                                publish_date=datetime.now(),
                                                seo_data=SEOData(
                                                    title=keyword.strip(),
                                                    meta_description=f"Content about {keyword.strip()}",
                                                    keywords=[keyword.strip()],
                                                    structured_data={}
                                                )
                                            )
                                            
                                            # Generate content using AI generator
                                            content_idea = ai_generator.enhance_content(
                                                content=content_item,
                                                enhancement_type='content_generation',
                                                target_audience={
                                                    'content_settings': {
                                                        'tone': 'professional',
                                                        'length': 'medium',
                                                        'engagement_goal': 'awareness',
                                                        'creativity_level': 5
                                                    }
                                                }
                                            )
                                            
                                            if content_idea:
                                                content_ideas.append({
                                                    'title': content_idea.get('title', keyword.strip()),
                                                    'introduction': content_idea.get('content', f"Content about {keyword.strip()}"),
                                                    'platform': platform,
                                                    'meta_description': content_idea.get('meta_description', ''),
                                                    'keywords': [keyword.strip()]
                                                })
                                        except Exception as e:
                                            logger.error(f"Error generating content for {keyword} on {platform}: {str(e)}")
                                            continue
                            
                            if content_ideas:
                                # Create calendar entries
                                calendar = st.session_state.calendar_manager.get_calendar()
                                for idea in content_ideas:
                                    try:
                                        # Create content item
                                        content_item = ContentItem(
                                            title=idea['title'],
                                            description=idea['introduction'],
                                            content_type=ContentType.BLOG_POST if idea['platform'] == "WEBSITE" else ContentType.SOCIAL_MEDIA,
                                            platforms=[Platform[idea['platform']]],
                                            publish_date=datetime.now(),
                                            seo_data=SEOData(
                                                title=idea['title'],
                                                meta_description=idea.get('meta_description', ''),
                                                keywords=idea.get('keywords', []),
                                                structured_data={}
                                            )
                                        )
                                        calendar.add_content(content_item)
                                    except Exception as e:
                                        logger.error(f"Error adding content to calendar: {str(e)}")
                                        continue
                                
                                st.success("Content calendar generated successfully!")
                                st.rerun()  # Refresh to show new content
                            else:
                                st.error("Failed to generate any content ideas. Please try different keywords or settings.")
                        except Exception as e:
                            logger.error(f"Error generating content calendar: {str(e)}")
                            st.error("An error occurred while generating the content calendar. Please try again.")
        
        with col2:
            st.header("Scheduled Content")
            # Get all content from calendar
            calendar = st.session_state.calendar_manager.get_calendar()
            if not calendar:
                st.info("No content scheduled yet. Generate content using the form on the left.")
            else:
                # Group content by platform
                platform_content = {}
                for item in calendar.get_all_content():
                    platform = item.platforms[0].name if item.platforms else "Unknown"
                    if platform not in platform_content:
                        platform_content[platform] = []
                    platform_content[platform].append(item)
                
                # Create tabs for each platform
                platform_tabs = st.tabs(list(platform_content.keys()))
                
                for i, (platform, content) in enumerate(platform_content.items()):
                    with platform_tabs[i]:
                        st.write(f"### {platform} Content")
                        
                        # Convert content to DataFrame for better display
                        content_data = []
                        for item in content:
                            content_data.append({
                                'Date': item.publish_date.strftime('%Y-%m-%d'),
                                'Title': item.title,
                                'Type': item.content_type.name,
                                'Status': item.status
                            })
                        
                        if content_data:
                            df = pd.DataFrame(content_data)
                            st.dataframe(df, use_container_width=True)
                            
                            # Add action buttons for each content item
                            for item in content:
                                with st.expander(f"Actions for: {item.title}"):
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        if st.button("Edit", key=f"edit_{item.title}"):
                                            st.session_state.selected_content = item.title
                                    with col2:
                                        if st.button("Optimize", key=f"optimize_{item.title}"):
                                            st.session_state.selected_content = item.title
                                            st.session_state.active_tab = "Content Optimization"
                                    with col3:
                                        if st.button("Delete", key=f"delete_{item.title}"):
                                            calendar.remove_content(item)
                                            st.success(f"Removed {item.title}")
                                            st.rerun()
    
    with main_tabs[1]:
        st.header("Content Optimization")
        # Get available content
        calendar = st.session_state.calendar_manager.get_calendar()
        if not calendar:
            st.info("No content available for optimization. Use the Content Planning tab to generate content.")
            return
        
        available_content = calendar.get_all_content()
        content_options = [item.title for item in available_content]
        
        # Content selection
        selected_content = st.selectbox(
            "Select content to optimize",
            options=content_options,
            key="optimize_content_select"
        )
        
        if selected_content:
            try:
                content_item = next(
                    item for item in available_content
                    if item.title == selected_content
                )
                
                # Create tabs for different optimization aspects
                opt_tabs = st.tabs(["Content Optimization", "SEO Optimization", "Preview", "History", "Analytics"])
                
                with opt_tabs[0]:
                    st.subheader("Content Optimization")
                    
                    # Show onboarding info if no optimization history
                    if not optimization_manager.get_optimization_history(content_item.title):
                        st.info("""
                        ### Content Optimization Guide
                        
                        Use these tools to enhance your content:
                        
                        - **Content Tone**: Adjust the writing style to match your brand voice
                        - **Content Length**: Optimize for your target platform's requirements
                        - **Engagement Goal**: Focus on specific audience actions
                        - **Creativity Level**: Balance between creative and professional content
                        
                        Click 'Generate Optimization' to get started!
                        """)
                    
                    # Advanced Optimization Settings
                    col1, col2 = st.columns(2)
                    with col1:
                        tone = st.select_slider(
                            "Content Tone",
                            options=["Professional", "Casual", "Educational", "Entertaining", "Persuasive"],
                            value="Professional"
                        )
                        length = st.radio(
                            "Content Length",
                            ["Short", "Medium", "Long"],
                            horizontal=True
                        )
                    with col2:
                        engagement_goal = st.selectbox(
                            "Engagement Goal",
                            ["Awareness", "Consideration", "Conversion", "Retention"]
                        )
                        creativity_level = st.slider(
                            "Creativity Level",
                            min_value=1,
                            max_value=10,
                            value=5
                        )
                    
                    if st.button("Generate Optimization", type="primary"):
                        with st.spinner("Optimizing content..."):
                            try:
                                # Generate optimization
                                optimization = content_generator.optimize_content(
                                    content=content_item,
                                    tone=tone,
                                    length=length,
                                    engagement_goal=engagement_goal,
                                    creativity_level=creativity_level
                                )
                                
                                if optimization:
                                    st.success("Content optimized successfully!")
                                    
                                    # Show optimization results
                                    st.subheader("Optimization Results")
                                    st.write(optimization.get('content', ''))
                                    
                                    # Save optimization history
                                    optimization_manager.track_optimization(
                                        content_item.title,
                                        {
                                            'tone': tone,
                                            'length': length,
                                            'engagement_goal': engagement_goal,
                                            'creativity_level': creativity_level,
                                            'content': optimization.get('content', ''),
                                            'timestamp': datetime.now()
                                        }
                                    )
                                else:
                                    st.error("Failed to optimize content. Please try again.")
                            except Exception as e:
                                logger.error(f"Error optimizing content: {str(e)}")
                                st.error("An error occurred while optimizing content. Please try again.")
                
                with opt_tabs[1]:
                    st.subheader("SEO Optimization")
                    # SEO optimization content here
                
                with opt_tabs[2]:
                    st.subheader("Content Preview")
                    # Content preview here
                
                with opt_tabs[3]:
                    st.subheader("Optimization History")
                    # Optimization history here
                
                with opt_tabs[4]:
                    st.subheader("Performance Analytics")
                    # Analytics content here
                    
            except Exception as e:
                logger.error(f"Error processing selected content: {str(e)}")
                st.error("Error processing selected content. Please try again.")

# Remove everything after this point 