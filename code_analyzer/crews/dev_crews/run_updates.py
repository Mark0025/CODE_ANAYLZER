"""
Run updates using DevUpdaterCrew
"""
import asyncio
import yaml
import click
from pathlib import Path
from loguru import logger
from .dev_updater_crew import DevUpdaterCrew

@click.command()
@click.option('--spec', required=True, help='Path to update specification YAML file')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.option('--target', default=".", help='Target directory path')
def run_updates(spec: str, verbose: bool, target: str):
    """Run updates using the specified YAML configuration."""
    try:
        spec_path = Path(spec)
        if not spec_path.exists():
            click.echo(f"Error: Specification file not found: {spec}")
            return

        target_path = Path(target).resolve()
        if not target_path.exists():
            click.echo(f"Error: Target directory not found: {target}")
            return

        logger.info(f"Loading update spec from: {spec}")
        with open(spec_path) as f:
            update_spec = yaml.safe_load(f)

        if verbose:
            click.echo(f"Loaded update specification: {update_spec['update_plan']['name']}")
            click.echo(f"Target directory: {target_path}")

        async def run():
            updater = DevUpdaterCrew(name="DevUpdater", target_path=str(target_path))
            results = await updater.execute_updates(update_spec)
            
            if verbose:
                click.echo("\nUpdate Results:")
                for key, value in results.items():
                    click.echo(f"{key}: {value}")
            else:
                click.echo(f"Update completed: {results.get('status', 'unknown')}")

        asyncio.run(run())

    except Exception as e:
        logger.error(f"Update failed: {e}")
        click.echo(f"Error: {e}")

if __name__ == '__main__':
    run_updates(prog_name="run_updates") 