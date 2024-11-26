import click
from pathlib import Path
import subprocess
from loguru import logger

@click.group()
def cli():
    """Code Analyzer Test Runner"""
    pass

@cli.command()
@click.option('--all', '-a', is_flag=True, help='Run all tests')
@click.option('--coverage', '-c', is_flag=True, help='Show coverage report')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--file', '-f', help='Test specific file')
@click.option('--pattern', '-p', help='Test files matching pattern')
def test(all, coverage, verbose, file, pattern):
    """Run tests with specified options"""
    cmd = ["pytest"]
    
    if verbose:
        cmd.append("-v")
        
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=term-missing"])
    
    if file:
        cmd.append(file)
    elif pattern:
        cmd.append(f"tests/*{pattern}*")
    elif all:
        cmd.append("tests/")
    else:
        cmd.append("tests/")
        
    logger.info(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)

@cli.command()
def refresh():
    """Refresh environment and run all tests"""
    subprocess.run(["./scripts/refresh.sh"])

if __name__ == "__main__":
    cli() 