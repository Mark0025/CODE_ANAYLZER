#!/bin/bash
set -e

# Setup logging
exec 1> >(tee "fix_$(date +%Y%m%d_%H%M%S).log")
exec 2>&1

echo "🔄 Starting CODE_ANALYZER fix..."

# 1. Create backup
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="backups/backup_${timestamp}"
mkdir -p "$backup_dir"
echo "📦 Creating backup in $backup_dir"
cp -r code_analyzer "$backup_dir/"

# 2. Fix imports
echo "🔧 Fixing imports..."
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/from code_analyzer.crewsdoc_crews/from code_analyzer.crews.doc_crews/g' \
    -e 's/from ..doc_crews/from code_analyzer.crews.doc_crews/g' \
    -e 's/from ..base_crew/from code_analyzer.crews.base_crew/g' {} +

# 3. Add missing methods
echo "📝 Adding missing methods..."
cat >> code_analyzer/crews/analysis_crews/pattern_detector.py << 'EOF'

async def _detect_code_smells(self, tree: ast.AST) -> List[PatternMatch]:
    """Detect code smells in AST."""
    return []  # Placeholder implementation

def _is_singleton(self, tree: ast.AST) -> bool:
    """Check if class is singleton."""
    return False  # Placeholder implementation

def _get_class_name(self, tree: ast.AST) -> str:
    """Get class name from node."""
    return getattr(tree, 'name', 'Unknown')

def _is_factory(self, tree: ast.AST) -> bool:
    """Check if class is factory."""
    return False  # Placeholder implementation
EOF

# 4. Run verification
echo "🧪 Running tests..."
pytest tests/test_combined_analysis.py -v --log-cli-level=INFO

echo "✅ Fix completed"
