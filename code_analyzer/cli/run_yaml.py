"""YAML-based command runner for CODE_ANALYZER."""
import sys
import yaml
import click
from pathlib import Path
from loguru import logger
from code_analyzer.models.db_manager import DatabaseManager
from code_analyzer.scripts.init_db import setup_database
from code_analyzer.scripts.verify_system import verify_system

@click.command()
@click.argument('yaml_file', type=click.Path(exists=True))
@click.option('--force', is_flag=True, help='Force run without confirmation')
def run_yaml(yaml_file: str, force: bool = False):
    """Run CODE_ANALYZER commands from YAML file."""
    logger.info(f"Loading YAML file: {yaml_file}")
    
    try:
        with open(yaml_file) as f:
            config = yaml.safe_load(f)
        
        # Print plan
        print("\n🚀 CODE_ANALYZER Implementation Plan")
        print("=" * 50)
        print(f"Name: {config['name']}")
        print(f"Version: {config['version']}")
        print(f"Priority: {config['priority']}")
        print("=" * 50)
        
        if not force:
            confirm = input("\nProceed with implementation? [y/N]: ")
            if confirm.lower() != 'y':
                print("Implementation cancelled.")
                return
        
        # Execute sequence
        for step in config['sequence']:
            print(f"\n⚡ Executing: {step['name']}")
            
            if 'command' in step:
                # Execute command
                result = system(step['command'])
                if result != 0:
                    raise Exception(f"Command failed: {step['command']}")
            
            if 'steps' in step:
                for substep in step['steps']:
                    print(f"  📍 {substep['name']}")
                    if 'yaml' in substep:
                        # Execute sub-yaml
                        run_yaml(substep['yaml'], force=True)
        
        # Verify implementation
        print("\n🔍 Verifying implementation...")
        verify_system()
        
        print("\n✅ Implementation complete!")
        print(f"Visit: http://localhost:8000/DEV-NOW")
        
    except Exception as e:
        logger.error(f"Implementation failed: {e}")
        if not force:
            print("\n🔄 Rolling back changes...")
            system("python -m code_analyzer.scripts.rollback --all")
        sys.exit(1)

if __name__ == "__main__":
    run_yaml() 