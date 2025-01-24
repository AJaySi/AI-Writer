# AI Agents Content Planner

This document describes the `ai_agents_planner` module, a sophisticated tool for creating highly detailed and SEO-optimized content calendars. This module leverages AI agents to perform web research, trend analysis, and content planning.

## Prerequisites

To use this module, ensure the following are installed:
- Python 3.6 or higher
- Streamlit
- Crewai
- Crewai Tools
- Langchain Google GenAI
- Google Gemini API key

## Installation

Install the required Python packages using pip:

```bash
pip install streamlit crewai crewai_tools langchain_google_genai
```

## Environment Setup

Ensure that you have set up the following environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key.
- `SEARCH_SAVE_FILE`: Path to the file where search results are saved.

## Module Overview

The `ai_agents_planner` module consists of several key functions:

- **create_agents(search_keywords, already_written_on)**
  - This function creates the AI agents required for content research and planning. Each agent is assigned a specific role and set of tools to achieve their goals.
  - Agents:
    - **content_researcher**: Conducts web research to identify content opportunities.
    - **content_planner**: Develops a content calendar based on the research.
    - **google_trends_researcher**: Analyzes Google Trends data to suggest relevant keywords and titles.
    - **content_marketing_manager**: Ensures the content calendar is optimized and avoids keyword cannibalization.

- **create_tasks(agents, search_keywords, already_written_on)**
  - This function creates tasks for each agent, including web analysis, Google Trends analysis, content calendar development, and final review.

- **execute_tasks(agents, tasks)**
  - Executes the tasks assigned to each agent. The results are compiled into a comprehensive content calendar.

- **ai_agents_planner(search_keywords)**
  - The main function that orchestrates the creation of agents, assignment of tasks, and execution of the content planning process. It performs Google Trends analysis and generates the final content calendar.

## Example Usage

To use the `ai_agents_planner` module, follow these steps:

1. Set up the environment variables.
2. Import the module and call the `ai_agents_planner` function with your target keywords.

```python
import os
from your_module import ai_agents_planner

# Set up environment variables
os.environ['GEMINI_API_KEY'] = 'your_google_gemini_api_key'
os.environ['SEARCH_SAVE_FILE'] = '/path/to/search_save_file.txt'

# Run the planner
ai_agents_planner('your_target_keywords')
```

## Detailed Agent Roles and Responsibilities

### Content Researcher: Aisha Sharma
**Role**: Senior Web Research Analyst (Content Strategy)  
**Goal**: Create a detailed content calendar focused on specific keywords.  
**Responsibilities**:
- Conduct web research and competitor analysis.
- Identify high-value content opportunities.

### Content Planner: Ted XingPi
**Role**: Senior Content Strategist & Planner  
**Goal**: Craft a series of content titles for a 2-month-long series.  
**Responsibilities**:
- Develop a content calendar with unique and non-repetitive titles.
- Ensure alignment with SEO best practices.

### Google Trends Researcher: Sarah Qureshi
**Role**: Content Marketing & Google Trends Specialist  
**Goal**: Analyze Google Trends data and provide keyword recommendations.  
**Responsibilities**:
- Identify high-volume, low-competition keywords.
- Collaborate on content strategy and planning.

### Content Marketing Manager: Diksha Yuj
**Role**: Content Marketing Manager  
**Goal**: Optimize the content calendar and ensure no keyword cannibalization.  
**Responsibilities**:
- Review and finalize the content calendar.
- Ensure all content is unique and SEO-optimized.

## Final Content Calendar

The result of the `ai_agents_planner` module is a highly detailed content calendar that positions your target keywords effectively. The content calendar includes:
- Head Term Keyword
- Long-Tail Keyword
- Blog Post Title

This structured approach ensures a comprehensive content strategy, optimized for search engines and tailored to your audience.

## Conclusion

The `ai_agents_planner` module provides a robust framework for content planning and strategy. By leveraging AI agents and integrating web research, trend analysis, and content planning, it delivers a detailed content calendar tailored to your audience and optimized for search engines.

For further information and detailed documentation, refer to the module's code and comments.
