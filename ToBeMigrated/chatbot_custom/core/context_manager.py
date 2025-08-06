"""
Context Manager for Enhanced ALwrity Chatbot.

Manages conversation context, state, and user preferences with persistence.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ConversationTurn:
    """Represents a single conversation turn."""
    timestamp: str
    user_input: str
    intent: str
    tools_used: List[str]
    response_summary: str
    satisfaction_score: Optional[float] = None


@dataclass
class UserPreferences:
    """User preferences and settings."""
    content_preferences: List[str]
    preferred_tone: str
    preferred_length: str
    industry_focus: List[str]
    language: str
    timezone: str
    notification_settings: Dict[str, bool]


@dataclass
class WorkflowState:
    """Represents the state of an active workflow."""
    workflow_id: str
    workflow_name: str
    current_step: int
    total_steps: int
    step_data: Dict[str, Any]
    started_at: str
    last_updated: str
    is_paused: bool = False


class ContextManager:
    """Advanced conversation context and state management."""
    
    def __init__(self, user_id: str = "default", context_file: str = None):
        self.user_id = user_id
        self.context_file = context_file or f"user_context_{user_id}.json"
        self.context_dir = "lib/chatbot_custom/user_contexts"
        
        # Ensure context directory exists
        os.makedirs(self.context_dir, exist_ok=True)
        self.context_path = os.path.join(self.context_dir, self.context_file)
        
        # Initialize context data
        self.conversation_history: List[ConversationTurn] = []
        self.user_preferences: UserPreferences = UserPreferences(
            content_preferences=[],
            preferred_tone="professional",
            preferred_length="medium",
            industry_focus=[],
            language="en",
            timezone="UTC",
            notification_settings={}
        )
        self.active_workflows: List[WorkflowState] = []
        self.tool_usage_history: List[Dict[str, Any]] = []
        self.session_data: Dict[str, Any] = {}
        self.analytics_data: Dict[str, Any] = {
            "total_interactions": 0,
            "tools_used_count": {},
            "workflows_completed": 0,
            "average_session_length": 0,
            "last_active": None
        }
        
        # Load existing context
        self.load_context()
    
    def add_conversation_turn(self, user_input: str, intent: str, 
                            tools_used: List[str], response_summary: str,
                            satisfaction_score: Optional[float] = None):
        """Add a new conversation turn to history."""
        turn = ConversationTurn(
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            intent=intent,
            tools_used=tools_used,
            response_summary=response_summary,
            satisfaction_score=satisfaction_score
        )
        
        self.conversation_history.append(turn)
        
        # Keep only last 50 turns to manage memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
        
        # Update analytics
        self.analytics_data["total_interactions"] += 1
        self.analytics_data["last_active"] = datetime.now().isoformat()
        
        # Update tool usage statistics
        for tool in tools_used:
            if tool in self.analytics_data["tools_used_count"]:
                self.analytics_data["tools_used_count"][tool] += 1
            else:
                self.analytics_data["tools_used_count"][tool] = 1
        
        self.save_context()
    
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """Update user preferences."""
        for key, value in preferences.items():
            if hasattr(self.user_preferences, key):
                setattr(self.user_preferences, key, value)
        
        self.save_context()
    
    def get_recent_context(self, turns: int = 5) -> List[ConversationTurn]:
        """Get recent conversation turns for context."""
        return self.conversation_history[-turns:] if self.conversation_history else []
    
    def get_recent_topics(self, hours: int = 24) -> List[str]:
        """Get topics discussed in recent hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_topics = []
        
        for turn in self.conversation_history:
            turn_time = datetime.fromisoformat(turn.timestamp)
            if turn_time > cutoff_time:
                # Extract topics from intent and tools used
                recent_topics.append(turn.intent)
                recent_topics.extend(turn.tools_used)
        
        # Return unique topics
        return list(set(recent_topics))
    
    def get_tool_usage_history(self, limit: int = 10) -> List[str]:
        """Get recent tool usage history."""
        recent_tools = []
        for turn in self.conversation_history[-limit:]:
            recent_tools.extend(turn.tools_used)
        
        return recent_tools
    
    def start_workflow(self, workflow_id: str, workflow_name: str, total_steps: int):
        """Start a new workflow."""
        workflow_state = WorkflowState(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            current_step=0,
            total_steps=total_steps,
            step_data={},
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        self.active_workflows.append(workflow_state)
        self.save_context()
        
        return workflow_state
    
    def update_workflow_step(self, workflow_id: str, step_data: Dict[str, Any]):
        """Update workflow step data."""
        for workflow in self.active_workflows:
            if workflow.workflow_id == workflow_id:
                workflow.current_step += 1
                workflow.step_data.update(step_data)
                workflow.last_updated = datetime.now().isoformat()
                
                # Check if workflow is completed
                if workflow.current_step >= workflow.total_steps:
                    self.complete_workflow(workflow_id)
                
                self.save_context()
                return workflow
        
        return None
    
    def complete_workflow(self, workflow_id: str):
        """Mark workflow as completed and remove from active workflows."""
        self.active_workflows = [w for w in self.active_workflows if w.workflow_id != workflow_id]
        self.analytics_data["workflows_completed"] += 1
        self.save_context()
    
    def pause_workflow(self, workflow_id: str):
        """Pause an active workflow."""
        for workflow in self.active_workflows:
            if workflow.workflow_id == workflow_id:
                workflow.is_paused = True
                workflow.last_updated = datetime.now().isoformat()
                self.save_context()
                return True
        return False
    
    def resume_workflow(self, workflow_id: str):
        """Resume a paused workflow."""
        for workflow in self.active_workflows:
            if workflow.workflow_id == workflow_id:
                workflow.is_paused = False
                workflow.last_updated = datetime.now().isoformat()
                self.save_context()
                return True
        return False
    
    def get_active_workflows(self) -> List[WorkflowState]:
        """Get all active workflows."""
        return [w for w in self.active_workflows if not w.is_paused]
    
    def get_paused_workflows(self) -> List[WorkflowState]:
        """Get all paused workflows."""
        return [w for w in self.active_workflows if w.is_paused]
    
    def set_session_data(self, key: str, value: Any):
        """Set session-specific data."""
        self.session_data[key] = value
    
    def get_session_data(self, key: str, default: Any = None) -> Any:
        """Get session-specific data."""
        return self.session_data.get(key, default)
    
    def clear_session_data(self):
        """Clear all session data."""
        self.session_data.clear()
    
    def get_context_for_intent_analysis(self) -> Dict[str, Any]:
        """Get context data for intent analysis."""
        return {
            "recent_topics": self.get_recent_topics(),
            "user_preferences": asdict(self.user_preferences),
            "active_workflows": [w.workflow_name for w in self.get_active_workflows()],
            "tool_usage_history": self.get_tool_usage_history(),
            "session_data": self.session_data
        }
    
    def get_user_analytics(self) -> Dict[str, Any]:
        """Get user analytics and usage statistics."""
        # Calculate average session length
        if self.conversation_history:
            session_starts = []
            current_session_start = None
            
            for turn in self.conversation_history:
                turn_time = datetime.fromisoformat(turn.timestamp)
                if not current_session_start:
                    current_session_start = turn_time
                elif (turn_time - current_session_start).total_seconds() > 3600:  # 1 hour gap = new session
                    session_starts.append(current_session_start)
                    current_session_start = turn_time
            
            if current_session_start:
                session_starts.append(current_session_start)
        
        # Most used tools
        most_used_tools = sorted(
            self.analytics_data["tools_used_count"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Recent activity pattern
        recent_activity = {}
        for turn in self.conversation_history[-20:]:  # Last 20 turns
            date = turn.timestamp.split('T')[0]  # Get date part
            if date in recent_activity:
                recent_activity[date] += 1
            else:
                recent_activity[date] = 1
        
        return {
            **self.analytics_data,
            "most_used_tools": most_used_tools,
            "recent_activity_pattern": recent_activity,
            "active_workflows_count": len(self.get_active_workflows()),
            "paused_workflows_count": len(self.get_paused_workflows()),
            "conversation_turns": len(self.conversation_history)
        }
    
    def export_conversation_history(self, format: str = "json") -> str:
        """Export conversation history in specified format."""
        if format.lower() == "json":
            return json.dumps([asdict(turn) for turn in self.conversation_history], indent=2)
        elif format.lower() == "txt":
            text_export = []
            for turn in self.conversation_history:
                text_export.append(f"[{turn.timestamp}] User: {turn.user_input}")
                text_export.append(f"Intent: {turn.intent}, Tools: {', '.join(turn.tools_used)}")
                text_export.append(f"Response: {turn.response_summary}")
                text_export.append("-" * 50)
            return "\n".join(text_export)
        else:
            raise ValueError("Unsupported export format. Use 'json' or 'txt'.")
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old conversation data beyond specified days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        self.conversation_history = [
            turn for turn in self.conversation_history
            if datetime.fromisoformat(turn.timestamp) > cutoff_date
        ]
        
        self.save_context()
    
    def save_context(self):
        """Save context data to file."""
        try:
            context_data = {
                "user_id": self.user_id,
                "conversation_history": [asdict(turn) for turn in self.conversation_history],
                "user_preferences": asdict(self.user_preferences),
                "active_workflows": [asdict(workflow) for workflow in self.active_workflows],
                "analytics_data": self.analytics_data,
                "last_saved": datetime.now().isoformat()
            }
            
            with open(self.context_path, 'w', encoding='utf-8') as f:
                json.dump(context_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving context: {e}")
    
    def load_context(self):
        """Load context data from file."""
        try:
            if os.path.exists(self.context_path):
                with open(self.context_path, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)
                
                # Load conversation history
                self.conversation_history = [
                    ConversationTurn(**turn_data) 
                    for turn_data in context_data.get("conversation_history", [])
                ]
                
                # Load user preferences
                prefs_data = context_data.get("user_preferences", {})
                if prefs_data:
                    self.user_preferences = UserPreferences(**prefs_data)
                
                # Load active workflows
                self.active_workflows = [
                    WorkflowState(**workflow_data)
                    for workflow_data in context_data.get("active_workflows", [])
                ]
                
                # Load analytics data
                self.analytics_data.update(context_data.get("analytics_data", {}))
                
        except Exception as e:
            print(f"Error loading context: {e}")
            # Continue with default values if loading fails
    
    def reset_context(self):
        """Reset all context data (use with caution)."""
        self.conversation_history.clear()
        self.active_workflows.clear()
        self.session_data.clear()
        self.analytics_data = {
            "total_interactions": 0,
            "tools_used_count": {},
            "workflows_completed": 0,
            "average_session_length": 0,
            "last_active": None
        }
        
        # Reset user preferences to defaults
        self.user_preferences = UserPreferences(
            content_preferences=[],
            preferred_tone="professional",
            preferred_length="medium",
            industry_focus=[],
            language="en",
            timezone="UTC",
            notification_settings={}
        )
        
        self.save_context()
    
    def get_context_summary(self) -> str:
        """Get a human-readable summary of the current context."""
        summary_parts = []
        
        # Basic stats
        summary_parts.append(f"Total interactions: {self.analytics_data['total_interactions']}")
        summary_parts.append(f"Conversation turns: {len(self.conversation_history)}")
        
        # Active workflows
        active_workflows = self.get_active_workflows()
        if active_workflows:
            workflow_names = [w.workflow_name for w in active_workflows]
            summary_parts.append(f"Active workflows: {', '.join(workflow_names)}")
        
        # Recent topics
        recent_topics = self.get_recent_topics(hours=6)  # Last 6 hours
        if recent_topics:
            summary_parts.append(f"Recent topics: {', '.join(recent_topics[:5])}")
        
        # User preferences
        if self.user_preferences.content_preferences:
            summary_parts.append(f"Content preferences: {', '.join(self.user_preferences.content_preferences)}")
        
        summary_parts.append(f"Preferred tone: {self.user_preferences.preferred_tone}")
        
        return "\n".join(summary_parts) 