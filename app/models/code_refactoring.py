#AI assistance was used for creating this file
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import uuid

from app.core.database import Base

class CodeRefactoring(Base):
    """Model for storing code refactoring requests and results."""
    __tablename__ = "code_refactorings"
    # Primary key using UUID for better security and distribution
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # The original code that needs to be refactored
    original_code = Column(Text, nullable=False)
    # The improved version of the code after refactoring
    refactored_code = Column(Text, nullable=True)
    # Explanation of what changes were made and why
    explanation = Column(Text, nullable=True)
    # Current status of the refactoring
    status = Column(String, nullable=False)
    # Timestamps for tracking when the refactoring was created and last updated
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    # Relationship to feedback entries
    feedback = relationship("RefactoringFeedback", back_populates="refactoring", cascade="all, delete-orphan")

class RefactoringFeedback(Base):
    """Model for storing user feedback on refactored code."""
    __tablename__ = "refactoring_feedback"
    # Primary key using UUID for better security and distribution
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Foreign key linking to the code refactoring this feedback is for
    refactoring_id = Column(UUID(as_uuid=True), ForeignKey("code_refactorings.id"), nullable=False)
    # Numerical rating of the refactoring (e.g., 1-5 stars)
    rating = Column(Integer, nullable=False)
    # Optional text feedback about the refactoring
    comment = Column(Text, nullable=True)
    # Timestamp of when the feedback was given
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    # Relationship to the parent refactoring
    refactoring = relationship("CodeRefactoring", back_populates="feedback") 