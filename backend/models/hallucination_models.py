"""Pydantic models for hallucination detection API."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum


class HallucinationAssessment(str, Enum):
    """Possible assessments for claim verification."""
    SUPPORTED = "supported"
    REFUTED = "refuted"
    INSUFFICIENT_INFORMATION = "insufficient_information"
    PARTIALLY_SUPPORTED = "partially_supported"


class TextInput(BaseModel):
    """Input model for text to be analyzed for hallucinations."""
    text: str = Field(..., description="The text content to analyze for factual claims and potential hallucinations")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "The Eiffel Tower was built in 1889 and stands 324 meters tall. It was designed by Gustave Eiffel and is located in Berlin, Germany."
            }
        }


class SourceDocument(BaseModel):
    """Model representing a source document used for verification."""
    url: str = Field(..., description="URL of the source document")
    title: Optional[str] = Field(None, description="Title of the source document")
    text: str = Field(..., description="Relevant text content from the source")
    relevance_score: Optional[float] = Field(None, description="Relevance score of the source to the claim (0-1)")


class ClaimVerification(BaseModel):
    """Model representing the verification result of a single claim."""
    claim: str = Field(..., description="The extracted factual claim")
    assessment: HallucinationAssessment = Field(..., description="Assessment of the claim's veracity")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the assessment (0-1)")
    explanation: str = Field(..., description="Detailed explanation of the assessment")
    supporting_sources: List[SourceDocument] = Field(default=[], description="Sources that support the claim")
    refuting_sources: List[SourceDocument] = Field(default=[], description="Sources that refute the claim")
    
    class Config:
        schema_extra = {
            "example": {
                "claim": "The Eiffel Tower is located in Berlin, Germany",
                "assessment": "refuted",
                "confidence_score": 0.95,
                "explanation": "Multiple reliable sources confirm that the Eiffel Tower is located in Paris, France, not Berlin, Germany.",
                "supporting_sources": [],
                "refuting_sources": [
                    {
                        "url": "https://en.wikipedia.org/wiki/Eiffel_Tower",
                        "title": "Eiffel Tower - Wikipedia",
                        "text": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",
                        "relevance_score": 0.98
                    }
                ]
            }
        }


class HallucinationDetectionRequest(BaseModel):
    """Request model for hallucination detection."""
    text: str = Field(..., description="The text content to analyze")
    search_depth: Optional[int] = Field(default=5, ge=1, le=10, description="Number of sources to retrieve per claim")
    confidence_threshold: Optional[float] = Field(default=0.7, ge=0.0, le=1.0, description="Minimum confidence threshold for assessments")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "The Great Wall of China is visible from space with the naked eye. It was built entirely during the Ming Dynasty and stretches for exactly 21,196 kilometers.",
                "search_depth": 5,
                "confidence_threshold": 0.7
            }
        }


class HallucinationDetectionResponse(BaseModel):
    """Response model for hallucination detection results."""
    original_text: str = Field(..., description="The original text that was analyzed")
    total_claims: int = Field(..., description="Total number of claims extracted")
    claims_analysis: List[ClaimVerification] = Field(..., description="Detailed analysis of each claim")
    overall_assessment: Dict[str, Any] = Field(..., description="Overall assessment summary")
    processing_time: Optional[float] = Field(None, description="Time taken to process the request in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "original_text": "The Great Wall of China is visible from space...",
                "total_claims": 3,
                "claims_analysis": [
                    {
                        "claim": "The Great Wall of China is visible from space with the naked eye",
                        "assessment": "refuted",
                        "confidence_score": 0.92,
                        "explanation": "This is a common myth. Astronauts and space agencies have confirmed that the Great Wall is not visible from space with the naked eye.",
                        "supporting_sources": [],
                        "refuting_sources": [
                            {
                                "url": "https://www.nasa.gov/vision/space/workinginspace/great_wall.html",
                                "title": "NASA - The Great Wall of China",
                                "text": "The Great Wall of China is not visible from space with the naked eye.",
                                "relevance_score": 0.95
                            }
                        ]
                    }
                ],
                "overall_assessment": {
                    "hallucination_detected": True,
                    "accuracy_score": 0.33,
                    "total_supported": 1,
                    "total_refuted": 2,
                    "total_insufficient_info": 0
                },
                "processing_time": 12.45
            }
        }


class BatchHallucinationRequest(BaseModel):
    """Request model for batch hallucination detection."""
    texts: List[str] = Field(..., description="List of texts to analyze")
    search_depth: Optional[int] = Field(default=5, ge=1, le=10, description="Number of sources to retrieve per claim")
    confidence_threshold: Optional[float] = Field(default=0.7, ge=0.0, le=1.0, description="Minimum confidence threshold for assessments")
    
    class Config:
        schema_extra = {
            "example": {
                "texts": [
                    "The sun rises in the west and sets in the east.",
                    "Water boils at 100 degrees Celsius at sea level."
                ],
                "search_depth": 3,
                "confidence_threshold": 0.8
            }
        }


class BatchHallucinationResponse(BaseModel):
    """Response model for batch hallucination detection results."""
    results: List[HallucinationDetectionResponse] = Field(..., description="Results for each input text")
    batch_summary: Dict[str, Any] = Field(..., description="Summary statistics for the entire batch")
    total_processing_time: Optional[float] = Field(None, description="Total time taken to process all texts")
    
    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {
                        "original_text": "The sun rises in the west...",
                        "total_claims": 1,
                        "claims_analysis": [],
                        "overall_assessment": {},
                        "processing_time": 8.2
                    }
                ],
                "batch_summary": {
                    "total_texts_processed": 2,
                    "total_claims_analyzed": 3,
                    "average_accuracy_score": 0.65,
                    "texts_with_hallucinations": 1
                },
                "total_processing_time": 15.7
            }
        }


class HallucinationHealthCheck(BaseModel):
    """Health check response model for hallucination detection service."""
    status: str = Field(..., description="Service status")
    services_available: Dict[str, bool] = Field(..., description="Availability of required services")
    version: str = Field(..., description="Service version")
    timestamp: str = Field(..., description="Health check timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "services_available": {
                    "exa_search": True,
                    "openai_api": True,
                    "claim_extraction": True,
                    "verification_engine": True
                },
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }