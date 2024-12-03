#!/bin/bash
set -e

echo "🏗️ Setting up CODE_ANALYZER Database Integration..."

# 1. Backup existing data
echo "📦 Backing up existing data..."
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="backups/data_migration_$timestamp"
mkdir -p "$backup_dir"

# Backup any existing files
if [ -d "code_analyzer/crews/crew-output" ]; then
    cp -r code_analyzer/crews/crew-output/* "$backup_dir/"
fi
if [ -d "code_analyzer/core/output" ]; then
    cp -r code_analyzer/core/output/* "$backup_dir/"
fi

# 2. Clean old structure
echo "🧹 Cleaning old structure..."
rm -rf code_analyzer/crews/crew-output
rm -rf code_analyzer/core/output/db/*.db

# 3. Initialize database with proper models
echo "💾 Initializing database..."
python3 -c '
from code_analyzer.models.base import init_db
from code_analyzer.models.crew_output import CrewOutput, ErrorHandlingResult, CodeAnalysisResult, LogEntry
from code_analyzer.models.db_manager import DatabaseManager

# Initialize database
init_db()

# Create database manager
db = DatabaseManager()

print("Database initialized with models:")
print("- CrewOutput")
print("- ErrorHandlingResult")
print("- CodeAnalysisResult")
print("- LogEntry")
'

# 4. Create indexes for performance
echo "📊 Creating indexes..."
python3 -c '
from sqlalchemy import create_engine, text
from code_analyzer.models.base import get_engine

engine = get_engine()
with engine.connect() as conn:
    # Create indexes
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_crew_outputs_timestamp 
        ON crew_outputs(timestamp);
        
        CREATE INDEX IF NOT EXISTS idx_analysis_priority 
        ON code_analysis_results(priority);
        
        CREATE INDEX IF NOT EXISTS idx_log_entries_level 
        ON log_entries(level);
    """))
    conn.commit()
'

# 5. Verify setup
echo "✅ Verifying setup..."
python3 -c '
from code_analyzer.models.db_manager import DatabaseManager
db = DatabaseManager()
print("Database connection verified!")
'

echo "🎉 Database integration complete!"
