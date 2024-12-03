from crewai import Task
from typing import Dict, Any

class CleanupTask(Task):
    """Task for cleaning up codebase."""
    
    def __init__(self, path: str):
        super().__init__(
            description=f"""Clean up this codebase:
            Path: {path}
            
            1. Consolidate similar files
            2. Remove duplicates
            3. Organize structure
            4. Update documentation
            
            Provide specific changes to make.
            """,
            expected_output="Detailed cleanup plan"
        )
        self.path = path
    
    async def execute(self) -> Dict[str, Any]:
        """Execute cleanup task."""
        # Analyze structure
        structure = self.analyze_structure()
        
        # Find consolidation opportunities
        consolidation = self.find_consolidation(structure)
        
        # Create cleanup plan
        plan = self.create_plan(consolidation)
        
        return {
            "structure": structure,
            "consolidation": consolidation,
            "plan": plan
        } 