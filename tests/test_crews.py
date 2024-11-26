"""Tests for crew functionality."""
import pytest
from pathlib import Path
from loguru import logger
from crews.code_analysis_crew import CodeAnalysisCrew
from openai import OpenAI

@pytest.mark.asyncio
async def test_crew_initialization(load_env):
    """Test crew initialization."""
    api_key = load_env
    crew = CodeAnalysisCrew("test_path")
    assert crew is not None
    assert crew.name == "CodeAnalysis"

@pytest.mark.asyncio
async def test_analysis_output_format(load_env, test_project_path):
    """Test the format of analysis output."""
    api_key = load_env
    crew = CodeAnalysisCrew(str(test_project_path))
    results = await crew.analyze_directory(str(test_project_path))
    
    assert isinstance(results, dict)
    assert "status" in results
    assert results["status"] == "completed"
    