"""Helper functions for code analysis."""
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger

def get_file_type(path: Path) -> str:
    """Get file type from extension.
    
    Args:
        path: Path to file
        
    Returns:
        File type as string (e.g. 'python', 'markdown')
    """
    ext = path.suffix.lower()
    type_map = {
        '.py': 'python',
        '.md': 'markdown',
        '.txt': 'text'
    }
    return type_map.get(ext, 'unknown')

def filter_files(files: List[Path], ignore_patterns: List[str]) -> List[Path]:
    """Filter files based on ignore patterns."""
    return [f for f in files if not any(pattern in str(f) for pattern in ignore_patterns)] 

def format_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format analysis output consistently"""
    return {
        "timestamp": data.get("timestamp"),
        "analysis": data.get("analysis", {}),
        "metadata": {
            "file_count": data.get("file_count", 0),
            "line_count": data.get("line_count", 0)
        }
    } 