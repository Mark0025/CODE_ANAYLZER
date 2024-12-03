#!/bin/bash
set -e

echo "🏗️ Adding Pattern Detection Methods..."

# Add methods to pattern_detector.py
cat >> code_analyzer/crews/analysis_crews/pattern_detector.py << 'EOF'

    async def _detect_code_smells(self, tree: ast.AST) -> List[PatternMatch]:
        """Detect code smells in AST."""
        patterns = []
        
        # Check for long methods
        if isinstance(tree, ast.FunctionDef):
            if len(tree.body) > 20:  # More than 20 lines
                patterns.append(PatternMatch(
                    type="code_smell",
                    name="long_method",
                    location={"function": tree.name},
                    confidence=0.9,
                    description="Method is too long",
                    suggestion="Consider breaking into smaller functions"
                ))
        
        return patterns

    def _is_singleton(self, tree: ast.AST) -> bool:
        """Check if class follows singleton pattern."""
        if not isinstance(tree, ast.ClassDef):
            return False
            
        # Look for private instance variable
        has_private_instance = False
        # Look for getInstance method
        has_get_instance = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id.startswith('_instance'):
                has_private_instance = True
            if isinstance(node, ast.FunctionDef) and node.name == 'getInstance':
                has_get_instance = True
                
        return has_private_instance and has_get_instance

    def _get_class_name(self, tree: ast.AST) -> str:
        """Get class name from AST node."""
        if isinstance(tree, ast.ClassDef):
            return tree.name
        return ""

    def _is_factory(self, tree: ast.AST) -> bool:
        """Check if class follows factory pattern."""
        if not isinstance(tree, ast.ClassDef):
            return False
            
        # Look for create methods
        create_methods = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and (
                node.name.startswith('create') or 
                node.name.startswith('make') or
                node.name.startswith('build')
            ):
                create_methods += 1
                
        return create_methods > 0

    async def analyze_patterns(self, code: str) -> Dict[str, List[PatternMatch]]:
        """Analyze code for all patterns."""
        tree = ast.parse(code)
        
        # Store results in database
        db = DatabaseManager()
        results = {
            "code_smells": await self._detect_code_smells(tree),
            "design_patterns": []
        }
        
        # Save to database
        db.save_crew_output(
            crew_name="pattern_detector",
            output_type="pattern_analysis",
            status="completed",
            results=results
        )
        
        return results
EOF

# Add imports at top
sed -i '' '1i\
import ast\
from typing import List, Dict\
from code_analyzer.models.db_manager import DatabaseManager\
' code_analyzer/crews/analysis_crews/pattern_detector.py

echo "✨ Pattern detection methods added!"
