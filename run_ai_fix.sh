#!/bin/bash
set -e

echo "🤖 Starting AI-Powered Fix..."

# Set up context
echo "📚 Preparing AI Context..."
python3 -c "
from code_analyzer.utils.ai_helpers import create_context
context = create_context([
    'TEST-EXECUTION-ANALYSIS.md',
    'GOALS.md',
    'test_run_*.log'
])
"

# Run AI fix
echo "🔧 Running AI Fix..."
python3 ai_powered_fix.py

echo "✨ AI Fix complete!"
