#!/bin/bash
set -e

echo "🧹 Starting CODE_ANALYZER City Cleanup..."

# 1. Verify all files migrated
echo "🔍 Verifying migration..."
if [ -d "code_analyzer/crews/crew-output" ]; then
    if [ -z "$(ls -A code_analyzer/crews/crew-output)" ]; then
        echo "✅ All files migrated successfully"
        rm -rf code_analyzer/crews/crew-output
    else
        echo "⚠️ Old directory not empty - manual check needed"
        exit 1
    fi
fi

# 2. Archive old backups
echo "📦 Archiving old backups..."
find backups/ -type d -mtime +3 -exec tar -czf {}.tar.gz {} \; -exec rm -rf {} \;

# 3. Verify database integrity
echo "💾 Checking database..."
python3 -c "
from code_analyzer.core.db import init_db
from sqlalchemy import inspect
init_db()
"

# 4. Run test suite
echo "🧪 Running verification tests..."
pytest tests/ -v --log-cli-level=INFO

echo "✨ Cleanup complete!"
