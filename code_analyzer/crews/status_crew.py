from pathlib import Path
from typing import Dict, Any
from loguru import logger
from crewai import Task, Agent, Crew
from .base_crew import BaseCrew

class StatusCrew(BaseCrew):
    """Crew for tracking project status."""
    
    def __init__(self, target_path: str):
        super().__init__("Status", target_path)
        
        self.status_agent = Agent(
            role="Status Tracker",
            goal="Track and analyze project status",
            backstory="Expert at monitoring project metrics and status"
        )
        
    async def track_status(self) -> Dict[str, Any]:
        """Track project status with resource management."""
        async with self.managed_operation():
            try:
                task = Task(
                    description="Track and analyze project status",
                    agent=self.status_agent
                )
                
                crew = Crew(
                    agents=[self.status_agent],
                    tasks=[task],
                    verbose=True
                )
                
                results = crew.kickoff()
                
                return {
                    "status": "completed",
                    "timestamp": self.get_timestamp(),
                    "results": results
                }
                
            except Exception as e:
                self.logger.error(f"Status tracking failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                } 