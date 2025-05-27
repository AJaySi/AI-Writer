# ALwrity Installation for Mac Users

## Prerequisites
- macOS 10.15 or later
- Terminal access
- Internet connection

## Installation Methods

### Method 1: Easy Setup (Recommended)
1. Open Terminal
2. Navigate to this directory
3. Run: `python setup.py`
4. Follow the on-screen instructions

### Method 2: Docker Installation
1. Install Docker Desktop for Mac
   - Visit [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Download and install the Apple Silicon (M1/M2) or Intel version
2. Build and run:
   ```bash
   docker build -t alwrity .
   docker run -p 8501:8501 alwrity