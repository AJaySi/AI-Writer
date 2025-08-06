"""Research Utilities Service for ALwrity Backend.

This service handles research functionality and result processing,
extracted from the legacy AI research utilities.
"""

from typing import Dict, Any, List, Optional
from loguru import logger
import asyncio
from datetime import datetime

class ResearchUtilities:
    """Business logic for research functionality and result processing."""
    
    def __init__(self):
        """Initialize the Research Utilities service."""
        self.research_providers = {
            'tavily': 'TAVILY_API_KEY',
            'serper': 'SERPER_API_KEY',
            'metaphor': 'METAPHOR_API_KEY',
            'firecrawl': 'FIRECRAWL_API_KEY'
        }
    
    async def research_topic(self, topic: str, api_keys: Dict[str, str]) -> Dict[str, Any]:
        """
        Research a topic using available AI services.
        
        Args:
            topic: The topic to research
            api_keys: Dictionary of API keys for different services
            
        Returns:
            Dict containing research results and metadata
        """
        try:
            logger.info(f"Starting research on topic: {topic}")
            
            # Validate topic
            if not topic or len(topic.strip()) < 3:
                return {
                    'success': False,
                    'topic': topic,
                    'error': 'Topic must be at least 3 characters long'
                }
            
            # Check available API keys
            available_providers = []
            for provider, key_name in self.research_providers.items():
                if api_keys.get(key_name):
                    available_providers.append(provider)
            
            if not available_providers:
                return {
                    'success': False,
                    'topic': topic,
                    'error': 'No research providers available. Please configure API keys.'
                }
            
            # Simulate research processing (in real implementation, this would call actual AI services)
            research_results = await self._simulate_research(topic, available_providers)
            
            logger.info(f"Research completed successfully for topic: {topic}")
            
            return {
                'success': True,
                'topic': topic,
                'results': research_results,
                'metadata': {
                    'providers_used': available_providers,
                    'research_timestamp': datetime.now().isoformat(),
                    'topic_length': len(topic)
                }
            }
            
        except Exception as e:
            logger.error(f"Error during research: {str(e)}")
            return {
                'success': False,
                'topic': topic,
                'error': str(e)
            }
    
    async def _simulate_research(self, topic: str, providers: List[str]) -> Dict[str, Any]:
        """
        Simulate research processing for demonstration purposes.
        In real implementation, this would call actual AI research services.
        
        Args:
            topic: The research topic
            providers: List of available research providers
            
        Returns:
            Dict containing simulated research results
        """
        # Simulate async processing time
        await asyncio.sleep(0.1)
        
        # Generate simulated research results
        results = {
            'summary': f"Comprehensive research summary for '{topic}' based on multiple sources.",
            'key_points': [
                f"Key insight 1 about {topic}",
                f"Important finding 2 related to {topic}",
                f"Notable trend 3 in {topic}",
                f"Critical observation 4 regarding {topic}"
            ],
            'sources': [
                f"Research source 1 for {topic}",
                f"Academic paper on {topic}",
                f"Industry report about {topic}",
                f"Expert analysis of {topic}"
            ],
            'trends': [
                f"Emerging trend in {topic}",
                f"Growing interest in {topic}",
                f"Market shift related to {topic}"
            ],
            'recommendations': [
                f"Action item 1 for {topic}",
                f"Strategic recommendation for {topic}",
                f"Next steps regarding {topic}"
            ],
            'providers_used': providers,
            'research_depth': 'comprehensive',
            'confidence_score': 0.85
        }
        
        return results
    
    def process_research_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and format research results for better presentation.
        
        Args:
            results: Raw research results
            
        Returns:
            Dict containing processed and formatted results
        """
        try:
            logger.info("Processing research results")
            
            if not results or 'success' not in results:
                return {
                    'success': False,
                    'error': 'Invalid research results format'
                }
            
            if not results.get('success', False):
                return results  # Return error results as-is
            
            # Process successful results
            raw_results = results.get('results', {})
            metadata = results.get('metadata', {})
            
            # Format and structure the results
            processed_results = {
                'topic': results.get('topic', ''),
                'summary': raw_results.get('summary', ''),
                'key_insights': raw_results.get('key_points', []),
                'sources': raw_results.get('sources', []),
                'trends': raw_results.get('trends', []),
                'recommendations': raw_results.get('recommendations', []),
                'metadata': {
                    'providers_used': raw_results.get('providers_used', []),
                    'research_depth': raw_results.get('research_depth', 'standard'),
                    'confidence_score': raw_results.get('confidence_score', 0.0),
                    'processed_at': datetime.now().isoformat(),
                    'original_timestamp': metadata.get('research_timestamp')
                }
            }
            
            logger.info("Research results processed successfully")
            
            return {
                'success': True,
                'processed_results': processed_results
            }
            
        except Exception as e:
            logger.error(f"Error processing research results: {str(e)}")
            return {
                'success': False,
                'error': f"Results processing error: {str(e)}"
            }
    
    def validate_research_request(self, topic: str, api_keys: Dict[str, str]) -> Dict[str, Any]:
        """
        Validate a research request before processing.
        
        Args:
            topic: The research topic
            api_keys: Available API keys
            
        Returns:
            Dict containing validation results
        """
        try:
            logger.info(f"Validating research request for topic: {topic}")
            
            errors = []
            warnings = []
            
            # Validate topic
            if not topic or len(topic.strip()) < 3:
                errors.append("Topic must be at least 3 characters long")
            elif len(topic.strip()) > 500:
                errors.append("Topic is too long (maximum 500 characters)")
            
            # Check API keys
            available_providers = []
            for provider, key_name in self.research_providers.items():
                if api_keys.get(key_name):
                    available_providers.append(provider)
                else:
                    warnings.append(f"No API key for {provider}")
            
            if not available_providers:
                errors.append("No research providers available. Please configure at least one API key.")
            
            # Determine validation result
            is_valid = len(errors) == 0
            
            return {
                'valid': is_valid,
                'errors': errors,
                'warnings': warnings,
                'available_providers': available_providers,
                'topic_length': len(topic.strip()) if topic else 0
            }
            
        except Exception as e:
            logger.error(f"Error validating research request: {str(e)}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': [],
                'available_providers': [],
                'topic_length': 0
            }
    
    def get_research_providers_info(self) -> Dict[str, Any]:
        """
        Get information about available research providers.
        
        Returns:
            Dict containing provider information
        """
        return {
            'providers': {
                'tavily': {
                    'name': 'Tavily',
                    'description': 'Intelligent web research',
                    'api_key_name': 'TAVILY_API_KEY',
                    'url': 'https://tavily.com/#api'
                },
                'serper': {
                    'name': 'Serper',
                    'description': 'Google search functionality',
                    'api_key_name': 'SERPER_API_KEY',
                    'url': 'https://serper.dev/signup'
                },
                'metaphor': {
                    'name': 'Metaphor',
                    'description': 'Advanced web search',
                    'api_key_name': 'METAPHOR_API_KEY',
                    'url': 'https://dashboard.exa.ai/login'
                },
                'firecrawl': {
                    'name': 'Firecrawl',
                    'description': 'Web content extraction',
                    'api_key_name': 'FIRECRAWL_API_KEY',
                    'url': 'https://www.firecrawl.dev/account'
                }
            },
            'total_providers': len(self.research_providers)
        }
    
    def generate_research_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a formatted research report from processed results.
        
        Args:
            results: Processed research results
            
        Returns:
            Dict containing formatted research report
        """
        try:
            logger.info("Generating research report")
            
            if not results.get('success', False):
                return {
                    'success': False,
                    'error': 'Cannot generate report from failed research'
                }
            
            processed_results = results.get('processed_results', {})
            
            # Generate formatted report
            report = {
                'title': f"Research Report: {processed_results.get('topic', 'Unknown Topic')}",
                'executive_summary': processed_results.get('summary', ''),
                'key_findings': processed_results.get('key_insights', []),
                'trends_analysis': processed_results.get('trends', []),
                'recommendations': processed_results.get('recommendations', []),
                'sources': processed_results.get('sources', []),
                'metadata': processed_results.get('metadata', {}),
                'generated_at': datetime.now().isoformat(),
                'report_format': 'structured'
            }
            
            logger.info("Research report generated successfully")
            
            return {
                'success': True,
                'report': report
            }
            
        except Exception as e:
            logger.error(f"Error generating research report: {str(e)}")
            return {
                'success': False,
                'error': f"Report generation error: {str(e)}"
            } 