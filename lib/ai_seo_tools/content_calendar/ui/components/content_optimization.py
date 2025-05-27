import streamlit as st
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd
from ...core.content_generator import ContentGenerator
from ...core.ai_generator import AIGenerator
from ...integrations.seo_optimizer import SEOOptimizer
from ...models.calendar import ContentItem, ContentType, Platform, SEOData
import logging

logger = logging.getLogger('content_calendar.optimization')

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
    st.header("Content Optimization")
    
    # Initialize optimization manager
    optimization_manager = OptimizationManager()
    
    # Check if calendar manager is available
    if 'calendar_manager' not in st.session_state:
        st.error("Calendar manager not initialized. Please refresh the page.")
        return
    
    # Get available content
    try:
        available_content = st.session_state.calendar_manager.get_calendar().get_all_content()
        content_options = [item.title for item in available_content]
    except Exception as e:
        logger.error(f"Error getting content options: {str(e)}")
        st.error("Error loading content. Please try again.")
        return
    
    if not content_options:
        st.info("No content available for optimization. Please add some content first.")
        return
    
    # Content Selection
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
                
                # Advanced Optimization Settings
                with st.expander("Advanced Settings", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        tone = st.select_slider(
                            "Content Tone",
                            options=['Professional', 'Casual', 'Friendly', 'Authoritative', 'Conversational'],
                            value='Professional'
                        )
                        length = st.select_slider(
                            "Content Length",
                            options=['Short', 'Medium', 'Long', 'Comprehensive'],
                            value='Medium'
                        )
                    
                    with col2:
                        engagement_goal = st.select_slider(
                            "Engagement Goal",
                            options=['Awareness', 'Consideration', 'Conversion', 'Retention'],
                            value='Consideration'
                        )
                        creativity_level = st.slider(
                            "Creativity Level",
                            min_value=1,
                            max_value=10,
                            value=5
                        )
                
                # Platform-Specific Optimization
                st.subheader("Platform-Specific Optimization")
                platforms = st.multiselect(
                    "Target Platforms",
                    options=[p.name for p in content_item.platforms],
                    default=[p.name for p in content_item.platforms]
                )
                
                # Generate Optimization
                if st.button("Generate Optimization"):
                    with st.spinner("Generating optimization..."):
                        try:
                            # Generate optimized content
                            optimized_content = content_generator.optimize_for_platform(
                                content=content_item,
                                platform=Platform[platforms[0]] if platforms else content_item.platforms[0],
                                requirements={
                                    'tone': tone,
                                    'length': length,
                                    'engagement_goal': engagement_goal,
                                    'creativity_level': creativity_level
                                }
                            )
                            
                            if optimized_content:
                                # Track optimization
                                optimization_manager.track_optimization(
                                    content_item.title,
                                    {
                                        'type': 'content',
                                        'changes': optimized_content.get('changes', []),
                                        'metrics': optimized_content.get('metrics', {}),
                                        'content': optimized_content.get('content', ''),
                                        'engagement_metrics': optimized_content.get('engagement_metrics', {})
                                    }
                                )
                                
                                # Save preview
                                optimization_manager.save_preview(
                                    content_item.title,
                                    {
                                        'original': content_item.description,
                                        'optimized': optimized_content.get('content', ''),
                                        'changes': optimized_content.get('changes', []),
                                        'metrics': optimized_content.get('metrics', {})
                                    }
                                )
                                
                                st.success("Content optimized successfully!")
                        except Exception as e:
                            logger.error(f"Error optimizing content: {str(e)}")
                            st.error(f"Error optimizing content: {str(e)}")
            
            with opt_tabs[1]:
                st.subheader("SEO Optimization")
                
                # SEO Settings
                with st.expander("SEO Settings", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        keyword_density = st.slider(
                            "Target Keyword Density",
                            min_value=1,
                            max_value=5,
                            value=2,
                            help="Target percentage of keywords in content"
                        )
                        internal_linking = st.checkbox(
                            "Enable Internal Linking",
                            value=True,
                            help="Automatically add internal links to related content"
                        )
                    
                    with col2:
                        external_linking = st.checkbox(
                            "Enable External Linking",
                            value=True,
                            help="Add relevant external links for credibility"
                        )
                        structured_data = st.checkbox(
                            "Add Structured Data",
                            value=True,
                            help="Include schema.org structured data"
                        )
                
                # Generate SEO Optimization
                if st.button("Generate SEO Optimization"):
                    with st.spinner("Generating SEO optimization..."):
                        try:
                            # Generate SEO-optimized content
                            seo_optimized = seo_optimizer.optimize_content(
                                content=content_item,
                                content_type=content_item.content_type.name,
                                language='English',
                                search_intent='Informational Intent',
                                settings={
                                    'keyword_density': keyword_density,
                                    'internal_linking': internal_linking,
                                    'external_linking': external_linking,
                                    'structured_data': structured_data
                                }
                            )
                            
                            if seo_optimized:
                                # Track optimization
                                optimization_manager.track_optimization(
                                    content_item.title,
                                    {
                                        'type': 'seo',
                                        'changes': seo_optimized.get('changes', []),
                                        'metrics': seo_optimized.get('metrics', {}),
                                        'seo_data': seo_optimized
                                    }
                                )
                                
                                # Save preview
                                optimization_manager.save_preview(
                                    content_item.title,
                                    {
                                        'meta_description': seo_optimized.get('meta_description', ''),
                                        'keywords': seo_optimized.get('keywords', []),
                                        'structured_data': seo_optimized.get('structured_data', {}),
                                        'changes': seo_optimized.get('changes', [])
                                    }
                                )
                                
                                st.success("SEO optimization completed!")
                        except Exception as e:
                            logger.error(f"Error optimizing SEO: {str(e)}")
                            st.error(f"Error optimizing SEO: {str(e)}")
            
            with opt_tabs[2]:
                st.subheader("Optimization Preview")
                
                preview_data = optimization_manager.get_preview(content_item.title)
                if preview_data:
                    # Content Preview
                    if 'original' in preview_data:
                        st.markdown("### Content Changes")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### Original Content")
                            st.write(preview_data['original'])
                        
                        with col2:
                            st.markdown("#### Optimized Content")
                            st.write(preview_data['optimized'])
                        
                        st.markdown("#### Key Changes")
                        for change in preview_data.get('changes', []):
                            st.write(f"- {change}")
                    
                    # SEO Preview
                    if 'meta_description' in preview_data:
                        st.markdown("### SEO Changes")
                        st.markdown("#### Meta Description")
                        st.write(preview_data['meta_description'])
                        
                        st.markdown("#### Keywords")
                        st.write(", ".join(preview_data['keywords']))
                        
                        st.markdown("#### Structured Data")
                        st.json(preview_data['structured_data'])
                    
                    # Metrics Preview
                    if 'metrics' in preview_data:
                        st.markdown("### Optimization Metrics")
                        metrics = preview_data['metrics']
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Readability Score", f"{metrics.get('readability_score', 0):.1%}")
                        with col2:
                            st.metric("SEO Score", f"{metrics.get('seo_score', 0):.1%}")
                        with col3:
                            st.metric("Engagement Potential", f"{metrics.get('engagement_potential', 0):.1%}")
                else:
                    st.info("No optimization preview available. Generate optimization first.")
            
            with opt_tabs[3]:
                st.subheader("Optimization History")
                
                history = optimization_manager.get_optimization_history(content_item.title)
                if history:
                    for entry in history:
                        with st.expander(f"Optimization at {entry['timestamp']}"):
                            st.write(f"Type: {entry['type']}")
                            st.write("Changes:")
                            for change in entry.get('changes', []):
                                st.write(f"- {change}")
                            
                            if 'metrics' in entry:
                                st.write("Metrics:")
                                st.json(entry['metrics'])
                else:
                    st.info("No optimization history available.")
            
            with opt_tabs[4]:
                st.subheader("Optimization Analytics")
                
                metrics_history = optimization_manager.get_optimization_metrics(content_item.title)
                if metrics_history:
                    # Convert metrics history to DataFrame
                    df = pd.DataFrame(metrics_history)
                    
                    # Plot metrics over time
                    st.line_chart(df[['readability_score', 'seo_score', 'engagement_potential', 'content_quality']])
                    
                    # Display current metrics
                    current_metrics = metrics_history[-1]
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Readability", f"{current_metrics.get('readability_score', 0):.1%}")
                    with col2:
                        st.metric("SEO Score", f"{current_metrics.get('seo_score', 0):.1%}")
                    with col3:
                        st.metric("Engagement", f"{current_metrics.get('engagement_potential', 0):.1%}")
                    with col4:
                        st.metric("Overall Quality", f"{current_metrics.get('content_quality', 0):.1%}")
                    
                    # Display keyword density trend
                    st.subheader("Keyword Density Trend")
                    st.line_chart(df['keyword_density'])
                else:
                    st.info("No optimization metrics available. Generate optimization first.") 