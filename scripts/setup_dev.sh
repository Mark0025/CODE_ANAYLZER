#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Code Analyzer development environment...${NC}\n"

# Function to detect shell type
get_shell_rc() {
    if [ -n "$ZSH_VERSION" ]; then
        echo "$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        echo "$HOME/.bashrc"
    else
        echo ""
    fi
}

# Get shell rc file
SHELL_RC=$(get_shell_rc)

if [ -z "$SHELL_RC" ]; then
    echo -e "${RED}❌ Unsupported shell. Please manually add aliases to your shell config.${NC}"
    exit 1
fi

# Create local bin directory if it doesn't exist
mkdir -p scripts/bin

# Create test command
cat > scripts/bin/test <<EOL
#!/bin/bash
python code_analyzer/cli/test_runner.py "\$@"
EOL

# Make it executable
chmod +x scripts/bin/test

# Add aliases to shell config if they don't exist
if ! grep -q "# Code Analyzer aliases" "$SHELL_RC"; then
    echo -e "\n# Code Analyzer aliases" >> "$SHELL_RC"
    echo "alias test='$PWD/scripts/bin/test'" >> "$SHELL_RC"
    echo "alias start='$PWD/start.sh'" >> "$SHELL_RC"
    echo -e "${GREEN}✅ Added aliases to $SHELL_RC${NC}"
else
    echo -e "${YELLOW}⚠️  Aliases already exist in $SHELL_RC${NC}"
fi

# Create or update local aliases file
cat > scripts/bin/aliases <<EOL
# Local project aliases
alias test='$PWD/scripts/bin/test'
alias start='$PWD/start.sh'
EOL

# Make aliases file executable
chmod +x scripts/bin/aliases

echo -e "\n${BLUE}📦 Setting up virtual environment...${NC}"
./scripts/refresh.sh

echo -e "\n${GREEN}✨ Setup complete! To activate aliases, run:${NC}"
echo -e "${YELLOW}source $SHELL_RC${NC}"
echo -e "or"
echo -e "${YELLOW}source scripts/bin/aliases${NC}"

echo -e "\n${BLUE}🧪 You can now use:${NC}"
echo -e "  ${GREEN}test --all${NC}         Run all tests"
echo -e "  ${GREEN}test --coverage${NC}    Run tests with coverage"
echo -e "  ${GREEN}test --file FILE${NC}   Test specific file"
echo -e "  ${GREEN}start${NC}              Start the application" 