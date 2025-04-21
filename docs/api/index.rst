.. _api-reference:

API Reference
============

This section provides detailed documentation for the AI-Writer API, including module references, class hierarchies, and function specifications.

.. toctree::
   :maxdepth: 2
   :caption: API Documentation:

   core
   ai_writers
   database
   utils
   analytics
   web_crawlers

Core Modules
-----------

.. automodule:: alwrity
   :members:
   :undoc-members:
   :show-inheritance:

AI Writers
---------

The AI Writers modules provide specialized content generation for different platforms and content types.

.. toctree::
   :maxdepth: 1
   
   ai_writers/linkedin
   ai_writers/twitter
   ai_writers/blog
   ai_writers/email

Database
-------

The database modules handle content storage, retrieval, and vector search capabilities.

.. toctree::
   :maxdepth: 1
   
   database/models
   database/vector_store
   database/relational_store

Utilities
--------

Utility modules provide supporting functionality across the application.

.. toctree::
   :maxdepth: 1
   
   utils/api_key_manager
   utils/ui_setup
   utils/seo_tools

Analytics
--------

Analytics modules provide content performance tracking and visualization.

.. toctree::
   :maxdepth: 1
   
   analytics/content_analyzer
   analytics/analytics_ui

Web Crawlers
-----------

Web crawler modules provide research capabilities by extracting information from the web.

.. toctree::
   :maxdepth: 1
   
   web_crawlers/async_web_crawler