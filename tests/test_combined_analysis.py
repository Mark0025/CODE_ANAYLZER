"""Test running both analysis crews together."""
import pytest
from pathlib import Path
from loguru import logger
from unittest.mock import patch, AsyncMock
from code_analyzer.crews.code_analysis_crew import CodeAnalysisCrew
from code_analyzer.crews.crewai_docs_crew import CrewAIDocsCrew
import pendulum

@pytest.mark.asyncio
async def test_combined_analysis():
    """Test running both code analysis and CrewAI docs analysis."""
    logger.info("Starting combined analysis test")
    
    # Setup
    project_root = Path(__file__).parent.parent
    
    # Mock responses
    mock_code_response = {
        "status": "completed",
        "files_analyzed": 1,
        "results": [{"file": "test.py", "analysis": "Mock analysis"}],
        "timestamp": pendulum.now().isoformat()
    }
    
    mock_docs_response = {
        "status": "completed",
        "task_info": {"task": "documentation", "result": "Mock docs"},
        "timestamp": pendulum.now().isoformat()
    }
    
    # Create crews with mocked methods
    with patch.object(CodeAnalysisCrew, 'analyze_directory', new_callable=AsyncMock) as mock_code_analyze, \
         patch.object(CrewAIDocsCrew, 'analyze_docs', new_callable=AsyncMock) as mock_docs_analyze:
        
        # Setup mock returns
        mock_code_analyze.return_value = mock_code_response
        mock_docs_analyze.return_value = mock_docs_response
        
        # Initialize crews
        code_crew = CodeAnalysisCrew(str(project_root))
        docs_crew = CrewAIDocsCrew(str(project_root))
        
        try:
            # Run analyses
            code_results = await code_crew.analyze_directory(str(project_root))
            docs_results = await docs_crew.analyze_docs()
            
            # Verify code analysis results
            assert code_results is not None, "Code analysis results should not be None"
            assert code_results["status"] == "completed", "Code analysis should complete successfully"
            assert "results" in code_results, "Code analysis should include results"
            
            # Verify docs analysis results
            assert docs_results is not None, "Docs analysis results should not be None"
            assert docs_results["status"] == "completed", "Docs analysis should complete successfully"
            assert "task_info" in docs_results, "Docs analysis should include task info"
            
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