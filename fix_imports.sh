#!/bin/bash
set -e

echo "1. Updating imports to use existing utils..."
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/from code_analyzer.crewsutils/from code_analyzer.utils/g' \
    -e 's/import code_analyzer.crewsutils/import code_analyzer.utils/g' {} +

echo "2. Verifying imports..."
python -c "from code_analyzer.utils.resource_monitor import ResourceMonitor" || exit 1

echo "3. Running tests..."
pytest tests/ -v --cov=code_analyzer

echo "✅ All steps completed"
