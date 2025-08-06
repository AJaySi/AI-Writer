from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, JSON, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class OnboardingSession(Base):
    __tablename__ = 'onboarding_sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # Replace with ForeignKey if you have a user table
    current_step = Column(Integer, default=1)
    progress = Column(Float, default=0.0)
    started_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    api_keys = relationship('APIKey', back_populates='session', cascade="all, delete-orphan")
    website_analyses = relationship('WebsiteAnalysis', back_populates='session', cascade="all, delete-orphan")
    research_preferences = relationship('ResearchPreferences', back_populates='session', cascade="all, delete-orphan", uselist=False)

    def __repr__(self):
        return f"<OnboardingSession(id={self.id}, user_id={self.user_id}, step={self.current_step}, progress={self.progress})>"

class APIKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('onboarding_sessions.id'))
    provider = Column(String(64), nullable=False)
    key = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    session = relationship('OnboardingSession', back_populates='api_keys')

    def __repr__(self):
        return f"<APIKey(id={self.id}, provider={self.provider}, session_id={self.session_id})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'provider': self.provider,
            'key': self.key,  # Note: In production, you might want to mask this
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WebsiteAnalysis(Base):
    """Stores website analysis results from onboarding step 2."""
    __tablename__ = 'website_analyses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('onboarding_sessions.id', ondelete='CASCADE'), nullable=False)
    website_url = Column(String(500), nullable=False)
    analysis_date = Column(DateTime, default=func.now())
    
    # Style analysis results
    writing_style = Column(JSON)  # Tone, voice, complexity, engagement_level
    content_characteristics = Column(JSON)  # Sentence structure, vocabulary, paragraph organization
    target_audience = Column(JSON)  # Demographics, expertise level, industry focus
    content_type = Column(JSON)  # Primary type, secondary types, purpose
    recommended_settings = Column(JSON)  # Writing tone, target audience, content type
    
    # Crawl results
    crawl_result = Column(JSON)  # Raw crawl data
    style_patterns = Column(JSON)  # Writing patterns analysis
    style_guidelines = Column(JSON)  # Generated guidelines
    
    # Metadata
    status = Column(String(50), default='completed')  # completed, failed, in_progress
    error_message = Column(Text)
    warning_message = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    session = relationship('OnboardingSession', back_populates='website_analyses')
    
    def __repr__(self):
        return f"<WebsiteAnalysis(id={self.id}, url={self.website_url}, status={self.status})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'website_url': self.website_url,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'writing_style': self.writing_style,
            'content_characteristics': self.content_characteristics,
            'target_audience': self.target_audience,
            'content_type': self.content_type,
            'recommended_settings': self.recommended_settings,
            'crawl_result': self.crawl_result,
            'style_patterns': self.style_patterns,
            'style_guidelines': self.style_guidelines,
            'status': self.status,
            'error_message': self.error_message,
            'warning_message': self.warning_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 

class ResearchPreferences(Base):
    """Stores research preferences from onboarding step 3."""
    __tablename__ = 'research_preferences'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('onboarding_sessions.id', ondelete='CASCADE'), nullable=False)
    
    # Research configuration
    research_depth = Column(String(50), nullable=False)  # Basic, Standard, Comprehensive, Expert
    content_types = Column(JSON, nullable=False)  # Array of content types
    auto_research = Column(Boolean, default=True)
    factual_content = Column(Boolean, default=True)
    
    # Style detection data (from step 2)
    writing_style = Column(JSON)  # Tone, voice, complexity from website analysis
    content_characteristics = Column(JSON)  # Sentence structure, vocabulary from analysis
    target_audience = Column(JSON)  # Demographics, expertise level from analysis
    recommended_settings = Column(JSON)  # AI-generated recommendations from analysis
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    session = relationship('OnboardingSession', back_populates='research_preferences')
    
    def __repr__(self):
        return f"<ResearchPreferences(id={self.id}, session_id={self.session_id}, depth={self.research_depth})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'research_depth': self.research_depth,
            'content_types': self.content_types,
            'auto_research': self.auto_research,
            'factual_content': self.factual_content,
            'writing_style': self.writing_style,
            'content_characteristics': self.content_characteristics,
            'target_audience': self.target_audience,
            'recommended_settings': self.recommended_settings,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 