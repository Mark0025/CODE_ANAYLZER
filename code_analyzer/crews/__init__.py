"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
from .base_crew import BaseCrew
from .code_analysis_crew import CodeAnalysisCrew
from .error_handler_crew import ErrorHandlerCrew
from .status_crew import StatusCrew
from .clean_dir_crew import CleanDirCrew
from .analyze_crews_crew import AnalyzeCrewsCrew
from .crewai_docs_crew import CrewAIDocsCrew
from .agent_factory import AgentFactory
from .cli import CLICrew

__all__ = [
    'BaseCrew',
    'CodeAnalysisCrew',
    'ErrorHandlerCrew',
    'StatusCrew',
    'CleanDirCrew',
    'AnalyzeCrewsCrew',
    'CrewAIDocsCrew',
    'AgentFactory',
    'CLICrew'
]

# Version info
__version__ = '0.1.0'
