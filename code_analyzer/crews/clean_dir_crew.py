from pathlib import Path
from typing import Dict, Any
from loguru import logger
from crewai import Task, Agent, Crew
from .base_crew import BaseCrew

class CleanDirCrew(BaseCrew):
    """Crew for analyzing and cleaning code directories."""
    
    def __init__(self, target_path: str):
        super().__init__("CleanDir", target_path)
        
        # Create specialized agents
        self.structure_analyzer = Agent(
            role="Structure Analyzer",
            goal="Analyze code structure and organization",
            backstory="Expert at code organization and architecture"
        )
        
        self.consolidation_advisor = Agent(
            role="Consolidation Advisor",
            goal="Recommend code consolidation opportunities",
            backstory="Expert at code optimization and cleanup"
        )
        
    async def analyze_directory(self) -> Dict[str, Any]:
        """Analyze directory for cleanup opportunities."""
        async with self.managed_operation():
            try:
                # Create analysis task
                analysis_task = Task(
                    description=f"Analyze this codebase: {self.target_path}",
                    agent=self.structure_analyzer
                )
                
                # Create consolidation task
                consolidation_task = Task(
                    description="Recommend consolidation opportunities",
                    agent=self.consolidation_advisor
                )
                
                crew = Crew(
                    agents=[self.structure_analyzer, self.consolidation_advisor],
                    tasks=[analysis_task, consolidation_task],
                    verbose=True
                )
                
                results = crew.kickoff()
                
                return {
                    "status": "completed",
                    "timestamp": self.get_timestamp(),
                    "results": results
                }
                
            except Exception as e:
                self.logger.error(f"Directory analysis failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                } 