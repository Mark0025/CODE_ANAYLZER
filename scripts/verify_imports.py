"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
from pathlib import Path
import ast
import sys
from typing import List, Dict
from rich.console import Console
from rich.table import Table

console = Console()

def find_analyzer_imports(file_path: Path) -> List[str]:
    """Find all analyzer imports in a file."""
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())
            
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    if 'analyzer' in name.name:
                        imports.append(name.name)
            elif isinstance(node, ast.ImportFrom):
                if 'analyzer' in node.module:
                    imports.append(f"{node.module}")
                    
        return imports
    except Exception as e:
        console.print(f"[red]Error parsing {file_path}: {e}[/red]")
        return []

def check_imports() -> Dict[str, List[str]]:
    """Check all Python files for analyzer imports."""
    root = Path('.')
    problematic_imports = {}
    
    for file in root.rglob('*.py'):
        if '.venv' in str(file):
            continue
            
        imports = find_analyzer_imports(file)
        if imports:
            if any('code_analyzer.analyzer' in imp for imp in imports):
                problematic_imports[str(file)] = imports
                
    return problematic_imports

def main():
    """Main verification function."""
    console.print("\n[bold blue]Checking analyzer imports...[/bold blue]")
    
    problems = check_imports()
    
    if problems:
        table = Table(title="Files with Incorrect Imports")
        table.add_column("File")
        table.add_column("Current Import")
        table.add_column("Should Be")
        
        for file, imports in problems.items():
            for imp in imports:
                if 'code_analyzer.analyzer' in imp:
                    table.add_row(
                        file,
                        imp,
                        imp.replace('code_analyzer.analyzer', 'code_analyzer.core.analyzer')
                    )
                    
        console.print(table)
        console.print("\n[red]Found problematic imports! Please update them.[/red]")
        sys.exit(1)
    else:
        console.print("[green]All analyzer imports are correct![/green]")

if __name__ == "__main__":
    main() 