"""Tests for real codebase analysis."""
import pytest
from pathlib import Path
import json
import sys
from datetime import datetime
from loguru import logger
from code_analyzer.crews.code_analysis_crew import CodeAnalysisCrew

# Configure loguru
logger.remove()  # Remove default handler
log_dir = Path("crews/crew-output/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logger.add(
    log_dir / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    rotation="1 day",
    retention="7 days",
    compression="zip"
)
logger.add(sys.stderr, level="INFO")

@pytest.fixture(autouse=True)
def setup_output_directories():
    """Ensure output directories exist."""
    dirs = [
        Path("crews/crew-output"),
        Path("crews/crew-output/analysis"),
        Path("crews/crew-output/logs")
    ]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    logger.info("Created output directories")

@pytest.mark.asyncio
async def test_analyze_real_codebase():
    """Test analyzing our actual codebase with detailed verification."""
    logger.info("Starting real codebase analysis test")
    
    # Setup
    project_root = Path(__file__).parent.parent
    crew = CodeAnalysisCrew(str(project_root))
    logger.info(f"Initialized crew for {project_root}")

    try:
        # Run analysis
        results = await crew.analyze_directory(str(project_root))
        logger.success("Analysis completed")
        
        # Verify results structure
        assert results is not None, "Results should not be None"
        assert isinstance(results, dict), "Results should be a dictionary"
        assert "status" in results, "Results should have status"
        assert results["status"] == "completed", "Analysis should complete successfully"
        assert "documentation_analysis" in results, "Results should include documentation analysis"
        assert "analysis_results" in results, "Results should include analysis results"
        assert "timestamp" in results, "Results should include timestamp"
        logger.info("Verified results structure")

        # Verify output files
        output_dir = Path("crews/crew-output")
        analysis_file = output_dir / "analysis_results.json"
        
        assert output_dir.exists(), "Output directory should exist"
        assert analysis_file.exists(), "Analysis results file should exist"
        logger.info("Verified output files exist")

        # Verify file content
        try:
            with open(analysis_file, 'r') as f:
                saved_results = json.load(f)
            
            # Verify saved results structure
            assert "status" in saved_results, "Saved results missing status"
            assert "documentation_analysis" in saved_results, "Saved results missing documentation analysis"
            assert "analysis_results" in saved_results, "Saved results missing analysis results"
            assert isinstance(saved_results["analysis_results"], dict), "Analysis results should be a dictionary"
            
            logger.success("Verified saved results structure")
            return results
            
        except Exception as e:
            logger.error(f"Failed to verify saved results: {e}")
            raise
            
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

def test_output_directory_structure():
    """Verify the complete output directory structure."""
    logger.info("Checking output directory structure")
    
    required_dirs = [
        Path("crews/crew-output"),
        Path("crews/crew-output/analysis"),
        Path("crews/crew-output/logs")
    ]
    
    for dir_path in required_dirs:
        assert dir_path.exists(), f"Required directory missing: {dir_path}"
        assert dir_path.is_dir(), f"Path exists but is not a directory: {dir_path}"
    
    logger.success("Output directory structure verified")
