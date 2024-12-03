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
            backstory="Expert at monitoring CrewAI's ecosystem",
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
            backstory="Expert at discovering CrewAI patterns",
            verbose=True,
            llm_config={
                "api_key": os.getenv('OPENAI_API_KEY'),
                "model": "gpt-3.5-turbo"
            }
        )
        
        self.pattern_analyzer = Agent(
            role='Pattern Analyzer',
            goal='Identify successful CrewAI patterns',
            backstory="Expert at identifying implementation patterns",
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
        """Analyze the CrewAI ecosystem with resource management."""
        async with self.managed_operation():
            try:
                # Version check task
                version_task = Task(
                    description="Track and analyze CrewAI updates",
                    agent=self.version_tracker,
                    expected_output={
                        "current_version": str,
                        "latest_version": str,
                        "breaking_changes": list
                    }
                )
                
                # Ecosystem scan task
                scan_task = Task(
                    description="Scan and map the CrewAI ecosystem",
                    agent=self.ecosystem_scanner,
                    expected_output={
                        "ecosystem_map": dict,
                        "patterns": list
                    }
                )
                
                # Pattern analysis task
                analysis_task = Task(
                    description="Analyze implementation patterns",
                    agent=self.pattern_analyzer,
                    expected_output={
                        "patterns": list,
                        "recommendations": dict
                    }
                )
                
                crew = Crew(
                    agents=[
                        self.version_tracker,
                        self.ecosystem_scanner,
                        self.pattern_analyzer
                    ],
                    tasks=[
                        version_task,
                        scan_task,
                        analysis_task
                    ],
                    verbose=True
                )
                
                results = crew.kickoff()
                
                return {
                    "status": "completed",
                    "timestamp": self.get_timestamp(),
                    "ecosystem_map": results[1].get("ecosystem_map", {}),
                    "patterns": results[2].get("patterns", []),
                    "version_info": {
                        "current_version": results[0].get("current_version"),
                        "latest_version": results[0].get("latest_version"),
                        "breaking_changes": results[0].get("breaking_changes", [])
                    }
                }
                
            except Exception as e:
                self.logger.error(f"Ecosystem analysis failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                }
                
    async def _check_latest_version(self) -> Dict[str, str]:
        """Check latest CrewAI version from PyPI with resource management."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://pypi.org/pypi/crewai/json') as response:
                    data = await response.json()
                    return {
                        "latest_version": data["info"]["version"],
                        "release_date": data["releases"][data["info"]["version"]][0]["upload_time"]
                    }
        except Exception as e:
            self.logger.error(f"Failed to check latest version: {e}")
            return {"error": str(e)}

    def _schedule_next_update(self) -> None:
        """Schedule next ecosystem analysis."""
        next_update = pendulum.now().add(days=1)  # Daily updates
        update_file = Path("core/output/ecosystem-analysis/next_update.json")
        update_file.write_text(json.dumps({
            "next_update": next_update.isoformat(),
            "frequency": "daily"
        }))

    def _get_next_update_time(self) -> str:
        """Get next scheduled update time."""
        update_file = Path("core/output/ecosystem-analysis/next_update.json")
        if update_file.exists():
            data = json.loads(update_file.read_text())
            return data["next_update"]
        return pendulum.now().add(days=1).isoformat()

    def _save_analysis(self, results: Dict) -> None:
        """Save analysis results to local storage."""
        output_dir = Path("core/output/ecosystem-analysis")
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