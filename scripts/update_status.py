#!/usr/bin/env python3
"""Update project status manually."""
import click
from code_analyzer.crews.status_crew import StatusCrew
from pathlib import Path
from rich.console import Console
from rich.table import Table
import asyncio

console = Console()

@click.group()
def cli():
    """Project status management tools."""
    pass

@cli.command()
@click.option('--message', '-m', help='Status update message')
def update(message: str):
    """Manually update project status."""
    status_crew = StatusCrew()
    asyncio.run(status_crew.track_status())
    console.print("[green]Status updated successfully!")

@cli.command()
def analyze():
    """Analyze current output directory."""
    status_crew = StatusCrew()
    results = asyncio.run(status_crew.track_status())
    
    # Create pretty table
    table = Table(title="Crew Status")
    table.add_column("Crew")
    table.add_column("Last Run")
    table.add_column("Status")
    
    if "crews" in results:
        for crew, data in results["crews"].items():
            table.add_row(
                crew,
                data.get("last_run", "Unknown"),
                data.get("status", "Unknown")
            )
    
    console.print(table)

@cli.command()
def show():
    """Show current project status."""
    status_crew = StatusCrew()
    results = asyncio.run(status_crew.track_status())
    
    console.print("[bold blue]Project Status[/bold blue]")
    console.print(f"Last Updated: {results.get('timestamp', 'Unknown')}")
    
    if "metrics" in results:
        metrics = results["metrics"]
        console.print(f"\nTest Coverage: {metrics.get('coverage', 0)}%")
        console.print(f"Tests: {metrics.get('passing', 0)}/{metrics.get('total', 0)}")

if __name__ == "__main__":
    cli() 