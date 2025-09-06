"""FastAPI router for hallucination detection endpoints."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from loguru import logger

# Import models
from models.hallucination_models import (
    HallucinationDetectionRequest,
    HallucinationDetectionResponse,
    BatchHallucinationRequest,
    BatchHallucinationResponse,
    TextInput,
    HallucinationHealthCheck
)

# Import service
from services.hallucination_detection_service import get_hallucination_service

# Create router
router = APIRouter(
    prefix="/api/hallucination-detection",
    tags=["Hallucination Detection"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)


@router.get("/health", response_model=HallucinationHealthCheck)
async def health_check():
    """
    Health check endpoint for hallucination detection service.
    
    Returns the current status of the service and its dependencies.
    """
    try:
        service = get_hallucination_service()
        health_status = await service.health_check()
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.post("/analyze", response_model=HallucinationDetectionResponse)
async def detect_hallucinations(request: HallucinationDetectionRequest):
    """
    Analyze text for potential hallucinations.
    
    This endpoint:
    1. Extracts factual claims from the provided text
    2. Searches for relevant sources to verify each claim
    3. Uses LLM analysis to determine if claims are supported or refuted
    4. Returns detailed analysis with confidence scores
    
    Args:
        request: HallucinationDetectionRequest containing text and optional parameters
        
    Returns:
        HallucinationDetectionResponse with detailed analysis results
        
    Example:
        ```json
        {
            "text": "The Eiffel Tower was built in 1889 and is located in Berlin, Germany.",
            "search_depth": 5,
            "confidence_threshold": 0.7
        }
        ```
    """
    try:
        logger.info(f"Processing hallucination detection request for text length: {len(request.text)}")
        
        service = get_hallucination_service()
        result = await service.detect_hallucinations(
            text=request.text,
            search_depth=request.search_depth,
            confidence_threshold=request.confidence_threshold
        )
        
        logger.info(f"Hallucination detection completed. Found {result.total_claims} claims.")
        return result
        
    except Exception as e:
        logger.error(f"Error in hallucination detection: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze text for hallucinations: {str(e)}"
        )


@router.post("/analyze-batch", response_model=BatchHallucinationResponse)
async def detect_hallucinations_batch(request: BatchHallucinationRequest):
    """
    Analyze multiple texts for potential hallucinations in batch.
    
    This endpoint processes multiple texts concurrently for efficient batch analysis.
    Each text is analyzed independently using the same process as the single analyze endpoint.
    
    Args:
        request: BatchHallucinationRequest containing list of texts and optional parameters
        
    Returns:
        BatchHallucinationResponse with results for all texts and batch summary
        
    Example:
        ```json
        {
            "texts": [
                "The sun rises in the west and sets in the east.",
                "Water boils at 100 degrees Celsius at sea level."
            ],
            "search_depth": 3,
            "confidence_threshold": 0.8
        }
        ```
    """
    try:
        if not request.texts:
            raise HTTPException(status_code=400, detail="No texts provided for analysis")
        
        if len(request.texts) > 50:  # Reasonable limit for batch processing
            raise HTTPException(status_code=400, detail="Too many texts. Maximum 50 texts per batch.")
        
        logger.info(f"Processing batch hallucination detection for {len(request.texts)} texts")
        
        service = get_hallucination_service()
        result = await service.detect_hallucinations_batch(
            texts=request.texts,
            search_depth=request.search_depth,
            confidence_threshold=request.confidence_threshold
        )
        
        logger.info(f"Batch hallucination detection completed for {len(result.results)} texts.")
        return result
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error in batch hallucination detection: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze texts for hallucinations: {str(e)}"
        )


@router.post("/extract-claims")
async def extract_claims(request: TextInput):
    """
    Extract factual claims from text without full verification.
    
    This is a lighter endpoint that only performs claim extraction,
    useful for understanding what claims would be verified in the full analysis.
    
    Args:
        request: TextInput containing the text to analyze
        
    Returns:
        Dictionary containing extracted claims
        
    Example:
        ```json
        {
            "text": "Paris is the capital of France with a population of 2.2 million people."
        }
        ```
    """
    try:
        logger.info(f"Extracting claims from text length: {len(request.text)}")
        
        service = get_hallucination_service()
        claims = await service.extract_claims(request.text)
        
        logger.info(f"Extracted {len(claims)} claims")
        return {
            "original_text": request.text,
            "claims": claims,
            "total_claims": len(claims)
        }
        
    except Exception as e:
        logger.error(f"Error in claim extraction: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract claims from text: {str(e)}"
        )


@router.post("/verify-claim")
async def verify_single_claim(
    claim: str,
    search_depth: int = 5,
    confidence_threshold: float = 0.7
):
    """
    Verify a single factual claim.
    
    This endpoint allows verification of individual claims without full text analysis,
    useful for targeted fact-checking or when claims are already known.
    
    Args:
        claim: The factual claim to verify
        search_depth: Number of sources to retrieve for verification
        confidence_threshold: Minimum confidence threshold for assessment
        
    Returns:
        ClaimVerification object with detailed analysis
        
    Example:
        POST /api/hallucination-detection/verify-claim?claim=The Eiffel Tower is in Paris&search_depth=3
    """
    try:
        if not claim or len(claim.strip()) < 10:
            raise HTTPException(status_code=400, detail="Claim must be at least 10 characters long")
        
        logger.info(f"Verifying single claim: {claim[:100]}...")
        
        service = get_hallucination_service()
        verification = await service.verify_claim(
            claim=claim.strip(),
            search_depth=search_depth,
            confidence_threshold=confidence_threshold
        )
        
        logger.info(f"Claim verification completed with assessment: {verification.assessment}")
        return verification
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error in single claim verification: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to verify claim: {str(e)}"
        )


@router.get("/demo")
async def demo_analysis():
    """
    Demonstration endpoint showing hallucination detection capabilities.
    
    Returns a pre-analyzed example to demonstrate the API functionality
    without requiring API keys or external services.
    
    Returns:
        Demo HallucinationDetectionResponse showing the service capabilities
    """
    try:
        demo_text = """The Great Wall of China is visible from space with the naked eye. 
        It was built entirely during the Ming Dynasty and stretches for exactly 21,196 kilometers. 
        The wall was constructed using modern concrete and steel materials."""
        
        # This could be a cached demo response or generated on-demand
        demo_response = {
            "original_text": demo_text,
            "total_claims": 4,
            "claims_analysis": [
                {
                    "claim": "The Great Wall of China is visible from space with the naked eye",
                    "assessment": "refuted",
                    "confidence_score": 0.92,
                    "explanation": "This is a common myth. Astronauts and space agencies have confirmed that the Great Wall is not visible from space with the naked eye without aid.",
                    "supporting_sources": [],
                    "refuting_sources": [
                        {
                            "url": "https://www.nasa.gov/vision/space/workinginspace/great_wall.html",
                            "title": "NASA - The Great Wall of China",
                            "text": "The Great Wall of China is not visible from space with the naked eye.",
                            "relevance_score": 0.95
                        }
                    ]
                },
                {
                    "claim": "It was built entirely during the Ming Dynasty",
                    "assessment": "refuted",
                    "confidence_score": 0.88,
                    "explanation": "The Great Wall was built over many dynasties, with significant construction during the Qin Dynasty (220-210 BC) and later reinforced during the Ming Dynasty.",
                    "supporting_sources": [],
                    "refuting_sources": [
                        {
                            "url": "https://en.wikipedia.org/wiki/Great_Wall_of_China",
                            "title": "Great Wall of China - Wikipedia",
                            "text": "The Great Wall was built over many dynasties, starting with the Warring States period.",
                            "relevance_score": 0.90
                        }
                    ]
                },
                {
                    "claim": "stretches for exactly 21,196 kilometers",
                    "assessment": "supported",
                    "confidence_score": 0.85,
                    "explanation": "Recent surveys by Chinese authorities have measured the total length of the Great Wall at approximately 21,196 kilometers.",
                    "supporting_sources": [
                        {
                            "url": "https://www.chinahighlights.com/great-wall/length.htm",
                            "title": "Great Wall Length - China Highlights",
                            "text": "The total length of the Great Wall is 21,196 kilometers according to recent surveys.",
                            "relevance_score": 0.92
                        }
                    ],
                    "refuting_sources": []
                },
                {
                    "claim": "The wall was constructed using modern concrete and steel materials",
                    "assessment": "refuted",
                    "confidence_score": 0.95,
                    "explanation": "The Great Wall was constructed using traditional materials like stone, brick, tamped earth, and wood. Modern concrete and steel were not available during its construction periods.",
                    "supporting_sources": [],
                    "refuting_sources": [
                        {
                            "url": "https://www.britannica.com/topic/Great-Wall-of-China",
                            "title": "Great Wall of China - Britannica",
                            "text": "The wall was built using stone, brick, tamped earth, and other traditional materials.",
                            "relevance_score": 0.93
                        }
                    ]
                }
            ],
            "overall_assessment": {
                "hallucination_detected": True,
                "accuracy_score": 0.25,
                "total_supported": 1,
                "total_refuted": 3,
                "total_insufficient_info": 0,
                "total_partially_supported": 0,
                "confidence_level": "high"
            },
            "processing_time": 12.45
        }
        
        return demo_response
        
    except Exception as e:
        logger.error(f"Error in demo analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Demo analysis failed: {str(e)}")


@router.get("/")
async def get_service_info():
    """
    Get information about the hallucination detection service.
    
    Returns:
        Service information including available endpoints and capabilities
    """
    return {
        "service": "Hallucination Detection API",
        "version": "1.0.0",
        "description": "AI-powered hallucination detection using claim extraction and verification",
        "endpoints": {
            "/analyze": "Analyze text for hallucinations",
            "/analyze-batch": "Batch analyze multiple texts",
            "/extract-claims": "Extract claims without verification",
            "/verify-claim": "Verify a single claim",
            "/demo": "Demonstration analysis",
            "/health": "Service health check"
        },
        "capabilities": [
            "Factual claim extraction from text",
            "Web search for verification sources",
            "LLM-powered claim verification",
            "Confidence scoring",
            "Batch processing",
            "Detailed explanations"
        ],
        "supported_languages": ["English"],
        "rate_limits": {
            "analyze": "10 requests per minute",
            "batch": "2 requests per minute",
            "max_batch_size": 50
        }
    }