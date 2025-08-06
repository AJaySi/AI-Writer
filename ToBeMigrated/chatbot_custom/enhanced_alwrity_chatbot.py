#!/usr/bin/env python3
"""
Enhanced ALwrity Chatbot - Complete Modular Version

An intelligent conversational AI assistant that provides comprehensive writing assistance,
SEO analysis, workflow automation, and content creation tools.
"""

import time
import os
import json
import streamlit as st
import sys
import traceback
import tempfile
import requests
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import pandas as pd
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Constants
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '🤖'
USER_AVATAR_ICON = '👤'
DATA_DIR = 'data/chatbot/'

# Initialize import flags
IMPORTS_SUCCESSFUL = True
IMPORT_ERRORS = []

try:
    # Import ALwrity components
    from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
except ImportError as e:
    IMPORT_ERRORS.append(f"Text generation: {str(e)}")
    llm_text_gen = None

try:
    from lib.ai_writers.ai_writer_dashboard import list_ai_writers
except ImportError as e:
    IMPORT_ERRORS.append(f"AI writers: {str(e)}")
    list_ai_writers = lambda: []

try:
    from lib.ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
except ImportError as e:
    IMPORT_ERRORS.append(f"Content gap analysis: {str(e)}")
    ContentGapAnalysis = None

try:
    from lib.database.models import ContentItem
except ImportError as e:
    IMPORT_ERRORS.append(f"Database models: {str(e)}")
    ContentItem = None

try:
    from lib.ai_seo_tools.content_calendar.ui.components.content_repurposing_ui import ContentRepurposingUI
except ImportError as e:
    IMPORT_ERRORS.append(f"Content repurposing: {str(e)}")
    ContentRepurposingUI = None

try:
    from lib.utils.alwrity_utils import essay_writer, ai_news_writer, ai_finance_ta_writer
except ImportError as e:
    IMPORT_ERRORS.append(f"ALwrity utils: {str(e)}")
    essay_writer = ai_news_writer = ai_finance_ta_writer = None

try:
    from lib.ai_writers.ai_blog_writer.ai_blog_generator import ai_blog_writer_page
    from lib.ai_writers.ai_story_writer.story_writer import story_input_section
    from lib.ai_writers.ai_product_description_writer import write_ai_prod_desc
    from lib.ai_writers.linkedin_writer import LinkedInAIWriter
    from lib.ai_writers.ai_facebook_writer.facebook_ai_writer import FacebookAIWriter
    from lib.ai_writers.youtube_writers.youtube_ai_writer import youtube_main_menu
except ImportError as e:
    IMPORT_ERRORS.append(f"AI writers modules: {str(e)}")

try:
    from lib.ai_seo_tools.on_page_seo_analyzer import analyze_onpage_seo, fetch_seo_data
    from lib.ai_seo_tools.weburl_seo_checker import run_analysis
    from lib.ai_seo_tools.technical_seo_crawler.crawler import TechnicalSEOCrawler
except ImportError as e:
    IMPORT_ERRORS.append(f"SEO tools: {str(e)}")
    analyze_onpage_seo = fetch_seo_data = run_analysis = None
    TechnicalSEOCrawler = None

try:
    # Import core modules
    from .core.workflow_engine import WorkflowEngine
    from .core.tool_router import SmartToolRouter
    from .core.intent_analyzer import IntentAnalyzer
    from .core.context_manager import ContextManager
except ImportError as e:
    IMPORT_ERRORS.append(f"Core modules: {str(e)}")
    WorkflowEngine = SmartToolRouter = IntentAnalyzer = ContextManager = None

try:
    # Import UI components
    from .ui.sidebar import SidebarManager
except ImportError as e:
    IMPORT_ERRORS.append(f"UI components: {str(e)}")
    SidebarManager = None

# Check if UI init exists
try:
    ui_init_path = Path(__file__).parent / "ui" / "__init__.py"
    if not ui_init_path.exists():
        # Create basic init file if missing
        ui_init_path.parent.mkdir(exist_ok=True)
        ui_init_path.write_text('"""UI Components for Enhanced ALwrity Chatbot."""\n')
except Exception as e:
    IMPORT_ERRORS.append(f"UI init setup: {str(e)}")

# Set global flag
if IMPORT_ERRORS:
    IMPORTS_SUCCESSFUL = False


class EnhancedALwrityChatbot:
    """Enhanced ALwrity Chatbot with comprehensive content creation capabilities."""
    
    def __init__(self):
        """Initialize the enhanced chatbot."""
        self.initialize_session_state()
        self.setup_ai_model()
        self.load_ai_writers()
        
        # Initialize core components with error handling
        try:
            self.workflow_engine = WorkflowEngine() if WorkflowEngine else None
            self.tool_router = SmartToolRouter() if SmartToolRouter else None
            self.intent_analyzer = IntentAnalyzer() if IntentAnalyzer else None
            self.context_manager = ContextManager() if ContextManager else None
            self.content_gap_analyzer = ContentGapAnalysis() if ContentGapAnalysis else None
            self.technical_seo_crawler = TechnicalSEOCrawler() if TechnicalSEOCrawler else None
        except Exception as e:
            st.warning(f"Some advanced features may not be available: {str(e)}")
            self.workflow_engine = None
            self.tool_router = None
            self.intent_analyzer = None
            self.context_manager = None
            self.content_gap_analyzer = None
            self.technical_seo_crawler = None
        
        # Initialize UI components with error handling
        try:
            self.sidebar_manager = SidebarManager(
                self.context_manager, 
                self.workflow_engine, 
                self.tool_router
            ) if SidebarManager and self.context_manager else None
        except Exception as e:
            st.warning(f"Advanced UI features may not be available: {str(e)}")
            self.sidebar_manager = None
        
        # Track UI state
        if "ui_state" not in st.session_state:
            st.session_state.ui_state = {}
    
    def initialize_session_state(self):
        """Initialize session state variables."""
        if "enhanced_chat_messages" not in st.session_state:
            st.session_state.enhanced_chat_messages = [
                {
                    "role": "assistant", 
                    "content": "🚀 **Welcome to Enhanced ALwrity - Your AI Content Creation Hub!**\n\n"
                              "I'm your intelligent assistant that can help you with:\n\n"
                              "**🎯 Smart Content Creation**\n"
                              "• Blog posts, articles, stories with AI optimization\n"
                              "• Social media content for all platforms\n"
                              "• Product descriptions and marketing copy\n\n"
                              "**🔍 Advanced SEO & Analysis**\n"
                              "• Content gap analysis vs competitors\n"
                              "• Technical SEO audits and recommendations\n"
                              "• Keyword research and optimization\n\n"
                              "**📊 Intelligent Workflows**\n"
                              "• Multi-tool automation for complex tasks\n"
                              "• Content calendar and strategy planning\n"
                              "• Document analysis and insights\n\n"
                              "**💡 What makes me special:**\n"
                              "• I suggest the best tools for your specific needs\n"
                              "• I can chain multiple tools together for complex workflows\n"
                              "• I learn from your preferences and improve suggestions\n\n"
                              "**Ready to create amazing content? Try asking:**\n"
                              "• *\"Help me write a blog post about sustainable technology\"*\n"
                              "• *\"Analyze my website's SEO compared to competitors\"*\n"
                              "• *\"Create a social media campaign for my product launch\"*\n\n"
                              "What content challenge can I help you solve today? 🎨",
                    "avatar": AI_AVATAR_ICON
                }
            ]
        
        # Enhanced context tracking
        if "chat_context" not in st.session_state:
            st.session_state.chat_context = {
                "current_task": None,
                "user_preferences": {
                    "preferred_writing_style": None,
                    "industry": None,
                    "target_audience": None,
                    "content_goals": []
                },
                "uploaded_files": [],
                "content_history": [],
                "active_workflows": [],
                "tool_usage_history": [],
                "conversation_summary": ""
            }
            
        if "content_workspace" not in st.session_state:
            st.session_state.content_workspace = {
                "drafts": [],
                "templates": [],
                "research_data": {},
                "seo_insights": {},
                "competitor_data": {},
                "keyword_data": {}
            }
        
        # Initialize messages for modular interface
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def setup_ai_model(self):
        """Setup the AI model for conversation."""
        try:
            # Using ALwrity's main text generation instead of direct API calls
            st.session_state.enhanced_model_ready = True
        except Exception as e:
            st.error(f"Error setting up AI model: {str(e)}")
    
    def load_ai_writers(self):
        """Load available AI writers."""
        try:
            if list_ai_writers:
                self.ai_writers = list_ai_writers()
                self.writer_functions = {
                    writer['name']: writer['function'] for writer in self.ai_writers
                }
            else:
                self.ai_writers = []
                self.writer_functions = {}
        except Exception as e:
            st.warning(f"Could not load AI writers: {str(e)}")
            self.ai_writers = []
            self.writer_functions = {}
    
    def process_message(self, prompt: str) -> str:
        """Process user message and generate response."""
        try:
            # Ensure session state is properly initialized
            if "chat_context" not in st.session_state:
                st.warning("🔧 Initializing session state...")
                self.initialize_session_state()
            
            # Validate session state structure
            if not isinstance(st.session_state.chat_context, dict):
                st.error(f"🐛 Invalid chat_context type: {type(st.session_state.chat_context)}")
                st.session_state.chat_context = {
                    "user_preferences": {},
                    "tool_usage_history": [],
                    "active_workflows": [],
                    "conversation_summary": ""
                }
            
            # Analyze user intent if available
            if self.intent_analyzer:
                try:
                    intent = self.intent_analyzer.analyze_user_intent(prompt, st.session_state.chat_context)
                    
                    # Debug: Log the type and content of intent
                    if not isinstance(intent, dict):
                        st.error(f"🐛 DEBUG: Intent analyzer returned {type(intent)}: {intent}")
                        intent = self._create_fallback_intent(prompt)
                    
                    # Validate that intent is a dictionary
                    if not isinstance(intent, dict):
                        st.warning(f"Intent analyzer returned unexpected type: {type(intent)}")
                        intent = self._create_fallback_intent(prompt)
                    
                    # Ensure required keys exist
                    required_keys = ['primary_intent', 'all_intents', 'sub_intents', 'content_types', 'urgency', 'complexity']
                    for key in required_keys:
                        if key not in intent:
                            intent[key] = self._get_default_intent_value(key)
                    
                    # Final validation before proceeding
                    if not isinstance(intent, dict):
                        st.error("🚨 Critical: Intent is still not a dictionary after fallback. Creating emergency fallback.")
                        intent = {
                            "primary_intent": "general",
                            "all_intents": ["general"],
                            "sub_intents": [],
                            "content_types": [],
                            "urgency": {"level": "normal", "score": 0.5, "is_urgent": False},
                            "complexity": {"level": "medium", "score": 0.5, "word_count": len(prompt.split())},
                            "suggested_workflows": [],
                            "suggested_tools": []
                        }
                    
                    # Generate response based on intent
                    response = self.generate_contextual_response(prompt, intent)
                    # Update conversation context
                    self.update_conversation_context(prompt, response, intent)
                    
                except Exception as intent_error:
                    st.warning(f"Intent analysis failed: {str(intent_error)}. Using fallback mode.")
                    # Create fallback intent structure
                    intent = self._create_fallback_intent(prompt)
                    response = self.generate_contextual_response(prompt, intent)
                    self.update_conversation_context(prompt, response, intent)
            else:
                # Fallback to simple text generation
                response = self.generate_simple_response(prompt)
            
            return response
            
        except Exception as e:
            st.error(f"🚨 Critical error in process_message: {str(e)}")
            return f"I apologize, but I encountered an error processing your request: {str(e)}. Let me suggest some alternative approaches based on what you're trying to achieve."
    
    def generate_contextual_response(self, prompt: str, intent: Dict[str, Any]) -> str:
        """Enhanced contextual response generation with smart tool integration."""
        try:
            # Validate intent parameter
            if not isinstance(intent, dict):
                st.warning("Invalid intent data received. Using fallback response.")
                return self.generate_simple_response(prompt)
            
            # Build comprehensive context
            context = self.build_comprehensive_context()
            
            # Create advanced system prompt
            system_prompt = self.create_advanced_system_prompt(intent, context)
            
            # Safely extract intent values with defaults
            primary_intent = intent.get('primary_intent', 'general')
            all_intents = intent.get('all_intents', [primary_intent])
            sub_intents = intent.get('sub_intents', [])
            content_types = intent.get('content_types', [])
            complexity = intent.get('complexity', {})
            urgency = intent.get('urgency', {})
            suggested_workflows = intent.get('suggested_workflows', [])
            suggested_tools = intent.get('suggested_tools', [])
            
            # Generate enhanced AI prompt
            ai_prompt = f"""
            **CONVERSATION CONTEXT:**
            {context}
            
            **USER INTENT ANALYSIS:**
            • Primary Intent: {primary_intent}
            • All Intents: {', '.join(all_intents)}
            • Sub-intents: {', '.join(sub_intents)}
            • Content Types: {', '.join(content_types)}
            • Complexity: {complexity.get('level', 'medium')}
            • Urgency: {"High" if urgency.get('is_urgent', False) else "Normal"}
            
            **USER MESSAGE:** {prompt}
            
            **RESPONSE INSTRUCTIONS:**
            1. **Immediate Value**: Provide actionable insights right away
            2. **Tool Integration**: Suggest specific ALwrity tools with clear benefits
            3. **Workflow Automation**: Recommend multi-step workflows when appropriate
            4. **Personalization**: Use context to personalize suggestions
            5. **Next Steps**: Always provide clear next steps
            
            **AVAILABLE ALWRITY ECOSYSTEM:**
            • AI Writers: {[w.get('name', 'Unknown') if isinstance(w, dict) else str(w) for w in self.ai_writers] if self.ai_writers else ['Basic AI Writer']}
            • SEO Tools: Content Gap Analysis, Technical SEO Crawler, On-Page SEO
            • Workflows: {[w.get('name', 'Workflow') if isinstance(w, dict) else str(w) for w in suggested_workflows] if suggested_workflows else ['Basic Workflow']}
            • Smart Tools: {[t.get('tool', 'Tool') if isinstance(t, dict) else str(t) for t in suggested_tools[:3]] if suggested_tools else ['Basic Tools']}
            
            **RESPONSE STRUCTURE:**
            1. Acknowledge user's specific need
            2. Provide immediate helpful information
            3. Suggest relevant tools with clear value propositions
            4. Offer workflow automation if applicable
            5. Include actionable next steps with buttons/links
            
            Create a response that is conversational, helpful, and leverages ALwrity's full capabilities.
            """
            
            if llm_text_gen:
                response = llm_text_gen(
                    prompt=ai_prompt,
                    system_prompt=system_prompt
                )
            else:
                response = f"I understand you're looking for help with {primary_intent}. While I'm running in limited mode, I can still assist you with basic guidance and suggestions."
            
            # Add smart tool suggestions and workflow recommendations
            response += self.add_smart_suggestions(intent, prompt)
            
            # Add quick actions if relevant
            response += self.add_contextual_actions(intent, prompt)
            
            return response
            
        except Exception as e:
            st.error(f"Error in contextual response generation: {str(e)}")
            return f"I apologize, but I encountered an error processing your request: {str(e)}. Let me suggest some alternative approaches based on what you're trying to achieve."
    
    def create_advanced_system_prompt(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Create an advanced system prompt based on intent and context."""
        try:
            base_prompt = """You are ALwrity AI, the most advanced content creation and SEO assistant. You have deep expertise in:

• Content Strategy & Creation across all formats and platforms
• Advanced SEO optimization and technical analysis  
• Competitive intelligence and market research
• Multi-platform social media marketing
• Workflow automation and process optimization
• Data-driven content performance analysis

You are equipped with a comprehensive suite of specialized tools and can orchestrate complex workflows."""
            
            # Add intent-specific expertise
            intent_expertise = {
                "write": "Focus on content creation excellence, writing optimization, and audience engagement strategies.",
                "analyze": "Focus on data analysis, competitive intelligence, and actionable insights generation.",
                "seo": "Focus on technical SEO, content optimization, and search performance improvement.",
                "social": "Focus on platform-specific optimization, audience engagement, and viral content creation.",
                "research": "Focus on market intelligence, competitor analysis, and opportunity identification.",
                "plan": "Focus on strategic planning, workflow optimization, and systematic execution.",
                "workflow": "Focus on process automation, multi-tool integration, and efficiency optimization."
            }
            
            # Safely get primary intent
            primary_intent = 'general'
            if isinstance(intent, dict):
                primary_intent = intent.get('primary_intent', 'general')
            
            specific_expertise = intent_expertise.get(primary_intent, "Provide comprehensive, expert assistance.")
            
            # Add context awareness
            context_prompt = ""
            if isinstance(context, dict):
                user_preferences = context.get('user_preferences', {})
                if isinstance(user_preferences, dict):
                    if user_preferences.get('industry'):
                        context_prompt += f"\n• User's Industry: {user_preferences['industry']}"
                    if user_preferences.get('target_audience'):
                        context_prompt += f"\n• Target Audience: {user_preferences['target_audience']}"
                
                tool_usage_history = context.get('tool_usage_history', [])
                if isinstance(tool_usage_history, list) and tool_usage_history:
                    recent_tools = [tool for tool in tool_usage_history[-3:] if tool]
                    if recent_tools:
                        context_prompt += f"\n• Recently Used Tools: {', '.join(recent_tools)}"
            
            return f"{base_prompt}\n\n{specific_expertise}\n\nCONTEXT AWARENESS:{context_prompt}\n\nAlways provide specific, actionable guidance and leverage ALwrity's ecosystem effectively."
            
        except Exception as e:
            st.warning(f"Error creating system prompt: {str(e)}")
            return """You are ALwrity AI, a helpful content creation and SEO assistant. Provide clear, helpful, and actionable responses about writing, content creation, and SEO guidance."""
    
    def build_comprehensive_context(self) -> Dict[str, Any]:
        """Build comprehensive context from conversation history and user data."""
        context = {
            "conversation_length": len(st.session_state.enhanced_chat_messages),
            "user_preferences": st.session_state.chat_context.get("user_preferences", {}),
            "tool_usage_history": st.session_state.chat_context.get("tool_usage_history", []),
            "active_workflows": st.session_state.chat_context.get("active_workflows", []),
            "recent_topics": [],
            "content_workspace": st.session_state.content_workspace
        }
        
        # Extract recent topics from conversation
        recent_messages = st.session_state.enhanced_chat_messages[-5:]
        for msg in recent_messages:
            if msg['role'] == 'user':
                # Simple keyword extraction
                words = msg['content'].lower().split()
                context["recent_topics"].extend([word for word in words if len(word) > 4])
        
        # Remove duplicates and limit
        context["recent_topics"] = list(set(context["recent_topics"]))[:10]
        
        return context
    
    def add_smart_suggestions(self, intent: Dict[str, Any], prompt: str) -> str:
        """Add smart tool suggestions based on intent analysis."""
        try:
            # Validate intent parameter with detailed logging
            if not isinstance(intent, dict):
                st.error(f"🐛 add_smart_suggestions received {type(intent)}: {intent}")
                return "\n\n**🎯 Smart Recommendations:** Available in full mode."
            
            suggestions = "\n\n**🎯 Smart Recommendations:**\n"
            
            # Add workflow suggestions if available
            suggested_workflows = intent.get('suggested_workflows', [])
            if suggested_workflows:
                suggestions += "\n**🔄 Automated Workflows:**\n"
                for workflow in suggested_workflows[:2]:
                    if isinstance(workflow, dict):
                        workflow_name = workflow.get('name', 'Workflow')
                        workflow_desc = workflow.get('description', 'Automated process')
                        suggestions += f"• **{workflow_name}** - {workflow_desc}\n"
                    else:
                        suggestions += f"• **{workflow}** - Automated process\n"
            
            # Add tool suggestions
            suggested_tools = intent.get('suggested_tools', [])
            if suggested_tools:
                suggestions += "\n**🛠️ Recommended Tools:**\n"
                for tool in suggested_tools[:3]:
                    if isinstance(tool, dict):
                        tool_name = tool.get('tool', '').replace('_', ' ').title()
                        confidence = tool.get('confidence', 0.5)
                        confidence_indicator = "🔥" if confidence > 0.8 else "⭐" if confidence > 0.6 else "💡"
                        category = tool.get('category', 'general')
                        suggestions += f"• {confidence_indicator} **{tool_name}** ({category})\n"
                    else:
                        tool_name = str(tool).replace('_', ' ').title()
                        suggestions += f"• 💡 **{tool_name}** (general)\n"
            
            # Add content-specific suggestions
            content_types = intent.get('content_types', [])
            if 'blog' in content_types:
                suggestions += "\n**📝 Blog Creation Pipeline:**\n"
                suggestions += "• Keyword Research → Content Gap Analysis → AI Writing → SEO Optimization\n"
            
            primary_intent = intent.get('primary_intent', 'general')
            if primary_intent == 'seo':
                suggestions += "\n**🔍 SEO Analysis Suite:**\n"
                suggestions += "• Technical SEO Audit → Content Optimization → Competitor Analysis\n"
            
            return suggestions
            
        except Exception as e:
            st.error(f"🚨 Error in add_smart_suggestions: {str(e)}")
            return "\n\n**🎯 Smart Recommendations:** Available in full mode."
    
    def add_contextual_actions(self, intent: Dict[str, Any], prompt: str) -> str:
        """Add contextual action buttons and quick starts."""
        try:
            # Validate intent parameter with detailed logging
            if not isinstance(intent, dict):
                st.error(f"🐛 add_contextual_actions received {type(intent)}: {intent}")
                return "\n\n**⚡ Quick Actions:** Available in full mode."
            
            actions = "\n\n**⚡ Quick Actions:**\n"
            
            # Intent-based actions
            primary_intent = intent.get('primary_intent', 'general')
            if primary_intent == 'write':
                actions += "🎬 [Start Blog Workflow] | 📱 [Social Media Creation] | ✍️ [Custom Writing]\n"
            elif primary_intent == 'analyze':
                actions += "🔍 [Website Analysis] | 🏆 [Competitor Research] | 📊 [Content Audit]\n"
            elif primary_intent == 'seo':
                actions += "🎯 [SEO Audit] | 📈 [Content Gap Analysis] | 🔧 [Technical SEO]\n"
            elif primary_intent == 'plan':
                actions += "📅 [Content Calendar] | 🗺️ [Strategy Planning] | 🔄 [Workflow Setup]\n"
            
            # Add urgency-based actions
            urgency = intent.get('urgency', {})
            if isinstance(urgency, dict) and urgency.get('is_urgent', False):
                actions += "\n**🚨 Express Options:** Fast-track tools for immediate results\n"
            
            # Add follow-up suggestions
            actions += "\n**💬 Try asking:**\n"
            follow_ups = self.generate_follow_up_questions(intent)
            for follow_up in follow_ups[:3]:
                actions += f"• *\"{follow_up}\"*\n"
            
            return actions
            
        except Exception as e:
            st.error(f"🚨 Error in add_contextual_actions: {str(e)}")
            return "\n\n**⚡ Quick Actions:** Available in full mode."
    
    def generate_follow_up_questions(self, intent: Dict[str, Any]) -> List[str]:
        """Generate relevant follow-up questions based on intent."""
        try:
            # Validate intent parameter
            if not isinstance(intent, dict):
                return [
                    "What specific aspect would you like help with?",
                    "Should I suggest a workflow to automate this process?",
                    "Would you like me to analyze any existing content?"
                ]
            
            follow_ups = {
                "write": [
                    "What tone should I use for my target audience?",
                    "Can you help me optimize this content for SEO?",
                    "How can I repurpose this content for social media?"
                ],
                "analyze": [
                    "What are my biggest content gaps compared to competitors?",
                    "Which keywords should I target next?",
                    "How can I improve my website's SEO score?"
                ],
                "seo": [
                    "What technical SEO issues should I fix first?",
                    "How can I improve my content's search rankings?",
                    "What keywords are my competitors ranking for?"
                ],
                "plan": [
                    "How often should I publish new content?",
                    "What content types perform best in my industry?",
                    "Can you create a content calendar for next month?"
                ]
            }
            
            primary_intent = intent.get('primary_intent', 'general')
            return follow_ups.get(primary_intent, [
                "What specific aspect would you like help with?",
                "Should I suggest a workflow to automate this process?",
                "Would you like me to analyze any existing content?"
            ])
            
        except Exception as e:
            st.warning(f"Error generating follow-up questions: {str(e)}")
            return [
                "What specific aspect would you like help with?",
                "Should I suggest a workflow to automate this process?",
                "Would you like me to analyze any existing content?"
            ]
    
    def update_conversation_context(self, prompt: str, response: str, intent: Dict[str, Any]):
        """Update conversation context with new information."""
        try:
            # Validate intent parameter
            if not isinstance(intent, dict):
                return
            
            # Update tool usage history
            suggested_tools = intent.get('suggested_tools', [])
            for tool in suggested_tools:
                if isinstance(tool, dict):
                    tool_name = tool.get('tool', '')
                else:
                    tool_name = str(tool)
                
                if tool_name and tool_name not in st.session_state.chat_context['tool_usage_history']:
                    st.session_state.chat_context['tool_usage_history'].append(tool_name)
            
            # Update user preferences based on conversation
            content_types = intent.get('content_types', [])
            if content_types:
                if 'content_preferences' not in st.session_state.chat_context['user_preferences']:
                    st.session_state.chat_context['user_preferences']['content_preferences'] = []
                st.session_state.chat_context['user_preferences']['content_preferences'].extend(content_types)
            
            # Update conversation summary
            primary_intent = intent.get('primary_intent', 'general')
            summary_update = f"User interested in {primary_intent} related to {', '.join(content_types)}. "
            st.session_state.chat_context['conversation_summary'] += summary_update
            
            # Limit conversation summary length
            if len(st.session_state.chat_context['conversation_summary']) > 500:
                st.session_state.chat_context['conversation_summary'] = st.session_state.chat_context['conversation_summary'][-500:]
                
        except Exception as e:
            st.warning(f"Error updating conversation context: {str(e)}")
    
    def perform_real_time_analysis(self, url: str):
        """Perform real-time SEO analysis and add results to chat."""
        try:
            with st.spinner("🔍 Analyzing URL..."):
                # Basic SEO analysis
                seo_analysis = run_analysis(url)
                
                # Content gap analysis
                content_analysis = self.content_gap_analyzer.website_analyzer.analyze_website(url)
                
                # Format results
                analysis_message = f"""🔍 **Real-time Analysis: {url}**

**📊 SEO Overview:**
• Overall Score: {seo_analysis.get('overall_score', 'N/A')}/100
• Page Speed: {seo_analysis.get('page_speed', 'N/A')}
• Mobile Friendly: {'✅' if seo_analysis.get('mobile_friendly') else '❌'}

**🎯 Content Analysis:**
• Title: {content_analysis.get('analysis', {}).get('basic_info', {}).get('title', 'N/A')[:50]}...
• Word Count: {content_analysis.get('analysis', {}).get('content_metrics', {}).get('word_count', 'N/A')}
• Headings: {content_analysis.get('analysis', {}).get('content_metrics', {}).get('heading_count', 'N/A')}

**💡 Quick Recommendations:**
• {seo_analysis.get('recommendations', ['No specific recommendations available'])[0] if seo_analysis.get('recommendations') else 'Analysis complete'}

**⚡ Next Steps:**
• Run full Content Gap Analysis for detailed insights
• Use Technical SEO Crawler for comprehensive audit
• Generate optimized content based on findings"""
                
                st.session_state.enhanced_chat_messages.append({
                    "role": "assistant",
                    "content": analysis_message,
                    "avatar": AI_AVATAR_ICON
                })
                
                # Store analysis in workspace
                st.session_state.content_workspace["seo_insights"][url] = {
                    "timestamp": datetime.now().isoformat(),
                    "seo_analysis": seo_analysis,
                    "content_analysis": content_analysis
                }
                
                st.rerun()
                
        except Exception as e:
            st.error(f"Error analyzing URL: {str(e)}")
    
    def run(self):
        """Run the modular chatbot interface."""
        try:
            
            # Render sidebar and get actions if available
            if self.sidebar_manager:
                sidebar_data = self.sidebar_manager.render_sidebar()
                # Handle sidebar actions
                self._handle_sidebar_actions(sidebar_data)
            else:
                # Simple sidebar fallback
                st.sidebar.title("🚀 ALwrity Assistant")
                st.sidebar.info("Running in simplified mode")
                if not IMPORTS_SUCCESSFUL:
                    with st.sidebar.expander("⚠️ Import Issues"):
                        for error in IMPORT_ERRORS[:3]:  # Show first 3 errors
                            st.sidebar.text(f"• {error}")
            
            # Main chat interface
            self._render_main_interface()
            
            # Handle chat interactions
            self._handle_chat_interactions()
            
        except Exception as e:
            st.error(f"Application Error: {str(e)}")
            with st.expander("Error Details"):
                st.code(traceback.format_exc())
    
    def _handle_sidebar_actions(self, sidebar_data: Dict[str, Any]):
        """Handle actions from the sidebar."""
        if not sidebar_data:
            return
            
        # Handle quick actions
        quick_actions = sidebar_data.get("quick_actions", {})
        if "action" in quick_actions:
            action = quick_actions["action"]
            self._execute_quick_action(action)
        
        # Handle workflow actions
        workflow_actions = sidebar_data.get("workflow_actions", {})
        for action_type, action_value in workflow_actions.items():
            self._handle_workflow_action(action_type, action_value)
        
        # Handle preferences updates
        preferences_updated = sidebar_data.get("preferences_updated", {})
        if preferences_updated and self.context_manager:
            self.context_manager.update_user_preferences(preferences_updated)
            if self.sidebar_manager:
                self.sidebar_manager.show_notification("Preferences updated successfully!", "success")
        
        # Handle export actions
        export_actions = sidebar_data.get("export_actions", {})
        if export_actions:
            self._handle_export_actions(export_actions)
    
    def _execute_quick_action(self, action: str):
        """Execute a quick action from the sidebar."""
        action_map = {
            "blog_writer": "I want to write a blog post",
            "social_post": "I need to create a social media post",
            "email_writer": "Help me write an email",
            "story_writer": "I want to write a story",
            "technical_seo": "I need a technical SEO analysis",
            "content_gap": "I want to analyze content gaps",
            "keyword_research": "I need keyword research",
            "competitor_analysis": "I want competitor analysis",
            "website_analyzer": "I want to analyze a website",
            "onpage_seo": "I need on-page SEO analysis",
            "url_seo_check": "I want to check URL SEO",
            "social_analyzer": "I need social media analysis"
        }
        
        if action in action_map:
            # Add to chat history and trigger processing
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            user_message = action_map[action]
            st.session_state.messages.append({"role": "user", "content": user_message})
            
            # Process the message
            with st.spinner("Processing your request..."):
                response = self.process_message(user_message)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    def _handle_workflow_action(self, action_type: str, action_value: Any):
        """Handle workflow-related actions."""
        if not self.workflow_engine:
            st.warning("Workflow engine not available in current mode.")
            return
            
        if action_type == "start":
            workflow_name = action_value
            result = self.workflow_engine.start_workflow(workflow_name)
            if result.get("success"):
                if self.sidebar_manager:
                    self.sidebar_manager.show_notification(
                        f"Started workflow: {workflow_name}", "success"
                    )
                else:
                    st.success(f"Started workflow: {workflow_name}")
            else:
                if self.sidebar_manager:
                    self.sidebar_manager.show_notification(
                        f"Failed to start workflow: {result.get('error')}", "error"
                    )
                else:
                    st.error(f"Failed to start workflow: {result.get('error')}")
        
        elif action_type == "pause":
            workflow_id = action_value
            result = self.workflow_engine.pause_workflow(workflow_id)
            if result.get("success"):
                if self.sidebar_manager:
                    self.sidebar_manager.show_notification("Workflow paused", "info")
                else:
                    st.info("Workflow paused")
        
        elif action_type in ["continue", "resume"]:
            workflow_id = action_value
            result = self.workflow_engine.resume_workflow(workflow_id)
            if result.get("success"):
                if self.sidebar_manager:
                    self.sidebar_manager.show_notification("Workflow resumed", "success")
                else:
                    st.success("Workflow resumed")
    
    def _handle_export_actions(self, export_actions: Dict[str, Any]):
        """Handle data export and cleanup actions."""
        if not self.context_manager:
            st.warning("Export features not available in current mode.")
            return
            
        if "export" in export_actions:
            export_config = export_actions["export"]
            export_type = export_config["type"]
            export_format = export_config["format"]
            
            if export_type == "conversation_history":
                data = self.context_manager.export_conversation_history(export_format)
                self._download_data(data, f"conversation_history.{export_format}")
            
            elif export_type == "analytics":
                data = self.context_manager.export_analytics(export_format)
                self._download_data(data, f"analytics.{export_format}")
        
        elif "cleanup" in export_actions:
            days = export_actions["cleanup"]
            result = self.context_manager.cleanup_old_data(days)
            if result.get("success"):
                if self.sidebar_manager:
                    self.sidebar_manager.show_notification(
                        f"Cleaned up data older than {days} days", "success"
                    )
                else:
                    st.success(f"Cleaned up data older than {days} days")
        
        elif "reset" in export_actions and export_actions["reset"]:
            self.context_manager.reset_all_data()
            if self.sidebar_manager:
                self.sidebar_manager.show_notification("All data reset", "warning")
            else:
                st.warning("All data reset")
            st.rerun()
    
    def _download_data(self, data: str, filename: str):
        """Provide download button for exported data."""
        st.download_button(
            label=f"📥 Download {filename}",
            data=data,
            file_name=filename,
            mime="application/octet-stream"
        )
    
    def _render_main_interface(self):
        """Render the main chat interface."""
        # Header
        st.title("🚀 Enhanced ALwrity Assistant")
        st.markdown("*Your intelligent content creation and SEO analysis companion*")
        
        # Main content area
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Chat messages container
            self._render_chat_messages()
        
        with col2:
            # Context and suggestions panel
            self._render_context_panel()
    
    def _render_chat_messages(self):
        """Render the chat messages."""
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def _render_context_panel(self):
        """Render the context and suggestions panel."""
        with st.container():
            st.markdown("### 💡 Context & Suggestions")
            
            # Current context
            if self.context_manager and hasattr(self.context_manager, 'get_current_context'):
                current_context = self.context_manager.get_current_context()
                if current_context:
                    with st.expander("🧠 Current Context"):
                        st.text(current_context[:200] + "..." if len(current_context) > 200 else current_context)
            
            # Active workflows
            if self.context_manager:
                active_workflows = self.context_manager.get_active_workflows()
                if active_workflows:
                    st.markdown("**🔄 Active Workflows:**")
                    for workflow in active_workflows[:3]:
                        progress = workflow.current_step / workflow.total_steps
                        st.progress(progress, text=f"{workflow.workflow_name} ({workflow.current_step}/{workflow.total_steps})")
            
            # Quick suggestions
            st.markdown("**💡 Quick Suggestions:**")
            suggestions = [
                "Analyze this website's SEO",
                "Create a blog post outline",
                "Generate social media content",
                "Check technical SEO issues",
                "Research competitors"
            ]
            
            for suggestion in suggestions:
                if st.button(suggestion, key=f"suggestion_{suggestion.replace(' ', '_')}"):
                    # Add suggestion to chat
                    if "messages" not in st.session_state:
                        st.session_state.messages = []
                    
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    
                    # Process the suggestion
                    with st.spinner("Processing..."):
                        response = self.process_message(suggestion)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    st.rerun()
    
    def _handle_chat_interactions(self):
        """Handle chat input and interactions."""
        # Chat input
        if prompt := st.chat_input("Ask me anything about content creation, SEO, or writing..."):
            # Initialize messages if not exists
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.process_message(prompt)
                    st.markdown(response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Check for suggestions and update sidebar if available
            if self.intent_analyzer and self.sidebar_manager:
                intent_analysis = self.intent_analyzer.analyze_user_intent(prompt)
                
                # Render suggestions if available
                suggested_workflow = self.sidebar_manager.render_workflow_suggestions(intent_analysis)
                if suggested_workflow:
                    self._handle_workflow_action("start", suggested_workflow)
                
                suggested_tool = self.sidebar_manager.render_tool_suggestions(intent_analysis)
                if suggested_tool:
                    self._execute_quick_action(suggested_tool)

    def generate_simple_response(self, prompt: str) -> str:
        """Generate a simple response when advanced features are not available."""
        try:
            if llm_text_gen:
                system_prompt = """You are ALwrity AI, a helpful writing and content creation assistant. 
                You help users with writing, content creation, SEO, and digital marketing tasks.
                Provide clear, helpful, and actionable responses."""
                
                response = llm_text_gen(
                    prompt=prompt,
                    system_prompt=system_prompt
                )
                return response
            else:
                return ("I'm currently running in limited mode. While I can't access all my advanced features right now, "
                       "I'm still here to help! Please describe what you'd like to work on, and I'll do my best to assist you "
                       "with writing, content creation, or SEO guidance.")
        except Exception as e:
            return f"I'm having some technical difficulties right now. Error: {str(e)}. Please try again or contact support if the issue persists."

    def _create_fallback_intent(self, prompt: str) -> Dict[str, Any]:
        """Create a fallback intent structure when intent analysis fails."""
        prompt_lower = prompt.lower()
        
        # Simple keyword-based intent detection
        primary_intent = "general"
        if any(word in prompt_lower for word in ['write', 'create', 'generate', 'compose']):
            primary_intent = "write"
        elif any(word in prompt_lower for word in ['analyze', 'check', 'review', 'examine']):
            primary_intent = "analyze"
        elif any(word in prompt_lower for word in ['seo', 'optimize', 'rank', 'search']):
            primary_intent = "seo"
        elif any(word in prompt_lower for word in ['social', 'facebook', 'twitter', 'linkedin']):
            primary_intent = "social"
        elif any(word in prompt_lower for word in ['plan', 'strategy', 'calendar']):
            primary_intent = "plan"
        
        return {
            "primary_intent": primary_intent,
            "all_intents": [primary_intent],
            "sub_intents": [],
            "content_types": [],
            "confidence_scores": {primary_intent: 0.5},
            "urgency": {"level": "normal", "score": 0.5, "is_urgent": False},
            "complexity": {"level": "medium", "score": 0.5, "word_count": len(prompt.split())},
            "suggested_workflows": [],
            "suggested_tools": [],
            "intent_strength": "moderate",
            "multi_intent": False,
            "context_enhanced": False
        }
    
    def _get_default_intent_value(self, key: str) -> Any:
        """Get default value for missing intent keys."""
        defaults = {
            "primary_intent": "general",
            "all_intents": ["general"],
            "sub_intents": [],
            "content_types": [],
            "confidence_scores": {"general": 0.5},
            "urgency": {"level": "normal", "score": 0.5, "is_urgent": False},
            "complexity": {"level": "medium", "score": 0.5, "word_count": 0},
            "suggested_workflows": [],
            "suggested_tools": [],
            "intent_strength": "moderate",
            "multi_intent": False,
            "context_enhanced": False
        }
        return defaults.get(key, None)


def run_enhanced_chatbot():
    """
    Main entry point for the enhanced ALwrity chatbot.
    This function is called from the UI setup module.
    """
    # Show import warnings if any
    if not IMPORTS_SUCCESSFUL and IMPORT_ERRORS:
        with st.expander("⚠️ Import Warnings", expanded=False):
            st.warning("Some features may not be available due to import issues:")
            for error in IMPORT_ERRORS:
                st.text(f"• {error}")
            st.info("The chatbot will run in limited mode with available features.")
    
    try:
        # Initialize and run the chatbot
        chatbot = EnhancedALwrityChatbot()
        chatbot.run()
    except Exception as e:
        st.error(f"Failed to initialize Enhanced ALwrity Chatbot: {str(e)}")
        st.error("Please check your configuration and try again.")
        with st.expander("🔍 Error Details"):
            st.code(traceback.format_exc())
        
        # Provide fallback simple chatbot interface
        st.markdown("---")
        st.markdown("### 🔧 Fallback Mode")
        st.info("Running in simplified mode due to initialization issues.")
        
        # Simple chat interface as fallback
        if "fallback_messages" not in st.session_state:
            st.session_state.fallback_messages = [
                {
                    "role": "assistant",
                    "content": "Hello! I'm running in simplified mode. I can still help with basic text generation and writing tasks."
                }
            ]
        
        # Display messages
        for message in st.session_state.fallback_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("How can I help you today?"):
            # Add user message
            st.session_state.fallback_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response using basic text generation
            with st.chat_message("assistant"):
                try:
                    if llm_text_gen:
                        with st.spinner("Generating response..."):
                            response = llm_text_gen(
                                prompt=prompt,
                                system_prompt="You are ALwrity AI, a helpful writing assistant. Provide clear, helpful responses about writing, content creation, and SEO."
                            )
                            st.markdown(response)
                            st.session_state.fallback_messages.append({"role": "assistant", "content": response})
                    else:
                        error_response = "I'm currently unable to generate responses. Please check the system configuration."
                        st.markdown(error_response)
                        st.session_state.fallback_messages.append({"role": "assistant", "content": error_response})
                except Exception as gen_error:
                    error_response = f"I apologize, but I'm having trouble generating a response right now. Error: {str(gen_error)}"
                    st.markdown(error_response)
                    st.session_state.fallback_messages.append({"role": "assistant", "content": error_response})


def main():
    """Main function to run the modular chatbot."""
    run_enhanced_chatbot()


if __name__ == "__main__":
    main() 