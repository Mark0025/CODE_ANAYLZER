"""Verify and fix database tables."""
from pathlib import Path
from code_analyzer.models.base import engine, Base
from code_analyzer.models.log_entry import LogEntry
from code_analyzer.models.crew_output import CrewOutput
from code_analyzer.models.development_timeline import (
    DevelopmentEvent, FileChange, ShellCommand, 
    CrewOperation, TestResult
)
from sqlalchemy import inspect

def verify_database():
    """Verify database tables exist and create if missing."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    required_tables = {
        'log_entries': LogEntry.__table__,
        'crew_outputs': CrewOutput.__table__,
        'development_events': DevelopmentEvent.__table__,
        'file_changes': FileChange.__table__,
        'shell_commands': ShellCommand.__table__,
        'crew_operations': CrewOperation.__table__,
        'test_results': TestResult.__table__
    }
    
    # Create missing tables
    for table_name, table in required_tables.items():
        if table_name not in existing_tables:
            print(f"Creating missing table: {table_name}")
            table.create(engine)
    
    print("\nVerified tables:")
    for table in inspector.get_table_names():
        print(f"✓ {table}")

if __name__ == "__main__":
    verify_database() 