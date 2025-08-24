"""
AI SEO Tools FastAPI Router

This module provides FastAPI endpoints for all AI SEO tools migrated from ToBeMigrated/ai_seo_tools.
Includes intelligent logging, exception handling, and structured responses.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl, Field, validator
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json
import traceback
from loguru import logger
import os
import tempfile
import asyncio

# Import services
from services.llm_providers.main_text_generation import llm_text_gen
from services.seo_tools.meta_description_service import MetaDescriptionService
from services.seo_tools.pagespeed_service import PageSpeedService
from services.seo_tools.sitemap_service import SitemapService
from services.seo_tools.image_alt_service import ImageAltService
from services.seo_tools.opengraph_service import OpenGraphService
from services.seo_tools.on_page_seo_service import OnPageSEOService
from services.seo_tools.technical_seo_service import TechnicalSEOService
from services.seo_tools.enterprise_seo_service import EnterpriseSEOService
from services.seo_tools.content_strategy_service import ContentStrategyService
from middleware.logging_middleware import log_api_call, save_to_file

router = APIRouter(prefix="/api/seo", tags=["AI SEO Tools"])

# Configuration for intelligent logging
LOG_DIR = "/workspace/backend/logs/seo_tools"
os.makedirs(LOG_DIR, exist_ok=True)

# Request/Response Models
class BaseResponse(BaseModel):
    """Base response model for all SEO tools"""
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    execution_time: Optional[float] = None
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseResponse):
    """Error response model"""
    error_type: str
    error_details: Optional[str] = None
    traceback: Optional[str] = None

class MetaDescriptionRequest(BaseModel):
    """Request model for meta description generation"""
    keywords: List[str] = Field(..., description="Target keywords for meta description")
    tone: str = Field(default="General", description="Desired tone for meta description")
    search_intent: str = Field(default="Informational Intent", description="Search intent type")
    language: str = Field(default="English", description="Preferred language")
    custom_prompt: Optional[str] = Field(None, description="Custom prompt for generation")
    
    @validator('keywords')
    def validate_keywords(cls, v):
        if not v or len(v) == 0:
            raise ValueError("At least one keyword is required")
        return v

class PageSpeedRequest(BaseModel):
    """Request model for PageSpeed Insights analysis"""
    url: HttpUrl = Field(..., description="URL to analyze")
    strategy: str = Field(default="DESKTOP", description="Analysis strategy (DESKTOP/MOBILE)")
    locale: str = Field(default="en", description="Locale for analysis")
    categories: List[str] = Field(default=["performance", "accessibility", "best-practices", "seo"])

class SitemapAnalysisRequest(BaseModel):
    """Request model for sitemap analysis"""
    sitemap_url: HttpUrl = Field(..., description="Sitemap URL to analyze")
    analyze_content_trends: bool = Field(default=True, description="Analyze content trends")
    analyze_publishing_patterns: bool = Field(default=True, description="Analyze publishing patterns")

class ImageAltRequest(BaseModel):
    """Request model for image alt text generation"""
    image_url: Optional[HttpUrl] = Field(None, description="URL of image to analyze")
    context: Optional[str] = Field(None, description="Context about the image")
    keywords: Optional[List[str]] = Field(None, description="Keywords to include in alt text")

class OpenGraphRequest(BaseModel):
    """Request model for OpenGraph tag generation"""
    url: HttpUrl = Field(..., description="URL for OpenGraph tags")
    title_hint: Optional[str] = Field(None, description="Hint for title")
    description_hint: Optional[str] = Field(None, description="Hint for description")
    platform: str = Field(default="General", description="Platform (General/Facebook/Twitter)")

class OnPageSEORequest(BaseModel):
    """Request model for on-page SEO analysis"""
    url: HttpUrl = Field(..., description="URL to analyze")
    target_keywords: Optional[List[str]] = Field(None, description="Target keywords for analysis")
    analyze_images: bool = Field(default=True, description="Include image analysis")
    analyze_content_quality: bool = Field(default=True, description="Analyze content quality")

class TechnicalSEORequest(BaseModel):
    """Request model for technical SEO analysis"""
    url: HttpUrl = Field(..., description="URL to crawl and analyze")
    crawl_depth: int = Field(default=3, description="Crawl depth (1-5)")
    include_external_links: bool = Field(default=True, description="Include external link analysis")
    analyze_performance: bool = Field(default=True, description="Include performance analysis")

class WorkflowRequest(BaseModel):
    """Request model for SEO workflow execution"""
    website_url: HttpUrl = Field(..., description="Primary website URL")
    workflow_type: str = Field(..., description="Type of workflow to execute")
    competitors: Optional[List[HttpUrl]] = Field(None, description="Competitor URLs (max 5)")
    target_keywords: Optional[List[str]] = Field(None, description="Target keywords")
    custom_parameters: Optional[Dict[str, Any]] = Field(None, description="Custom workflow parameters")

# Exception Handler
async def handle_seo_tool_exception(func_name: str, error: Exception, request_data: Dict) -> ErrorResponse:
    """Handle exceptions from SEO tools with intelligent logging"""
    error_id = f"seo_{func_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    error_msg = str(error)
    error_trace = traceback.format_exc()
    
    # Log error with structured data
    error_log = {
        "error_id": error_id,
        "function": func_name,
        "error_type": type(error).__name__,
        "error_message": error_msg,
        "request_data": request_data,
        "traceback": error_trace,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.error(f"SEO Tool Error [{error_id}]: {error_msg}")
    
    # Save error to file
    await save_to_file(f"{LOG_DIR}/errors.jsonl", error_log)
    
    return ErrorResponse(
        success=False,
        message=f"Error in {func_name}: {error_msg}",
        error_type=type(error).__name__,
        error_details=error_msg,
        traceback=error_trace if os.getenv("DEBUG", "false").lower() == "true" else None
    )

# SEO Tool Endpoints

@router.post("/meta-description", response_model=BaseResponse)
@log_api_call
async def generate_meta_description(
    request: MetaDescriptionRequest,
    background_tasks: BackgroundTasks
) -> Union[BaseResponse, ErrorResponse]:
    """
    Generate AI-powered SEO meta descriptions
    
    Generates compelling, SEO-optimized meta descriptions based on keywords,
    tone, and search intent using advanced AI analysis.
    """
    start_time = datetime.utcnow()
    
    try:
        service = MetaDescriptionService()
        result = await service.generate_meta_description(
            keywords=request.keywords,
            tone=request.tone,
            search_intent=request.search_intent,
            language=request.language,
            custom_prompt=request.custom_prompt
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "meta_description_generation",
            "keywords_count": len(request.keywords),
            "tone": request.tone,
            "language": request.language,
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/operations.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="Meta description generated successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("generate_meta_description", e, request.dict())

@router.post("/pagespeed-analysis", response_model=BaseResponse)
@log_api_call
async def analyze_pagespeed(
    request: PageSpeedRequest,
    background_tasks: BackgroundTasks
) -> Union[BaseResponse, ErrorResponse]:
    """
    Analyze website performance using Google PageSpeed Insights
    
    Provides comprehensive performance analysis including Core Web Vitals,
    accessibility, SEO, and best practices scores with AI-enhanced insights.
    """
    start_time = datetime.utcnow()
    
    try:
        service = PageSpeedService()
        result = await service.analyze_pagespeed(
            url=str(request.url),
            strategy=request.strategy,
            locale=request.locale,
            categories=request.categories
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "pagespeed_analysis",
            "url": str(request.url),
            "strategy": request.strategy,
            "categories": request.categories,
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/operations.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="PageSpeed analysis completed successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("analyze_pagespeed", e, request.dict())

@router.post("/sitemap-analysis", response_model=BaseResponse)
@log_api_call
async def analyze_sitemap(
    request: SitemapAnalysisRequest,
    background_tasks: BackgroundTasks
) -> Union[BaseResponse, ErrorResponse]:
    """
    Analyze website sitemap for content structure and trends
    
    Provides insights into content distribution, publishing patterns,
    and SEO opportunities with AI-powered recommendations.
    """
    start_time = datetime.utcnow()
    
    try:
        service = SitemapService()
        result = await service.analyze_sitemap(
            sitemap_url=str(request.sitemap_url),
            analyze_content_trends=request.analyze_content_trends,
            analyze_publishing_patterns=request.analyze_publishing_patterns
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "sitemap_analysis",
            "sitemap_url": str(request.sitemap_url),
            "urls_found": result.get("total_urls", 0),
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/operations.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="Sitemap analysis completed successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("analyze_sitemap", e, request.dict())

@router.post("/image-alt-text", response_model=BaseResponse)
@log_api_call
async def generate_image_alt_text(
    request: ImageAltRequest = None,
    image_file: UploadFile = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> Union[BaseResponse, ErrorResponse]:
    """
    Generate AI-powered alt text for images
    
    Creates SEO-optimized alt text for images using advanced AI vision
    models with context-aware keyword integration.
    """
    start_time = datetime.utcnow()
    
    try:
        service = ImageAltService()
        
        if image_file:
            # Handle uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_file.filename.split('.')[-1]}") as tmp_file:
                content = await image_file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            result = await service.generate_alt_text_from_file(
                image_path=tmp_file_path,
                context=request.context if request else None,
                keywords=request.keywords if request else None
            )
            
            # Cleanup
            os.unlink(tmp_file_path)
            
        elif request and request.image_url:
            result = await service.generate_alt_text_from_url(
                image_url=str(request.image_url),
                context=request.context,
                keywords=request.keywords
            )
        else:
            raise ValueError("Either image_file or image_url must be provided")
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "image_alt_text_generation",
            "has_image_file": image_file is not None,
            "has_image_url": request.image_url is not None if request else False,
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/operations.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="Image alt text generated successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("generate_image_alt_text", e, 
                                              request.dict() if request else {})

@router.post("/opengraph-tags", response_model=BaseResponse)
@log_api_call
async def generate_opengraph_tags(
    request: OpenGraphRequest,
    background_tasks: BackgroundTasks
) -> Union[BaseResponse, ErrorResponse]:
    """
    Generate OpenGraph tags for social media optimization
    
    Creates platform-specific OpenGraph tags optimized for Facebook,
    Twitter, and other social platforms with AI-powered content analysis.
    """
    start_time = datetime.utcnow()
    
    try:
        service = OpenGraphService()
        result = await service.generate_opengraph_tags(
            url=str(request.url),
            title_hint=request.title_hint,
            description_hint=request.description_hint,
            platform=request.platform
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "opengraph_generation",
            "url": str(request.url),
            "platform": request.platform,
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/operations.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="OpenGraph tags generated successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("generate_opengraph_tags", e, request.dict())

@router.post("/on-page-analysis", response_model=BaseResponse)
@log_api_call
async def analyze_on_page_seo(
    request: OnPageSEORequest,
    background_tasks: BackgroundTasks
) -> Union[BaseResponse, ErrorResponse]:
    """
    Comprehensive on-page SEO analysis
    
    Analyzes meta tags, content quality, keyword optimization, internal linking,
    and provides actionable AI-powered recommendations for improvement.
    """
    start_time = datetime.utcnow()
    
    try:
        service = OnPageSEOService()
        result = await service.analyze_on_page_seo(
            url=str(request.url),
            target_keywords=request.target_keywords,
            analyze_images=request.analyze_images,
            analyze_content_quality=request.analyze_content_quality
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "on_page_seo_analysis",
            "url": str(request.url),
            "target_keywords_count": len(request.target_keywords) if request.target_keywords else 0,
            "seo_score": result.get("overall_score", 0),
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/operations.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="On-page SEO analysis completed successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("analyze_on_page_seo", e, request.dict())

@router.post("/technical-seo", response_model=BaseResponse)
@log_api_call
async def analyze_technical_seo(
    request: TechnicalSEORequest,
    background_tasks: BackgroundTasks
) -> Union[BaseResponse, ErrorResponse]:
    """
    Technical SEO analysis and crawling
    
    Performs comprehensive technical SEO audit including site structure,
    crawlability, indexability, and performance with AI-enhanced insights.
    """
    start_time = datetime.utcnow()
    
    try:
        service = TechnicalSEOService()
        result = await service.analyze_technical_seo(
            url=str(request.url),
            crawl_depth=request.crawl_depth,
            include_external_links=request.include_external_links,
            analyze_performance=request.analyze_performance
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "technical_seo_analysis",
            "url": str(request.url),
            "crawl_depth": request.crawl_depth,
            "pages_crawled": result.get("pages_crawled", 0),
            "issues_found": len(result.get("issues", [])),
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/operations.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="Technical SEO analysis completed successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("analyze_technical_seo", e, request.dict())

# Workflow Endpoints

@router.post("/workflow/website-audit", response_model=BaseResponse)
@log_api_call
async def execute_website_audit(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks
) -> Union[BaseResponse, ErrorResponse]:
    """
    Complete website SEO audit workflow
    
    Executes a comprehensive SEO audit combining on-page analysis,
    technical SEO, performance analysis, and competitive intelligence.
    """
    start_time = datetime.utcnow()
    
    try:
        service = EnterpriseSEOService()
        result = await service.execute_complete_audit(
            website_url=str(request.website_url),
            competitors=[str(comp) for comp in request.competitors] if request.competitors else [],
            target_keywords=request.target_keywords or []
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "website_audit_workflow",
            "website_url": str(request.website_url),
            "competitors_count": len(request.competitors) if request.competitors else 0,
            "overall_score": result.get("overall_score", 0),
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/workflows.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="Website audit completed successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("execute_website_audit", e, request.dict())

@router.post("/workflow/content-analysis", response_model=BaseResponse)
@log_api_call
async def execute_content_analysis(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks
) -> Union[BaseResponse, ErrorResponse]:
    """
    AI-powered content analysis workflow
    
    Analyzes content gaps, opportunities, and competitive positioning
    with AI-generated strategic recommendations for content creators.
    """
    start_time = datetime.utcnow()
    
    try:
        service = ContentStrategyService()
        result = await service.analyze_content_strategy(
            website_url=str(request.website_url),
            competitors=[str(comp) for comp in request.competitors] if request.competitors else [],
            target_keywords=request.target_keywords or [],
            custom_parameters=request.custom_parameters or {}
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log successful operation
        log_data = {
            "operation": "content_analysis_workflow",
            "website_url": str(request.website_url),
            "content_gaps_found": len(result.get("content_gaps", [])),
            "opportunities_identified": len(result.get("opportunities", [])),
            "execution_time": execution_time,
            "success": True
        }
        background_tasks.add_task(save_to_file, f"{LOG_DIR}/workflows.jsonl", log_data)
        
        return BaseResponse(
            success=True,
            message="Content analysis completed successfully",
            execution_time=execution_time,
            data=result
        )
        
    except Exception as e:
        return await handle_seo_tool_exception("execute_content_analysis", e, request.dict())

# Health and Status Endpoints

@router.get("/health", response_model=BaseResponse)
async def health_check() -> BaseResponse:
    """Health check endpoint for SEO tools"""
    return BaseResponse(
        success=True,
        message="AI SEO Tools API is healthy",
        data={
            "status": "operational",
            "available_tools": [
                "meta_description",
                "pagespeed_analysis", 
                "sitemap_analysis",
                "image_alt_text",
                "opengraph_tags",
                "on_page_analysis",
                "technical_seo",
                "website_audit",
                "content_analysis"
            ],
            "version": "1.0.0"
        }
    )

@router.get("/tools/status", response_model=BaseResponse)
async def get_tools_status() -> BaseResponse:
    """Get status of all SEO tools and their dependencies"""
    
    tools_status = {}
    overall_healthy = True
    
    # Check each service
    services = [
        ("meta_description", MetaDescriptionService),
        ("pagespeed", PageSpeedService),
        ("sitemap", SitemapService),
        ("image_alt", ImageAltService),
        ("opengraph", OpenGraphService),
        ("on_page_seo", OnPageSEOService),
        ("technical_seo", TechnicalSEOService),
        ("enterprise_seo", EnterpriseSEOService),
        ("content_strategy", ContentStrategyService)
    ]
    
    for service_name, service_class in services:
        try:
            service = service_class()
            status = await service.health_check() if hasattr(service, 'health_check') else {"status": "unknown"}
            tools_status[service_name] = {
                "healthy": status.get("status") == "operational",
                "details": status
            }
            if not tools_status[service_name]["healthy"]:
                overall_healthy = False
        except Exception as e:
            tools_status[service_name] = {
                "healthy": False,
                "error": str(e)
            }
            overall_healthy = False
    
    return BaseResponse(
        success=overall_healthy,
        message="Tools status check completed",
        data={
            "overall_healthy": overall_healthy,
            "tools": tools_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    )