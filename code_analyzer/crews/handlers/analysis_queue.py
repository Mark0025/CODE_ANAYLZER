from collections import deque
from pathlib import Path
from typing import Dict, List
from loguru import logger
import asyncio
from .rate_limit import RateLimitHandler

class AnalysisQueue:
    def __init__(self, config: Dict):
        """Initialize analysis queue.
        
        Args:
            config: Configuration dictionary
        """
        self.queues = {
            "fast": deque(),
            "balanced": deque(),
            "depth": deque()
        }
        self.config = config
        self.rate_handler = RateLimitHandler()
        
    def add_files(self, files: List[Path]):
        """Add files to appropriate queues based on complexity"""
        for file in files:
            complexity = self._analyze_complexity(file)
            tier = self._determine_tier(complexity)
            self.queues[tier].append(file)
            
        logger.info(f"Added {len(files)} files to analysis queues")
        
    async def process_queues(self):
        """Process all queues with rate limiting."""
        default_config = {
            "batch_size": 10,
            "concurrent_requests": 1
        }
        
        while any(self.queues.values()):
            for tier in self.queues:
                if self.queues[tier]:
                    # Get config with defaults
                    phase_config = self.config.get("analysis_phases", {}).get(tier, default_config)
                    batch_size = phase_config.get("batch_size", default_config["batch_size"])
                    batch = [self.queues[tier].popleft() 
                            for _ in range(min(batch_size, len(self.queues[tier])))]
                            
                    provider = self.rate_handler.get_available_provider(tier)
                    if provider:
                        await self._process_batch(batch, provider)
                    else:
                        # Re-add to queue if no provider available
                        self.queues[tier].extend(batch)
                        await asyncio.sleep(1)
                        
    def _analyze_complexity(self, file: Path) -> float:
        """Analyze file complexity with encoding detection."""
        try:
            # Try UTF-8 first
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fallback to detected encoding
            import chardet
            with open(file, 'rb') as f:
                raw = f.read()
                encoding = chardet.detect(raw)['encoding'] or 'utf-8'
            with open(file, 'r', encoding=encoding) as f:
                content = f.read()
        
        # Simple complexity score based on file size and content
        score = len(content) / 1000  # Size factor
        score += content.count("class ") * 2  # Class complexity
        score += content.count("def ") * 1.5  # Function complexity
        score += content.count("async ") * 1.5  # Async complexity
        
        return score
        
    def _determine_tier(self, complexity: float) -> str:
        """Determine processing tier based on complexity score"""
        if complexity < 5:
            return "fast"
        elif complexity < 15:
            return "balanced"
        return "depth" 

    async def _process_batch(self, batch: List[Path], provider: Dict) -> None:
        """Process a batch of files.
        
        Args:
            batch: List of files to process
            provider: AI provider configuration
        """
        logger.info(f"Processing batch of {len(batch)} files with {provider['name']}")
        
        for file in batch:
            try:
                # Process file using the provider
                await self.rate_handler.handle_request(provider["name"], 0)  # Token count will be added later
                
                # Add your file processing logic here
                logger.info(f"Processed {file}")
                
            except Exception as e:
                logger.error(f"Error processing {file}: {e}")
                continue 