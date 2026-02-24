#database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

# Use fixed database URL (handles Render's postgres:// vs postgresql://)
engine = create_engine(
    settings.database_url_fixed,  # Use the fixed property
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """Initialize database - create all tables"""
    from . import models
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()