#!/bin/bash
set -e

echo "🏗️ Testing and Fixing CODE_ANALYZER..."

# 1. Fix pattern detector method
echo "🔧 Fixing pattern detector..."
python3 -c '
from pathlib import Path
import ast

file_path = Path("code_analyzer/crews/analysis_crews/pattern_detector.py")
content = file_path.read_text()

# Rename method
content = content.replace("async def detect_patterns", "async def analyze_patterns")

# Write back
file_path.write_text(content)
'

# 2. Run test with database logging
echo "🧪 Running test with logging..."
python3 -c '
from code_analyzer.crews.analysis_crews.pattern_detector import PatternDetector
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger
import asyncio
import pendulum

# Set up logging to database
db = DatabaseManager()

async def run_test():
    try:
        # Run analysis
        detector = PatternDetector()
        test_code = """
        class Singleton:
            _instance = None
            
            @classmethod
            def getInstance(cls):
                if cls._instance is None:
                    cls._instance = cls()
                return cls._instance
                
        def long_method():
            # This is a long method
            pass
            pass
            pass
            # More lines...
        """
        
        results = await detector.analyze_patterns(test_code)
        
        # Save results to database
        analysis_record = db.save_crew_output(
            crew_name="test_run",
            output_type="pattern_analysis",
            status="completed",
            results=results
        )
        
        # Log success
        logger.success(f"Analysis complete: {results}")
        
        # Query and show results
        print("\n📊 Database Query Results:")
        latest = db.get_crew_outputs(crew_name="test_run")
        for record in latest:
            print(f"- Analysis at {record.timestamp}")
            print(f"  Status: {record.status}")
            print(f"  Findings: {record.results}")
            
    except Exception as e:
        # Log error
        logger.error(f"Test failed: {e}")
        db.save_crew_output(
            crew_name="test_run",
            output_type="pattern_analysis",
            status="failed",
            results={"error": str(e)}
        )
        raise

asyncio.run(run_test())
'

echo "✨ Test and fix complete!"
