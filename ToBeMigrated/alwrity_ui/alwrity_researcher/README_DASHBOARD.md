# AI Web Researcher Dashboard

## Overview

The AI Web Researcher Dashboard is a modern, intuitive interface designed specifically for content creators and digital marketing professionals. This dashboard integrates various web research tools to streamline the content research process, enhance content quality, and improve workflow efficiency.

## Features

### 1. Intuitive User Interface
- Modern, colorful, and professional design
- Easy navigation through different research tools
- Responsive layout that works on various screen sizes

### 2. Integrated Research Tools
- **Search Engine Research**: Google SERP Search and Tavily AI Search
- **Neural Search**: Metaphor Neural Search for finding conceptually similar content
- **Trend Analysis**: Google Trends Researcher for analyzing search term popularity
- **Web Crawling & Analysis**: Tools for extracting and analyzing web content

### 3. Guided Research Workflows
- Comprehensive Topic Research workflow
- Content Gap Analysis workflow
- Content Refresh & Update workflow

## Installation

1. Ensure you have Python 3.8+ installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the necessary API keys in your environment variables or .env file

## Usage

1. Navigate to the dashboard directory:
   ```
   cd AI-Writer/lib/alwrity_ui/alwrity_researcher
   ```

2. Run the dashboard:
   ```
   python -m streamlit run main.py
   ```

3. Access the dashboard in your web browser at http://localhost:8501

## Dashboard Sections

### Dashboard Home
Provides an overview of available research tools and featured workflows.

### Search Tools
Access to Google SERP Search and Tavily AI Search for comprehensive search capabilities.

### Neural Search
Use Metaphor Neural Search to find content based on conceptual similarity rather than keyword matching.

### Trend Analysis
Analyze search term popularity over time using Google Trends Researcher.

### Web Crawling
Extract structured content from websites using various web crawling tools.

### Research Workflows
Guided workflows that combine multiple tools for specific research objectives.

## Current Implementation Status

This is the initial implementation of the dashboard with placeholder functionality. The UI is fully implemented, but the actual integration with the AI web research modules will be completed in the next phase.

### What's Implemented
- Complete user interface with all sections and forms
- Mock data visualization for demonstration purposes
- Placeholder functionality for all research tools

### Next Steps
- Integrate with actual AI web research modules
- Implement data processing and visualization with real data
- Add user authentication and result saving functionality

## Technical Details

- Built with Streamlit for rapid UI development
- Modular design for easy extension and maintenance
- Responsive layout that works on desktop and mobile devices

## File Structure

- `main.py`: Entry point for the application
- `dashboard.py`: Main dashboard implementation
- `utils.py`: Utility functions for data processing and visualization
- `style.css`: Custom CSS for styling the dashboard
- `requirements.txt`: Required Python packages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.