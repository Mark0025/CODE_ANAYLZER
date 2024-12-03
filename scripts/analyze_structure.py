#!/usr/bin/env python3
"""Analyze project structure without making changes."""
from pathlib import Path
from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from code_analyzer.crews.clean_dir_crew import CleanDirCrew
import asyncio
import json

console = Console()

async def analyze_safety():
    """Run safe analysis of project structure."""
    console.print("\n[bold blue]Running Safe Structure Analysis...[/bold blue]")
    
    # Initialize crew
    crew = CleanDirCrew(".")
    
    # Get current structure
    current_files = list(Path(".").rglob("*.py"))
    
    # Create structure tree
    tree = Tree("📁 Current Structure")
    for file in sorted(current_files):
        tree.add(f"[green]{file}[/green]")
    
    console.print(tree)
    
    # Run analysis
    results = await crew.analyze_directory()
    
    # Show recommendations
    console.print("\n[bold yellow]Recommendations:[/bold yellow]")
    
    table = Table(show_header=True)
    table.add_column("Type")
    table.add_column("File")
    table.add_column("Recommendation")
    table.add_column("Safety")
    
    for item in results.get("recommendations", []):
        table.add_row(
            item.get("type", "unknown"),
            item.get("file", ""),
            item.get("recommendation", ""),
            "✅" if item.get("safe", False) else "⚠️"
        )
    
    console.print(table)
    
    # Save analysis
    output_file = Path("DEV-MAN-CREW/WHATS-WORKING/structure_analysis.json")
    output_file.write_text(json.dumps(results, indent=2))
    
    console.print(f"\n[bold green]Analysis saved to {output_file}[/bold green]")
    
    return results

if __name__ == "__main__":
    asyncio.run(analyze_safety()) 