#!/bin/bash
set -e

echo "🧪 Running Phased Tests..."

# Phase 1: Core Components
echo "📦 Testing Core Components..."
python -m pytest tests/core/ -v

# Phase 2: Pattern Detection
echo "🔍 Testing Pattern Detection..."
python -m pytest tests/patterns/ -v

# Phase 3: Full Analysis
echo "🎯 Running Full Analysis..."
python -m code_analyzer.cli.main analyze ./ --verbose

echo "✨ Test suite complete!"
