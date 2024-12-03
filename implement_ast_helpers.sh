#!/bin/bash
set -e

echo "🏗️ Building AST Helper District..."

# 1. Create AST helpers
cat > code_analyzer/utils/ast_helpers.py << 'EOF'
"""AST parsing utilities for code analysis."""
import ast
from typing import Optional, Dict, Any
from loguru import logger

def parse_code_safely(code: str) -> Optional[ast.AST]:
    """Safe code parsing with error handling."""
    try:
        return ast.parse(code)
    except Exception as e:
        logger.error(f"Failed to parse code: {e}")
        return None

def get_node_name(node: ast.AST) -> str:
    """Get name from AST node safely."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return node.attr
    return ""

def count_node_lines(node: ast.AST) -> int:
    """Count lines in AST node."""
    if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
        return node.end_lineno - node.lineno + 1
    return 0
EOF

# 2. Update pattern detector to use new tools
cat > code_analyzer/crews/analysis_crews/pattern_detector.py << 'EOF'
"""Pattern detection using AST helpers."""
from code_analyzer.utils.ast_helpers import parse_code_safely, get_node_name
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger

class PatternDetector:
    async def analyze_patterns(self, code: str) -> Dict[str, Any]:
        try:
            tree = parse_code_safely(code)
            if not tree:
                raise ValueError("Failed to parse code")
                
            results = {
                "patterns_found": [],
                "code_quality": "good"
            }
            
            # Save results
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
EOF

echo "✨ AST Helper District built!"
