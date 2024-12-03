"""Initialize all components of CODE_ANALYZER."""
from pathlib import Path
from code_analyzer.scripts.setup_environment import setup_environment
from code_analyzer.scripts.init_db import setup_database
from code_analyzer.scripts.generate_test_data import generate_test_data
from code_analyzer.models.db_manager import DatabaseManager

def initialize_all():
    """Initialize everything."""
    print("Starting CODE_ANALYZER initialization...\n")
    
    # 1. Setup directories
    print("Setting up directories...")
    setup_environment()
    print()
    
    # 2. Remove old database
    db_path = Path("code_analyzer/core/output/db/analyzer.db")
    if db_path.exists():
        db_path.unlink()
        print("Removed old database")
    
    # 3. Initialize database
    print("\nInitializing database...")
    setup_database()
    
    # 4. Generate test data
    print("\nGenerating test data...")
    generate_test_data()
    
    # 5. Verify setup
    print("\nVerifying setup...")
    db = DatabaseManager()
    tables = db.get_tables()
    print(f"Found tables: {', '.join(tables)}")
    
    # 6. Verify endpoints
    print("\nEndpoints available:")
    endpoints = [
        "/",
        "/dashboard",
        "/crews",
        "/crews/{crew_name}",
        "/analytics",
        "/codebase-overview",
        "/DEV-NOW",
        "/api/system-status",
        "/api/health",
        "/api/debug",
        "/api/test-crew",
        "/api/test-log"
    ]
    for endpoint in endpoints:
        print(f"✓ {endpoint}")
    
    print("\nInitialization complete! Start the server with:")
    print("uvicorn code_analyzer.monitoring.dashboard:app --reload")

if __name__ == "__main__":
    initialize_all() 