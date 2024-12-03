#!/bin/bash
set -e

echo "🔄 Setting up virtual environment..."
python -m venv .venv
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🧪 Installing test dependencies..."
pip install pytest pytest-asyncio pytest-cov loguru

echo "✅ Dependencies installed"

# Verify installation
python -c "
from loguru import logger
logger.info('Dependencies verified!')
"

echo "🧪 Running tests..."
pytest tests/ -v --log-cli-level=INFO
