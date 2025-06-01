"""
Enhanced ALwrity Chatbot - Comprehensive Content Creation Assistant

This module provides an advanced chatbot interface that integrates all ALwrity features
including AI writers, SEO tools, content planning, and document analysis.
"""

import time
import os
import json
import joblib
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, List, Any, Optional
import tempfile
import requests
from urllib.parse import urlparse
import pandas as pd

# Import ALwrity components
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen
from ..ai_writers.ai_writer_dashboard import list_ai_writers
from ..ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
from ..database.models import ContentItem
from ..ai_seo_tools.content_calendar.ui.components.content_repurposing_ui import ContentRepurposingUI
from ..utils.alwrity_utils import essay_writer, ai_news_writer, ai_finance_ta_writer
from ..ai_writers.ai_blog_writer.ai_blog_generator import ai_blog_writer_page
from ..ai_writers.ai_story_writer.story_writer import story_input_section
from ..ai_writers.ai_product_description_writer import write_ai_prod_desc
from ..ai_writers.linkedin_writer import LinkedInAIWriter
from ..ai_writers.ai_facebook_writer.facebook_ai_writer import FacebookAIWriter
from ..ai_writers.youtube_writers.youtube_ai_writer import youtube_main_menu

# Load environment variables
load_dotenv()

# Constants
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '🤖'
USER_AVATAR_ICON = '👤'
DATA_DIR = 'data/chatbot/'

class EnhancedALwrityChatbot:
    """Enhanced ALwrity Chatbot with comprehensive content creation capabilities."""
    
    def __init__(self):
        """Initialize the enhanced chatbot."""
        self.initialize_session_state()
        self.setup_ai_model()
        self.load_ai_writers()
        
    def initialize_session_state(self):
        """Initialize session state variables."""
        if "enhanced_chat_messages" not in st.session_state:
            st.session_state.enhanced_chat_messages = [
                {
                    "role": "assistant", 
                    "content": "👋 Welcome to ALwrity! I'm your AI content creation assistant. I can help you with:\n\n"
                              "📝 **Content Writing**: Blog posts, articles, stories, essays\n"
                              "📱 **Social Media**: LinkedIn, Facebook, YouTube content\n"
                              "🔍 **SEO Analysis**: Competitor research, keyword analysis\n"
                              "📊 **Content Planning**: Calendar creation, repurposing\n"
                              "📄 **Document Analysis**: Upload files for insights\n\n"
                              "What would you like to create today?",
                    "avatar": AI_AVATAR_ICON
                }
            ]
        
        if "chat_context" not in st.session_state:
            st.session_state.chat_context = {
                "current_task": None,
                "user_preferences": {},
                "uploaded_files": [],
                "content_history": []
            }
            
        if "content_workspace" not in st.session_state:
            st.session_state.content_workspace = {
                "drafts": [],
                "templates": [],
                "research_data": {}
            }
    
    def setup_ai_model(self):
        """Setup the AI model for conversation."""
        try:
            st.session_state.enhanced_model = genai.GenerativeModel('gemini-pro')
            st.session_state.enhanced_chat = st.session_state.enhanced_model.start_chat(history=[])
        except Exception as e:
            st.error(f"Error setting up AI model: {str(e)}")
    
    def load_ai_writers(self):
        """Load available AI writers."""
        self.ai_writers = list_ai_writers()
        self.writer_functions = {
            writer['name']: writer['function'] for writer in self.ai_writers
        }
    
    def render_chatbot_ui(self):
        """Render the main chatbot interface."""
        st.title("🤖 ALwrity Assistant")
        
        # Sidebar with features and tools
        self.render_sidebar()
        
        # Main chat interface
        self.render_chat_interface()
        
        # File upload area
        self.render_file_upload()
        
        # Quick actions
        self.render_quick_actions()
    
    def render_sidebar(self):
        """Render the sidebar with available features."""
        with st.sidebar:
            st.header("🛠️ ALwrity Tools")
            
            # Content Writers
            with st.expander("📝 AI Writers", expanded=False):
                for writer in self.ai_writers:
                    if st.button(f"{writer['icon']} {writer['name']}", key=f"writer_{writer['name']}"):
                        self.suggest_writer_usage(writer)
            
            # SEO Tools
            with st.expander("🔍 SEO Tools", expanded=False):
                if st.button("🔍 Competitor Analysis"):
                    self.suggest_competitor_analysis()
                if st.button("📊 Content Gap Analysis"):
                    self.suggest_content_gap_analysis()
                if st.button("🎯 Keyword Research"):
                    self.suggest_keyword_research()
            
            # Content Planning
            with st.expander("📅 Content Planning", expanded=False):
                if st.button("📅 Content Calendar"):
                    self.suggest_content_calendar()
                if st.button("🔄 Content Repurposing"):
                    self.suggest_content_repurposing()
                if st.button("📈 Content Strategy"):
                    self.suggest_content_strategy()
            
            # Quick Templates
            with st.expander("📋 Quick Templates", expanded=False):
                templates = [
                    "Blog Post Outline",
                    "Social Media Campaign",
                    "Email Newsletter",
                    "Product Description",
                    "Press Release"
                ]
                for template in templates:
                    if st.button(template, key=f"template_{template}"):
                        self.suggest_template_usage(template)
            
            # Chat History
            with st.expander("💬 Chat History", expanded=False):
                if st.button("🗑️ Clear Chat"):
                    self.clear_chat_history()
                if st.button("💾 Save Chat"):
                    self.save_chat_history()
    
    def render_chat_interface(self):
        """Render the main chat interface."""
        # Display chat messages
        for message in st.session_state.enhanced_chat_messages:
            with st.chat_message(message["role"], avatar=message.get("avatar")):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about content creation..."):
            self.handle_user_input(prompt)
    
    def render_file_upload(self):
        """Render file upload interface."""
        with st.expander("📁 Upload Files for Analysis", expanded=False):
            uploaded_files = st.file_uploader(
                "Upload documents, images, or URLs",
                type=['txt', 'pdf', 'docx', 'csv', 'xlsx', 'jpg', 'png', 'gif'],
                accept_multiple_files=True,
                help="Upload files to analyze content, extract insights, or use as reference material"
            )
            
            if uploaded_files:
                self.process_uploaded_files(uploaded_files)
            
            # URL input
            url_input = st.text_input("Or enter a URL to analyze:")
            if url_input and st.button("Analyze URL"):
                self.process_url(url_input)
    
    def render_quick_actions(self):
        """Render quick action buttons."""
        st.subheader("⚡ Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📝 Write Blog Post"):
                self.quick_blog_post()
        
        with col2:
            if st.button("📱 Social Media Post"):
                self.quick_social_media()
        
        with col3:
            if st.button("🔍 SEO Analysis"):
                self.quick_seo_analysis()
        
        with col4:
            if st.button("📊 Content Ideas"):
                self.quick_content_ideas()
    
    def handle_user_input(self, prompt: str):
        """Handle user input and generate appropriate response."""
        # Add user message to chat
        st.session_state.enhanced_chat_messages.append({
            "role": "user",
            "content": prompt,
            "avatar": USER_AVATAR_ICON
        })
        
        # Analyze user intent
        intent = self.analyze_user_intent(prompt)
        
        # Generate response based on intent
        response = self.generate_contextual_response(prompt, intent)
        
        # Add assistant response to chat
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": response,
            "avatar": AI_AVATAR_ICON
        })
        
        st.rerun()
    
    def analyze_user_intent(self, prompt: str) -> Dict[str, Any]:
        """Analyze user intent from the prompt."""
        intent_keywords = {
            "write": ["write", "create", "generate", "compose", "draft"],
            "analyze": ["analyze", "review", "check", "examine", "evaluate"],
            "seo": ["seo", "optimize", "rank", "keyword", "search"],
            "social": ["social", "facebook", "twitter", "linkedin", "instagram"],
            "blog": ["blog", "article", "post", "content"],
            "help": ["help", "how", "what", "explain", "guide"],
            "research": ["research", "competitor", "market", "trend"],
            "plan": ["plan", "strategy", "calendar", "schedule"]
        }
        
        prompt_lower = prompt.lower()
        detected_intents = []
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                detected_intents.append(intent)
        
        return {
            "primary_intent": detected_intents[0] if detected_intents else "general",
            "all_intents": detected_intents,
            "confidence": len(detected_intents) / len(intent_keywords)
        }
    
    def generate_contextual_response(self, prompt: str, intent: Dict[str, Any]) -> str:
        """Generate a contextual response based on user intent."""
        try:
            # Build context from chat history and user preferences
            context = self.build_conversation_context()
            
            # Create system prompt based on intent
            system_prompt = self.create_system_prompt(intent)
            
            # Generate response using AI
            ai_prompt = f"""
            Context: {context}
            User Intent: {intent['primary_intent']}
            User Message: {prompt}
            
            Provide a helpful, actionable response that:
            1. Addresses the user's specific need
            2. Suggests relevant ALwrity tools if applicable
            3. Offers step-by-step guidance
            4. Includes examples when helpful
            5. Maintains a friendly, professional tone
            
            Available ALwrity Features:
            - AI Writers: {[w['name'] for w in self.ai_writers]}
            - SEO Tools: Competitor Analysis, Content Gap Analysis, Keyword Research
            - Content Planning: Calendar, Repurposing, Strategy
            - Document Analysis: File upload and URL analysis
            """
            
            response = llm_text_gen(
                prompt=ai_prompt,
                system_prompt=system_prompt
            )
            
            # Add action buttons if relevant
            if intent['primary_intent'] in ['write', 'create']:
                response += self.add_writer_suggestions(prompt)
            elif intent['primary_intent'] in ['analyze', 'seo']:
                response += self.add_analysis_suggestions(prompt)
            elif intent['primary_intent'] in ['plan', 'strategy']:
                response += self.add_planning_suggestions(prompt)
            
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error processing your request: {str(e)}. Please try rephrasing your question or use the quick actions below."
    
    def create_system_prompt(self, intent: Dict[str, Any]) -> str:
        """Create a system prompt based on user intent."""
        base_prompt = """You are ALwrity, an expert AI content creation assistant. You help users create high-quality content, optimize for SEO, and develop content strategies."""
        
        intent_prompts = {
            "write": "Focus on content creation guidance, writing tips, and suggesting appropriate AI writers.",
            "analyze": "Focus on content analysis, SEO evaluation, and providing actionable insights.",
            "seo": "Focus on SEO optimization, keyword research, and search engine best practices.",
            "social": "Focus on social media content creation and platform-specific optimization.",
            "research": "Focus on competitor analysis, market research, and content gap identification.",
            "plan": "Focus on content strategy, planning, and calendar management.",
            "help": "Focus on explaining features, providing tutorials, and guiding users."
        }
        
        specific_prompt = intent_prompts.get(intent['primary_intent'], "Provide helpful, comprehensive assistance.")
        
        return f"{base_prompt} {specific_prompt}"
    
    def build_conversation_context(self) -> str:
        """Build context from conversation history."""
        recent_messages = st.session_state.enhanced_chat_messages[-5:]  # Last 5 messages
        context_parts = []
        
        for msg in recent_messages:
            if msg['role'] == 'user':
                context_parts.append(f"User asked: {msg['content']}")
            else:
                context_parts.append(f"Assistant responded about: {msg['content'][:100]}...")
        
        return " | ".join(context_parts)
    
    def add_writer_suggestions(self, prompt: str) -> str:
        """Add writer suggestions based on the prompt."""
        suggestions = "\n\n**💡 Suggested ALwrity Tools:**\n"
        
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['blog', 'article', 'post']):
            suggestions += "- 📝 AI Blog Writer - Create comprehensive blog posts\n"
        
        if any(word in prompt_lower for word in ['story', 'narrative', 'fiction']):
            suggestions += "- 📚 Story Writer - Create engaging stories\n"
        
        if any(word in prompt_lower for word in ['linkedin', 'professional']):
            suggestions += "- 💼 LinkedIn AI Writer - Professional content\n"
        
        if any(word in prompt_lower for word in ['facebook', 'social']):
            suggestions += "- 📘 Facebook AI Writer - Social media content\n"
        
        if any(word in prompt_lower for word in ['product', 'description', 'ecommerce']):
            suggestions += "- 🛍️ Product Description Writer - Sales copy\n"
        
        return suggestions
    
    def add_analysis_suggestions(self, prompt: str) -> str:
        """Add analysis tool suggestions."""
        suggestions = "\n\n**🔍 Suggested Analysis Tools:**\n"
        suggestions += "- 🔍 Competitor Analysis - Analyze competitor content\n"
        suggestions += "- 📊 Content Gap Analysis - Find content opportunities\n"
        suggestions += "- 🎯 Keyword Research - Discover target keywords\n"
        
        return suggestions
    
    def add_planning_suggestions(self, prompt: str) -> str:
        """Add planning tool suggestions."""
        suggestions = "\n\n**📅 Suggested Planning Tools:**\n"
        suggestions += "- 📅 Content Calendar - Plan your content schedule\n"
        suggestions += "- 🔄 Content Repurposing - Maximize content value\n"
        suggestions += "- 📈 Content Strategy - Develop comprehensive plans\n"
        
        return suggestions
    
    def process_uploaded_files(self, uploaded_files):
        """Process uploaded files for analysis."""
        for file in uploaded_files:
            try:
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(file.getvalue())
                    tmp_path = tmp_file.name
                
                # Analyze file based on type
                file_analysis = self.analyze_file(tmp_path, file.name, file.type)
                
                # Add to chat
                analysis_message = f"📁 **File Analysis: {file.name}**\n\n{file_analysis}"
                st.session_state.enhanced_chat_messages.append({
                    "role": "assistant",
                    "content": analysis_message,
                    "avatar": AI_AVATAR_ICON
                })
                
                # Store in context
                st.session_state.chat_context["uploaded_files"].append({
                    "name": file.name,
                    "type": file.type,
                    "analysis": file_analysis
                })
                
                # Clean up
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"Error processing file {file.name}: {str(e)}")
    
    def analyze_file(self, file_path: str, file_name: str, file_type: str) -> str:
        """Analyze uploaded file content."""
        try:
            if file_type.startswith('text/') or file_name.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return self.analyze_text_content(content)
            
            elif file_type == 'application/pdf':
                # PDF analysis would require additional libraries
                return "PDF file uploaded. Content analysis available with additional setup."
            
            elif file_type.startswith('image/'):
                return "Image file uploaded. Visual content analysis available with additional setup."
            
            else:
                return f"File type {file_type} uploaded. Specialized analysis may be available."
                
        except Exception as e:
            return f"Error analyzing file: {str(e)}"
    
    def analyze_text_content(self, content: str) -> str:
        """Analyze text content using AI."""
        try:
            prompt = f"""
            Analyze the following text content and provide insights:
            
            Content: {content[:2000]}...
            
            Provide:
            1. Content summary
            2. Key topics and themes
            3. Writing style and tone
            4. Potential improvements
            5. Content repurposing suggestions
            """
            
            analysis = llm_text_gen(
                prompt=prompt,
                system_prompt="You are a content analysis expert. Provide detailed, actionable insights."
            )
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing content: {str(e)}"
    
    def process_url(self, url: str):
        """Process and analyze a URL."""
        try:
            # Basic URL validation
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                st.error("Please enter a valid URL (including http:// or https://)")
                return
            
            # Analyze URL using content gap analysis
            analyzer = ContentGapAnalysis()
            analysis = analyzer.website_analyzer.analyze_website(url)
            
            if analysis.get('success', False):
                analysis_message = f"🔗 **URL Analysis: {url}**\n\n"
                analysis_message += self.format_url_analysis(analysis['data'])
                
                st.session_state.enhanced_chat_messages.append({
                    "role": "assistant",
                    "content": analysis_message,
                    "avatar": AI_AVATAR_ICON
                })
            else:
                st.error(f"Error analyzing URL: {analysis.get('error', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"Error processing URL: {str(e)}")
    
    def format_url_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Format URL analysis data for display."""
        try:
            basic_info = analysis_data.get('analysis', {}).get('basic_info', {})
            seo_info = analysis_data.get('analysis', {}).get('seo_info', {})
            
            formatted = f"""
            **📊 Website Overview:**
            - Title: {basic_info.get('title', 'N/A')}
            - Description: {basic_info.get('meta_description', 'N/A')[:100]}...
            
            **🔍 SEO Analysis:**
            - Overall Score: {seo_info.get('overall_score', 'N/A')}
            - Meta Tags Status: {seo_info.get('meta_tags', {}).get('status', 'N/A')}
            
            **💡 Recommendations:**
            """
            
            recommendations = seo_info.get('recommendations', [])
            for i, rec in enumerate(recommendations[:3], 1):
                formatted += f"{i}. {rec}\n"
            
            return formatted
            
        except Exception as e:
            return f"Error formatting analysis: {str(e)}"
    
    def suggest_writer_usage(self, writer: Dict[str, Any]):
        """Suggest how to use a specific writer."""
        suggestion = f"💡 **{writer['name']}** - {writer['description']}\n\n"
        suggestion += "Would you like me to help you get started with this tool? Just tell me what you'd like to create!"
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def suggest_competitor_analysis(self):
        """Suggest competitor analysis usage."""
        suggestion = """🔍 **Competitor Analysis**
        
        I can help you analyze your competitors' content strategies. Here's what I can do:
        
        1. **Content Analysis** - Analyze competitor websites and content
        2. **SEO Comparison** - Compare SEO metrics and strategies
        3. **Content Gaps** - Identify opportunities in your market
        4. **Market Position** - Understand your competitive landscape
        
        To get started, please provide:
        - Your website URL (optional)
        - Competitor URLs (1-5 competitors)
        - Your industry or niche
        
        Example: "Analyze competitors for my fitness blog: competitor1.com, competitor2.com"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def quick_blog_post(self):
        """Quick blog post creation."""
        suggestion = """📝 **Quick Blog Post Creation**
        
        I'll help you create a blog post! Please provide:
        
        1. **Topic or Keywords** - What should the blog post be about?
        2. **Target Audience** - Who are you writing for?
        3. **Tone** - Professional, casual, technical, etc.
        4. **Length** - Short (500-800 words), Medium (800-1500 words), Long (1500+ words)
        
        Example: "Write a professional blog post about 'sustainable marketing practices' for business owners, medium length"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def quick_social_media(self):
        """Quick social media content creation."""
        suggestion = """📱 **Social Media Content Creation**
        
        I can create content for various platforms:
        
        **Platforms Available:**
        - 💼 LinkedIn (Professional posts, articles)
        - 📘 Facebook (Posts, ads, events)
        - 🎥 YouTube (Titles, descriptions, scripts)
        - 📸 Instagram (Captions, hashtags)
        
        **What I need:**
        1. Platform choice
        2. Content topic or message
        3. Target audience
        4. Call-to-action (if any)
        
        Example: "Create a LinkedIn post about AI in marketing for business professionals"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def quick_seo_analysis(self):
        """Quick SEO analysis."""
        suggestion = """🔍 **SEO Analysis**
        
        I can perform various SEO analyses:
        
        **Available Analyses:**
        1. **Website SEO Audit** - Comprehensive site analysis
        2. **Competitor SEO Analysis** - Compare with competitors
        3. **Keyword Research** - Find target keywords
        4. **Content Gap Analysis** - Identify content opportunities
        
        **To get started:**
        - Provide your website URL
        - Specify the type of analysis you want
        - Include competitor URLs (for competitive analysis)
        
        Example: "Analyze SEO for mywebsite.com and compare with competitor1.com"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def quick_content_ideas(self):
        """Generate quick content ideas."""
        suggestion = """📊 **Content Ideas Generator**
        
        I can help you brainstorm content ideas! Tell me:
        
        1. **Your Industry/Niche** - What field are you in?
        2. **Content Type** - Blog posts, social media, videos, etc.
        3. **Target Audience** - Who are you creating for?
        4. **Goals** - Education, entertainment, sales, etc.
        5. **Current Trends** - Any specific trends to focus on?
        
        I'll generate:
        - 10-20 content ideas
        - Content calendar suggestions
        - Platform-specific recommendations
        - SEO-optimized topics
        
        Example: "Generate content ideas for a digital marketing agency targeting small businesses"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def clear_chat_history(self):
        """Clear chat history."""
        st.session_state.enhanced_chat_messages = [
            {
                "role": "assistant",
                "content": "Chat history cleared! How can I help you today?",
                "avatar": AI_AVATAR_ICON
            }
        ]
        st.session_state.chat_context = {
            "current_task": None,
            "user_preferences": {},
            "uploaded_files": [],
            "content_history": []
        }
        st.rerun()
    
    def save_chat_history(self):
        """Save chat history."""
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            timestamp = int(time.time())
            filename = f"chat_history_{timestamp}.json"
            filepath = os.path.join(DATA_DIR, filename)
            
            chat_data = {
                "timestamp": timestamp,
                "messages": st.session_state.enhanced_chat_messages,
                "context": st.session_state.chat_context
            }
            
            with open(filepath, 'w') as f:
                json.dump(chat_data, f, indent=2)
            
            st.success(f"Chat history saved as {filename}")
            
        except Exception as e:
            st.error(f"Error saving chat history: {str(e)}")
    
    def suggest_content_gap_analysis(self):
        """Suggest content gap analysis usage."""
        suggestion = """📊 **Content Gap Analysis**
        
        I can help you identify content opportunities by analyzing gaps in your content strategy:
        
        **What I can analyze:**
        1. **Missing Topics** - Topics your competitors cover but you don't
        2. **Content Depth** - Areas where you need more comprehensive content
        3. **Keyword Gaps** - Keywords you're missing opportunities for
        4. **Format Gaps** - Content types you should consider
        
        **To get started, provide:**
        - Your website URL
        - 2-5 competitor URLs
        - Your target industry/niche
        - Specific topics you're interested in (optional)
        
        Example: "Analyze content gaps for mysite.com vs competitor1.com, competitor2.com in digital marketing"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def suggest_keyword_research(self):
        """Suggest keyword research usage."""
        suggestion = """🎯 **Keyword Research**
        
        I can help you discover valuable keywords for your content strategy:
        
        **Research Types:**
        1. **Seed Keywords** - Find related keywords from your main topics
        2. **Long-tail Keywords** - Discover specific, less competitive phrases
        3. **Competitor Keywords** - See what keywords competitors rank for
        4. **Content Keywords** - Keywords for specific content pieces
        
        **What I need:**
        - Your main topic or industry
        - Target audience description
        - Geographic location (if local business)
        - Content type you're planning
        
        Example: "Research keywords for 'sustainable fashion' targeting eco-conscious millennials"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def suggest_content_calendar(self):
        """Suggest content calendar usage."""
        suggestion = """📅 **Content Calendar Planning**
        
        I can help you create a strategic content calendar:
        
        **Calendar Features:**
        1. **Content Scheduling** - Plan posts across multiple platforms
        2. **Topic Planning** - Organize themes and campaigns
        3. **Content Mix** - Balance different content types
        4. **Seasonal Planning** - Align with holidays and events
        
        **To create your calendar:**
        - Specify time period (weekly, monthly, quarterly)
        - List your content platforms
        - Define your content goals
        - Share your target audience
        - Mention any upcoming events or campaigns
        
        Example: "Create a monthly content calendar for a fitness brand on Instagram, Facebook, and blog"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def suggest_content_repurposing(self):
        """Suggest content repurposing usage."""
        suggestion = """🔄 **Content Repurposing**
        
        I can help you maximize your content's reach by repurposing it across platforms:
        
        **Repurposing Options:**
        1. **Blog to Social** - Turn blog posts into social media content
        2. **Long-form to Short-form** - Create snippets and highlights
        3. **Cross-platform Adaptation** - Optimize for different platforms
        4. **Format Transformation** - Convert text to infographics, videos, etc.
        
        **What I can do:**
        - Analyze existing content for repurposing opportunities
        - Create platform-specific versions
        - Suggest content series from single pieces
        - Generate social media campaigns from blog posts
        
        Example: "Repurpose my blog post about 'remote work productivity' for LinkedIn, Twitter, and Instagram"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def suggest_content_strategy(self):
        """Suggest content strategy usage."""
        suggestion = """📈 **Content Strategy Development**
        
        I can help you develop a comprehensive content strategy:
        
        **Strategy Components:**
        1. **Audience Analysis** - Define and understand your target audience
        2. **Content Pillars** - Establish core themes and topics
        3. **Platform Strategy** - Choose the right channels for your content
        4. **Content Mix** - Balance educational, promotional, and entertaining content
        5. **Performance Metrics** - Define success metrics and KPIs
        
        **To develop your strategy:**
        - Describe your business/brand
        - Define your target audience
        - Share your business goals
        - List your current content challenges
        - Specify your available resources
        
        Example: "Develop a content strategy for a B2B SaaS company targeting marketing managers"
        """
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()
    
    def suggest_template_usage(self, template: str):
        """Suggest how to use a specific template."""
        template_guides = {
            "Blog Post Outline": """📋 **Blog Post Outline Template**
            
            I'll help you create a structured blog post outline:
            
            **What I'll include:**
            - Compelling headline options
            - Introduction hook
            - Main sections with subheadings
            - Key points for each section
            - Conclusion and call-to-action
            - SEO recommendations
            
            **Just tell me:**
            - Your blog post topic
            - Target audience
            - Desired word count
            - Key points you want to cover
            
            Example: "Create a blog post outline about 'email marketing best practices' for small business owners"
            """,
            
            "Social Media Campaign": """📱 **Social Media Campaign Template**
            
            I'll help you plan a complete social media campaign:
            
            **Campaign Elements:**
            - Campaign objectives and goals
            - Target audience definition
            - Content calendar (posts, stories, etc.)
            - Platform-specific content
            - Hashtag strategy
            - Engagement tactics
            - Performance metrics
            
            **Provide details about:**
            - Campaign goal (awareness, sales, engagement)
            - Target platforms
            - Campaign duration
            - Product/service to promote
            - Budget considerations
            
            Example: "Create a social media campaign to launch a new fitness app targeting young professionals"
            """,
            
            "Email Newsletter": """📧 **Email Newsletter Template**
            
            I'll help you create an engaging email newsletter:
            
            **Newsletter Structure:**
            - Compelling subject line
            - Personal greeting
            - Main content sections
            - Featured articles/products
            - Call-to-action buttons
            - Footer with social links
            
            **Tell me about:**
            - Newsletter purpose (updates, promotions, education)
            - Your audience
            - Key content to include
            - Desired tone and style
            - Frequency of sending
            
            Example: "Create a monthly newsletter for a digital marketing agency showcasing case studies and tips"
            """,
            
            "Product Description": """🛍️ **Product Description Template**
            
            I'll help you write compelling product descriptions:
            
            **Description Elements:**
            - Attention-grabbing headline
            - Key features and benefits
            - Problem-solution positioning
            - Technical specifications
            - Social proof elements
            - Clear call-to-action
            
            **Product details needed:**
            - Product name and category
            - Key features and benefits
            - Target customer
            - Unique selling points
            - Price point (if relevant)
            
            Example: "Write a product description for wireless noise-canceling headphones targeting remote workers"
            """,
            
            "Press Release": """📰 **Press Release Template**
            
            I'll help you write a professional press release:
            
            **Press Release Structure:**
            - Newsworthy headline
            - Dateline and location
            - Lead paragraph (who, what, when, where, why)
            - Supporting paragraphs with details
            - Company boilerplate
            - Contact information
            
            **Information needed:**
            - News announcement details
            - Company information
            - Key quotes from executives
            - Supporting data/statistics
            - Target media outlets
            
            Example: "Write a press release announcing our company's Series A funding round of $5M"
            """
        }
        
        suggestion = template_guides.get(template, f"I'll help you create a {template}. Please provide more details about what you need.")
        
        st.session_state.enhanced_chat_messages.append({
            "role": "assistant",
            "content": suggestion,
            "avatar": AI_AVATAR_ICON
        })
        st.rerun()

def run_enhanced_chatbot():
    """Main function to run the enhanced chatbot."""
    try:
        # Initialize chatbot
        chatbot = EnhancedALwrityChatbot()
        
        # Render UI
        chatbot.render_chatbot_ui()
        
    except Exception as e:
        st.error(f"Error running enhanced chatbot: {str(e)}")
        st.info("Please check your configuration and try again.")

if __name__ == "__main__":
    run_enhanced_chatbot() 