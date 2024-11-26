"""Tests for the analyzer module."""
import pytest
from pathlib import Path
from loguru import logger
from crews.code_analysis_crew import CodeAnalysisCrew

@pytest.mark.asyncio
async def test_self_analysis(test_project_path, mock_crew_response):
    """Test analyzing the code_analyzer project itself"""
    logger.info(f"Testing self-analysis on {test_project_path}")
    
    crew = CodeAnalysisCrew(str(test_project_path))
    results = await crew.analyze_directory(str(test_project_path))
    
    assert "timestamp" in results
    assert "analysis_results" in results
    assert "path_analyzed" in results
    assert str(test_project_path) in results["path_analyzed"]

@pytest.mark.asyncio
async def test_analyze_specific_module(mock_crew_response):
    """Test analyzing a specific module"""
    module_path = Path("code_analyzer/analyzer.py")
    logger.info(f"Testing analysis of {module_path}")
    
    crew = CodeAnalysisCrew(str(module_path))
    results = await crew.analyze_directory(str(module_path))
    
    assert "analysis_results" in results
    assert "summary" in results
    assert results["summary"]["scan_complete"] is True

@pytest.mark.asyncio
@pytest.mark.parametrize("directory", [
    "code_analyzer",
    "crews",
    "tests"
])
async def test_analyze_directories(directory, test_project_path, mock_crew_response):
    """Test analyzing different project directories"""
    dir_path = test_project_path / directory
    logger.info(f"Testing analysis of directory: {directory}")
    
    crew = CodeAnalysisCrew(str(dir_path))
    results = await crew.analyze_directory(str(dir_path))
    
    assert results is not None
    assert "timestamp" in results
    assert "analysis_results" in results
    assert "summary" in results
    assert results["summary"]["scan_complete"] is True 