#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting project migration...${NC}"

# Create backup
echo -e "${YELLOW}Creating backup...${NC}"
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="../CODE_ANALYZER_backup_${timestamp}"
cp -r . "$backup_dir"
echo -e "${GREEN}Backup created at: ${backup_dir}${NC}"

# Create new structure
echo -e "${YELLOW}Creating new directory structure...${NC}"
mkdir -p code_analyzer/{crews,cli,core,utils,monitoring}

# Move crews
echo -e "${YELLOW}Moving crews...${NC}"
mv crews/* code_analyzer/crews/ 2>/dev/null || true

# Update imports
echo -e "${YELLOW}Updating imports...${NC}"
find . -type f -name "*.py" -exec sed -i '' \
    -e 's/from crews\./from code_analyzer.crews./g' \
    -e 's/import crews\./import code_analyzer.crews./g' {} +

# Move other components
echo -e "${YELLOW}Moving other components...${NC}"
mv code_analyzer/analyzer.py code_analyzer/core/ 2>/dev/null || true
mv code_analyzer/utils/* code_analyzer/utils/ 2>/dev/null || true

# Create __init__.py files
echo -e "${YELLOW}Creating __init__.py files...${NC}"
for dir in code_analyzer/{crews,cli,core,utils,monitoring}; do
    touch "$dir/__init__.py"
done

# Update pyproject.toml
echo -e "${YELLOW}Updating pyproject.toml...${NC}"
cat > pyproject.toml << EOL
[project]
name = "code_analyzer"
version = "0.1.0"
description = "AI-powered code analysis and optimization"
requires-python = ">=3.9"
dependencies = [
    "crewai>=0.1.0",
    "click>=8.0.0",
    "rich>=10.0.0",
    "loguru>=0.7.0",
    "pendulum>=2.0.0",
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "gitpython>=3.1.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "litellm>=1.0.0"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
addopts = "--cov=code_analyzer --cov-report=html --cov-report=term-missing"
testpaths = ["tests"]
asyncio_mode = "auto"

[project.scripts]
code-analyzer = "code_analyzer.cli.main:cli"
EOL

# Update tests
echo -e "${YELLOW}Updating test imports...${NC}"
find tests -type f -name "*.py" -exec sed -i '' \
    -e 's/from crews\./from code_analyzer.crews./g' \
    -e 's/import crews\./import code_analyzer.crews./g' {} +

# Create new run script
echo -e "${YELLOW}Creating new run script...${NC}"
cat > run << EOL
#!/bin/bash

# Ensure we're in project root
cd "\$(dirname "\$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/.initialized" ]; then
    echo "Installing dependencies..."
    uv pip install -e .
    touch .venv/.initialized
fi

# Run command
case "\$1" in
    "test")
        pytest tests/ "\${@:2}"
        ;;
    "analyze")
        python -m code_analyzer.cli.main analyze "\${@:2}"
        ;;
    "clean")
        python -m code_analyzer.cli.main clean "\${@:2}"
        ;;
    *)
        python -m code_analyzer.cli.main "\$@"
        ;;
esac
EOL

chmod +x run

# Clean up
echo -e "${YELLOW}Cleaning up...${NC}"
rm -rf crews/

# Install in development mode
echo -e "${YELLOW}Installing in development mode...${NC}"
source .venv/bin/activate
uv pip install -e .

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
./run test

echo -e "${GREEN}Migration complete!${NC}"
echo -e "${YELLOW}Please check that everything works as expected.${NC}"
echo -e "${YELLOW}Backup is available at: ${backup_dir}${NC}" 