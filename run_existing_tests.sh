#!/bin/bash
set -e

echo "�� Running Existing Tests..."

# Run tests in existing structure
echo "📦 Running Tests..."
python -m pytest tests/ -v

# If successful, run analysis
if [ $? -eq 0 ]; then
    echo "🎯 Running Full Analysis..."
    python -m code_analyzer.cli.main analyze ./ --verbose
fi

echo "✨ Test suite complete!"
