"""Tests for real codebase analysis."""
import pytest
from pathlib import Path
from loguru import logger
from crews.code_analysis_crew import CodeAnalysisCrew
import os
from dotenv import load_dotenv

# Load .env once at module level
load_dotenv()

@pytest.mark.asyncio
async def test_analyze_real_codebase():
    """Test analyzing our actual codebase."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not found in environment")
    
    try:
        crew = CodeAnalysisCrew(str(Path(__file__).parent.parent))
        results = await crew.analyze_directory(str(Path(__file__).parent.parent))
        assert results["status"] == "completed"
        return results
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise
    
