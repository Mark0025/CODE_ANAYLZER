"""Tests for LiteLLM documentation analysis."""
import pytest
from pathlib import Path
from loguru import logger
from crews.litellm_doc_crew import LiteLLMDocCrew
from dotenv import load_dotenv
import os
from openai import OpenAI
from rich.console import Console

@pytest.mark.asyncio
async def test_litellm_analysis(load_env):
    """Test LiteLLM documentation analysis."""
    api_key = load_env  # Get key from fixture
    
    try:
        # Initialize crew
        crew = LiteLLMDocCrew(".")
        results = await crew.analyze_litellm()
        
        assert results is not None
        return results
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise