"""
Sitemap Analysis Service

AI-enhanced sitemap analyzer that provides insights into website structure,
content distribution, and publishing patterns for SEO optimization.
"""

import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from loguru import logger
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin
import pandas as pd

from ..llm_providers.main_text_generation import llm_text_gen
from ...middleware.logging_middleware import seo_logger


class SitemapService:
    """Service for analyzing website sitemaps with AI insights"""
    
    def __init__(self):
        """Initialize the sitemap service"""
        self.service_name = "sitemap_analyzer"
        logger.info(f"Initialized {self.service_name}")
    
    async def analyze_sitemap(
        self,
        sitemap_url: str,
        analyze_content_trends: bool = True,
        analyze_publishing_patterns: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze website sitemap for structure and patterns
        
        Args:
            sitemap_url: URL of the sitemap to analyze
            analyze_content_trends: Whether to analyze content trends
            analyze_publishing_patterns: Whether to analyze publishing patterns
            
        Returns:
            Dictionary containing sitemap analysis and AI insights
        """
        try:
            start_time = datetime.utcnow()
            
            if not sitemap_url:
                raise ValueError("Sitemap URL is required")
            
            logger.info(f"Analyzing sitemap: {sitemap_url}")
            
            # Fetch and parse sitemap data
            sitemap_data = await self._fetch_sitemap_data(sitemap_url)
            
            if not sitemap_data:
                raise Exception("Failed to fetch sitemap data")
            
            # Analyze sitemap structure
            structure_analysis = self._analyze_sitemap_structure(sitemap_data)
            
            # Analyze content trends if requested
            content_trends = {}
            if analyze_content_trends and sitemap_data.get("urls"):
                content_trends = self._analyze_content_trends(sitemap_data["urls"])
            
            # Analyze publishing patterns if requested  
            publishing_patterns = {}
            if analyze_publishing_patterns and sitemap_data.get("urls"):
                publishing_patterns = self._analyze_publishing_patterns(sitemap_data["urls"])
            
            # Generate AI insights
            ai_insights = await self._generate_ai_insights(
                structure_analysis, content_trends, publishing_patterns, sitemap_url
            )
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            result = {
                "sitemap_url": sitemap_url,
                "analysis_date": datetime.utcnow().isoformat(),
                "total_urls": len(sitemap_data.get("urls", [])),
                "structure_analysis": structure_analysis,
                "content_trends": content_trends,
                "publishing_patterns": publishing_patterns,
                "ai_insights": ai_insights,
                "seo_recommendations": self._generate_seo_recommendations(
                    structure_analysis, content_trends, publishing_patterns
                ),
                "execution_time": execution_time
            }
            
            # Log the operation
            await seo_logger.log_tool_usage(
                tool_name=self.service_name,
                input_data={
                    "sitemap_url": sitemap_url,
                    "analyze_content_trends": analyze_content_trends,
                    "analyze_publishing_patterns": analyze_publishing_patterns
                },
                output_data=result,
                success=True
            )
            
            logger.info(f"Sitemap analysis completed for {sitemap_url}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing sitemap {sitemap_url}: {e}")
            
            # Log the error
            await seo_logger.log_tool_usage(
                tool_name=self.service_name,
                input_data={
                    "sitemap_url": sitemap_url,
                    "analyze_content_trends": analyze_content_trends,
                    "analyze_publishing_patterns": analyze_publishing_patterns
                },
                output_data={"error": str(e)},
                success=False
            )
            
            raise
    
    async def _fetch_sitemap_data(self, sitemap_url: str) -> Dict[str, Any]:
        """Fetch and parse sitemap data"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(sitemap_url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch sitemap: HTTP {response.status}")
                    
                    content = await response.text()
                    
                    # Parse XML
                    root = ET.fromstring(content)
                    
                    # Handle different sitemap formats
                    urls = []
                    sitemaps = []
                    
                    # Check if it's a sitemap index
                    if root.tag.endswith('sitemapindex'):
                        # Extract nested sitemaps
                        for sitemap in root:
                            if sitemap.tag.endswith('sitemap'):
                                loc = sitemap.find('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                                if loc is not None:
                                    sitemaps.append(loc.text)
                        
                        # Fetch and parse nested sitemaps
                        for nested_url in sitemaps[:10]:  # Limit to 10 sitemaps
                            try:
                                nested_data = await self._fetch_sitemap_data(nested_url)
                                urls.extend(nested_data.get("urls", []))
                            except Exception as e:
                                logger.warning(f"Failed to fetch nested sitemap {nested_url}: {e}")
                    
                    else:
                        # Regular sitemap with URLs
                        for url_element in root:
                            if url_element.tag.endswith('url'):
                                url_data = {}
                                
                                for child in url_element:
                                    tag_name = child.tag.split('}')[-1]  # Remove namespace
                                    url_data[tag_name] = child.text
                                
                                if 'loc' in url_data:
                                    urls.append(url_data)
                    
                    return {
                        "urls": urls,
                        "sitemaps": sitemaps,
                        "total_urls": len(urls)
                    }
                    
        except ET.ParseError as e:
            raise Exception(f"Failed to parse sitemap XML: {e}")
        except Exception as e:
            logger.error(f"Error fetching sitemap data: {e}")
            raise
    
    def _analyze_sitemap_structure(self, sitemap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the structure of the sitemap"""
        
        urls = sitemap_data.get("urls", [])
        
        if not urls:
            return {"error": "No URLs found in sitemap"}
        
        # Analyze URL patterns
        url_patterns = {}
        file_types = {}
        path_levels = []
        
        for url_info in urls:
            url = url_info.get("loc", "")
            parsed_url = urlparse(url)
            
            # Analyze path patterns
            path_parts = parsed_url.path.strip('/').split('/')
            path_levels.append(len(path_parts))
            
            # Categorize by first path segment
            if len(path_parts) > 0 and path_parts[0]:
                category = path_parts[0]
                url_patterns[category] = url_patterns.get(category, 0) + 1
            
            # Analyze file types
            if '.' in parsed_url.path:
                extension = parsed_url.path.split('.')[-1].lower()
                file_types[extension] = file_types.get(extension, 0) + 1
        
        # Calculate statistics
        avg_path_depth = sum(path_levels) / len(path_levels) if path_levels else 0
        
        return {
            "total_urls": len(urls),
            "url_patterns": dict(sorted(url_patterns.items(), key=lambda x: x[1], reverse=True)[:10]),
            "file_types": dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True)),
            "average_path_depth": round(avg_path_depth, 2),
            "max_path_depth": max(path_levels) if path_levels else 0,
            "structure_quality": self._assess_structure_quality(url_patterns, avg_path_depth)
        }
    
    def _analyze_content_trends(self, urls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content publishing trends"""
        
        # Extract dates from lastmod
        dates = []
        for url_info in urls:
            lastmod = url_info.get("lastmod")
            if lastmod:
                try:
                    # Parse various date formats
                    date_str = lastmod.split('T')[0]  # Remove time component
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    dates.append(date_obj)
                except ValueError:
                    continue
        
        if not dates:
            return {"message": "No valid dates found for trend analysis"}
        
        # Analyze trends
        dates.sort()
        
        # Monthly distribution
        monthly_counts = {}
        yearly_counts = {}
        
        for date in dates:
            month_key = date.strftime("%Y-%m")
            year_key = date.strftime("%Y")
            
            monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1
            yearly_counts[year_key] = yearly_counts.get(year_key, 0) + 1
        
        # Calculate publishing velocity
        date_range = (dates[-1] - dates[0]).days
        publishing_velocity = len(dates) / max(date_range, 1) if date_range > 0 else 0
        
        return {
            "date_range": {
                "earliest": dates[0].isoformat(),
                "latest": dates[-1].isoformat(),
                "span_days": date_range
            },
            "monthly_distribution": dict(sorted(monthly_counts.items())[-12:]),  # Last 12 months
            "yearly_distribution": yearly_counts,
            "publishing_velocity": round(publishing_velocity, 3),
            "total_dated_urls": len(dates),
            "trends": self._identify_publishing_trends(monthly_counts)
        }
    
    def _analyze_publishing_patterns(self, urls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze publishing patterns and frequency"""
        
        # Extract and analyze priority and changefreq
        priority_distribution = {}
        changefreq_distribution = {}
        
        for url_info in urls:
            priority = url_info.get("priority")
            if priority:
                try:
                    priority_float = float(priority)
                    priority_range = f"{int(priority_float * 10)}/10"
                    priority_distribution[priority_range] = priority_distribution.get(priority_range, 0) + 1
                except ValueError:
                    pass
            
            changefreq = url_info.get("changefreq")
            if changefreq:
                changefreq_distribution[changefreq] = changefreq_distribution.get(changefreq, 0) + 1
        
        return {
            "priority_distribution": priority_distribution,
            "changefreq_distribution": changefreq_distribution,
            "optimization_opportunities": self._identify_optimization_opportunities(
                priority_distribution, changefreq_distribution, len(urls)
            )
        }
    
    async def _generate_ai_insights(
        self,
        structure_analysis: Dict[str, Any],
        content_trends: Dict[str, Any],
        publishing_patterns: Dict[str, Any],
        sitemap_url: str
    ) -> Dict[str, Any]:
        """Generate AI-powered insights for sitemap analysis"""
        
        try:
            # Build prompt with analysis data
            prompt = self._build_ai_analysis_prompt(
                structure_analysis, content_trends, publishing_patterns, sitemap_url
            )
            
            # Generate AI insights
            ai_response = llm_text_gen(
                prompt=prompt,
                system_prompt=self._get_system_prompt()
            )
            
            # Parse and structure insights
            insights = self._parse_ai_insights(ai_response)
            
            # Log AI analysis
            await seo_logger.log_ai_analysis(
                tool_name=self.service_name,
                prompt=prompt,
                response=ai_response,
                model_used="gemini-2.0-flash-001"
            )
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating AI insights: {e}")
            return {
                "summary": "AI analysis unavailable",
                "content_strategy": [],
                "seo_opportunities": [],
                "technical_recommendations": []
            }
    
    def _build_ai_analysis_prompt(
        self,
        structure_analysis: Dict[str, Any],
        content_trends: Dict[str, Any],
        publishing_patterns: Dict[str, Any],
        sitemap_url: str
    ) -> str:
        """Build AI prompt for sitemap analysis"""
        
        total_urls = structure_analysis.get("total_urls", 0)
        url_patterns = structure_analysis.get("url_patterns", {})
        avg_depth = structure_analysis.get("average_path_depth", 0)
        
        publishing_velocity = content_trends.get("publishing_velocity", 0)
        date_range = content_trends.get("date_range", {})
        
        prompt = f"""
Analyze this website sitemap data and provide strategic insights for content creators and digital marketers:

Sitemap URL: {sitemap_url}
Total URLs: {total_urls}
Average Path Depth: {avg_depth}
Publishing Velocity: {publishing_velocity} posts/day

URL Patterns (top categories):
{chr(10).join([f"- {category}: {count} URLs" for category, count in list(url_patterns.items())[:5]])}

Content Timeline:
- Date Range: {date_range.get('span_days', 0)} days
- Publishing Rate: {publishing_velocity:.2f} pages per day

Please provide:
1. Content Strategy Insights (opportunities for new content categories)
2. SEO Structure Assessment (how well the site is organized for search engines)
3. Publishing Pattern Analysis (content frequency and consistency)
4. Growth Recommendations (specific actions for content expansion)
5. Technical SEO Opportunities (sitemap optimization suggestions)

Focus on actionable insights for content creators and digital marketing professionals.
"""
        
        return prompt
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for AI analysis"""
        return """You are an SEO and content strategy expert specializing in website structure analysis.
        Your audience includes content creators, digital marketers, and solopreneurs who need to understand how their site structure impacts SEO and content performance.
        
        Provide practical, actionable insights that help users:
        - Optimize their content strategy
        - Improve site structure for SEO
        - Identify content gaps and opportunities
        - Plan future content development
        
        Always explain the business impact of your recommendations.
        """
    
    def _parse_ai_insights(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI response into structured insights"""
        
        insights = {
            "summary": "",
            "content_strategy": [],
            "seo_opportunities": [],
            "technical_recommendations": [],
            "growth_recommendations": []
        }
        
        try:
            # Split into sections and parse
            sections = ai_response.split('\n\n')
            
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                
                if 'content strategy' in section.lower():
                    insights["content_strategy"] = self._extract_list_items(section)
                elif 'seo' in section.lower() and 'opportunities' in section.lower():
                    insights["seo_opportunities"] = self._extract_list_items(section)
                elif 'technical' in section.lower():
                    insights["technical_recommendations"] = self._extract_list_items(section)
                elif 'growth' in section.lower() or 'recommendations' in section.lower():
                    insights["growth_recommendations"] = self._extract_list_items(section)
                elif 'analysis' in section.lower() or 'assessment' in section.lower():
                    insights["summary"] = self._extract_content(section)
            
            # Fallback
            if not any(insights.values()):
                insights["summary"] = ai_response[:300] + "..." if len(ai_response) > 300 else ai_response
                
        except Exception as e:
            logger.error(f"Error parsing AI insights: {e}")
            insights["summary"] = "AI analysis completed but parsing failed"
        
        return insights
    
    def _extract_content(self, section: str) -> str:
        """Extract content from a section"""
        lines = section.split('\n')
        content_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.endswith(':') and not line.startswith('#'):
                content_lines.append(line)
        
        return ' '.join(content_lines)
    
    def _extract_list_items(self, section: str) -> List[str]:
        """Extract list items from a section"""
        items = []
        lines = section.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('*') or 
                        (line[0].isdigit() and '.' in line[:3])):
                clean_line = line.lstrip('-*0123456789. ').strip()
                if clean_line:
                    items.append(clean_line)
        
        return items[:5]
    
    def _assess_structure_quality(self, url_patterns: Dict[str, int], avg_depth: float) -> str:
        """Assess the quality of site structure"""
        
        if avg_depth < 2:
            return "Shallow structure - may lack content organization"
        elif avg_depth > 5:
            return "Deep structure - may hurt crawlability"
        elif len(url_patterns) < 3:
            return "Limited content categories - opportunity for expansion"
        else:
            return "Well-structured site with good organization"
    
    def _identify_publishing_trends(self, monthly_counts: Dict[str, int]) -> List[str]:
        """Identify publishing trends from monthly data"""
        
        trends = []
        
        if not monthly_counts or len(monthly_counts) < 3:
            return ["Insufficient data for trend analysis"]
        
        # Get recent months
        recent_months = list(monthly_counts.values())[-6:]  # Last 6 months
        
        if len(recent_months) >= 3:
            # Check for growth trend
            if recent_months[-1] > recent_months[-3]:
                trends.append("Increasing publishing frequency")
            elif recent_months[-1] < recent_months[-3]:
                trends.append("Decreasing publishing frequency")
            
            # Check consistency
            avg_posts = sum(recent_months) / len(recent_months)
            if max(recent_months) - min(recent_months) <= avg_posts * 0.5:
                trends.append("Consistent publishing schedule")
            else:
                trends.append("Irregular publishing pattern")
        
        return trends or ["Stable publishing pattern"]
    
    def _identify_optimization_opportunities(
        self,
        priority_dist: Dict[str, int],
        changefreq_dist: Dict[str, int],
        total_urls: int
    ) -> List[str]:
        """Identify sitemap optimization opportunities"""
        
        opportunities = []
        
        # Check if priorities are being used
        if not priority_dist:
            opportunities.append("Add priority values to sitemap URLs")
        
        # Check if changefreq is being used
        if not changefreq_dist:
            opportunities.append("Add changefreq values to sitemap URLs")
        
        # Check for overuse of high priority
        high_priority_count = priority_dist.get("10/10", 0) + priority_dist.get("9/10", 0)
        if high_priority_count > total_urls * 0.3:
            opportunities.append("Reduce number of high-priority pages (max 30%)")
        
        return opportunities or ["Sitemap is well-optimized"]
    
    def _generate_seo_recommendations(
        self,
        structure_analysis: Dict[str, Any],
        content_trends: Dict[str, Any],
        publishing_patterns: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate specific SEO recommendations"""
        
        recommendations = []
        
        # Structure recommendations
        total_urls = structure_analysis.get("total_urls", 0)
        avg_depth = structure_analysis.get("average_path_depth", 0)
        
        if avg_depth > 4:
            recommendations.append({
                "category": "Site Structure",
                "priority": "High",
                "recommendation": "Reduce URL depth to improve crawlability",
                "impact": "Better search engine indexing"
            })
        
        if total_urls > 50000:
            recommendations.append({
                "category": "Sitemap Management",
                "priority": "Medium",
                "recommendation": "Split large sitemap into smaller files",
                "impact": "Improved crawl efficiency"
            })
        
        # Content recommendations
        publishing_velocity = content_trends.get("publishing_velocity", 0)
        
        if publishing_velocity < 0.1:  # Less than 1 post per 10 days
            recommendations.append({
                "category": "Content Strategy", 
                "priority": "High",
                "recommendation": "Increase content publishing frequency",
                "impact": "Better search visibility and freshness signals"
            })
        
        return recommendations
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the sitemap service"""
        try:
            # Test with a simple sitemap
            test_url = "https://www.google.com/sitemap.xml"
            result = await self.analyze_sitemap(test_url, False, False)
            
            return {
                "status": "operational",
                "service": self.service_name,
                "test_passed": bool(result.get("total_urls", 0) > 0),
                "last_check": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "service": self.service_name,
                "error": str(e),
                "last_check": datetime.utcnow().isoformat()
            }