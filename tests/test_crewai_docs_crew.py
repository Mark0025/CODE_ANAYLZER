import pytest
from pathlib import Path
from loguru import logger
from code_analyzer.crews.crewai_docs_crew import CrewAIDocsCrew

@pytest.mark.asyncio
async def test_analyze_crewai_docs():
    """Test analyzing CrewAI documentation."""
    crew = CrewAIDocsCrew(str(Path(__file__).parent.parent))
    
    try:
        results = await crew.analyze_docs()
        
        # Verify results
        assert results is not None
        assert "documentation_analysis" in results
        assert "implementation_guide" in results
        assert "recommendations" in results
        
        # Verify output file
        output_file = Path("crews/crew-output/docs-analysis/crewai_docs_analysis.json")
        assert output_file.exists()
        
        logger.success("CrewAI docs analysis completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise 