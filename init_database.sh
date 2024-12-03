#!/bin/bash
set -e

echo "🏗️ Setting up CODE_ANALYZER Database District..."

# 1. Create database directory
echo "📁 Creating database directory..."
mkdir -p code_analyzer/core/output/db

# 2. Initialize database with schema
echo "💾 Creating database schema..."
python3 -c '
from code_analyzer.core.db import init_db
from sqlalchemy import create_engine, inspect
from pathlib import Path

# Ensure directory exists
db_path = Path("code_analyzer/core/output/db")
db_path.mkdir(parents=True, exist_ok=True)

# Initialize database
init_db()

# Verify tables
engine = create_engine(f"sqlite:///{db_path}/analyzer.db")
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Created tables: {tables}")
'

# 3. Verify database exists
echo "🔍 Verifying database..."
if [ -f "code_analyzer/core/output/db/analyzer.db" ]; then
    echo "✅ Database created successfully"
    sqlite3 code_analyzer/core/output/db/analyzer.db ".tables"
else
    echo "❌ Database creation failed"
    exit 1
fi

echo "✨ Database District setup complete!"
