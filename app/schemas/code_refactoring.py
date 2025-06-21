from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class CodeRefactoringBase(BaseModel):
    original_code: str = Field(..., description="The original code to be refactored")
    language: Optional[str] = Field(None, description="Programming language (auto-detected if not provided)")
    focus_areas: Optional[List[str]] = Field(None, description="Areas to focus on during refactoring")

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

class CodeAnalysisResult(BaseModel):
    complexity_score: int = Field(..., ge=1, le=10, description="Code complexity score (1-10)")
    readability_score: int = Field(..., ge=1, le=10, description="Code readability score (1-10)")
    issues: List[dict] = Field(default_factory=list, description="List of identified issues")
    overall_assessment: str = Field(..., description="Overall assessment of code quality")

class CodeRefactoringResponse(CodeRefactoringBase):
    id: UUID
    refactored_code: Optional[str] = None
    explanation: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    feedback: list[RefactoringFeedbackResponse] = []
    analysis_result: Optional[CodeAnalysisResult] = None

    class Config:
        from_attributes = True

class CodeSuggestion(BaseModel):
    category: str = Field(..., description="Category of suggestion")
    priority: str = Field(..., description="Priority level")
    title: str = Field(..., description="Brief title of suggestion")
    description: str = Field(..., description="Detailed description")
    example: Optional[str] = Field(None, description="Code example")
    rationale: str = Field(..., description="Why this improvement is beneficial")

class CodeSuggestionsResponse(BaseModel):
    suggestions: List[CodeSuggestion]
    language: str
    code_length: int 