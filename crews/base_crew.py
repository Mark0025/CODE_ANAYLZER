from pathlib import Path
from datetime import datetime
from loguru import logger
from typing import Optional
import sys


class BaseCrew:
    """Base class for all crews with consistent logging"""
    
    def __init__(self, crew_name: str, target_path: Optional[str] = None):
        # Setup paths
        self.output_dir = Path("crews/crew-output")
        self.logs_dir = self.output_dir / "logs"
        
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging(crew_name, target_path)
    
    def setup_logging(self, crew_name: str, target_path: Optional[str] = None) -> None:
        """Configure loguru logger with consistent format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_info = f"_{target_path}" if target_path else ""
        
        # Remove default logger
        logger.remove()
        
        # Add file logger
        logger.add(
            self.logs_dir / f"{crew_name}{target_info}_{timestamp}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module}:{function}:{line} | {message}",
            level="INFO",
            rotation="500 MB"
        )
        
        # Add console logger with colors
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
            level="INFO",
            colorize=True
        )
        
        logger.info(f"Starting {crew_name} crew analysis" + (f" for {target_path}" if target_path else ""))
    
    def save_output(self, content: str, filename: str) -> Path:
        """Save output with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"{filename}_{timestamp}.json"
        output_file.write_text(content)
        logger.info(f"Saved output to {output_file}")
        return output_file
    
    def log_analysis_summary(self, success_count: int, fail_count: int) -> None:
        """Log analysis summary with consistent format"""
        logger.info("Analysis Summary:")
        logger.info(f"✅ Successful analyses: {success_count}")
        logger.info(f"❌ Failed analyses: {fail_count}")
        logger.info(f"📊 Success rate: {(success_count/(success_count+fail_count))*100:.2f}%")