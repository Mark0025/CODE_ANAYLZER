"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
import psutil
import os
from pathlib import Path
from loguru import logger
from typing import Dict, List, Any
import asyncio
import time

class ResourceMonitor:
    """Monitor system resources and file handles."""
    
    def __init__(self, cpu_threshold: float = 95.0):
        self.process = psutil.Process()
        self.cpu_threshold = cpu_threshold
        self.open_files = set()
        self._lock = asyncio.Lock()
        
    async def track_resource(self, resource_type: str, resource: Any):
        """Track a resource with locking."""
        async with self._lock:
            if resource_type == 'file':
                self.open_files.add(id(resource))
                
    async def untrack_resource(self, resource_type: str, resource: Any):
        """Untrack a resource with locking."""
        async with self._lock:
            if resource_type == 'file':
                self.open_files.discard(id(resource))
                
    def check_resources(self) -> Dict:
        """Check resources with better CPU sampling."""
        try:
            # Average CPU over 3 samples
            cpu_samples = []
            for _ in range(3):
                cpu_samples.append(self.process.cpu_percent())
                time.sleep(0.1)
            
            cpu_percent = sum(cpu_samples) / len(cpu_samples)
            memory_info = self.process.memory_info()
            
            return {
                "cpu_percent": cpu_percent,
                "memory_mb": memory_info.rss / 1024 / 1024,
                "open_files": len(self.open_files)
            }
            
        except Exception as e:
            logger.error(f"Resource check failed: {e}")
            return {
                "cpu_percent": 0,
                "memory_mb": 0,
                "open_files": 0
            }
        
    def cleanup(self):
        """Force cleanup of resources."""
        for file in self.open_files:
            try:
                file.close()
            except:
                pass
        self.open_files.clear() 