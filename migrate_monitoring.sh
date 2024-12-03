#!/bin/bash
set -e

echo "🔄 Migrating monitoring to FastAPI..."

# 1. Apply migration YAML
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/fixes/migrate_to_fastapi.yaml \
    --verbose

# 2. Start monitoring
echo "🚀 Starting monitoring dashboard..."
uvicorn code_analyzer.monitoring.dashboard:app --reload --port 8000

echo "✨ Migration complete! Dashboard available at http://localhost:8000"
