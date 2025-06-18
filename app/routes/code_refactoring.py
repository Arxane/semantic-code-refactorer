from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.code_refactoring import CodeRefactoring, RefactoringFeedback
from app.schemas.code_refactoring import (
    CodeRefactoringCreate,
    CodeRefactoringResponse,
    RefactoringFeedbackCreate,
    RefactoringFeedbackResponse
)

router = APIRouter(prefix="/api/refactoring", tags=["code-refactoring"])

@router.post("/", response_model=CodeRefactoringResponse)
async def create_refactoring(
    refactoring: CodeRefactoringCreate,
    db: Session = Depends(get_db)
):
    db_refactoring = CodeRefactoring(
        original_code=refactoring.original_code,
        status="pending"
    )
    db.add(db_refactoring)
    db.commit()
    db.refresh(db_refactoring)
    return db_refactoring

@router.get("/{refactoring_id}", response_model=CodeRefactoringResponse)
async def get_refactoring(
    refactoring_id: UUID,
    db: Session = Depends(get_db)
):
    refactoring = db.query(CodeRefactoring).filter(CodeRefactoring.id == refactoring_id).first()
    if not refactoring:
        raise HTTPException(status_code=404, detail="Refactoring not found")
    return refactoring

@router.post("/{refactoring_id}/feedback", response_model=RefactoringFeedbackResponse)
async def create_feedback(
    refactoring_id: UUID,
    feedback: RefactoringFeedbackCreate,
    db: Session = Depends(get_db)
):
    refactoring = db.query(CodeRefactoring).filter(CodeRefactoring.id == refactoring_id).first()
    if not refactoring:
        raise HTTPException(status_code=404, detail="Refactoring not found")
    
    db_feedback = RefactoringFeedback(
        refactoring_id=refactoring_id,
        rating=feedback.rating,
        comment=feedback.comment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback 