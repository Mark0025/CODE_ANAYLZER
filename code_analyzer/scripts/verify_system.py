"""System verification utilities."""
from pathlib import Path
from loguru import logger
from code_analyzer.models.db_manager import DatabaseManager

def verify_system(verbose: bool = False) -> bool:
    """Verify system state and components."""
    try:
        # Check directories
        required_dirs = [
            "code_analyzer/core/output/db",
            "code_analyzer/core/output/logs",
            "code_analyzer/monitoring/templates",
            "code_analyzer/monitoring/static"
        ]
        
        for dir_path in required_dirs:
            path = Path(dir_path)
            if not path.exists():
                if verbose:
                    logger.warning(f"Creating missing directory: {dir_path}")
                path.mkdir(parents=True, exist_ok=True)
        
        # Check database
        db = DatabaseManager()
        db.verify_connection()
        
        if verbose:
            logger.info("System verification complete")
        return True
        
    except Exception as e:
        logger.error(f"System verification failed: {e}")
        return False 