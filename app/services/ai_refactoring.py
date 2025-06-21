import openai
import re
from typing import Dict, List, Optional, Tuple
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIRefactoringService:
    """Service for AI-powered code refactoring."""
    
    def __init__(self):
        """Initialize the AI refactoring service with OpenAI client."""
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.supported_languages = {
            'python': '.py',
            'javascript': '.js',
            'typescript': '.ts',
            'java': '.java',
            'cpp': '.cpp',
            'csharp': '.cs',
            'go': '.go',
            'rust': '.rs',
            'php': '.php',
            'ruby': '.rb',
            'swift': '.swift',
            'kotlin': '.kt',
            'scala': '.scala',
            'r': '.r',
            'matlab': '.m',
            'sql': '.sql',
            'html': '.html',
            'css': '.css',
            'scss': '.scss',
            'sass': '.sass'
        }
    
    def detect_language(self, code: str) -> str:
        """
        Detect the programming language of the provided code.
        
        Args:
            code: The source code to analyze
            
        Returns:
            str: Detected programming language
        """
        # Simple heuristics for language detection
        code_lower = code.lower()
        
        if 'def ' in code_lower and 'import ' in code_lower:
            return 'python'
        elif 'function ' in code_lower and ('var ' in code_lower or 'let ' in code_lower or 'const ' in code_lower):
            return 'javascript'
        elif 'function ' in code_lower and 'type ' in code_lower:
            return 'typescript'
        elif 'public class ' in code_lower or 'private ' in code_lower:
            return 'java'
        elif '#include ' in code_lower and ('int main' in code_lower or 'std::' in code_lower):
            return 'cpp'
        elif 'using System;' in code_lower or 'namespace ' in code_lower:
            return 'csharp'
        elif 'package ' in code_lower and 'func ' in code_lower:
            return 'go'
        elif 'fn ' in code_lower and 'let ' in code_lower:
            return 'rust'
        elif '<?php' in code_lower:
            return 'php'
        elif 'def ' in code_lower and 'end' in code_lower:
            return 'ruby'
        elif 'func ' in code_lower and 'import ' in code_lower:
            return 'swift'
        elif 'fun ' in code_lower and 'val ' in code_lower:
            return 'kotlin'
        elif 'def ' in code_lower and 'val ' in code_lower:
            return 'scala'
        elif '<!DOCTYPE html>' in code_lower or '<html>' in code_lower:
            return 'html'
        elif '{' in code_lower and ':' in code_lower and ';' in code_lower:
            return 'css'
        elif 'SELECT ' in code_lower or 'INSERT ' in code_lower or 'UPDATE ' in code_lower:
            return 'sql'
        else:
            return 'python'  # Default fallback
    
    def analyze_code_quality(self, code: str, language: str) -> Dict[str, any]:
        """
        Analyze code quality and identify potential refactoring opportunities.
        
        Args:
            code: The source code to analyze
            language: Programming language of the code
            
        Returns:
            Dict containing analysis results
        """
        analysis_prompt = f"""
        Analyze the following {language} code for potential refactoring opportunities. 
        Focus on:
        1. Code complexity and readability
        2. Performance issues
        3. Code smells (long methods, duplicate code, etc.)
        4. Best practices violations
        5. Security concerns
        
        Code:
        {code}
        
        Provide a JSON response with the following structure:
        {{
            "complexity_score": 1-10,
            "readability_score": 1-10,
            "issues": [
                {{
                    "type": "complexity|readability|performance|security|best_practice",
                    "severity": "low|medium|high|critical",
                    "description": "Description of the issue",
                    "line_numbers": [1, 2, 3],
                    "suggestion": "How to fix this issue"
                }}
            ],
            "overall_assessment": "Brief summary of code quality"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer and refactoring specialist. Provide detailed, actionable analysis in JSON format."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            # Parse the JSON response
            import json
            analysis_result = json.loads(response.choices[0].message.content)
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing code quality: {e}")
            return {
                "complexity_score": 5,
                "readability_score": 5,
                "issues": [],
                "overall_assessment": "Unable to analyze code quality due to an error."
            }
    
    def refactor_code(self, code: str, language: str, focus_areas: Optional[List[str]] = None) -> Tuple[str, str]:
        """
        Refactor the provided code using AI.
        
        Args:
            code: The source code to refactor
            language: Programming language of the code
            focus_areas: Optional list of specific areas to focus on (e.g., ['performance', 'readability'])
            
        Returns:
            Tuple of (refactored_code, explanation)
        """
        if focus_areas is None:
            focus_areas = ['readability', 'performance', 'best_practices']
        
        focus_areas_str = ', '.join(focus_areas)
        
        refactoring_prompt = f"""
        Refactor the following {language} code to improve {focus_areas_str}.
        
        Requirements:
        1. Maintain the same functionality
        2. Improve code quality and readability
        3. Follow {language} best practices
        4. Add helpful comments where appropriate
        5. Optimize performance if possible
        
        Original Code:
        {code}
        
        Please provide your response in the following JSON format:
        {{
            "refactored_code": "The improved code",
            "explanation": "Detailed explanation of what was changed and why",
            "improvements": [
                {{
                    "type": "readability|performance|security|best_practice",
                    "description": "What was improved",
                    "impact": "How this improvement helps"
                }}
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} developer and refactoring specialist. Always maintain functionality while improving code quality."},
                    {"role": "user", "content": refactoring_prompt}
                ],
                temperature=0.2,
                max_tokens=3000
            )
            
            # Parse the JSON response
            import json
            result = json.loads(response.choices[0].message.content)
            
            return result["refactored_code"], result["explanation"]
            
        except Exception as e:
            logger.error(f"Error refactoring code: {e}")
            return code, f"Unable to refactor code due to an error: {str(e)}"
    
    def suggest_improvements(self, code: str, language: str) -> List[Dict[str, str]]:
        """
        Suggest specific improvements for the code without refactoring it.
        
        Args:
            code: The source code to analyze
            language: Programming language of the code
            
        Returns:
            List of improvement suggestions
        """
        suggestions_prompt = f"""
        Analyze the following {language} code and suggest specific improvements.
        Focus on actionable, specific suggestions that can be implemented.
        
        Code:
        {code}
        
        Provide your response in JSON format:
        {{
            "suggestions": [
                {{
                    "category": "readability|performance|security|maintainability|best_practice",
                    "priority": "low|medium|high|critical",
                    "title": "Brief title of the suggestion",
                    "description": "Detailed description of the improvement",
                    "example": "Code example showing the improvement",
                    "rationale": "Why this improvement is beneficial"
                }}
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} developer providing actionable improvement suggestions."},
                    {"role": "user", "content": suggestions_prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result.get("suggestions", [])
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return []
    
    def explain_code(self, code: str, language: str) -> str:
        """
        Generate a detailed explanation of what the code does.
        
        Args:
            code: The source code to explain
            language: Programming language of the code
            
        Returns:
            Detailed explanation of the code
        """
        explanation_prompt = f"""
        Explain the following {language} code in detail. Include:
        1. What the code does overall
        2. How each major function/class works
        3. Key algorithms or patterns used
        4. Any important variables or data structures
        5. Potential edge cases or considerations
        
        Code:
        {code}
        
        Provide a clear, educational explanation suitable for developers.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} developer and educator. Provide clear, detailed explanations."},
                    {"role": "user", "content": explanation_prompt}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error explaining code: {e}")
            return f"Unable to explain code due to an error: {str(e)}" 