from datetime import datetime
import pendulum
from pathlib import Path
from typing import Dict, List, Any
from loguru import logger
from crewai import Agent, Task, Crew
from .base_crew import BaseCrew
import os
import json
from .github_integration import GitHubIntegration

class PRGeneratorCrew(BaseCrew):
    """Crew responsible for generating GitHub PRs from analysis results."""
    
    def __init__(self, target_path: str):
        super().__init__("PRGenerator", target_path)
        self.github = GitHubIntegration()
        
        self.pr_architect = Agent(
            role='PR Architect',
            goal='Design clear, focused pull requests',
            backstory="""You are an expert software architect who excels at breaking down 
            changes into logical, reviewable pull requests. You understand git workflows 
            and best practices for code reviews.""",
            verbose=True
        )
        
        self.code_improver = Agent(
            role='Code Improver',
            goal='Implement code improvements',
            backstory="""You are a senior developer who can implement code improvements
            while maintaining project consistency. You write clean, tested code.""",
            verbose=True
        )
        
        self.pr_writer = Agent(
            role='PR Writer',
            goal='Create clear PR descriptions',
            backstory="""You excel at writing clear, detailed pull request descriptions
            that explain changes, rationale, and testing approaches.""",
            verbose=True
        )

    async def generate_prs(self, analysis_results: Dict) -> List[Dict]:
        """Generate pull requests from analysis results."""
        try:
            # First, plan the PRs
            plan_task = Task(
                description=f"""Review these analysis results and plan logical PRs:
                {json.dumps(analysis_results, indent=2)}
                
                Break changes into focused, reviewable PRs following these rules:
                1. Each PR should address one concern
                2. Changes should be testable
                3. PRs should be ordered by dependency
                4. Include clear success criteria
                """,
                expected_output="Structured PR plan with dependencies",
                agent=self.pr_architect
            )

            # Then, implement changes
            implement_task = Task(
                description="""For each planned PR:
                1. Implement the code changes
                2. Add/update tests
                3. Verify improvements
                4. Document changes
                """,
                expected_output="Implemented changes with tests",
                agent=self.code_improver
            )

            # Finally, write PR descriptions
            describe_task = Task(
                description="""Create detailed PR descriptions including:
                1. Clear title and summary
                2. Problem being solved
                3. Implementation approach
                4. Testing strategy
                5. Rollback plan
                """,
                expected_output="PR descriptions and metadata",
                agent=self.pr_writer
            )

            crew = Crew(
                agents=[self.pr_architect, self.code_improver, self.pr_writer],
                tasks=[plan_task, implement_task, describe_task],
                verbose=True
            )

            results = crew.kickoff()
            
            # Save PR data
            self._save_pr_data(results)
            
            # Create PRs on GitHub
            pr_results = []
            for pr in self._format_prs(results):
                github_pr = await self.github.create_pr(pr)
                pr_results.append({
                    **pr,
                    **github_pr
                })
            
            return pr_results

        except Exception as e:
            logger.error(f"PR generation failed: {e}")
            return []

    def _save_pr_data(self, results: List[Dict]) -> None:
        """Save PR data for tracking."""
        output_dir = Path("core/output/prs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = pendulum.now().format("YYYYMMDD_HHmmss")
        
        # Save raw results
        pr_file = output_dir / f"prs_{timestamp}.json"
        pr_file.write_text(json.dumps({
            "timestamp": pendulum.now().isoformat(),
            "prs": results,
            "status": "pending",
            "target_repo": os.getenv("TARGET_REPO"),
            "target_dir": os.getenv("TARGET_DIR")
        }, indent=2))

    def _format_prs(self, results: List[Dict]) -> List[Dict]:
        """Format PR data for GitHub."""
        prs = []
        for pr_data in results:
            pr = {
                "title": pr_data["title"],
                "body": self._format_pr_body(pr_data),
                "branch": f"fix/{pr_data['id']}",
                "changes": pr_data["changes"],
                "tests": pr_data["tests"],
                "dependencies": pr_data.get("dependencies", []),
                "status": "ready",
                "created_at": pendulum.now().isoformat()
            }
            prs.append(pr)
        return prs

    def _format_pr_body(self, pr_data: Dict) -> str:
        """Format PR description in GitHub markdown."""
        return f"""
# {pr_data['title']}

## Problem
{pr_data['problem']}

## Solution
{pr_data['solution']}

## Implementation
{pr_data['implementation']}

## Testing
{pr_data['testing']}

## Rollback Plan
{pr_data['rollback']}

## Dependencies
{self._format_dependencies(pr_data.get('dependencies', []))}

## Success Criteria
{self._format_criteria(pr_data['criteria'])}
"""

    def _format_dependencies(self, deps: List[str]) -> str:
        """Format PR dependencies."""
        if not deps:
            return "No dependencies"
        return "\n".join(f"- {dep}" for dep in deps)

    def _format_criteria(self, criteria: List[str]) -> str:
        """Format success criteria."""
        return "\n".join(f"- [ ] {criterion}" for criterion in criteria) 