"""
AI-Powered Competitive Intelligence

Advanced competitive intelligence for entrepreneurs using AI.
Provides strategic insights, competitor analysis, and market opportunities.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from loguru import logger
import streamlit as st
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# Import existing Alwrity modules
from lib.ai_seo_tools.content_gap_analysis.competitor_analyzer import CompetitorAnalyzer
from lib.ai_web_researcher.gpt_online_researcher import do_google_pytrends_analysis
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen


class AICompetitiveIntelligence:
    """
    AI-powered competitive intelligence for entrepreneurs and startups.
    Uses existing AI capabilities to provide strategic insights.
    """
    
    def __init__(self):
        """Initialize the AI competitive intelligence."""
        self.competitor_analyzer = CompetitorAnalyzer()
        self.analysis_history = []
        
        logger.info("AI Competitive Intelligence initialized")
    
    async def analyze_competitors(
        self, 
        competitor_urls: List[str], 
        industry: str,
        your_strengths: List[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze competitors using AI-powered insights.
        
        Args:
            competitor_urls: List of competitor URLs
            industry: Your industry/niche
            your_strengths: Your current strengths (optional)
            
        Returns:
            AI-powered competitive analysis
        """
        logger.info(f"Starting AI competitive analysis for {len(competitor_urls)} competitors")
        
        try:
            analysis_report = {
                'analysis_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'competitors_analyzed': len(competitor_urls),
                    'industry': industry,
                    'your_strengths': your_strengths or []
                },
                'competitor_insights': {},
                'strategic_opportunities': [],
                'content_gap_analysis': {},
                'ai_recommendations': [],
                'quick_wins': [],
                'competitive_positioning': {}
            }
            
            # Step 1: Basic competitor analysis using existing tools
            st.info("🔍 Analyzing competitor basics...")
            basic_analysis = self.competitor_analyzer.analyze(competitor_urls, industry)
            
            # Step 2: AI-powered deep analysis
            st.info("🧠 AI is analyzing competitive landscape...")
            ai_insights = await self._get_ai_competitive_insights(
                competitor_urls, industry, basic_analysis, your_strengths
            )
            
            # Step 3: Content gap opportunities
            st.info("🎯 Identifying content opportunities...")
            content_opportunities = await self._find_content_opportunities(
                competitor_urls, industry, basic_analysis
            )
            
            # Step 4: Strategic recommendations
            st.info("💡 Generating strategic recommendations...")
            strategic_recommendations = await self._generate_strategic_recommendations(
                competitor_urls, industry, ai_insights, content_opportunities, your_strengths
            )
            
            # Compile results
            analysis_report.update({
                'competitor_insights': ai_insights,
                'content_gap_analysis': content_opportunities,
                'ai_recommendations': strategic_recommendations,
                'quick_wins': self._extract_quick_wins(strategic_recommendations),
                'competitive_positioning': self._analyze_positioning(ai_insights, your_strengths)
            })
            
            # Save to history
            self.analysis_history.append({
                'timestamp': datetime.now().isoformat(),
                'industry': industry,
                'competitors_count': len(competitor_urls),
                'report_id': f"{industry}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            })
            
            logger.info("AI competitive analysis completed successfully")
            return analysis_report
            
        except Exception as e:
            error_msg = f"Error in competitive analysis: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'error': error_msg}
    
    async def _get_ai_competitive_insights(
        self, 
        competitor_urls: List[str], 
        industry: str, 
        basic_analysis: Dict[str, Any],
        your_strengths: List[str] = None
    ) -> Dict[str, Any]:
        """Get AI-powered competitive insights."""
        
        competitors_list = [urlparse(url).netloc for url in competitor_urls]
        your_strengths_str = ', '.join(your_strengths) if your_strengths else "Not specified"
        
        insights_prompt = f"""
        You are a competitive intelligence expert analyzing the {industry} market.
        
        COMPETITORS TO ANALYZE:
        {', '.join(competitors_list)}
        
        BASIC COMPETITIVE ANALYSIS DATA:
        {json.dumps(basic_analysis, indent=2)[:3000]}
        
        YOUR CURRENT STRENGTHS:
        {your_strengths_str}
        
        Please provide a comprehensive competitive analysis with these insights:
        
        1. MARKET LANDSCAPE OVERVIEW:
           - Who are the dominant players?
           - What's the competitive intensity like?
           - What are the key market trends?
           - Where are the market gaps?
        
        2. COMPETITOR STRENGTHS & WEAKNESSES:
           For each major competitor, identify:
           - Their main competitive advantages
           - Their key weaknesses or blind spots
           - Their content strategy approach
           - Their target audience focus
        
        3. DIFFERENTIATION OPPORTUNITIES:
           - How can you position differently?
           - What unique value can you offer?
           - Which competitor weaknesses can you exploit?
           - What underserved market segments exist?
        
        4. THREAT ASSESSMENT:
           - Which competitors pose the biggest threat to you?
           - What are they doing better than you?
           - Where are they vulnerable?
           - How quickly are they evolving?
        
        5. STRATEGIC INSIGHTS:
           - What patterns do you see across all competitors?
           - What are they all missing that you could provide?
           - Where is the market heading?
           - What first-mover opportunities exist?
        
        Provide specific, actionable insights that a solo entrepreneur can use to compete effectively.
        Focus on realistic strategies that don't require massive resources.
        """
        
        try:
            ai_insights = llm_text_gen(
                insights_prompt,
                system_prompt="You are a strategic business consultant specializing in competitive analysis for startups and small businesses. Provide practical, actionable insights."
            )
            
            return {
                'full_analysis': ai_insights,
                'key_insights': self._extract_key_insights(ai_insights),
                'threat_levels': self._assess_threat_levels(ai_insights, competitors_list),
                'opportunities': self._extract_opportunities(ai_insights)
            }
            
        except Exception as e:
            logger.error(f"Error getting AI insights: {str(e)}")
            return {
                'full_analysis': f"Error generating insights: {str(e)}",
                'key_insights': ["Unable to generate AI insights"],
                'threat_levels': {},
                'opportunities': []
            }
    
    async def _find_content_opportunities(
        self, 
        competitor_urls: List[str], 
        industry: str, 
        basic_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Find content opportunities using AI analysis."""
        
        content_gaps = basic_analysis.get('content_gaps', [])
        advantages = basic_analysis.get('advantages', [])
        
        content_prompt = f"""
        Analyze content opportunities in the {industry} space based on competitor analysis:
        
        COMPETITOR CONTENT GAPS IDENTIFIED:
        {json.dumps(content_gaps[:10], indent=2)}
        
        COMPETITOR ADVANTAGES:
        {json.dumps(advantages[:10], indent=2)}
        
        INDUSTRY: {industry}
        
        Provide specific content opportunities analysis:
        
        1. HIGH-PRIORITY CONTENT GAPS:
           - What topics are competitors not covering well?
           - What questions are audiences asking that aren't being answered?
           - What content formats are underutilized?
           - What pain points are being ignored?
        
        2. CONTENT DIFFERENTIATION OPPORTUNITIES:
           - How can you approach common topics differently?
           - What unique perspective can you bring?
           - What content formats can you innovate with?
           - How can you provide more value than competitors?
        
        3. TRENDING CONTENT OPPORTUNITIES:
           - What emerging topics should you cover first?
           - What seasonal content opportunities exist?
           - What industry changes create content needs?
           - What tools/technologies need better content coverage?
        
        4. AUDIENCE-SPECIFIC CONTENT GAPS:
           - Which audience segments are underserved?
           - What skill levels need better content?
           - What use cases are poorly addressed?
           - What demographics are being ignored?
        
        5. QUICK CONTENT WINS:
           - What content can you create quickly that competitors lack?
           - What simple explanations are missing from the market?
           - What FAQ content is needed but not provided?
           - What beginner content opportunities exist?
        
        Prioritize opportunities that a solo creator can realistically execute.
        """
        
        try:
            content_analysis = llm_text_gen(
                content_prompt,
                system_prompt="You are a content strategist specializing in competitive content analysis. Provide specific, actionable content opportunities."
            )
            
            return {
                'full_analysis': content_analysis,
                'priority_gaps': self._extract_priority_gaps(content_analysis),
                'quick_wins': self._extract_content_quick_wins(content_analysis),
                'differentiation_opportunities': self._extract_differentiation_opps(content_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error finding content opportunities: {str(e)}")
            return {
                'full_analysis': f"Error analyzing content opportunities: {str(e)}",
                'priority_gaps': content_gaps[:5],
                'quick_wins': [],
                'differentiation_opportunities': []
            }
    
    async def _generate_strategic_recommendations(
        self, 
        competitor_urls: List[str], 
        industry: str, 
        ai_insights: Dict[str, Any],
        content_opportunities: Dict[str, Any],
        your_strengths: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate strategic recommendations using AI."""
        
        your_strengths_str = ', '.join(your_strengths) if your_strengths else "Not specified"
        
        strategy_prompt = f"""
        Based on the competitive analysis, provide strategic recommendations for competing in {industry}:
        
        AI COMPETITIVE INSIGHTS:
        {ai_insights.get('full_analysis', '')[:2000]}
        
        CONTENT OPPORTUNITIES:
        {content_opportunities.get('full_analysis', '')[:2000]}
        
        YOUR CURRENT STRENGTHS:
        {your_strengths_str}
        
        BUDGET CONSTRAINT: Solo entrepreneur with limited resources
        
        Provide specific, actionable recommendations in these categories:
        
        1. IMMEDIATE ACTIONS (0-30 days):
           - What can you implement this week?
           - Which competitor weaknesses can you exploit quickly?
           - What low-cost marketing tactics should you try?
           - Which content should you create first?
        
        2. SHORT-TERM STRATEGY (1-3 months):
           - How should you position against competitors?
           - What features/content should you prioritize?
           - Which partnerships should you pursue?
           - How should you differentiate your messaging?
        
        3. MEDIUM-TERM POSITIONING (3-6 months):
           - How can you build sustainable competitive advantages?
           - Which market segments should you focus on?
           - What unique value proposition should you develop?
           - How can you build barriers to competition?
        
        4. RESOURCE ALLOCATION:
           - Where should you spend your limited time?
           - Which marketing channels offer best ROI?
           - What tools/software investments are worthwhile?
           - How should you prioritize feature development?
        
        5. COMPETITIVE DEFENSE:
           - How can you protect against competitor moves?
           - What should you do if competitors copy you?
           - How can you build customer loyalty?
           - What contingency plans should you have?
        
        For each recommendation:
        - Specify the exact action to take
        - Estimate time/resource requirements
        - Explain expected impact
        - Rate priority (High/Medium/Low)
        - Provide success metrics
        
        Focus on David vs Goliath strategies that work for solo entrepreneurs.
        """
        
        try:
            strategic_recommendations = llm_text_gen(
                strategy_prompt,
                system_prompt="You are a startup strategist specializing in helping solo entrepreneurs compete against established players. Provide practical, executable strategies."
            )
            
            return self._parse_strategic_recommendations(strategic_recommendations)
            
        except Exception as e:
            logger.error(f"Error generating strategic recommendations: {str(e)}")
            return [
                {
                    'category': 'Content Strategy',
                    'priority': 'High',
                    'timeframe': '0-30 days',
                    'action': 'Create content addressing competitor blind spots',
                    'expected_impact': 'Attract underserved audience segments',
                    'resources_needed': 'Time for content creation',
                    'success_metrics': 'Website traffic, engagement rates'
                }
            ]
    
    def _extract_key_insights(self, ai_analysis: str) -> List[str]:
        """Extract key insights from AI analysis."""
        insights = []
        
        # Simple parsing to extract key points
        lines = ai_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                insight = line.lstrip('•-* ').strip()
                if len(insight) > 20:  # Only substantial insights
                    insights.append(insight)
        
        return insights[:8]  # Return top 8 insights
    
    def _assess_threat_levels(self, ai_analysis: str, competitors: List[str]) -> Dict[str, str]:
        """Assess threat levels for each competitor."""
        threat_levels = {}
        
        # Simple heuristic based on AI analysis content
        for competitor in competitors:
            if competitor.lower() in ai_analysis.lower():
                if any(word in ai_analysis.lower() for word in ['dominant', 'leader', 'strong', 'established']):
                    threat_levels[competitor] = 'High'
                elif any(word in ai_analysis.lower() for word in ['weak', 'vulnerable', 'gaps', 'opportunity']):
                    threat_levels[competitor] = 'Low'
                else:
                    threat_levels[competitor] = 'Medium'
            else:
                threat_levels[competitor] = 'Medium'  # Default
        
        return threat_levels
    
    def _extract_opportunities(self, ai_analysis: str) -> List[str]:
        """Extract opportunities from AI analysis."""
        opportunities = []
        
        # Look for opportunity-related keywords
        opportunity_keywords = ['opportunity', 'gap', 'underserved', 'missing', 'lack', 'could', 'should']
        
        lines = ai_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in opportunity_keywords) and len(line) > 30:
                opportunities.append(line.lstrip('•-* ').strip())
        
        return opportunities[:6]  # Return top 6 opportunities
    
    def _extract_priority_gaps(self, content_analysis: str) -> List[str]:
        """Extract priority content gaps."""
        gaps = []
        
        # Look for gaps in the analysis
        gap_keywords = ['gap', 'missing', 'lack', 'absent', 'underserved', 'neglected']
        
        lines = content_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in gap_keywords) and len(line) > 20:
                gaps.append(line.lstrip('•-* ').strip())
        
        return gaps[:5]  # Top 5 priority gaps
    
    def _extract_content_quick_wins(self, content_analysis: str) -> List[str]:
        """Extract content quick wins."""
        quick_wins = []
        
        # Look for quick win indicators
        quick_keywords = ['quick', 'easy', 'simple', 'immediately', 'now', 'today']
        
        lines = content_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in quick_keywords) and len(line) > 15:
                quick_wins.append(line.lstrip('•-* ').strip())
        
        return quick_wins[:4]  # Top 4 quick wins
    
    def _extract_differentiation_opps(self, content_analysis: str) -> List[str]:
        """Extract differentiation opportunities."""
        diff_opps = []
        
        # Look for differentiation keywords
        diff_keywords = ['different', 'unique', 'innovative', 'better', 'superior', 'distinct']
        
        lines = content_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in diff_keywords) and len(line) > 20:
                diff_opps.append(line.lstrip('•-* ').strip())
        
        return diff_opps[:4]  # Top 4 differentiation opportunities
    
    def _parse_strategic_recommendations(self, recommendations: str) -> List[Dict[str, Any]]:
        """Parse strategic recommendations into structured format."""
        structured_recs = []
        
        # Split by sections and parse
        sections = recommendations.split('\n\n')
        
        for section in sections:
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) > 30:  # Substantial recommendations
                    structured_recs.append({
                        'category': 'Strategic Recommendation',
                        'priority': 'Medium',  # Default
                        'timeframe': 'Short-term',
                        'action': line.lstrip('•-* ').strip()[:300],  # Limit length
                        'expected_impact': 'Competitive advantage',
                        'resources_needed': 'Time and effort',
                        'success_metrics': 'Market position improvement'
                    })
        
        return structured_recs[:10]  # Return top 10 recommendations
    
    def _extract_quick_wins(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Extract quick wins from recommendations."""
        quick_wins = []
        
        for rec in recommendations:
            action = rec.get('action', '').lower()
            if any(word in action for word in ['quick', 'immediate', 'now', 'today', 'easy', 'simple']):
                quick_wins.append({
                    'action': rec.get('action', ''),
                    'timeframe': rec.get('timeframe', '0-30 days'),
                    'impact': rec.get('expected_impact', 'Quick improvement')
                })
        
        # Add some default quick wins if none found
        if len(quick_wins) < 3:
            quick_wins.extend([
                {
                    'action': 'Create content addressing competitor blind spots',
                    'timeframe': '1-2 weeks',
                    'impact': 'Immediate traffic from underserved topics'
                },
                {
                    'action': 'Optimize social media with competitor hashtag gaps',
                    'timeframe': '1 week',
                    'impact': 'Better discoverability'
                },
                {
                    'action': 'Set up Google Alerts for competitor mentions',
                    'timeframe': '1 day',
                    'impact': 'Real-time competitive intelligence'
                }
            ])
        
        return quick_wins[:5]  # Top 5 quick wins
    
    def _analyze_positioning(self, ai_insights: Dict[str, Any], your_strengths: List[str]) -> Dict[str, Any]:
        """Analyze competitive positioning."""
        return {
            'your_advantages': your_strengths or ['Agility', 'Personal touch', 'Niche focus'],
            'competitor_weaknesses': ai_insights.get('opportunities', [])[:3],
            'positioning_strategy': 'Focus on agility and personal service vs big competitors',
            'unique_value_prop': 'Personalized solutions that big players can\'t match'
        }
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of analysis activities."""
        return {
            'total_analyses': len(self.analysis_history),
            'recent_analyses': self.analysis_history[-3:] if self.analysis_history else [],
            'capabilities': [
                'AI-powered competitive insights',
                'Content gap analysis', 
                'Strategic recommendations',
                'Quick win identification',
                'Positioning strategy'
            ]
        }


# Streamlit interface for AI competitive intelligence
def render_ai_competitive_intelligence_ui():
    """Render the AI competitive intelligence interface."""
    st.title("🥷 AI Competitive Intelligence")
    st.markdown("AI-powered competitive analysis for solo entrepreneurs and bootstrapped startups")
    
    # Initialize intelligence engine
    if 'ai_intel' not in st.session_state:
        st.session_state.ai_intel = AICompetitiveIntelligence()
    
    intel_engine = st.session_state.ai_intel
    
    # Input section
    st.header("🎯 Competitor Analysis Setup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        industry = st.text_input(
            "Your Industry/Niche", 
            value="AI Content Creation",
            help="What industry are you competing in?"
        )
        
        competitor_urls = st.text_area(
            "Competitor URLs (one per line)",
            value="https://jasper.ai\nhttps://copy.ai\nhttps://writesonic.com",
            height=100,
            help="Enter competitor websites to analyze"
        )
    
    with col2:
        your_strengths = st.text_area(
            "Your Current Strengths (optional)",
            value="Personal touch, Agility, Niche expertise",
            height=100,
            help="What are your competitive advantages?"
        )
    
    # Process inputs
    urls = [url.strip() for url in competitor_urls.split('\n') if url.strip()]
    strengths = [s.strip() for s in your_strengths.split(',') if s.strip()] if your_strengths else []
    
    if st.button("🧠 Analyze Competitors", type="primary"):
        if urls and industry:
            with st.spinner("🕵️ AI is analyzing your competition..."):
                results = asyncio.run(
                    intel_engine.analyze_competitors(urls, industry, strengths)
                )
            
            if 'error' not in results:
                st.success("✅ Competitive analysis complete!")
                
                # Analysis overview
                metadata = results.get('analysis_metadata', {})
                st.header("📊 Analysis Overview")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Competitors Analyzed", metadata.get('competitors_analyzed', 0))
                with col2:
                    st.metric("Industry", metadata.get('industry', 'N/A'))
                with col3:
                    st.metric("Your Strengths", len(metadata.get('your_strengths', [])))
                
                # Quick wins first (most important for bootstrapped entrepreneurs)
                quick_wins = results.get('quick_wins', [])
                if quick_wins:
                    st.header("🚀 Quick Wins (Do These First!)")
                    
                    for i, win in enumerate(quick_wins):
                        with st.expander(f"Quick Win #{i+1}: {win.get('timeframe', 'N/A')}"):
                            st.write(f"**Action:** {win.get('action', 'N/A')}")
                            st.write(f"**Expected Impact:** {win.get('impact', 'N/A')}")
                            st.write(f"**Timeframe:** {win.get('timeframe', 'N/A')}")
                
                # Key competitive insights
                insights = results.get('competitor_insights', {})
                if insights:
                    st.header("🧠 AI Competitive Insights")
                    
                    key_insights = insights.get('key_insights', [])
                    for insight in key_insights[:5]:
                        st.info(f"💡 {insight}")
                    
                    # Threat levels
                    threat_levels = insights.get('threat_levels', {})
                    if threat_levels:
                        st.subheader("⚠️ Competitor Threat Assessment")
                        
                        for competitor, threat in threat_levels.items():
                            color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(threat, '⚪')
                            st.write(f"{color} **{competitor}**: {threat} threat level")
                
                # Content opportunities
                content_opps = results.get('content_gap_analysis', {})
                if content_opps:
                    st.header("✍️ Content Opportunities")
                    
                    priority_gaps = content_opps.get('priority_gaps', [])
                    if priority_gaps:
                        st.subheader("🎯 Priority Content Gaps")
                        for gap in priority_gaps[:4]:
                            st.write(f"• {gap}")
                    
                    quick_content_wins = content_opps.get('quick_wins', [])
                    if quick_content_wins:
                        st.subheader("⚡ Quick Content Wins")
                        for win in quick_content_wins[:3]:
                            st.write(f"• {win}")
                
                # Strategic recommendations
                recommendations = results.get('ai_recommendations', [])
                if recommendations:
                    st.header("🎯 Strategic Recommendations")
                    
                    for i, rec in enumerate(recommendations[:6]):
                        with st.expander(f"Strategy #{i+1}: {rec.get('category', 'Strategic Move')}"):
                            st.write(f"**Action:** {rec.get('action', 'N/A')}")
                            st.write(f"**Timeframe:** {rec.get('timeframe', 'N/A')}")
                            st.write(f"**Expected Impact:** {rec.get('expected_impact', 'N/A')}")
                            st.write(f"**Priority:** {rec.get('priority', 'Medium')}")
                
                # Competitive positioning
                positioning = results.get('competitive_positioning', {})
                if positioning:
                    st.header("🏆 Your Competitive Position")
                    
                    st.subheader("Your Key Advantages:")
                    for advantage in positioning.get('your_advantages', []):
                        st.write(f"✅ {advantage}")
                    
                    st.subheader("Competitor Weaknesses to Exploit:")
                    for weakness in positioning.get('competitor_weaknesses', []):
                        st.write(f"🎯 {weakness}")
                
                # Full AI analysis
                with st.expander("🤖 Complete AI Analysis"):
                    ai_analysis = insights.get('full_analysis', 'No detailed analysis available')
                    st.write(ai_analysis)
                
                # Export functionality
                st.subheader("📥 Export Analysis")
                if st.button("Download Report"):
                    report_json = json.dumps(results, indent=2, default=str)
                    st.download_button(
                        label="Download JSON Report",
                        data=report_json,
                        file_name=f"competitor_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            else:
                st.error(f"❌ Analysis failed: {results.get('error')}")
        else:
            st.warning("⚠️ Please provide competitor URLs and industry information")
    
    # Sidebar with tips
    st.sidebar.header("💡 AI Competition Tips")
    st.sidebar.info("""
    **David vs Goliath Strategies:**
    
    • Focus on what big competitors can't do
    • Be more personal and responsive  
    • Serve niche audiences they ignore
    • Move faster than they can
    • Provide better customer service
    • Build deeper relationships
    • Innovate in areas they neglect
    """)
    
    # Analysis history
    summary = intel_engine.get_analysis_summary()
    st.sidebar.metric("Total Analyses", summary.get('total_analyses', 0))


# Main execution
if __name__ == "__main__":
    render_ai_competitive_intelligence_ui() 