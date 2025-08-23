"""
AI Insights Service for GSC and Google Trends Analysis

This service uses Google's Gemini AI to provide intelligent insights by analyzing
the combination of Google Search Console performance data and Google Trends data.
It generates actionable recommendations, identifies patterns, and provides strategic
content optimization suggestions.

Features:
- Combined GSC + Trends analysis
- Intelligent pattern recognition
- Strategic content recommendations
- Opportunity identification
- Competitive intelligence insights
- Seasonal optimization strategies
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

from services.logging_service import ai_logger
from services.google_trends_service import TrendData, SeasonalInsight, TrendComparison
from services.gsc_website_audit_service import AuditReport, PagePerformance, QueryPerformance

logger = logging.getLogger(__name__)

@dataclass
class AIInsight:
    """Data class for AI-generated insights."""
    insight_type: str
    title: str
    description: str
    priority: str
    confidence_score: float
    action_items: List[str]
    expected_impact: str
    timeframe: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

@dataclass
class ContentStrategy:
    """Data class for AI-generated content strategy."""
    strategy_type: str
    primary_keywords: List[str]
    content_themes: List[str]
    seasonal_calendar: Dict[str, List[str]]
    competitive_gaps: List[str]
    trending_opportunities: List[str]
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

@dataclass
class CombinedAnalysis:
    """Data class for comprehensive combined analysis."""
    analysis_date: datetime
    site_url: str
    executive_summary: str
    key_insights: List[AIInsight]
    content_strategy: ContentStrategy
    performance_forecast: Dict[str, Any]
    action_plan: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result['analysis_date'] = self.analysis_date.isoformat()
        return result

class AIInsightsService:
    """
    AI-powered insights service for website audit analysis.
    
    Combines GSC performance data with Google Trends insights to generate
    intelligent recommendations using Gemini AI.
    """
    
    def __init__(self):
        self.max_tokens = 8192
        self.temperature = 0.7
        
    async def generate_comprehensive_insights(
        self,
        gsc_report: AuditReport,
        trends_data: List[TrendData],
        seasonal_insights: List[SeasonalInsight],
        trend_comparisons: List[TrendComparison]
    ) -> CombinedAnalysis:
        """
        Generate comprehensive AI insights from combined GSC and Trends data.
        
        Args:
            gsc_report: Complete GSC audit report
            trends_data: Google Trends data for key queries
            seasonal_insights: Seasonal pattern analysis
            trend_comparisons: Query comparison analysis
            
        Returns:
            CombinedAnalysis with AI-generated insights and recommendations
        """
        try:
            ai_logger.info_connection_event(
                "ai_analysis_started", "gemini", 0,
                {"site_url": gsc_report.site_url, "queries_analyzed": len(trends_data)}
            )
            
            # Prepare data for AI analysis
            analysis_data = self._prepare_analysis_data(
                gsc_report, trends_data, seasonal_insights, trend_comparisons
            )
            
            # Generate insights using Gemini
            insights = await self._generate_insights_with_gemini(analysis_data)
            
            # Generate content strategy
            content_strategy = await self._generate_content_strategy(analysis_data, insights)
            
            # Generate performance forecast
            forecast = await self._generate_performance_forecast(analysis_data)
            
            # Create action plan
            action_plan = await self._create_action_plan(insights, content_strategy)
            
            # Assess risks
            risk_assessment = await self._assess_risks(analysis_data)
            
            # Create executive summary
            executive_summary = await self._create_executive_summary(
                analysis_data, insights, content_strategy
            )
            
            combined_analysis = CombinedAnalysis(
                analysis_date=datetime.utcnow(),
                site_url=gsc_report.site_url,
                executive_summary=executive_summary,
                key_insights=insights,
                content_strategy=content_strategy,
                performance_forecast=forecast,
                action_plan=action_plan,
                risk_assessment=risk_assessment
            )
            
            ai_logger.info_connection_event(
                "ai_analysis_completed", "gemini", 0,
                {"site_url": gsc_report.site_url, "insights_generated": len(insights)}
            )
            
            return combined_analysis
            
        except Exception as e:
            ai_logger.error_platform_api(
                "gemini", "comprehensive_analysis", e,
                {"site_url": gsc_report.site_url}
            )
            raise

    def _prepare_analysis_data(
        self,
        gsc_report: AuditReport,
        trends_data: List[TrendData],
        seasonal_insights: List[SeasonalInsight],
        trend_comparisons: List[TrendComparison]
    ) -> Dict[str, Any]:
        """Prepare structured data for AI analysis."""
        
        return {
            "gsc_summary": {
                "total_pages": gsc_report.total_pages,
                "total_queries": gsc_report.total_queries,
                "total_impressions": gsc_report.total_impressions,
                "total_clicks": gsc_report.total_clicks,
                "average_ctr": gsc_report.average_ctr,
                "average_position": gsc_report.average_position,
                "date_range": gsc_report.date_range
            },
            "performance_categories": {
                "top_performers": [
                    {
                        "url": page.url,
                        "clicks": page.metrics.clicks,
                        "impressions": page.metrics.impressions,
                        "ctr": page.metrics.ctr,
                        "position": page.metrics.position
                    }
                    for page in gsc_report.top_performers[:10]
                ],
                "low_hanging_fruit": [
                    {
                        "url": page.url,
                        "clicks": page.metrics.clicks,
                        "impressions": page.metrics.impressions,
                        "ctr": page.metrics.ctr,
                        "position": page.metrics.position
                    }
                    for page in gsc_report.low_hanging_fruit[:10]
                ],
                "striking_distance": [
                    {
                        "query": query.query,
                        "position": query.metrics.position,
                        "impressions": query.metrics.impressions,
                        "intent_type": query.intent_type
                    }
                    for query in gsc_report.striking_distance[:15]
                ]
            },
            "content_clusters": [
                {
                    "topic": cluster.topic,
                    "page_count": len(cluster.pages),
                    "total_clicks": cluster.total_metrics.clicks,
                    "performance_score": cluster.performance_score
                }
                for cluster in gsc_report.content_clusters[:10]
            ],
            "trends_analysis": [
                {
                    "query": trend.query,
                    "average_interest": trend.average_interest,
                    "trend_direction": trend.trend_direction,
                    "seasonal_pattern": trend.seasonal_pattern,
                    "related_queries": trend.related_queries[:5],
                    "rising_queries": trend.rising_queries[:5]
                }
                for trend in trends_data
            ],
            "seasonal_patterns": [
                {
                    "query": insight.query,
                    "peak_months": insight.peak_months,
                    "pattern_type": insight.pattern_type,
                    "seasonality_score": insight.seasonality_score
                }
                for insight in seasonal_insights
            ],
            "trend_comparisons": [
                {
                    "queries": comparison.queries,
                    "winner": comparison.winner,
                    "insights": comparison.insights
                }
                for comparison in trend_comparisons
            ]
        }

    async def _generate_insights_with_gemini(
        self,
        analysis_data: Dict[str, Any]
    ) -> List[AIInsight]:
        """Generate insights using Gemini AI with structured output."""
        
        try:
            # Import Gemini provider
            from services.ai_providers.gemini_provider import gemini_provider
            
            prompt = self._create_insights_prompt(analysis_data)
            
            # Define the expected JSON schema for insights
            schema = {
                "type": "object",
                "properties": {
                    "insights": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "insight_type": {"type": "string"},
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                                "confidence_score": {"type": "number", "minimum": 0, "maximum": 1},
                                "action_items": {"type": "array", "items": {"type": "string"}},
                                "expected_impact": {"type": "string"},
                                "timeframe": {"type": "string"}
                            },
                            "required": ["insight_type", "title", "description", "priority", "confidence_score", "action_items", "expected_impact", "timeframe"]
                        }
                    }
                },
                "required": ["insights"]
            }
            
            # Get structured response from Gemini
            response = await gemini_provider.get_structured_response(
                prompt=prompt,
                schema=schema,
                temperature=self.temperature
            )
            
            # Convert to AIInsight objects
            insights = []
            for insight_data in response.get("insights", []):
                insight = AIInsight(**insight_data)
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights with Gemini: {e}")
            # Return fallback insights
            return self._generate_fallback_insights(analysis_data)

    def _create_insights_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for AI insight generation."""
        
        prompt = f"""
You are an expert SEO and content strategy analyst. Analyze the following combined Google Search Console and Google Trends data to generate actionable insights.

GSC PERFORMANCE DATA:
- Total Pages: {analysis_data['gsc_summary']['total_pages']}
- Total Queries: {analysis_data['gsc_summary']['total_queries']}
- Total Impressions: {analysis_data['gsc_summary']['total_impressions']:,}
- Total Clicks: {analysis_data['gsc_summary']['total_clicks']:,}
- Average CTR: {analysis_data['gsc_summary']['average_ctr']:.2f}%
- Average Position: {analysis_data['gsc_summary']['average_position']:.1f}

TOP PERFORMING CONTENT:
{self._format_pages_data(analysis_data['performance_categories']['top_performers'])}

LOW HANGING FRUIT OPPORTUNITIES:
{self._format_pages_data(analysis_data['performance_categories']['low_hanging_fruit'])}

STRIKING DISTANCE QUERIES:
{self._format_queries_data(analysis_data['performance_categories']['striking_distance'])}

CONTENT CLUSTERS:
{self._format_clusters_data(analysis_data['content_clusters'])}

GOOGLE TRENDS ANALYSIS:
{self._format_trends_data(analysis_data['trends_analysis'])}

SEASONAL PATTERNS:
{self._format_seasonal_data(analysis_data['seasonal_patterns'])}

TREND COMPARISONS:
{self._format_comparison_data(analysis_data['trend_comparisons'])}

Generate 5-8 strategic insights that combine both GSC performance and Google Trends data. Focus on:

1. PERFORMANCE OPTIMIZATION: Identify specific opportunities to improve CTR, rankings, and traffic
2. CONTENT GAPS: Discover trending topics not adequately covered
3. SEASONAL STRATEGIES: Leverage seasonal patterns for content planning
4. COMPETITIVE OPPORTUNITIES: Identify rising trends to capitalize on
5. RISK MITIGATION: Spot declining trends that may impact performance
6. QUICK WINS: Immediate optimization opportunities
7. LONG-TERM STRATEGY: Strategic content development recommendations

For each insight, provide:
- Clear insight type (performance_optimization, content_gap, seasonal_strategy, etc.)
- Compelling title
- Detailed description explaining the finding
- Priority level (high/medium/low)
- Confidence score (0.0-1.0)
- Specific action items
- Expected impact description
- Implementation timeframe

Ensure insights are data-driven, actionable, and combine both GSC and Trends intelligence.
"""
        
        return prompt

    def _format_pages_data(self, pages: List[Dict[str, Any]]) -> str:
        """Format pages data for prompt."""
        if not pages:
            return "No data available"
        
        formatted = []
        for page in pages[:5]:  # Limit to top 5
            formatted.append(
                f"- {page['url'][:60]}... | Clicks: {page['clicks']} | CTR: {page['ctr']:.1f}% | Pos: {page['position']:.1f}"
            )
        return "\n".join(formatted)

    def _format_queries_data(self, queries: List[Dict[str, Any]]) -> str:
        """Format queries data for prompt."""
        if not queries:
            return "No data available"
        
        formatted = []
        for query in queries[:10]:  # Limit to top 10
            formatted.append(
                f"- '{query['query']}' | Pos: {query['position']:.1f} | Impressions: {query['impressions']} | Intent: {query['intent_type']}"
            )
        return "\n".join(formatted)

    def _format_clusters_data(self, clusters: List[Dict[str, Any]]) -> str:
        """Format clusters data for prompt."""
        if not clusters:
            return "No data available"
        
        formatted = []
        for cluster in clusters[:5]:  # Limit to top 5
            formatted.append(
                f"- Topic: {cluster['topic']} | Pages: {cluster['page_count']} | Clicks: {cluster['total_clicks']} | Score: {cluster['performance_score']:.1f}/10"
            )
        return "\n".join(formatted)

    def _format_trends_data(self, trends: List[Dict[str, Any]]) -> str:
        """Format trends data for prompt."""
        if not trends:
            return "No data available"
        
        formatted = []
        for trend in trends:
            related = ", ".join([q['query'] for q in trend['related_queries'][:3]])
            rising = ", ".join([q['query'] for q in trend['rising_queries'][:3]])
            
            formatted.append(
                f"- Query: '{trend['query']}' | Avg Interest: {trend['average_interest']} | Trend: {trend['trend_direction']} | Pattern: {trend['seasonal_pattern']}"
            )
            if related:
                formatted.append(f"  Related: {related}")
            if rising:
                formatted.append(f"  Rising: {rising}")
        
        return "\n".join(formatted)

    def _format_seasonal_data(self, seasonal: List[Dict[str, Any]]) -> str:
        """Format seasonal data for prompt."""
        if not seasonal:
            return "No data available"
        
        formatted = []
        for insight in seasonal:
            formatted.append(
                f"- '{insight['query']}' | Pattern: {insight['pattern_type']} | Peak: {', '.join(insight['peak_months'][:2])} | Score: {insight['seasonality_score']}"
            )
        return "\n".join(formatted)

    def _format_comparison_data(self, comparisons: List[Dict[str, Any]]) -> str:
        """Format comparison data for prompt."""
        if not comparisons:
            return "No data available"
        
        formatted = []
        for comp in comparisons:
            formatted.append(
                f"- Compared: {', '.join(comp['queries'])} | Winner: '{comp['winner']}'"
            )
            for insight in comp['insights'][:2]:  # Top 2 insights
                formatted.append(f"  {insight}")
        
        return "\n".join(formatted)

    async def _generate_content_strategy(
        self,
        analysis_data: Dict[str, Any],
        insights: List[AIInsight]
    ) -> ContentStrategy:
        """Generate content strategy using Gemini AI."""
        
        try:
            from services.ai_providers.gemini_provider import gemini_provider
            
            prompt = f"""
Based on the previous analysis and the following insights, create a comprehensive content strategy:

GENERATED INSIGHTS:
{self._format_insights_for_strategy(insights)}

TRENDS DATA:
{self._format_trends_data(analysis_data['trends_analysis'])}

SEASONAL PATTERNS:
{self._format_seasonal_data(analysis_data['seasonal_patterns'])}

Create a strategic content plan that includes:
1. Primary keywords to focus on based on GSC performance and trends
2. Content themes that align with trending topics and performance gaps
3. Monthly seasonal calendar for content planning
4. Competitive gaps identified from the analysis
5. Trending opportunities to capitalize on
6. Specific actionable recommendations

Ensure the strategy combines both current performance data and future trend predictions.
"""
            
            schema = {
                "type": "object",
                "properties": {
                    "strategy_type": {"type": "string"},
                    "primary_keywords": {"type": "array", "items": {"type": "string"}},
                    "content_themes": {"type": "array", "items": {"type": "string"}},
                    "seasonal_calendar": {
                        "type": "object",
                        "additionalProperties": {"type": "array", "items": {"type": "string"}}
                    },
                    "competitive_gaps": {"type": "array", "items": {"type": "string"}},
                    "trending_opportunities": {"type": "array", "items": {"type": "string"}},
                    "recommendations": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["strategy_type", "primary_keywords", "content_themes", "seasonal_calendar", "competitive_gaps", "trending_opportunities", "recommendations"]
            }
            
            response = await gemini_provider.get_structured_response(
                prompt=prompt,
                schema=schema,
                temperature=self.temperature
            )
            
            return ContentStrategy(**response)
            
        except Exception as e:
            logger.error(f"Error generating content strategy: {e}")
            return self._generate_fallback_strategy(analysis_data)

    def _format_insights_for_strategy(self, insights: List[AIInsight]) -> str:
        """Format insights for strategy generation."""
        formatted = []
        for insight in insights:
            formatted.append(f"- {insight.title}: {insight.description[:100]}...")
        return "\n".join(formatted)

    async def _generate_performance_forecast(
        self,
        analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate performance forecast based on trends and GSC data."""
        
        try:
            from services.ai_providers.gemini_provider import gemini_provider
            
            prompt = f"""
Based on the current GSC performance and Google Trends data, provide a 6-month performance forecast:

CURRENT PERFORMANCE:
- Current CTR: {analysis_data['gsc_summary']['average_ctr']:.2f}%
- Current Position: {analysis_data['gsc_summary']['average_position']:.1f}
- Monthly Clicks: {analysis_data['gsc_summary']['total_clicks']:,}

TREND DIRECTIONS:
{self._format_trends_data(analysis_data['trends_analysis'])}

Provide realistic forecasts for:
1. Expected CTR improvement
2. Position improvements
3. Traffic growth potential
4. Seasonal impact predictions
5. Risk factors

Be conservative but optimistic in projections.
"""
            
            schema = {
                "type": "object",
                "properties": {
                    "forecast_period": {"type": "string"},
                    "expected_ctr_improvement": {"type": "number"},
                    "expected_position_improvement": {"type": "number"},
                    "traffic_growth_potential": {"type": "number"},
                    "seasonal_impact": {"type": "string"},
                    "confidence_level": {"type": "string"},
                    "key_assumptions": {"type": "array", "items": {"type": "string"}},
                    "risk_factors": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["forecast_period", "expected_ctr_improvement", "expected_position_improvement", "traffic_growth_potential", "seasonal_impact", "confidence_level", "key_assumptions", "risk_factors"]
            }
            
            response = await gemini_provider.get_structured_response(
                prompt=prompt,
                schema=schema,
                temperature=0.5  # Lower temperature for forecasts
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating forecast: {e}")
            return {
                "forecast_period": "6 months",
                "expected_ctr_improvement": 0.5,
                "expected_position_improvement": 2.0,
                "traffic_growth_potential": 15.0,
                "seasonal_impact": "Moderate seasonal variations expected",
                "confidence_level": "Medium",
                "key_assumptions": ["Consistent optimization efforts", "No major algorithm changes"],
                "risk_factors": ["Competition increase", "Seasonal downturns"]
            }

    async def _create_action_plan(
        self,
        insights: List[AIInsight],
        content_strategy: ContentStrategy
    ) -> List[Dict[str, Any]]:
        """Create prioritized action plan from insights and strategy."""
        
        action_plan = []
        
        # Sort insights by priority and confidence
        sorted_insights = sorted(
            insights,
            key=lambda x: (
                {"high": 3, "medium": 2, "low": 1}[x.priority],
                x.confidence_score
            ),
            reverse=True
        )
        
        for i, insight in enumerate(sorted_insights):
            action_plan.append({
                "order": i + 1,
                "title": insight.title,
                "description": insight.description,
                "action_items": insight.action_items,
                "priority": insight.priority,
                "timeframe": insight.timeframe,
                "expected_impact": insight.expected_impact,
                "confidence_score": insight.confidence_score,
                "category": insight.insight_type
            })
        
        return action_plan

    async def _assess_risks(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess potential risks from the analysis."""
        
        risks = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "mitigation_strategies": []
        }
        
        # Analyze declining trends
        declining_trends = [
            trend for trend in analysis_data['trends_analysis']
            if trend['trend_direction'] == 'declining'
        ]
        
        if declining_trends:
            risks["high_risk"].append({
                "risk": "Declining search interest",
                "details": f"{len(declining_trends)} queries showing declining trends",
                "impact": "Potential traffic reduction"
            })
        
        # Check for low CTR
        avg_ctr = analysis_data['gsc_summary']['average_ctr']
        if avg_ctr < 2.0:
            risks["medium_risk"].append({
                "risk": "Low click-through rate",
                "details": f"Current CTR {avg_ctr:.2f}% below industry average",
                "impact": "Missing traffic opportunities"
            })
        
        # Check for high average position
        avg_position = analysis_data['gsc_summary']['average_position']
        if avg_position > 10:
            risks["medium_risk"].append({
                "risk": "Poor search rankings",
                "details": f"Average position {avg_position:.1f} on second page",
                "impact": "Limited visibility and traffic"
            })
        
        # Add mitigation strategies
        risks["mitigation_strategies"] = [
            "Monitor declining trends closely and create fresh content",
            "Optimize title tags and meta descriptions for better CTR",
            "Focus on striking distance keywords for quick ranking wins",
            "Diversify content strategy across multiple trending topics"
        ]
        
        return risks

    async def _create_executive_summary(
        self,
        analysis_data: Dict[str, Any],
        insights: List[AIInsight],
        content_strategy: ContentStrategy
    ) -> str:
        """Create executive summary of the analysis."""
        
        try:
            from services.ai_providers.gemini_provider import gemini_provider
            
            high_priority_insights = [i for i in insights if i.priority == "high"]
            
            prompt = f"""
Create a concise executive summary for website performance analysis:

CURRENT PERFORMANCE:
- {analysis_data['gsc_summary']['total_pages']} pages analyzed
- {analysis_data['gsc_summary']['total_clicks']:,} monthly clicks
- {analysis_data['gsc_summary']['average_ctr']:.2f}% average CTR
- Position {analysis_data['gsc_summary']['average_position']:.1f} average ranking

KEY FINDINGS:
{len(high_priority_insights)} high-priority optimization opportunities identified
{len(content_strategy.trending_opportunities)} trending opportunities discovered
{len(content_strategy.competitive_gaps)} competitive gaps found

Write a professional 3-4 sentence executive summary highlighting the most important findings and opportunities.
"""
            
            response = await gemini_provider.generate_content_async(
                prompt,
                max_tokens=200,
                temperature=0.6
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error creating executive summary: {e}")
            return f"Analysis of {analysis_data['gsc_summary']['total_pages']} pages reveals {len(insights)} optimization opportunities with potential for significant performance improvement through strategic content optimization and trend-based targeting."

    def _generate_fallback_insights(self, analysis_data: Dict[str, Any]) -> List[AIInsight]:
        """Generate fallback insights when AI fails."""
        
        insights = []
        
        # CTR optimization insight
        if analysis_data['gsc_summary']['average_ctr'] < 3.0:
            insights.append(AIInsight(
                insight_type="performance_optimization",
                title="CTR Optimization Opportunity",
                description=f"Current average CTR of {analysis_data['gsc_summary']['average_ctr']:.2f}% is below industry standards. Significant traffic gains possible through title and meta description optimization.",
                priority="high",
                confidence_score=0.9,
                action_items=[
                    "Audit and rewrite title tags for top-performing pages",
                    "Optimize meta descriptions with compelling calls-to-action",
                    "Implement structured data for rich snippets"
                ],
                expected_impact="15-25% increase in organic traffic",
                timeframe="2-4 weeks"
            ))
        
        return insights

    def _generate_fallback_strategy(self, analysis_data: Dict[str, Any]) -> ContentStrategy:
        """Generate fallback content strategy when AI fails."""
        
        return ContentStrategy(
            strategy_type="optimization_focused",
            primary_keywords=[
                trend['query'] for trend in analysis_data['trends_analysis'][:5]
            ],
            content_themes=[
                "SEO optimization",
                "Content performance",
                "Search trends"
            ],
            seasonal_calendar={
                "Q1": ["Performance analysis", "Strategy planning"],
                "Q2": ["Content creation", "Optimization"],
                "Q3": ["Trend analysis", "Competitive research"],
                "Q4": ["Strategy review", "Planning for next year"]
            },
            competitive_gaps=["Technical SEO", "Content depth"],
            trending_opportunities=["Rising search queries", "Seasonal content"],
            recommendations=[
                "Focus on low-hanging fruit optimization",
                "Create content around trending topics",
                "Improve technical SEO foundation"
            ]
        )

# Global service instance
ai_insights_service = AIInsightsService()