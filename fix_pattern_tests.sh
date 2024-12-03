#!/bin/bash
set -e

echo "🧪 Fixing Pattern Detection Tests..."

# Update test patterns script
cat > test_patterns.sh << 'EOF'
#!/bin/bash
set -e

echo "🧪 Testing Pattern Detection with Database Logging..."

python3 -c '
from code_analyzer.crews.analysis_crews.pattern_detector import PatternDetector
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger
import asyncio

async def run_test():
    try:
        # Create valid test code
        test_code = """
class TestClass:
    def test_method(self):
        pass
        """
        
        detector = PatternDetector()
        results = await detector.analyze_patterns(test_code)
        
        logger.success(f"Analysis complete!")
        logger.info(f"Results: {results}")
        
        # Show database records
        print("\n📊 Database Records:")
        db = DatabaseManager()
        outputs = db.get_crew_outputs(crew_name="pattern_detector")
        for record in outputs:
            print(f"Analysis at: {record.timestamp}")
            print(f"Status: {record.status}")
            print(f"Findings: {record.results}")
            
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

asyncio.run(run_test())
'

echo "✨ Test complete!"
EOF

chmod +x test_patterns.sh

echo "✅ Pattern tests fixed!"
