from code_analyzer.models.log_entry import LogEntry
from code_analyzer.models.base import get_session

def verify_model():
    """Verify LogEntry model has get_metadata."""
    # Create test entry
    entry = LogEntry(
        level="INFO",
        message="Test Message",
        crew_name="TEST"
    )
    
    # Verify property exists
    assert hasattr(entry, 'get_metadata'), "get_metadata property missing"
    
    # Verify it returns correct data
    metadata = entry.get_metadata
    assert isinstance(metadata, dict), "get_metadata should return dict"
    assert all(k in metadata for k in ['id', 'timestamp', 'level']), "Missing required fields"
    
    print("✅ Model verification passed")

if __name__ == "__main__":
    verify_model() 