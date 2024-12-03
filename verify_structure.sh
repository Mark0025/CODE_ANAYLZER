#!/bin/bash
set -e

echo "1. Verifying current structure..."
if [ ! -d "code_analyzer/crews" ]; then
    echo "❌ Missing code_analyzer/crews/"
    exit 1
fi

echo "2. Fixing imports..."
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/from \.\./from code_analyzer.crews/g' \
    -e 's/from crews\./from code_analyzer.crews./g' \
    -e 's/import crews\./import code_analyzer.crews./g' {} +

echo "3. Adding missing methods..."
if [ -f "code_analyzer/crews/analysis_crews/complexity_analyzer.py" ]; then
    # Check if methods already exist
    if ! grep -q "_calculate_maintainability" "code_analyzer/crews/analysis_crews/complexity_analyzer.py"; then
        cat >> code_analyzer/crews/analysis_crews/complexity_analyzer.py << 'EOL'

async def _calculate_maintainability(self, node: ast.AST) -> float:
    """Calculate maintainability index."""
    return 100.0  # Placeholder implementation

async def _calculate_halstead(self, node: ast.AST) -> dict:
    """Calculate Halstead metrics."""
    return {"volume": 0, "difficulty": 0}  # Placeholder implementation
EOL
    fi
fi

echo "4. Running tests..."
pytest tests/ -v --cov=code_analyzer

echo "5. Verifying imports..."
python -c "from code_analyzer.crews.base_crew import BaseCrew" || exit 1

echo "✅ All steps completed"
