from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import json
import logging

from app.core.database import get_db
from app.models.code_refactoring import CodeRefactoring, RefactoringFeedback
from app.schemas.code_refactoring import (
    CodeRefactoringCreate,
    CodeRefactoringResponse,
    RefactoringFeedbackCreate,
    RefactoringFeedbackResponse,
    CodeAnalysisResult,
    CodeSuggestionsResponse,
    CodeSuggestion
)
from app.services.mock_ai_refactoring import MockAIRefactoringService

router = APIRouter(prefix="/api/refactoring", tags=["code-refactoring"])

ai_service = MockAIRefactoringService()

async def process_refactoring_background(refactoring_id: UUID, db: Session):
    """Background task to process refactoring with AI."""
    logging.info(f"Starting background refactoring for ID: {refactoring_id}")
    try:
        refactoring = db.query(CodeRefactoring).filter(CodeRefactoring.id == refactoring_id).first()
        if not refactoring:
            logging.error(f"Refactoring ID not found in background task: {refactoring_id}")
            return
        
        logging.info(f"Processing refactoring for language: {refactoring.language}")
        
        language = refactoring.language or ai_service.detect_language(refactoring.original_code)
        
        analysis_result = ai_service.analyze_code_quality(refactoring.original_code, language)
        
        refactored_code, explanation = ai_service.refactor_code(
            refactoring.original_code, 
            language,
            refactoring.focus_areas
        )
        
        refactoring.refactored_code = refactored_code
        refactoring.explanation = explanation
        refactoring.status = "completed"
        refactoring.analysis_result = json.dumps(analysis_result)
        
        db.commit()
        logging.info(f"Successfully completed refactoring for ID: {refactoring_id}")
        
    except Exception as e:
        logging.error(f"Error during background refactoring for ID {refactoring_id}: {e}", exc_info=True)
        refactoring = db.query(CodeRefactoring).filter(CodeRefactoring.id == refactoring_id).first()
        if refactoring:
            refactoring.status = "failed"
            refactoring.explanation = f"Refactoring failed: {str(e)}"
            db.commit()

@router.post("/", response_model=CodeRefactoringResponse)
async def create_refactoring(
    refactoring: CodeRefactoringCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new code refactoring request."""
    language = refactoring.language or ai_service.detect_language(refactoring.original_code)
    
    db_refactoring = CodeRefactoring(
        original_code=refactoring.original_code,
        language=language,
        focus_areas=refactoring.focus_areas,
        status="processing"
    )
    db.add(db_refactoring)
    db.commit()
    db.refresh(db_refactoring)
    
    background_tasks.add_task(process_refactoring_background, db_refactoring.id, db)
    
    return db_refactoring

@router.get("/{refactoring_id}", response_model=CodeRefactoringResponse)
async def get_refactoring(
    refactoring_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific refactoring by ID."""
    refactoring = db.query(CodeRefactoring).filter(CodeRefactoring.id == refactoring_id).first()
    if not refactoring:
        raise HTTPException(status_code=404, detail="Refactoring not found")
    
    # Parse analysis result if it exists
    if refactoring.analysis_result:
        try:
            analysis_data = json.loads(refactoring.analysis_result)
            refactoring.analysis_result = CodeAnalysisResult(**analysis_data)
        except:
            refactoring.analysis_result = None
    
    return refactoring

@router.post("/{refactoring_id}/feedback", response_model=RefactoringFeedbackResponse)
async def create_feedback(
    refactoring_id: UUID,
    feedback: RefactoringFeedbackCreate,
    db: Session = Depends(get_db)
):
    """Add feedback to a refactoring."""
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

@router.post("/analyze", response_model=CodeAnalysisResult)
async def analyze_code(
    code: str,
    language: str = None
):
    """Analyze code quality without refactoring."""
    if not language:
        language = ai_service.detect_language(code)
    
    analysis_result = ai_service.analyze_code_quality(code, language)
    return CodeAnalysisResult(**analysis_result)

@router.post("/suggestions", response_model=CodeSuggestionsResponse)
async def get_suggestions(
    code: str,
    language: str = None
):
    """Get improvement suggestions for code."""
    if not language:
        language = ai_service.detect_language(code)
    
    suggestions = ai_service.suggest_improvements(code, language)
    
    # Convert to CodeSuggestion objects
    code_suggestions = [
        CodeSuggestion(**suggestion) for suggestion in suggestions
    ]
    
    return CodeSuggestionsResponse(
        suggestions=code_suggestions,
        language=language,
        code_length=len(code)
    )

@router.post("/explain")
async def explain_code(
    code: str,
    language: str = None
):
    """Get a detailed explanation of what the code does."""
    if not language:
        language = ai_service.detect_language(code)
    
    explanation = ai_service.explain_code(code, language)
    return {"explanation": explanation, "language": language}

@router.get("/", response_model=List[CodeRefactoringResponse])
async def list_refactorings(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all refactorings with pagination."""
    refactorings = db.query(CodeRefactoring).offset(skip).limit(limit).all()
    
    for refactoring in refactorings:
        if refactoring.analysis_result:
            try:
                analysis_data = json.loads(refactoring.analysis_result)
                refactoring.analysis_result = CodeAnalysisResult(**analysis_data)
            except:
                refactoring.analysis_result = None
    
    return refactorings 