"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
import pytest
from pathlib import Path
from code_analyzer.crews.error_handler_crew import ErrorHandlerCrew
from loguru import logger

@pytest.mark.asyncio
async def test_error_handler_analysis():
    """Test error handler crew analysis."""
    # Create test file
    test_file = Path("test_sample.py")
    test_file.write_text("""
def risky_function():
    data = open('nonexistent.txt').read()
    return data.split()

def another_function():
    result = 10 / 0
    return result
    """)
    
    try:
        crew = ErrorHandlerCrew(str(test_file))
        results = await crew.analyze_and_add_error_handling()
        
        # Verify results
        assert results["status"] == "completed"
        assert "files_analyzed" in results
        assert len(results["results"]) > 0
        
        # Check suggested changes
        file_result = results["results"][0]
        assert "try/except blocks needed" in file_result["analysis"]
        assert "FileNotFoundError" in str(file_result["analysis"])
        assert "ZeroDivisionError" in str(file_result["analysis"])
        
    finally:
        # Cleanup
        test_file.unlink(missing_ok=True)

@pytest.mark.asyncio
async def test_error_handler_implementation():
    """Test error handler crew code updates."""
    # Create test file
    test_file = Path("test_implement.py")
    test_file.write_text("""
def risky_function():
    data = open('nonexistent.txt').read()
    return data.split()
    """)
    
    try:
        crew = ErrorHandlerCrew(str(test_file))
        results = await crew.implement_error_handling()
        
        # Verify implementation
        assert results["status"] == "completed"
        
        # Check updated code
        updated_code = test_file.read_text()
        assert "try:" in updated_code
        assert "except FileNotFoundError as e:" in updated_code
        assert "logger.error" in updated_code
        
    finally:
        # Cleanup
        test_file.unlink(missing_ok=True) 