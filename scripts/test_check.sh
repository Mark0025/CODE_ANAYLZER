#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Running pre-test checks...${NC}"

# Check structure
echo "Checking project structure..."
required_dirs=(
    "code_analyzer/crews"
    "code_analyzer/core"
    "code_analyzer/utils"
    "code_analyzer/cli"
    "code_analyzer/monitoring"
)

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "${RED}Missing directory: $dir${NC}"
        exit 1
    fi
done

# Check critical files
echo "Checking critical files..."
required_files=(
    "code_analyzer/__init__.py"
    "code_analyzer/core/analyzer.py"
    "code_analyzer/crews/base_crew.py"
    "code_analyzer/crews/code_analysis_crew.py"
    "code_analyzer/cli/main.py"
    "pyproject.toml"
    "run"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Missing file: $file${NC}"
        exit 1
    fi
done

# Check imports
echo "Checking imports..."
python3 -c "
import code_analyzer
from code_analyzer.core.analyzer import analyze_directory
from code_analyzer.crews.code_analysis_crew import CodeAnalysisCrew
" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "${RED}Import check failed${NC}"
    exit 1
fi

echo -e "${GREEN}Pre-test checks passed!${NC}"
echo "Ready to run tests. Use:"
echo "./run test" 