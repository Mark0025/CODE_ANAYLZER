from pathlib import Path
from typing import Dict
from loguru import logger
import os
from dotenv import load_dotenv

class BaseCrew:
    """Base class for all crews"""
    
    def __init__(self, name: str, target_path: str):
        """Initialize base crew.
        
        Args:
            name: Name of the crew
            target_path: Target path for analysis
        """
        self.name = name
        self.target_path = target_path
        
        # Load environment variables first
        load_dotenv()
        
        # Get and verify API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
            
        logger.info(f"Initializing {name} crew for {target_path}")