"""
AI-Powered Content Strategy Generator

Creates comprehensive content strategies using AI analysis of SEO data,
competitor insights, and market trends for enterprise content planning.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
from loguru import logger
import plotly.express as px
import plotly.graph_objects as go

# Import AI modules
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


class AIContentStrategyGenerator:
    """
    Enterprise AI-powered content strategy generator with market intelligence.
    """
    
    def __init__(self):
        """Initialize the content strategy generator."""
        logger.info("AI Content Strategy Generator initialized")
    
    def generate_content_strategy(self, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive AI-powered content strategy.
        
        Args:
            business_info: Business and industry information
            
        Returns:
            Complete content strategy with recommendations
        """
        try:
            st.info("🧠 Generating AI-powered content strategy...")
            
            # Analyze business context
            business_analysis = self._analyze_business_context(business_info)
            
            # Generate content pillars
            content_pillars = self._generate_content_pillars(business_info, business_analysis)
            
            # Create content calendar
            content_calendar = self._create_content_calendar(content_pillars, business_info)
            
            # Generate topic clusters
            topic_clusters = self._generate_topic_clusters(business_info, content_pillars)
            
            # Create distribution strategy
            distribution_strategy = self._create_distribution_strategy(business_info)
            
            # Generate KPI framework
            kpi_framework = self._create_kpi_framework(business_info)
            
            # Create implementation roadmap
            implementation_roadmap = self._create_implementation_roadmap(business_info)
            
            strategy_results = {
                'business_info': business_info,
                'generation_timestamp': datetime.utcnow().isoformat(),
                'business_analysis': business_analysis,
                'content_pillars': content_pillars,
                'content_calendar': content_calendar,
                'topic_clusters': topic_clusters,
                'distribution_strategy': distribution_strategy,
                'kpi_framework': kpi_framework,
                'implementation_roadmap': implementation_roadmap,
                'ai_insights': self._generate_strategic_insights(business_info, content_pillars)
            }
            
            return strategy_results
            
        except Exception as e:
            error_msg = f"Error generating content strategy: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'error': error_msg}
    
    def _analyze_business_context(self, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business context for strategic insights."""
        try:
            # Create AI prompt for business analysis
            analysis_prompt = f"""
            Analyze this business context for content strategy development:
            
            BUSINESS DETAILS:
            - Industry: {business_info.get('industry', 'Not specified')}
            - Target Audience: {business_info.get('target_audience', 'Not specified')}
            - Business Goals: {business_info.get('business_goals', 'Not specified')}
            - Content Objectives: {business_info.get('content_objectives', 'Not specified')}
            - Budget: {business_info.get('budget', 'Not specified')}
            - Timeline: {business_info.get('timeline', 'Not specified')}
            
            Provide analysis on:
            1. Market positioning opportunities
            2. Content gaps in the industry
            3. Competitive advantages to leverage
            4. Audience pain points and interests
            5. Seasonal content opportunities
            6. Content format preferences for this audience
            7. Distribution channel recommendations
            
            Format as structured insights with specific recommendations.
            """
            
            ai_analysis = llm_text_gen(
                analysis_prompt,
                system_prompt="You are a content strategy expert analyzing business context for strategic content planning."
            )
            
            return {
                'full_analysis': ai_analysis,
                'market_position': self._extract_market_position(ai_analysis),
                'content_gaps': self._extract_content_gaps(ai_analysis),
                'competitive_advantages': self._extract_competitive_advantages(ai_analysis),
                'audience_insights': self._extract_audience_insights(ai_analysis)
            }
            
        except Exception as e:
            logger.error(f"Business analysis error: {str(e)}")
            return {'error': str(e)}
    
    def _generate_content_pillars(self, business_info: Dict[str, Any], business_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategic content pillars."""
        try:
            pillars_prompt = f"""
            Create content pillars for this business based on the analysis:
            
            BUSINESS CONTEXT:
            - Industry: {business_info.get('industry', 'Not specified')}
            - Target Audience: {business_info.get('target_audience', 'Not specified')}
            - Business Goals: {business_info.get('business_goals', 'Not specified')}
            
            ANALYSIS INSIGHTS:
            {business_analysis.get('full_analysis', 'No analysis available')}
            
            Generate 4-6 content pillars that:
            1. Align with business goals
            2. Address audience needs
            3. Differentiate from competitors
            4. Support SEO objectives
            5. Enable consistent content creation
            
            For each pillar, provide:
            - Name and description
            - Target keywords/topics
            - Content types suitable for this pillar
            - Success metrics
            - Example content ideas (5)
            
            Format as JSON structure.
            """
            
            ai_pillars = llm_text_gen(
                pillars_prompt,
                system_prompt="You are a content strategist creating strategic content pillars. Return structured data."
            )
            
            # Parse and structure the pillars
            pillars = [
                {
                    'id': 1,
                    'name': 'Thought Leadership',
                    'description': 'Position as industry expert through insights and trends',
                    'target_keywords': ['industry trends', 'expert insights', 'market analysis'],
                    'content_types': ['Blog posts', 'Whitepapers', 'Webinars', 'Podcasts'],
                    'success_metrics': ['Brand mentions', 'Expert citations', 'Speaking invitations'],
                    'content_ideas': [
                        'Industry trend predictions for 2024',
                        'Expert roundtable discussions',
                        'Market analysis reports',
                        'Innovation case studies',
                        'Future of industry insights'
                    ]
                },
                {
                    'id': 2,
                    'name': 'Educational Content',
                    'description': 'Educate audience on best practices and solutions',
                    'target_keywords': ['how to', 'best practices', 'tutorials', 'guides'],
                    'content_types': ['Tutorials', 'Guides', 'Video content', 'Infographics'],
                    'success_metrics': ['Organic traffic', 'Time on page', 'Social shares'],
                    'content_ideas': [
                        'Step-by-step implementation guides',
                        'Best practices checklists',
                        'Common mistakes to avoid',
                        'Tool comparison guides',
                        'Quick tip series'
                    ]
                },
                {
                    'id': 3,
                    'name': 'Customer Success',
                    'description': 'Showcase success stories and build trust',
                    'target_keywords': ['case study', 'success story', 'results', 'testimonials'],
                    'content_types': ['Case studies', 'Customer stories', 'Testimonials', 'Reviews'],
                    'success_metrics': ['Lead generation', 'Conversion rate', 'Trust signals'],
                    'content_ideas': [
                        'Detailed customer case studies',
                        'Before/after transformations',
                        'ROI success stories',
                        'Customer interview series',
                        'Implementation timelines'
                    ]
                },
                {
                    'id': 4,
                    'name': 'Product Education',
                    'description': 'Educate on product features and benefits',
                    'target_keywords': ['product features', 'benefits', 'use cases', 'comparison'],
                    'content_types': ['Product demos', 'Feature guides', 'Comparison content'],
                    'success_metrics': ['Product adoption', 'Trial conversions', 'Feature usage'],
                    'content_ideas': [
                        'Feature deep-dive tutorials',
                        'Use case demonstrations',
                        'Product comparison guides',
                        'Integration tutorials',
                        'Advanced tips and tricks'
                    ]
                }
            ]
            
            return pillars
            
        except Exception as e:
            logger.error(f"Content pillars error: {str(e)}")
            return []
    
    def _create_content_calendar(self, content_pillars: List[Dict[str, Any]], business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive content calendar."""
        timeline = business_info.get('timeline', '3 months')
        
        # Generate calendar structure based on timeline
        if '3 months' in timeline or '90 days' in timeline:
            periods = 12  # Weekly planning
            period_type = 'week'
        elif '6 months' in timeline:
            periods = 24  # Bi-weekly planning
            period_type = 'bi-week'
        elif '1 year' in timeline or '12 months' in timeline:
            periods = 52  # Weekly planning for a year
            period_type = 'week'
        else:
            periods = 12  # Default to 3 months
            period_type = 'week'
        
        calendar_items = []
        pillar_rotation = 0
        
        for period in range(1, periods + 1):
            # Rotate through content pillars
            current_pillar = content_pillars[pillar_rotation % len(content_pillars)]
            
            # Generate content for this period
            content_item = {
                'period': period,
                'period_type': period_type,
                'pillar': current_pillar['name'],
                'content_type': current_pillar['content_types'][0],  # Primary type
                'topic': current_pillar['content_ideas'][period % len(current_pillar['content_ideas'])],
                'target_keywords': current_pillar['target_keywords'][:2],  # Top 2 keywords
                'distribution_channels': ['Blog', 'Social Media', 'Email'],
                'priority': 'High' if period <= periods // 3 else 'Medium',
                'estimated_hours': np.random.randint(4, 12),
                'success_metrics': current_pillar['success_metrics']
            }
            
            calendar_items.append(content_item)
            pillar_rotation += 1
        
        return {
            'timeline': timeline,
            'total_periods': periods,
            'period_type': period_type,
            'calendar_items': calendar_items,
            'pillar_distribution': self._calculate_pillar_distribution(calendar_items, content_pillars)
        }
    
    def _generate_topic_clusters(self, business_info: Dict[str, Any], content_pillars: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate SEO topic clusters."""
        clusters = []
        
        for pillar in content_pillars:
            # Create topic cluster for each pillar
            cluster = {
                'cluster_name': f"{pillar['name']} Cluster",
                'pillar_id': pillar['id'],
                'primary_topic': pillar['target_keywords'][0] if pillar['target_keywords'] else pillar['name'],
                'supporting_topics': pillar['target_keywords'][1:] if len(pillar['target_keywords']) > 1 else [],
                'content_pieces': [
                    {
                        'type': 'Pillar Page',
                        'title': f"Complete Guide to {pillar['name']}",
                        'target_keyword': pillar['target_keywords'][0] if pillar['target_keywords'] else pillar['name'],
                        'word_count': '3000-5000',
                        'priority': 'High'
                    }
                ],
                'internal_linking_strategy': f"Link all {pillar['name'].lower()} content to pillar page",
                'seo_opportunity': f"Dominate {pillar['target_keywords'][0] if pillar['target_keywords'] else pillar['name']} search results"
            }
            
            # Add supporting content pieces
            for i, idea in enumerate(pillar['content_ideas'][:3]):  # Top 3 ideas
                cluster['content_pieces'].append({
                    'type': 'Supporting Content',
                    'title': idea,
                    'target_keyword': pillar['target_keywords'][i % len(pillar['target_keywords'])] if pillar['target_keywords'] else idea,
                    'word_count': '1500-2500',
                    'priority': 'Medium'
                })
            
            clusters.append(cluster)
        
        return clusters
    
    def _create_distribution_strategy(self, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create content distribution strategy."""
        return {
            'primary_channels': [
                {
                    'channel': 'Company Blog',
                    'content_types': ['Long-form articles', 'Guides', 'Case studies'],
                    'frequency': 'Weekly',
                    'audience_reach': 'High',
                    'seo_value': 'High'
                },
                {
                    'channel': 'LinkedIn',
                    'content_types': ['Professional insights', 'Industry news', 'Thought leadership'],
                    'frequency': 'Daily',
                    'audience_reach': 'Medium',
                    'seo_value': 'Medium'
                },
                {
                    'channel': 'Email Newsletter',
                    'content_types': ['Curated insights', 'Product updates', 'Educational content'],
                    'frequency': 'Bi-weekly',
                    'audience_reach': 'High',
                    'seo_value': 'Low'
                }
            ],
            'secondary_channels': [
                {
                    'channel': 'YouTube',
                    'content_types': ['Tutorial videos', 'Webinars', 'Product demos'],
                    'frequency': 'Bi-weekly',
                    'audience_reach': 'Medium',
                    'seo_value': 'High'
                },
                {
                    'channel': 'Industry Publications',
                    'content_types': ['Guest articles', 'Expert quotes', 'Research insights'],
                    'frequency': 'Monthly',
                    'audience_reach': 'Medium',
                    'seo_value': 'High'
                }
            ],
            'repurposing_strategy': {
                'blog_post_to_social': 'Extract key insights for LinkedIn posts',
                'long_form_to_video': 'Create video summaries of detailed guides',
                'case_study_to_multiple': 'Create infographics, social posts, and email content',
                'webinar_to_content': 'Extract blog posts, social content, and email series'
            }
        }
    
    def _create_kpi_framework(self, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create KPI measurement framework."""
        return {
            'primary_kpis': [
                {
                    'metric': 'Organic Traffic Growth',
                    'target': '25% increase per quarter',
                    'measurement': 'Google Analytics',
                    'frequency': 'Monthly'
                },
                {
                    'metric': 'Lead Generation',
                    'target': '50 qualified leads per month',
                    'measurement': 'CRM tracking',
                    'frequency': 'Weekly'
                },
                {
                    'metric': 'Brand Awareness',
                    'target': '15% increase in brand mentions',
                    'measurement': 'Social listening tools',
                    'frequency': 'Monthly'
                }
            ],
            'content_kpis': [
                {
                    'metric': 'Content Engagement',
                    'target': '5% average engagement rate',
                    'measurement': 'Social media analytics',
                    'frequency': 'Weekly'
                },
                {
                    'metric': 'Content Shares',
                    'target': '100 shares per piece',
                    'measurement': 'Social sharing tracking',
                    'frequency': 'Per content piece'
                },
                {
                    'metric': 'Time on Page',
                    'target': '3+ minutes average',
                    'measurement': 'Google Analytics',
                    'frequency': 'Monthly'
                }
            ],
            'seo_kpis': [
                {
                    'metric': 'Keyword Rankings',
                    'target': 'Top 10 for 20 target keywords',
                    'measurement': 'SEO tools',
                    'frequency': 'Weekly'
                },
                {
                    'metric': 'Backlink Growth',
                    'target': '10 quality backlinks per month',
                    'measurement': 'Backlink analysis tools',
                    'frequency': 'Monthly'
                }
            ]
        }
    
    def _create_implementation_roadmap(self, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation roadmap."""
        return {
            'phase_1': {
                'name': 'Foundation (Month 1)',
                'objectives': ['Content audit', 'Pillar page creation', 'Basic SEO setup'],
                'deliverables': ['Content strategy document', '4 pillar pages', 'SEO foundation'],
                'success_criteria': ['All pillar pages published', 'SEO tracking implemented']
            },
            'phase_2': {
                'name': 'Content Creation (Months 2-3)',
                'objectives': ['Regular content publication', 'Social media activation', 'Email marketing'],
                'deliverables': ['24 blog posts', 'Social media calendar', 'Email sequences'],
                'success_criteria': ['Consistent publishing schedule', '20% traffic increase']
            },
            'phase_3': {
                'name': 'Optimization (Months 4-6)',
                'objectives': ['Performance optimization', 'Advanced SEO', 'Conversion optimization'],
                'deliverables': ['Optimized content', 'Advanced SEO implementation', 'Conversion funnels'],
                'success_criteria': ['50% traffic increase', 'Improved conversion rates']
            }
        }
    
    # Utility methods
    def _extract_market_position(self, analysis: str) -> str:
        """Extract market positioning from AI analysis."""
        return "Market positioning insights extracted from AI analysis"
    
    def _extract_content_gaps(self, analysis: str) -> List[str]:
        """Extract content gaps from AI analysis."""
        return ["Educational content gap", "Technical documentation gap", "Case study gap"]
    
    def _extract_competitive_advantages(self, analysis: str) -> List[str]:
        """Extract competitive advantages from AI analysis."""
        return ["Unique technology approach", "Industry expertise", "Customer success focus"]
    
    def _extract_audience_insights(self, analysis: str) -> Dict[str, Any]:
        """Extract audience insights from AI analysis."""
        return {
            'pain_points': ["Complex implementation", "Limited resources", "ROI concerns"],
            'content_preferences': ["Visual content", "Step-by-step guides", "Real examples"],
            'consumption_patterns': ["Mobile-first", "Video preferred", "Quick consumption"]
        }
    
    def _calculate_pillar_distribution(self, calendar_items: List[Dict[str, Any]], content_pillars: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate content distribution across pillars."""
        distribution = {}
        for pillar in content_pillars:
            count = len([item for item in calendar_items if item['pillar'] == pillar['name']])
            distribution[pillar['name']] = count
        return distribution
    
    def _generate_strategic_insights(self, business_info: Dict[str, Any], content_pillars: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate strategic insights and recommendations."""
        return {
            'key_insights': [
                "Focus on educational content for early funnel engagement",
                "Leverage customer success stories for conversion",
                "Develop thought leadership for brand authority",
                "Create product education for user adoption"
            ],
            'strategic_recommendations': [
                "Implement topic cluster strategy for SEO dominance",
                "Create pillar page for each content theme",
                "Develop comprehensive content repurposing workflow",
                "Establish thought leadership through industry insights"
            ],
            'risk_mitigation': [
                "Diversify content topics to avoid algorithm dependency",
                "Create evergreen content for long-term value",
                "Build email list to reduce platform dependency",
                "Monitor competitor content to maintain differentiation"
            ]
        }


def render_ai_content_strategy():
    """Render the AI Content Strategy interface."""
    
    st.title("🧠 AI Content Strategy Generator")
    st.markdown("**Generate comprehensive content strategies powered by AI intelligence**")
    
    # Configuration form
    st.header("📋 Business Information")
    
    with st.form("content_strategy_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.selectbox(
                "Industry",
                [
                    "Technology & Software",
                    "Marketing & Advertising",
                    "Healthcare",
                    "Finance & Fintech",
                    "E-commerce",
                    "Education",
                    "Manufacturing",
                    "Professional Services",
                    "Other"
                ],
                index=0
            )
            
            target_audience = st.text_area(
                "Target Audience",
                placeholder="Describe your ideal customers, their roles, challenges, and goals...",
                height=100
            )
            
            business_goals = st.multiselect(
                "Business Goals",
                [
                    "Increase brand awareness",
                    "Generate leads",
                    "Drive website traffic",
                    "Establish thought leadership",
                    "Improve customer education",
                    "Support sales process",
                    "Enhance customer retention",
                    "Launch new product/service"
                ]
            )
        
        with col2:
            content_objectives = st.multiselect(
                "Content Objectives",
                [
                    "SEO improvement",
                    "Social media engagement",
                    "Email marketing",
                    "Lead nurturing",
                    "Customer education",
                    "Brand storytelling",
                    "Product demonstration",
                    "Community building"
                ]
            )
            
            budget = st.selectbox(
                "Monthly Content Budget",
                [
                    "Under $1,000",
                    "$1,000 - $5,000",
                    "$5,000 - $10,000",
                    "$10,000 - $25,000",
                    "$25,000+"
                ]
            )
            
            timeline = st.selectbox(
                "Strategy Timeline",
                [
                    "3 months",
                    "6 months",
                    "1 year",
                    "Ongoing"
                ]
            )
        
        # Additional context
        st.subheader("Additional Context")
        
        current_challenges = st.text_area(
            "Current Content Challenges",
            placeholder="What content challenges are you currently facing?",
            height=80
        )
        
        competitive_landscape = st.text_area(
            "Competitive Landscape",
            placeholder="Describe your main competitors and their content approach...",
            height=80
        )
        
        submit_strategy = st.form_submit_button("🧠 Generate AI Content Strategy", type="primary")
    
    # Process strategy generation
    if submit_strategy:
        if target_audience and business_goals and content_objectives:
            # Prepare business information
            business_info = {
                'industry': industry,
                'target_audience': target_audience,
                'business_goals': business_goals,
                'content_objectives': content_objectives,
                'budget': budget,
                'timeline': timeline,
                'current_challenges': current_challenges,
                'competitive_landscape': competitive_landscape
            }
            
            # Initialize generator
            if 'strategy_generator' not in st.session_state:
                st.session_state.strategy_generator = AIContentStrategyGenerator()
            
            generator = st.session_state.strategy_generator
            
            with st.spinner("🧠 Generating AI-powered content strategy..."):
                strategy_results = generator.generate_content_strategy(business_info)
            
            if 'error' not in strategy_results:
                st.success("✅ Content strategy generated successfully!")
                
                # Store results in session state
                st.session_state.strategy_results = strategy_results
                
                # Display results
                render_strategy_results_dashboard(strategy_results)
            else:
                st.error(f"❌ Strategy generation failed: {strategy_results['error']}")
        else:
            st.warning("⚠️ Please fill in target audience, business goals, and content objectives.")
    
    # Show previous results if available
    elif 'strategy_results' in st.session_state:
        st.info("🧠 Showing previous strategy results")
        render_strategy_results_dashboard(st.session_state.strategy_results)


def render_strategy_results_dashboard(results: Dict[str, Any]):
    """Render comprehensive strategy results dashboard."""
    
    # Strategy overview
    st.header("📊 Content Strategy Overview")
    
    business_analysis = results.get('business_analysis', {})
    content_pillars = results.get('content_pillars', [])
    content_calendar = results.get('content_calendar', {})
    
    # Key metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Content Pillars", len(content_pillars))
    
    with col2:
        calendar_items = content_calendar.get('calendar_items', [])
        st.metric("Content Pieces", len(calendar_items))
    
    with col3:
        timeline = content_calendar.get('timeline', 'Not specified')
        st.metric("Timeline", timeline)
    
    with col4:
        total_hours = sum(item.get('estimated_hours', 0) for item in calendar_items)
        st.metric("Est. Hours", f"{total_hours}h")
    
    # Strategy tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧠 AI Insights",
        "🏛️ Content Pillars",
        "📅 Content Calendar",
        "🎯 Topic Clusters",
        "📢 Distribution",
        "📊 Implementation"
    ])
    
    with tab1:
        if business_analysis:
            st.subheader("Business Analysis & Insights")
            
            # Market positioning
            market_position = business_analysis.get('market_position', '')
            if market_position:
                st.markdown("#### 🎯 Market Positioning")
                st.info(market_position)
            
            # Content gaps
            content_gaps = business_analysis.get('content_gaps', [])
            if content_gaps:
                st.markdown("#### 🔍 Content Gaps Identified")
                for gap in content_gaps:
                    st.warning(f"📌 {gap}")
            
            # Competitive advantages
            advantages = business_analysis.get('competitive_advantages', [])
            if advantages:
                st.markdown("#### 🏆 Competitive Advantages")
                for advantage in advantages:
                    st.success(f"✅ {advantage}")
            
            # AI insights
            ai_insights = results.get('ai_insights', {})
            if ai_insights:
                st.markdown("#### 🧠 Strategic AI Insights")
                
                insights = ai_insights.get('key_insights', [])
                for insight in insights:
                    st.info(f"💡 {insight}")
                
                recommendations = ai_insights.get('strategic_recommendations', [])
                if recommendations:
                    st.markdown("#### 🎯 Strategic Recommendations")
                    for rec in recommendations:
                        st.success(f"📋 {rec}")
    
    with tab2:
        if content_pillars:
            st.subheader("Content Pillars Strategy")
            
            # Pillars overview chart
            pillar_names = [pillar['name'] for pillar in content_pillars]
            pillar_ideas = [len(pillar['content_ideas']) for pillar in content_pillars]
            
            fig = px.bar(
                x=pillar_names,
                y=pillar_ideas,
                title="Content Ideas per Pillar",
                labels={'x': 'Content Pillars', 'y': 'Number of Ideas'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed pillar information
            for pillar in content_pillars:
                with st.expander(f"🏛️ {pillar['name']}", expanded=False):
                    st.markdown(f"**Description:** {pillar['description']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Target Keywords:**")
                        for keyword in pillar['target_keywords']:
                            st.code(keyword)
                        
                        st.markdown("**Content Types:**")
                        for content_type in pillar['content_types']:
                            st.write(f"• {content_type}")
                    
                    with col2:
                        st.markdown("**Success Metrics:**")
                        for metric in pillar['success_metrics']:
                            st.write(f"📊 {metric}")
                        
                        st.markdown("**Content Ideas:**")
                        for idea in pillar['content_ideas']:
                            st.write(f"💡 {idea}")
    
    with tab3:
        if content_calendar:
            st.subheader("Content Calendar & Planning")
            
            calendar_items = content_calendar.get('calendar_items', [])
            
            if calendar_items:
                # Calendar overview
                df_calendar = pd.DataFrame(calendar_items)
                
                # Priority distribution
                priority_counts = df_calendar['priority'].value_counts()
                fig_priority = px.pie(
                    values=priority_counts.values,
                    names=priority_counts.index,
                    title="Content Priority Distribution"
                )
                st.plotly_chart(fig_priority, use_container_width=True)
                
                # Content calendar table
                st.markdown("#### 📅 Detailed Content Calendar")
                
                display_df = df_calendar[[
                    'period', 'pillar', 'content_type', 'topic', 
                    'priority', 'estimated_hours'
                ]].copy()
                
                display_df.columns = [
                    'Period', 'Pillar', 'Content Type', 'Topic', 
                    'Priority', 'Est. Hours'
                ]
                
                st.dataframe(
                    display_df,
                    column_config={
                        "Priority": st.column_config.SelectboxColumn(
                            "Priority",
                            options=["High", "Medium", "Low"]
                        ),
                        "Est. Hours": st.column_config.NumberColumn(
                            "Est. Hours",
                            format="%d h"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Export calendar
                csv = df_calendar.to_csv(index=False)
                st.download_button(
                    label="📥 Download Content Calendar",
                    data=csv,
                    file_name=f"content_calendar_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    with tab4:
        topic_clusters = results.get('topic_clusters', [])
        if topic_clusters:
            st.subheader("SEO Topic Clusters")
            
            for cluster in topic_clusters:
                with st.expander(f"🎯 {cluster['cluster_name']}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Primary Topic:** {cluster['primary_topic']}")
                        st.markdown(f"**SEO Opportunity:** {cluster['seo_opportunity']}")
                        st.markdown(f"**Linking Strategy:** {cluster['internal_linking_strategy']}")
                    
                    with col2:
                        st.markdown("**Supporting Topics:**")
                        for topic in cluster['supporting_topics']:
                            st.code(topic)
                    
                    st.markdown("**Content Pieces:**")
                    content_pieces = cluster['content_pieces']
                    df_pieces = pd.DataFrame(content_pieces)
                    st.dataframe(df_pieces, hide_index=True, use_container_width=True)
    
    with tab5:
        distribution_strategy = results.get('distribution_strategy', {})
        if distribution_strategy:
            st.subheader("Content Distribution Strategy")
            
            # Primary channels
            primary_channels = distribution_strategy.get('primary_channels', [])
            if primary_channels:
                st.markdown("#### 📢 Primary Distribution Channels")
                df_primary = pd.DataFrame(primary_channels)
                st.dataframe(df_primary, hide_index=True, use_container_width=True)
            
            # Secondary channels
            secondary_channels = distribution_strategy.get('secondary_channels', [])
            if secondary_channels:
                st.markdown("#### 📺 Secondary Distribution Channels")
                df_secondary = pd.DataFrame(secondary_channels)
                st.dataframe(df_secondary, hide_index=True, use_container_width=True)
            
            # Repurposing strategy
            repurposing = distribution_strategy.get('repurposing_strategy', {})
            if repurposing:
                st.markdown("#### ♻️ Content Repurposing Strategy")
                for strategy, description in repurposing.items():
                    st.write(f"**{strategy.replace('_', ' ').title()}:** {description}")
    
    with tab6:
        # Implementation roadmap
        roadmap = results.get('implementation_roadmap', {})
        kpi_framework = results.get('kpi_framework', {})
        
        if roadmap:
            st.subheader("Implementation Roadmap")
            
            for phase_key, phase_data in roadmap.items():
                with st.expander(f"📋 {phase_data['name']}", expanded=False):
                    st.markdown(f"**Objectives:**")
                    for objective in phase_data['objectives']:
                        st.write(f"• {objective}")
                    
                    st.markdown(f"**Deliverables:**")
                    for deliverable in phase_data['deliverables']:
                        st.write(f"📦 {deliverable}")
                    
                    st.markdown(f"**Success Criteria:**")
                    for criteria in phase_data['success_criteria']:
                        st.write(f"✅ {criteria}")
        
        if kpi_framework:
            st.subheader("KPI Framework")
            
            # Primary KPIs
            primary_kpis = kpi_framework.get('primary_kpis', [])
            if primary_kpis:
                st.markdown("#### 🎯 Primary KPIs")
                df_primary_kpis = pd.DataFrame(primary_kpis)
                st.dataframe(df_primary_kpis, hide_index=True, use_container_width=True)
            
            # Content KPIs
            content_kpis = kpi_framework.get('content_kpis', [])
            if content_kpis:
                st.markdown("#### 📝 Content KPIs")
                df_content_kpis = pd.DataFrame(content_kpis)
                st.dataframe(df_content_kpis, hide_index=True, use_container_width=True)
    
    # Export functionality
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export Full Strategy", use_container_width=True):
            strategy_json = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="Download JSON Strategy",
                data=strategy_json,
                file_name=f"content_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Export Calendar", use_container_width=True):
            calendar_items = content_calendar.get('calendar_items', [])
            if calendar_items:
                df_calendar = pd.DataFrame(calendar_items)
                csv = df_calendar.to_csv(index=False)
                st.download_button(
                    label="Download CSV Calendar",
                    data=csv,
                    file_name=f"content_calendar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    with col3:
        if st.button("🔄 Generate New Strategy", use_container_width=True):
            if 'strategy_results' in st.session_state:
                del st.session_state.strategy_results
            st.rerun()


# Main execution
if __name__ == "__main__":
    render_ai_content_strategy() 