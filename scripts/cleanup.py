from pathlib import Path
from typing import Dict, Any
from loguru import logger
from rich.console import Console
from rich.table import Table
from datetime import datetime
import json
import shutil

console = Console()

class CodebaseAnalyzer:
    """Analyze codebase structure and suggest improvements."""
    
    def __init__(self):
        self.tmp_dir = Path("../tmp")
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    async def analyze(self) -> Dict[str, Any]:
        """Analyze codebase and create report."""
        from code_analyzer.crews.clean_dir_crew import CleanDirCrew
        
        # Run analysis
        crew = CleanDirCrew(".")
        results = await crew.analyze_directory()
        
        # Create report
        report = self._create_report(results)
        
        # Save report
        self._save_report(report)
        
        return report
    
    def _create_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed analysis report."""
        report = {
            "timestamp": self.timestamp,
            "suggestions": [],
            "safety_checks": [],
            "benefits": []
        }
        
        # Analyze file structure
        duplicate_files = self._find_duplicates()
        similar_content = self._find_similar_content()
        
        # Add suggestions
        if duplicate_files:
            report["suggestions"].append({
                "type": "consolidation",
                "files": duplicate_files,
                "reason": "Duplicate files found",
                "benefit": "Reduce code duplication"
            })
            
        if similar_content:
            report["suggestions"].append({
                "type": "merge",
                "files": similar_content,
                "reason": "Similar content found",
                "benefit": "Improve code organization"
            })
            
        # Add safety checks
        report["safety_checks"] = [
            {"test_coverage": self._check_test_coverage()},
            {"git_status": self._check_git_status()},
            {"backup_status": self._check_backups()}
        ]
        
        return report
    
    def _save_report(self, report: Dict[str, Any]):
        """Save analysis report."""
        # Save JSON
        json_file = self.tmp_dir / f"cleanup_analysis_{self.timestamp}.json"
        json_file.write_text(json.dumps(report, indent=2))
        
        # Create markdown report
        md_content = self._create_markdown(report)
        md_file = self.tmp_dir / f"cleanup_analysis_{self.timestamp}.md"
        md_file.write_text(md_content)
        
        console.print(f"\n[green]Reports saved to:[/green]")
        console.print(f"JSON: {json_file}")
        console.print(f"Markdown: {md_file}")
    
    def _create_markdown(self, report: Dict[str, Any]) -> str:
        """Create markdown report."""
        md = f"""# Codebase Cleanup Analysis
Generated: {self.timestamp}

## Suggested Changes

"""
        # Add suggestions
        for suggestion in report["suggestions"]:
            md += f"""### {suggestion['type'].title()}
- **Files**: {', '.join(suggestion['files'])}
- **Reason**: {suggestion['reason']}
- **Benefit**: {suggestion['benefit']}

"""

        # Add safety checks
        md += "\n## Safety Checks\n"
        for check in report["safety_checks"]:
            for key, value in check.items():
                md += f"- **{key}**: {value}\n"
                
        return md
    
    def _find_duplicates(self) -> list:
        """Find duplicate files."""
        duplicates = []
        seen = {}
        
        for file in Path(".").rglob("*.py"):
            content = file.read_text()
            if content in seen:
                duplicates.append((str(file), seen[content]))
            else:
                seen[content] = str(file)
                
        return duplicates
    
    def _find_similar_content(self) -> list:
        """Find files with similar content."""
        from difflib import SequenceMatcher
        similar = []
        
        files = list(Path(".").rglob("*.py"))
        for i, file1 in enumerate(files):
            for file2 in files[i+1:]:
                content1 = file1.read_text()
                content2 = file2.read_text()
                ratio = SequenceMatcher(None, content1, content2).ratio()
                if ratio > 0.7:  # 70% similarity
                    similar.append((str(file1), str(file2), ratio))
                    
        return similar
    
    def _check_test_coverage(self) -> str:
        """Check test coverage."""
        try:
            import pytest
            import coverage
            cov = coverage.Coverage()
            cov.start()
            pytest.main(["tests/"])
            cov.stop()
            cov.save()
            return f"{cov.report()}% coverage"
        except Exception as e:
            return f"Unable to check coverage: {e}"
    
    def _check_git_status(self) -> str:
        """Check git status."""
        try:
            import git
            repo = git.Repo(".")
            return "Clean" if not repo.is_dirty() else "Has uncommitted changes"
        except Exception as e:
            return f"Unable to check git status: {e}"
    
    def _check_backups(self) -> str:
        """Check backup status."""
        backup_dir = Path("backup")
        return "Exists" if backup_dir.exists() else "No backups found"

# Add to CLI
@click.command()
@click.option('--analyze', is_flag=True, help='Analyze codebase')
def cleanup(analyze):
    """Analyze codebase for cleanup opportunities."""
    if analyze:
        analyzer = CodebaseAnalyzer()
        results = analyzer.analyze()
        console.print("[bold green]Analysis complete! Check ../tmp for reports.[/bold green]") 