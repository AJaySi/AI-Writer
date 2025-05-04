"""
Enhanced FAQ Generator

This module provides a comprehensive FAQ generation system that can create detailed,
well-researched FAQs from various content sources with customizable options.
"""

import sys
import json
from typing import Dict, List, Optional, Union
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from loguru import logger

from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.ai_web_researcher.google_serp_search import google_search
from lib.ai_web_researcher.tavily_ai_search import tavily_search
from lib.ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles

logger.remove()
logger.add(sys.stdout,
          colorize=True,
          format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

class TargetAudience(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

class FAQStyle(Enum):
    TECHNICAL = "technical"
    CONVERSATIONAL = "conversational"
    PROFESSIONAL = "professional"

class SearchDepth(Enum):
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    EXPERT = "expert"

@dataclass
class FAQConfig:
    """Configuration for FAQ generation."""
    num_faqs: int = 5
    target_audience: TargetAudience = TargetAudience.INTERMEDIATE
    faq_style: FAQStyle = FAQStyle.PROFESSIONAL
    include_emojis: bool = True
    include_code_examples: bool = True
    include_references: bool = True
    search_depth: SearchDepth = SearchDepth.COMPREHENSIVE
    time_range: str = "last_6_months"
    exclude_domains: List[str] = None
    language: str = "English"

@dataclass
class FAQItem:
    """Individual FAQ item with metadata."""
    question: str
    answer: str
    category: str
    code_example: Optional[str] = None
    references: List[Dict[str, str]] = None
    confidence_score: float = 0.0
    last_updated: str = None

class FAQGenerator:
    """Enhanced FAQ Generator with research capabilities."""
    
    def __init__(self, config: Optional[FAQConfig] = None):
        """Initialize the FAQ generator with optional configuration."""
        self.config = config or FAQConfig()
        self.faqs: List[FAQItem] = []
        self.research_results = {}
        
    async def generate_faqs(self, content: str, content_type: str = "general") -> List[FAQItem]:
        """Generate FAQs from the given content with research integration."""
        try:
            # Step 1: Research the topic
            research_results = await self._conduct_research(content)
            
            # Step 2: Generate initial FAQs
            initial_faqs = await self._generate_initial_faqs(content, research_results)
            
            # Step 3: Enhance FAQs with research
            enhanced_faqs = await self._enhance_faqs_with_research(initial_faqs, research_results)
            
            # Step 4: Add code examples if requested
            if self.config.include_code_examples:
                enhanced_faqs = await self._add_code_examples(enhanced_faqs)
            
            # Step 5: Add references if requested
            if self.config.include_references:
                enhanced_faqs = await self._add_references(enhanced_faqs, research_results)
            
            self.faqs = enhanced_faqs
            return enhanced_faqs
            
        except Exception as err:
            logger.error(f"Failed to generate FAQs: {err}")
            raise
    
    async def _conduct_research(self, content: str) -> Dict:
        """Conduct online research based on the content."""
        try:
            research_prompt = f"""Based on the following content, identify key topics and questions for research:
            {content}
            
            Please provide a list of research topics and questions that would help create comprehensive FAQs.
            Focus on:
            1. Key concepts and terms
            2. Common questions users might have
            3. Technical aspects that need clarification
            4. Best practices and recommendations
            """
            
            research_topics = await llm_text_gen(research_prompt)
            
            # Conduct research for each topic
            research_results = {}
            for topic in research_topics.split('\n'):
                if topic.strip():
                    # Select search function based on search depth
                    if self.config.search_depth == SearchDepth.BASIC:
                        results = await google_search(topic.strip())
                    elif self.config.search_depth == SearchDepth.COMPREHENSIVE:
                        results = await tavily_search(topic.strip())
                    elif self.config.search_depth == SearchDepth.EXPERT:
                        results = await metaphor_search_articles(topic.strip())
                    else:
                        logger.warning(f"Unknown search depth: {self.config.search_depth}, defaulting to Google search")
                        results = await google_search(topic.strip())
                    
                    research_results[topic.strip()] = results
            
            return research_results
            
        except Exception as err:
            logger.error(f"Failed to conduct research: {err}")
            return {}
    
    async def _generate_initial_faqs(self, content: str, research_results: Dict) -> List[FAQItem]:
        """Generate initial FAQs using LLM."""
        try:
            system_prompt = f"""You are an expert FAQ generator with deep knowledge in content creation and technical writing.
            Your task is to create comprehensive FAQs based on the given content and research.

            Guidelines:
            1. Target Audience: {self.config.target_audience.value}
            2. Style: {self.config.faq_style.value}
            3. Include emojis: {self.config.include_emojis}
            4. Language: {self.config.language}
            5. Number of FAQs: {self.config.num_faqs}

            Create FAQs that are:
            - Clear and concise
            - Well-structured
            - Technically accurate
            - Engaging and informative
            - Based on the provided research
            - Relevant to the target audience
            - Written in the specified style
            """
            
            prompt = f"""Content to generate FAQs from:
            {content}

            Research Results:
            {json.dumps(research_results, indent=2)}

            Please generate {self.config.num_faqs} FAQs following the guidelines above.
            Format each FAQ with:
            - Question
            - Detailed answer
            - Category
            - Confidence score (0-1)
            """
            
            response = await llm_text_gen(prompt, system_prompt=system_prompt)
            
            # Parse the response into FAQItem objects
            faqs = []
            current_faq = None
            
            for line in response.split('\n'):
                if line.startswith('Q:'):
                    if current_faq:
                        faqs.append(current_faq)
                    current_faq = FAQItem(question=line[2:].strip(), answer="", category="")
                elif line.startswith('A:'):
                    if current_faq:
                        current_faq.answer = line[2:].strip()
                elif line.startswith('Category:'):
                    if current_faq:
                        current_faq.category = line[9:].strip()
                elif line.startswith('Confidence:'):
                    if current_faq:
                        current_faq.confidence_score = float(line[11:].strip())
            
            if current_faq:
                faqs.append(current_faq)
            
            return faqs
            
        except Exception as err:
            logger.error(f"Failed to generate initial FAQs: {err}")
            raise
    
    async def _enhance_faqs_with_research(self, faqs: List[FAQItem], research_results: Dict) -> List[FAQItem]:
        """Enhance FAQs with research findings."""
        try:
            enhanced_faqs = []
            
            for faq in faqs:
                # Find relevant research for this FAQ
                relevant_research = self._find_relevant_research(faq, research_results)
                
                if relevant_research:
                    # Enhance the answer with research findings
                    enhancement_prompt = f"""Enhance the following FAQ answer with the provided research:
                    
                    Question: {faq.question}
                    Current Answer: {faq.answer}
                    
                    Research:
                    {json.dumps(relevant_research, indent=2)}
                    
                    Please enhance the answer while:
                    1. Maintaining the original style and tone
                    2. Adding relevant information from the research
                    3. Ensuring technical accuracy
                    4. Keeping the answer concise and clear
                    """
                    
                    enhanced_answer = await llm_text_gen(enhancement_prompt)
                    faq.answer = enhanced_answer
                
                enhanced_faqs.append(faq)
            
            return enhanced_faqs
            
        except Exception as err:
            logger.error(f"Failed to enhance FAQs with research: {err}")
            return faqs
    
    async def _add_code_examples(self, faqs: List[FAQItem]) -> List[FAQItem]:
        """Add code examples to FAQs where applicable."""
        try:
            for faq in faqs:
                if self._is_technical_question(faq.question):
                    code_prompt = f"""Generate a code example for the following FAQ:
                    
                    Question: {faq.question}
                    Answer: {faq.answer}
                    
                    Please provide a relevant code example that:
                    1. Illustrates the answer clearly
                    2. Includes comments and explanations
                    3. Follows best practices
                    4. Is easy to understand
                    """
                    
                    code_example = await llm_text_gen(code_prompt)
                    faq.code_example = code_example
            
            return faqs
            
        except Exception as err:
            logger.error(f"Failed to add code examples: {err}")
            return faqs
    
    async def _add_references(self, faqs: List[FAQItem], research_results: Dict) -> List[FAQItem]:
        """Add references to FAQs."""
        try:
            for faq in faqs:
                relevant_research = self._find_relevant_research(faq, research_results)
                if relevant_research:
                    faq.references = [
                        {
                            "title": ref.get("title", ""),
                            "url": ref.get("url", ""),
                            "source": ref.get("source", ""),
                            "date": ref.get("date", "")
                        }
                        for ref in relevant_research.get("references", [])
                    ]
            
            return faqs
            
        except Exception as err:
            logger.error(f"Failed to add references: {err}")
            return faqs
    
    def _find_relevant_research(self, faq: FAQItem, research_results: Dict) -> Dict:
        """Find research relevant to a specific FAQ."""
        # Simple keyword matching for now - can be enhanced with semantic search
        relevant_research = {}
        for topic, results in research_results.items():
            if any(keyword in faq.question.lower() for keyword in topic.lower().split()):
                relevant_research[topic] = results
        return relevant_research
    
    def _is_technical_question(self, question: str) -> bool:
        """Determine if a question is technical and might benefit from a code example."""
        technical_keywords = ["code", "program", "function", "method", "class", "api", "syntax", "error", "debug"]
        return any(keyword in question.lower() for keyword in technical_keywords)
    
    def to_markdown(self) -> str:
        """Convert FAQs to markdown format."""
        markdown = "# Frequently Asked Questions\n\n"
        
        for i, faq in enumerate(self.faqs, 1):
            markdown += f"## {i}. {faq.question}\n\n"
            markdown += f"{faq.answer}\n\n"
            
            if faq.code_example:
                markdown += "```\n"
                markdown += f"{faq.code_example}\n"
                markdown += "```\n\n"
            
            if faq.references:
                markdown += "### References\n"
                for ref in faq.references:
                    markdown += f"- [{ref['title']}]({ref['url']}) - {ref['source']} ({ref['date']})\n"
                markdown += "\n"
        
        return markdown
    
    def to_html(self) -> str:
        """Convert FAQs to HTML format."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Frequently Asked Questions</title>
            <style>
                .faq-container { max-width: 800px; margin: 0 auto; }
                .faq-item { margin-bottom: 2em; }
                .question { font-weight: bold; font-size: 1.2em; }
                .answer { margin: 1em 0; }
                .code-example { background: #f5f5f5; padding: 1em; }
                .references { margin-top: 1em; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="faq-container">
                <h1>Frequently Asked Questions</h1>
        """
        
        for i, faq in enumerate(self.faqs, 1):
            html += f"""
                <div class="faq-item">
                    <div class="question">{i}. {faq.question}</div>
                    <div class="answer">{faq.answer}</div>
            """
            
            if faq.code_example:
                html += f"""
                    <pre class="code-example">{faq.code_example}</pre>
                """
            
            if faq.references:
                html += """
                    <div class="references">
                        <h3>References</h3>
                        <ul>
                """
                for ref in faq.references:
                    html += f"""
                            <li><a href="{ref['url']}">{ref['title']}</a> - {ref['source']} ({ref['date']})</li>
                    """
                html += """
                        </ul>
                    </div>
                """
            
            html += """
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
