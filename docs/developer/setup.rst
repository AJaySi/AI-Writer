Development Environment Setup
============================

This guide will help you set up a development environment for contributing to the AI-Writer project.

Prerequisites
------------

Before setting up the development environment, ensure you have the following installed:

* Python 3.9 or higher
* Git
* A code editor (VS Code, PyCharm, etc.)
* Docker (optional, for containerized development)

Setting Up the Development Environment
------------------------------------

1. **Clone the Repository**

   .. code-block:: bash

      git clone https://github.com/AJaySi/AI-Writer.git
      cd AI-Writer

2. **Create a Virtual Environment**

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Development Dependencies**

   .. code-block:: bash

      pip install -r requirements.txt
      pip install -r requirements-dev.txt  # Install development dependencies

4. **Set Up Pre-commit Hooks**

   .. code-block:: bash

      pip install pre-commit
      pre-commit install

5. **Configure Environment Variables**

   Create a `.env` file in the project root with the following variables:

   .. code-block:: bash

      # API Keys
      OPENAI_API_KEY=your_openai_api_key
      GOOGLE_API_KEY=your_google_api_key
      
      # Database Configuration
      DB_PATH=sqlite:///./data/alwrity.db
      VECTOR_DB_PATH=./data/vectordb
      
      # Development Settings
      DEBUG=True
      ENVIRONMENT=development

6. **Initialize the Database**

   .. code-block:: bash

      python -c "from lib.database.db_manager import init_db; init_db()"

7. **Run the Development Server**

   .. code-block:: bash

      streamlit run alwrity.py

Development Workflow
------------------

1. **Create a Feature Branch**

   Always create a new branch for your changes:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make Changes and Test**

   Implement your changes and test them thoroughly:

   .. code-block:: bash

      # Run tests
      pytest
      
      # Run linting
      flake8
      
      # Run type checking
      mypy .

3. **Commit Changes**

   Follow the commit message conventions:

   .. code-block:: bash

      git add .
      git commit -m "feat: add new feature"

4. **Push Changes and Create a Pull Request**

   .. code-block:: bash

      git push origin feature/your-feature-name

   Then create a pull request on GitHub.

Using Docker for Development
--------------------------

For containerized development:

1. **Build the Development Container**

   .. code-block:: bash

      docker build -t alwrity-dev -f Dockerfile.dev .

2. **Run the Development Container**

   .. code-block:: bash

      docker run -p 8501:8501 -v $(pwd):/app alwrity-dev

3. **Using Docker Compose**

   .. code-block:: bash

      docker-compose -f docker-compose.dev.yml up

Troubleshooting
-------------

Common development setup issues:

1. **Dependency Conflicts**

   If you encounter dependency conflicts, try:

   .. code-block:: bash

      pip install --upgrade pip
      pip install -r requirements.txt --no-cache-dir

2. **Database Migration Issues**

   If you encounter database migration issues:

   .. code-block:: bash

      # Reset the database
      rm -rf ./data/alwrity.db
      rm -rf ./data/vectordb
      
      # Reinitialize
      python -c "from lib.database.db_manager import init_db; init_db()"

3. **Streamlit Port Already in Use**

   If the Streamlit port is already in use:

   .. code-block:: bash

      streamlit run alwrity.py --server.port=8502