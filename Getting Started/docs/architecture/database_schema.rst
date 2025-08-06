Database Schema
==============

This document describes the database schema used in the AI-Writer platform, including both the relational database and vector database components.

Relational Database Schema
------------------------

AI-Writer uses SQLAlchemy ORM to interact with the relational database. The schema consists of the following main tables:

User
~~~~

Stores user information and preferences.

.. code-block:: python

   class User(Base):
       __tablename__ = "users"
       
       id = Column(Integer, primary_key=True)
       username = Column(String, unique=True, nullable=False)
       email = Column(String, unique=True, nullable=False)
       password_hash = Column(String, nullable=False)
       created_at = Column(DateTime, default=datetime.utcnow)
       updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
       
       # Relationships
       api_keys = relationship("ApiKey", back_populates="user")
       contents = relationship("Content", back_populates="user")
       settings = relationship("UserSetting", back_populates="user", uselist=False)

ApiKey
~~~~~~

Stores encrypted API keys for various services.

.. code-block:: python

   class ApiKey(Base):
       __tablename__ = "api_keys"
       
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey("users.id"))
       service_name = Column(String, nullable=False)
       encrypted_key = Column(String, nullable=False)
       is_active = Column(Boolean, default=True)
       created_at = Column(DateTime, default=datetime.utcnow)
       updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
       
       # Relationships
       user = relationship("User", back_populates="api_keys")

Content
~~~~~~~

Stores generated content with metadata.

.. code-block:: python

   class Content(Base):
       __tablename__ = "contents"
       
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey("users.id"))
       title = Column(String, nullable=False)
       content_type = Column(String, nullable=False)  # blog, linkedin, twitter, etc.
       content_text = Column(Text, nullable=False)
       metadata = Column(JSON)
       created_at = Column(DateTime, default=datetime.utcnow)
       updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
       
       # Relationships
       user = relationship("User", back_populates="contents")
       versions = relationship("ContentVersion", back_populates="content")
       analytics = relationship("ContentAnalytics", back_populates="content")

ContentVersion
~~~~~~~~~~~~~

Tracks versions of content for history and rollback.

.. code-block:: python

   class ContentVersion(Base):
       __tablename__ = "content_versions"
       
       id = Column(Integer, primary_key=True)
       content_id = Column(Integer, ForeignKey("contents.id"))
       version_number = Column(Integer, nullable=False)
       content_text = Column(Text, nullable=False)
       metadata = Column(JSON)
       created_at = Column(DateTime, default=datetime.utcnow)
       
       # Relationships
       content = relationship("Content", back_populates="versions")

ContentAnalytics
~~~~~~~~~~~~~~

Stores analytics data for content performance.

.. code-block:: python

   class ContentAnalytics(Base):
       __tablename__ = "content_analytics"
       
       id = Column(Integer, primary_key=True)
       content_id = Column(Integer, ForeignKey("contents.id"))
       views = Column(Integer, default=0)
       likes = Column(Integer, default=0)
       shares = Column(Integer, default=0)
       comments = Column(Integer, default=0)
       engagement_rate = Column(Float, default=0.0)
       last_updated = Column(DateTime, default=datetime.utcnow)
       
       # Relationships
       content = relationship("Content", back_populates="analytics")

UserSetting
~~~~~~~~~~

Stores user preferences and settings.

.. code-block:: python

   class UserSetting(Base):
       __tablename__ = "user_settings"
       
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey("users.id"), unique=True)
       preferred_ai_provider = Column(String)
       default_content_type = Column(String)
       ui_theme = Column(String, default="light")
       language = Column(String, default="en")
       settings_json = Column(JSON)
       
       # Relationships
       user = relationship("User", back_populates="settings")

Template
~~~~~~~

Stores reusable content templates.

.. code-block:: python

   class Template(Base):
       __tablename__ = "templates"
       
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey("users.id"))
       name = Column(String, nullable=False)
       content_type = Column(String, nullable=False)
       template_text = Column(Text, nullable=False)
       variables = Column(JSON)
       created_at = Column(DateTime, default=datetime.utcnow)
       updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
       
       # Relationships
       user = relationship("User")

ContentGapAnalysis
~~~~~~~~~~~~~~~~~

Stores content gap analysis results.

.. code-block:: python

   class ContentGapAnalysis(Base):
       __tablename__ = "content_gap_analyses"
       
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey("users.id"))
       website_url = Column(String, nullable=False)
       industry = Column(String, nullable=False)
       analysis_date = Column(DateTime, default=datetime.utcnow)
       status = Column(String, nullable=False)  # completed, in_progress, failed
       metadata = Column(JSON)
       
       # Relationships
       user = relationship("User", back_populates="content_gap_analyses")
       website_analysis = relationship("WebsiteAnalysis", back_populates="content_gap_analysis")
       competitor_analysis = relationship("CompetitorAnalysis", back_populates="content_gap_analysis")
       keyword_analysis = relationship("KeywordAnalysis", back_populates="content_gap_analysis")
       recommendations = relationship("ContentRecommendation", back_populates="content_gap_analysis")

WebsiteAnalysis
~~~~~~~~~~~~~~

Stores website analysis results.

.. code-block:: python

   class WebsiteAnalysis(Base):
       __tablename__ = "website_analyses"
       
       id = Column(Integer, primary_key=True)
       content_gap_analysis_id = Column(Integer, ForeignKey("content_gap_analyses.id"))
       content_score = Column(Float)
       seo_score = Column(Float)
       structure_score = Column(Float)
       content_metrics = Column(JSON)
       seo_metrics = Column(JSON)
       technical_metrics = Column(JSON)
       ai_insights = Column(JSON)
       created_at = Column(DateTime, default=datetime.utcnow)
       
       # Relationships
       content_gap_analysis = relationship("ContentGapAnalysis", back_populates="website_analysis")

CompetitorAnalysis
~~~~~~~~~~~~~~~~

Stores competitor analysis results.

.. code-block:: python

   class CompetitorAnalysis(Base):
       __tablename__ = "competitor_analyses"
       
       id = Column(Integer, primary_key=True)
       content_gap_analysis_id = Column(Integer, ForeignKey("content_gap_analyses.id"))
       competitor_url = Column(String, nullable=False)
       market_position = Column(JSON)
       content_gaps = Column(JSON)
       competitive_advantages = Column(JSON)
       trend_analysis = Column(JSON)
       created_at = Column(DateTime, default=datetime.utcnow)
       
       # Relationships
       content_gap_analysis = relationship("ContentGapAnalysis", back_populates="competitor_analysis")

KeywordAnalysis
~~~~~~~~~~~~~

Stores keyword analysis results.

.. code-block:: python

   class KeywordAnalysis(Base):
       __tablename__ = "keyword_analyses"
       
       id = Column(Integer, primary_key=True)
       content_gap_analysis_id = Column(Integer, ForeignKey("content_gap_analyses.id"))
       top_keywords = Column(JSON)
       search_intent = Column(JSON)
       opportunities = Column(JSON)
       trend_analysis = Column(JSON)
       created_at = Column(DateTime, default=datetime.utcnow)
       
       # Relationships
       content_gap_analysis = relationship("ContentGapAnalysis", back_populates="keyword_analysis")

ContentRecommendation
~~~~~~~~~~~~~~~~~~~

Stores content recommendations.

.. code-block:: python

   class ContentRecommendation(Base):
       __tablename__ = "content_recommendations"
       
       id = Column(Integer, primary_key=True)
       content_gap_analysis_id = Column(Integer, ForeignKey("content_gap_analyses.id"))
       recommendation_type = Column(String, nullable=False)  # content, seo, technical, etc.
       priority_score = Column(Float)
       recommendation = Column(Text, nullable=False)
       implementation_steps = Column(JSON)
       expected_impact = Column(JSON)
       status = Column(String, nullable=False)  # pending, in_progress, completed, rejected
       created_at = Column(DateTime, default=datetime.utcnow)
       updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
       
       # Relationships
       content_gap_analysis = relationship("ContentGapAnalysis", back_populates="recommendations")

AnalysisHistory
~~~~~~~~~~~~~

Tracks the history of analysis runs.

.. code-block:: python

   class AnalysisHistory(Base):
       __tablename__ = "analysis_histories"
       
       id = Column(Integer, primary_key=True)
       content_gap_analysis_id = Column(Integer, ForeignKey("content_gap_analyses.id"))
       run_date = Column(DateTime, default=datetime.utcnow)
       status = Column(String, nullable=False)  # completed, in_progress, failed
       metrics = Column(JSON)  # Performance metrics for the analysis run
       error_log = Column(Text)  # Any errors encountered during analysis
       
       # Relationships
       content_gap_analysis = relationship("ContentGapAnalysis")

Vector Database Schema
--------------------

AI-Writer uses ChromaDB for vector storage, which enables semantic search and retrieval of content. The vector database stores:

1. **Content Embeddings**
   
   * Generated from content text using embedding models
   * Used for semantic search and content similarity

2. **Metadata**
   
   * Content ID (linking to relational database)
   * Content type
   * Creation date
   * Keywords and tags

3. **Collections**
   
   ChromaDB organizes embeddings into collections:
   
   * `content_embeddings`: Main collection for all content
   * `user_{user_id}_content`: Per-user content collections
   * `{content_type}_embeddings`: Collections by content type

Vector Database Operations
------------------------

The vector database supports the following operations:

1. **Adding Content**
   
   .. code-block:: python

      def add_content_to_vector_db(content_id, content_text, metadata):
          """Add content to the vector database.
          
          Args:
              content_id: The ID of the content in the relational database.
              content_text: The text content to embed.
              metadata: Additional metadata for the content.
          """
          embeddings = get_embeddings(content_text)
          collection = get_collection("content_embeddings")
          collection.add(
              ids=[str(content_id)],
              embeddings=[embeddings],
              metadatas=[metadata],
              documents=[content_text]
          )

2. **Searching Content**
   
   .. code-block:: python

      def search_similar_content(query_text, limit=5):
          """Search for similar content using vector similarity.
          
          Args:
              query_text: The query text to search for.
              limit: Maximum number of results to return.
              
          Returns:
              List of similar content items with their similarity scores.
          """
          query_embedding = get_embeddings(query_text)
          collection = get_collection("content_embeddings")
          results = collection.query(
              query_embeddings=[query_embedding],
              n_results=limit
          )
          return results

3. **Updating Content**
   
   .. code-block:: python

      def update_content_in_vector_db(content_id, new_content_text, metadata):
          """Update content in the vector database.
          
          Args:
              content_id: The ID of the content to update.
              new_content_text: The updated text content.
              metadata: Updated metadata.
          """
          new_embedding = get_embeddings(new_content_text)
          collection = get_collection("content_embeddings")
          collection.update(
              ids=[str(content_id)],
              embeddings=[new_embedding],
              metadatas=[metadata],
              documents=[new_content_text]
          )

Database Migrations
-----------------

AI-Writer uses Alembic for database migrations. The migration workflow is:

1. **Create Migration**
   
   .. code-block:: bash

      alembic revision --autogenerate -m "Description of changes"

2. **Apply Migration**
   
   .. code-block:: bash

      alembic upgrade head

3. **Rollback Migration**
   
   .. code-block:: bash

      alembic downgrade -1

Database Backup and Restore
-------------------------

Regular database backups are recommended:

1. **SQLite Backup**
   
   .. code-block:: bash

      # Backup
      sqlite3 data/alwrity.db .dump > backup.sql
      
      # Restore
      sqlite3 data/alwrity.db < backup.sql

2. **Vector Database Backup**
   
   ChromaDB data is stored in the specified directory and can be backed up by copying the directory:
   
   .. code-block:: bash

      # Backup
      cp -r data/vectordb data/vectordb_backup
      
      # Restore
      rm -rf data/vectordb
      cp -r data/vectordb_backup data/vectordb