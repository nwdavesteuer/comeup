"""
Database connection and session management
Supports both SQLite (local dev) and PostgreSQL (production)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings

# Determine if we're using SQLite or PostgreSQL
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

# Create database engine with appropriate settings
if is_sqlite:
    # SQLite configuration (local development)
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        echo=False  # Set to True for SQL query logging in development
    )
else:
    # PostgreSQL configuration (production)
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        echo=False  # Set to True for SQL query logging in development
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for getting database session.
    Use in FastAPI route dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

