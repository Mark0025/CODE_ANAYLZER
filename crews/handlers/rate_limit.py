from typing import Dict, Optional
import json
from pathlib import Path
import asyncio
from loguru import logger
import pendulum
from code_analyzer.utils.rate_monitor import RateMonitor

class RateLimitHandler:
    """Smart rate limit handler with tiered model approach."""
    
    def __init__(self):
        self.config = self._load_config()
        self.monitor = RateMonitor()
        self.usage = {
            "gpt-3.5-turbo": {
                "tokens": 0,
                "last_reset": pendulum.now(),
                "requests": []
            },
            "gpt-4": {
                "tokens": 0,
                "last_reset": pendulum.now(),
                "requests": []
            }
        }
        
    def _load_config(self) -> Dict:
        """Load AI model configuration."""
        config_path = Path("configs/ai_models.json")
        if not config_path.exists():
            raise FileNotFoundError("AI models config not found")
        return json.loads(config_path.read_text())

    def get_model_for_task(self, task_type: str, content_length: int) -> Dict:
        """Get appropriate model based on task complexity."""
        if task_type == "scan":
            # Use GPT-3.5 for initial scanning
            return self.config["model_tiers"]["fast"]["providers"][0]
        elif task_type == "analyze":
            # Use GPT-4 for deep analysis
            return self.config["model_tiers"]["depth"]["providers"][0]
        elif task_type == "improve":
            # Use balanced tier for improvements
            return self.config["model_tiers"]["balanced"]["providers"][0]
        
        # Default to fast tier
        return self.config["model_tiers"]["fast"]["providers"][0]

    async def handle_request(self, task_type: str, content_length: int) -> None:
        """Handle request with monitoring."""
        model = self.get_model_for_task(task_type, content_length)
        
        # Calculate cost
        cost = (content_length / 1000) * model["cost"]
        
        # Log request
        self.monitor.log_request(
            model=model["name"],
            tokens=content_length,
            cost=cost
        )
        
        # Check rate limits
        while not self._can_make_request(model["name"], content_length):
            wait_time = self._get_wait_time(model["name"])
            logger.info(f"Rate limit reached for {model['name']}, waiting {wait_time}s")
            await asyncio.sleep(wait_time)
        
        # Track usage
        self._track_request(model["name"], content_length)

    def _can_make_request(self, model: str, tokens: int) -> bool:
        """Check if request can be made within rate limits."""
        now = pendulum.now()
        usage = self.usage[model]
        
        # Reset if minute has passed
        if (now - usage["last_reset"]).total_seconds() >= 60:
            usage["tokens"] = 0
            usage["last_reset"] = now
            usage["requests"] = []
        
        # Check token limit
        limit = self.config["model_tiers"]["fast"]["providers"][0]["rate_limit"] \
            if "3.5" in model else self.config["model_tiers"]["depth"]["providers"][0]["rate_limit"]
            
        return (usage["tokens"] + tokens) <= limit

    def _track_request(self, model: str, tokens: int) -> None:
        """Track request usage."""
        usage = self.usage[model]
        usage["tokens"] += tokens
        usage["requests"].append({
            "tokens": tokens,
            "timestamp": pendulum.now().isoformat()
        })

    def _get_wait_time(self, model: str) -> int:
        """Calculate wait time until next request allowed."""
        now = pendulum.now()
        usage = self.usage[model]
        seconds_since_reset = (now - usage["last_reset"]).total_seconds()
        
        if seconds_since_reset >= 60:
            return 0
            
        return int(60 - seconds_since_reset)

    def get_available_provider(self) -> Dict:
        """Get available provider based on rate limits."""
        for tier in ["fast", "balanced", "depth"]:
            for provider in self.config["model_tiers"][tier]["providers"]:
                if self._can_make_request(provider["name"], 0):
                    return provider
        return None