"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
from openai import AsyncOpenAI
import asyncio
from .base_crew import BaseCrew
import pendulum

class CodeAnalysisCrew(BaseCrew):
    """Crew for analyzing code with resource management."""
    
    def __init__(self, target_path: str):
        super().__init__("CodeAnalysis", target_path)
        self._client = None
        self.logger.info("Initialized CodeAnalysis crew")
        
    async def analyze_directory(self, directory_path: str) -> Dict[str, Any]:
        """Analyze a directory of code with proper resource management."""
        async with self.managed_operation():
            try:
                directory = Path(directory_path)
                if not directory.exists():
                    raise ValueError(f"Directory not found: {directory}")
                
                results = []
                for file_path in directory.rglob('*.py'):
                    await self.throttle()  # Throttle between files
                    
                    async with self.managed_file(file_path) as f:
                        content = f.read()
                        result = await self._analyze_content(content, str(file_path))
                        results.append(result)
                
                return {
                    "status": "completed",
                    "files_analyzed": len(results),
                    "results": results,
                    "timestamp": self.get_timestamp()
                }
                
            except Exception as e:
                self.logger.error(f"Analysis failed: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                }
                
    async def _analyze_content(self, content: str, file_path: str) -> Dict[str, Any]:
        """Analyze file content with throttling."""
        try:
            await self.throttle()  # Throttle before API call
            
            if not self._client:
                self._client = AsyncOpenAI()
                
            response = await self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "You are a code analysis expert."
                }, {
                    "role": "user",
                    "content": f"Analyze this code:\n\n{content}"
                }]
            )
            
            return {
                "file": file_path,
                "analysis": response.choices[0].message.content,
                "status": "completed"
            }
            
        except Exception as e:
            self.logger.error(f"Content analysis failed: {e}")
            return {
                "file": file_path,
                "status": "failed",
                "error": str(e)
            }