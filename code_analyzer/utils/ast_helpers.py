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
