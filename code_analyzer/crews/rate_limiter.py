"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
from typing import Dict
import asyncio
import time
from loguru import logger

class RateLimiter:
    """Rate limiting for API calls."""
    
    def __init__(self):
        self.last_call = 0
        self.calls_per_minute = 50  # Default limit
        self.min_interval = 60.0 / self.calls_per_minute
        self.token_usage = {}
        
    async def should_wait(self) -> bool:
        """Check if we need to wait."""
        current_time = time.time()
        time_since_last = current_time - self.last_call
        return time_since_last < self.min_interval
        
    async def wait(self):
        """Wait if needed."""
        if await self.should_wait():
            wait_time = self.min_interval - (time.time() - self.last_call)
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)
            
    def track_usage(self, tokens: int):
        """Track token usage."""
        current_minute = int(time.time() / 60)
        if current_minute not in self.token_usage:
            self.token_usage = {current_minute: tokens}
        else:
            self.token_usage[current_minute] += tokens
            
    def get_usage(self) -> Dict[str, int]:
        """Get current usage stats."""
        current_minute = int(time.time() / 60)
        return {
            "current_minute_tokens": self.token_usage.get(current_minute, 0),
            "total_tokens": sum(self.token_usage.values())
        } 