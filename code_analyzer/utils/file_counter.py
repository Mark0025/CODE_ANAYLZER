"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
from pathlib import Path
from typing import Dict, List
import fnmatch

class FileCounter:
    """Accurate file counting with proper filtering."""
    
    def __init__(self, ignore_file: Path = Path(".codeA.ignore")):
        self.ignore_patterns = self._load_ignore_patterns(ignore_file)
        
    def _load_ignore_patterns(self, ignore_file: Path) -> List[str]:
        """Load patterns from .codeA.ignore."""
        if not ignore_file.exists():
            return []
        return [
            line.strip() for line in ignore_file.read_text().splitlines()
            if line.strip() and not line.startswith('#')
        ]
        
    def should_ignore(self, file_path: str) -> bool:
        """Check if file should be ignored."""
        for pattern in self.ignore_patterns:
            if pattern.startswith('!'):
                # Include pattern
                if fnmatch.fnmatch(file_path, pattern[1:]):
                    return False
            elif fnmatch.fnmatch(file_path, pattern):
                return True
        return False
        
    def count_files(self, path: Path) -> Dict[str, List[Path]]:
        """Count files by category."""
        categories = {
            "core": [],      # Core Python files
            "cli": [],       # CLI files
            "crews": [],     # Crew files
            "utils": [],     # Utility files
            "tests": [],     # Test files
            "docs": []       # Documentation
        }
        
        for file in path.rglob("*.py"):
            rel_path = str(file.relative_to(path))
            
            if self.should_ignore(rel_path):
                continue
                
            if "code_analyzer/core" in str(file):
                categories["core"].append(file)
            elif "code_analyzer/cli" in str(file):
                categories["cli"].append(file)
            elif "code_analyzer/crews" in str(file):
                categories["crews"].append(file)
            elif "code_analyzer/utils" in str(file):
                categories["utils"].append(file)
            elif "tests" in str(file):
                categories["tests"].append(file)
                
        return categories
        
    def estimate_cost(self, files: Dict[str, List[Path]]) -> float:
        """Estimate analysis cost."""
        # Cost per token: $0.01 per 1K tokens
        # Average Python file: ~200 tokens
        total_files = sum(len(f) for f in files.values())
        total_tokens = total_files * 200
        return (total_tokens / 1000) * 0.01 