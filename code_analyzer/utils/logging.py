"""Logging configuration."""
from loguru import logger as loguru_logger
from code_analyzer.models.db_manager import DatabaseManager
import sys
from pathlib import Path

class DatabaseLogHandler:
    """Handler for storing logs in database."""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def __call__(self, message):
        """Handle log message."""
        record = message.record
        
        # Extract crew name from extras or context
        crew_name = record["extra"].get("crew_name", "system")
        
        # Save to database
        self.db.save_log_entry(
            level=record["level"].name,
            message=record["message"],
            metadata={
                "function": record["function"],
                "file": record["file"].name,
                "line": record["line"],
                "time": record["time"].isoformat(),
                "thread": record["thread"].name,
                "process": record["process"].id
            },
            crew_name=crew_name
        )

def setup_logging():
    """Setup logging configuration."""
    # Create log directory
    log_dir = Path("code_analyzer/core/output/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure with empty handlers first
    loguru_logger.configure(handlers=[])
    
    # Add handlers
    loguru_logger.add(sys.stderr, level="INFO")
    loguru_logger.add(
        log_dir / "code_analyzer_{time}.log",
        rotation="500 MB",
        retention="10 days",
        level="DEBUG"
    )
    loguru_logger.add(
        DatabaseLogHandler(),
        level="INFO"
    )
    
    return loguru_logger 