#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Pushing all code to GitHub...${NC}"

# Function to check for sensitive files
check_sensitive() {
    if [ -f ".env" ] || [ -f ".env.example" ] || [ -f ".env.template" ]; then
        echo -e "${RED}❌ Found sensitive files! Removing...${NC}"
        rm -f .env .env.example .env.template
    fi
}

# Function to add all code
add_all_code() {
    echo -e "${YELLOW}📦 Adding all code...${NC}"
    
    # Core Python packages
    git add code_analyzer/
    git add crews/
    git add tests/
    
    # Documentation
    git add DEV-MAN-CREW/
    git add docs/
    git add *.md
    
    # Configuration
    git add configs/
    git add pyproject.toml
    git add setup.py
    git add conftest.py
    
    # Scripts
    git add scripts/
    git add *.sh
    
    # Project structure
    git add project_structure
    git add .currsorules
    git add LICENSE
}

# Function to create commit
create_commit() {
    echo -e "${YELLOW}💾 Creating commit...${NC}"
    
    git commit -m "🏗️ Complete Core Architecture Implementation

MAJOR ADDITIONS:
---------------
- Added complete code_analyzer package
- Added crews system
- Added comprehensive documentation
- Added test suite
- Added configuration system

TECHNICAL DETAILS:
----------------
- Removed sensitive files
- Added proper gitignore
- Structured documentation
- Added test infrastructure

Coded by THE AI RE INVESTOR -- WWW.THEAIREINVESTOR.COM
For AI Development & Consulting Services
Call: 405-963-2596"
}

# Function to push
push_code() {
    echo -e "${YELLOW}📤 Pushing to GitHub...${NC}"
    git push origin feature/rebuild-core-architecture
}

# Main execution
check_sensitive
add_all_code
create_commit
push_code

echo -e "${GREEN}✨ Done! Check GitHub for your changes.${NC}" 