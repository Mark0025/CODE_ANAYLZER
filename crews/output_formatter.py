from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import difflib
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel
from rich.markdown import Markdown
from icecream import ic
from objprint import op
import os

class AnalysisFormatter:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.console = Console()
        
    def display_code_diff(self, original: str, updated: str) -> None:
        """Display beautiful code diff in terminal."""
        # Show original code
        self.console.print("\n[bold yellow]Original Code:[/]")
        self.console.print(Panel(Syntax(original, "python", theme="monokai")))
        
        # Show updated code
        self.console.print("\n[bold green]Improved Code:[/]")
        self.console.print(Panel(Syntax(updated, "python", theme="monokai")))
        
        # Show diff
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile='original',
            tofile='improved'
        )
        diff_text = ''.join(diff)
        if diff_text:
            self.console.print("\n[bold red]Changes Made:[/]")
            self.console.print(Panel(Syntax(diff_text, "diff", theme="monokai")))

    def display_analysis(self, analysis: Dict) -> None:
        """Display analysis results with enhanced formatting."""
        # Debug output
        ic(analysis)  # Show debug info
        
        # Print full object structure
        op.configure(line_numbers=True, color=True)
        op(analysis)  # Show detailed object structure
        
        # Rich formatting
        self.console.print("\n[bold magenta]Analysis Results[/]")
        
        # Create issues table
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Type", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Severity", style="yellow")
        
        for issue in analysis.get("issues", []):
            table.add_row(
                issue["type"],
                issue["description"],
                "🔴" if issue.get("severity") == "high" else 
                "🟡" if issue.get("severity") == "medium" else "🟢"
            )
        
        self.console.print(table)
        
        # Show code improvements
        if "improvements" in analysis:
            self.console.print("\n[bold green]Code Improvements:[/]")
            for imp in analysis["improvements"]:
                self.console.print(Panel(
                    Syntax(imp["code"], "python", theme="monokai"),
                    title=imp["description"],
                    border_style="green"
                ))

    def save_analysis(self, analysis: Dict, output_dir: Path) -> Path:
        """Save analysis results as JSON and generate HTML report."""
        # Save JSON
        output_file = output_dir / f"analysis_{self.timestamp}.json"
        output_file.write_text(json.dumps(analysis, indent=2))
        
        # Generate HTML report
        html_file = output_dir / f"analysis_{self.timestamp}.html"
        self._generate_html_report(analysis, html_file)
        
        return output_file

    def _generate_html_report(self, analysis: Dict, output_file: Path) -> None:
        """Generate beautiful HTML report."""
        from rich.markdown import Markdown
        
        # Convert analysis to markdown
        md_content = f"""
# Code Analysis Report

## Overview
- **Timestamp**: {analysis.get('timestamp')}
- **Files Analyzed**: {len(analysis.get('files', []))}
- **Issues Found**: {len(analysis.get('issues', []))}

## Issues
| Type | Description | Severity |
|------|-------------|----------|
"""
        
        for issue in analysis.get("issues", []):
            md_content += f"| {issue['type']} | {issue['description']} | {issue.get('severity', 'low')} |\n"
        
        # Convert markdown to HTML using Rich
        markdown = Markdown(md_content)
        console = Console(record=True, force_terminal=True)
        console.print(markdown)
        html = console.export_html()
        
        output_file.write_text(html)

    def format_pr_output(self, analysis: Dict) -> Dict:
        """Format analysis results for PR generation."""
        return {
            "metadata": {
                "timestamp": analysis.get("timestamp"),
                "target_repo": os.getenv("TARGET_REPO"),
                "target_dir": os.getenv("TARGET_DIR")
            },
            "changes": [
                {
                    "id": f"change_{i}",
                    "file": change.get("file"),
                    "type": change.get("type"),
                    "description": change.get("description"),
                    "implementation": change.get("implementation"),
                    "tests": change.get("tests", []),
                    "priority": change.get("priority", "medium")
                }
                for i, change in enumerate(analysis.get("changes", []))
            ],
            "pr_pipeline": {
                "status": "pending",
                "total_changes": len(analysis.get("changes", [])),
                "completed": 0,
                "next_up": analysis.get("changes", [])[0] if analysis.get("changes") else None
            }
        }

class CrewOutput(BaseModel):
    raw: str
    
    def __str__(self) -> str:
        return self.raw
    
    def split(self, *args, **kwargs) -> list:
        """Add split method to make string operations work"""
        return self.raw.split(*args, **kwargs)

def format_analysis(file_path: str, analysis_result: str) -> Dict[str, Any]:
    """Format analysis results."""
    return {
        "file": file_path,
        "analysis": str(analysis_result),
        "issues": _parse_analysis(analysis_result)
    } 

class OutputFormatter:
    """Format analysis results consistently"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        
    def format_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format analysis results"""
        return {
            "metadata": {
                "timestamp": results.get("timestamp"),
                "version": "0.1.0"
            },
            "analysis": {
                "original": results.get("original_code"),
                "improved": results.get("improved_code"),
                "suggestions": self._extract_suggestions(results)
            }
        }
        
    def _extract_suggestions(self, results: Dict) -> list:
        """Extract improvement suggestions"""
        if isinstance(results.get("improved_code"), str):
            # Parse suggestions from AI response
            suggestions = []
            for line in results["improved_code"].split("\n"):
                if line.startswith("-"):
                    suggestions.append(line[2:])
            return suggestions
        return []
        
    def save_results(self, results: Dict[str, Any], filename: str):
        """Save formatted results"""
        formatted = self.format_analysis(results)
        output_file = self.output_dir / filename
        
        with open(output_file, 'w') as f:
            json.dump(formatted, f, indent=2) 