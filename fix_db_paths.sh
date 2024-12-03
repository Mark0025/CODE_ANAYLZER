#!/bin/bash
set -e

echo "🔄 Fixing Database Paths..."

# 1. Update core/db to use models
echo "📝 Updating core DB imports..."
cat > code_analyzer/core/db/__init__.py << 'EOF'
"""Database initialization using existing models."""
from code_analyzer.models.base import init_db, get_session, get_engine, Base
from code_analyzer.models.crew_output import (
    CrewOutput, 
    ErrorHandlingResult, 
    CodeAnalysisResult,
    LogEntry
)

# Re-export everything from models
__all__ = [
    'init_db',
    'get_session',
    'get_engine',
    'Base',
    'CrewOutput',
    'ErrorHandlingResult',
    'CodeAnalysisResult',
    'LogEntry'
]
EOF

# 2. Create output directory structure
echo "📁 Creating output structure..."
mkdir -p code_analyzer/core/output/{analysis,logs,db}

# 3. Update database path in models/base.py
echo "🔧 Updating database path..."
sed -i '' 's|DB_DIR = Path("core/output")|DB_DIR = Path("code_analyzer/core/output/db")|g' code_analyzer/models/base.py

# 4. Clean up duplicate locations
echo "🧹 Cleaning up duplicates..."
rm -rf code_analyzer/crews/crew-output
rm -rf code_analyzer/core/output/db/*.db

# 5. Initialize database in correct location
echo "💾 Initializing database..."
python3 -c '
from code_analyzer.models.base import init_db
init_db()
print("Database initialized in correct location")
'

echo "✅ Database paths fixed!"
