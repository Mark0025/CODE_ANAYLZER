from pathlib import Path
from typing import Dict, Any
from loguru import logger
import asyncio
from contextlib import asynccontextmanager
from code_analyzer.utils.resource_monitor import ResourceMonitor
from code_analyzer.models.db_manager import DatabaseManager
import pendulum

class BaseCrew:
    """Base class for all crews with resource management."""
    
    def __init__(self, name: str, target_path: str):
        self.name = name
        self.target_path = target_path
        self.output_dir = Path("core/output") / name.lower()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize resource monitor first
        self.resource_monitor = ResourceMonitor()
        
        # Initialize logger with crew name
        self.logger = logger.bind(crew_name=self.name)
        
        # Initialize database manager
        self.db = DatabaseManager()
        
        # Track active resources
        self._active_resources = set()
        
    @asynccontextmanager
    async def managed_operation(self):
        """Context manager for any crew operation."""
        try:
            await self.resource_monitor.track_resource('crew', self)
            yield
        finally:
            await self.resource_monitor.untrack_resource('crew', self)
            await self.cleanup()
            
    @asynccontextmanager
    async def managed_file(self, path: Path):
        """Safely manage file resources."""
        file_obj = None
        try:
            file_obj = open(path)
            await self.resource_monitor.track_resource('file', file_obj)
            yield file_obj
        finally:
            if file_obj:
                await self.resource_monitor.untrack_resource('file', file_obj)
                file_obj.close()
                
    async def throttle(self):
        """Throttle operations if CPU is high."""
        if self.resource_monitor.check_resources()["cpu_percent"] > 80:
            await asyncio.sleep(0.1)
            
    async def cleanup(self):
        """Clean up all resources."""
        for resource in self._active_resources.copy():
            try:
                if hasattr(resource, 'close'):
                    resource.close()
                self._active_resources.remove(resource)
            except Exception as e:
                self.logger.error(f"Cleanup failed for resource: {e}")
                
    def get_timestamp(self) -> str:
        """Get standardized timestamp in UTC."""
        return pendulum.now('UTC').isoformat()
        
    async def save_output(self, output: Dict[str, Any]) -> None:
        """Save crew output to database."""
        try:
            self.db.save_crew_output(
                crew_name=self.name,
                output=output
            )
            self.logger.info(f"Saved output: {output}")
        except Exception as e:
            self.logger.error(f"Failed to save output: {e}")
            raise