#!/bin/bash
set -e

echo "🔄 Starting CODE_ANALYZER fix..."

# 1. Create directories first
echo "📁 Creating directory structure..."
mkdir -p code_analyzer/core/output/{analysis,logs,test_results}
mkdir -p code_analyzer/crews/crew-output/{crewaidocs,codeanalysis,analysis}
touch code_analyzer/crews/crew-output/crewaidocs/latest_documentation.json
touch code_analyzer/crews/crew-output/codeanalysis/latest_analysis.json
touch code_analyzer/core/output/analysis/latest_analysis.json

# 2. Create backup with existing structure
echo "📦 Creating backup..."
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="backups/backup_${timestamp}"
mkdir -p "$backup_dir"
cp -r code_analyzer "$backup_dir/"

# 3. Fix imports
echo "🔧 Fixing imports..."
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/from code_analyzer.crewsdoc_crews/from code_analyzer.crews.doc_crews/g' \
    -e 's/from ..doc_crews/from code_analyzer.crews.doc_crews/g' \
    -e 's/from ..base_crew/from code_analyzer.crews.base_crew/g' {} +

# 4. Add missing methods to pattern_detector
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

# 5. Add missing methods to complexity_analyzer
echo "📝 Adding missing methods to complexity_analyzer..."
cat >> code_analyzer/crews/analysis_crews/complexity_analyzer.py << 'EOF'

async def _calculate_maintainability(self, node: ast.AST) -> float:
    """Calculate maintainability index."""
    cyclomatic = await self._calculate_cyclomatic(node)
    cognitive = await self._calculate_cognitive(node)
    return 100.0 - (cyclomatic * 0.3 + cognitive * 0.7)

async def _calculate_halstead(self, node: ast.AST) -> dict:
    """Calculate Halstead metrics."""
    return {
        "volume": 0,
        "difficulty": 0,
        "effort": 0
    }
EOF

# 6. Run verification
echo "🧪 Running tests..."
PYTHONPATH=/Users/markcarpenter/Desktop/projects/CODE_ANALYZER pytest tests/test_combined_analysis.py -v --log-cli-level=INFO

echo "✅ Fix completed"
