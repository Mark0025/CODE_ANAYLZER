"""Setup environment for CODE_ANALYZER."""
from pathlib import Path
import shutil

def setup_environment():
    """Create all required directories and verify structure."""
    # Base directories
    dirs = {
        "core": "code_analyzer/core",
        "output": "code_analyzer/core/output",
        "db": "code_analyzer/core/output/db",
        "logs": "code_analyzer/core/output/logs",
        "templates": "code_analyzer/monitoring/templates",
        "static": "code_analyzer/monitoring/static",
    }
    
    # Create directories
    for name, path in dirs.items():
        Path(path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {name} directory: {path}")
    
    # Verify templates
    template_files = [
        "index.html",
        "dashboard.html",
        "crews.html",
        "crew_detail.html",
        "analytics.html",
        "codebase_overview.html",
        "dev_now.html"
    ]
    
    templates_dir = Path("code_analyzer/monitoring/templates")
    for template in template_files:
        template_path = templates_dir / template
        if not template_path.exists():
            print(f"✗ Missing template: {template}")
        else:
            print(f"✓ Found template: {template}")
    
    print("\nEnvironment setup complete!")

if __name__ == "__main__":
    setup_environment() 