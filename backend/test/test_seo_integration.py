#!/usr/bin/env python3
"""
Test script for SEO analyzer integration
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.comprehensive_seo_analyzer import ComprehensiveSEOAnalyzer
from services.database import init_database, get_db_session
from services.seo_analysis_service import SEOAnalysisService
from loguru import logger

async def test_seo_analyzer():
    """Test the SEO analyzer functionality."""
    
    print("🔍 Testing SEO Analyzer Integration")
    print("=" * 50)
    
    try:
        # Initialize database
        print("📊 Initializing database...")
        init_database()
        print("✅ Database initialized successfully")
        
        # Test URL
        test_url = "https://example.com"
        print(f"🌐 Testing with URL: {test_url}")
        
        # Create analyzer
        analyzer = ComprehensiveSEOAnalyzer()
        
        # Run analysis
        print("🔍 Running comprehensive SEO analysis...")
        result = analyzer.analyze_url(test_url)
        
        print(f"📈 Analysis Results:")
        print(f"   URL: {result.url}")
        print(f"   Overall Score: {result.overall_score}/100")
        print(f"   Health Status: {result.health_status}")
        print(f"   Critical Issues: {len(result.critical_issues)}")
        print(f"   Warnings: {len(result.warnings)}")
        print(f"   Recommendations: {len(result.recommendations)}")
        
        # Test database storage
        print("\n💾 Testing database storage...")
        db_session = get_db_session()
        if db_session:
            try:
                seo_service = SEOAnalysisService(db_session)
                stored_analysis = seo_service.store_analysis_result(result)
                
                if stored_analysis:
                    print(f"✅ Analysis stored in database with ID: {stored_analysis.id}")
                    
                    # Test retrieval
                    retrieved_analysis = seo_service.get_latest_analysis(test_url)
                    if retrieved_analysis:
                        print(f"✅ Analysis retrieved from database")
                        print(f"   Stored Score: {retrieved_analysis.overall_score}")
                        print(f"   Stored Status: {retrieved_analysis.health_status}")
                    else:
                        print("❌ Failed to retrieve analysis from database")
                else:
                    print("❌ Failed to store analysis in database")
                    
            except Exception as e:
                print(f"❌ Database error: {str(e)}")
            finally:
                db_session.close()
        else:
            print("❌ Failed to get database session")
        
        # Test statistics
        print("\n📊 Testing statistics...")
        db_session = get_db_session()
        if db_session:
            try:
                seo_service = SEOAnalysisService(db_session)
                stats = seo_service.get_analysis_statistics()
                print(f"📈 Analysis Statistics:")
                print(f"   Total Analyses: {stats['total_analyses']}")
                print(f"   Total URLs: {stats['total_urls']}")
                print(f"   Average Score: {stats['average_score']}")
                print(f"   Health Distribution: {stats['health_distribution']}")
            except Exception as e:
                print(f"❌ Statistics error: {str(e)}")
            finally:
                db_session.close()
        
        print("\n🎉 SEO Analyzer Integration Test Completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        logger.error(f"Test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_seo_analyzer()) 