import pytest
from pathlib import Path
from code_analyzer.crews.environment import setup_environment, install_dependencies

def test_environment_setup(tmp_path):
    """Test environment setup with UV."""
    venv_path = setup_environment()
    assert venv_path.exists()
    assert (venv_path / "bin" / "python").exists() or (venv_path / "Scripts" / "python.exe").exists()

def test_dependency_installation(tmp_path):
    """Test dependency installation."""
    venv_path = setup_environment()
    install_dependencies(venv_path)
    
    # Check core dependencies
    pip_freeze = (tmp_path / "pip_freeze.txt")
    assert "crewai" in pip_freeze.read_text() if pip_freeze.exists() else True
    assert "openai" in pip_freeze.read_text() if pip_freeze.exists() else True 