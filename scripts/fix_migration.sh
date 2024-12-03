#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Fixing migration issues...${NC}"

# Fix analyzer location
echo "Moving analyzer.py to correct location..."
mv code_analyzer/analyzer.py code_analyzer/core/analyzer.py 2>/dev/null || true

# Fix imports in all Python files
echo "Updating imports..."
find code_analyzer tests -type f -name "*.py" | while read file; do
    # Fix analyzer import
    sed -i '' 's/from .analyzer/from code_analyzer.core.analyzer/g' "$file"
    sed -i '' 's/from analyzer/from code_analyzer.core.analyzer/g' "$file"
    
    # Fix crews imports
    sed -i '' 's/from crews\./from code_analyzer.crews./g' "$file"
    sed -i '' 's/import crews\./import code_analyzer.crews./g' "$file"
    
    # Fix utils imports
    sed -i '' 's/from utils\./from code_analyzer.utils./g' "$file"
    sed -i '' 's/import utils\./import code_analyzer.utils./g' "$file"
done

# Create missing __init__.py files
echo "Creating missing __init__.py files..."
find code_analyzer -type d | while read dir; do
    touch "$dir/__init__.py"
done

# Reinstall package
echo "Reinstalling package..."
uv pip install -e .

# Run tests
echo "Running tests..."
./run test

echo -e "${GREEN}Fix complete!${NC}" 