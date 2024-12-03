"""Main CLI entry point."""
import click
from loguru import logger
from code_analyzer.core.analyzer import CodeAnalyzer, analyze_directory
from rich import print as rprint

@click.group()
def cli():
    """CODE_ANALYZER CLI"""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True), required=False)
@click.option('--github', help='GitHub repository URL to analyze')
@click.option('--branch', default='main', help='Git branch to analyze (default: main)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def analyze(path, github, branch, verbose):
    """Analyze code directory or GitHub repository."""
    try:
        if github:
            logger.info(f"Analyzing repository: {github}")
            # TODO: Implement GitHub analysis
            raise NotImplementedError("GitHub analysis not yet implemented")
        else:
            logger.info(f"Analyzing path: {path}")
            results = analyze_directory(path)
            
            # Print results in a nice format
            rprint("\n[bold green]Analysis Results:[/bold green]")
            rprint(f"📂 Path: {results['path']}")
            rprint(f"✨ Status: {results['status']}")
            
            if results['status'] == 'success':
                summary = results['summary']
                rprint("\n[bold]Summary:[/bold]")
                rprint(f"📊 Total files: {summary['total_files']}")
                rprint(f"🐍 Python files: {summary['python_files']}")
                rprint(f"📄 Other files: {summary['other_files']}")
                
                if verbose:
                    rprint("\n[bold]Files Analyzed:[/bold]")
                    for file in results['files_analyzed']:
                        rprint(f"  • {file}")
            else:
                rprint(f"[bold red]Error:[/bold red] {results.get('error', 'Unknown error')}")

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        rprint(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()

@cli.command()
def version():
    """Show version information."""
    from code_analyzer import __version__
    click.echo(f"code-analyzer version {__version__}")

if __name__ == '__main__':
    cli() 