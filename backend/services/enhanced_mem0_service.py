"""
Enhanced Mem0 Service with Intelligent Caching and Audit Trail
Handles ALwrity memory with caching, change tracking, and comprehensive strategy storage
"""

import os
import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from loguru import logger
from mem0 import Memory
from sqlalchemy.orm import Session
from services.database import get_db_session

@dataclass
class MemoryAuditEntry:
    """Audit entry for memory changes"""
    memory_id: str
    strategy_id: int
    user_id: int
    action: str  # 'created', 'updated', 'deleted', 'activated'
    timestamp: datetime
    changes: Dict[str, Any]
    metadata: Dict[str, Any]
    content_hash: str

@dataclass
class CachedMemory:
    """Cached memory with metadata"""
    memory_id: str
    content: str
    metadata: Dict[str, Any]
    cached_at: datetime
    expires_at: datetime
    content_hash: str

class EnhancedMem0Service:
    """Enhanced service for integrating with mem0 AI memory platform with caching and audit trail"""
    
    # Cache configuration
    CACHE_TTL_MINUTES = 30
    MAX_CACHE_SIZE = 1000
    
    # Intelligent categories for different user types
    CONTENT_CREATOR_CATEGORIES = [
        "creative_strategy", "content_pillars", "audience_engagement", 
        "brand_voice", "content_formats", "seasonal_content"
    ]
    
    DIGITAL_MARKETER_CATEGORIES = [
        "marketing_strategy", "conversion_optimization", "competitive_analysis",
        "performance_metrics", "roi_tracking", "campaign_strategy"
    ]
    
    INDUSTRY_CATEGORIES = [
        "technology", "healthcare", "finance", "retail", "education", 
        "manufacturing", "services", "nonprofit", "entertainment"
    ]
    
    def __init__(self, db_session: Optional[Session] = None):
        """Initialize enhanced mem0 service with caching and audit trail"""
        self.api_key = os.getenv("MEM0_API_KEY")
        self.db_session = db_session or get_db_session()
        self._memory_cache: Dict[str, CachedMemory] = {}
        self._stats_cache: Dict[int, Dict[str, Any]] = {}
        self._audit_trail: List[MemoryAuditEntry] = []
        
        if not self.api_key:
            logger.warning("MEM0_API_KEY not found in environment variables. Mem0 functionality will be disabled.")
            self.memory = None
        else:
            try:
                # Initialize mem0 client with advanced configuration
                config = {
                    "vector_store": {
                        "provider": "qdrant",
                        "config": {
                            "collection_name": "alwrity_strategies",
                            "embedding_model_dims": 1536,
                        }
                    }
                }
                self.memory = Memory.from_config(config)
                logger.info("Enhanced Mem0 service initialized with intelligent caching and audit trail")
            except Exception as e:
                logger.error(f"Failed to initialize mem0 service: {e}")
                self.memory = None
    
    def is_available(self) -> bool:
        """Check if mem0 service is available"""
        return self.memory is not None
    
    def _generate_content_hash(self, content: str) -> str:
        """Generate hash for content to detect changes"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _is_cache_valid(self, cached_memory: CachedMemory) -> bool:
        """Check if cached memory is still valid"""
        return datetime.utcnow() < cached_memory.expires_at
    
    def _cleanup_cache(self):
        """Remove expired entries from cache"""
        current_time = datetime.utcnow()
        expired_keys = [
            key for key, cached_memory in self._memory_cache.items()
            if current_time >= cached_memory.expires_at
        ]
        for key in expired_keys:
            del self._memory_cache[key]
        
        # Limit cache size
        if len(self._memory_cache) > self.MAX_CACHE_SIZE:
            # Remove oldest entries
            sorted_items = sorted(
                self._memory_cache.items(),
                key=lambda x: x[1].cached_at
            )
            items_to_remove = len(self._memory_cache) - self.MAX_CACHE_SIZE
            for key, _ in sorted_items[:items_to_remove]:
                del self._memory_cache[key]
    
    def _add_audit_entry(self, memory_id: str, strategy_id: int, user_id: int, 
                        action: str, changes: Dict[str, Any], metadata: Dict[str, Any],
                        content_hash: str):
        """Add entry to audit trail"""
        audit_entry = MemoryAuditEntry(
            memory_id=memory_id,
            strategy_id=strategy_id,
            user_id=user_id,
            action=action,
            timestamp=datetime.utcnow(),
            changes=changes,
            metadata=metadata,
            content_hash=content_hash
        )
        self._audit_trail.append(audit_entry)
        
        # Keep only last 1000 audit entries in memory
        if len(self._audit_trail) > 1000:
            self._audit_trail = self._audit_trail[-1000:]
        
        logger.info(f"Audit trail: {action} memory {memory_id} for strategy {strategy_id} by user {user_id}")
    
    def _extract_all_strategy_inputs(self, strategy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all 30+ strategic inputs from strategy data"""
        all_inputs = {}
        
        # Business Context (8 inputs)
        business_context = {
            "business_objectives": strategy_data.get('business_objectives', []),
            "target_metrics": strategy_data.get('target_metrics', {}),
            "content_budget": strategy_data.get('content_budget'),
            "team_size": strategy_data.get('team_size'),
            "implementation_timeline": strategy_data.get('implementation_timeline'),
            "market_share": strategy_data.get('market_share'),
            "competitive_position": strategy_data.get('competitive_position'),
            "performance_metrics": strategy_data.get('performance_metrics', {})
        }
        all_inputs["business_context"] = business_context
        
        # Audience Intelligence (6 inputs)
        audience_intelligence = {
            "content_preferences": strategy_data.get('content_preferences', {}),
            "consumption_patterns": strategy_data.get('consumption_patterns', {}),
            "audience_pain_points": strategy_data.get('audience_pain_points', []),
            "buying_journey": strategy_data.get('buying_journey', {}),
            "seasonal_trends": strategy_data.get('seasonal_trends', {}),
            "engagement_metrics": strategy_data.get('engagement_metrics', {})
        }
        all_inputs["audience_intelligence"] = audience_intelligence
        
        # Competitive Intelligence (5 inputs)
        competitive_intelligence = {
            "top_competitors": strategy_data.get('top_competitors', []),
            "competitor_content_strategies": strategy_data.get('competitor_content_strategies', {}),
            "market_gaps": strategy_data.get('market_gaps', []),
            "industry_trends": strategy_data.get('industry_trends', []),
            "emerging_trends": strategy_data.get('emerging_trends', [])
        }
        all_inputs["competitive_intelligence"] = competitive_intelligence
        
        # Content Strategy (7 inputs)
        content_strategy = {
            "preferred_formats": strategy_data.get('preferred_formats', []),
            "content_mix": strategy_data.get('content_mix', {}),
            "content_frequency": strategy_data.get('content_frequency'),
            "optimal_timing": strategy_data.get('optimal_timing', {}),
            "quality_metrics": strategy_data.get('quality_metrics', {}),
            "editorial_guidelines": strategy_data.get('editorial_guidelines', {}),
            "brand_voice": strategy_data.get('brand_voice', {})
        }
        all_inputs["content_strategy"] = content_strategy
        
        # Performance & Analytics (4 inputs)
        performance_analytics = {
            "traffic_sources": strategy_data.get('traffic_sources', {}),
            "conversion_rates": strategy_data.get('conversion_rates', {}),
            "content_roi_targets": strategy_data.get('content_roi_targets', {}),
            "ab_testing_capabilities": strategy_data.get('ab_testing_capabilities', False)
        }
        all_inputs["performance_analytics"] = performance_analytics
        
        # Legacy and Enhanced fields
        legacy_enhanced = {
            "target_audience": strategy_data.get('target_audience', {}),
            "content_pillars": strategy_data.get('content_pillars', []),
            "ai_recommendations": strategy_data.get('ai_recommendations', {}),
            "comprehensive_ai_analysis": strategy_data.get('comprehensive_ai_analysis', {}),
            "onboarding_data_used": strategy_data.get('onboarding_data_used', {}),
            "strategic_scores": strategy_data.get('strategic_scores', {}),
            "market_positioning": strategy_data.get('market_positioning', {}),
            "competitive_advantages": strategy_data.get('competitive_advantages', []),
            "strategic_risks": strategy_data.get('strategic_risks', []),
            "opportunity_analysis": strategy_data.get('opportunity_analysis', {})
        }
        all_inputs["legacy_enhanced"] = legacy_enhanced
        
        # Basic information
        all_inputs["basic_info"] = {
            "id": strategy_data.get('id'),
            "name": strategy_data.get('name'),
            "industry": strategy_data.get('industry'),
            "user_id": strategy_data.get('user_id'),
            "created_at": strategy_data.get('created_at'),
            "updated_at": strategy_data.get('updated_at'),
            "completion_percentage": strategy_data.get('completion_percentage', 0.0)
        }
        
        return all_inputs
    
    def _prepare_comprehensive_memory_content(self, strategy_data: Dict[str, Any], strategy_id: int) -> str:
        """Prepare comprehensive memory content with all 30+ strategic inputs"""
        try:
            # Extract all strategic inputs
            all_inputs = self._extract_all_strategy_inputs(strategy_data)
            basic_info = all_inputs["basic_info"]
            business_context = all_inputs["business_context"]
            audience_intelligence = all_inputs["audience_intelligence"]
            competitive_intelligence = all_inputs["competitive_intelligence"]
            content_strategy = all_inputs["content_strategy"]
            performance_analytics = all_inputs["performance_analytics"]
            legacy_enhanced = all_inputs["legacy_enhanced"]
            
            # Build comprehensive memory content
            memory_parts = [
                f"ACTIVATED CONTENT STRATEGY: {basic_info.get('name', f'Strategy {strategy_id}')}",
                f"Strategy ID: {strategy_id}",
                f"Industry: {basic_info.get('industry', 'General')}",
                f"Completion: {basic_info.get('completion_percentage', 0):.1f}%",
                f"Activated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "=" * 60,
                "BUSINESS CONTEXT (8 Strategic Inputs)",
                "=" * 60
            ]
            
            # Business Objectives
            if business_context.get('business_objectives'):
                memory_parts.append("\n📊 BUSINESS OBJECTIVES:")
                for i, obj in enumerate(business_context['business_objectives'][:5], 1):
                    if isinstance(obj, dict):
                        obj_text = obj.get('description', obj.get('objective', str(obj)))
                    else:
                        obj_text = str(obj)
                    memory_parts.append(f"  {i}. {obj_text}")
            
            # Target Metrics & KPIs
            if business_context.get('target_metrics'):
                memory_parts.append("\n📈 TARGET METRICS & KPIs:")
                for metric, value in list(business_context['target_metrics'].items())[:5]:
                    memory_parts.append(f"  • {metric}: {value}")
            
            # Resource Information
            memory_parts.append(f"\n💰 BUDGET: {business_context.get('content_budget', 'Not specified')}")
            memory_parts.append(f"👥 TEAM SIZE: {business_context.get('team_size', 'Not specified')}")
            memory_parts.append(f"⏱️ TIMELINE: {business_context.get('implementation_timeline', 'Not specified')}")
            memory_parts.append(f"📊 MARKET SHARE: {business_context.get('market_share', 'Not specified')}")
            memory_parts.append(f"🏆 COMPETITIVE POSITION: {business_context.get('competitive_position', 'Not specified')}")
            
            # Audience Intelligence Section
            memory_parts.extend([
                "",
                "=" * 60,
                "AUDIENCE INTELLIGENCE (6 Strategic Inputs)",
                "=" * 60
            ])
            
            # Target Audience (Enhanced)
            target_audience = legacy_enhanced.get('target_audience', {})
            if target_audience:
                memory_parts.append("\n👥 TARGET AUDIENCE:")
                if isinstance(target_audience, dict):
                    if target_audience.get('demographics'):
                        memory_parts.append(f"  Demographics: {target_audience['demographics']}")
                    if target_audience.get('age_range'):
                        memory_parts.append(f"  Age Range: {target_audience['age_range']}")
                    if target_audience.get('interests'):
                        interests = target_audience['interests']
                        if isinstance(interests, list):
                            memory_parts.append(f"  Interests: {', '.join(interests[:5])}")
                        else:
                            memory_parts.append(f"  Interests: {interests}")
            
            # Content Preferences
            if audience_intelligence.get('content_preferences'):
                memory_parts.append("\n📱 CONTENT PREFERENCES:")
                prefs = audience_intelligence['content_preferences']
                if isinstance(prefs, dict):
                    for pref_type, details in list(prefs.items())[:3]:
                        memory_parts.append(f"  • {pref_type}: {details}")
            
            # Consumption Patterns
            if audience_intelligence.get('consumption_patterns'):
                memory_parts.append("\n⏰ CONSUMPTION PATTERNS:")
                patterns = audience_intelligence['consumption_patterns']
                if isinstance(patterns, dict):
                    for pattern, details in list(patterns.items())[:3]:
                        memory_parts.append(f"  • {pattern}: {details}")
            
            # Pain Points
            if audience_intelligence.get('audience_pain_points'):
                memory_parts.append("\n😰 AUDIENCE PAIN POINTS:")
                for i, pain_point in enumerate(audience_intelligence['audience_pain_points'][:3], 1):
                    memory_parts.append(f"  {i}. {pain_point}")
            
            # Competitive Intelligence Section
            memory_parts.extend([
                "",
                "=" * 60,
                "COMPETITIVE INTELLIGENCE (5 Strategic Inputs)",
                "=" * 60
            ])
            
            # Top Competitors
            if competitive_intelligence.get('top_competitors'):
                memory_parts.append("\n🏢 KEY COMPETITORS:")
                for i, competitor in enumerate(competitive_intelligence['top_competitors'][:5], 1):
                    if isinstance(competitor, dict):
                        comp_name = competitor.get('name', competitor.get('domain', f'Competitor {i}'))
                        comp_details = competitor.get('description', competitor.get('strategy', ''))
                        memory_parts.append(f"  {i}. {comp_name}")
                        if comp_details:
                            memory_parts.append(f"     Strategy: {comp_details}")
                    else:
                        memory_parts.append(f"  {i}. {str(competitor)}")
            
            # Market Gaps
            if competitive_intelligence.get('market_gaps'):
                memory_parts.append("\n🎯 MARKET GAPS & OPPORTUNITIES:")
                for i, gap in enumerate(competitive_intelligence['market_gaps'][:3], 1):
                    memory_parts.append(f"  {i}. {gap}")
            
            # Industry Trends
            if competitive_intelligence.get('industry_trends'):
                memory_parts.append("\n📊 INDUSTRY TRENDS:")
                for i, trend in enumerate(competitive_intelligence['industry_trends'][:3], 1):
                    memory_parts.append(f"  {i}. {trend}")
            
            # Content Strategy Section
            memory_parts.extend([
                "",
                "=" * 60,
                "CONTENT STRATEGY (7 Strategic Inputs)",
                "=" * 60
            ])
            
            # Content Pillars
            content_pillars = legacy_enhanced.get('content_pillars', [])
            if content_pillars:
                memory_parts.append("\n🏛️ CONTENT PILLARS:")
                for i, pillar in enumerate(content_pillars[:5], 1):
                    if isinstance(pillar, dict):
                        pillar_text = pillar.get('title', pillar.get('name', str(pillar)))
                        pillar_desc = pillar.get('description', '')
                        memory_parts.append(f"  {i}. {pillar_text}")
                        if pillar_desc:
                            memory_parts.append(f"     {pillar_desc}")
                    else:
                        memory_parts.append(f"  {i}. {str(pillar)}")
            
            # Preferred Formats
            if content_strategy.get('preferred_formats'):
                formats = content_strategy['preferred_formats']
                memory_parts.append(f"\n📝 PREFERRED FORMATS: {', '.join(formats[:5])}")
            
            # Content Mix
            if content_strategy.get('content_mix'):
                memory_parts.append("\n📊 CONTENT MIX:")
                for content_type, percentage in list(content_strategy['content_mix'].items())[:5]:
                    memory_parts.append(f"  • {content_type}: {percentage}")
            
            # Publishing Strategy
            memory_parts.append(f"\n📅 PUBLISHING FREQUENCY: {content_strategy.get('content_frequency', 'Not specified')}")
            
            # Brand Voice
            if content_strategy.get('brand_voice'):
                memory_parts.append("\n🎭 BRAND VOICE:")
                brand_voice = content_strategy['brand_voice']
                if isinstance(brand_voice, dict):
                    for aspect, details in list(brand_voice.items())[:3]:
                        memory_parts.append(f"  • {aspect}: {details}")
                else:
                    memory_parts.append(f"  {brand_voice}")
            
            # Performance & Analytics Section
            memory_parts.extend([
                "",
                "=" * 60,
                "PERFORMANCE & ANALYTICS (4 Strategic Inputs)",
                "=" * 60
            ])
            
            # Performance Metrics
            if business_context.get('performance_metrics'):
                memory_parts.append("\n📊 CURRENT PERFORMANCE METRICS:")
                for metric, value in list(business_context['performance_metrics'].items())[:5]:
                    memory_parts.append(f"  • {metric}: {value}")
            
            # Traffic Sources
            if performance_analytics.get('traffic_sources'):
                memory_parts.append("\n🔗 PRIMARY TRAFFIC SOURCES:")
                for source, details in list(performance_analytics['traffic_sources'].items())[:5]:
                    memory_parts.append(f"  • {source}: {details}")
            
            # ROI Targets
            if performance_analytics.get('content_roi_targets'):
                memory_parts.append("\n💰 ROI TARGETS:")
                for target, value in list(performance_analytics['content_roi_targets'].items())[:3]:
                    memory_parts.append(f"  • {target}: {value}")
            
            # A/B Testing
            memory_parts.append(f"\n🧪 A/B TESTING: {'Enabled' if performance_analytics.get('ab_testing_capabilities') else 'Not Available'}")
            
            # Enhanced AI Analysis
            if legacy_enhanced.get('comprehensive_ai_analysis'):
                memory_parts.extend([
                    "",
                    "=" * 60,
                    "AI ANALYSIS & RECOMMENDATIONS",
                    "=" * 60
                ])
                
                ai_analysis = legacy_enhanced['comprehensive_ai_analysis']
                if isinstance(ai_analysis, dict):
                    for analysis_type, details in list(ai_analysis.items())[:3]:
                        memory_parts.append(f"\n🤖 {analysis_type.upper()}:")
                        if isinstance(details, (list, dict)):
                            memory_parts.append(f"  {str(details)[:200]}...")
                        else:
                            memory_parts.append(f"  {details}")
            
            # Strategic Scores
            if legacy_enhanced.get('strategic_scores'):
                memory_parts.append("\n📊 STRATEGIC SCORES:")
                for score_type, value in list(legacy_enhanced['strategic_scores'].items())[:5]:
                    memory_parts.append(f"  • {score_type}: {value}")
            
            # Footer
            memory_parts.extend([
                "",
                "=" * 60,
                f"MEMORY GENERATED: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
                f"TOTAL STRATEGIC INPUTS CAPTURED: 30+",
                f"STRATEGY STATUS: ACTIVATED",
                "=" * 60
            ])
            
            return "\n".join(memory_parts)
            
        except Exception as e:
            logger.error(f"Error preparing comprehensive memory content: {e}")
            # Fallback to basic representation
            return f"ACTIVATED Content Strategy #{strategy_id}: {json.dumps(strategy_data, indent=2)[:2000]}..."
    
    def _determine_user_type(self, strategy_data: Dict[str, Any]) -> str:
        """Determine user type based on strategy data for intelligent categorization"""
        if not strategy_data or not isinstance(strategy_data, dict):
            return "content_creator"  # Safe default
        
        try:
            # Check for digital marketer indicators
            digital_marketer_indicators = [
                'conversion_rates', 'traffic_sources', 'content_roi_targets', 
                'performance_metrics', 'ab_testing_capabilities', 'target_metrics'
            ]
            if any(key in strategy_data and strategy_data[key] for key in digital_marketer_indicators):
                return "digital_marketer"
            
            # Check for content creator indicators
            content_creator_indicators = [
                'brand_voice', 'editorial_guidelines', 'content_mix', 
                'preferred_formats', 'content_pillars', 'content_preferences'
            ]
            if any(key in strategy_data and strategy_data[key] for key in content_creator_indicators):
                return "content_creator"
            
            # Default to content creator
            return "content_creator"
        except Exception as e:
            logger.warning(f"Error determining user type: {e}, defaulting to content_creator")
            return "content_creator"
    
    def _categorize_strategy(self, strategy_data: Dict[str, Any], user_type: str) -> List[str]:
        """Intelligently categorize strategy based on content and user type"""
        if not strategy_data or not isinstance(strategy_data, dict):
            return ["general"]  # Safe default
        
        try:
            categories = []
            
            # Add industry category
            industry = str(strategy_data.get('industry', '')).lower().strip()
            if industry in self.INDUSTRY_CATEGORIES:
                categories.append(industry)
            elif industry:
                categories.append("other_industry")
            
            # Add user-type specific categories
            if user_type == "digital_marketer":
                if strategy_data.get('top_competitors') or strategy_data.get('competitor_content_strategies'):
                    categories.append("competitive_analysis")
                if strategy_data.get('conversion_rates') or strategy_data.get('content_roi_targets'):
                    categories.append("conversion_optimization")
                if strategy_data.get('performance_metrics') or strategy_data.get('traffic_sources'):
                    categories.append("performance_metrics")
                categories.append("marketing_strategy")
            else:  # content_creator
                if strategy_data.get('content_pillars'):
                    categories.append("content_pillars")
                if strategy_data.get('brand_voice') or strategy_data.get('editorial_guidelines'):
                    categories.append("brand_voice")
                if strategy_data.get('preferred_formats') or strategy_data.get('content_mix'):
                    categories.append("content_formats")
                categories.append("creative_strategy")
            
            # Add seasonal category if seasonal trends exist
            if strategy_data.get('seasonal_trends'):
                categories.append("seasonal_content")
            
            # Ensure we always have at least one category
            if not categories:
                categories = ["general"]
            
            return categories
        except Exception as e:
            logger.warning(f"Error categorizing strategy: {e}, returning default category")
            return ["general"]
    
    async def store_activated_content_strategy(self, 
                                             strategy_data: Dict[str, Any], 
                                             user_id: int, 
                                             strategy_id: int,
                                             domain_name: str = "ALwrity") -> bool:
        """
        Store ACTIVATED content strategy with all 30+ inputs as memory
        Only called when strategy is marked as 'Active'
        
        Args:
            strategy_data: Complete strategy data with all 30+ inputs
            user_id: User ID for memory association
            strategy_id: Strategy ID for reference
            domain_name: Domain name for toast notification
            
        Returns:
            bool: Success status
        """
        if not self.is_available():
            logger.warning("Mem0 service not available, skipping memory storage")
            return False
        
        try:
            # Check if this strategy is already in cache
            cache_key = f"strategy_{strategy_id}"
            content = self._prepare_comprehensive_memory_content(strategy_data, strategy_id)
            content_hash = self._generate_content_hash(content)
            
            # Check if we have a cached version with same content
            if cache_key in self._memory_cache:
                cached_memory = self._memory_cache[cache_key]
                if self._is_cache_valid(cached_memory) and cached_memory.content_hash == content_hash:
                    logger.info(f"Strategy {strategy_id} content unchanged, using cached version")
                    return True
            
            # Determine user type and categories
            user_type = self._determine_user_type(strategy_data)
            categories = self._categorize_strategy(strategy_data, user_type)
            
            # Prepare comprehensive metadata
            metadata = {
                "type": "activated_content_strategy",
                "strategy_id": strategy_id,
                "activation_date": datetime.utcnow().isoformat(),
                "source": "alwrity_strategy_activation",
                "user_type": user_type,
                "categories": categories,
                "industry": strategy_data.get('industry', 'general'),
                "strategy_name": strategy_data.get('name', f'Strategy {strategy_id}'),
                "completion_percentage": strategy_data.get('completion_percentage', 0.0),
                "domain_name": domain_name,
                
                # Enhanced metadata for tracking
                "total_inputs_captured": 30,
                "has_competitors": bool(strategy_data.get('top_competitors')),
                "has_metrics": bool(strategy_data.get('performance_metrics')),
                "has_ai_analysis": bool(strategy_data.get('comprehensive_ai_analysis')),
                "content_pillar_count": len(strategy_data.get('content_pillars', [])),
                "target_audience_defined": bool(strategy_data.get('target_audience')),
                "budget_defined": bool(strategy_data.get('content_budget')),
                "timeline_defined": bool(strategy_data.get('implementation_timeline')),
                "brand_voice_defined": bool(strategy_data.get('brand_voice')),
                
                # Audit trail metadata
                "content_hash": content_hash,
                "stored_by": f"user_{user_id}",
                "storage_method": "automatic_activation",
                "inputs_checksum": hashlib.sha256(json.dumps(strategy_data, sort_keys=True).encode()).hexdigest()[:16]
            }
            
            # Store in mem0 with comprehensive metadata
            result = self.memory.add(
                messages=[{"role": "system", "content": content}],
                user_id=str(user_id),
                metadata=metadata,
                filters={
                    "categories": {"in": categories},
                    "user_type": user_type,
                    "industry": strategy_data.get('industry', 'general'),
                    "type": "activated_content_strategy"
                }
            )
            
            if result:
                # Update cache
                expires_at = datetime.utcnow() + timedelta(minutes=self.CACHE_TTL_MINUTES)
                cached_memory = CachedMemory(
                    memory_id=str(result.get('id', 'unknown')),
                    content=content,
                    metadata=metadata,
                    cached_at=datetime.utcnow(),
                    expires_at=expires_at,
                    content_hash=content_hash
                )
                self._memory_cache[cache_key] = cached_memory
                
                # Add audit trail entry
                self._add_audit_entry(
                    memory_id=cached_memory.memory_id,
                    strategy_id=strategy_id,
                    user_id=user_id,
                    action="activated",
                    changes={"strategy_activated": True, "inputs_captured": 30},
                    metadata=metadata,
                    content_hash=content_hash
                )
                
                # Clean up cache periodically
                self._cleanup_cache()
                
                logger.info(f"Successfully stored ACTIVATED strategy {strategy_id} in mem0 for user {user_id} with {len(categories)} categories")
                return True
            else:
                logger.error(f"Failed to store ACTIVATED strategy {strategy_id} in mem0")
                return False
                
        except Exception as e:
            logger.error(f"Error storing ACTIVATED strategy in mem0: {e}")
            return False
    
    async def get_memory_statistics(self, user_id: int, use_cache: bool = True) -> Dict[str, Any]:
        """Get comprehensive memory statistics with intelligent caching"""
        
        # Check cache first
        if use_cache and user_id in self._stats_cache:
            cached_stats = self._stats_cache[user_id]
            cache_time = datetime.fromisoformat(cached_stats.get('cached_at', '2020-01-01'))
            if datetime.utcnow() - cache_time < timedelta(minutes=5):  # 5-minute cache for stats
                return cached_stats
        
        if not self.is_available():
            return {
                "total_memories": 0,
                "activated_strategies": 0,
                "categories": {},
                "user_types": {},
                "industries": {},
                "recent_memories": 0,
                "cache_hits": len(self._memory_cache),
                "audit_entries": len(self._audit_trail),
                "available": False,
                "cached_at": datetime.utcnow().isoformat()
            }
        
        try:
            # Get all user memories (this should be cached by mem0 itself)
            all_memories = await self.retrieve_strategy_memories(user_id=user_id, limit=1000)
            
            # Filter for activated strategies
            activated_memories = [
                m for m in all_memories 
                if m.get('metadata', {}).get('type') == 'activated_content_strategy'
            ]
            
            stats = {
                "total_memories": len(all_memories),
                "activated_strategies": len(activated_memories),
                "categories": {},
                "user_types": {},
                "industries": {},
                "recent_memories": 0,
                "cache_hits": len(self._memory_cache),
                "audit_entries": len(self._audit_trail),
                "available": True,
                "cached_at": datetime.utcnow().isoformat()
            }
            
            # Analyze memories
            for memory in all_memories:
                metadata = memory.get('metadata', {})
                
                # Count categories
                categories = metadata.get('categories', [])
                for category in categories:
                    stats["categories"][category] = stats["categories"].get(category, 0) + 1
                
                # Count user types
                user_type = metadata.get('user_type', 'unknown')
                stats["user_types"][user_type] = stats["user_types"].get(user_type, 0) + 1
                
                # Count industries
                industry = metadata.get('industry', 'unknown')
                stats["industries"][industry] = stats["industries"].get(industry, 0) + 1
                
                # Count recent memories (last 7 days)
                activation_date = metadata.get('activation_date')
                if activation_date:
                    try:
                        memory_date = datetime.fromisoformat(activation_date.replace('Z', '+00:00'))
                        if memory_date > datetime.utcnow() - timedelta(days=7):
                            stats["recent_memories"] += 1
                    except:
                        pass
            
            # Add formatted categories for UI
            stats["formatted_categories"] = [
                {"name": category, "count": count, "percentage": round((count / max(stats["total_memories"], 1)) * 100, 1)}
                for category, count in stats["categories"].items()
            ]
            
            stats["status_message"] = f"ALwrity has stored {stats['activated_strategies']} activated strategic memories for you"
            
            # Cache the results
            self._stats_cache[user_id] = stats
            
            logger.info(f"Retrieved memory statistics for user {user_id}: {stats['total_memories']} total, {stats['activated_strategies']} activated")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting memory statistics: {e}")
            return {
                "total_memories": 0,
                "activated_strategies": 0,
                "categories": {},
                "user_types": {},
                "industries": {},
                "recent_memories": 0,
                "cache_hits": 0,
                "audit_entries": 0,
                "available": False,
                "error": str(e),
                "cached_at": datetime.utcnow().isoformat()
            }
    
    async def retrieve_strategy_memories(self, 
                                       user_id: int, 
                                       query: Optional[str] = None,
                                       user_type: Optional[str] = None,
                                       industry: Optional[str] = None,
                                       categories: Optional[List[str]] = None,
                                       limit: int = 10,
                                       use_cache: bool = True) -> List[Dict[str, Any]]:
        """Retrieve content strategy memories with intelligent caching"""
        
        if not self.is_available():
            logger.warning("Mem0 service not available")
            return []
        
        try:
            # Build cache key for this query
            cache_key = f"query_{hashlib.sha256(f'{user_id}_{query}_{user_type}_{industry}_{categories}_{limit}'.encode()).hexdigest()[:16]}"
            
            # Check cache first
            if use_cache and cache_key in self._memory_cache:
                cached_memory = self._memory_cache[cache_key]
                if self._is_cache_valid(cached_memory):
                    logger.debug(f"Cache hit for memory query: {cache_key}")
                    return json.loads(cached_memory.content)
            
            # Build advanced filters
            filters = {
                "AND": [
                    {"metadata.type": {"in": ["content_strategy", "activated_content_strategy"]}}
                ]
            }
            
            if user_type:
                filters["AND"].append({"metadata.user_type": user_type})
            
            if industry:
                filters["AND"].append({"metadata.industry": industry})
            
            if categories:
                filters["AND"].append({"metadata.categories": {"in": categories}})
            
            if query:
                # Advanced search with filters
                results = self.memory.search(
                    query=query,
                    user_id=str(user_id),
                    filters=filters,
                    limit=limit
                )
            else:
                # Get all strategy memories with filters
                results = self.memory.get_all(
                    user_id=str(user_id),
                    filters=filters,
                    limit=limit
                )
            
            # Ensure we only return strategy memories
            strategy_memories = []
            for memory in results:
                metadata = memory.get('metadata', {})
                memory_type = metadata.get('type', '')
                if memory_type in ['content_strategy', 'activated_content_strategy']:
                    strategy_memories.append(memory)
            
            # Cache the results if it's a cacheable query
            if not query or len(query) > 3:  # Don't cache very short queries
                expires_at = datetime.utcnow() + timedelta(minutes=self.CACHE_TTL_MINUTES)
                cached_memory = CachedMemory(
                    memory_id=cache_key,
                    content=json.dumps(strategy_memories),
                    metadata={"query_type": "retrieve_memories"},
                    cached_at=datetime.utcnow(),
                    expires_at=expires_at,
                    content_hash=self._generate_content_hash(json.dumps(strategy_memories))
                )
                self._memory_cache[cache_key] = cached_memory
            
            logger.info(f"Retrieved {len(strategy_memories)} strategy memories for user {user_id}")
            return strategy_memories
            
        except Exception as e:
            logger.error(f"Error retrieving strategy memories: {e}")
            return []
    
    def get_audit_trail(self, user_id: Optional[int] = None, strategy_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get audit trail for memory changes"""
        filtered_entries = []
        
        for entry in self._audit_trail:
            if user_id and entry.user_id != user_id:
                continue
            if strategy_id and entry.strategy_id != strategy_id:
                continue
            
            filtered_entries.append({
                "memory_id": entry.memory_id,
                "strategy_id": entry.strategy_id,
                "user_id": entry.user_id,
                "action": entry.action,
                "timestamp": entry.timestamp.isoformat(),
                "changes": entry.changes,
                "metadata": entry.metadata,
                "content_hash": entry.content_hash
            })
        
        # Sort by timestamp, most recent first
        filtered_entries.sort(key=lambda x: x['timestamp'], reverse=True)
        return filtered_entries
    
    def clear_cache(self, user_id: Optional[int] = None):
        """Clear memory cache for a specific user or all users"""
        if user_id:
            # Clear user-specific cache entries
            keys_to_remove = [
                key for key in self._memory_cache.keys()
                if f"user_{user_id}" in key or key.startswith(f"strategy_{user_id}_")
            ]
            for key in keys_to_remove:
                del self._memory_cache[key]
            
            # Clear stats cache
            if user_id in self._stats_cache:
                del self._stats_cache[user_id]
                
            logger.info(f"Cleared cache for user {user_id}")
        else:
            # Clear all cache
            self._memory_cache.clear()
            self._stats_cache.clear()
            logger.info("Cleared all memory cache")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        return {
            "cache_size": len(self._memory_cache),
            "stats_cache_size": len(self._stats_cache),
            "audit_trail_entries": len(self._audit_trail),
            "max_cache_size": self.MAX_CACHE_SIZE,
            "cache_ttl_minutes": self.CACHE_TTL_MINUTES,
            "cache_hit_ratio": "calculated_dynamically"  # Would need hit/miss counters for actual ratio
        }