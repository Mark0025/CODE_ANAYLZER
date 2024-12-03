"""Database integration tests."""
import pytest
from loguru import logger
from code_analyzer.crews.error_handler_crew import ErrorHandlerCrew
from code_analyzer.models.crew_output import CrewOutput, LogEntry
from code_analyzer.models.base import get_session

@pytest.fixture(autouse=True)
def setup_logger():
    """Configure logger for tests."""
    logger.remove()  # Remove default handler
    logger.add(lambda msg: None, level="INFO")  # Add null handler for tests

@pytest.mark.asyncio
async def test_log_entry_creation(db_session):
    """Test log entry creation."""
    # Create test crew
    crew = ErrorHandlerCrew("test_path")
    
    # Generate test logs
    crew.logger.info("Test log message")
    crew.logger.error("Test error message")
    
    # Force commit
    db_session.commit()
    
    # Query logs
    logs = db_session.query(LogEntry).filter_by(crew_name="ErrorHandler").all()
    
    # Print logs for debugging
    print(f"\nFound {len(logs)} logs:")
    for log in logs:
        print(f"- {log.level}: {log.message}")
    
    # We should have at least 2 logs
    assert len(logs) >= 2
    
    # Verify content
    messages = [log.message for log in logs]
    assert any("Test log message" in msg for msg in messages)
    assert any("Test error message" in msg for msg in messages)

@pytest.mark.asyncio
async def test_crew_output_saving(db_session):
    """Test crew output saving."""
    crew = ErrorHandlerCrew("test_path")
    
    # Create a test output
    output = CrewOutput(
        crew_name=crew.name,
        output_type="test",
        status="completed",
        results={"test": "data"}
    )
    db_session.add(output)
    db_session.commit()
    
    # Query outputs
    outputs = db_session.query(CrewOutput).filter_by(crew_name="ErrorHandler").all()
    assert len(outputs) > 0
    
    # Verify output content
    latest = outputs[-1]
    assert latest.status == "completed"
    assert latest.results["test"] == "data"

@pytest.mark.asyncio
async def test_crew_database_integration():
    """Test full crew database integration."""
    # Create test crew
    crew = ErrorHandlerCrew("test_path")
    
    # Run analysis
    results = await crew.analyze_and_add_error_handling()
    assert results["status"] == "completed"
    
    # Get session
    session = get_session()
    
    try:
        # Check outputs
        outputs = session.query(CrewOutput).filter_by(
            crew_name="ErrorHandler",
            output_type="error_analysis"
        ).all()
        
        # Should have at least one output
        assert len(outputs) > 0
        
        # Verify latest output
        latest = outputs[-1]
        assert latest.status == "completed"
        assert "files_analyzed" in latest.results
        assert "timestamp" in latest.results
        
        # Check logs
        logs = session.query(LogEntry).filter_by(crew_name="ErrorHandler").all()
        assert len(logs) > 0
        assert any("Analysis completed" in log.message for log in logs)
        
    finally:
        session.close()