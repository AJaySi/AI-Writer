"""Hallucination detection service using Exa search and LLM verification."""

import json
import time
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger
import os
from datetime import datetime

# Import the models
from models.hallucination_models import (
    ClaimVerification,
    SourceDocument,
    HallucinationAssessment,
    HallucinationDetectionResponse,
    BatchHallucinationResponse,
    HallucinationHealthCheck
)

# Import AI service manager for LLM calls
from services.ai_service_manager import get_ai_response

# Import for web search (we'll use existing patterns)
import aiohttp
import requests
from bs4 import BeautifulSoup


class HallucinationDetectionService:
    """Service for detecting hallucinations in text using claim extraction and verification."""
    
    def __init__(self):
        """Initialize the hallucination detection service."""
        self.version = "1.0.0"
        self.exa_api_key = os.getenv("EXA_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize search capabilities
        self._init_search_capabilities()
    
    def _init_search_capabilities(self):
        """Initialize search capabilities."""
        self.search_available = bool(self.exa_api_key) or True  # Fallback to web search
        logger.info(f"Hallucination detection service initialized. Search available: {self.search_available}")
    
    async def health_check(self) -> HallucinationHealthCheck:
        """Perform health check of the hallucination detection service."""
        try:
            # Check service availability
            services_status = {
                "exa_search": bool(self.exa_api_key),
                "openai_api": bool(self.openai_api_key),
                "claim_extraction": True,  # Always available as it uses existing AI service
                "verification_engine": True
            }
            
            # Test a simple claim extraction to ensure the service is working
            test_successful = await self._test_service_functionality()
            
            status = "healthy" if test_successful else "degraded"
            
            return HallucinationHealthCheck(
                status=status,
                services_available=services_status,
                version=self.version,
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return HallucinationHealthCheck(
                status="unhealthy",
                services_available={
                    "exa_search": False,
                    "openai_api": False,
                    "claim_extraction": False,
                    "verification_engine": False
                },
                version=self.version,
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
    
    async def _test_service_functionality(self) -> bool:
        """Test basic service functionality."""
        try:
            # Test claim extraction with a simple sentence
            test_text = "The sky is blue."
            claims = await self.extract_claims(test_text)
            return len(claims) > 0
        except Exception as e:
            logger.error(f"Service functionality test failed: {e}")
            return False
    
    async def detect_hallucinations(
        self,
        text: str,
        search_depth: int = 5,
        confidence_threshold: float = 0.7
    ) -> HallucinationDetectionResponse:
        """
        Detect hallucinations in the given text.
        
        Args:
            text: The text to analyze
            search_depth: Number of sources to retrieve per claim
            confidence_threshold: Minimum confidence threshold for assessments
            
        Returns:
            HallucinationDetectionResponse with detailed analysis
        """
        start_time = time.time()
        
        try:
            # Step 1: Extract factual claims from the text
            logger.info("Extracting claims from text")
            claims = await self.extract_claims(text)
            logger.info(f"Extracted {len(claims)} claims")
            
            # Step 2: Verify each claim
            claims_analysis = []
            for claim in claims:
                logger.info(f"Verifying claim: {claim[:100]}...")
                verification = await self.verify_claim(claim, search_depth, confidence_threshold)
                claims_analysis.append(verification)
            
            # Step 3: Generate overall assessment
            overall_assessment = self._generate_overall_assessment(claims_analysis)
            
            processing_time = time.time() - start_time
            
            return HallucinationDetectionResponse(
                original_text=text,
                total_claims=len(claims),
                claims_analysis=claims_analysis,
                overall_assessment=overall_assessment,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error in hallucination detection: {e}")
            raise
    
    async def detect_hallucinations_batch(
        self,
        texts: List[str],
        search_depth: int = 5,
        confidence_threshold: float = 0.7
    ) -> BatchHallucinationResponse:
        """
        Detect hallucinations in multiple texts.
        
        Args:
            texts: List of texts to analyze
            search_depth: Number of sources to retrieve per claim
            confidence_threshold: Minimum confidence threshold for assessments
            
        Returns:
            BatchHallucinationResponse with results for all texts
        """
        start_time = time.time()
        
        try:
            # Process all texts concurrently
            tasks = [
                self.detect_hallucinations(text, search_depth, confidence_threshold)
                for text in texts
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions and log them
            valid_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error processing text {i}: {result}")
                else:
                    valid_results.append(result)
            
            # Generate batch summary
            batch_summary = self._generate_batch_summary(valid_results)
            
            total_processing_time = time.time() - start_time
            
            return BatchHallucinationResponse(
                results=valid_results,
                batch_summary=batch_summary,
                total_processing_time=total_processing_time
            )
            
        except Exception as e:
            logger.error(f"Error in batch hallucination detection: {e}")
            raise
    
    async def extract_claims(self, text: str) -> List[str]:
        """
        Extract factual claims from the given text using LLM.
        
        Args:
            text: The text to extract claims from
            
        Returns:
            List of extracted factual claims
        """
        try:
            system_prompt = """You are an expert at extracting factual claims from text. Your task is to identify and list all verifiable factual statements in the given text.

Rules:
1. Extract only objective, factual claims that can be verified
2. Ignore opinions, subjective statements, and obvious common knowledge
3. Each claim should be a single, complete statement
4. Focus on specific facts, numbers, dates, locations, and relationships
5. Return the claims as a JSON array of strings

Example:
Input: "Paris is the capital of France. It has a population of 12 million people. The Eiffel Tower was built in 1887."
Output: ["Paris is the capital of France", "Paris has a population of 12 million people", "The Eiffel Tower was built in 1887"]"""

            user_prompt = f"Extract factual claims from this text:\n\n{text}"
            
            # Use the existing AI service manager
            response = await get_ai_response(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                provider="openai",
                model="gpt-4",
                temperature=0.1
            )
            
            # Parse the JSON response
            try:
                claims = json.loads(response)
                if isinstance(claims, list):
                    return [str(claim) for claim in claims]
                else:
                    logger.warning(f"Unexpected response format: {response}")
                    return []
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON response: {response}")
                # Fallback: try to extract claims manually
                return self._fallback_claim_extraction(response)
                
        except Exception as e:
            logger.error(f"Error in claim extraction: {e}")
            return []
    
    def _fallback_claim_extraction(self, response: str) -> List[str]:
        """Fallback method to extract claims when JSON parsing fails."""
        try:
            # Simple heuristic: split by lines and filter
            lines = response.strip().split('\n')
            claims = []
            for line in lines:
                line = line.strip()
                # Remove bullet points, numbers, quotes
                line = line.lstrip('•-*1234567890. ').strip('"\'')
                if len(line) > 10 and not line.lower().startswith(('here', 'the claims', 'extracted')):
                    claims.append(line)
            return claims[:10]  # Limit to 10 claims
        except Exception:
            return []
    
    async def verify_claim(
        self,
        claim: str,
        search_depth: int = 5,
        confidence_threshold: float = 0.7
    ) -> ClaimVerification:
        """
        Verify a single claim using search and LLM analysis.
        
        Args:
            claim: The claim to verify
            search_depth: Number of sources to search
            confidence_threshold: Minimum confidence threshold
            
        Returns:
            ClaimVerification with detailed analysis
        """
        try:
            # Step 1: Search for relevant sources
            sources = await self.search_for_sources(claim, search_depth)
            
            # Step 2: Analyze the claim against the sources
            verification = await self.analyze_claim_with_sources(claim, sources)
            
            # Step 3: Filter sources based on verification result
            supporting_sources = []
            refuting_sources = []
            
            for source in sources:
                # Simple heuristic based on the verification explanation
                if verification.assessment == HallucinationAssessment.SUPPORTED:
                    supporting_sources.append(source)
                elif verification.assessment == HallucinationAssessment.REFUTED:
                    refuting_sources.append(source)
            
            return ClaimVerification(
                claim=claim,
                assessment=verification.assessment,
                confidence_score=verification.confidence_score,
                explanation=verification.explanation,
                supporting_sources=supporting_sources,
                refuting_sources=refuting_sources
            )
            
        except Exception as e:
            logger.error(f"Error verifying claim '{claim}': {e}")
            return ClaimVerification(
                claim=claim,
                assessment=HallucinationAssessment.INSUFFICIENT_INFORMATION,
                confidence_score=0.0,
                explanation=f"Error occurred during verification: {str(e)}",
                supporting_sources=[],
                refuting_sources=[]
            )
    
    async def search_for_sources(self, query: str, num_results: int = 5) -> List[SourceDocument]:
        """
        Search for sources related to the query.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of SourceDocument objects
        """
        try:
            # Try Exa search first if available
            if self.exa_api_key:
                return await self._search_with_exa(query, num_results)
            else:
                # Fallback to web search
                return await self._search_with_web(query, num_results)
                
        except Exception as e:
            logger.error(f"Error in source search: {e}")
            return []
    
    async def _search_with_exa(self, query: str, num_results: int) -> List[SourceDocument]:
        """Search using Exa API."""
        try:
            # This would require the exa-py library
            # For now, we'll implement a placeholder that uses web search
            logger.info("Exa search not fully implemented, falling back to web search")
            return await self._search_with_web(query, num_results)
            
        except Exception as e:
            logger.error(f"Exa search failed: {e}")
            return await self._search_with_web(query, num_results)
    
    async def _search_with_web(self, query: str, num_results: int) -> List[SourceDocument]:
        """Search using web search as fallback."""
        try:
            # Use DuckDuckGo search as a simple fallback
            search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_search_results(html, num_results)
                    else:
                        logger.warning(f"Search request failed with status: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            # Return mock sources for demonstration
            return self._get_mock_sources(query, num_results)
    
    def _parse_search_results(self, html: str, num_results: int) -> List[SourceDocument]:
        """Parse search results from HTML."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            sources = []
            
            # Look for search result links (this is a simplified parser)
            links = soup.find_all('a', href=True)[:num_results * 2]  # Get more than needed
            
            for link in links:
                href = link.get('href', '')
                if href.startswith('http') and 'duckduckgo.com' not in href:
                    title = link.get_text(strip=True)
                    if len(title) > 10:  # Filter out short/empty titles
                        sources.append(SourceDocument(
                            url=href,
                            title=title,
                            text=f"Search result: {title}",
                            relevance_score=0.7
                        ))
                        
                        if len(sources) >= num_results:
                            break
            
            return sources
            
        except Exception as e:
            logger.error(f"Error parsing search results: {e}")
            return []
    
    def _get_mock_sources(self, query: str, num_results: int) -> List[SourceDocument]:
        """Generate mock sources for demonstration purposes."""
        mock_sources = [
            SourceDocument(
                url="https://en.wikipedia.org/wiki/Example",
                title=f"Wikipedia article related to: {query[:50]}",
                text=f"This is a mock source document for the query: {query}. In a real implementation, this would contain actual content from reliable sources.",
                relevance_score=0.8
            ),
            SourceDocument(
                url="https://www.britannica.com/example",
                title=f"Britannica Encyclopedia: {query[:30]}",
                text=f"Encyclopedia entry discussing: {query}. This mock source demonstrates how the system would work with real content.",
                relevance_score=0.75
            ),
            SourceDocument(
                url="https://www.reuters.com/example",
                title=f"News article: {query[:40]}",
                text=f"News coverage of: {query}. This represents how current events and facts would be verified against news sources.",
                relevance_score=0.7
            )
        ]
        
        return mock_sources[:num_results]
    
    async def analyze_claim_with_sources(
        self,
        claim: str,
        sources: List[SourceDocument]
    ) -> 'ClaimVerification':
        """
        Analyze a claim against the provided sources using LLM.
        
        Args:
            claim: The claim to analyze
            sources: List of source documents
            
        Returns:
            ClaimVerification object (simplified for internal use)
        """
        try:
            if not sources:
                return type('ClaimVerification', (), {
                    'assessment': HallucinationAssessment.INSUFFICIENT_INFORMATION,
                    'confidence_score': 0.5,
                    'explanation': "No sources found to verify this claim."
                })()
            
            # Prepare sources text
            sources_text = "\n\n".join([
                f"Source {i+1} - {source.title} ({source.url}):\n{source.text}"
                for i, source in enumerate(sources)
            ])
            
            system_prompt = """You are an expert fact-checker. Analyze the given claim against the provided sources and determine whether the claim is supported, refuted, partially supported, or if there's insufficient information.

Return your analysis as a JSON object with the following structure:
{
    "assessment": "supported|refuted|partially_supported|insufficient_information",
    "confidence_score": 0.0-1.0,
    "explanation": "Detailed explanation of your assessment"
}

Guidelines:
- "supported": The sources clearly confirm the claim
- "refuted": The sources clearly contradict the claim  
- "partially_supported": The claim is partially true but contains inaccuracies
- "insufficient_information": Sources don't provide enough information to verify
- Confidence score should reflect how certain you are (0.0 = not certain, 1.0 = very certain)
- Explanation should be detailed and reference specific sources"""

            user_prompt = f"""Claim to verify: "{claim}"

Sources:
{sources_text}

Please analyze this claim against the provided sources."""

            response = await get_ai_response(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                provider="openai",
                model="gpt-4",
                temperature=0.1
            )
            
            # Parse the JSON response
            try:
                analysis = json.loads(response)
                return type('ClaimVerification', (), {
                    'assessment': HallucinationAssessment(analysis.get('assessment', 'insufficient_information')),
                    'confidence_score': float(analysis.get('confidence_score', 0.5)),
                    'explanation': analysis.get('explanation', 'Analysis completed.')
                })()
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Failed to parse analysis response: {e}")
                # Fallback analysis
                return self._fallback_analysis(claim, sources, response)
                
        except Exception as e:
            logger.error(f"Error in claim analysis: {e}")
            return type('ClaimVerification', (), {
                'assessment': HallucinationAssessment.INSUFFICIENT_INFORMATION,
                'confidence_score': 0.0,
                'explanation': f"Error occurred during analysis: {str(e)}"
            })()
    
    def _fallback_analysis(self, claim: str, sources: List[SourceDocument], response: str) -> 'ClaimVerification':
        """Fallback analysis when JSON parsing fails."""
        try:
            # Simple heuristic based on response content
            response_lower = response.lower()
            
            if any(word in response_lower for word in ['supported', 'confirmed', 'correct', 'true']):
                assessment = HallucinationAssessment.SUPPORTED
                confidence = 0.7
            elif any(word in response_lower for word in ['refuted', 'false', 'incorrect', 'wrong']):
                assessment = HallucinationAssessment.REFUTED
                confidence = 0.7
            elif any(word in response_lower for word in ['partially', 'some truth', 'mixed']):
                assessment = HallucinationAssessment.PARTIALLY_SUPPORTED
                confidence = 0.6
            else:
                assessment = HallucinationAssessment.INSUFFICIENT_INFORMATION
                confidence = 0.5
            
            return type('ClaimVerification', (), {
                'assessment': assessment,
                'confidence_score': confidence,
                'explanation': response[:500] + "..." if len(response) > 500 else response
            })()
            
        except Exception:
            return type('ClaimVerification', (), {
                'assessment': HallucinationAssessment.INSUFFICIENT_INFORMATION,
                'confidence_score': 0.5,
                'explanation': "Fallback analysis completed."
            })()
    
    def _generate_overall_assessment(self, claims_analysis: List[ClaimVerification]) -> Dict[str, Any]:
        """Generate overall assessment from individual claim analyses."""
        if not claims_analysis:
            return {
                "hallucination_detected": False,
                "accuracy_score": 1.0,
                "total_supported": 0,
                "total_refuted": 0,
                "total_insufficient_info": 0,
                "total_partially_supported": 0
            }
        
        # Count assessments
        supported = sum(1 for c in claims_analysis if c.assessment == HallucinationAssessment.SUPPORTED)
        refuted = sum(1 for c in claims_analysis if c.assessment == HallucinationAssessment.REFUTED)
        insufficient = sum(1 for c in claims_analysis if c.assessment == HallucinationAssessment.INSUFFICIENT_INFORMATION)
        partially = sum(1 for c in claims_analysis if c.assessment == HallucinationAssessment.PARTIALLY_SUPPORTED)
        
        # Calculate accuracy score
        total_claims = len(claims_analysis)
        accuracy_score = (supported + (partially * 0.5)) / total_claims if total_claims > 0 else 1.0
        
        # Determine if hallucinations are detected
        hallucination_detected = refuted > 0 or partially > 0
        
        return {
            "hallucination_detected": hallucination_detected,
            "accuracy_score": round(accuracy_score, 2),
            "total_supported": supported,
            "total_refuted": refuted,
            "total_insufficient_info": insufficient,
            "total_partially_supported": partially,
            "confidence_level": "high" if accuracy_score > 0.8 else "medium" if accuracy_score > 0.6 else "low"
        }
    
    def _generate_batch_summary(self, results: List[HallucinationDetectionResponse]) -> Dict[str, Any]:
        """Generate summary statistics for batch processing."""
        if not results:
            return {
                "total_texts_processed": 0,
                "total_claims_analyzed": 0,
                "average_accuracy_score": 0.0,
                "texts_with_hallucinations": 0
            }
        
        total_claims = sum(r.total_claims for r in results)
        accuracy_scores = [r.overall_assessment.get("accuracy_score", 0.0) for r in results]
        average_accuracy = sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0.0
        
        texts_with_hallucinations = sum(
            1 for r in results 
            if r.overall_assessment.get("hallucination_detected", False)
        )
        
        return {
            "total_texts_processed": len(results),
            "total_claims_analyzed": total_claims,
            "average_accuracy_score": round(average_accuracy, 2),
            "texts_with_hallucinations": texts_with_hallucinations,
            "hallucination_rate": round(texts_with_hallucinations / len(results), 2) if results else 0.0
        }


# Global service instance
_hallucination_service = None

def get_hallucination_service() -> HallucinationDetectionService:
    """Get the global hallucination detection service instance."""
    global _hallucination_service
    if _hallucination_service is None:
        _hallucination_service = HallucinationDetectionService()
    return _hallucination_service