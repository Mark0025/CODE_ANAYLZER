from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional
import difflib

class AnalysisFormatter:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def create_diff(self, original: str, updated: str) -> str:
        """Create a git-style diff between original and updated code"""
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile='original',
            tofile='updated'
        )
        return ''.join(diff)

    def format_analysis(self, file_path: str, analysis_result: str) -> Dict:
        """Format analysis results into structured output"""
        return {
            "analysis_id": f"analysis_{self.timestamp}",
            "file_path": str(Path(file_path).relative_to(self.base_path)),
            "status": "needs_update",  # We'll make this dynamic later
            "issues": self._parse_analysis(analysis_result),
            "timestamp": self.timestamp
        }

    def _parse_analysis(self, analysis: str) -> List[Dict]:
        """Parse the analysis text into structured issues"""
        # We'll enhance this to better parse the AI output
        issues = []
        current_issue = None
        
        for line in analysis.split('\n'):
            if line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                if current_issue:
                    issues.append(current_issue)
                current_issue = {
                    "type": "improvement",
                    "description": line.split('.', 1)[1].strip(),
                    "suggested_fix": {
                        "code_before": "",
                        "code_after": "",
                        "git_patch": ""
                    },
                    "breaking_changes": [],
                    "dependencies": {
                        "affected_files": [],
                        "required_updates": []
                    }
                }
        
        if current_issue:
            issues.append(current_issue)
            
        return issues

    def save_analysis(self, analysis: Dict, output_dir: Path) -> Path:
        """Save analysis results as JSON"""
        output_file = output_dir / f"analysis_{self.timestamp}.json"
        output_file.write_text(json.dumps(analysis, indent=2))
        return output_file 