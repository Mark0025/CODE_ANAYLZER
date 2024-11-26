from pathlib import Path
import subprocess
from typing import List, Dict
from rich.console import Console
from rich.table import Table
import os

class DebugSearcher:
    """Search codebase for patterns and debug information."""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.console = Console()
        
    def search_pattern(self, pattern: str, exclude_dirs: List[str] = None) -> Dict:
        """Search for pattern in codebase."""
        if exclude_dirs is None:
            exclude_dirs = ['.git', '__pycache__', '.venv', 'node_modules']
            
        # Create grep command
        grep_cmd = f'grep -r "{pattern}" {self.root_dir}'
        
        # Add exclusions
        for dir_name in exclude_dirs:
            grep_cmd += f' --exclude-dir="{dir_name}"'
            
        # Run search
        try:
            result = subprocess.run(
                grep_cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            
            # Parse results
            findings = []
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line:
                        file_path, content = line.split(':', 1)
                        findings.append({
                            'file': file_path,
                            'content': content.strip()
                        })
                        
            # Display results
            table = Table(title=f"Search Results for: {pattern}")
            table.add_column("File", style="cyan")
            table.add_column("Content", style="yellow")
            
            for find in findings:
                table.add_row(find['file'], find['content'])
                
            self.console.print(table)
            
            return {
                'pattern': pattern,
                'findings': findings,
                'count': len(findings)
            }
            
        except Exception as e:
            self.console.print(f"Search failed: {e}", style="red")
            return {'error': str(e)} 