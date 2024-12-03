"""
Code complexity analysis
"""
from typing import Dict, Any
import ast
from pydantic import BaseModel

class ComplexityMetrics(BaseModel):
    """Code complexity measurements"""
    cyclomatic: int
    cognitive: int
    maintainability: float
    halstead: Dict[str, float]

class ComplexityAnalyzer:
    """Analyzes code complexity"""
    
    def calculate_complexity(self, node: ast.AST) -> ComplexityMetrics:
        """Calculate various complexity metrics"""
        return ComplexityMetrics(
            cyclomatic=self._calculate_cyclomatic(node),
            cognitive=self._calculate_cognitive(node),
            maintainability=self._calculate_maintainability(node),
            halstead=self._calculate_halstead(node)
        )
    
    def _calculate_cyclomatic(self, node: ast.AST) -> int:
        """Calculate McCabe cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.And, ast.Or)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
                
        return complexity
    
    def _calculate_cognitive(self, node: ast.AST) -> int:
        """Calculate cognitive complexity"""
        complexity = 0
        nesting_level = 0
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity += (1 + nesting_level)
                nesting_level += 1
                
        return complexity 