from icecream import ic
from objprint import op
from rich.console import Console
from typing import Any

console = Console()

def debug_object(obj: Any, title: str = "Debug Info") -> None:
    """Enhanced object debugging."""
    console.print(f"\n[bold red]{title}[/]")
    
    # Show with icecream
    ic(obj)
    
    # Show detailed structure
    op.configure(line_numbers=True, color=True)
    op(obj)
    
def debug_code(code: str, title: str = "Code Analysis") -> None:
    """Debug code snippets."""
    console.print(f"\n[bold yellow]{title}[/]")
    console.print(Panel(
        Syntax(code, "python", theme="monokai"),
        border_style="yellow"
    )) 