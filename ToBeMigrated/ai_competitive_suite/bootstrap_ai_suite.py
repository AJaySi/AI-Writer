"""
Bootstrap AI Competitive Suite

All-in-one AI-powered competitive tools for solo entrepreneurs.
Combines content performance prediction and competitive intelligence.
"""

import asyncio
import streamlit as st
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

# Import the AI-powered tools
from lib.content_performance_predictor.ai_performance_predictor import AIContentPerformancePredictor
from lib.competitive_intelligence.ai_competitive_intelligence import AICompetitiveIntelligence


class BootstrapAISuite:
    """
    Unified AI suite for bootstrapped entrepreneurs.
    Combines content performance prediction and competitive intelligence.
    """
    
    def __init__(self):
        """Initialize the bootstrap AI suite."""
        self.content_predictor = AIContentPerformancePredictor()
        self.competitor_intel = AICompetitiveIntelligence()
        
        logger.info("Bootstrap AI Suite initialized")
    
    def get_suite_capabilities(self) -> Dict[str, Any]:
        """Get all suite capabilities."""
        return {
            'content_prediction': {
                'name': 'AI Content Performance Predictor',
                'description': 'Predict content performance using AI analysis',
                'features': [
                    'Platform-specific optimization',
                    'Engagement prediction',
                    'Content recommendations',
                    'Hashtag optimization',
                    'Posting time suggestions'
                ]
            },
            'competitive_intelligence': {
                'name': 'Bootstrap Competitive Intelligence',
                'description': 'AI-powered competitor analysis for startups',
                'features': [
                    'Competitor weakness identification',
                    'Content gap analysis',
                    'Strategic recommendations',
                    'Quick win opportunities',
                    'Market positioning advice'
                ]
            },
            'integrated_workflows': {
                'name': 'Smart Workflows',
                'description': 'Combined insights from both tools',
                'features': [
                    'Competitor-informed content strategy',
                    'Performance-optimized competitive positioning',
                    'Data-driven differentiation',
                    'Strategic content calendar'
                ]
            }
        }
    
    async def get_competitive_content_strategy(
        self, 
        content: str,
        target_platform: str,
        competitor_urls: List[str],
        industry: str,
        your_strengths: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get a comprehensive content strategy combining performance prediction
        and competitive analysis.
        """
        logger.info("Generating competitive content strategy")
        
        try:
            # Step 1: Predict content performance
            st.info("🎯 Analyzing content performance potential...")
            performance_analysis = await self.content_predictor.predict_performance(
                content, target_platform
            )
            
            # Step 2: Get competitive intelligence
            st.info("🕵️ Analyzing competitive landscape...")
            competitive_analysis = await self.competitor_intel.analyze_competitors(
                competitor_urls, industry, your_strengths
            )
            
            # Step 3: Generate integrated strategy
            st.info("🧠 Creating integrated strategy...")
            integrated_strategy = await self._create_integrated_strategy(
                performance_analysis, competitive_analysis, content, target_platform
            )
            
            return {
                'content_performance': performance_analysis,
                'competitive_intelligence': competitive_analysis,
                'integrated_strategy': integrated_strategy,
                'action_plan': self._create_action_plan(
                    performance_analysis, competitive_analysis, integrated_strategy
                )
            }
            
        except Exception as e:
            error_msg = f"Error generating competitive content strategy: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'error': error_msg}
    
    async def _create_integrated_strategy(
        self,
        performance_analysis: Dict[str, Any],
        competitive_analysis: Dict[str, Any],
        content: str,
        platform: str
    ) -> Dict[str, Any]:
        """Create integrated strategy combining both analyses."""
        
        # Extract key insights
        predicted_performance = performance_analysis.get('predictions', {})
        competitor_insights = competitive_analysis.get('competitor_insights', {})
        content_gaps = competitive_analysis.get('content_gap_analysis', {})
        
        from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
        
        integration_prompt = f"""
        Create an integrated content strategy that combines performance prediction and competitive analysis:
        
        CONTENT TO ANALYZE:
        "{content[:500]}"
        
        TARGET PLATFORM: {platform}
        
        PERFORMANCE PREDICTIONS:
        {predicted_performance}
        
        COMPETITIVE INSIGHTS:
        Key Insights: {competitor_insights.get('key_insights', [])}
        Content Gaps: {content_gaps.get('priority_gaps', [])}
        Quick Wins: {competitive_analysis.get('quick_wins', [])}
        
        Provide an integrated strategy that answers:
        
        1. CONTENT OPTIMIZATION BASED ON COMPETITION:
           - How can you modify your content to outperform competitors?
           - What competitive advantages can you highlight?
           - How can you fill content gaps while maintaining performance?
           
        2. STRATEGIC POSITIONING:
           - How does your predicted performance compare to competitive landscape?
           - What unique angle can you take that competitors miss?
           - How can you leverage competitor weaknesses in your content?
           
        3. PERFORMANCE ENHANCEMENT:
           - What competitive insights can improve your predicted performance?
           - Which competitor strategies should you adopt or avoid?
           - How can you differentiate while maintaining engagement?
           
        4. TACTICAL EXECUTION:
           - What specific changes will maximize both performance and competitive advantage?
           - How should you sequence your content to beat competitors?
           - What metrics should you track for competitive success?
           
        Provide specific, actionable recommendations for a solo entrepreneur.
        """
        
        try:
            integrated_analysis = llm_text_gen(
                integration_prompt,
                system_prompt="You are a strategic content consultant specializing in competitive content strategy for solo entrepreneurs. Combine performance optimization with competitive intelligence."
            )
            
            return {
                'full_strategy': integrated_analysis,
                'optimization_recommendations': self._extract_optimization_recs(integrated_analysis),
                'competitive_positioning': self._extract_positioning_strategy(integrated_analysis),
                'performance_tactics': self._extract_performance_tactics(integrated_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error creating integrated strategy: {str(e)}")
            return {
                'full_strategy': f"Error generating integrated strategy: {str(e)}",
                'optimization_recommendations': [],
                'competitive_positioning': 'Focus on unique value proposition',
                'performance_tactics': []
            }
    
    def _extract_optimization_recs(self, strategy: str) -> List[str]:
        """Extract optimization recommendations."""
        recommendations = []
        
        lines = strategy.split('\n')
        for line in lines:
            line = line.strip()
            if ('optimize' in line.lower() or 'improve' in line.lower() or 
                'enhance' in line.lower()) and len(line) > 20:
                recommendations.append(line.lstrip('•-* ').strip())
        
        return recommendations[:5]
    
    def _extract_positioning_strategy(self, strategy: str) -> str:
        """Extract positioning strategy."""
        lines = strategy.split('\n')
        for line in lines:
            if ('position' in line.lower() or 'unique' in line.lower() or 
                'differentiate' in line.lower()) and len(line) > 30:
                return line.strip()
        
        return "Focus on unique value proposition that competitors can't match"
    
    def _extract_performance_tactics(self, strategy: str) -> List[str]:
        """Extract performance tactics."""
        tactics = []
        
        lines = strategy.split('\n')
        for line in lines:
            line = line.strip()
            if ('tactic' in line.lower() or 'execute' in line.lower() or 
                'implement' in line.lower()) and len(line) > 20:
                tactics.append(line.lstrip('•-* ').strip())
        
        return tactics[:4]
    
    def _create_action_plan(
        self,
        performance_analysis: Dict[str, Any],
        competitive_analysis: Dict[str, Any],
        integrated_strategy: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create actionable plan from all analyses."""
        
        action_plan = []
        
        # From performance analysis
        recommendations = performance_analysis.get('recommendations', [])
        for rec in recommendations[:2]:
            action_plan.append({
                'category': 'Content Performance',
                'action': rec,
                'priority': 'High',
                'timeframe': 'Immediate',
                'source': 'AI Performance Predictor'
            })
        
        # From competitive analysis
        quick_wins = competitive_analysis.get('quick_wins', [])
        for win in quick_wins[:2]:
            action_plan.append({
                'category': 'Competitive Strategy',
                'action': win.get('action', win),
                'priority': 'High',
                'timeframe': win.get('timeframe', '1-2 weeks') if isinstance(win, dict) else '1-2 weeks',
                'source': 'Competitive Intelligence'
            })
        
        # From integrated strategy
        optimization_recs = integrated_strategy.get('optimization_recommendations', [])
        for rec in optimization_recs[:2]:
            action_plan.append({
                'category': 'Integrated Strategy',
                'action': rec,
                'priority': 'Medium',
                'timeframe': '1-4 weeks',
                'source': 'Integrated Analysis'
            })
        
        return action_plan


def render_bootstrap_ai_suite():
    """Render the complete bootstrap AI suite interface."""
    
    st.set_page_config(
        page_title="Bootstrap AI Competitive Suite",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Bootstrap AI Competitive Suite")
    st.markdown("**The complete AI toolkit for solo entrepreneurs competing against big players**")
    
    # Initialize suite
    if 'ai_suite' not in st.session_state:
        st.session_state.ai_suite = BootstrapAISuite()
    
    suite = st.session_state.ai_suite
    
    # Sidebar with capabilities
    st.sidebar.header("🎯 AI Suite Capabilities")
    capabilities = suite.get_suite_capabilities()
    
    for key, capability in capabilities.items():
        with st.sidebar.expander(capability['name']):
            st.write(capability['description'])
            for feature in capability['features']:
                st.write(f"• {feature}")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "🎯 Content Performance Predictor",
        "🕵️ Competitive Intelligence", 
        "🧠 Integrated Strategy"
    ])
    
    # Tab 1: Content Performance Predictor
    with tab1:
        st.header("🎯 AI Content Performance Predictor")
        st.markdown("Predict how well your content will perform before you publish")
        
        # Import and render the AI predictor UI
        from lib.content_performance_predictor.ai_performance_predictor import render_ai_predictor_ui
        render_ai_predictor_ui()
    
    # Tab 2: Competitive Intelligence
    with tab2:
        st.header("🕵️ Bootstrap Competitive Intelligence")
        st.markdown("Analyze competitors and find opportunities to outmaneuver them")
        
        # Import and render the competitive intelligence UI
        from lib.competitive_intelligence.ai_competitive_intelligence import render_ai_competitive_intelligence_ui
        render_ai_competitive_intelligence_ui()
    
    # Tab 3: Integrated Strategy
    with tab3:
        st.header("🧠 Integrated AI Strategy")
        st.markdown("Combine content performance prediction with competitive intelligence for maximum impact")
        
        # Input section
        st.subheader("Strategy Input")
        
        col1, col2 = st.columns(2)
        
        with col1:
            content = st.text_area(
                "Content to Analyze",
                value="Discover how AI can revolutionize your content creation process with our innovative tools designed specifically for solo entrepreneurs and small businesses.",
                height=100,
                help="Enter the content you want to optimize"
            )
            
            platform = st.selectbox(
                "Target Platform",
                ["Twitter", "LinkedIn", "Facebook", "Instagram"],
                help="Which platform will you publish on?"
            )
        
        with col2:
            industry = st.text_input(
                "Your Industry",
                value="AI Content Creation",
                help="What industry are you in?"
            )
            
            competitor_urls = st.text_area(
                "Competitor URLs (one per line)",
                value="https://jasper.ai\nhttps://copy.ai\nhttps://writesonic.com",
                height=80,
                help="URLs of your main competitors"
            )
            
            your_strengths = st.text_input(
                "Your Key Strengths (comma-separated)",
                value="Personal touch, Agility, Niche expertise",
                help="What advantages do you have?"
            )
        
        # Process inputs
        urls = [url.strip() for url in competitor_urls.split('\n') if url.strip()]
        strengths = [s.strip() for s in your_strengths.split(',') if s.strip()] if your_strengths else []
        
        if st.button("🚀 Generate Integrated Strategy", type="primary"):
            if content and platform and urls and industry:
                with st.spinner("🧠 AI is creating your competitive content strategy..."):
                    strategy_result = asyncio.run(
                        suite.get_competitive_content_strategy(
                            content, platform, urls, industry, strengths
                        )
                    )
                
                if 'error' not in strategy_result:
                    st.success("✅ Integrated strategy generated!")
                    
                    # Action Plan First (most important)
                    action_plan = strategy_result.get('action_plan', [])
                    if action_plan:
                        st.header("📋 Your Action Plan")
                        st.markdown("**Do these actions in order for maximum impact:**")
                        
                        for i, action in enumerate(action_plan):
                            with st.expander(f"Action #{i+1}: {action.get('category', 'Action')} - {action.get('priority', 'Medium')} Priority"):
                                st.write(f"**What to do:** {action.get('action', 'N/A')}")
                                st.write(f"**Timeframe:** {action.get('timeframe', 'N/A')}")
                                st.write(f"**Source:** {action.get('source', 'N/A')}")
                    
                    # Integrated Strategy
                    integrated = strategy_result.get('integrated_strategy', {})
                    if integrated:
                        st.header("🧠 Integrated Strategy")
                        
                        # Key recommendations
                        optimization_recs = integrated.get('optimization_recommendations', [])
                        if optimization_recs:
                            st.subheader("🎯 Content Optimization")
                            for rec in optimization_recs:
                                st.info(f"💡 {rec}")
                        
                        # Positioning strategy
                        positioning = integrated.get('competitive_positioning', '')
                        if positioning:
                            st.subheader("🏆 Competitive Positioning")
                            st.success(f"📍 {positioning}")
                        
                        # Performance tactics
                        tactics = integrated.get('performance_tactics', [])
                        if tactics:
                            st.subheader("⚡ Performance Tactics")
                            for tactic in tactics:
                                st.write(f"• {tactic}")
                    
                    # Detailed analyses in expandable sections
                    with st.expander("📊 Content Performance Analysis"):
                        performance = strategy_result.get('content_performance', {})
                        predictions = performance.get('predictions', {})
                        
                        if predictions:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Engagement Score", f"{predictions.get('engagement_score', 0)}/10")
                            with col2:
                                st.metric("Virality Potential", f"{predictions.get('virality_potential', 0)}/10")
                            with col3:
                                st.metric("Platform Fit", f"{predictions.get('platform_optimization', 0)}/10")
                        
                        recommendations = performance.get('recommendations', [])
                        if recommendations:
                            st.write("**Performance Recommendations:**")
                            for rec in recommendations:
                                st.write(f"• {rec}")
                    
                    with st.expander("🕵️ Competitive Intelligence"):
                        competitive = strategy_result.get('competitive_intelligence', {})
                        insights = competitive.get('competitor_insights', {})
                        
                        key_insights = insights.get('key_insights', [])
                        if key_insights:
                            st.write("**Key Competitive Insights:**")
                            for insight in key_insights[:3]:
                                st.write(f"• {insight}")
                        
                        quick_wins = competitive.get('quick_wins', [])
                        if quick_wins:
                            st.write("**Quick Competitive Wins:**")
                            for win in quick_wins[:3]:
                                if isinstance(win, dict):
                                    st.write(f"• {win.get('action', win)}")
                                else:
                                    st.write(f"• {win}")
                    
                    with st.expander("🤖 Complete Strategic Analysis"):
                        full_strategy = integrated.get('full_strategy', 'No detailed strategy available')
                        st.write(full_strategy)
                
                else:
                    st.error(f"❌ Strategy generation failed: {strategy_result.get('error')}")
            else:
                st.warning("⚠️ Please fill in all required fields")
    
    # Footer
    st.markdown("---")
    st.markdown("**💡 Pro Tip:** Use all three tools together for maximum competitive advantage. Start with the integrated strategy for best results!")


# Main execution
if __name__ == "__main__":
    render_bootstrap_ai_suite() 