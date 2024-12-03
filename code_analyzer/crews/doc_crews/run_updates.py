"""
Run documentation updates using DocUpdaterCrew
"""
import click
import yaml
from pathlib import Path
from loguru import logger
from code_analyzer.crewsdoc_crews.doc_updater_crew import DocUpdaterCrew

@click.command()
@click.option(
    "--spec",
    required=True,
    help="Path to the update specification YAML file"
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose output"
)
@click.option(
    "--target",
    required=True,
    help="Target directory to update"
)
def run_updates(spec: str, verbose: bool, target: str):
    """Run documentation updates based on specification."""
    try:
        # Load update spec
        logger.info(f"Loading update spec from: {spec}")
        with open(spec, 'r') as f:
            update_spec = yaml.safe_load(f)
            
        # Log loaded spec
        logger.info(f"Loaded update specification: {update_spec['update_plan']['name']}")
        logger.info(f"Target directory: {target}")
        
        # Create target path
        target_path = Path(target)
        
        # Run async update
        import asyncio
        async def run():
            updater = DocUpdaterCrew(name="DocUpdater", target_path=str(target_path))
            results = await updater.update_docs(update_spec)
            
            if verbose:
                click.echo("\nUpdate Results:")
                click.echo(yaml.dump(results, indent=2))
                
        asyncio.run(run())
        
    except Exception as e:
        logger.error(f"Failed to run updates: {e}")
        raise

if __name__ == '__main__':
    run_updates() 