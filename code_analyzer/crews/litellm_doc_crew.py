from code_analyzer.crews.base_crew import BaseCrew
from pathlib import Path
from typing import Dict, Any
from loguru import logger
from crewai import Agent, Task, Crew
# import litellm  # Commented out for now
from dotenv import load_dotenv
import os
from openai import OpenAI  # Direct OpenAI import

class LiteLLMDocCrew(BaseCrew):
    """Crew for analyzing LiteLLM documentation and implementation."""
    
    def __init__(self, target_path: str):
        super().__init__("LiteLLMDoc", target_path)
        
        # Load environment variables first
        load_dotenv()
        
        # Initialize OpenAI client directly
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Create specialized agents with direct OpenAI config
        self.doc_analyzer = Agent(
            role='LiteLLM Documentation Expert',
            goal='Understand LiteLLM implementation details',
            backstory="""You are an expert at analyzing documentation and 
            understanding library implementations.""",
            verbose=True,
            llm_config={
                "api_key": os.getenv('OPENAI_API_KEY'),
                "model": "gpt-3.5-turbo"
            }
        )
        
        self.implementation_advisor = Agent(
            role='Implementation Advisor',
            goal='Provide implementation guidance',
            backstory="""You are an expert at implementing AI libraries
            and providing practical implementation advice.""",
            verbose=True,
            llm_config={
                "api_key": os.getenv('OPENAI_API_KEY'),
                "model": "gpt-3.5-turbo"
            }
        )

    async def analyze_litellm(self) -> Dict[str, Any]:
        """Analyze LiteLLM documentation and provide implementation guidance."""
        try:
            # First, analyze the documentation
            doc_task = Task(
                description="""Analyze LiteLLM documentation focusing on:
                1. API key handling
                2. Rate limiting
                3. Model fallbacks
                4. Best practices
                
                Provide detailed implementation recommendations.
                """,
                expected_output="Detailed LiteLLM implementation guide",
                agent=self.doc_analyzer
            )

            # Then, get implementation recommendations
            impl_task = Task(
                description="""Based on the documentation analysis, provide:
                1. Correct API key setup
                2. Rate limit handling
                3. Error management
                4. Implementation patterns
                
                Focus on production-ready implementation.
                """,
                expected_output="Implementation recommendations",
                agent=self.implementation_advisor
            )

            crew = Crew(
                agents=[self.doc_analyzer, self.implementation_advisor],
                tasks=[doc_task, impl_task],
                verbose=True
            )

            results = crew.kickoff()
            
            return {
                "documentation_analysis": results[0],
                "implementation_guide": results[1],
                "recommendations": {
                    "api_key_handling": "Use environment variables with load_dotenv()",
                    "rate_limiting": "Implement proper rate limit handling",
                    "error_handling": "Use try/except with specific error types"
                }
            }
            
        except Exception as e:
            logger.error(f"LiteLLM analysis failed: {e}")
            return {
                "error": str(e),
                "status": "failed"
            } 