import sys
import subprocess
import os
from pathlib import Path
import tomli  # For reading TOML files
from typing import List, Dict
from loguru import logger
from datetime import datetime

def read_pyproject_toml() -> dict:
    """Read dependencies from pyproject.toml"""
    try:
        with open("pyproject.toml", "rb") as f:
            return tomli.load(f)
    except FileNotFoundError:
        print("Error: pyproject.toml not found")
        sys.exit(1)

def setup_environment():
    """Create and setup virtual environment using UV"""
    venv_path = Path(".venv")
    
    try:
        # Create venv if it doesn't exist
        if not venv_path.exists():
            print("Creating virtual environment...")
            subprocess.run(["uv", "venv", ".venv"], check=True)
        
        # Get Python path
        python_path = venv_path / "bin" / "python"
        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
            
        return python_path
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtual environment: {e}")
        sys.exit(1)

def install_dependencies(python_path: Path):
    """Install dependencies from pyproject.toml using UV"""
    try:
        # Read dependencies from pyproject.toml
        pyproject = read_pyproject_toml()
        dependencies = pyproject["project"]["dependencies"]
        
        print("Installing dependencies with UV...")
        subprocess.check_call([
            "uv", "pip", "install",
            "--python", str(python_path),
            *dependencies
        ])
        
        print("Dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_logging(analysis_path: str) -> None:
    """Setup loguru logger with proper format and file output"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path("crews/crew-output/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove default logger and add our configured one
    logger.remove()
    logger.add(
        log_dir / f"code_analysis_{analysis_path}_{timestamp}.log",
        format="{time} | {level} | {module}:{function}:{line} - {message}",
        level="INFO",
        rotation="500 MB"
    )
    
    # Also add console output
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )

class CodeAnalysisCrew:
    def __init__(self, target_path: str):
        # Import here to avoid circular imports
        from openai import OpenAI
        from crewai import Agent, Task, Crew
        
        # Setup logging for this analysis run
        setup_logging(Path(target_path).name)
        logger.info(f"Initializing code analysis for: {target_path}")
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Create specialized agents
        self.code_analyzer = Agent(
            role='Code Analyzer',
            goal='Analyze code and suggest improvements',
            backstory="""You are an expert software engineer who specializes in 
            code review and suggesting improvements while maintaining functionality.""",
            verbose=True
        )
        
        self.breaking_changes_detector = Agent(
            role='Breaking Changes Detector',
            goal='Identify potential breaking changes in code modifications',
            backstory="""You are an expert in analyzing code changes and identifying
            potential breaking changes or compatibility issues.""",
            verbose=True
        )

def analyze_directory(path: str = ".") -> List[Dict]:
    """Analyze all Python files in directory and their relationships"""
    # Import here to avoid circular imports
    from crewai import Task, Crew
    
    analyzer = CodeAnalysisCrew(path)
    results = {
        "files": [],
        "dependencies": {},
        "suggested_improvements": [],
        "breaking_changes": [],
        "modularization_opportunities": [],
        "library_recommendations": []
    }
    
    # Skip system, backup and build files
    skip_dirs = {
        '.venv', 'code-analyzer-env', '__pycache__', '.git',
        'build', 'dist', '*.egg-info', 'Backup-Melbudget',
        'migration_', 'backup_'
    }
    
    def should_analyze_file(file_path: Path) -> bool:
        """Determine if file should be analyzed"""
        # Skip files in excluded directories
        if any(skip_dir in str(file_path) for skip_dir in skip_dirs):
            return False
            
        # Skip test files for initial analysis
        if 'test' in str(file_path):
            return False
            
        # Only analyze main application code
        valid_dirs = ['melbudget', 'credit_cards', 'app', 'core', 'utils']
        return any(valid_dir in str(file_path) for valid_dir in valid_dirs)
    
    # First pass: Map project structure and dependencies
    dependency_map = {}
    for file_path in Path(path).rglob("*.py"):
        if not should_analyze_file(file_path):
            continue
            
        try:
            logger.info(f"Analyzing file: {file_path}")
            with open(file_path) as f:
                code = f.read()
            
            # Create analysis task
            analysis_task = Task(
                description=f"""Analyze this Python file and provide comprehensive recommendations:
                
                File: {file_path}
                Code: {code}
                
                Consider:
                1. Code Quality & Best Practices
                   - Identify code that could be simplified
                   - Suggest better patterns
                   - Point out potential bugs
                
                2. Modularization Opportunities
                   - Could this code be split into smaller modules?
                   - Should any functionality be moved to a separate package?
                   - Are there repeated patterns across files?
                
                3. Library Recommendations
                   - Are we reinventing the wheel?
                   - What existing libraries could replace custom code?
                   - Which dependencies could be optimized?
                
                4. Integration Points
                   - How does this file interact with others?
                   - Are there potential breaking changes?
                   - What would fix breaking changes?
                
                Provide specific, actionable recommendations with code examples.
                """,
                expected_output="Detailed analysis with specific recommendations",
                agent=analyzer.code_analyzer
            )

            # Run analysis
            crew = Crew(
                agents=[analyzer.code_analyzer, analyzer.breaking_changes_detector],
                tasks=[analysis_task],
                verbose=True
            )

            result = crew.kickoff()
            
            # Parse and categorize recommendations
            analysis = parse_recommendations(result, file_path)
            results["files"].append(analysis)
            
            # Update global recommendations
            update_global_recommendations(results, analysis)
            
        except Exception as e:
            logger.error(f"Failed to analyze {file_path}: {e}")
    
    # Second pass: Analyze relationships and suggest larger improvements
    results["modularization_opportunities"].extend(
        analyze_project_structure(dependency_map)
    )
    
    return results

def analyze_imports(code: str) -> Dict:
    """Analyze imports and their usage in code"""
    # Implementation to analyze imports
    pass

def parse_recommendations(result: str, file_path: str) -> Dict:
    """Parse and structure the AI recommendations"""
    return {
        "file": str(file_path),
        "improvements": [],
        "breaking_changes": [],
        "library_suggestions": [],
        "modularization": []
    }

def update_global_recommendations(results: Dict, analysis: Dict):
    """Update global recommendation lists"""
    # Implementation to aggregate recommendations
    pass

def analyze_project_structure(dependency_map: Dict) -> List[Dict]:
    """Analyze overall project structure and suggest improvements"""
    return [
        {
            "type": "modularization",
            "suggestion": "Split into separate package",
            "affected_files": [],
            "reasoning": "",
            "implementation_steps": []
        }
    ]

def main():
    # Setup environment and install dependencies
    if not os.environ.get("CREW_VENV_ACTIVE"):
        python_path = setup_environment()
        install_dependencies(python_path)
        
        # Rerun script in venv
        print("Activating virtual environment...")
        os.environ["CREW_VENV_ACTIVE"] = "1"
        os.execv(str(python_path), [str(python_path), __file__])
    
    # Now import dependencies after they're installed
    from dotenv import load_dotenv
    from loguru import logger
    from crewai import Agent, Task, Crew  # Only import what we need
    from crews.output_formatter import AnalysisFormatter
    import json
    
    # Initialize
    load_dotenv()
    logger.info("Starting code analysis...")
    
    # Run analysis on core project files only
    core_dirs = [
        "melbudget/credit_cards",
        "melbudget/app",
        "melbudget/core",
        "melbudget/utils"
    ]
    
    results = []
    for dir_name in core_dirs:
        if Path(dir_name).exists():
            logger.info(f"Analyzing core directory: {dir_name}")
            results.extend(analyze_directory(dir_name))
    
    # Save results
    output_dir = Path("crews/crew-output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "complete_analysis.json"
    output_file.write_text(json.dumps(results, indent=2))
    
    print(f"\nAnalysis complete! Results saved to:")
    print(f"- Complete analysis: {output_file}")
    print(f"- Individual analyses: crews/crew-output/analysis/")

if __name__ == "__main__":
    main()
