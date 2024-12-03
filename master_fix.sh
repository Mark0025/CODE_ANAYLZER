#!/bin/bash
set -e

echo "🏗️ Starting CODE_ANALYZER City Renovation..."

# 1. Fix Storage District (Consolidate Outputs)
echo "📦 Organizing Storage District..."
mkdir -p code_analyzer/core/output/{analysis,logs,db,test_results}
rsync -av --remove-source-files \
    code_analyzer/crews/crew-output/ \
    code_analyzer/core/output/

# 2. Fix Import District
echo "🔄 Fixing Import Paths..."
find code_analyzer -type f -name "*.py" -exec sed -i '' \
    -e 's/from code_analyzer.crewsutils/from code_analyzer.utils/g' \
    -e 's/import code_analyzer.crewsutils/import code_analyzer.utils/g' {} +

# 3. Update Dependencies
echo "📚 Updating City Libraries..."
pip install --upgrade pydantic litellm pytest pytest-asyncio

# 4. Fix Test Configuration
echo "🧪 Optimizing Test Zone..."
cat > tests/conftest.py << 'PYTEST_EOF'
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "timeout: mark test with timeout in seconds"
    )

@pytest.fixture(autouse=True)
def _add_timeout(request):
    item = request.node
    item.add_marker(pytest.mark.timeout(30))
PYTEST_EOF

echo "✅ City Renovation Complete!"
