"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
from crewai import Agent, Task, Crew
import yaml
from code_analyzer.crews.base_crew import BaseCrew

class DevUpdaterCrew(BaseCrew):
    """Crew for handling systematic codebase updates."""
    
    def __init__(self, target_path: str):
        super().__init__("DevUpdater", target_path)
        
        # Specialized agents
        self.analyzer_agent = Agent(
            role="Update Analyzer",
            goal="Analyze required codebase updates",
            backstory="Expert at understanding code patterns and required changes"
        )
        
        self.planner_agent = Agent(
            role="Update Planner",
            goal="Plan systematic code updates",
            backstory="Expert at planning and organizing code changes"
        )
        
        self.executor_agent = Agent(
            role="Update Executor",
            goal="Execute code updates safely",
            backstory="Expert at implementing code changes with precision"
        )
        
    async def plan_updates(self, update_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Plan updates based on specification."""
        async with self.managed_operation():
            try:
                # Analyze required updates
                analysis_task = Task(
                    description=f"""
                    Analyze these updates:
                    {yaml.dump(update_spec, default_flow_style=False)}
                    
                    Consider:
                    1. Files needing updates
                    2. Pattern changes required
                    3. Potential risks
                    4. Dependencies affected
                    """,
                    agent=self.analyzer_agent
                )
                
                # Create update plan
                planning_task = Task(
                    description="""
                    Create detailed update plan including:
                    1. Order of updates
                    2. Required changes per file
                    3. Validation steps
                    4. Rollback procedures
                    """,
                    agent=self.planner_agent
                )
                
                crew = Crew(
                    agents=[self.analyzer_agent, self.planner_agent],
                    tasks=[analysis_task, planning_task],
                    verbose=True
                )
                
                results = crew.kickoff()
                
                return {
                    "status": "completed",
                    "timestamp": self.get_timestamp(),
                    "update_plan": results
                }
                
            except Exception as e:
                self.logger.error(f"Update planning failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                }
                
    async def execute_updates(self, update_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute planned updates with safety checks."""
        async with self.managed_operation():
            try:
                execution_task = Task(
                    description=f"""
                    Execute these updates:
                    {yaml.dump(update_plan, default_flow_style=False)}
                    
                    Follow these steps:
                    1. Backup affected files
                    2. Apply changes systematically
                    3. Validate each change
                    4. Report progress
                    """,
                    agent=self.executor_agent
                )
                
                crew = Crew(
                    agents=[self.executor_agent],
                    tasks=[execution_task],
                    verbose=True
                )
                
                results = crew.kickoff()
                
                return {
                    "status": "completed",
                    "timestamp": self.get_timestamp(),
                    "updates_applied": results
                }
                
            except Exception as e:
                self.logger.error(f"Update execution failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                } 