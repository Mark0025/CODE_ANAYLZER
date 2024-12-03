"""Core analyzer module for code analysis."""
from pathlib import Path
from typing import Dict, Any, Optional, List, Set
from loguru import logger

class CodeAnalyzer:
    """Main code analyzer class."""
    
    IGNORE_DIRS = {
        'venv', '.venv', 'env', '.env',  # Virtual environments
        '__pycache__', '.pytest_cache',   # Cache directories
        '.git', '.hg', '.svn',            # Version control
        'node_modules', 'build', 'dist',   # Build directories
        'egg-info', '*.egg-info',         # Package info
    }
    
    def __init__(self, path: Optional[str] = None):
        """Initialize the analyzer.
        
        Args:
            path: Optional path to analyze
        """
        self.path = Path(path) if path else None
        self.logger = logger.bind(analyzer="CodeAnalyzer")
        self._files_seen: Set[str] = set()  # Track unique files
        
    def should_analyze_dir(self, path: Path) -> bool:
        """Check if a directory should be analyzed."""
        parts = path.parts
        return not any(part.startswith('.') or part in self.IGNORE_DIRS 
                      for part in parts)
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze the code at the specified path."""
        if not self.path:
            raise ValueError("No path specified for analysis")
            
        if not self.path.exists():
            raise FileNotFoundError(f"Path does not exist: {self.path}")
            
        self.logger.info(f"Starting analysis of {self.path}")
        
        results = {
            "status": "success",
            "path": str(self.path),
            "files_analyzed": [],
            "summary": {
                "total_files": 0,
                "python_files": 0,
                "other_files": 0,
                "directories_skipped": []
            }
        }
        
        try:
            # Analyze Python files
            for file_path in self.path.rglob("*.py"):
                # Convert to absolute path to handle symlinks
                abs_path = str(file_path.resolve())
                
                # Skip if we've seen this file before
                if abs_path in self._files_seen:
                    continue
                    
                # Skip if in ignored directory
                if not self.should_analyze_dir(file_path.parent):
                    dir_name = str(file_path.parent)
                    if dir_name not in results["summary"]["directories_skipped"]:
                        results["summary"]["directories_skipped"].append(dir_name)
                    continue
                
                self._files_seen.add(abs_path)
                results["files_analyzed"].append(str(file_path))
                results["summary"]["python_files"] += 1
                results["summary"]["total_files"] += 1
                
            self.logger.info(f"Analysis complete. Found {results['summary']['python_files']} Python files.")
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            results["status"] = "error"
            results["error"] = str(e)
            
        return results

def analyze_directory(path: str) -> Dict[str, Any]:
    """Analyze a directory of code.
    
    Args:
        path: Directory path to analyze
        
    Returns:
        Analysis results including file counts and any issues found
    """
    analyzer = CodeAnalyzer(path)
    return analyzer.analyze() 