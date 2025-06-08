"""
Intent Analyzer for Enhanced ALwrity Chatbot.

Advanced user intent analysis with context awareness and multi-intent detection.
"""

from typing import Dict, List, Any


class IntentAnalyzer:
    """Advanced user intent analysis with context awareness."""
    
    def __init__(self):
        self.intent_keywords = {
            "write": {
                "keywords": ["write", "create", "generate", "compose", "draft", "author", "produce", "craft"],
                "sub_intents": ["blog", "article", "story", "social", "product", "email", "copy", "script"]
            },
            "analyze": {
                "keywords": ["analyze", "review", "check", "examine", "evaluate", "audit", "assess", "study"],
                "sub_intents": ["seo", "competitor", "website", "content", "performance", "traffic", "keywords"]
            },
            "seo": {
                "keywords": ["seo", "optimize", "rank", "keyword", "search", "meta", "visibility", "serp"],
                "sub_intents": ["on_page", "technical", "content_gap", "backlinks", "local", "mobile"]
            },
            "social": {
                "keywords": ["social", "facebook", "twitter", "linkedin", "instagram", "youtube", "tiktok"],
                "sub_intents": ["post", "campaign", "engagement", "hashtags", "stories", "ads"]
            },
            "research": {
                "keywords": ["research", "competitor", "market", "trend", "keyword", "analysis", "study"],
                "sub_intents": ["competitor", "keyword", "market", "content_gap", "audience", "trends"]
            },
            "plan": {
                "keywords": ["plan", "strategy", "calendar", "schedule", "roadmap", "organize", "structure"],
                "sub_intents": ["content_calendar", "strategy", "campaign", "workflow", "editorial"]
            },
            "workflow": {
                "keywords": ["workflow", "automate", "process", "step", "guide", "complete", "pipeline"],
                "sub_intents": ["blog_creation", "seo_audit", "social_campaign", "content_strategy"]
            },
            "optimize": {
                "keywords": ["optimize", "improve", "enhance", "boost", "increase", "maximize", "refine"],
                "sub_intents": ["seo", "content", "performance", "conversion", "speed", "engagement"]
            },
            "learn": {
                "keywords": ["learn", "how", "tutorial", "guide", "help", "explain", "teach", "show"],
                "sub_intents": ["seo", "content", "social", "tools", "strategy", "best_practices"]
            },
            "fix": {
                "keywords": ["fix", "solve", "repair", "troubleshoot", "debug", "resolve", "correct"],
                "sub_intents": ["seo_issues", "technical", "content", "performance", "errors"]
            }
        }
        
        self.content_type_keywords = {
            "blog": ["blog", "article", "post", "content"],
            "social": ["social", "post", "tweet", "update", "story"],
            "email": ["email", "newsletter", "campaign", "sequence"],
            "video": ["video", "youtube", "script", "transcript"],
            "ad": ["ad", "advertisement", "promotion", "campaign"],
            "product": ["product", "description", "listing", "catalog"],
            "news": ["news", "press", "announcement", "release"],
            "story": ["story", "narrative", "fiction", "creative"],
            "technical": ["technical", "documentation", "manual", "guide"],
            "academic": ["academic", "research", "paper", "thesis"]
        }
        
        self.urgency_keywords = {
            "high": ["urgent", "asap", "immediately", "emergency", "critical", "now"],
            "medium": ["soon", "quickly", "fast", "priority", "important"],
            "low": ["eventually", "when possible", "later", "sometime"]
        }
        
        self.complexity_indicators = {
            "high": ["comprehensive", "detailed", "complete", "full", "extensive", "thorough"],
            "medium": ["moderate", "standard", "regular", "normal", "typical"],
            "low": ["simple", "basic", "quick", "brief", "short", "minimal"]
        }
    
    def analyze_user_intent(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enhanced user intent analysis with context awareness."""
        prompt_lower = prompt.lower()
        
        # Detect primary and secondary intents
        detected_intents = self._detect_intents(prompt_lower)
        
        # Detect sub-intents
        sub_intents = self._detect_sub_intents(prompt_lower, detected_intents)
        
        # Determine content types
        content_types = self._detect_content_types(prompt_lower)
        
        # Assess urgency
        urgency = self._assess_urgency(prompt_lower)
        
        # Determine complexity
        complexity = self._assess_complexity(prompt_lower)
        
        # Calculate confidence scores
        confidence_scores = self._calculate_confidence_scores(prompt_lower, detected_intents)
        
        # Context-aware enhancements
        if context:
            detected_intents, confidence_scores = self._enhance_with_context(
                detected_intents, confidence_scores, context, prompt_lower
            )
        
        # Determine primary intent
        primary_intent = self._determine_primary_intent(detected_intents, confidence_scores)
        
        # Generate suggestions
        suggested_workflows = self._suggest_workflows(detected_intents, content_types)
        suggested_tools = self._suggest_tools(detected_intents, sub_intents, content_types)
        
        return {
            "primary_intent": primary_intent,
            "all_intents": detected_intents,
            "sub_intents": sub_intents,
            "content_types": content_types,
            "confidence_scores": confidence_scores,
            "urgency": urgency,
            "complexity": complexity,
            "suggested_workflows": suggested_workflows,
            "suggested_tools": suggested_tools,
            "intent_strength": self._calculate_intent_strength(confidence_scores),
            "multi_intent": len(detected_intents) > 1,
            "context_enhanced": context is not None
        }
    
    def _detect_intents(self, prompt_lower: str) -> List[str]:
        """Detect all intents in the user prompt."""
        detected_intents = []
        
        for intent, data in self.intent_keywords.items():
            matches = sum(1 for keyword in data["keywords"] if keyword in prompt_lower)
            if matches > 0:
                detected_intents.append(intent)
        
        return detected_intents
    
    def _detect_sub_intents(self, prompt_lower: str, detected_intents: List[str]) -> List[str]:
        """Detect sub-intents based on primary intents."""
        sub_intents = []
        
        for intent in detected_intents:
            if intent in self.intent_keywords:
                for sub_intent in self.intent_keywords[intent]["sub_intents"]:
                    if sub_intent in prompt_lower:
                        sub_intents.append(sub_intent)
        
        return list(set(sub_intents))  # Remove duplicates
    
    def _detect_content_types(self, prompt_lower: str) -> List[str]:
        """Detect content types mentioned in the prompt."""
        content_types = []
        
        for content_type, keywords in self.content_type_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                content_types.append(content_type)
        
        return content_types
    
    def _assess_urgency(self, prompt_lower: str) -> Dict[str, Any]:
        """Assess the urgency level of the request."""
        urgency_level = "normal"
        urgency_score = 0.5
        
        for level, keywords in self.urgency_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in prompt_lower)
            if matches > 0:
                if level == "high":
                    urgency_level = "high"
                    urgency_score = 0.9
                    break
                elif level == "medium" and urgency_level == "normal":
                    urgency_level = "medium"
                    urgency_score = 0.7
                elif level == "low" and urgency_level == "normal":
                    urgency_level = "low"
                    urgency_score = 0.3
        
        return {
            "level": urgency_level,
            "score": urgency_score,
            "is_urgent": urgency_level in ["high", "medium"]
        }
    
    def _assess_complexity(self, prompt_lower: str) -> Dict[str, Any]:
        """Assess the complexity level of the request."""
        complexity_level = "medium"
        complexity_score = 0.5
        
        for level, keywords in self.complexity_indicators.items():
            matches = sum(1 for keyword in keywords if keyword in prompt_lower)
            if matches > 0:
                complexity_level = level
                complexity_score = {"high": 0.9, "medium": 0.5, "low": 0.3}[level]
                break
        
        # Additional complexity indicators
        word_count = len(prompt_lower.split())
        if word_count > 50:
            complexity_score = min(complexity_score + 0.2, 1.0)
        elif word_count < 10:
            complexity_score = max(complexity_score - 0.2, 0.1)
        
        return {
            "level": complexity_level,
            "score": complexity_score,
            "word_count": word_count
        }
    
    def _calculate_confidence_scores(self, prompt_lower: str, detected_intents: List[str]) -> Dict[str, float]:
        """Calculate confidence scores for detected intents."""
        confidence_scores = {}
        
        for intent in detected_intents:
            if intent in self.intent_keywords:
                keywords = self.intent_keywords[intent]["keywords"]
                matches = sum(1 for keyword in keywords if keyword in prompt_lower)
                confidence = matches / len(keywords)
                
                # Boost confidence for exact matches
                if intent in prompt_lower:
                    confidence += 0.3
                
                # Boost confidence for multiple keyword matches
                if matches > 2:
                    confidence += 0.2
                
                confidence_scores[intent] = min(confidence, 1.0)
        
        return confidence_scores
    
    def _enhance_with_context(self, detected_intents: List[str], confidence_scores: Dict[str, float], 
                             context: Dict[str, Any], prompt_lower: str) -> tuple:
        """Enhance intent detection with conversation context."""
        enhanced_intents = detected_intents.copy()
        enhanced_scores = confidence_scores.copy()
        
        # Recent conversation topics
        recent_topics = context.get("recent_topics", [])
        for topic in recent_topics:
            if topic.lower() in prompt_lower:
                # Boost related intents
                for intent in self.intent_keywords:
                    if topic.lower() in self.intent_keywords[intent]["keywords"]:
                        if intent in enhanced_scores:
                            enhanced_scores[intent] += 0.1
                        else:
                            enhanced_intents.append(intent)
                            enhanced_scores[intent] = 0.4
        
        # User preferences
        user_prefs = context.get("user_preferences", {})
        if user_prefs.get("content_preferences"):
            for pref in user_prefs["content_preferences"]:
                if pref in prompt_lower:
                    # Boost content creation intents
                    if "write" in enhanced_scores:
                        enhanced_scores["write"] += 0.15
        
        # Active workflows
        active_workflows = context.get("active_workflows", [])
        if active_workflows:
            # Boost workflow-related intents
            if "workflow" in enhanced_scores:
                enhanced_scores["workflow"] += 0.2
            else:
                enhanced_intents.append("workflow")
                enhanced_scores["workflow"] = 0.6
        
        # Tool usage history
        tool_history = context.get("tool_usage_history", [])
        if tool_history:
            last_tools = tool_history[-3:]  # Last 3 tools
            for tool in last_tools:
                # Map tools to intents and boost related intents
                tool_intent_mapping = {
                    "ai_blog_writer": "write",
                    "content_gap_analysis": "analyze",
                    "technical_seo": "seo",
                    "linkedin_writer": "social"
                }
                
                if tool in tool_intent_mapping:
                    intent = tool_intent_mapping[tool]
                    if intent in enhanced_scores:
                        enhanced_scores[intent] += 0.1
        
        return enhanced_intents, enhanced_scores
    
    def _determine_primary_intent(self, detected_intents: List[str], confidence_scores: Dict[str, float]) -> str:
        """Determine the primary intent from detected intents."""
        if not detected_intents:
            return "general"
        
        if len(detected_intents) == 1:
            return detected_intents[0]
        
        # Return intent with highest confidence
        primary_intent = max(detected_intents, key=lambda x: confidence_scores.get(x, 0))
        return primary_intent
    
    def _suggest_workflows(self, detected_intents: List[str], content_types: List[str]) -> List[str]:
        """Suggest relevant workflows based on intents and content types."""
        suggested_workflows = []
        
        # Intent-based workflow suggestions
        workflow_mapping = {
            "write": ["blog_creation_workflow", "content_strategy_workflow"],
            "analyze": ["competitor_analysis_workflow", "seo_audit_workflow"],
            "seo": ["seo_audit_workflow", "content_gap_workflow"],
            "social": ["social_media_workflow", "content_repurposing_workflow"],
            "plan": ["content_strategy_workflow", "editorial_calendar_workflow"]
        }
        
        for intent in detected_intents:
            if intent in workflow_mapping:
                suggested_workflows.extend(workflow_mapping[intent])
        
        # Content type specific workflows
        if "blog" in content_types:
            suggested_workflows.append("blog_creation_workflow")
        if "social" in content_types:
            suggested_workflows.append("social_media_workflow")
        
        return list(set(suggested_workflows))  # Remove duplicates
    
    def _suggest_tools(self, detected_intents: List[str], sub_intents: List[str], 
                      content_types: List[str]) -> List[str]:
        """Suggest relevant tools based on intents, sub-intents, and content types."""
        suggested_tools = []
        
        # Intent-based tool suggestions
        tool_mapping = {
            "write": ["ai_blog_writer", "story_writer", "email_writer"],
            "analyze": ["content_gap_analysis", "website_analyzer", "competitor_analyzer"],
            "seo": ["technical_seo", "on_page_seo", "keyword_research"],
            "social": ["linkedin_writer", "facebook_writer", "social_campaign"],
            "research": ["competitor_analysis", "keyword_research", "market_research"],
            "optimize": ["seo_optimizer", "content_optimizer", "performance_optimizer"]
        }
        
        for intent in detected_intents:
            if intent in tool_mapping:
                suggested_tools.extend(tool_mapping[intent])
        
        # Sub-intent specific tools
        sub_intent_tools = {
            "blog": ["ai_blog_writer", "seo_optimizer"],
            "competitor": ["competitor_analysis", "content_gap_analysis"],
            "technical": ["technical_seo", "performance_analyzer"],
            "social": ["linkedin_writer", "facebook_writer"]
        }
        
        for sub_intent in sub_intents:
            if sub_intent in sub_intent_tools:
                suggested_tools.extend(sub_intent_tools[sub_intent])
        
        # Content type specific tools
        content_tools = {
            "blog": ["ai_blog_writer", "seo_optimizer"],
            "social": ["linkedin_writer", "facebook_writer"],
            "email": ["email_writer", "campaign_creator"],
            "video": ["youtube_writer", "script_generator"]
        }
        
        for content_type in content_types:
            if content_type in content_tools:
                suggested_tools.extend(content_tools[content_type])
        
        return list(set(suggested_tools))  # Remove duplicates
    
    def _calculate_intent_strength(self, confidence_scores: Dict[str, float]) -> str:
        """Calculate overall intent strength."""
        if not confidence_scores:
            return "weak"
        
        max_confidence = max(confidence_scores.values())
        avg_confidence = sum(confidence_scores.values()) / len(confidence_scores)
        
        if max_confidence >= 0.8 and avg_confidence >= 0.6:
            return "strong"
        elif max_confidence >= 0.6 or avg_confidence >= 0.4:
            return "moderate"
        else:
            return "weak"
    
    def get_intent_explanation(self, intent_analysis: Dict[str, Any]) -> str:
        """Generate a human-readable explanation of the intent analysis."""
        primary = intent_analysis["primary_intent"]
        confidence = intent_analysis["confidence_scores"].get(primary, 0)
        urgency = intent_analysis["urgency"]["level"]
        complexity = intent_analysis["complexity"]["level"]
        
        explanation = f"Primary intent: {primary} (confidence: {confidence:.2f})\n"
        
        if intent_analysis["multi_intent"]:
            other_intents = [i for i in intent_analysis["all_intents"] if i != primary]
            explanation += f"Additional intents: {', '.join(other_intents)}\n"
        
        if intent_analysis["content_types"]:
            explanation += f"Content types: {', '.join(intent_analysis['content_types'])}\n"
        
        explanation += f"Urgency: {urgency}, Complexity: {complexity}\n"
        
        if intent_analysis["suggested_tools"]:
            explanation += f"Recommended tools: {', '.join(intent_analysis['suggested_tools'][:3])}"
        
        return explanation 