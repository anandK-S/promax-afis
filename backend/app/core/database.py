# ========================================
# Pro-Max AFIS - Database Configuration
# ========================================
# PostgreSQL + TimescaleDB connection setup
# Author: Pro-Max Development Team

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from typing import Generator
import logging

from .config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine with optimized settings
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.debug,
    future=True,
    connect_args={
        "options": "-c timezone=Asia/Kolkata"
    } if settings.database_url.startswith("postgresql") else {}
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency for getting database sessions
    Yields database session and ensures cleanup
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables
    """
    try:
        # Import all models to ensure they're registered with Base
        from app.models import user, business, financial, inventory, ml_predictions
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Enable TimescaleDB extension if available
        if settings.timescaledb_enabled:
            try:
                with engine.connect() as conn:
                    conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
                    conn.commit()
                logger.info("TimescaleDB extension enabled")
            except Exception as e:
                logger.warning(f"Could not enable TimescaleDB extension: {str(e)}")
                
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise


def check_db_connection() -> bool:
    """
    Check database connection health
    Returns True if connection is successful
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False