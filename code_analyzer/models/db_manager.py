"""Database manager module."""
from sqlalchemy import inspect, text
from typing import Dict, Any, List
from loguru import logger
from datetime import datetime

# Change relative imports to absolute
from code_analyzer.models.base import get_session
from code_analyzer.models.crew_output import CrewOutput, ErrorHandlingResult, CodeAnalysisResult
from code_analyzer.models.log_entry import LogEntry

class DatabaseManager:
    """Manager for database operations."""
    
    def __init__(self):
        self.session = get_session()
        
    def save_crew_output(self, crew_name: str, output: Dict[str, Any]) -> CrewOutput:
        """Save crew output to database."""
        crew_output = CrewOutput(
            crew_name=crew_name,
            output=output,
            timestamp=datetime.utcnow()
        )
        self.session.add(crew_output)
        self.session.commit()
        return crew_output
        
    def save_error_handling(self, crew_output_id: int, file_path: str,
                          changes: Dict[str, Any], status: str) -> ErrorHandlingResult:
        """Save error handling result."""
        try:
            result = ErrorHandlingResult(
                crew_output_id=crew_output_id,
                file_path=file_path,
                changes_made=changes,
                status=status
            )
            self.session.add(result)
            self.session.commit()
            return result
            
        except Exception as e:
            logger.error(f"Error saving error handling result: {e}")
            self.session.rollback()
            raise
            
    def get_crew_outputs(self, crew_name: str = None, 
                        status: str = None) -> List[CrewOutput]:
        """Get crew outputs with optional filtering."""
        query = self.session.query(CrewOutput)
        
        if crew_name:
            query = query.filter(CrewOutput.crew_name == crew_name)
        if status:
            query = query.filter(CrewOutput.status == status)
            
        return query.all() 
    def get_tables(self) -> List[str]:
        """Get all tables in database."""
        try:
            inspector = inspect(self.session.get_bind())
            return inspector.get_table_names()
        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []

    def get_indexes(self) -> Dict[str, List[str]]:
        """Get all indexes in database."""
        try:
            inspector = inspect(self.session.get_bind())
            indexes = {}
            for table in self.get_tables():
                indexes[table] = [idx['name'] for idx in inspector.get_indexes(table)]
            return indexes
        except Exception as e:
            logger.error(f"Failed to get indexes: {e}")
            return {}

    def verify_setup(self) -> Dict[str, bool]:
        """Verify database setup."""
        try:
            tables = self.get_tables()
            required_tables = {
                'crew_outputs': False,
                'error_handling_results': False,
                'code_analysis_results': False,
                'log_entries': False
            }
            
            for table in tables:
                if table in required_tables:
                    required_tables[table] = True
                    
            return required_tables
        except Exception as e:
            logger.error(f"Failed to verify setup: {e}")
            return {}

    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            self.session.execute(text('SELECT 1'))
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

    def save_log_entry(self, level: str, message: str, metadata: dict = None, crew_name: str = None) -> LogEntry:
        """Save a log entry to the database."""
        log = LogEntry(
            level=level,
            message=message,
            extra_data=metadata,
            crew_name=crew_name
        )
        self.session.add(log)
        self.session.commit()
        return log

    def get_recent_logs(self, limit: int = 100) -> List[LogEntry]:
        """Get recent log entries."""
        return self.session.query(LogEntry).order_by(
            LogEntry.timestamp.desc()
        ).limit(limit).all()

