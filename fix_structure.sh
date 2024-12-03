#!/bin/bash
set -e

echo "🔄 Consolidating output structure..."

# 1. Create unified directory structure
mkdir -p code_analyzer/core/output/{analysis,logs,db,test_results}

# 2. Move existing data
rsync -av --remove-source-files \
    code_analyzer/crews/crew-output/ \
    code_analyzer/core/output/

# 3. Update database location
if [ -f code_analyzer/crews/crew-output/monitoring.db ]; then
    mv code_analyzer/crews/crew-output/monitoring.db \
       code_analyzer/core/output/db/
fi

# 4. Fix imports
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/from code_analyzer.crewsutils/from code_analyzer.utils/g' \
    -e 's/import code_analyzer.crewsutils/import code_analyzer.utils/g' {} +

# 5. Initialize database
python -c "
from code_analyzer.core.db import init_db
init_db()
"

echo "✅ Structure consolidated"
