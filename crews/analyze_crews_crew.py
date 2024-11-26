from datetime import datetime
import pendulum
from pathlib import Path
from typing import Dict, List, Any
from loguru import logger
from crewai import Agent, Task, Crew
from .base_crew import BaseCrew
import aiohttp
import json
from datetime import timedelta
from dotenv import load_dotenv
import os
from openai import OpenAI

class AnalyzeCrewsCrew(BaseCrew):
    """Meta-crew that analyzes CrewAI ecosystem and updates development strategies."""
    
    def __init__(self, target_path: str):
        """Initialize the meta-analysis crew."""
        super().__init__("AnalyzeCrews", target_path)
        
        # Initialize OpenAI client directly
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Update all agents with direct OpenAI config
        self.version_tracker = Agent(
            role='Version Tracker',
            goal='Track CrewAI updates and best practices',
            backstory="""You monitor CrewAI's GitHub, PyPI, and community channels 
            for updates, new features, and evolving best practices.""",
            verbose=True,
            llm_config={
                "api_key": os.getenv('OPENAI_API_KEY'),
                "model": "gpt-3.5-turbo"
            }
        )
        
        # Create specialized agents
        self.ecosystem_scanner = Agent(
            role='CrewAI Ecosystem Scanner',
            goal='Map the entire CrewAI ecosystem',
            backstory="""You are an expert at discovering and analyzing how developers 
            are using CrewAI across GitHub and documentation.""",
            verbose=True,
            llm_config={
                "api_key": os.getenv('OPENAI_API_KEY'),
                "model": "gpt-3.5-turbo"
            }
        )
        
        self.pattern_analyzer = Agent(
            role='Pattern Analyzer',
            goal='Identify successful CrewAI implementation patterns',
            backstory="""You are a senior AI architect who excels at identifying 
            successful patterns in how developers are using CrewAI. You can spot 
            trends and best practices.""",
            verbose=True
        )
        
        self.rules_engineer = Agent(
            role='Rules Engineer',
            goal='Create and update development rules based on findings',
            backstory="""You are an expert at creating development rules and 
            guidelines. You can translate patterns and best practices into 
            clear, actionable rules.""",
            verbose=True
        )

    async def analyze_ecosystem(self) -> Dict[str, Any]:
        """Analyze the CrewAI ecosystem and generate insights."""
        try:
            # Add version check task
            version_task = Task(
                description="""Track and analyze CrewAI updates:
                1. Check latest PyPI version
                2. Monitor GitHub releases
                3. Review recent issues/PRs
                4. Analyze release notes
                5. Identify breaking changes
                
                Ensure we're using the latest features effectively.
                """,
                expected_output="Version analysis and update recommendations",
                agent=self.version_tracker
            )

            # Task 1: Scan Ecosystem
            scan_task = Task(
                description="""Scan and map the CrewAI ecosystem:
                1. GitHub repositories using CrewAI
                2. Blog posts and articles
                3. YouTube tutorials and demos
                4. Documentation and examples
                5. Community discussions
                
                Create a comprehensive map of how people are using CrewAI.
                """,
                expected_output="Detailed ecosystem map with sources and patterns",
                agent=self.ecosystem_scanner
            )

            # Task 2: Analyze Patterns
            analysis_task = Task(
                description="""Analyze the ecosystem data to identify:
                1. Common implementation patterns
                2. Successful approaches
                3. Novel use cases
                4. Best practices
                5. Anti-patterns to avoid
                
                Focus on how developers are leveraging CrewAI's strengths.
                """,
                expected_output="Pattern analysis with concrete examples",
                agent=self.pattern_analyzer
            )

            # Task 3: Generate Rules
            rules_task = Task(
                description="""Create development rules based on findings:
                1. Update .currsorules format
                2. Define AI-first approaches
                3. Document successful patterns
                4. Create implementation guidelines
                5. Define best practices
                
                Format as structured rules that can be added to .currsorules.
                """,
                expected_output="Updated .currsorules content",
                agent=self.rules_engineer
            )

            crew = Crew(
                agents=[
                    self.version_tracker,  # Add version tracker
                    self.ecosystem_scanner,
                    self.pattern_analyzer,
                    self.rules_engineer
                ],
                tasks=[
                    version_task,  # Check versions first
                    scan_task,
                    analysis_task,
                    rules_task
                ],
                verbose=True
            )

            results = crew.kickoff()
            
            # Save results and update rules
            self._save_analysis(results)
            
            # Schedule next update
            self._schedule_next_update()
            
            return {
                "timestamp": pendulum.now().isoformat(),
                "ecosystem_map": results[1],  # Scan results
                "patterns": results[2],      # Analysis results
                "rules_update": results[3],  # New rules
                "version_info": {           # Add version info
                    "current_version": results[0].get("current_version"),
                    "latest_version": results[0].get("latest_version"),
                    "update_needed": results[0].get("update_needed"),
                    "breaking_changes": results[0].get("breaking_changes", [])
                },
                "summary": {
                    "sources_analyzed": len(results[1].get("sources", [])),
                    "patterns_identified": len(results[2].get("patterns", [])),
                    "rules_generated": len(results[3].get("rules", [])),
                    "analyzed_at": pendulum.now().isoformat(),
                    "next_update": self._get_next_update_time()
                }
            }
            
        except Exception as e:
            logger.error(f"Ecosystem analysis failed: {e}")
            return {
                "timestamp": pendulum.now().isoformat(),
                "error": str(e),
                "status": "failed"
            }

    async def _check_latest_version(self) -> Dict[str, str]:
        """Check latest CrewAI version from PyPI."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://pypi.org/pypi/crewai/json') as response:
                    data = await response.json()
                    return {
                        "latest_version": data["info"]["version"],
                        "release_date": data["releases"][data["info"]["version"]][0]["upload_time"]
                    }
        except Exception as e:
            logger.error(f"Failed to check latest version: {e}")
            return {"error": str(e)}

    def _schedule_next_update(self) -> None:
        """Schedule next ecosystem analysis."""
        next_update = pendulum.now().add(days=1)  # Daily updates
        update_file = Path("crews/crew-output/ecosystem-analysis/next_update.json")
        update_file.write_text(json.dumps({
            "next_update": next_update.isoformat(),
            "frequency": "daily"
        }))

    def _get_next_update_time(self) -> str:
        """Get next scheduled update time."""
        update_file = Path("crews/crew-output/ecosystem-analysis/next_update.json")
        if update_file.exists():
            data = json.loads(update_file.read_text())
            return data["next_update"]
        return pendulum.now().add(days=1).isoformat()

    def _save_analysis(self, results: Dict) -> None:
        """Save analysis results to local storage."""
        output_dir = Path("crews/crew-output/ecosystem-analysis")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save raw results
        (output_dir / f"analysis_{pendulum.now().strftime('%Y%m%d_%H%M%S')}.json").write_text(
            str(results)
        )
        
        # Update .currsorules if new rules were generated
        if "rules" in results:
            self._update_currsorules(results["rules"])
            
    def _update_currsorules(self, new_rules: Dict) -> None:
        """Update .currsorules with new rules and versioning."""
        rules_file = Path(".currsorules")
        if rules_file.exists():
            current_rules = rules_file.read_text()
            
            # Add version info section if not exists
            if "version_tracking" not in current_rules:
                current_rules += "\n\nversion_tracking:\n  last_updated: {}\n  crewai_version: {}".format(
                    pendulum.now().isoformat(),
                    new_rules.get("version_info", {}).get("current_version", "unknown")
                )
            
            # Smart merge of new rules
            rules_file.write_text(current_rules + "\n\n# New Rules (Added {})\n".format(
                pendulum.now().format("YYYY-MM-DD HH:mm:ss")
            ) + str(new_rules))