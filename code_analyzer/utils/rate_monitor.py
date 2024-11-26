from loguru import logger
import pendulum
from typing import Dict
from pathlib import Path
import json
from rich.console import Console
from rich.table import Table
from code_analyzer.monitoring.models import APICall, get_session

class RateMonitor:
    """Monitor API rate limits and usage across the application."""
    
    def __init__(self):
        self.console = Console()
        self.session = get_session()
        
    def log_request(self, model: str, tokens: int, cost: float):
        """Log an API request to database."""
        api_call = APICall(
            model=model,
            tokens=tokens,
            cost=cost,
            endpoint="completion",
            success=1
        )
        self.session.add(api_call)
        self.session.commit()
        
        # Also log to file for immediate feedback
        logger.bind(rate_limit=True, model=model, tokens=tokens).info(
            f"Request: {tokens} tokens (${cost:.4f})"
        )
        
        # Show warning if approaching limits
        self._check_limits(model, tokens)
    
    def display_usage(self):
        """Display current usage statistics."""
        table = Table(title="API Usage Statistics")
        table.add_column("Model", style="cyan")
        table.add_column("Requests", justify="right")
        table.add_column("Tokens", justify="right")
        table.add_column("Cost", justify="right", style="green")
        
        for model, stats in self.usage.items():
            table.add_row(
                model,
                str(stats["requests"]),
                f"{stats['tokens']:,}",
                f"${stats['cost']:.2f}"
            )
            
        self.console.print(table)
        
    def _save_usage(self):
        """Save usage statistics to file."""
        usage_file = self.log_dir / "usage_stats.json"
        current_usage = {
            "timestamp": pendulum.now().isoformat(),
            "usage": self.usage,
            "total_cost": sum(m["cost"] for m in self.usage.values())
        }
        usage_file.write_text(json.dumps(current_usage, indent=2))
        
    def _check_limits(self, model: str, tokens: int):
        """Check if approaching rate limits."""
        # Get limits from config
        limits = {
            "gpt-3.5-turbo": 90000,  # 90% of actual limit
            "gpt-4": 9000            # 90% of actual limit
        }
        
        if model in limits:
            usage = self.usage[model]["tokens"]
            limit = limits[model]
            
            if usage > limit * 0.8:  # 80% warning
                logger.warning(
                    f"⚠️ {model} usage at {usage/limit*100:.1f}% of limit"
                )
            elif usage > limit * 0.95:  # 95% critical
                logger.critical(
                    f"🚨 {model} usage at {usage/limit*100:.1f}% of limit!"
                ) 