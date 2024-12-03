#!/bin/bash
set -e

echo "�� Running Focused Tests..."

# Set asyncio scope
export PYTEST_ASYNCIO_LOOP_SCOPE=function

# Run specific tests first
echo "📦 Running Core Tests..."
python -m pytest tests/test_analyzer.py tests/test_db_integration.py -v

# Then run combined tests with timeout
echo "🔄 Running Combined Tests..."
python -m pytest tests/test_combined_analysis.py -v --timeout=30

echo "✨ Test suite complete!"
