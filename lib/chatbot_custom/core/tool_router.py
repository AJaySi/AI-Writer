"""
Smart Tool Router for Enhanced ALwrity Chatbot.

Intelligent tool routing based on user intent and context.
"""

from typing import Dict, List, Any


class SmartToolRouter:
    """Intelligent tool routing based on user intent and context."""
    
    def __init__(self):
        self.tool_categories = {
            "content_creation": [
                "ai_blog_writer", "story_writer", "essay_writer", 
                "product_description", "email_writer", "news_writer"
            ],
            "seo_tools": [
                "content_gap_analysis", "technical_seo", "on_page_seo", 
                "competitor_analysis", "keyword_research", "meta_generator"
            ],
            "social_media": [
                "linkedin_writer", "facebook_writer", "youtube_writer", 
                "instagram_writer", "twitter_writer", "social_campaign"
            ],
            "analysis": [
                "website_analyzer", "content_analyzer", "competitor_analyzer",
                "performance_analyzer", "seo_analyzer"
            ],
            "planning": [
                "content_calendar", "content_repurposing", "strategy_planner",
                "campaign_planner", "editorial_calendar"
            ],
            "optimization": [
                "seo_optimizer", "content_optimizer", "performance_optimizer",
                "conversion_optimizer", "speed_optimizer"
            ]
        }
        
        self.intent_tool_mapping = {
            "write": ["ai_blog_writer", "story_writer", "essay_writer", "email_writer"],
            "analyze": ["content_gap_analysis", "technical_seo", "website_analyzer", "competitor_analyzer"],
            "seo": ["on_page_seo", "technical_seo", "content_gap_analysis", "seo_optimizer"],
            "social": ["linkedin_writer", "facebook_writer", "youtube_writer", "social_campaign"],
            "plan": ["content_calendar", "content_repurposing", "strategy_planner", "campaign_planner"],
            "research": ["competitor_analysis", "content_gap_analysis", "keyword_research", "market_research"],
            "optimize": ["seo_optimizer", "content_optimizer", "performance_optimizer"],
            "create": ["ai_blog_writer", "content_creator", "social_content_creation"],
            "audit": ["technical_seo", "seo_analyzer", "website_analyzer", "performance_analyzer"]
        }
        
        # Tool confidence weights based on effectiveness
        self.tool_weights = {
            "ai_blog_writer": 0.9,
            "content_gap_analysis": 0.85,
            "technical_seo": 0.8,
            "linkedin_writer": 0.85,
            "competitor_analysis": 0.8,
            "seo_optimizer": 0.75,
            "content_calendar": 0.7
        }
    
    def route_to_tools(self, user_intent: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Route user intent to relevant tools with confidence scoring."""
        suggested_tools = []
        user_intent_lower = user_intent.lower()
        
        # Primary intent matching
        for intent, tools in self.intent_tool_mapping.items():
            if intent in user_intent_lower:
                for tool in tools:
                    confidence = self._calculate_confidence(intent, user_intent, context)
                    suggested_tools.append({
                        "tool": tool,
                        "category": self._get_tool_category(tool),
                        "confidence": confidence,
                        "intent_match": intent,
                        "reason": f"Matches '{intent}' intent"
                    })
        
        # Context-based suggestions
        context_tools = self._get_context_based_suggestions(context, user_intent)
        suggested_tools.extend(context_tools)
        
        # Remove duplicates and sort by confidence
        unique_tools = {}
        for tool in suggested_tools:
            tool_name = tool["tool"]
            if tool_name not in unique_tools or tool["confidence"] > unique_tools[tool_name]["confidence"]:
                unique_tools[tool_name] = tool
        
        # Sort by confidence and return top suggestions
        sorted_tools = sorted(unique_tools.values(), key=lambda x: x["confidence"], reverse=True)
        return sorted_tools[:8]  # Return top 8 suggestions
    
    def _get_tool_category(self, tool: str) -> str:
        """Get category for a tool."""
        for category, tools in self.tool_categories.items():
            if tool in tools:
                return category
        return "general"
    
    def _calculate_confidence(self, intent: str, user_text: str, context: Dict[str, Any]) -> float:
        """Calculate confidence score for tool suggestion."""
        base_score = 0.5
        user_text_lower = user_text.lower()
        
        # Intent match bonus
        if intent in user_text_lower:
            base_score += 0.3
        
        # Keyword bonuses
        keyword_bonuses = {
            "write": ["create", "generate", "compose", "draft", "author", "produce"],
            "analyze": ["check", "review", "examine", "evaluate", "assess", "study"],
            "seo": ["optimize", "rank", "search", "keywords", "meta", "visibility"],
            "social": ["post", "share", "engage", "campaign", "viral", "audience"],
            "plan": ["schedule", "organize", "strategy", "roadmap", "timeline"],
            "research": ["study", "investigate", "explore", "discover", "find"]
        }
        
        if intent in keyword_bonuses:
            for keyword in keyword_bonuses[intent]:
                if keyword in user_text_lower:
                    base_score += 0.1
        
        # Context bonuses
        if context:
            # Recent tool usage
            recent_tools = context.get('tool_usage_history', [])[-3:]
            if any(tool in user_text_lower for tool in recent_tools):
                base_score += 0.15
            
            # User preferences
            user_prefs = context.get('user_preferences', {})
            if user_prefs.get('industry') and user_prefs['industry'].lower() in user_text_lower:
                base_score += 0.1
        
        # Urgency bonus
        urgency_keywords = ["urgent", "asap", "quickly", "fast", "immediate", "now"]
        if any(keyword in user_text_lower for keyword in urgency_keywords):
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _get_context_based_suggestions(self, context: Dict[str, Any], user_intent: str) -> List[Dict[str, Any]]:
        """Get tool suggestions based on conversation context."""
        context_tools = []
        
        if not context:
            return context_tools
        
        # Recent tool usage patterns
        recent_tools = context.get('tool_usage_history', [])
        if recent_tools:
            # Suggest complementary tools
            last_tool = recent_tools[-1] if recent_tools else None
            complementary_tools = self._get_complementary_tools(last_tool)
            
            for tool in complementary_tools:
                context_tools.append({
                    "tool": tool,
                    "category": self._get_tool_category(tool),
                    "confidence": 0.6,
                    "intent_match": "context",
                    "reason": f"Complements recent use of {last_tool}"
                })
        
        # Active workflows
        active_workflows = context.get('active_workflows', [])
        if active_workflows:
            # Suggest tools for current workflow steps
            for workflow in active_workflows:
                workflow_tools = self._get_workflow_tools(workflow)
                for tool in workflow_tools:
                    context_tools.append({
                        "tool": tool,
                        "category": self._get_tool_category(tool),
                        "confidence": 0.7,
                        "intent_match": "workflow",
                        "reason": f"Next step in {workflow} workflow"
                    })
        
        # User preferences
        user_prefs = context.get('user_preferences', {})
        if user_prefs.get('content_preferences'):
            pref_tools = self._get_preference_based_tools(user_prefs['content_preferences'])
            for tool in pref_tools:
                context_tools.append({
                    "tool": tool,
                    "category": self._get_tool_category(tool),
                    "confidence": 0.65,
                    "intent_match": "preference",
                    "reason": "Based on your content preferences"
                })
        
        return context_tools
    
    def _get_complementary_tools(self, last_tool: str) -> List[str]:
        """Get tools that complement the last used tool."""
        complementary_mapping = {
            "ai_blog_writer": ["seo_optimizer", "meta_generator", "content_gap_analysis"],
            "content_gap_analysis": ["ai_blog_writer", "keyword_research", "competitor_analysis"],
            "technical_seo": ["on_page_seo", "content_optimizer", "performance_analyzer"],
            "linkedin_writer": ["social_campaign", "content_calendar", "hashtag_research"],
            "competitor_analysis": ["content_gap_analysis", "keyword_research", "strategy_planner"],
            "keyword_research": ["ai_blog_writer", "content_gap_analysis", "seo_optimizer"]
        }
        
        return complementary_mapping.get(last_tool, [])
    
    def _get_workflow_tools(self, workflow: str) -> List[str]:
        """Get tools associated with a specific workflow."""
        workflow_tools = {
            "blog_creation_workflow": ["keyword_research", "ai_blog_writer", "seo_optimizer"],
            "competitor_analysis_workflow": ["competitor_analysis", "content_gap_analysis"],
            "social_media_workflow": ["linkedin_writer", "facebook_writer", "social_campaign"],
            "seo_audit_workflow": ["technical_seo", "on_page_seo", "competitor_analysis"]
        }
        
        return workflow_tools.get(workflow, [])
    
    def _get_preference_based_tools(self, content_preferences: List[str]) -> List[str]:
        """Get tools based on user content preferences."""
        preference_tools = []
        
        for pref in content_preferences:
            if pref in ["blog", "article"]:
                preference_tools.extend(["ai_blog_writer", "seo_optimizer"])
            elif pref in ["social", "post"]:
                preference_tools.extend(["linkedin_writer", "facebook_writer"])
            elif pref in ["seo", "optimization"]:
                preference_tools.extend(["technical_seo", "on_page_seo"])
        
        return list(set(preference_tools))  # Remove duplicates
    
    def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific tool."""
        tool_info = {
            "ai_blog_writer": {
                "name": "AI Blog Writer",
                "description": "Create comprehensive, SEO-optimized blog posts",
                "category": "content_creation",
                "use_cases": ["Blog posts", "Articles", "Long-form content"],
                "estimated_time": "5-10 minutes"
            },
            "content_gap_analysis": {
                "name": "Content Gap Analysis",
                "description": "Identify content opportunities vs competitors",
                "category": "seo_tools",
                "use_cases": ["Competitor research", "Content strategy", "SEO planning"],
                "estimated_time": "10-15 minutes"
            },
            "technical_seo": {
                "name": "Technical SEO Crawler",
                "description": "Comprehensive technical SEO audit",
                "category": "seo_tools",
                "use_cases": ["Site audits", "Technical issues", "Performance analysis"],
                "estimated_time": "15-20 minutes"
            },
            "linkedin_writer": {
                "name": "LinkedIn Writer",
                "description": "Create professional LinkedIn content",
                "category": "social_media",
                "use_cases": ["LinkedIn posts", "Professional articles", "Networking content"],
                "estimated_time": "3-5 minutes"
            }
        }
        
        return tool_info.get(tool_name, {
            "name": tool_name.replace('_', ' ').title(),
            "description": f"ALwrity {tool_name.replace('_', ' ')} tool",
            "category": self._get_tool_category(tool_name),
            "use_cases": ["Content creation", "Analysis", "Optimization"],
            "estimated_time": "5-10 minutes"
        })
    
    def get_category_tools(self, category: str) -> List[str]:
        """Get all tools in a specific category."""
        return self.tool_categories.get(category, [])
    
    def get_all_categories(self) -> List[str]:
        """Get all available tool categories."""
        return list(self.tool_categories.keys()) 