#!/bin/bash
set -e

echo "🔧 Smart Database Fix..."

# 1. Preserve existing data
if [ -d "code_analyzer/crews/crew-output" ]; then
    echo "📦 Backing up existing data..."
    mkdir -p backups/crew_output_$(date +%Y%m%d)
    cp -r code_analyzer/crews/crew-output/* backups/crew_output_$(date +%Y%m%d)/
fi

# 2. Initialize database without disrupting files
python3 -c "
from code_analyzer.core.db import init_db
from sqlalchemy import inspect

# Create DB with proper schema
init_db()

# Verify tables
engine = inspect(init_db()).get_engine()
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f'Created tables: {tables}')
" 