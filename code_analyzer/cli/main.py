"""Main CLI entry point."""
import os
import sys
import argparse
import tempfile
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
import git
from crews.environment import setup_environment, install_dependencies
from crews.code_analysis_crew import CodeAnalysisCrew
import click

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze code directories')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('path', nargs='?', default=None,
                      help='Path to analyze')
    group.add_argument('--github', type=str,
                      help='GitHub repository URL to analyze')
    parser.add_argument('--branch', type=str, default='main',
                       help='Git branch to analyze (default: main)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    return parser.parse_args()

def clone_repository(url: str, branch: str) -> Path:
    """Clone a GitHub repository to a temporary directory"""
    temp_dir = Path(tempfile.mkdtemp(prefix='code_analyzer_'))
    logger.info(f"Cloning {url} (branch: {branch}) to {temp_dir}")
    
    try:
        git.Repo.clone_from(url, temp_dir, branch=branch)
        return temp_dir
    except Exception as e:
        logger.error(f"Failed to clone repository: {e}")
        sys.exit(1)

def cleanup(temp_dir: Path):
    """Clean up temporary directory"""
    try:
        import shutil
        shutil.rmtree(temp_dir)
        logger.info(f"Cleaned up temporary directory: {temp_dir}")
    except Exception as e:
        logger.warning(f"Failed to clean up {temp_dir}: {e}")

def main():
    # Setup environment if needed
    if not os.environ.get("CREW_VENV_ACTIVE"):
        python_path = setup_environment()
        install_dependencies(python_path)
        
        # Rerun script in venv
        logger.info("Activating virtual environment...")
        os.environ["CREW_VENV_ACTIVE"] = "1"
        os.execv(str(python_path), [str(python_path), __file__])
    
    # Load environment variables
    load_dotenv()
    
    # Parse arguments
    args = parse_args()
    
    try:
        # Handle GitHub repository
        if args.github:
            path = clone_repository(args.github, args.branch)
            cleanup_needed = True
        else:
            path = Path(args.path).resolve()
            cleanup_needed = False
        
        # Initialize crew and run analysis
        crew = CodeAnalysisCrew(str(path))
        results = crew.analyze_directory(str(path))
        
        # Save results
        output_dir = Path("crews/crew-output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        from crews.output_formatter import AnalysisFormatter
        formatter = AnalysisFormatter(path)
        output_file = formatter.save_analysis(results, output_dir)
        
        logger.info(f"Analysis complete! Results saved to: {output_file}")
        
    finally:
        # Cleanup if we cloned a repository
        if cleanup_needed:
            cleanup(path)

@click.command()
def monitor():
    """Launch monitoring dashboard."""
    from code_analyzer.monitoring.dashboard import MonitoringDashboard
    dashboard = MonitoringDashboard()
    dashboard.run()

if __name__ == '__main__':
    main() 