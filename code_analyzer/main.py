"""Main entry point for code analyzer."""
import os
import sys
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

def check_dependencies():
    """Ensure all required dependencies are installed."""
    required_packages = [
        "loguru",
        "openai",
        "crewai",
        "python-dotenv",
        "pytest",
        "pytest-cov"
    ]
    
    try:
        import pkg_resources
        for package in required_packages:
            pkg_resources.require(package)
    except pkg_resources.DistributionNotFound:
        logger.error(f"Missing required dependencies. Installing...")
        try:
            import subprocess
            subprocess.check_call(["uv", "pip", "install", "-e", "."])
            logger.info("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            sys.exit(1)

def main():
    """Main entry point."""
    # Setup logging first
    logger.remove()
    logger.add(
        "crews/crew-output/logs/code_analyzer_{time}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="500 MB"
    )
    logger.add(sys.stderr, level="INFO")
    
    try:
        # Check dependencies first
        check_dependencies()
        
        # Load environment variables
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OPENAI_API_KEY not found in environment")
            sys.exit(1)
        
        # Rest of your main function...
        
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 