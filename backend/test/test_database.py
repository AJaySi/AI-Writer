"""
Test script for database functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.database import init_database, get_db_session, close_database
from services.website_analysis_service import WebsiteAnalysisService
from models.onboarding import WebsiteAnalysis, OnboardingSession

def test_database_functionality():
    """Test database initialization and basic operations."""
    try:
        print("Testing database functionality...")
        
        # Initialize database
        init_database()
        print("✅ Database initialized successfully")
        
        # Get database session
        db_session = get_db_session()
        if not db_session:
            print("❌ Failed to get database session")
            return False
        
        print("✅ Database session created successfully")
        
        # Test website analysis service
        analysis_service = WebsiteAnalysisService(db_session)
        print("✅ Website analysis service created successfully")
        
        # Test creating a session
        session = OnboardingSession(user_id=1, current_step=2, progress=25.0)
        db_session.add(session)
        db_session.commit()
        print(f"✅ Created onboarding session with ID: {session.id}")
        
        # Test saving analysis
        test_analysis_data = {
            'style_analysis': {
                'writing_style': {
                    'tone': 'professional',
                    'voice': 'active',
                    'complexity': 'moderate',
                    'engagement_level': 'high'
                },
                'target_audience': {
                    'demographics': ['professionals', 'business owners'],
                    'expertise_level': 'intermediate',
                    'industry_focus': 'technology',
                    'geographic_focus': 'global'
                },
                'content_type': {
                    'primary_type': 'blog',
                    'secondary_types': ['article', 'guide'],
                    'purpose': 'informational',
                    'call_to_action': 'subscribe'
                },
                'recommended_settings': {
                    'writing_tone': 'professional',
                    'target_audience': 'business professionals',
                    'content_type': 'blog posts',
                    'creativity_level': 'balanced',
                    'geographic_location': 'global'
                }
            },
            'crawl_result': {
                'content': 'Sample website content...',
                'word_count': 1500
            },
            'style_patterns': {
                'sentence_length': 'medium',
                'paragraph_structure': 'well-organized'
            },
            'style_guidelines': {
                'tone_guidelines': 'Maintain professional tone',
                'structure_guidelines': 'Use clear headings'
            }
        }
        
        analysis_id = analysis_service.save_analysis(
            session_id=session.id,
            website_url='https://example.com',
            analysis_data=test_analysis_data
        )
        
        if analysis_id:
            print(f"✅ Saved analysis with ID: {analysis_id}")
        else:
            print("❌ Failed to save analysis")
            return False
        
        # Test retrieving analysis
        analysis = analysis_service.get_analysis(analysis_id)
        if analysis:
            print("✅ Retrieved analysis successfully")
            print(f"   Website URL: {analysis['website_url']}")
            print(f"   Writing Style: {analysis['writing_style']['tone']}")
        else:
            print("❌ Failed to retrieve analysis")
            return False
        
        # Test checking existing analysis
        existing_check = analysis_service.check_existing_analysis(
            session_id=session.id,
            website_url='https://example.com'
        )
        
        if existing_check and existing_check.get('exists'):
            print("✅ Existing analysis check works")
        else:
            print("❌ Existing analysis check failed")
            return False
        
        # Clean up
        if analysis_id:
            analysis_service.delete_analysis(analysis_id)
        db_session.delete(session)
        db_session.commit()
        print("✅ Cleanup completed")
        
        print("\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False
    finally:
        close_database()

if __name__ == "__main__":
    success = test_database_functionality()
    if success:
        print("\n✅ Database functionality is working correctly!")
    else:
        print("\n❌ Database functionality has issues!")
        sys.exit(1) 