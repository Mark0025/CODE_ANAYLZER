import sys
import subprocess
from pathlib import Path
import tomli
from typing import Dict
from loguru import logger

def read_pyproject_toml() -> Dict:
    """Read dependencies from pyproject.toml"""
    try:
        with open("pyproject.toml", "rb") as f:
            return tomli.load(f)
    except FileNotFoundError:
        logger.error("Error: pyproject.toml not found")
        sys.exit(1)

def setup_environment() -> Path:
    """Create and setup virtual environment using UV."""
    venv_path = Path(".venv")
    
    try:
        if not venv_path.exists():
            logger.info("Creating virtual environment...")
            subprocess.run(["uv", "venv", str(venv_path)], check=True)
        
        # Get correct python path based on platform
        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"
            
        if not python_path.exists():
            raise RuntimeError(f"Python executable not found at {python_path}")
            
        return venv_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create virtual environment: {e}")
        sys.exit(1)

def install_dependencies(python_path: Path) -> None:
    """Install dependencies from pyproject.toml using UV"""
    try:
        pyproject = read_pyproject_toml()
        dependencies = pyproject["project"]["dependencies"]
        
        logger.info("Installing dependencies with UV...")
        subprocess.check_call([
            "uv", "pip", "install",
            "--python", str(python_path),
            *dependencies
        ])
        
        # Install test dependencies
        subprocess.check_call([
            "uv", "pip", "install",
            "-e", ".",  # Install package in editable mode
        ])
        
        logger.info("Dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing dependencies: {e}")
        sys.exit(1) 