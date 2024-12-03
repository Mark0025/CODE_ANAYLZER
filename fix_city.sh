#!/bin/bash
set -e

echo "🏗️ Rebuilding CODE_ANALYZER City..."

# 1. Fix Database District
python3 -c "
from pathlib import Path
import sqlite3
import shutil

# Backup database
db_path = Path('code_analyzer/core/output/analyzer.db')
if db_path.exists():
    shutil.copy(db_path, f'backups/analyzer_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')

# Initialize new database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS crew_outputs (
    id INTEGER PRIMARY KEY,
    crew_name TEXT,
    output_type TEXT,
    data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()
"

# 2. Fix Import District
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/from code_analyzer.crewsdoc_crews/from code_analyzer.crews.doc_crews/g' \
    -e 's/from ..doc_crews/from code_analyzer.crews.doc_crews/g' {} +

# 3. Fix Test District
cat > tests/test_combined_analysis.py << 'EOL'
"""Test combined analysis functionality"""
import pytest
from loguru import logger
import asyncio
from code_analyzer.crews.code_analysis_crew import CodeAnalysisCrew
from code_analyzer.crews.crewai_docs_crew import CrewAIDocsCrew

@pytest.mark.timeout(30)
@pytest.mark.asyncio
async def test_combined_analysis():
    """Test running combined analysis."""
    logger.info("Starting combined analysis test")
    
    async def log_progress():
        while True:
            logger.info("Test in progress...")
            await asyncio.sleep(5)
    
    progress_task = asyncio.create_task(log_progress())
    try:
        code_crew = CodeAnalysisCrew("./")
        docs_crew = CrewAIDocsCrew("./")
        
        code_results = await code_crew.analyze_directory()
        docs_results = await docs_crew.analyze_docs()
        
        assert code_results["status"] == "completed"
        assert docs_results["status"] == "completed"
    finally:
        progress_task.cancel()
EOL

echo "🏗️ Running verification..."
pytest tests/test_combined_analysis.py -v --log-cli-level=INFO
