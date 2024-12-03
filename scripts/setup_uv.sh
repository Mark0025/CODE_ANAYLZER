#!/bin/bash

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment
echo "Creating virtual environment with uv..."
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies with uv
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Install development dependencies
echo "Installing development dependencies..."
uv pip install pytest pytest-cov pytest-asyncio

# Verify installation
python -c "import click, rich, crewai, loguru" || {
    echo "Error: Dependencies not installed correctly"
    exit 1
}

echo "Setup complete! Virtual environment is active."
echo "Virtual environment: $VIRTUAL_ENV"
echo "Python version: $(python --version)"
echo "To activate the virtual environment, run:"
echo "source .venv/bin/activate" 