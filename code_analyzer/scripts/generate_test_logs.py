"""Generate test logs for development."""
from code_analyzer.models.db_manager import DatabaseManager
from datetime import datetime
import random
import time

def generate_test_logs():
    """Generate some test logs."""
    db = DatabaseManager()
    
    # Sample crews
    crews = ["CodeAnalysisCrew", "ErrorHandlerCrew", "StatusCrew"]
    
    # Sample messages
    messages = [
        "Analyzing code structure...",
        "Found potential optimization",
        "Processing file: main.py",
        "Detected code pattern",
        "Running security checks",
        "Updating documentation",
        "Performing health check"
    ]
    
    # Sample log levels
    levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    
    # Generate 10 test logs
    for i in range(10):
        db.save_log_entry(
            level=random.choice(levels),
            message=random.choice(messages),
            metadata={
                "test": True,
                "index": i,
                "timestamp": datetime.utcnow().isoformat()
            },
            crew_name=random.choice(crews)
        )
        time.sleep(0.5)  # Small delay between logs
        print(f"Generated log {i+1}/10")

if __name__ == "__main__":
    generate_test_logs() 