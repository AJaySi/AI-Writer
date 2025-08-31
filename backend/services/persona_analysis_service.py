"""
Persona Analysis Service
Uses Gemini structured responses to analyze onboarding data and create writing personas.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime
import json

from services.database import get_db_session
from models.onboarding import OnboardingSession, WebsiteAnalysis, ResearchPreferences
from models.persona_models import WritingPersona, PlatformPersona, PersonaAnalysisResult
from services.llm_providers.gemini_provider import gemini_structured_json_response

class PersonaAnalysisService:
    """Service for analyzing onboarding data and generating writing personas using Gemini AI."""
    
    def __init__(self):
        """Initialize the persona analysis service."""
        logger.info("PersonaAnalysisService initialized")
    
    def generate_persona_from_onboarding(self, user_id: int, onboarding_session_id: int = None) -> Dict[str, Any]:
        """
        Generate a comprehensive writing persona from user's onboarding data.
        
        Args:
            user_id: User ID to generate persona for
            onboarding_session_id: Optional specific onboarding session ID
            
        Returns:
            Generated persona data with platform adaptations
        """
        try:
            logger.info(f"Generating persona for user {user_id}")
            
            # Get onboarding data
            onboarding_data = self._collect_onboarding_data(user_id, onboarding_session_id)
            
            if not onboarding_data:
                logger.warning(f"No onboarding data found for user {user_id}")
                return {"error": "No onboarding data available for persona generation"}
            
            # Generate core persona using Gemini
            core_persona = self._generate_core_persona(onboarding_data)
            
            if "error" in core_persona:
                return core_persona
            
            # Generate platform-specific adaptations
            platform_personas = self._generate_platform_adaptations(core_persona, onboarding_data)
            
            # Save to database
            saved_persona = self._save_persona_to_db(user_id, core_persona, platform_personas, onboarding_data)
            
            return {
                "persona_id": saved_persona.id,
                "core_persona": core_persona,
                "platform_personas": platform_personas,
                "analysis_metadata": {
                    "confidence_score": core_persona.get("confidence_score", 0.0),
                    "data_sufficiency": self._calculate_data_sufficiency(onboarding_data),
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating persona for user {user_id}: {str(e)}")
            return {"error": f"Failed to generate persona: {str(e)}"}
    
    def _collect_onboarding_data(self, user_id: int, session_id: int = None) -> Optional[Dict[str, Any]]:
        """Collect comprehensive onboarding data for persona analysis."""
        try:
            session = get_db_session()
            
            # Find onboarding session
            if session_id:
                onboarding_session = session.query(OnboardingSession).filter(
                    OnboardingSession.id == session_id,
                    OnboardingSession.user_id == user_id
                ).first()
            else:
                onboarding_session = session.query(OnboardingSession).filter(
                    OnboardingSession.user_id == user_id
                ).order_by(OnboardingSession.updated_at.desc()).first()
            
            if not onboarding_session:
                return None
            
            # Get website analysis
            website_analysis = session.query(WebsiteAnalysis).filter(
                WebsiteAnalysis.session_id == onboarding_session.id
            ).first()
            
            # Get research preferences
            research_prefs = session.query(ResearchPreferences).filter(
                ResearchPreferences.session_id == onboarding_session.id
            ).first()
            
            # Compile comprehensive data
            onboarding_data = {
                "session_info": {
                    "session_id": onboarding_session.id,
                    "current_step": onboarding_session.current_step,
                    "progress": onboarding_session.progress,
                    "started_at": onboarding_session.started_at.isoformat() if onboarding_session.started_at else None
                },
                "website_analysis": website_analysis.to_dict() if website_analysis else None,
                "research_preferences": research_prefs.to_dict() if research_prefs else None
            }
            
            session.close()
            return onboarding_data
            
        except Exception as e:
            logger.error(f"Error collecting onboarding data: {str(e)}")
            return None
    
    def _generate_core_persona(self, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate core writing persona using Gemini structured response."""
        
        # Build analysis prompt
        prompt = self._build_persona_analysis_prompt(onboarding_data)
        
        # Define schema for structured response
        persona_schema = {
            "type": "object",
            "properties": {
                "identity": {
                    "type": "object",
                    "properties": {
                        "persona_name": {"type": "string"},
                        "archetype": {"type": "string"},
                        "core_belief": {"type": "string"},
                        "brand_voice_description": {"type": "string"}
                    },
                    "required": ["persona_name", "archetype", "core_belief"]
                },
                "linguistic_fingerprint": {
                    "type": "object",
                    "properties": {
                        "sentence_metrics": {
                            "type": "object",
                            "properties": {
                                "average_sentence_length_words": {"type": "number"},
                                "preferred_sentence_type": {"type": "string"},
                                "active_to_passive_ratio": {"type": "string"},
                                "complexity_level": {"type": "string"}
                            }
                        },
                        "lexical_features": {
                            "type": "object",
                            "properties": {
                                "go_to_words": {"type": "array", "items": {"type": "string"}},
                                "go_to_phrases": {"type": "array", "items": {"type": "string"}},
                                "avoid_words": {"type": "array", "items": {"type": "string"}},
                                "contractions": {"type": "string"},
                                "filler_words": {"type": "string"},
                                "vocabulary_level": {"type": "string"}
                            }
                        },
                        "rhetorical_devices": {
                            "type": "object",
                            "properties": {
                                "metaphors": {"type": "string"},
                                "analogies": {"type": "string"},
                                "rhetorical_questions": {"type": "string"},
                                "storytelling_style": {"type": "string"}
                            }
                        }
                    }
                },
                "tonal_range": {
                    "type": "object",
                    "properties": {
                        "default_tone": {"type": "string"},
                        "permissible_tones": {"type": "array", "items": {"type": "string"}},
                        "forbidden_tones": {"type": "array", "items": {"type": "string"}},
                        "emotional_range": {"type": "string"}
                    }
                },
                "stylistic_constraints": {
                    "type": "object",
                    "properties": {
                        "punctuation": {
                            "type": "object",
                            "properties": {
                                "ellipses": {"type": "string"},
                                "em_dash": {"type": "string"},
                                "exclamation_points": {"type": "string"}
                            }
                        },
                        "formatting": {
                            "type": "object",
                            "properties": {
                                "paragraphs": {"type": "string"},
                                "lists": {"type": "string"},
                                "markdown": {"type": "string"}
                            }
                        }
                    }
                },
                "confidence_score": {"type": "number"},
                "analysis_notes": {"type": "string"}
            },
            "required": ["identity", "linguistic_fingerprint", "tonal_range", "confidence_score"]
        }
        
        try:
            # Generate structured response using Gemini
            response = gemini_structured_json_response(
                prompt=prompt,
                schema=persona_schema,
                temperature=0.2,  # Low temperature for consistent analysis
                max_tokens=8192,
                system_prompt="You are an expert writing style analyst and persona developer. Analyze the provided data to create a precise, actionable writing persona."
            )
            
            if "error" in response:
                logger.error(f"Gemini API error: {response['error']}")
                return {"error": f"AI analysis failed: {response['error']}"}
            
            logger.info("✅ Core persona generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error generating core persona: {str(e)}")
            return {"error": f"Failed to generate core persona: {str(e)}"}
    
    def _generate_platform_adaptations(self, core_persona: Dict[str, Any], onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate platform-specific persona adaptations."""
        
        platforms = ["twitter", "linkedin", "instagram", "facebook", "blog", "medium", "substack"]
        platform_personas = {}
        
        for platform in platforms:
            try:
                platform_persona = self._generate_single_platform_persona(core_persona, platform, onboarding_data)
                if "error" not in platform_persona:
                    platform_personas[platform] = platform_persona
                else:
                    logger.warning(f"Failed to generate {platform} persona: {platform_persona['error']}")
            except Exception as e:
                logger.error(f"Error generating {platform} persona: {str(e)}")
        
        return platform_personas
    
    def _generate_single_platform_persona(self, core_persona: Dict[str, Any], platform: str, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate persona adaptation for a specific platform."""
        
        prompt = self._build_platform_adaptation_prompt(core_persona, platform, onboarding_data)
        
        # Platform-specific schema
        platform_schema = {
            "type": "object",
            "properties": {
                "platform_type": {"type": "string"},
                "sentence_metrics": {
                    "type": "object",
                    "properties": {
                        "max_sentence_length": {"type": "number"},
                        "optimal_sentence_length": {"type": "number"},
                        "sentence_variety": {"type": "string"}
                    }
                },
                "lexical_adaptations": {
                    "type": "object",
                    "properties": {
                        "platform_specific_words": {"type": "array", "items": {"type": "string"}},
                        "hashtag_strategy": {"type": "string"},
                        "emoji_usage": {"type": "string"},
                        "mention_strategy": {"type": "string"}
                    }
                },
                "content_format_rules": {
                    "type": "object",
                    "properties": {
                        "character_limit": {"type": "number"},
                        "paragraph_structure": {"type": "string"},
                        "call_to_action_style": {"type": "string"},
                        "link_placement": {"type": "string"}
                    }
                },
                "engagement_patterns": {
                    "type": "object",
                    "properties": {
                        "posting_frequency": {"type": "string"},
                        "optimal_posting_times": {"type": "array", "items": {"type": "string"}},
                        "engagement_tactics": {"type": "array", "items": {"type": "string"}},
                        "community_interaction": {"type": "string"}
                    }
                },
                "platform_best_practices": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["platform_type", "sentence_metrics", "content_format_rules", "engagement_patterns"]
        }
        
        try:
            response = gemini_structured_json_response(
                prompt=prompt,
                schema=platform_schema,
                temperature=0.2,
                max_tokens=4096,
                system_prompt=f"You are an expert in {platform} content strategy and platform-specific writing optimization."
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating {platform} persona: {str(e)}")
            return {"error": f"Failed to generate {platform} persona: {str(e)}"}
    
    def _build_persona_analysis_prompt(self, onboarding_data: Dict[str, Any]) -> str:
        """Build the main persona analysis prompt."""
        
        website_analysis = onboarding_data.get("website_analysis", {})
        research_prefs = onboarding_data.get("research_preferences", {})
        
        prompt = f"""
PERSONA GENERATION TASK: Create a comprehensive writing persona based on user onboarding data.

ONBOARDING DATA ANALYSIS:

Website Analysis:
- URL: {website_analysis.get('website_url', 'Not provided')}
- Writing Style: {json.dumps(website_analysis.get('writing_style', {}), indent=2)}
- Content Characteristics: {json.dumps(website_analysis.get('content_characteristics', {}), indent=2)}
- Target Audience: {json.dumps(website_analysis.get('target_audience', {}), indent=2)}
- Content Type: {json.dumps(website_analysis.get('content_type', {}), indent=2)}
- Style Patterns: {json.dumps(website_analysis.get('style_patterns', {}), indent=2)}

Research Preferences:
- Research Depth: {research_prefs.get('research_depth', 'Not set')}
- Content Types: {research_prefs.get('content_types', [])}
- Auto Research: {research_prefs.get('auto_research', False)}
- Factual Content: {research_prefs.get('factual_content', False)}

PERSONA GENERATION REQUIREMENTS:

1. IDENTITY CREATION:
   - Create a memorable persona name that captures the essence of the writing style
   - Define a clear archetype (e.g., "The Pragmatic Futurist", "The Thoughtful Educator")
   - Articulate a core belief that drives the writing philosophy
   - Write a comprehensive brand voice description

2. LINGUISTIC FINGERPRINT (Quantitative Analysis):
   - Calculate average sentence length based on website analysis
   - Determine preferred sentence types (simple, compound, complex)
   - Analyze active vs passive voice ratio
   - Identify go-to words and phrases from the content analysis
   - List words and phrases to avoid
   - Determine contraction usage patterns
   - Assess vocabulary complexity level

3. RHETORICAL ANALYSIS:
   - Identify metaphor patterns and themes
   - Analyze analogy usage
   - Assess rhetorical question frequency and style
   - Determine storytelling approach

4. TONAL RANGE:
   - Define the default tone
   - List permissible tones for different contexts
   - Identify forbidden tones that don't match the brand
   - Describe emotional range and expression

5. STYLISTIC CONSTRAINTS:
   - Define punctuation preferences and rules
   - Set formatting guidelines
   - Establish paragraph structure preferences

ANALYSIS INSTRUCTIONS:
- Base your analysis on the actual data provided from the website analysis
- If data is limited, make reasonable inferences but note the confidence level
- Ensure the persona is actionable and specific enough for AI content generation
- Provide a confidence score (0-100) based on data availability and quality
- Include analysis notes explaining your reasoning

Generate a comprehensive persona profile that can be used to replicate this writing style across different platforms.
"""
        
        return prompt
    
    def _build_platform_adaptation_prompt(self, core_persona: Dict[str, Any], platform: str, onboarding_data: Dict[str, Any]) -> str:
        """Build prompt for platform-specific persona adaptation."""
        
        platform_constraints = self._get_platform_constraints(platform)
        
        prompt = f"""
PLATFORM ADAPTATION TASK: Adapt the core writing persona for {platform.upper()}.

CORE PERSONA:
{json.dumps(core_persona, indent=2)}

PLATFORM: {platform.upper()}

PLATFORM CONSTRAINTS:
{json.dumps(platform_constraints, indent=2)}

ADAPTATION REQUIREMENTS:

1. SENTENCE METRICS:
   - Adjust sentence length for platform optimal performance
   - Adapt sentence variety for platform engagement
   - Consider platform reading patterns

2. LEXICAL ADAPTATIONS:
   - Identify platform-specific vocabulary and slang
   - Define hashtag strategy (if applicable)
   - Set emoji usage guidelines
   - Establish mention and tagging strategy

3. CONTENT FORMAT RULES:
   - Respect character/word limits
   - Optimize paragraph structure for platform
   - Define call-to-action style
   - Set link placement strategy

4. ENGAGEMENT PATTERNS:
   - Determine optimal posting frequency
   - Identify best posting times for audience
   - Define engagement tactics
   - Set community interaction guidelines

5. PLATFORM BEST PRACTICES:
   - List platform-specific optimization techniques
   - Consider algorithm preferences
   - Include trending format adaptations

INSTRUCTIONS:
- Maintain the core persona identity while optimizing for platform performance
- Ensure all adaptations align with the original brand voice
- Consider platform-specific audience behavior
- Provide actionable, specific guidelines

Generate a platform-optimized persona adaptation that maintains brand consistency while maximizing platform performance.
"""
        
        return prompt
    
    def _get_platform_constraints(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific constraints and best practices."""
        
        constraints = {
            "twitter": {
                "character_limit": 280,
                "optimal_length": "120-150 characters",
                "hashtag_limit": 3,
                "image_support": True,
                "thread_support": True,
                "link_shortening": True
            },
            "linkedin": {
                "character_limit": 3000,
                "optimal_length": "150-300 words",
                "professional_tone": True,
                "hashtag_limit": 5,
                "rich_media": True,
                "long_form": True
            },
            "instagram": {
                "caption_limit": 2200,
                "optimal_length": "125-150 words",
                "hashtag_limit": 30,
                "visual_first": True,
                "story_support": True,
                "emoji_friendly": True
            },
            "facebook": {
                "character_limit": 63206,
                "optimal_length": "40-80 words",
                "algorithm_favors": "engagement",
                "link_preview": True,
                "event_support": True,
                "group_sharing": True
            },
            "blog": {
                "word_count": "800-2000 words",
                "seo_important": True,
                "header_structure": True,
                "internal_linking": True,
                "meta_descriptions": True,
                "readability_score": True
            },
            "medium": {
                "word_count": "1000-3000 words",
                "storytelling_focus": True,
                "subtitle_support": True,
                "publication_support": True,
                "clap_optimization": True,
                "follower_building": True
            },
            "substack": {
                "newsletter_format": True,
                "email_optimization": True,
                "subscription_focus": True,
                "long_form": True,
                "personal_connection": True,
                "monetization_support": True
            }
        }
        
        return constraints.get(platform, {})
    
    def _save_persona_to_db(self, user_id: int, core_persona: Dict[str, Any], platform_personas: Dict[str, Any], onboarding_data: Dict[str, Any]) -> WritingPersona:
        """Save generated persona to database."""
        try:
            session = get_db_session()
            
            # Create main persona record
            writing_persona = WritingPersona(
                user_id=user_id,
                persona_name=core_persona.get("identity", {}).get("persona_name", "Generated Persona"),
                archetype=core_persona.get("identity", {}).get("archetype"),
                core_belief=core_persona.get("identity", {}).get("core_belief"),
                brand_voice_description=core_persona.get("identity", {}).get("brand_voice_description"),
                linguistic_fingerprint=core_persona.get("linguistic_fingerprint", {}),
                platform_adaptations={"platforms": list(platform_personas.keys())},
                onboarding_session_id=onboarding_data.get("session_info", {}).get("session_id"),
                source_website_analysis=onboarding_data.get("website_analysis"),
                source_research_preferences=onboarding_data.get("research_preferences"),
                ai_analysis_version="gemini_v1.0",
                confidence_score=core_persona.get("confidence_score", 0.0)
            )
            
            session.add(writing_persona)
            session.commit()
            session.refresh(writing_persona)
            
            # Create platform-specific persona records
            for platform, platform_data in platform_personas.items():
                platform_persona = PlatformPersona(
                    writing_persona_id=writing_persona.id,
                    platform_type=platform,
                    sentence_metrics=platform_data.get("sentence_metrics", {}),
                    lexical_features=platform_data.get("lexical_adaptations", {}),
                    rhetorical_devices=core_persona.get("linguistic_fingerprint", {}).get("rhetorical_devices", {}),
                    tonal_range=core_persona.get("tonal_range", {}),
                    stylistic_constraints=core_persona.get("stylistic_constraints", {}),
                    content_format_rules=platform_data.get("content_format_rules", {}),
                    engagement_patterns=platform_data.get("engagement_patterns", {}),
                    platform_best_practices={"practices": platform_data.get("platform_best_practices", [])}
                )
                session.add(platform_persona)
            
            # Save analysis result
            analysis_result = PersonaAnalysisResult(
                user_id=user_id,
                writing_persona_id=writing_persona.id,
                analysis_prompt=self._build_persona_analysis_prompt(onboarding_data)[:5000],  # Truncate for storage
                input_data=onboarding_data,
                linguistic_analysis=core_persona.get("linguistic_fingerprint", {}),
                personality_analysis=core_persona.get("identity", {}),
                platform_recommendations=platform_personas,
                style_guidelines=core_persona.get("stylistic_constraints", {}),
                analysis_confidence=core_persona.get("confidence_score", 0.0),
                data_sufficiency_score=self._calculate_data_sufficiency(onboarding_data),
                ai_provider="gemini",
                model_version="gemini-2.5-flash"
            )
            session.add(analysis_result)
            
            session.commit()
            session.close()
            
            logger.info(f"✅ Persona saved to database with ID: {writing_persona.id}")
            return writing_persona
            
        except Exception as e:
            logger.error(f"Error saving persona to database: {str(e)}")
            if session:
                session.rollback()
                session.close()
            raise
    
    def _calculate_data_sufficiency(self, onboarding_data: Dict[str, Any]) -> float:
        """Calculate how sufficient the onboarding data is for persona generation."""
        score = 0.0
        
        website_analysis = onboarding_data.get("website_analysis", {})
        research_prefs = onboarding_data.get("research_preferences", {})
        
        # Website analysis components (70% of score)
        if website_analysis.get("writing_style"):
            score += 25
        if website_analysis.get("content_characteristics"):
            score += 20
        if website_analysis.get("target_audience"):
            score += 15
        if website_analysis.get("style_patterns"):
            score += 10
        
        # Research preferences components (30% of score)
        if research_prefs.get("research_depth"):
            score += 10
        if research_prefs.get("content_types"):
            score += 10
        if research_prefs.get("writing_style"):
            score += 10
        
        return min(score, 100.0)
    
    def get_user_personas(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all personas for a user."""
        try:
            session = get_db_session()
            
            personas = session.query(WritingPersona).filter(
                WritingPersona.user_id == user_id,
                WritingPersona.is_active == True
            ).all()
            
            result = []
            for persona in personas:
                persona_dict = persona.to_dict()
                
                # Get platform personas
                platform_personas = session.query(PlatformPersona).filter(
                    PlatformPersona.writing_persona_id == persona.id,
                    PlatformPersona.is_active == True
                ).all()
                
                persona_dict["platforms"] = [pp.to_dict() for pp in platform_personas]
                result.append(persona_dict)
            
            session.close()
            return result
            
        except Exception as e:
            logger.error(f"Error getting user personas: {str(e)}")
            return []
    
    def get_persona_for_platform(self, user_id: int, platform: str) -> Optional[Dict[str, Any]]:
        """Get the best persona for a specific platform."""
        try:
            session = get_db_session()
            
            # Get the most recent active persona
            persona = session.query(WritingPersona).filter(
                WritingPersona.user_id == user_id,
                WritingPersona.is_active == True
            ).order_by(WritingPersona.created_at.desc()).first()
            
            if not persona:
                return None
            
            # Get platform-specific adaptation
            platform_persona = session.query(PlatformPersona).filter(
                PlatformPersona.writing_persona_id == persona.id,
                PlatformPersona.platform_type == platform,
                PlatformPersona.is_active == True
            ).first()
            
            result = {
                "core_persona": persona.to_dict(),
                "platform_adaptation": platform_persona.to_dict() if platform_persona else None
            }
            
            session.close()
            return result
            
        except Exception as e:
            logger.error(f"Error getting persona for platform {platform}: {str(e)}")
            return None