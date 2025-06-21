import time
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class MockAIRefactoringService:
    """A mock service for AI-powered code refactoring that returns dummy data."""
    
    def __init__(self):
        logger.info("Using MockAIRefactoringService.")

    def detect_language(self, code: str) -> str:
        """Mock language detection."""
        return 'python'

    def analyze_code_quality(self, code: str, language: str) -> Dict[str, any]:
        """Mock code quality analysis."""
        return {
            "complexity_score": 3,
            "readability_score": 7,
            "issues": [
                {
                    "type": "readability",
                    "severity": "low",
                    "description": "The function can be simplified using Python's built-in `sum()` function.",
                    "line_numbers": [1, 2, 3, 4],
                    "suggestion": "Replace the for loop with `return sum(numbers)`."
                }
            ],
            "overall_assessment": "The code is functional but can be more concise and Pythonic."
        }

    def refactor_code(self, code: str, language:str, focus_areas: Optional[List[str]] = None) -> Tuple[str, str]:
        """Mock code refactoring."""
        time.sleep(2)
        
        refactored_code = "def efficient_sum(numbers):\n    \"\"\"Calculates the sum of a list of numbers.\"\"\"\n    return sum(numbers)"
        explanation = "The original for-loop was replaced with Python's built-in `sum()` function. This is more efficient, readable, and less prone to errors."
        
        return refactored_code, explanation

    def suggest_improvements(self, code: str, language: str) -> List[Dict[str, str]]:
        """Mock improvement suggestions."""
        return [
            {
                "category": "best_practice",
                "priority": "medium",
                "title": "Use Built-in `sum()` function",
                "description": "The current implementation uses a manual loop to sum numbers. Python's built-in `sum()` function is more idiomatic and performant.",
                "example": "return sum(numbers)",
                "rationale": "Built-in functions are highly optimized and improve code readability."
            }
        ]

    def explain_code(self, code: str, language: str) -> str:
        """Mock code explanation."""
        return "This Python function `inefficient_sum` takes a list of numbers, initializes a variable `s` to 0, iterates through the list, adds each number to `s`, and finally returns the total sum." 