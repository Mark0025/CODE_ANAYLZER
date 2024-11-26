#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Setting up environment with UV...${NC}"

# Add UV to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}Adding UV to PATH...${NC}"
    export PATH="$HOME/.local/bin:$PATH"
    source "$HOME/.local/bin/env"
fi

# Check if UV is available
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}UV not found. Installing...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    source "$HOME/.local/bin/env"
fi

echo -e "${YELLOW}Creating virtual environment...${NC}"
uv venv .venv

echo -e "${YELLOW}Installing dependencies...${NC}"
source .venv/bin/activate || exit 1

# Verify venv is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${RED}Failed to activate virtual environment${NC}"
    exit 1
fi

# Install dependencies
uv pip install -e .

echo -e "${GREEN}Setup complete! Virtual environment is active.${NC}"
echo -e "${YELLOW}Virtual environment: ${VIRTUAL_ENV}${NC}"
echo -e "${YELLOW}Python version: $(python --version)${NC}"
echo -e "${YELLOW}To activate the virtual environment, run:${NC}"
echo -e "source .venv/bin/activate"

# Keep the venv active in the current shell
exec $SHELL