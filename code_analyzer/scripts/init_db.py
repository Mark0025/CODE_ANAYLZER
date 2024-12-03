"""Database initialization script."""
import os
from pathlib import Path
from code_analyzer.models.base import init_db, engine
from code_analyzer.models import Base
from code_analyzer.models.crew_output import CrewOutput
from code_analyzer.models.log_entry import LogEntry
from sqlalchemy import inspect

def setup_database():
    """Set up the database and create all tables."""
    try:
        # Create database directory if it doesn't exist
        db_dir = Path("code_analyzer/core/output/db")
        db_dir.mkdir(parents=True, exist_ok=True)
        
        # Drop existing tables
        print("Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {', '.join(tables)}")
        
        # Verify columns in log_entries
        columns = [col['name'] for col in inspector.get_columns('log_entries')]
        print(f"\nLog entries columns: {', '.join(columns)}")
        
        print("Database initialization complete!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    setup_database() 