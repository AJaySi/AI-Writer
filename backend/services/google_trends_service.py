"""
Google Trends Service

A comprehensive service for analyzing Google Trends data to augment GSC website audit insights.
This service provides search interest trends, related queries, rising trends, and seasonal patterns
to enhance content strategy and optimization recommendations.

Features:
- Search interest trends over time
- Related queries and topics
- Rising search trends
- Seasonal pattern analysis
- Geographic interest distribution
- Query comparison analysis
- Trend forecasting insights
"""

import asyncio
import time
import random
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np
from collections import defaultdict
import logging

from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError, ResponseError

from services.logging_service import trends_logger

logger = logging.getLogger(__name__)

@dataclass
class TrendData:
    """Data class for trend information."""
    query: str
    interest_over_time: List[Dict[str, Any]]
    average_interest: float
    peak_interest: int
    trend_direction: str
    seasonal_pattern: str
    related_queries: List[Dict[str, Any]]
    rising_queries: List[Dict[str, Any]]
    geographic_data: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

@dataclass
class TrendComparison:
    """Data class for comparing multiple trends."""
    queries: List[str]
    comparison_data: Dict[str, Any]
    winner: str
    insights: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

@dataclass
class SeasonalInsight:
    """Data class for seasonal analysis."""
    query: str
    peak_months: List[str]
    low_months: List[str]
    seasonality_score: float
    pattern_type: str
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

class GoogleTrendsService:
    """
    Comprehensive Google Trends analysis service.
    
    Provides search interest trends, related queries, and seasonal patterns
    to augment GSC data for enhanced website audit insights.
    """
    
    def __init__(self):
        self.pytrends = None
        self.max_retries = 3
        self.base_delay = 1
        self.geo_codes = {
            'US': 'United States',
            'GB': 'United Kingdom', 
            'CA': 'Canada',
            'AU': 'Australia',
            'DE': 'Germany',
            'FR': 'France',
            'JP': 'Japan',
            'IN': 'India'
        }
        
    async def initialize_client(self) -> None:
        """Initialize pytrends client with error handling."""
        try:
            self.pytrends = TrendReq(
                hl='en-US',
                tz=360,
                timeout=(10, 25),
                retries=2,
                backoff_factor=0.1
            )
            logger.info("Google Trends client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Trends client: {e}")
            raise

    async def get_trends_for_queries(
        self,
        queries: List[str],
        timeframe: str = 'today 12-m',
        geo: str = '',
        category: int = 0
    ) -> List[TrendData]:
        """
        Get comprehensive trend data for multiple queries.
        
        Args:
            queries: List of search queries to analyze
            timeframe: Time period for analysis (e.g., 'today 12-m', 'today 3-m')
            geo: Geographic region (e.g., 'US', 'GB', '')
            category: Google Trends category ID
            
        Returns:
            List of TrendData objects with comprehensive analysis
        """
        if not self.pytrends:
            await self.initialize_client()
        
        trends_data = []
        
        for query in queries:
            try:
                trend_data = await self._analyze_single_query(
                    query, timeframe, geo, category
                )
                if trend_data:
                    trends_data.append(trend_data)
                    
                # Rate limiting - random delay between requests
                await asyncio.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.warning(f"Failed to get trends for query '{query}': {e}")
                trends_logger.warning_security_event(
                    "trends_query_failed",
                    {"query": query, "error": str(e)}
                )
                continue
        
        return trends_data

    async def _analyze_single_query(
        self,
        query: str,
        timeframe: str,
        geo: str,
        category: int
    ) -> Optional[TrendData]:
        """Analyze a single query with comprehensive metrics."""
        
        for attempt in range(self.max_retries):
            try:
                # Build payload
                self.pytrends.build_payload(
                    [query],
                    cat=category,
                    timeframe=timeframe,
                    geo=geo,
                    gprop=''
                )
                
                # Get interest over time
                interest_data = await self._get_interest_over_time()
                
                # Get related queries
                related_data = await self._get_related_queries()
                
                # Get geographic data
                geo_data = await self._get_geographic_interest()
                
                # Analyze trends
                trend_analysis = self._analyze_trend_pattern(interest_data, query)
                
                # Create comprehensive trend data
                trend_data = TrendData(
                    query=query,
                    interest_over_time=interest_data,
                    average_interest=trend_analysis['average_interest'],
                    peak_interest=trend_analysis['peak_interest'],
                    trend_direction=trend_analysis['trend_direction'],
                    seasonal_pattern=trend_analysis['seasonal_pattern'],
                    related_queries=related_data.get('related', []),
                    rising_queries=related_data.get('rising', []),
                    geographic_data=geo_data
                )
                
                trends_logger.info_connection_event(
                    "trends_analysis_completed", "google_trends", 0,
                    {"query": query, "average_interest": trend_analysis['average_interest']}
                )
                
                return trend_data
                
            except TooManyRequestsError:
                delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                logger.warning(f"Rate limited. Retrying in {delay:.2f} seconds...")
                await asyncio.sleep(delay)
                continue
                
            except Exception as e:
                logger.error(f"Error analyzing query '{query}' on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    return None
                await asyncio.sleep(self.base_delay * (attempt + 1))
                continue
        
        return None

    async def _get_interest_over_time(self) -> List[Dict[str, Any]]:
        """Get interest over time data."""
        try:
            interest_df = self.pytrends.interest_over_time()
            
            if interest_df.empty:
                return []
            
            # Convert to list of dictionaries
            interest_data = []
            for date, row in interest_df.iterrows():
                query_col = [col for col in interest_df.columns if col != 'isPartial'][0]
                interest_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'interest': int(row[query_col]),
                    'is_partial': row.get('isPartial', False)
                })
            
            return interest_data
            
        except Exception as e:
            logger.error(f"Error getting interest over time: {e}")
            return []

    async def _get_related_queries(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get related and rising queries."""
        try:
            related_queries = self.pytrends.related_queries()
            
            result = {
                'related': [],
                'rising': []
            }
            
            for query, data in related_queries.items():
                if data.get('top') is not None:
                    result['related'] = [
                        {'query': row['query'], 'value': row['value']}
                        for _, row in data['top'].iterrows()
                    ]
                
                if data.get('rising') is not None:
                    result['rising'] = [
                        {'query': row['query'], 'value': row['value']}
                        for _, row in data['rising'].iterrows()
                    ]
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting related queries: {e}")
            return {'related': [], 'rising': []}

    async def _get_geographic_interest(self) -> List[Dict[str, Any]]:
        """Get geographic interest distribution."""
        try:
            geo_df = self.pytrends.interest_by_region(resolution='COUNTRY')
            
            if geo_df.empty:
                return []
            
            # Convert to list of dictionaries
            geo_data = []
            query_col = geo_df.columns[0]
            
            # Get top 10 countries
            top_countries = geo_df.nlargest(10, query_col)
            
            for country, row in top_countries.iterrows():
                geo_data.append({
                    'country': country,
                    'country_name': self.geo_codes.get(country, country),
                    'interest': int(row[query_col])
                })
            
            return geo_data
            
        except Exception as e:
            logger.error(f"Error getting geographic data: {e}")
            return []

    def _analyze_trend_pattern(
        self,
        interest_data: List[Dict[str, Any]],
        query: str
    ) -> Dict[str, Any]:
        """Analyze trend patterns and calculate insights."""
        
        if not interest_data:
            return {
                'average_interest': 0,
                'peak_interest': 0,
                'trend_direction': 'stable',
                'seasonal_pattern': 'no_data'
            }
        
        # Extract interest values
        interests = [point['interest'] for point in interest_data]
        
        # Calculate basic metrics
        average_interest = np.mean(interests)
        peak_interest = max(interests)
        
        # Determine trend direction
        if len(interests) >= 4:
            recent_avg = np.mean(interests[-4:])  # Last 4 data points
            earlier_avg = np.mean(interests[:4])   # First 4 data points
            
            if recent_avg > earlier_avg * 1.1:
                trend_direction = 'rising'
            elif recent_avg < earlier_avg * 0.9:
                trend_direction = 'declining'
            else:
                trend_direction = 'stable'
        else:
            trend_direction = 'insufficient_data'
        
        # Analyze seasonality (if we have enough data)
        seasonal_pattern = self._detect_seasonal_pattern(interests)
        
        return {
            'average_interest': round(average_interest, 2),
            'peak_interest': peak_interest,
            'trend_direction': trend_direction,
            'seasonal_pattern': seasonal_pattern
        }

    def _detect_seasonal_pattern(self, interests: List[int]) -> str:
        """Detect seasonal patterns in interest data."""
        
        if len(interests) < 12:  # Need at least 12 months for seasonal analysis
            return 'insufficient_data'
        
        try:
            # Convert to numpy array for analysis
            data = np.array(interests)
            
            # Calculate variance to determine if there's significant seasonality
            variance = np.var(data)
            mean_interest = np.mean(data)
            
            if variance < mean_interest * 0.1:  # Low variance
                return 'stable'
            
            # Look for quarterly patterns
            quarterly_averages = []
            for i in range(0, len(interests), 3):
                quarter = interests[i:i+3]
                if quarter:
                    quarterly_averages.append(np.mean(quarter))
            
            if len(quarterly_averages) >= 4:
                q_variance = np.var(quarterly_averages)
                if q_variance > mean_interest * 0.2:
                    return 'quarterly'
            
            # Look for monthly patterns (simplified)
            if variance > mean_interest * 0.3:
                return 'seasonal'
            else:
                return 'stable'
                
        except Exception as e:
            logger.error(f"Error detecting seasonal pattern: {e}")
            return 'unknown'

    async def compare_queries(
        self,
        queries: List[str],
        timeframe: str = 'today 12-m',
        geo: str = ''
    ) -> Optional[TrendComparison]:
        """
        Compare multiple queries to identify the most popular.
        
        Args:
            queries: List of queries to compare (max 5)
            timeframe: Time period for comparison
            geo: Geographic region
            
        Returns:
            TrendComparison object with analysis
        """
        if not self.pytrends:
            await self.initialize_client()
        
        if len(queries) > 5:
            queries = queries[:5]  # Google Trends limit
        
        try:
            self.pytrends.build_payload(
                queries,
                timeframe=timeframe,
                geo=geo
            )
            
            # Get comparison data
            interest_df = self.pytrends.interest_over_time()
            
            if interest_df.empty:
                return None
            
            # Calculate average interest for each query
            averages = {}
            comparison_data = {}
            
            for query in queries:
                if query in interest_df.columns:
                    avg_interest = interest_df[query].mean()
                    averages[query] = avg_interest
                    
                    comparison_data[query] = {
                        'average_interest': round(avg_interest, 2),
                        'peak_interest': int(interest_df[query].max()),
                        'trend_data': [
                            {
                                'date': date.strftime('%Y-%m-%d'),
                                'interest': int(interest_df.loc[date, query])
                            }
                            for date in interest_df.index
                        ]
                    }
            
            # Determine winner
            winner = max(averages.items(), key=lambda x: x[1])[0] if averages else queries[0]
            
            # Generate insights
            insights = self._generate_comparison_insights(averages, queries)
            
            return TrendComparison(
                queries=queries,
                comparison_data=comparison_data,
                winner=winner,
                insights=insights
            )
            
        except Exception as e:
            logger.error(f"Error comparing queries: {e}")
            return None

    def _generate_comparison_insights(
        self,
        averages: Dict[str, float],
        queries: List[str]
    ) -> List[str]:
        """Generate insights from query comparison."""
        
        insights = []
        
        if not averages:
            return ["No comparison data available"]
        
        # Sort by average interest
        sorted_queries = sorted(averages.items(), key=lambda x: x[1], reverse=True)
        
        winner = sorted_queries[0]
        insights.append(f"'{winner[0]}' has the highest search interest with {winner[1]:.1f} average score")
        
        if len(sorted_queries) > 1:
            runner_up = sorted_queries[1]
            percentage_diff = ((winner[1] - runner_up[1]) / runner_up[1]) * 100
            insights.append(f"'{winner[0]}' outperforms '{runner_up[0]}' by {percentage_diff:.1f}%")
        
        # Identify low-performing queries
        low_performers = [q for q, score in sorted_queries if score < 20]
        if low_performers:
            insights.append(f"Low search interest detected for: {', '.join(low_performers)}")
        
        # Identify high-performing queries
        high_performers = [q for q, score in sorted_queries if score > 70]
        if high_performers:
            insights.append(f"High search interest detected for: {', '.join(high_performers)}")
        
        return insights

    async def get_seasonal_insights(
        self,
        queries: List[str],
        timeframe: str = 'today 5-y'
    ) -> List[SeasonalInsight]:
        """
        Analyze seasonal patterns for queries over a longer timeframe.
        
        Args:
            queries: List of queries to analyze
            timeframe: Extended timeframe for seasonal analysis
            
        Returns:
            List of SeasonalInsight objects
        """
        seasonal_insights = []
        
        for query in queries:
            try:
                # Get long-term trend data
                trend_data = await self._analyze_single_query(
                    query, timeframe, '', 0
                )
                
                if not trend_data or not trend_data.interest_over_time:
                    continue
                
                # Analyze seasonal patterns
                seasonal_analysis = self._analyze_seasonal_patterns(
                    trend_data.interest_over_time, query
                )
                
                if seasonal_analysis:
                    seasonal_insights.append(seasonal_analysis)
                
                # Rate limiting
                await asyncio.sleep(random.uniform(1, 2))
                
            except Exception as e:
                logger.error(f"Error getting seasonal insights for '{query}': {e}")
                continue
        
        return seasonal_insights

    def _analyze_seasonal_patterns(
        self,
        interest_data: List[Dict[str, Any]],
        query: str
    ) -> Optional[SeasonalInsight]:
        """Analyze detailed seasonal patterns."""
        
        if len(interest_data) < 24:  # Need at least 2 years of data
            return None
        
        try:
            # Convert to DataFrame for easier analysis
            df = pd.DataFrame(interest_data)
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.month
            df['month_name'] = df['date'].dt.month_name()
            
            # Calculate monthly averages
            monthly_avg = df.groupby(['month', 'month_name'])['interest'].mean().reset_index()
            monthly_avg = monthly_avg.sort_values('month')
            
            # Identify peak and low months
            peak_months = monthly_avg.nlargest(3, 'interest')['month_name'].tolist()
            low_months = monthly_avg.nsmallest(3, 'interest')['month_name'].tolist()
            
            # Calculate seasonality score
            max_interest = monthly_avg['interest'].max()
            min_interest = monthly_avg['interest'].min()
            avg_interest = monthly_avg['interest'].mean()
            
            if avg_interest > 0:
                seasonality_score = (max_interest - min_interest) / avg_interest
            else:
                seasonality_score = 0
            
            # Determine pattern type
            if seasonality_score > 1.0:
                pattern_type = 'highly_seasonal'
            elif seasonality_score > 0.5:
                pattern_type = 'moderately_seasonal'
            elif seasonality_score > 0.2:
                pattern_type = 'mildly_seasonal'
            else:
                pattern_type = 'non_seasonal'
            
            # Generate recommendations
            recommendations = self._generate_seasonal_recommendations(
                peak_months, low_months, pattern_type, seasonality_score
            )
            
            return SeasonalInsight(
                query=query,
                peak_months=peak_months,
                low_months=low_months,
                seasonality_score=round(seasonality_score, 2),
                pattern_type=pattern_type,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing seasonal patterns for '{query}': {e}")
            return None

    def _generate_seasonal_recommendations(
        self,
        peak_months: List[str],
        low_months: List[str],
        pattern_type: str,
        seasonality_score: float
    ) -> List[str]:
        """Generate seasonal optimization recommendations."""
        
        recommendations = []
        
        if pattern_type == 'highly_seasonal':
            recommendations.append(f"Strong seasonal pattern detected. Focus content creation and promotion during {', '.join(peak_months)}")
            recommendations.append(f"Prepare content in advance for peak months: {', '.join(peak_months)}")
            recommendations.append(f"Use low-interest months ({', '.join(low_months)}) for content planning and preparation")
            
        elif pattern_type == 'moderately_seasonal':
            recommendations.append(f"Moderate seasonality detected. Increase content focus during {', '.join(peak_months[:2])}")
            recommendations.append("Consider year-round content strategy with seasonal optimization")
            
        elif pattern_type == 'mildly_seasonal':
            recommendations.append("Slight seasonal variations detected. Maintain consistent content strategy")
            recommendations.append(f"Minor boost during {', '.join(peak_months[:1])} may be beneficial")
            
        else:
            recommendations.append("No significant seasonal pattern. Focus on consistent, high-quality content year-round")
            recommendations.append("Monitor for emerging seasonal trends as search behavior evolves")
        
        return recommendations

    async def get_trending_topics(
        self,
        geo: str = 'US',
        category: str = 'all'
    ) -> List[Dict[str, Any]]:
        """
        Get current trending topics and searches.
        
        Args:
            geo: Geographic region
            category: Trend category
            
        Returns:
            List of trending topics with metadata
        """
        if not self.pytrends:
            await self.initialize_client()
        
        try:
            # Get trending searches
            trending_df = self.pytrends.trending_searches(pn=geo)
            
            trending_topics = []
            for topic in trending_df[0].head(20):  # Top 20 trending
                trending_topics.append({
                    'topic': topic,
                    'region': geo,
                    'timestamp': datetime.now().isoformat()
                })
            
            return trending_topics
            
        except Exception as e:
            logger.error(f"Error getting trending topics: {e}")
            return []

# Global service instance
google_trends_service = GoogleTrendsService()