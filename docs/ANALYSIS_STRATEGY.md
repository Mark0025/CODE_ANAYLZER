# Code Analysis Strategy 📊

## Analysis Phases and Rate Limiting

### 1. Initial Project Assessment
- Count total files and estimate tokens
- Calculate expected API calls
- Estimate total time and cost
- Show progress bar with ETA

```python
def estimate_analysis_time(project_path: Path) -> Dict:
    files = list(project_path.rglob("*.py"))
    total_lines = sum(len(file.read_text().splitlines()) for file in files)
    
    return {
        "files": len(files),
        "lines": total_lines,
        "estimated_tokens": total_lines * 4,  # Average tokens per line
        "estimated_time": calculate_time_with_rate_limits(total_lines),
        "estimated_cost": calculate_cost(total_lines)
    }
```

### 2. Smart Batching Strategy


1. **File Grouping**
   - Group files by size and complexity
   - Prioritize smaller, simpler files first
   - Use faster models for simple analysis

2. **Rate Limit Management**
   - Track token usage per minute
   - Implement exponential backoff
   - Switch between providers when needed

3. **Progress Tracking**
   ```python
   class AnalysisProgress:
       def __init__(self, total_files: int):
           self.total = total_files
           self.completed = 0
           self.start_time = time.time()
           
       def update(self, files_processed: int):
           self.completed += files_processed
           elapsed = time.time() - self.start_time
           rate = self.completed / elapsed
           eta = (self.total - self.completed) / rate
           return f"Progress: {self.completed}/{self.total} (ETA: {eta:.1f}s)"
   ```

### 3. Model Selection Strategy

#### Fast Tier (Initial Scan)
- Use for: Syntax checking, basic metrics
- Models: GPT-3.5-turbo, Claude-instant
- Rate Limit: 3500 tokens/min
- Cost: $0.002/1K tokens

#### Balanced Tier (Main Analysis)
- Use for: Code review, suggestions
- Models: GPT-4, Claude-2
- Rate Limit: 200-300 tokens/min
- Cost: $0.03/1K tokens

#### Depth Tier (Critical Analysis)
- Use for: Breaking changes, security
- Models: GPT-4-turbo
- Rate Limit: 150 tokens/min
- Cost: $0.01/1K tokens

### 4. Implementation Plan

1. **Analysis Queue System**
```python
class AnalysisQueue:
    def __init__(self, config: Dict):
        self.queues = {
            "fast": deque(),
            "balanced": deque(),
            "depth": deque()
        }
        self.rate_limits = config["rate_limit_strategies"]
        
    def add_task(self, file: Path, priority: str):
        complexity = analyze_file_complexity(file)
        tier = self.determine_tier(complexity)
        self.queues[tier].append((file, priority))
        
    async def process_queue(self):
        while any(self.queues.values()):
            for tier in self.queues:
                if self.queues[tier]:
                    await self.process_batch(tier)
                    await self.apply_rate_limit(tier)
```

2. **Rate Limit Handler**
```python
class RateLimitHandler:
    def __init__(self):
        self.provider_limits = {}
        self.usage_tracking = defaultdict(int)
        
    async def handle_rate_limit(self, provider: str):
        if self.is_rate_limited(provider):
            await self.apply_backoff_strategy(provider)
            return self.get_alternative_provider()
        return provider
        
    def track_usage(self, provider: str, tokens: int):
        self.usage_tracking[provider] += tokens
```

### 5. Progress Reporting

1. **Console Output**
```
Analyzing FINANCES project:
Files: 150 | Lines: 25,000 | Est. Time: 45min
Progress: [===========------] 65%
Current: analyzing melbudget/core/
Rate Limits: OpenAI(70%), Anthropic(45%)
ETA: 15min remaining
```

2. **Detailed Logging**
```python
logger.info(f"Analysis Progress: {progress.completed}/{progress.total}")
logger.debug(f"Rate Limit Status: {rate_handler.get_status()}")
logger.info(f"Current Model: {current_model} ({current_provider})")
```

## Environment Setup
1. Create .env file with required keys
2. Load environment variables
3. Validate API key presence and format
4. Use environment variables throughout

## Testing Strategy
1. Use fixtures for environment setup
2. No hardcoded values
3. Proper error handling
4. Clear logging

## Next Steps

1. [ ] Implement smart batching system
2. [ ] Add provider rotation logic
3. [ ] Create progress visualization
4. [ ] Add cost estimation and tracking
5. [ ] Implement adaptive model selection 