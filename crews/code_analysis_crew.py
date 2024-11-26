from datetime import datetime
import pendulum
from pathlib import Path
from typing import Dict, List
from loguru import logger
from crewai import Agent, Task, Crew
from .base_crew import BaseCrew
import os
from dotenv import load_dotenv
from openai import OpenAI

class CodeAnalysisCrew(BaseCrew):
    """AI-powered code analysis crew."""
    
    def __init__(self, target_path: str):
        """Initialize with optional mock for testing"""
        super().__init__("CodeAnalysis", target_path)
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # Create specialized agents with explicit OpenAI config
        self.code_analyzer = Agent(
            role='Code Analyzer',
            goal='Analyze code and suggest improvements',
            backstory="""You are an expert software engineer who specializes in 
            code review and suggesting improvements.""",
            verbose=True,
            llm_config={
                "config_list": [{
                    "model": "gpt-3.5-turbo",
                    "api_key": self.api_key,
                    "base_url": "https://api.openai.com/v1"
                }]
            }
        )
        
        self.breaking_changes_detector = Agent(
            role='Breaking Changes Detector',
            goal='Identify potential breaking changes',
            backstory="""You are an expert in analyzing code changes and identifying
            potential breaking changes or compatibility issues.""",
            verbose=True,
            llm_config={
                "api_key": os.getenv('OPENAI_API_KEY'),
                "model": "gpt-3.5-turbo"
            }
        )

    def _should_analyze_file(self, file_path: Path) -> bool:
        """Determine if file should be analyzed."""
        try:
            # Skip virtual environment files
            if ".venv" in str(file_path):
                return False
            
            # Skip non-Python files
            if not str(file_path).endswith('.py'):
                return False
            
            # Try reading file to check encoding
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            return True
        except UnicodeDecodeError:
            logger.warning(f"Skipping file with encoding issues: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")
            return False

    async def analyze_directory(self, path: str = ".") -> Dict:
        """Analyze directory using CrewAI agents."""
        try:
            analysis_task = Task(
                description=f"""Analyze this codebase:
                Path: {path}
                
                Consider:
                1. Code Quality & Best Practices
                2. Modularization Opportunities
                3. Library Recommendations
                4. Integration Points
                
                Provide specific, actionable recommendations.
                """,
                expected_output="Detailed analysis with recommendations",
                agent=self.code_analyzer
            )

            crew = Crew(
                agents=[self.code_analyzer, self.breaking_changes_detector],
                tasks=[analysis_task],
                verbose=True
            )

            results = crew.kickoff()
            
            return {
                "status": "completed",
                "analysis_results": results,
                "timestamp": pendulum.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": pendulum.now().isoformat()
            }

    async def _analyze_content(self, content: str) -> Dict:
        """Analyze code content with mock support for testing"""
        if self._mock_response and not os.getenv("FORCE_REAL_API"):
            return self._mock_response
            
        try:
            # Use litellm instead of OpenAI client directly
            response = await completion(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "You are a code analysis expert."
                }, {
                    "role": "user", 
                    "content": f"Analyze this code:\n{content}"
                }],
                api_key=self.api_key
            )
            
            return {
                "status": "completed",
                "original_code": content,
                "improved_code": response.choices[0].message.content,
                "timestamp": pendulum.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": pendulum.now().isoformat()
            } 