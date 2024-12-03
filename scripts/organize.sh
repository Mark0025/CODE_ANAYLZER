#!/bin/bash

# Create new structure
mkdir -p code_analyzer/{crews,cli,core}

# Move crews to proper location
mv crews/* code_analyzer/crews/

# Update imports in all files
find code_analyzer -name "*.py" -type f -exec sed -i '' 's/from crews\./from code_analyzer.crews./g' {} +
find code_analyzer -name "*.py" -type f -exec sed -i '' 's/import crews\./import code_analyzer.crews./g' {} + 