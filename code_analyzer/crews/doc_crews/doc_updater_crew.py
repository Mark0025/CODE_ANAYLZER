"""
DocUpdaterCrew for systematic documentation updates
"""
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
import pendulum
from code_analyzer.crews.base_crew import BaseCrew
from pydantic import BaseModel, Field
import yaml

class DocUpdate(BaseModel):
    type: str
    target: str
    content: Dict[str, Any]
    template: str = Field(default="default")

class DocUpdaterCrew(BaseCrew):
    """Crew for handling documentation updates."""
    
    async def update_docs(self, update_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Update documentation based on specification."""
        async with self.managed_operation():
            try:
                # Create log directory
                log_dir = Path(self.target_path) / "core/output/logs"
                log_dir.mkdir(parents=True, exist_ok=True)
                
                # Configure file logging
                logger.add(
                    log_dir / "doc_updater.log",
                    rotation="1 day",
                    retention="7 days",
                    level="DEBUG"
                )
                
                # Debug logging
                self.logger.debug(f"Received update_spec: {yaml.dump(update_spec)}")
                
                # Validate spec structure
                if "update_plan" not in update_spec:
                    self.logger.error("Missing 'update_plan' key")
                    self.logger.debug(f"Available keys: {list(update_spec.keys())}")
                    raise ValueError("Missing 'update_plan' in specification")
                
                plan = update_spec["update_plan"]
                self.logger.debug(f"Found update_plan: {yaml.dump(plan)}")
                
                if "content" not in plan:
                    self.logger.error("Missing 'content' key in update_plan")
                    self.logger.debug(f"Available keys in plan: {list(plan.keys())}")
                    raise ValueError("Missing 'content' in update_plan")
                
                if "readme" not in plan["content"]:
                    self.logger.error("Missing 'readme' key in content")
                    self.logger.debug(f"Available keys in content: {list(plan['content'].keys())}")
                    raise ValueError("Missing 'readme' in content")

                # Create output directory with full path
                output_dir = Path(self.target_path) / "core/output/docs"
                self.logger.info(f"Creating output directory: {output_dir}")
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Generate timestamp for report
                timestamp = self.get_timestamp().replace(":", "-")
                report_file = output_dir / f"doc_update_{timestamp}.md"
                
                results = {
                    "status": "in_progress",
                    "timestamp": self.get_timestamp(),
                    "updates": []
                }
                
                # Update README
                self.logger.info("Updating README.md...")
                readme_results = await self.update_readme(plan["content"]["readme"])
                results["updates"].append(readme_results)
                
                # Generate report
                report_content = f"""
# Documentation Update Report
Generated: {self.get_timestamp()}

## Updates Performed:
{yaml.dump(results, indent=2)}

## Files Modified:
- README.md
- [Other files...]

## Validation:
- [ ] Documentation is accurate
- [ ] Links are working
- [ ] Formatting is correct

## Next Steps:
1. Review generated documentation
2. Verify all sections are complete
3. Check for consistency
                """
                
                # Save report
                report_file.write_text(report_content)
                
                # Create latest symlink
                latest_file = output_dir / "doc_update_latest.md"
                if latest_file.exists():
                    latest_file.unlink()
                latest_file.symlink_to(report_file.name)
                
                results["status"] = "completed"
                results["report_path"] = str(report_file)
                
                self.logger.info(f"Documentation report saved to: {report_file}")
                return results
                
            except Exception as e:
                self.logger.error(f"Documentation update failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                }
    
    async def update_readme(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Update README.md with project information."""
        async with self.managed_operation():
            try:
                readme_path = Path("README.md")
                template = """
# CODE_ANALYZER 🔍

## What it Does
{description}

## Key Features
{features}

## Working Components
{components}

## Installation
```bash
pip install code-analyzer
```

## Quick Start
```python
{quick_start}
```

## Documentation
{documentation}

## Contributing
{contributing}

## License
{license}

---
Built by THE AI RE INVESTOR
For AI Development & Consulting Services
Call: 405-963-2596
                """
                
                content = template.format(**project_info)
                readme_path.write_text(content)
                
                return {
                    "status": "completed",
                    "file": str(readme_path),
                    "timestamp": self.get_timestamp()
                }
                
            except Exception as e:
                logger.error(f"README update failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                } 