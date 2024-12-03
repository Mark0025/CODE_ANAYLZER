#!/bin/bash

# 1. Backup current broken state
mkdir -p backups/broken_$(date +%Y%m%d)
cp -r code_analyzer backups/broken_$(date +%Y%m%d)/

# 2. Restore from working commit
git checkout 5ac85c5 -- code_analyzer/

# 3. Clean up broken files
rm -rf code_analyzer/core/
rm -f yaml_tools/fixes/dev_now_*

# 4. Initialize database
python -m code_analyzer.scripts.init_db --force

# 5. Start server
uvicorn code_analyzer.monitoring.dashboard:app --reload
EOF 