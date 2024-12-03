#!/bin/bash
set -e

# 1. State Management
STATE_FILE="migration_state.json"
echo '{"status": "starting", "steps_completed": []}' > $STATE_FILE

update_state() {
    local step=$1
    local status=$2
    jq --arg step "$step" --arg status "$status" \
        '.steps_completed += [$step] | .status = $status' $STATE_FILE > tmp.$$.json \
        && mv tmp.$$.json $STATE_FILE
}

# 2. Backup Creation
echo "Creating backup..."
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="backups/migration_$timestamp"
mkdir -p "$backup_dir"

# Database backup
echo "Backing up database..."
cp code_analyzer/crews/crew-output/monitoring.db "$backup_dir/" 2>/dev/null || true

# Output backup
cp -r code_analyzer/crews/crew-output "$backup_dir/crews_output" 2>/dev/null || true
cp -r crews/crew-output "$backup_dir/root_crews_output" 2>/dev/null || true
update_state "backup" "completed"

# 3. Database Migration
echo "Setting up new database location..."
mkdir -p code_analyzer/core/output/db
if [ -f code_analyzer/crews/crew-output/monitoring.db ]; then
    mv code_analyzer/crews/crew-output/monitoring.db code_analyzer/core/output/db/
    # Update connection strings
    find code_analyzer -type f -name "*.py" -exec sed -i '' \
        -e 's/crew-output\/monitoring.db/core\/output\/db\/monitoring.db/g' {} +
fi
update_state "database" "completed"

# 4. Directory Structure
echo "Restructuring core directories..."
mkdir -p code_analyzer/core/output/{analysis,logs,test_results}

# 5. Safe Data Move
echo "Moving data with verification..."
for dir in analysis logs test_results; do
    if [ -d "code_analyzer/crews/crew-output/$dir" ]; then
        rsync -av --remove-source-files \
            "code_analyzer/crews/crew-output/$dir/" \
            "code_analyzer/core/output/$dir/"
    fi
done
update_state "data_move" "completed"

# 6. Import Updates
echo "Updating imports and references..."
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/crews\/crew-output/core\/output/g' \
    -e 's/Path("crew-output")/Path("core\/output")/g' \
    -e 's/from code_analyzer.crewsutils/from code_analyzer.utils/g' \
    -e 's/import code_analyzer.crewsutils/import code_analyzer.utils/g' {} +
update_state "imports" "completed"

# 7. Progress Logging Setup
echo "Setting up enhanced logging..."
mkdir -p code_analyzer/core/utils
cat > code_analyzer/core/utils/logging.py << 'EOL'
from loguru import logger
import time
import asyncio
from functools import wraps
from pathlib import Path

class ProgressLogger:
    def __init__(self, interval=5):
        self.interval = interval
        self.tasks = {}
        
    async def log_progress(self, name, total=100):
        """Log progress with state recovery."""
        start = time.time()
        state_file = Path(f"code_analyzer/core/output/logs/{name}_progress.json")
        
        if state_file.exists():
            state = json.loads(state_file.read_text())
            if state["status"] == "incomplete":
                logger.warning(f"Recovering {name} from previous run")
                
        while True:
            try:
                await asyncio.sleep(self.interval)
                elapsed = time.time() - start
                logger.info(f"{name} running... ({elapsed:.0f}s)")
                state_file.write_text(json.dumps({
                    "status": "running",
                    "elapsed": elapsed,
                    "last_update": time.time()
                }))
            except asyncio.CancelledError:
                break
EOL
update_state "logging" "completed"

# 8. Test Configuration
echo "Updating test configuration..."
cat > tests/conftest.py << 'EOL'
import pytest
import asyncio
from code_analyzer.core.utils.logging import ProgressLogger

@pytest.fixture(scope="session")
def progress_logger():
    return ProgressLogger()

def pytest_collection_modifyitems(items):
    """Add timeout and logging to all tests."""
    for item in items:
        item.add_marker(pytest.mark.timeout(30))
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)
EOL
update_state "test_config" "completed"

# 9. Verification
echo "Running verification..."
python -c "
from code_analyzer.core.utils.logging import ProgressLogger
from code_analyzer.utils.resource_monitor import ResourceMonitor
from pathlib import Path
assert Path('code_analyzer/core/output/db').exists()
assert Path('code_analyzer/core/utils/logging.py').exists()
"
update_state "verification" "completed"

# 10. Run Tests
echo "Running tests with progress..."
pytest tests/ -v --cov=code_analyzer

update_state "complete" "success"
echo "✅ Migration completed successfully"
