#!/bin/bash
set -e

# Setup logging with loguru
python -c "
from loguru import logger
logger.add('implementation_{time}.log', rotation='1 day')
logger.info('Starting master implementation')
"

echo "🚀 Starting CODE_ANALYZER Master Implementation..."

# Phase 1: Setup Foundation
echo "📦 Phase 1: Setting up foundation..."
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/master/01_setup_foundation.yaml \
    --verbose

# Phase 2: Enhance Monitoring
echo "📊 Phase 2: Enhancing monitoring..."
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/master/02_enhance_monitoring.yaml \
    --verbose

# Phase 3: Fabric Integration
echo "🔌 Phase 3: Integrating Fabric AI..."
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/master/03_fabric_integration.yaml \
    --verbose

# Phase 4: Testing
echo "🧪 Phase 4: Running tests..."
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/master/04_run_tests.yaml \
    --verbose

# Phase 5: Verification
echo "✅ Phase 5: Verifying implementation..."
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/master/05_verify_all.yaml \
    --verbose

echo "✨ Master implementation complete!"
