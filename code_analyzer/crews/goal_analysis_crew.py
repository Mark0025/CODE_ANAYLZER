"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
from pathlib import Path
from typing import Dict, Any
from crewai import Task
from .base_crew import BaseCrew
from loguru import logger

class GoalAnalysisCrew(BaseCrew):
    """Analyzes .md files to understand project goals and direction."""
    
    def __init__(self, docs_path: str = "DEV-MAN-CREW"):
        super().__init__("GoalAnalysis", docs_path)
        
    async def analyze_goals(self) -> Dict[str, Any]:
        """Analyze all .md files to extract goals and direction."""
        try:
            # Gather all .md files
            md_files = list(Path(self.target_path).rglob("*.md"))
            
            # Create analysis task
            task = Task(
                description=f"""Analyze these documentation files:
                Files: {[str(f) for f in md_files]}
                
                Extract:
                1. Current project goals
                2. Implementation status
                3. Next steps
                4. Success metrics
                
                Provide a cohesive understanding of project direction.
                """,
                agent=self.status_agent
            )
            
            # Run analysis
            results = await self.handle_task_output(task, "goal")
            
            # Update status files
            await self._update_goal_status(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Goal analysis failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
            
    async def _update_goal_status(self, results: Dict[str, Any]):
        """Update goal-related status files."""
        # Update GOALS.md
        goals_file = Path("DEV-MAN-CREW/GOALS.md")
        if goals_file.exists():
            current = goals_file.read_text()
            goals_file.write_text(f"# Latest Goals\n\n{results['goal_analysis']['summary']}\n\n---\n\n{current}") 