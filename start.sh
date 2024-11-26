#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Source local aliases if they exist
if [ -f "scripts/bin/aliases" ]; then
    source scripts/bin/aliases
fi

echo -e "${BLUE}🚀 Starting Code Analyzer...${NC}\n"

# Activate virtual environment if needed
if [[ -z "${VIRTUAL_ENV}" ]]; then
    source .venv/bin/activate
fi

# Run the application
python code_analyzer/main.py "$@"

echo -e "\n${GREEN}✨ Done!${NC}" 