from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class CodeRefactoringBase(BaseModel):
    original_code: str = Field(..., description="The original code to be refactored")

class CodeRefactoringCreate(CodeRefactoringBase):
    pass

class RefactoringFeedbackBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(None, description="Optional feedback comment")

class RefactoringFeedbackCreate(RefactoringFeedbackBase):
    pass

class RefactoringFeedbackResponse(RefactoringFeedbackBase):
    id: UUID
    refactoring_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class CodeRefactoringResponse(CodeRefactoringBase):
    id: UUID
    refactored_code: Optional[str] = None
    explanation: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    feedback: list[RefactoringFeedbackResponse] = []

    class Config:
        from_attributes = True 