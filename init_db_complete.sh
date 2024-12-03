#!/bin/bash
set -e

echo "🏗️ Setting up Complete Database..."

# 1. Initialize database with schema
echo "💾 Creating database schema..."
python3 -c '
from code_analyzer.models.base import init_db, get_engine
from code_analyzer.models.crew_output import CrewOutput, ErrorHandlingResult, CodeAnalysisResult, LogEntry
from sqlalchemy import inspect
from loguru import logger

# Initialize database
init_db()

# Verify tables
engine = get_engine()
inspector = inspect(engine)
tables = inspector.get_table_names()

logger.info(f"Created tables: {tables}")

# Verify each required table
required_tables = [
    "crew_outputs",
    "error_handling_results",
    "code_analysis_results",
    "log_entries"
]

for table in required_tables:
    if table in tables:
        logger.success(f"✅ Table {table} created")
    else:
        logger.error(f"❌ Table {table} missing")
'

# 2. Test database operations
echo "🧪 Testing database operations..."
python3 -c '
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger

db = DatabaseManager()

# Test save operation
try:
    output = db.save_crew_output(
        crew_name="test_crew",
        output_type="test",
        status="completed",
        results={"test": True}
    )
    logger.success("✅ Database operations working")
except Exception as e:
    logger.error(f"❌ Database operations failed: {e}")
    raise
'

echo "✨ Database setup complete!"
