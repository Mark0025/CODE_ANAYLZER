"""Test running both analysis crews together."""
import pytest
from pathlib import Path
from loguru import logger
from code_analyzer.crews.code_analysis_crew import CodeAnalysisCrew
from code_analyzer.crews.crewai_docs_crew import CrewAIDocsCrew
import pendulum

@pytest.mark.asyncio
async def test_combined_analysis():
    """Test running both code analysis and CrewAI docs analysis."""
    logger.info("Starting combined analysis test")
    
    # Setup
    project_root = Path(__file__).parent.parent
    code_crew = CodeAnalysisCrew(str(project_root))
    docs_crew = CrewAIDocsCrew(str(project_root))
    
    try:
        # Run analyses
        code_results = await code_crew.analyze_directory(str(project_root))
        docs_results = await docs_crew.analyze_docs()
        
        # Verify code analysis results
        assert code_results is not None, "Code analysis results should not be None"
        assert code_results["status"] == "completed", "Code analysis should complete successfully"
        assert "analysis_results" in code_results, "Code analysis should include results"
        
        # Verify docs analysis results
        assert docs_results is not None, "Docs analysis results should not be None"
        assert docs_results["status"] == "completed", "Docs analysis should complete successfully"
        assert "task_info" in docs_results, "Docs analysis should include task info"
        
        # Verify output files
        code_output = Path("crews/crew-output/codeanalysis/latest_analysis.json")
        docs_output = Path("crews/crew-output/crewaidocs/latest_documentation.json")
        
        assert code_output.exists(), "Code analysis output file should exist"
        assert docs_output.exists(), "Docs analysis output file should exist"
        
        # Return combined results
        return {
            "status": "completed",
            "code_analysis": code_results,
            "docs_analysis": docs_results,
            "timestamp": pendulum.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Combined analysis failed: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": pendulum.now().isoformat()
        }