#!/bin/bash
set -e

echo "🧪 Testing CODE_ANALYZER Components..."

# 1. Check database
echo "💾 Checking database..."
python3 -c '
from code_analyzer.models.db_manager import DatabaseManager
db = DatabaseManager()

# Check tables
tables = db.get_tables()
print(f"Found tables: {tables}")

# Try basic operations
output = db.save_crew_output(
    crew_name="test_crew",
    output_type="test",
    status="completed",
    results={"test": True}
)
print("Database operations: ✅")
'

echo "✨ Verification complete!"
