#!/bin/bash
set -e

echo "🔧 Fixing immediate issues..."

# 1. Fix dependencies
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/fixes/fix_dependencies.yaml \
    --verbose

# 2. Fix imports
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/fixes/fix_model_imports.yaml \
    --verbose

# 3. Copy templates
mkdir -p yaml_tools/master/
cp DEV-NOW/current-state/YAML-TEMPLATES/*.yaml yaml_tools/master/

echo "✨ Immediate fixes complete!"
