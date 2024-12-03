"""SQLAlchemy log handler for database logging."""
from loguru import logger
from code_analyzer.crewsmodels.crew_output import LogEntry
from code_analyzer.crewsmodels.base import get_session
import pendulum

class SQLAlchemyLogHandler:
    """Handler for storing logs in database."""
    
    def __init__(self):
        self.session = get_session()
        
    def write(self, message):
        """Write log message to database."""
        try:
            record = message.record
            
            # Create log entry
            entry = LogEntry(
                timestamp=pendulum.now(),
                level=record["level"].name,
                message=record["message"],
                crew_name=record["extra"].get("crew_name"),
                log_metadata={
                    "function": record["function"],
                    "file": record["file"].name,
                    "line": record["line"]
                }
            )
            
            # Save to database
            self.session.add(entry)
            self.session.commit()
            
        except Exception as e:
            # Don't use logger here to avoid recursion
            print(f"Failed to save log: {e}") 