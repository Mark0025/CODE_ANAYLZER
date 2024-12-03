"""
DevUpdaterCrew for systematic code updates
"""
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
import pendulum
from code_analyzer.crews.base_crew import BaseCrew
from pydantic import BaseModel, Field
import yaml

class UpdateChange(BaseModel):
    type: str
    target: str
    imports: List[str] = Field(default_factory=list)
    method: Dict[str, Any] = Field(default_factory=dict)

class UpdatePhase(BaseModel):
    description: str
    changes: List[UpdateChange]

class UpdatePlan(BaseModel):
    name: str
    description: str
    priority: str
    phases: Dict[str, UpdatePhase]

class DevUpdaterCrew(BaseCrew):
    """Crew for handling systematic code updates."""
    
    def __init__(self, name: str, target_path: str):
        super().__init__(name, target_path)
        self.logger.info(f"Initialized {name} for path: {target_path}")

    def _validate_spec(self, update_spec: Dict[str, Any]) -> UpdatePlan:
        """Validate update specification."""
        try:
            if "update_plan" not in update_spec:
                raise ValueError("Missing 'update_plan' in specification")
            
            plan = UpdatePlan(**update_spec["update_plan"])
            return plan
        except Exception as e:
            raise ValueError(f"Invalid update specification: {e}")

    async def execute_updates(self, update_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Execute updates based on specification."""
        async with self.managed_operation():
            try:
                self.logger.info("Starting update execution")
                results = {
                    "status": "in_progress",
                    "timestamp": self.get_timestamp(),
                    "updates": []
                }

                # Validate spec
                plan = self._validate_spec(update_spec)
                self.logger.info(f"Validated update plan: {plan.name}")

                # Execute phases in order
                for phase_name, phase_config in plan.phases.items():
                    phase_result = await self._execute_phase(phase_name, phase_config)
                    results["updates"].append(phase_result)

                results["status"] = "completed"
                return results

            except Exception as e:
                self.logger.error(f"Update execution failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                }

    async def _execute_phase(self, phase_name: str, phase_config: UpdatePhase) -> Dict[str, Any]:
        """Execute a single update phase."""
        self.logger.info(f"Executing phase: {phase_name}")
        
        try:
            # Access Pydantic model attributes properly
            for change in phase_config.changes:
                self.logger.info(f"Processing change type: {change.type}")
                
                if change.type == "add_imports":
                    await self._add_imports(change)
                elif change.type == "add_method":
                    await self._add_timestamp_method(change)
                elif change.type == "add_methods":
                    await self._add_error_handler_methods(change)

            return {
                "phase": phase_name,
                "status": "completed",
                "timestamp": self.get_timestamp()
            }

        except Exception as e:
            self.logger.error(f"Phase {phase_name} failed: {e}")
            return {
                "phase": phase_name,
                "status": "failed",
                "error": str(e),
                "timestamp": self.get_timestamp()
            }

    async def _add_imports(self, change: UpdateChange) -> None:
        """Add imports to target files."""
        async with self.managed_operation():
            target_file = Path(change.target)
            if target_file.exists():
                content = target_file.read_text()
                # Add imports if not present
                for import_line in change.imports:
                    if import_line not in content:
                        new_content = f"{import_line}\n{content}"
                        target_file.write_text(new_content)
                        self.logger.info(f"Added import to {target_file}: {import_line}")

    async def _add_timestamp_method(self, change: UpdateChange) -> None:
        """Add timestamp method to BaseCrew."""
        async with self.managed_operation():
            target_file = Path(change.target)
            if target_file.exists():
                content = target_file.read_text()
                if "get_timestamp" not in content:
                    method_code = change.method["code"]
                    # Add before last class line
                    lines = content.splitlines()
                    insert_point = len(lines) - 1
                    lines.insert(insert_point, method_code)
                    target_file.write_text("\n".join(lines))
                    self.logger.info(f"Added method to {target_file}: {change.method['name']}")

    async def _add_error_handler_methods(self, change: UpdateChange) -> None:
        """Add error handler methods."""
        async with self.managed_operation():
            target_file = Path(change.target)
            if target_file.exists():
                content = target_file.read_text()
                # Add methods from the change
                for method in change.method.get("methods", []):
                    if method["name"] not in content:
                        method_code = method["code"]
                        # Add before last class line
                        lines = content.splitlines()
                        insert_point = len(lines) - 1
                        lines.insert(insert_point, method_code)
                        target_file.write_text("\n".join(lines))
                        self.logger.info(f"Added method to {target_file}: {method['name']}")