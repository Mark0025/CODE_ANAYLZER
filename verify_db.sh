#!/bin/bash
set -e

echo "🧪 Testing CODE_ANALYZER Database..."

# 1. Check database setup
echo "💾 Verifying database setup..."
python3 -c '
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger

db = DatabaseManager()

# Test connection
if db.test_connection():
    logger.info("✅ Database connection successful")
else:
    logger.error("❌ Database connection failed")
    exit(1)

# Check tables
tables = db.get_tables()
logger.info(f"Found tables: {tables}")

# Check indexes
indexes = db.get_indexes()
logger.info(f"Found indexes: {indexes}")

# Verify required tables
setup = db.verify_setup()
for table, exists in setup.items():
    status = "✅" if exists else "❌"
    logger.info(f"{status} {table}")

# Try basic operation
try:
    output = db.save_crew_output(
        crew_name="test_crew",
        output_type="test",
        status="completed",
        results={"test": True}
    )
    logger.info("✅ Database operations working")
except Exception as e:
    logger.error(f"❌ Database operations failed: {e}")
    exit(1)
'

echo "✨ Verification complete!"
