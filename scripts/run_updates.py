"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
import asyncio
from pathlib import Path
from code_analyzer.crews.dev_crews.dev_updater_crew import DevUpdaterCrew
import yaml
from loguru import logger

async def main():
    """Run the updates."""
    try:
        updater = DevUpdaterCrew("./")
        logger.info("Initialized DevUpdaterCrew")
        
        with open('updates/fix_linter_errors.yaml') as f:
            update_spec = yaml.safe_load(f)
            
        results = await updater.execute_updates(update_spec)
        
        if results["status"] == "completed":
            logger.success("Updates completed successfully!")
        else:
            logger.error(f"Updates failed: {results.get('error')}")
            
    except Exception as e:
        logger.error(f"Update process failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 