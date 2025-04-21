Installation
============

System Requirements
------------------

Before installing AI-Writer, ensure your system meets the following requirements:

* Python 3.9 or higher
* 4GB RAM minimum (8GB recommended)
* 2GB free disk space
* Internet connection for AI API access

Installation Methods
------------------

There are several ways to install and run AI-Writer:

Method 1: Using pip (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/AJaySi/AI-Writer.git
   cd AI-Writer
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the application
   streamlit run alwrity.py

Method 2: Using Docker
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/AJaySi/AI-Writer.git
   cd AI-Writer
   
   # Build and run with Docker Compose
   docker-compose up -d

Method 3: Manual Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer to install dependencies manually:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/AJaySi/AI-Writer.git
   cd AI-Writer
   
   # Create a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install core dependencies
   pip install streamlit openai google-generativeai chromadb sqlalchemy

   # Install additional dependencies as needed
   pip install beautifulsoup4 requests pandas matplotlib plotly

   # Run the application
   streamlit run alwrity.py

Configuration
------------

After installation, you'll need to configure AI-Writer with your API keys:

1. Launch the application using `streamlit run alwrity.py`
2. Follow the setup wizard to configure:
   - AI provider API keys (OpenAI, Google Gemini, etc.)
   - Research tools settings
   - Database configuration
   - Personalization options

The configuration will be saved and can be modified later through the settings page.

Troubleshooting
--------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Dependency Conflicts**

   If you encounter dependency conflicts, try installing in a fresh virtual environment:

   .. code-block:: bash

      python -m venv fresh_venv
      source fresh_venv/bin/activate
      pip install -r requirements.txt

2. **Port Already in Use**

   If Streamlit cannot start because the port is in use:

   .. code-block:: bash

      streamlit run alwrity.py --server.port=8501

3. **Database Connection Issues**

   Ensure you have proper permissions for creating and accessing database files:

   .. code-block:: bash

      # Check permissions
      chmod 755 -R ./data

For additional help, please refer to the project's GitHub issues page or contact the maintainers.