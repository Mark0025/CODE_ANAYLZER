"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
import asyncio
from pathlib import Path
import yaml
from loguru import logger
from code_analyzer.crews.analyze_crews_crew import AnalyzeCrewsCrew

async def analyze_codebase():
    """Analyze entire codebase structure."""
    try:
        # Initialize crew
        analyzer = AnalyzeCrewsCrew("./")
        
        # Load analysis spec
        with open('DEV-MAN-CREW/analysis/full_codebase_analysis.yaml') as f:
            analysis_spec = yaml.safe_load(f)
            
        # Run analysis
        results = await analyzer.analyze_ecosystem()
        
        # Save detailed analysis
        output_path = Path("DEV-MAN-CREW/ANALYSIS-RESULTS")
        output_path.mkdir(exist_ok=True)
        
        with open(output_path / "FULL-ANALYSIS.md", 'w') as f:
            f.write(results["analysis"])
            
        logger.success("Analysis complete!")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(analyze_codebase()) 