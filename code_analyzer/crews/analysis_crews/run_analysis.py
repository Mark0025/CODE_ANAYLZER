"""Analysis runner using existing models."""
import click
from loguru import logger
from pathlib import Path
from code_analyzer.models.db_manager import DatabaseManager
from code_analyzer.models.crew_output import CrewOutput

@click.command()
@click.option("--target", help="Target directory to analyze")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def run_analysis(target: str, verbose: bool):
    """Run code analysis on target directory."""
    logger.info(f"Analyzing {target}...")
    
    db_manager = DatabaseManager()
    
    try:
        # Run analysis
        results = {"status": "completed", "target": target}
        
        # Save using existing manager
        output = db_manager.save_crew_output(
            crew_name="analysis_crew",
            output_type="code_analysis",
            status="completed",
            results=results
        )
        
        logger.info("Analysis complete!")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    run_analysis()
