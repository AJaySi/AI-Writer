import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import logging
import sys
import hashlib
from pathlib import Path
from typing import Dict, Any
from .calendar_view import render_calendar_view
from .filters import render_filters
from .add_content_modal import render_add_content_modal
from .ai_suggestions_modal import render_ai_suggestions_modal
from .components.content_optimization import render_content_optimization
from .components.ab_testing import render_ab_testing
from .components.content_series import render_content_series_generator
from .components.performance_insights import render_performance_insights
import json
from lib.content_scheduler.ui.dashboard import run_dashboard as run_scheduler_dashboard

# Add parent directory to path to import existing tools
parent_dir = str(Path(__file__).parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from lib.database.models import ContentItem, ContentType, Platform, get_engine, get_session, init_db
from ..core.calendar_manager import CalendarManager
from ..core.content_generator import ContentGenerator
from ..core.ai_generator import AIGenerator
from ..core.content_brief import ContentBriefGenerator
from ..integrations.seo_optimizer import SEOOptimizer
from lib.integrations.platform_adapters import PlatformAdapter, UnifiedPlatformAdapter

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize DB/session (do this once at app startup)
engine = get_engine()
init_db(engine)
session = get_session(engine)

# Import content repurposing UI with error handling
def render_smart_repurposing_tab():
    """Render the Smart Content Repurposing tab with error handling."""
    try:
        from lib.ai_seo_tools.content_calendar.ui.components.content_repurposing_ui import render_content_repurposing_ui
        render_content_repurposing_ui()
    except ImportError as e:
        st.error(f"Smart Content Repurposing feature is not available: {str(e)}")
        st.info("Please ensure all dependencies are installed correctly.")
    except Exception as e:
        st.error(f"Error loading Smart Content Repurposing: {str(e)}")
        st.info("Please check the logs for more details.")

class ContentCalendarDashboard:
    """Interactive dashboard for content calendar management."""
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.dashboard')
        self.logger.info("Initializing ContentCalendarDashboard")
        self.content_brief_generator = ContentBriefGenerator()
        self.content_generator = ContentGenerator()
        self.ai_generator = AIGenerator()
        self.platform_adapter = UnifiedPlatformAdapter()
        self.seo_optimizer = SEOOptimizer()
        # Initialize session state variables
        if 'ab_test_results' not in st.session_state:
            st.session_state.ab_test_results = {}
        if 'optimization_history' not in st.session_state:
            st.session_state.optimization_history = {}
        if 'calendar_data' not in st.session_state:
            st.session_state.calendar_data = None
        if 'selected_content' not in st.session_state:
            st.session_state.selected_content = None
        if 'view_mode' not in st.session_state:
            st.session_state.view_mode = 'day'
        if 'selected_date' not in st.session_state:
            st.session_state.selected_date = datetime.now()
        self.logger.info("ContentCalendarDashboard initialized successfully")

    def render(self):
        self.logger.info("Starting dashboard render (tabbed UI)")
        try:
            self._inject_custom_css()
            st.title("AI Content Planning")
            st.markdown("""
            Plan, schedule, and manage your content strategy with AI-powered insights. Use the calendar to organize your content and leverage AI tools for optimization.
            """)
            tabs = st.tabs([
                "Content Planning",
                "Content Optimization",
                "🔄 Smart Repurposing",
                "A/B Testing",
                "Content Series",
                "Analytics",
                "Content Scheduling"
            ])
            with tabs[0]:
                icon_map = {
                    'Blog': '📝', 'Website': '🌐', 'Instagram': '📸', 'Twitter': '🐦', 'LinkedIn': '💼', 'Facebook': '📘',
                    'Article': '📄', 'Social Post': '💬', 'Video': '🎬', 'Newsletter': '✉️'
                }
                status_color = {
                    'Draft': '#bdbdbd', 'Scheduled': '#1976d2', 'Published': '#43a047', 'Archived': '#757575'
                }
                calendar_data = self._get_calendar_data()
                def on_edit(row):
                    try:
                        st.session_state.editing_content = row
                        st.rerun()
                    except Exception as e:
                        logger.error(f"Error handling edit action: {str(e)}")
                        st.error("An error occurred while editing content. Please try again.")
                def on_delete(row):
                    try:
                        self._delete_content(row)
                        st.success(f"Successfully deleted content: {row['title']}")
                        st.rerun()
                    except Exception as e:
                        logger.error(f"Error handling delete action: {str(e)}")
                        st.error("An error occurred while deleting content. Please try again.")
                def on_generate(row):
                    st.session_state['show_ai_modal'] = True
                    st.session_state['ai_modal_topic'] = row['title']
                    st.session_state['ai_modal_type'] = str(row['type'])
                    st.session_state['ai_modal_platform'] = str(row['platform'])
                    st.rerun()
                render_calendar_view(
                    calendar_data=calendar_data,
                    icon_map=icon_map,
                    status_color=status_color,
                    on_edit=on_edit,
                    on_delete=on_delete,
                    on_generate=on_generate,
                    get_item_key=self._get_item_key
                )
                st.markdown("---")
                render_filters()
                def handle_add_content(title, platform, content_type, publish_date):
                    self._add_content({
                        'title': title,
                        'platform': platform,
                        'type': content_type,
                        'publish_date': publish_date
                    })
                    st.session_state['show_add_content_dialog'] = False
                    st.success("Content added!")
                    st.rerun()
                def handle_generate_with_ai(title, platform, content_type):
                    st.session_state['show_add_content_dialog'] = False
                    st.session_state['show_ai_modal'] = True
                    st.session_state['ai_modal_topic'] = title
                    st.session_state['ai_modal_type'] = content_type
                    st.session_state['ai_modal_platform'] = platform
                render_add_content_modal(
                    selected_date=st.session_state.selected_date,
                    on_add_content=handle_add_content,
                    on_generate_with_ai=handle_generate_with_ai
                )
                if st.session_state.get('show_ai_modal', False):
                    st.markdown("### AI Content Suggestions")
                    with st.container():
                        render_ai_suggestions_modal(
                            generate_ai_suggestions=self._generate_ai_suggestions,
                            on_create_brief=self._create_content_brief,
                            on_schedule=self._schedule_content,
                            on_refine=self._refine_suggestion,
                            on_customize=self._customize_suggestion
                        )
                        if st.button("Close"):
                            st.session_state['show_ai_modal'] = False
            with tabs[1]:
                render_content_optimization(
                    content_generator=self.content_generator,
                    ai_generator=self.ai_generator,
                    seo_optimizer=self.seo_optimizer
                )
            with tabs[2]:
                render_smart_repurposing_tab()
            with tabs[3]:
                render_ab_testing(self.content_generator, None)
            with tabs[4]:
                render_content_series_generator(
                    self.ai_generator,
                    self.content_generator,
                    self.seo_optimizer
                )
            with tabs[5]:
                st.header("Analytics")
                st.markdown("### Performance Insights")
                all_content = session.query(ContentItem).all()
                selected_content = st.selectbox(
                    "Select content to analyze",
                    options=[item.title for item in all_content],
                    key="analytics_content_select"
                )
                if selected_content:
                    content_item = next(
                        item for item in all_content
                        if item.title == selected_content
                    )
                    render_performance_insights(content_item, self.platform_adapter)
                st.markdown("### Optimization History")
                if selected_content in st.session_state.optimization_history:
                    st.json(st.session_state.optimization_history[selected_content])
            with tabs[6]:
                run_scheduler_dashboard()
            self.logger.info("Dashboard render completed successfully (tabbed UI)")
        except Exception as e:
            self.logger.error(f"Error rendering dashboard: {str(e)}", exc_info=True)
            st.error(f"An error occurred: {str(e)}")

    def _inject_custom_css(self):
        st.markdown("""
            <style>
            /* Add your custom CSS here if needed */
            </style>
        """, unsafe_allow_html=True)

    def _get_calendar_data(self):
        self.logger.info("_get_calendar_data called")
        try:
            all_content = session.query(ContentItem).all()
            data = []
            for item in all_content:
                data.append({
                    'date': item.publish_date,
                    'title': item.title,
                    'platform': item.platforms[0] if item.platforms else 'Unknown',
                    'type': item.content_type.value if hasattr(item.content_type, 'value') else str(item.content_type),
                    'status': item.status
                })
            df = pd.DataFrame(data) if data else None
            return df
        except Exception as e:
            self.logger.error(f"Error loading calendar data: {str(e)}", exc_info=True)
            st.error(f"Error loading calendar data: {str(e)}")
            return None

    def _add_content(self, content):
        platform_map = {
            'Blog': Platform.WEBSITE,
            'Instagram': Platform.INSTAGRAM,
            'Twitter': Platform.TWITTER,
            'LinkedIn': Platform.LINKEDIN,
            'Facebook': Platform.FACEBOOK,
        }
        platform_enum = platform_map.get(content['platform'], Platform.WEBSITE)
        content_type_map = {
            'Article': ContentType.BLOG_POST,
            'Social Post': ContentType.SOCIAL_MEDIA,
            'Video': ContentType.VIDEO,
            'Newsletter': ContentType.NEWSLETTER,
        }
        content_type_enum = content_type_map.get(content['type'], ContentType.BLOG_POST)
        new_item = ContentItem(
            title=content['title'],
            description="",
            content_type=content_type_enum,
            platforms=[platform_enum.value],
            publish_date=pd.to_datetime(content['publish_date']),
            status=content.get('status', 'Draft'),
            author=None,
            tags=[],
            notes=None,
            seo_data={}
        )
        session.add(new_item)
        session.commit()

    def _delete_content(self, row):
        # Find by title and publish_date (could be improved with unique IDs)
        all_content = session.query(ContentItem).all()
        for item in all_content:
            if (item.title == row['title'] and
                str(item.publish_date.date()) == str(row['date'].date()) and
                (item.platforms[0] if item.platforms else 'Unknown') == str(row['platform']) and
                (item.content_type.value if hasattr(item.content_type, 'value') else str(item.content_type)) == str(row['type'])):
                session.delete(item)
                session.commit()
                break

    def _edit_content(self, row, new_title, new_platform, new_type, new_status):
        self._delete_content(row)
        self._add_content({
            'title': new_title,
            'platform': new_platform,
            'type': new_type,
            'publish_date': row['date'],
            'status': new_status
        })

    def _get_item_key(self, row):
        key_str = f"{row['title']}_{row['date']}_{row['platform']}_{row['type']}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _generate_ai_suggestions(self, content_type, topic, audience, goals, tone, length, model_settings, style_preferences, seo_preferences, platform_settings):
        """Generate AI content suggestions based on input parameters."""
        try:
            self.logger.info(f"Generating AI suggestions for topic: {topic}")
            
            # Map content type string to ContentType enum
            content_type_map = {
                'Blog Post': ContentType.BLOG_POST,
                'Social Media Post': ContentType.SOCIAL_MEDIA,
                'Video': ContentType.VIDEO,
                'Newsletter': ContentType.NEWSLETTER,
                'Article': ContentType.BLOG_POST,
                'Social Post': ContentType.SOCIAL_MEDIA
            }
            content_type_enum = content_type_map.get(content_type, ContentType.BLOG_POST)
            
            # Map platform string to Platform enum
            platform_map = {
                'Blog': Platform.WEBSITE,
                'Instagram': Platform.INSTAGRAM,
                'Twitter': Platform.TWITTER,
                'LinkedIn': Platform.LINKEDIN,
                'Facebook': Platform.FACEBOOK,
                'Website': Platform.WEBSITE
            }
            platform = st.session_state.get('ai_modal_platform', 'Blog')
            platform_enum = platform_map.get(platform, Platform.WEBSITE)
            
            # Create a content item for the suggestion
            content_item = ContentItem(
                title=topic,
                description="",
                content_type=content_type_enum,
                platforms=[platform_enum],
                publish_date=datetime.now(),
                seo_data=SEOData(
                    title=topic,
                    meta_description="",
                    keywords=[],
                    structured_data={}
                ),
                status='Draft'
            )
            
            # Use AIGenerator to generate suggestions
            suggestions = self.ai_generator.generate_ai_suggestions(
                content_type=content_type_enum,
                topic=topic,
                audience=audience,
                goals=goals,
                tone=tone,
                length=length,
                model_settings=model_settings,
                style_preferences=style_preferences,
                seo_preferences=seo_preferences,
                platform_settings=platform_settings,
                platform=platform_enum
            )
            
            if not suggestions:
                self.logger.warning("No suggestions generated")
                return []
            
            # Format suggestions
            formatted_suggestions = []
            for suggestion in suggestions:
                formatted_suggestion = {
                    'title': suggestion.get('title', topic),
                    'type': content_type,
                    'platform': platform,
                    'audience': audience,
                    'impact': f"High impact for {', '.join(goals)}",
                    'preview': suggestion.get('preview', ''),
                    'style_elements': [
                        f"Tone: {tone}",
                        f"Length: {length}",
                        f"Creativity: {model_settings.get('Creativity Level', 'balanced')}",
                        f"Formality: {model_settings.get('Formality Level', 'professional')}"
                    ],
                    'seo_elements': [
                        f"Keyword Density: {seo_preferences.get('Keyword Density', '2')}%",
                        "Internal Linking: Enabled" if seo_preferences.get('Internal Linking', True) else "Internal Linking: Disabled",
                        "External Linking: Enabled" if seo_preferences.get('External Linking', True) else "External Linking: Disabled"
                    ],
                    'engagement_score': f"{85 + len(formatted_suggestions)*5}%",
                    'reach': 'High',
                    'conversion': f"{3.5 + len(formatted_suggestions)*0.5}%",
                    'seo_impact': 'Strong',
                    'platform_optimizations': suggestion.get('platform_optimizations', []),
                    'variations': suggestion.get('variations', [
                        "Alternative headline",
                        "Different content angle",
                        "Alternative format"
                    ]),
                    'seo_recommendations': suggestion.get('seo_elements', []),
                    'media_suggestions': suggestion.get('media_suggestions', [
                        "Featured image",
                        "Supporting graphics",
                        "Social media visuals"
                    ])
                }
                formatted_suggestions.append(formatted_suggestion)
            
            self.logger.info(f"Generated {len(formatted_suggestions)} suggestions successfully")
            return formatted_suggestions
            
        except Exception as e:
            self.logger.error(f"Error generating AI suggestions: {str(e)}", exc_info=True)
            st.error(f"Error generating suggestions: {str(e)}")
            return []

    def _create_content_brief(self, content_item: ContentItem) -> Dict[str, Any]:
        """Create a detailed content brief for the given content item."""
        try:
            self.logger.info(f"Creating content brief for: {content_item.title}")
            
            # Generate content brief using the content brief generator
            brief = self.content_brief_generator.generate_brief(
                content_item=content_item,
                target_audience={
                    'audience': content_item.description,
                    'goals': ['engage', 'inform', 'convert']
                }
            )
            
            # Enhance brief with SEO data
            if brief and 'content_flow' in brief:
                brief['seo_optimization'] = {
                    'meta_description': self.seo_optimizer.generate_meta_description(
                        brief['content_flow'].get('introduction', {}).get('summary', '')
                    ),
                    'keywords': self.seo_optimizer.extract_keywords(
                        brief['content_flow'].get('introduction', {}).get('summary', '')
                    ),
                    'structured_data': self.seo_optimizer.generate_structured_data(
                        content_item.content_type
                    )
                }
            
            self.logger.info(f"Content brief created successfully for: {content_item.title}")
            return brief
            
        except Exception as e:
            self.logger.error(f"Error creating content brief: {str(e)}", exc_info=True)
            st.error(f"Error creating content brief: {str(e)}")
            return {}

    def _schedule_content(self, content_item: ContentItem, publish_date: datetime) -> bool:
        """Schedule content for publishing on the specified date."""
        try:
            self.logger.info(f"Scheduling content: {content_item.title} for {publish_date}")
            
            # Get the calendar
            calendar = self.calendar_manager.get_calendar()
            if not calendar:
                raise ValueError("No calendar found")
            
            # Update the publish date
            content_item.publish_date = publish_date
            
            # Add to calendar
            calendar.add_content(content_item)
            
            # Save changes
            self.calendar_manager.save_calendar_to_json()
            
            self.logger.info(f"Content scheduled successfully: {content_item.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error scheduling content: {str(e)}", exc_info=True)
            st.error(f"Error scheduling content: {str(e)}")
            return False

    def _refine_suggestion(self, suggestion: Dict[str, Any], feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Refine an AI-generated suggestion based on user feedback."""
        try:
            self.logger.info("Refining AI suggestion based on feedback")
            
            # Update suggestion based on feedback
            if 'tone' in feedback:
                suggestion['style_elements'] = [
                    f"Tone: {feedback['tone']}",
                    *[elem for elem in suggestion['style_elements'] if not elem.startswith('Tone:')]
                ]
            
            if 'length' in feedback:
                suggestion['style_elements'] = [
                    f"Length: {feedback['length']}",
                    *[elem for elem in suggestion['style_elements'] if not elem.startswith('Length:')]
                ]
            
            if 'keywords' in feedback:
                suggestion['seo_elements'] = [
                    f"Keywords: {', '.join(feedback['keywords'])}",
                    *[elem for elem in suggestion['seo_elements'] if not elem.startswith('Keywords:')]
                ]
            
            # Regenerate content with refined parameters
            refined_content = self.content_brief_generator.generate_brief(
                content_item=ContentItem(
                    title=suggestion['title'],
                    description="",
                    content_type=ContentType[suggestion['type'].upper().replace(' ', '_')],
                    platforms=[Platform[suggestion['platform'].upper()]],
                    publish_date=datetime.now(),
                    seo_data=SEOData(
                        title=suggestion['title'],
                        meta_description="",
                        keywords=feedback.get('keywords', []),
                        structured_data={}
                    ),
                    status='Draft'
                ),
                target_audience={
                    'audience': suggestion['audience'],
                    'goals': feedback.get('goals', ['engage', 'inform']),
                    'preferences': {
                        'tone': feedback.get('tone', 'professional'),
                        'length': feedback.get('length', 'medium')
                    }
                }
            )
            
            if refined_content:
                suggestion['preview'] = refined_content.get('content_flow', {}).get('introduction', {}).get('summary', '')
            
            self.logger.info("Suggestion refined successfully")
            return suggestion
            
        except Exception as e:
            self.logger.error(f"Error refining suggestion: {str(e)}", exc_info=True)
            st.error(f"Error refining suggestion: {str(e)}")
            return suggestion

    def _customize_suggestion(self, suggestion: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Customize an AI-generated suggestion with specific requirements."""
        try:
            self.logger.info("Customizing AI suggestion")
            
            # Apply customizations
            if 'title' in customizations:
                suggestion['title'] = customizations['title']
            
            if 'platform' in customizations:
                suggestion['platform'] = customizations['platform']
            
            if 'style' in customizations:
                suggestion['style_elements'] = [
                    f"Tone: {customizations['style'].get('tone', 'professional')}",
                    f"Length: {customizations['style'].get('length', 'medium')}",
                    f"Creativity: {customizations['style'].get('creativity', 'balanced')}",
                    f"Formality: {customizations['style'].get('formality', 'professional')}"
                ]
            
            if 'seo' in customizations:
                suggestion['seo_elements'] = [
                    f"Keyword Density: {customizations['seo'].get('keyword_density', '2')}%",
                    "Internal Linking: Enabled" if customizations['seo'].get('internal_linking', True) else "Internal Linking: Disabled",
                    "External Linking: Enabled" if customizations['seo'].get('external_linking', True) else "External Linking: Disabled"
                ]
            
            # Regenerate content with customizations
            customized_content = self.content_brief_generator.generate_brief(
                content_item=ContentItem(
                    title=suggestion['title'],
                    description="",
                    content_type=ContentType[suggestion['type'].upper().replace(' ', '_')],
                    platforms=[Platform[suggestion['platform'].upper()]],
                    publish_date=datetime.now(),
                    seo_data=SEOData(
                        title=suggestion['title'],
                        meta_description="",
                        keywords=customizations.get('seo', {}).get('keywords', []),
                        structured_data={}
                    ),
                    status='Draft'
                ),
                target_audience={
                    'audience': suggestion['audience'],
                    'goals': customizations.get('goals', ['engage', 'inform']),
                    'preferences': customizations.get('style', {})
                }
            )
            
            if customized_content:
                suggestion['preview'] = customized_content.get('content_flow', {}).get('introduction', {}).get('summary', '')
            
            self.logger.info("Suggestion customized successfully")
            return suggestion
            
        except Exception as e:
            self.logger.error(f"Error customizing suggestion: {str(e)}", exc_info=True)
            st.error(f"Error customizing suggestion: {str(e)}")
            return suggestion

    def _optimize_content_for_platform(self, content_item: ContentItem, platform: Platform) -> Dict[str, Any]:
        """Optimize content specifically for a target platform."""
        try:
            self.logger.info(f"Optimizing content for {platform.name}: {content_item.title}")
            
            # Get platform-specific requirements
            platform_requirements = self.platform_adapter.get_platform_requirements(platform)
            
            # Generate platform-optimized content
            optimized_content = self.content_generator.optimize_for_platform(
                content=content_item,
                platform=platform,
                requirements=platform_requirements
            )
            
            if not optimized_content:
                raise ValueError(f"Failed to optimize content for {platform.name}")
            
            # Enhance with AI
            ai_enhanced = self.ai_generator.enhance_for_platform(
                content=optimized_content,
                platform=platform,
                enhancement_type='platform_specific'
            )
            
            if ai_enhanced:
                optimized_content.update(ai_enhanced)
            
            # Track optimization history
            if content_item.title not in st.session_state.optimization_history:
                st.session_state.optimization_history[content_item.title] = []
            st.session_state.optimization_history[content_item.title].append({
                'platform': platform.name,
                'timestamp': datetime.now(),
                'changes': optimized_content.get('changes', [])
            })
            
            self.logger.info(f"Content optimized successfully for {platform.name}")
            return optimized_content
            
        except Exception as e:
            self.logger.error(f"Error optimizing content: {str(e)}", exc_info=True)
            st.error(f"Error optimizing content: {str(e)}")
            return {}

if __name__ == "__main__":
    dashboard = ContentCalendarDashboard()
    dashboard.render() 