#!/usr/bin/env python3
"""
Script to create monitoring tables in the database.
Run this script to ensure all monitoring-related tables are created.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database import init_database, get_db_session
from models.monitoring_models import (
    StrategyMonitoringPlan,
    MonitoringTask,
    TaskExecutionLog,
    StrategyPerformanceMetrics,
    StrategyActivationStatus
)
from models.enhanced_strategy_models import EnhancedContentStrategy
from loguru import logger

def create_monitoring_tables():
    """Create all monitoring-related tables"""
    try:
        logger.info("Creating monitoring tables...")
        
        # Initialize database with all models
        init_database()
        
        logger.info("✅ Monitoring tables created successfully!")
        
        # Test database connection
        db_session = get_db_session()
        if db_session:
            logger.info("✅ Database connection test successful!")
            db_session.close()
        else:
            logger.warning("⚠️ Database connection test failed!")
            
    except Exception as e:
        logger.error(f"❌ Error creating monitoring tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_monitoring_tables()
