"""
Workflow Engine for Enhanced ALwrity Chatbot.

Handles multi-tool workflows and automation for complex content creation tasks.
"""

from typing import Dict, List, Any


class WorkflowEngine:
    """Handles multi-tool workflows and automation."""
    
    def __init__(self):
        self.workflows = {
            "blog_creation_workflow": {
                "name": "Complete Blog Creation",
                "description": "From idea to published blog post",
                "steps": [
                    {"tool": "keyword_research", "name": "Keyword Research"},
                    {"tool": "content_gap_analysis", "name": "Content Gap Analysis"},
                    {"tool": "blog_writing", "name": "Blog Writing"},
                    {"tool": "seo_optimization", "name": "SEO Optimization"},
                    {"tool": "meta_generation", "name": "Meta Tags Generation"}
                ]
            },
            "competitor_analysis_workflow": {
                "name": "Competitor Content Strategy",
                "description": "Analyze competitors and create content plan",
                "steps": [
                    {"tool": "competitor_analysis", "name": "Competitor Analysis"},
                    {"tool": "content_gap_analysis", "name": "Content Gap Analysis"},
                    {"tool": "content_calendar", "name": "Content Calendar Creation"},
                    {"tool": "content_ideas", "name": "Content Ideas Generation"}
                ]
            },
            "social_media_workflow": {
                "name": "Social Media Campaign",
                "description": "Create comprehensive social media content",
                "steps": [
                    {"tool": "audience_analysis", "name": "Audience Analysis"},
                    {"tool": "content_planning", "name": "Content Planning"},
                    {"tool": "social_content_creation", "name": "Social Content Creation"},
                    {"tool": "hashtag_research", "name": "Hashtag Research"}
                ]
            },
            "seo_audit_workflow": {
                "name": "Complete SEO Audit",
                "description": "Comprehensive website SEO analysis and optimization",
                "steps": [
                    {"tool": "technical_seo", "name": "Technical SEO Analysis"},
                    {"tool": "on_page_seo", "name": "On-Page SEO Review"},
                    {"tool": "content_gap_analysis", "name": "Content Gap Analysis"},
                    {"tool": "competitor_seo", "name": "Competitor SEO Analysis"},
                    {"tool": "optimization_plan", "name": "SEO Optimization Plan"}
                ]
            },
            "content_strategy_workflow": {
                "name": "Content Strategy Development",
                "description": "Develop comprehensive content strategy from research to execution",
                "steps": [
                    {"tool": "market_research", "name": "Market Research"},
                    {"tool": "audience_analysis", "name": "Audience Analysis"},
                    {"tool": "competitor_analysis", "name": "Competitor Analysis"},
                    {"tool": "content_pillars", "name": "Content Pillars Definition"},
                    {"tool": "content_calendar", "name": "Content Calendar Creation"}
                ]
            }
        }
    
    def suggest_workflows(self, user_intent: str) -> List[Dict[str, Any]]:
        """Suggest relevant workflows based on user intent."""
        relevant_workflows = []
        user_intent_lower = user_intent.lower()
        
        # Blog and content creation
        if any(word in user_intent_lower for word in ['blog', 'article', 'post', 'write', 'content']):
            relevant_workflows.append(self.workflows["blog_creation_workflow"])
        
        # Competitor and market analysis
        if any(word in user_intent_lower for word in ['competitor', 'analysis', 'research', 'market']):
            relevant_workflows.append(self.workflows["competitor_analysis_workflow"])
        
        # Social media
        if any(word in user_intent_lower for word in ['social', 'facebook', 'linkedin', 'campaign', 'instagram', 'twitter']):
            relevant_workflows.append(self.workflows["social_media_workflow"])
        
        # SEO related
        if any(word in user_intent_lower for word in ['seo', 'optimize', 'rank', 'search', 'audit']):
            relevant_workflows.append(self.workflows["seo_audit_workflow"])
        
        # Strategy and planning
        if any(word in user_intent_lower for word in ['strategy', 'plan', 'roadmap', 'framework']):
            relevant_workflows.append(self.workflows["content_strategy_workflow"])
        
        return relevant_workflows
    
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get a specific workflow by ID."""
        return self.workflows.get(workflow_id)
    
    def get_all_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Get all available workflows."""
        return self.workflows
    
    def create_custom_workflow(self, name: str, description: str, steps: List[Dict[str, str]]) -> str:
        """Create a custom workflow."""
        workflow_id = f"custom_{name.lower().replace(' ', '_')}"
        self.workflows[workflow_id] = {
            "name": name,
            "description": description,
            "steps": steps,
            "custom": True
        }
        return workflow_id
    
    def get_workflow_progress(self, workflow_id: str, completed_steps: List[str]) -> Dict[str, Any]:
        """Get progress information for a workflow."""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"error": "Workflow not found"}
        
        total_steps = len(workflow["steps"])
        completed_count = len(completed_steps)
        progress_percentage = (completed_count / total_steps) * 100 if total_steps > 0 else 0
        
        next_step = None
        if completed_count < total_steps:
            next_step = workflow["steps"][completed_count]
        
        return {
            "workflow_name": workflow["name"],
            "total_steps": total_steps,
            "completed_steps": completed_count,
            "progress_percentage": progress_percentage,
            "next_step": next_step,
            "is_complete": completed_count >= total_steps
        }
    
    def get_step_details(self, workflow_id: str, step_index: int) -> Dict[str, Any]:
        """Get detailed information about a specific workflow step."""
        workflow = self.workflows.get(workflow_id)
        if not workflow or step_index >= len(workflow["steps"]):
            return {"error": "Workflow or step not found"}
        
        step = workflow["steps"][step_index]
        
        # Add detailed descriptions for each tool
        step_descriptions = {
            "keyword_research": "Research and identify target keywords for your content",
            "content_gap_analysis": "Analyze competitor content to find opportunities",
            "blog_writing": "Create high-quality, SEO-optimized blog content",
            "seo_optimization": "Optimize content for search engines",
            "meta_generation": "Generate meta titles and descriptions",
            "competitor_analysis": "Analyze competitor strategies and performance",
            "content_calendar": "Plan and schedule content publication",
            "content_ideas": "Generate creative content ideas and topics",
            "audience_analysis": "Research and define target audience",
            "content_planning": "Plan content strategy and themes",
            "social_content_creation": "Create platform-specific social media content",
            "hashtag_research": "Research relevant hashtags for social media",
            "technical_seo": "Analyze technical SEO aspects of website",
            "on_page_seo": "Review and optimize on-page SEO elements"
        }
        
        return {
            "tool": step["tool"],
            "name": step["name"],
            "description": step_descriptions.get(step["tool"], "Execute this workflow step"),
            "step_number": step_index + 1,
            "total_steps": len(workflow["steps"])
        } 