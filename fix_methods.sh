#!/bin/bash
set -e

echo "1. Adding missing methods to pattern_detector.py..."
cat >> code_analyzer/crews/analysis_crews/pattern_detector.py << 'EOL'

async def _detect_code_smells(self, node: ast.AST) -> List[PatternMatch]:
    """Detect code smells in AST."""
    smells = []
    # Basic implementation
    return smells

def _is_singleton(self, node: ast.AST) -> bool:
    """Check if class is singleton."""
    return False  # Basic implementation

def _get_class_name(self, node: ast.AST) -> str:
    """Get class name from node."""
    return node.name if hasattr(node, 'name') else 'Unknown'

def _is_factory(self, node: ast.AST) -> bool:
    """Check if class is factory."""
    return False  # Basic implementation
EOL

echo "2. Fixing imports..."
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/from code_analyzer.crewsbase_crew/from code_analyzer.crews.base_crew/g' \
    -e 's/from ..base_crew/from code_analyzer.crews.base_crew/g' {} +

echo "3. Running tests..."
pytest tests/test_combined_analysis.py -v --log-cli-level=DEBUG
