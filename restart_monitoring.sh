#!/bin/bash
set -e

echo "🔄 Complete monitoring system restart..."

# 1. Install/update dependencies
echo "📦 Updating dependencies..."
pip install fastapi uvicorn jinja2 websockets python-multipart

# 2. Clean old files
echo "🧹 Cleaning old files..."
rm -f code_analyzer/monitoring/dashboard.py
rm -f code_analyzer/monitoring/__pycache__/dashboard.cpython-*.pyc

# 3. Apply clean migration
echo "🏗️ Applying clean migration..."
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/fixes/migrate_to_fastapi.yaml \
    --verbose

# 4. Verify file content
echo "🔍 Verifying migration..."
if grep -q "flask" code_analyzer/monitoring/dashboard.py; then
    echo "❌ Migration failed - Flask still present"
    exit 1
fi

# 5. Start monitoring
echo "🚀 Starting monitoring dashboard..."
uvicorn code_analyzer.monitoring.dashboard:app --reload --port 8000

echo "✨ Restart complete! Dashboard available at http://localhost:8000"
