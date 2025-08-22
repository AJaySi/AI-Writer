#!/usr/bin/env python3
"""
ALwrity Backend Server - Comprehensive Startup Script
Handles setup, dependency installation, and server startup.
Run this from the backend directory to set up and start the FastAPI server.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def install_requirements():
    """Install required Python packages."""
    print("📦 Installing required packages...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_env_file():
    """Create a .env file with default configuration."""
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print("ℹ️  .env file already exists")
        return True
    
    print("🔧 Creating .env file with default configuration...")
    
    env_content = """# ALwrity Backend Configuration

# API Keys (Configure these in the onboarding process)
# OPENAI_API_KEY=your_openai_api_key_here
# GEMINI_API_KEY=your_gemini_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# MISTRAL_API_KEY=your_mistral_api_key_here

# Research API Keys (Optional)
# TAVILY_API_KEY=your_tavily_api_key_here
# SERPER_API_KEY=your_serper_api_key_here
# METAPHOR_API_KEY=your_metaphor_api_key_here
# FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Logging
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def setup_monitoring_tables():
    """Set up API monitoring database tables."""
    print("📊 Setting up API monitoring tables...")
    
    try:
        # Import and run the monitoring table creation
        sys.path.append(str(Path(__file__).parent))
        from scripts.create_monitoring_tables import create_monitoring_tables
        
        if create_monitoring_tables():
            print("✅ API monitoring tables created successfully!")
            return True
        else:
            print("⚠️  Warning: Failed to create monitoring tables, continuing anyway...")
            return True  # Don't fail startup for monitoring issues
            
    except Exception as e:
        print(f"⚠️  Warning: Could not set up monitoring tables: {e}")
        print("   Monitoring will be disabled. Continuing startup...")
        return True  # Don't fail startup for monitoring issues

def setup_monitoring_middleware():
    """Set up monitoring middleware in app.py if not already present."""
    print("🔍 Setting up API monitoring middleware...")
    
    app_file = Path(__file__).parent / "app.py"
    
    if not app_file.exists():
        print("⚠️  Warning: app.py not found, skipping middleware setup")
        return True
    
    try:
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Check if monitoring middleware is already set up
        if "monitoring_middleware" in content:
            print("✅ Monitoring middleware already configured")
            return True
        
        # Add monitoring middleware import and setup
        monitoring_import = "from middleware.monitoring_middleware import monitoring_middleware\n"
        monitoring_setup = "app.middleware(\"http\")(monitoring_middleware)\n"
        
        # Find the right place to add the import (after other imports)
        lines = content.split('\n')
        import_end_index = 0
        
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                import_end_index = i + 1
            elif line.strip() and not line.strip().startswith('#'):
                break
        
        # Insert monitoring import
        lines.insert(import_end_index, monitoring_import)
        
        # Find the right place to add middleware setup (after app creation)
        app_creation_index = -1
        for i, line in enumerate(lines):
            if 'app = FastAPI(' in line or 'app = FastAPI()' in line:
                app_creation_index = i
                break
        
        if app_creation_index != -1:
            # Find the end of app configuration
            setup_index = app_creation_index + 1
            for i in range(app_creation_index + 1, len(lines)):
                if lines[i].strip() and not lines[i].strip().startswith('#'):
                    setup_index = i + 1
                    break
            
            lines.insert(setup_index, monitoring_setup)
        
        # Write back to file
        with open(app_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Monitoring middleware configured successfully!")
        return True
        
    except Exception as e:
        print(f"⚠️  Warning: Could not set up monitoring middleware: {e}")
        print("   Monitoring will be disabled. Continuing startup...")
        return True  # Don't fail startup for monitoring issues

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'loguru',
        'openai',
        'google.generativeai',
        'anthropic',
        'mistralai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        return install_requirements()
    else:
        print("\n✅ All dependencies are available!")
        return True

def setup_environment():
    """Set up the environment for the backend."""
    print("🔧 Setting up environment...")
    
    # Create necessary directories
    directories = [
        "lib/workspace/alwrity_content",
        "lib/workspace/alwrity_web_research", 
        "lib/workspace/alwrity_prompts",
        "lib/workspace/alwrity_config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created directory: {directory}")
    
    # Create .env file if it doesn't exist
    create_env_file()
    
    # Set up monitoring
    setup_monitoring_tables()
    setup_monitoring_middleware()
    
    print("✅ Environment setup complete")

def start_backend():
    """Start the backend server."""
    print("🚀 Starting ALwrity Backend...")
    
    # Set environment variables
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("PORT", "8000")
    os.environ.setdefault("RELOAD", "true")
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"   📍 Host: {host}")
    print(f"   🔌 Port: {port}")
    print(f"   🔄 Reload: {reload}")
    
    try:
        # Import and run the app
        from app import app
        import uvicorn
        
        print("\n🌐 Backend is starting...")
        print("   📖 API Documentation: http://localhost:8000/api/docs")
        print("   🔍 Health Check: http://localhost:8000/health")
        print("   📊 ReDoc: http://localhost:8000/api/redoc")
        print("   📈 API Monitoring: http://localhost:8000/api/content-planning/monitoring/health")
        print("\n⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        
        uvicorn.run(
            "app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Backend stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting backend: {e}")
        return False
    
    return True

def main():
    """Main function to set up and start the backend."""
    print("🎯 ALwrity Backend Server")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the backend directory.")
        print("   Current directory:", os.getcwd())
        print("   Expected files:", [f for f in os.listdir('.') if f.endswith('.py')])
        return False
    
    # Check and install dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Setup environment
    setup_environment()
    
    # Start backend
    return start_backend()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 