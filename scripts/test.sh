#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Function to run tests
run_tests() {
    echo -e "${GREEN}Running $1 tests...${NC}"
    pytest $2 -v --log-cli-level=INFO
}

# Parse arguments
case "$1" in
    "--all")
        run_tests "all" "tests/"
        ;;
    "--env")
        run_tests "environment" "tests/test_environment.py"
        ;;
    "--crews")
        run_tests "crews" "tests/test_crews.py"
        ;;
    "--real")
        run_tests "real analysis" "tests/test_real_analysis.py"
        ;;
    *)
        echo "Usage: ./test test [--all|--env|--crews|--real]"
        exit 1
        ;;
esac 