from pathlib import Path
from typing import Dict, List, Tuple
import tiktoken
import json
from loguru import logger
import os
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
import humanize

class CostEstimator:
    """Estimate API costs and time for code analysis."""
    
    def __init__(self):
        self.console = Console()
        self.config = self._load_config()
        self.encoders = {
            "gpt-3.5-turbo": tiktoken.encoding_for_model("gpt-3.5-turbo"),
            "gpt-4": tiktoken.encoding_for_model("gpt-4")
        }
        
    def _load_config(self) -> Dict:
        """Load AI model configuration."""
        config_path = Path("configs/ai_models.json")
        if not config_path.exists():
            raise FileNotFoundError("AI models config not found")
        return json.loads(config_path.read_text())

    def estimate_project(self, path: str) -> Dict:
        """Estimate full project analysis cost and time."""
        files = self._get_analyzable_files(Path(path))
        
        # Get token counts for all files
        total_tokens = 0
        file_estimates = []
        
        for file in files:
            tokens = self._count_tokens(file)
            total_tokens += tokens
            file_estimates.append({
                "file": str(file),
                "tokens": tokens,
                "tier": self._determine_tier(tokens)
            })
            
        # Calculate costs per tier
        costs = self._calculate_costs(file_estimates)
        time_estimate = self._estimate_time(file_estimates)
        
        return {
            "summary": {
                "total_files": len(files),
                "total_tokens": total_tokens,
                "estimated_cost": sum(costs.values()),
                "estimated_time": time_estimate,
                "cost_breakdown": costs
            },
            "files": file_estimates,
            "recommendations": self._get_recommendations(total_tokens, len(files))
        }
        
    def _get_analyzable_files(self, path: Path) -> List[Path]:
        """Get list of files to analyze."""
        if path.is_file():
            return [path] if self._should_analyze(path) else []
            
        files = []
        for item in path.rglob("*"):
            if item.is_file() and self._should_analyze(item):
                files.append(item)
        return files
        
    def _should_analyze(self, file: Path) -> bool:
        """Check if file should be analyzed."""
        ignore_patterns = [
            ".git", "__pycache__", ".venv",
            ".pyc", ".pyo", ".pyd", ".so"
        ]
        return (
            file.suffix == ".py" and
            not any(pattern in str(file) for pattern in ignore_patterns)
        )
        
    def _count_tokens(self, file: Path) -> int:
        """Count tokens in a file."""
        try:
            content = file.read_text()
            # Use GPT-3.5 encoder as baseline
            return len(self.encoders["gpt-3.5-turbo"].encode(content))
        except Exception as e:
            logger.warning(f"Could not count tokens for {file}: {e}")
            return 0
            
    def _determine_tier(self, tokens: int) -> str:
        """Determine which model tier to use."""
        if tokens < 1000:
            return "fast"
        elif tokens < 4000:
            return "balanced"
        return "depth"
        
    def _calculate_costs(self, files: List[Dict]) -> Dict[str, float]:
        """Calculate costs per tier."""
        costs = {"fast": 0.0, "balanced": 0.0, "depth": 0.0}
        
        for file in files:
            tier = file["tier"]
            tokens = file["tokens"]
            
            # Get cost per 1k tokens for this tier
            provider = self.config["model_tiers"][tier]["providers"][0]
            cost_per_1k = provider["cost"]
            
            # Calculate and add cost
            costs[tier] += (tokens / 1000) * cost_per_1k
            
        return costs
        
    def _estimate_time(self, files: List[Dict]) -> Dict:
        """Estimate processing time based on rate limits."""
        time_per_tier = {"fast": 0, "balanced": 0, "depth": 0}
        
        for file in files:
            tier = file["tier"]
            tokens = file["tokens"]
            
            # Get rate limit for this tier
            provider = self.config["model_tiers"][tier]["providers"][0]
            tokens_per_minute = provider["rate_limit"]
            
            # Add processing time in minutes
            time_per_tier[tier] += tokens / tokens_per_minute
            
        return {
            "minutes": sum(time_per_tier.values()),
            "breakdown": time_per_tier
        }
        
    def _get_recommendations(self, total_tokens: int, file_count: int) -> List[str]:
        """Get optimization recommendations."""
        recommendations = []
        
        if total_tokens > 100000:
            recommendations.append(
                "Consider breaking analysis into smaller batches"
            )
            
        if file_count > 50:
            recommendations.append(
                "Consider analyzing critical files first"
            )
            
        # Add cost-saving recommendations
        if total_tokens < 10000:
            recommendations.append(
                "Use fast tier (GPT-3.5) for initial analysis"
            )
        else:
            recommendations.append(
                "Use tiered approach: GPT-3.5 for scanning, GPT-4 for complex files"
            )
            
        return recommendations 

    def display_estimate(self, estimate: Dict) -> None:
        """Display beautiful cost estimate visualization."""
        # Show summary panel
        summary = Panel(
            f"""[bold green]Project Analysis Estimate[/]
            
Total Files: {estimate['summary']['total_files']}
Total Tokens: {humanize.intcomma(estimate['summary']['total_tokens'])}
Estimated Cost: ${estimate['summary']['estimated_cost']:.2f}
Estimated Time: {estimate['summary']['estimated_time']['minutes']:.1f} minutes
            """,
            title="Summary",
            border_style="green"
        )
        self.console.print(summary)

        # Show cost breakdown table
        table = Table(title="Cost Breakdown by Tier")
        table.add_column("Tier", style="cyan")
        table.add_column("Files", justify="right")
        table.add_column("Tokens", justify="right")
        table.add_column("Cost", justify="right", style="green")
        table.add_column("Time", justify="right", style="yellow")

        for tier, cost in estimate['summary']['cost_breakdown'].items():
            tier_files = len([f for f in estimate['files'] if f['tier'] == tier])
            tier_tokens = sum(f['tokens'] for f in estimate['files'] if f['tier'] == tier)
            tier_time = estimate['summary']['estimated_time']['breakdown'][tier]
            
            table.add_row(
                tier.capitalize(),
                str(tier_files),
                humanize.intcomma(tier_tokens),
                f"${cost:.2f}",
                f"{tier_time:.1f}m"
            )
            
        self.console.print(table)

        # Show file tree with costs
        tree = Tree("📁 Project Analysis")
        for file in estimate['files']:
            cost = (file['tokens'] / 1000) * self.config["model_tiers"][file['tier']]["providers"][0]["cost"]
            file_text = Text(
                f"{file['file']} ({file['tier']}) - {humanize.intcomma(file['tokens'])} tokens, ${cost:.3f}",
                style="blue"
            )
            tree.add(file_text)
            
        self.console.print(tree)

        # Show recommendations
        if estimate['recommendations']:
            rec_panel = Panel(
                "\n".join(f"• {rec}" for rec in estimate['recommendations']),
                title="Optimization Recommendations",
                border_style="yellow"
            )
            self.console.print(rec_panel)

    def optimize_costs(self, estimate: Dict) -> Dict:
        """Suggest cost optimization strategies."""
        optimizations = {
            "strategies": [],
            "potential_savings": 0.0
        }
        
        total_tokens = estimate['summary']['total_tokens']
        total_cost = estimate['summary']['estimated_cost']
        
        # Strategy 1: Batch small files
        small_files = [f for f in estimate['files'] if f['tokens'] < 1000]
        if len(small_files) > 5:
            potential_saving = len(small_files) * 0.002  # Approximate API call overhead
            optimizations["strategies"].append({
                "name": "Batch Small Files",
                "description": f"Combine {len(small_files)} small files into fewer API calls",
                "saving": potential_saving
            })
            optimizations["potential_savings"] += potential_saving

        # Strategy 2: Use GPT-3.5 for simple files
        simple_files = [f for f in estimate['files'] if f['tier'] == 'depth' and f['tokens'] < 2000]
        if simple_files:
            # Calculate savings from using cheaper model
            current_cost = sum((f['tokens'] / 1000) * 0.03 for f in simple_files)  # GPT-4 cost
            new_cost = sum((f['tokens'] / 1000) * 0.002 for f in simple_files)     # GPT-3.5 cost
            saving = current_cost - new_cost
            
            optimizations["strategies"].append({
                "name": "Use GPT-3.5 for Simple Files",
                "description": f"Switch {len(simple_files)} files to GPT-3.5",
                "saving": saving
            })
            optimizations["potential_savings"] += saving

        # Display optimization suggestions
        if optimizations["strategies"]:
            table = Table(title="Cost Optimization Strategies")
            table.add_column("Strategy", style="cyan")
            table.add_column("Description")
            table.add_column("Potential Saving", justify="right", style="green")
            
            for strat in optimizations["strategies"]:
                table.add_row(
                    strat["name"],
                    strat["description"],
                    f"${strat['saving']:.2f}"
                )
                
            self.console.print(table)
            
            savings_panel = Panel(
                f"Total Potential Savings: ${optimizations['potential_savings']:.2f}\n"
                f"Original Cost: ${total_cost:.2f}\n"
                f"Optimized Cost: ${total_cost - optimizations['potential_savings']:.2f}",
                title="Cost Optimization Summary",
                border_style="green"
            )
            self.console.print(savings_panel)
            
        return optimizations 