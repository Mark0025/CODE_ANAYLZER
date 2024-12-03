#!/bin/bash

# Ensure we're in project root
cd "$(dirname "$0")/.."

# Run tests with proper environment
PYTHONPATH=. pytest tests/ \
    -v \
    --cov=crews \
    --cov-report=html \
    --cov-report=term-missing 