import os
import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import loguru
from loguru import logger

# Configure logging
def pytest_configure(config):
    """Set up logging for tests"""
    log_path = project_root / "tests" / "logs"
    log_path.mkdir(parents=True, exist_ok=True)
    
    logger.remove()  # Remove default handler
    
    # Add file handler
    logger.add(
        log_path / "test_run_{time}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="1 MB"
    )
    
    # Add console handler
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO",
        colorize=True
    ) 

@pytest.fixture
def mock_ai_response():
    """Mock AI response for testing"""
    return {
        "code_analysis": {
            "raw": "### Code Analysis Results\n- Identified patterns\n- Suggested improvements",
            "json_dict": {
                "patterns": ["pattern1", "pattern2"],
                "improvements": ["improvement1", "improvement2"]
            }
        },
        "ecosystem_analysis": {
            "raw": "### Ecosystem Analysis\n- Current trends\n- Best practices",
            "json_dict": {
                "trends": ["trend1", "trend2"],
                "practices": ["practice1", "practice2"]
            }
        }
    }

@pytest.fixture
def mock_crew_response(mock_ai_response):
    """Mock CrewAI response"""
    async_mock = AsyncMock()
    async_mock.return_value = mock_ai_response
    return async_mock 