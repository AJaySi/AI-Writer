import streamlit as st
from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd
from lib.ai_seo_tools.content_calendar.core.content_generator import ContentGenerator
from lib.ai_seo_tools.content_calendar.core.ai_generator import AIGenerator
from lib.ai_seo_tools.content_calendar.integrations.seo_optimizer import SEOOptimizer
from lib.database.models import ContentItem, ContentType, Platform, SEOData
import logging

logger = logging.getLogger('content_calendar.series')

class SeriesManager:
    def __init__(self):
        self.series_data = {}
        if 'content_series' not in st.session_state:
            st.session_state.content_series = {}
        if 'series_relationships' not in st.session_state:
            st.session_state.series_relationships = {}
        if 'series_performance' not in st.session_state:
            st.session_state.series_performance = {}

    def create_series(self, series_id: str, topic: str, num_pieces: int, content_type: ContentType, 
                     platforms: List[Platform], schedule_strategy: str = 'linear', series_type: str = '', series_flow: str = '', metadata: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Create a new content series with tracking and scheduling."""
        try:
            series = {
                'id': series_id,
                'topic': topic,
                'num_pieces': num_pieces,
                'content_type': content_type,
                'platforms': platforms,
                'schedule_strategy': schedule_strategy,
                'series_type': series_type,
                'series_flow': series_flow,
                'pieces': [],
                'performance': {},
                'created_at': datetime.now(),
                'status': 'draft',
                'relationships': {},
                'platform_distribution': {p.name: [] for p in platforms},
                'metadata': metadata
            }
            st.session_state.content_series[series_id] = series
            return series
        except Exception as e:
            logger.error(f"Error creating series: {str(e)}")
            return None

    def add_piece(self, series_id: str, piece: Dict[str, Any]) -> bool:
        """Add a content piece to the series with relationship tracking."""
        try:
            if series_id in st.session_state.content_series:
                series = st.session_state.content_series[series_id]
                piece_id = f"piece_{len(series['pieces'])}"
                
                # Create a structured piece object
                structured_piece = {
                    'id': piece_id,
                    'title': piece.get('title', f"Part {len(series['pieces']) + 1}"),
                    'content': piece.get('content', ''),
                    'platform': piece.get('platform', series['platforms'][0]),
                    'scheduled_date': None,
                    'status': 'draft',
                    'relationships': {
                        'previous': None,
                        'next': None
                    },
                    'performance': {
                        'engagement': 0,
                        'reach': 0,
                        'conversion_rate': 0
                    }
                }
                
                # Track relationships
                if series['pieces']:
                    previous_piece = series['pieces'][-1]
                    structured_piece['relationships']['previous'] = previous_piece['id']
                    structured_piece['relationships']['next'] = piece_id
                
                # Add to platform distribution
                platform_name = structured_piece['platform'].name
                if platform_name in series['platform_distribution']:
                    series['platform_distribution'][platform_name].append(piece_id)
                
                series['pieces'].append(structured_piece)
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding piece to series: {str(e)}")
            return False

    def get_series_performance(self, series_id: str) -> Dict[str, Any]:
        """Get comprehensive performance analytics for a series."""
        try:
            if series_id in st.session_state.content_series:
                series = st.session_state.content_series[series_id]
                performance = {
                    'overall': {
                        'total_engagement': 0,
                        'total_reach': 0,
                        'conversion_rate': 0,
                        'average_engagement': 0
                    },
                    'platforms': {},
                    'pieces': {},
                    'trends': {
                        'engagement': [],
                        'reach': [],
                        'conversions': []
                    }
                }
                
                # Calculate overall metrics
                for piece in series['pieces']:
                    piece_performance = piece.get('performance', {})
                    performance['overall']['total_engagement'] += piece_performance.get('engagement', 0)
                    performance['overall']['total_reach'] += piece_performance.get('reach', 0)
                    performance['overall']['conversion_rate'] += piece_performance.get('conversion_rate', 0)
                    
                    # Track piece-specific performance
                    performance['pieces'][piece['id']] = piece_performance
                    
                    # Track trends
                    performance['trends']['engagement'].append(piece_performance.get('engagement', 0))
                    performance['trends']['reach'].append(piece_performance.get('reach', 0))
                    performance['trends']['conversions'].append(piece_performance.get('conversion_rate', 0))
                
                # Calculate averages
                num_pieces = len(series['pieces'])
                if num_pieces > 0:
                    performance['overall']['average_engagement'] = performance['overall']['total_engagement'] / num_pieces
                    performance['overall']['conversion_rate'] = performance['overall']['conversion_rate'] / num_pieces
                
                # Calculate platform-specific performance
                for platform in series['platforms']:
                    platform_pieces = series['platform_distribution'].get(platform.name, [])
                    platform_performance = {
                        'engagement': 0,
                        'reach': 0,
                        'conversion_rate': 0
                    }
                    
                    for piece_id in platform_pieces:
                        piece_performance = performance['pieces'].get(piece_id, {})
                        platform_performance['engagement'] += piece_performance.get('engagement', 0)
                        platform_performance['reach'] += piece_performance.get('reach', 0)
                        platform_performance['conversion_rate'] += piece_performance.get('conversion_rate', 0)
                    
                    if platform_pieces:
                        platform_performance['engagement'] /= len(platform_pieces)
                        platform_performance['conversion_rate'] /= len(platform_pieces)
                    
                    performance['platforms'][platform.name] = platform_performance
                
                return performance
            return {}
        except Exception as e:
            logger.error(f"Error getting series performance: {str(e)}")
            return {}

    def update_series_status(self, series_id: str, status: str) -> bool:
        """Update the status of a series."""
        try:
            if series_id in st.session_state.content_series:
                st.session_state.content_series[series_id]['status'] = status
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating series status: {str(e)}")
            return False

    def schedule_series(self, series_id: str, start_date: datetime, interval: int = 7) -> bool:
        """Schedule the series content with flexible scheduling strategies."""
        try:
            if series_id in st.session_state.content_series:
                series = st.session_state.content_series[series_id]
                current_date = start_date
                
                for piece in series['pieces']:
                    piece['scheduled_date'] = current_date
                    if series['schedule_strategy'] == 'linear':
                        current_date += timedelta(days=interval)
                    elif series['schedule_strategy'] == 'burst':
                        current_date += timedelta(days=1)
                    elif series['schedule_strategy'] == 'custom':
                        # Custom scheduling is handled by the UI
                        pass
                
                return True
            return False
        except Exception as e:
            logger.error(f"Error scheduling series: {str(e)}")
            return False

def render_content_series_generator(
    ai_generator: AIGenerator,
    content_generator: ContentGenerator,
    seo_optimizer: SEOOptimizer
):
    """Render the content series generator interface."""
    st.header("Content Series Generator")
    
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
        st.info("""
        ## Welcome to Content Series Generator! 📚
        
        Create and manage content series across multiple platforms. Here's what you can do:
        
        ### Features:
        - 📝 **Series Creation**: Generate connected content pieces
        - 🔄 **Cross-Platform Distribution**: Optimize for different platforms
        - 📊 **Series Analytics**: Track performance across the series
        - 📅 **Smart Scheduling**: Plan content distribution
        
        ### Getting Started:
        1. First, add some content to your calendar
        2. Select a topic for your content series
        3. Configure series parameters and platforms
        4. Generate and schedule your series
        
        Ready to get started? Add some content to your calendar first!
        """)
        return
    
    # Series Configuration
    st.subheader("Create New Content Series")
    
    # Show onboarding info if no series exist
    if not st.session_state.get('content_series', {}):
        st.info("""
        ### Content Series Guide
        
        Create engaging content series with these features:
        
        - **Series Planning**: Define your series structure and goals
        - **Content Generation**: Create connected content pieces
        - **Platform Optimization**: Adapt content for each platform
        - **Performance Tracking**: Monitor series success
        
        Fill out the form below to create your first series!
        """)
    
    # Initialize series manager
    series_manager = SeriesManager()
    
    # Series Creation Form
    with st.form("series_creation_form"):
        st.subheader("Create New Series")
        series_topic = st.text_input("Series Topic")
        num_pieces = st.slider("Number of pieces", 2, 10, 3)
        content_type = st.selectbox(
            "Content Type",
            options=[ct.name for ct in ContentType],
            key="series_content_type"
        )
        
        # Multi-platform selection
        platforms = st.multiselect(
            "Target Platforms",
            options=[p.name for p in Platform],
            default=['WEBSITE'],
            key="series_platforms"
        )
        
        # Schedule strategy
        schedule_strategy = st.selectbox(
            "Schedule Strategy",
            options=['linear', 'burst', 'custom'],
            help="Linear: Evenly spaced, Burst: Grouped together, Custom: Manual scheduling"
        )
        
        # Series metadata
        with st.expander("Series Metadata"):
            target_audience = st.text_area("Target Audience")
            series_goals = st.multiselect(
                "Series Goals",
                options=['Awareness', 'Engagement', 'Conversion', 'Education'],
                default=['Awareness']
            )
            series_tone = st.select_slider(
                "Series Tone",
                options=['Professional', 'Casual', 'Friendly', 'Authoritative', 'Conversational'],
                value='Professional'
            )
        
        submitted = st.form_submit_button("Generate Series")
        
        if submitted and series_topic:
            with st.spinner("Generating content series..."):
                try:
                    # Create series
                    series_id = f"series_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    # Prepare metadata with default values
                    metadata = {
                        'tone': series_tone,
                        'length': 'medium',  # Default length
                        'engagement_goal': series_goals[0] if series_goals else 'Awareness',
                        'creativity_level': 'balanced'  # Default creativity level
                    }
                    
                    series = series_manager.create_series(
                        series_id=series_id,
                        topic=series_topic,
                        num_pieces=num_pieces,
                        content_type=ContentType[content_type],
                        platforms=[Platform[p] for p in platforms],
                        schedule_strategy=schedule_strategy,
                        series_type=series_goals[0] if series_goals else 'Awareness',
                        series_flow='sequential',  # Default flow
                        metadata=metadata
                    )
                    
                    if series:
                        # Generate series content
                        series_content = content_generator.generate_content(
                            content_type=ContentType[content_type],
                            topic=series_topic,
                            platforms=[Platform[p] for p in platforms],
                            num_pieces=num_pieces,
                            requirements={
                                'tone': series_tone,
                                'length': metadata['length'],
                                'engagement_goal': metadata['engagement_goal'],
                                'creativity_level': metadata['creativity_level'],
                                'series_type': metadata['engagement_goal'],
                                'series_flow': 'sequential',
                                'target_audience': target_audience
                            }
                        )
                        
                        if series_content:
                            # Add content pieces to series
                            for piece in series_content:
                                series_manager.add_piece(
                                    series_id=series['id'],
                                    piece=piece
                                )
                            
                            # Schedule series
                            if schedule_strategy == 'linear':
                                start_date = st.date_input("Start Date", datetime.now())
                                interval = st.number_input("Days between pieces", min_value=1, value=7)
                                series_manager.schedule_series(
                                    series_id=series['id'],
                                    start_date=start_date,
                                    interval_days=interval
                                )
                            elif schedule_strategy == 'burst':
                                start_date = st.date_input("Start Date", datetime.now())
                                burst_size = st.number_input("Burst Size", min_value=1, value=1)
                                series_manager.schedule_series(
                                    series_id=series['id'],
                                    start_date=start_date,
                                    interval_days=1,
                                    burst_size=burst_size
                                )
                            else:  # custom
                                for i, piece in enumerate(series_manager.series_data[series['id']]['pieces']):
                                    piece['scheduled_date'] = st.date_input(
                                        f"Publish Date for Part {i+1}",
                                        datetime.now() + timedelta(days=i*7)
                                    )
                                
                                if st.button("Save Schedule"):
                                    st.success("Series schedule saved!")
                            
                            st.success(f"Generated {num_pieces} content pieces for series!")
                            
                            # Display series preview
                            with st.expander("Series Preview", expanded=True):
                                for piece in series_manager.series_data[series_id]['pieces']:
                                    st.markdown(f"### Part {piece['part_number']}")
                                    st.json(piece['content'])
                                    
                                    # Platform-specific previews
                                    st.markdown("#### Platform Previews")
                                    for platform in platforms:
                                        with st.expander(f"{platform} Preview"):
                                            st.write(piece['content'].get('platform_previews', {}).get(platform, 'No preview available'))
                            
                            # Series performance tracking
                            st.subheader("Series Performance")
                            performance_data = series_manager.get_series_performance(series_id)
                            if performance_data:
                                st.write("### Overall Performance")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total Engagement", f"{performance_data['overall']['total_engagement']:.1f}%")
                                with col2:
                                    st.metric("Total Reach", f"{performance_data['overall']['total_reach']:,}")
                                with col3:
                                    st.metric("Conversion Rate", f"{performance_data['overall']['conversion_rate']:.1f}%")
                                
                                # Platform-specific performance
                                st.write("### Platform Performance")
                                for platform in platforms:
                                    with st.expander(f"{platform} Performance"):
                                        platform_data = performance_data['platforms'].get(platform, {})
                                        st.write(f"Engagement: {platform_data.get('engagement', 0):.1f}%")
                                        st.write(f"Reach: {platform_data.get('reach', 0):,}")
                                        st.write(f"Conversions: {platform_data.get('conversion_rate', 0):.1f}%")
                                
                                # Performance trends
                                st.write("### Performance Trends")
                                trend_data = performance_data['trends']
                                st.line_chart(pd.DataFrame({
                                    'Engagement': trend_data['engagement'],
                                    'Reach': trend_data['reach'],
                                    'Conversions': trend_data['conversions']
                                }))
                        
                except Exception as e:
                    logger.error(f"Error generating series: {str(e)}", exc_info=True)
                    st.error(f"Error generating series: {str(e)}")

    # Display existing series
    if st.session_state.content_series:
        st.subheader("Existing Series")
        for series_id, series in st.session_state.content_series.items():
            with st.expander(f"Series: {series['topic']}"):
                st.write(f"Status: {series['status']}")
                st.write(f"Pieces: {len(series['pieces'])}")
                st.write(f"Created: {series['created_at']}")
                
                # Series actions
                if st.button(f"View Details", key=f"view_{series_id}"):
                    st.session_state.selected_series = series_id
                
                if st.button(f"Delete Series", key=f"delete_{series_id}"):
                    del st.session_state.content_series[series_id]
                    st.rerun()

def on_series_complete():
    """Handle series completion."""
    try:
        st.session_state.series_complete = True
        st.rerun()
    except Exception as e:
        logger.error(f"Error handling series completion: {str(e)}")
        st.error("An error occurred while completing the series. Please try again.") 