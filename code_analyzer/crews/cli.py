from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from crewai import Task, Crew, Agent
from loguru import logger
from typing import Dict, Any, List
from .base_crew import BaseCrew

class CLICrew(BaseCrew):
    """CrewAI-based CLI crew."""
    
    def __init__(self, target_path: str):
        super().__init__("CLI", target_path)
        self.console = Console()
        
        # Initialize agents
        self.command_agent = Agent(
            role="Command Handler",
            goal="Process CLI commands effectively",
            backstory="Expert at handling command-line operations"
        )
        
        self.output_agent = Agent(
            role="Output Formatter",
            goal="Format output clearly",
            backstory="Expert at creating readable CLI output"
        )
        
    async def handle_command(self, command: str) -> Dict[str, Any]:
        """Handle CLI command with resource management."""
        async with self.managed_operation():
            try:
                # Process command
                command_task = Task(
                    description=f"Process command: {command}",
                    agent=self.command_agent
                )
                
                # Format output
                output_task = Task(
                    description="Format command output",
                    agent=self.output_agent
                )
                
                crew = Crew(
                    agents=[self.command_agent, self.output_agent],
                    tasks=[command_task, output_task],
                    verbose=True
                )
                
                results = crew.kickoff()
                
                return {
                    "status": "completed",
                    "command": command,
                    "output": results,
                    "timestamp": self.get_timestamp()
                }
                
            except Exception as e:
                self.logger.error(f"Command handling failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                }
                
    def display_results(self, results: Dict[str, Any]) -> None:
        """Display results in a rich table."""
        table = Table(title="Command Results")
        table.add_column("Component")
        table.add_column("Status")
        table.add_column("Details")
        
        for key, value in results.items():
            if key != "timestamp":
                table.add_row(
                    key,
                    "✅" if value and value != "failed" else "❌",
                    str(value)
                )
                
        self.console.print(table) 