#AI assistance was used for creating this file
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,  # Don't automatically commit changes
    autoflush=False,   # Don't automatically flush changes
    bind=engine        # Use our engine for database operations
)

# Create base class for models
Base = declarative_base()

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 