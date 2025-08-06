import streamlit as st
from typing import Dict, Any, List
from lib.database.models import ContentItem
import logging
from lib.ai_seo_tools.content_calendar.core.content_generator import ContentGenerator
from lib.ai_seo_tools.content_calendar.core.calendar_manager import CalendarManager

logger = logging.getLogger(__name__)

def render_ab_testing(content_generator: ContentGenerator, calendar_manager: CalendarManager):
    """Render the A/B testing interface."""
    st.header("A/B Testing")
    
    # Check if calendar manager is available
    if 'calendar_manager' not in st.session_state:
        st.error("Calendar manager not initialized. Please refresh the page.")
        return
    
    # Get available content
    try:
        available_content = calendar_manager.get_calendar().get_all_content()
        content_options = [item.title for item in available_content]
    except Exception as e:
        logger.error(f"Error getting content options: {str(e)}")
        st.error("Error loading content. Please try again.")
        return
    
    if not content_options:
        st.info("""
        ## Welcome to A/B Testing! 🧪
        
        Test different versions of your content to find what works best. Here's what you can do:
        
        ### Features:
        - 🔄 **Variant Generation**: Create multiple versions of your content
        - 📊 **Performance Tracking**: Compare metrics across variants
        - 📈 **Statistical Analysis**: Get data-driven insights
        - 🎯 **Winner Selection**: Identify the best performing content
        
        ### Getting Started:
        1. First, add some content to your calendar
        2. Select the content you want to test
        3. Generate variants with different parameters
        4. Track performance and analyze results
        
        Ready to get started? Add some content to your calendar first!
        """)
        return
    
    # Content Selection
    selected_content = st.selectbox(
        "Select content to test",
        options=content_options,
        key="ab_test_content_select"
    )
    
    if selected_content:
        try:
            content_item = next(
                item for item in available_content
                if item.title == selected_content
            )
            
            # Show onboarding info if no test history
            if not st.session_state.get('ab_test_results', {}).get(content_item.title):
                st.info("""
                ### A/B Testing Guide
                
                Create and compare different versions of your content:
                
                - **Headline Variations**: Test different titles and hooks
                - **Content Structure**: Try different content flows
                - **Call-to-Action**: Test various CTAs
                - **Visual Elements**: Compare different media placements
                
                Click 'Generate Test Variants' to get started!
                """)
            
            # Test Configuration
            st.markdown("### Create A/B Test")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                test_content = st.selectbox(
                    "Select content to A/B test",
                    options=content_options,
                    key="ab_test_content_select_unique"
                )
            
            with col2:
                num_variants = st.slider(
                    "Number of variants",
                    min_value=2,
                    max_value=5,
                    value=2,
                    help="Number of different versions to test"
                )
            
            if test_content:
                content_item = next(
                    item for item in calendar_manager.get_calendar().get_all_content()
                    if item.title == test_content
                )
                
                # Test Settings
                with st.expander("Test Settings"):
                    col1, col2 = st.columns(2)
                    with col1:
                        test_duration = st.number_input(
                            "Test Duration (days)",
                            min_value=1,
                            max_value=30,
                            value=7
                        )
                        target_metric = st.selectbox(
                            "Primary Metric",
                            options=['Engagement', 'Conversion', 'Reach', 'Click-through'],
                            index=0
                        )
                    with col2:
                        audience_size = st.select_slider(
                            "Audience Size",
                            options=['Small', 'Medium', 'Large'],
                            value='Medium'
                        )
                        confidence_level = st.slider(
                            "Confidence Level",
                            min_value=90,
                            max_value=99,
                            value=95,
                            help="Statistical confidence level for test results"
                        )
                
                # Generate Variants
                if st.button("Generate Variants"):
                    with st.spinner("Generating variants..."):
                        variants = _generate_ab_test_variants(content_generator, content_item, num_variants)
                        if variants:
                            st.success(f"Generated {len(variants)} variants!")
                            
                            # Display variants in tabs
                            variant_tabs = st.tabs([f"Variant {i+1}" for i in range(len(variants))])
                            for i, tab in enumerate(variant_tabs):
                                with tab:
                                    st.markdown(f"### Variant {i+1}")
                                    st.json(variants[i]['content'])
                                    
                                    # Variant metrics
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric(
                                            "Engagement Score",
                                            f"{variants[i]['metrics']['engagement_score']:.1f}%"
                                        )
                                    with col2:
                                        st.metric(
                                            "Conversion Rate",
                                            f"{variants[i]['metrics']['conversion_rate']:.1f}%"
                                        )
                                    with col3:
                                        st.metric(
                                            "Reach",
                                            f"{variants[i]['metrics']['reach']:,}"
                                        )
            
            # Results Analysis
            st.markdown("### Analyze Results")
            if test_content in st.session_state.ab_test_results:
                test_data = st.session_state.ab_test_results[test_content]
                
                # Test Status
                st.info(f"Test Status: {test_data['status']}")
                st.write(f"Started: {test_data['start_time']}")
                
                if test_data['status'] == 'running':
                    if st.button("End Test and Analyze"):
                        with st.spinner("Analyzing results..."):
                            results = _analyze_ab_test_results(content_item)
                            if results:
                                st.success("Analysis complete!")
                                _display_test_results(results)
        
        except Exception as e:
            logger.error(f"Error in A/B testing interface: {str(e)}", exc_info=True)
            st.error(f"Error in A/B testing: {str(e)}")

def _generate_ab_test_variants(
    content_generator,
    content: ContentItem,
    num_variants: int
) -> List[Dict[str, Any]]:
    """Generate A/B test variants for content."""
    try:
        logger.info(f"Generating {num_variants} variants for content: {content.title}")
        
        # Convert content to dictionary format
        content_dict = {
            'title': content.title,
            'content': content.description,
            'metadata': {
                'platform': content.platforms[0].name if content.platforms else 'Unknown',
                'content_type': content.content_type.name
            }
        }
        
        variants = []
        for i in range(num_variants):
            # Generate different variations
            variant = content_generator.generate_variation(
                content=content_dict,
                variation_type=f"variant_{i+1}"
            )
            if variant:
                variants.append(variant)
        
        return variants
        
    except Exception as e:
        logger.error(f"Error generating variants: {str(e)}")
        return []

def _analyze_ab_test_results(content_item: ContentItem) -> Dict[str, Any]:
    """Analyze results of A/B testing for content optimization."""
    try:
        logger.info(f"Analyzing A/B test results for: {content_item.title}")
        
        if content_item.title not in st.session_state.ab_test_results:
            raise ValueError("No A/B test results found for this content")
        
        test_data = st.session_state.ab_test_results[content_item.title]
        variants = test_data['variants']
        
        # Calculate performance metrics
        results = {
            'total_engagement': sum(v['metrics']['engagement_score'] for v in variants),
            'total_conversions': sum(v['metrics']['conversion_rate'] for v in variants),
            'total_reach': sum(v['metrics']['reach'] for v in variants),
            'best_performing_variant': max(variants, key=lambda x: x['metrics']['engagement_score']),
            'recommendations': []
        }
        
        # Generate recommendations
        for variant in variants:
            if variant['metrics']['engagement_score'] > 0.7:  # High engagement threshold
                results['recommendations'].append({
                    'variant_id': variant['variant_id'],
                    'reason': 'High engagement score',
                    'suggested_actions': ['Scale this variant', 'Apply learnings to other content']
                })
        
        # Update test status
        test_data['status'] = 'completed'
        test_data['results'] = results
        
        logger.info("A/B test results analyzed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Error analyzing A/B test results: {str(e)}", exc_info=True)
        st.error(f"Error analyzing A/B test results: {str(e)}")
        return {}

def _display_test_results(results: Dict[str, Any]) -> None:
    """Display A/B test results in the UI."""
    with st.expander("Overall Performance", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Engagement",
                f"{results['total_engagement']:.1f}%"
            )
        with col2:
            st.metric(
                "Total Conversions",
                f"{results['total_conversions']:.1f}%"
            )
        with col3:
            st.metric(
                "Total Reach",
                f"{results['total_reach']:,}"
            )
    
    with st.expander("Best Performing Variant", expanded=True):
        best_variant = results['best_performing_variant']
        st.markdown(f"### {best_variant['variant_id']}")
        st.json(best_variant['content'])
    
    with st.expander("Recommendations", expanded=True):
        for rec in results['recommendations']:
            st.markdown(f"#### {rec['variant_id']}")
            st.write(f"Reason: {rec['reason']}")
            st.write("Suggested Actions:")
            for action in rec['suggested_actions']:
                st.write(f"- {action}") 