#!/bin/bash
set -e

echo "🏗️ Setting up YAML Tools..."

# 1. Create YAML directory structure
echo "📁 Creating YAML directories..."
mkdir -p yaml_tools/{fixes,setup,templates}

# 2. Create structure fix YAML
echo "📝 Creating fix YAML..."
cat > yaml_tools/fixes/structure_fix.yaml << 'EOF'
update_plan:
  name: "Fix All Structure Issues"
  description: "Fix imports, structure, and run updates"
  priority: "HIGH"
  
  phases:
    1_fix_imports:
      description: "Fix import statements"
      changes:
        - type: "modify_imports"
          target: "code_analyzer/crews/analysis_crews/pattern_detector.py"
          imports:
            - "from typing import Dict, Any, List"
            - "from code_analyzer.utils.ast_helpers import parse_code_safely"
            
    2_fix_structure:
      description: "Ensure proper structure"
      changes:
        - type: "create_directory"
          target: "code_analyzer/core/output/reports"
          recursive: true
          
    3_fix_run_updates:
      description: "Fix run_updates.py"
      changes:
        - type: "modify_file"
          target: "code_analyzer/crews/dev_crews/run_updates.py"
          updates:
            - type: "replace"
              old: "run_updates(prog_name=\"run_updates\")"
              new: "run_updates(prog_name=\"run_updates\", spec=\"yaml_tools/fixes/structure_fix.yaml\", verbose=True, target=\"./\")"
EOF

echo "✨ YAML tools ready!"
