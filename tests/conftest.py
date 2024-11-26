import pytest
from pathlib import Path
import os
from dotenv import load_dotenv
from loguru import logger

# Load .env once at module level
load_dotenv()

@pytest.fixture(autouse=True)
def load_env():
    """Get API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not found in environment")
    return api_key

