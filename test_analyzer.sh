#!/bin/bash
set -e

echo "🧪 Testing CODE_ANALYZER System..."

# 1. Run analysis on our own codebase
python3 -c '
from code_analyzer.crews.analysis_crews.pattern_detector import PatternDetector
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger
import asyncio

async def test_analysis():
    detector = PatternDetector()
    results = await detector.analyze_patterns("""
    class TestClass:
        def long_method(self):
            # This is a long method
            pass
            pass
            pass
            # ... more lines
    """)
    
    logger.info(f"Analysis results: {results}")

asyncio.run(test_analysis())
'

echo "✨ Test complete!"
