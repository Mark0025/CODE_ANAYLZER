import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_current_directory() -> Path:
    """Get the directory where the script is being run from."""
    return Path.cwd()

def analyze_directory(directory_path: Path) -> bool:
    """
    Analyze the contents of the given directory.
    
    Args:
        directory_path: Path object pointing to directory to analyze
        
    Returns:
        bool: True if analysis successful, False otherwise
    """
    try:
        if not directory_path.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return False
            
        if not directory_path.is_dir():
            logger.error(f"Path is not a directory: {directory_path}")
            return False

        # Walk through the directory
        for root, dirs, files in os.walk(directory_path):
            root_path = Path(root)
            logger.info(f"Analyzing {root_path}...")
            
            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if not file.startswith('.'):
                    logger.info(f"Processing file: {file}")
                    # Add your analysis logic here
                    
    except Exception as e:
        logger.error(f"Error analyzing directory: {e}", exc_info=True)
        return False
        
    return True

def main() -> None:
    try:
        # Get the current working directory
        current_dir = get_current_directory()
        logger.info(f"Starting analysis in: {current_dir}")
        
        # Run the analysis
        success = analyze_directory(current_dir)
        
        if not success:
            logger.error("Analysis failed")
            sys.exit(1)
            
        logger.info("Analysis completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 