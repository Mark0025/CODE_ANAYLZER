#!/bin/bash
set -e

echo "🏗️ Completing Pattern Detection System..."

# Update pattern detector with full implementation
cat > code_analyzer/crews/analysis_crews/pattern_detector.py << 'EOF'
"""Pattern detection using AST helpers."""
from typing import Dict, Any, List
from code_analyzer.utils.ast_helpers import parse_code_safely, get_node_name
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger
import ast

class PatternMatch:
    """Pattern match information"""
    def __init__(self, type: str, name: str, location: Dict[str, Any], confidence: float, description: str = "", suggestion: str = ""):
        self.type = type
        self.name = name
        self.location = location
        self.confidence = confidence
        self.description = description
        self.suggestion = suggestion

class PatternDetector:
    """Detects code patterns and anti-patterns"""
    
    async def analyze_patterns(self, code: str) -> Dict[str, Any]:
        """Analyze code for patterns"""
        try:
            tree = parse_code_safely(code)
            if not tree:
                raise ValueError("Failed to parse code")
            
            # Detect all patterns
            code_smells = await self._detect_code_smells(tree)
            design_patterns = await self._detect_design_patterns(tree)
            anti_patterns = await self._detect_anti_patterns(tree)
            
            results = {
                "code_smells": [self._pattern_to_dict(p) for p in code_smells],
                "design_patterns": [self._pattern_to_dict(p) for p in design_patterns],
                "anti_patterns": [self._pattern_to_dict(p) for p in anti_patterns],
                "metrics": await self._calculate_metrics(tree)
            }
            
            # Save to database
            db = DatabaseManager()
            db.save_crew_output(
                crew_name="pattern_detector",
                output_type="pattern_analysis",
                status="completed",
                results=results
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Pattern analysis failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _pattern_to_dict(self, pattern: PatternMatch) -> Dict[str, Any]:
        """Convert pattern to dictionary."""
        return {
            "type": pattern.type,
            "name": pattern.name,
            "location": pattern.location,
            "confidence": pattern.confidence,
            "description": pattern.description,
            "suggestion": pattern.suggestion
        }
    
    async def _detect_code_smells(self, tree: ast.AST) -> List[PatternMatch]:
        """Detect code smells in AST."""
        smells = []
        
        for node in ast.walk(tree):
            # Long method detection
            if isinstance(node, ast.FunctionDef) and len(node.body) > 20:
                smells.append(PatternMatch(
                    type="code_smell",
                    name="long_method",
                    location={"function": node.name},
                    confidence=0.9,
                    description="Method is too long (>20 lines)",
                    suggestion="Consider breaking into smaller functions"
                ))
            
            # Too many parameters
            if isinstance(node, ast.FunctionDef) and len(node.args.args) > 5:
                smells.append(PatternMatch(
                    type="code_smell",
                    name="too_many_parameters",
                    location={"function": node.name},
                    confidence=0.8,
                    description=f"Function has {len(node.args.args)} parameters",
                    suggestion="Consider using a configuration object"
                ))
        
        return smells
    
    async def _detect_design_patterns(self, tree: ast.AST) -> List[PatternMatch]:
        """Detect design patterns in AST."""
        patterns = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Singleton detection
                if self._is_singleton(node):
                    patterns.append(PatternMatch(
                        type="design_pattern",
                        name="singleton",
                        location={"class": node.name},
                        confidence=0.9,
                        description="Singleton pattern detected",
                        suggestion="Ensure global state is necessary"
                    ))
                
                # Factory detection
                if self._is_factory(node):
                    patterns.append(PatternMatch(
                        type="design_pattern",
                        name="factory",
                        location={"class": node.name},
                        confidence=0.85,
                        description="Factory pattern detected",
                        suggestion="Good for object creation abstraction"
                    ))
        
        return patterns
    
    async def _detect_anti_patterns(self, tree: ast.AST) -> List[PatternMatch]:
        """Detect anti-patterns in AST."""
        patterns = []
        
        for node in ast.walk(tree):
            # God class detection
            if isinstance(node, ast.ClassDef) and len(node.body) > 30:
                patterns.append(PatternMatch(
                    type="anti_pattern",
                    name="god_class",
                    location={"class": node.name},
                    confidence=0.7,
                    description="Class is too large (>30 methods/attributes)",
                    suggestion="Split into smaller, focused classes"
                ))
        
        return patterns
    
    def _is_singleton(self, node: ast.ClassDef) -> bool:
        """Check if class follows singleton pattern."""
        has_instance = False
        has_get_instance = False
        
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and child.id == "_instance":
                has_instance = True
            if isinstance(child, ast.FunctionDef) and child.name == "getInstance":
                has_get_instance = True
                
        return has_instance and has_get_instance
    
    def _is_factory(self, node: ast.ClassDef) -> bool:
        """Check if class follows factory pattern."""
        create_methods = 0
        
        for child in ast.walk(node):
            if isinstance(child, ast.FunctionDef) and (
                child.name.startswith('create') or 
                child.name.startswith('make') or
                child.name.startswith('build')
            ):
                create_methods += 1
                
        return create_methods > 0
    
    async def _calculate_metrics(self, tree: ast.AST) -> Dict[str, Any]:
        """Calculate code metrics."""
        return {
            "class_count": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
            "method_count": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
            "complexity_score": self._calculate_complexity(tree)
        }
    
    def _calculate_complexity(self, tree: ast.AST) -> float:
        """Calculate code complexity score."""
        complexity = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(node, ast.FunctionDef):
                complexity += len(node.args.args) * 0.1
                
        return round(complexity, 2)
EOF

echo "✨ Pattern detection completed!"
