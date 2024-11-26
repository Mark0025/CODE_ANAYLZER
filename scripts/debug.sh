#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Search pattern in codebase
search_pattern() {
    pattern="$1"
    echo -e "${BLUE}🔍 Searching for: ${pattern}${NC}\n"
    python -c "
from code_analyzer.utils.debug_search import DebugSearcher
searcher = DebugSearcher()
searcher.search_pattern('$pattern')
"
}

# Check for hardcoded values
check_hardcoded() {
    echo -e "${BLUE}🔍 Checking for hardcoded values...${NC}\n"
    patterns=(
        "test-key"
        "your-key-here"
        "placeholder"
        "xxx-xxx"
    )
    
    for pattern in "${patterns[@]}"; do
        search_pattern "$pattern"
    done
}

# Check .env usage
check_env_usage() {
    echo -e "${BLUE}🔍 Checking .env usage...${NC}\n"
    search_pattern "os.getenv"
    search_pattern "load_dotenv"
}

# Main menu
case "$1" in
    "search")
        search_pattern "$2"
        ;;
    "hardcoded")
        check_hardcoded
        ;;
    "env")
        check_env_usage
        ;;
    *)
        echo -e "${RED}Usage:${NC}"
        echo "  ./debug.sh search <pattern>"
        echo "  ./debug.sh hardcoded"
        echo "  ./debug.sh env"
        ;;
esac 