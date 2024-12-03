"""Factory for creating properly configured CrewAI agents."""
from crewai import Agent
from typing import Optional, List, Dict, Any
from loguru import logger
from .base_crew import BaseCrew

class AgentFactory(BaseCrew):
    """Factory for creating standardized CrewAI agents."""
    
    def __init__(self, target_path: str):
        super().__init__("AgentFactory", target_path)
        self._agents = {}
        
    async def create_agent(
        self,
        role: str,
        goal: str,
        backstory: Optional[str] = None,
        tools: Optional[List] = None,
        allow_delegation: bool = False
    ) -> Agent:
        """Create a properly configured agent with resource management."""
        async with self.managed_operation():
            try:
                agent_key = f"{role}:{goal}"
                
                if agent_key not in self._agents:
                    self._agents[agent_key] = Agent(
                        role=role,
                        goal=goal,
                        backstory=backstory or f"Expert at {goal.lower()}",
                        tools=tools or [],
                        allow_delegation=allow_delegation,
                        verbose=True
                    )
                
                return self._agents[agent_key]
                
            except Exception as e:
                self.logger.error(f"Agent creation failed: {e}")
                raise
                
    async def create_analyzer(self, name: str) -> Agent:
        """Create code analysis agent."""
        return await self.create_agent(
            role=f"{name} Analyzer",
            goal="Analyze code quality and structure",
            backstory="Expert at code analysis and best practices"
        )
        
    async def create_status_agent(self) -> Agent:
        """Create status tracking agent."""
        return await self.create_agent(
            role="Status Tracker",
            goal="Track and analyze project status",
            backstory="Expert at monitoring project metrics and status"
        )
        
    @classmethod
    def create_pr_agent(cls) -> Agent:
        """Create PR generation agent."""
        return cls.create_agent(
            role="PR Generator",
            goal="Generate high-quality pull requests",
            backstory="Expert at creating clear, actionable pull requests"
        ) 