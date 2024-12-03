# Learning Python Code Analysis 🎣

I'm a Python developer wanting to understand code analysis concepts so I can build better analysis tools and improve my programming skills.

## SUB_TOPICS
- File System Operations
- Async Programming
- Resource Management
- Error Handling
- Logging Best Practices
- Code Analysis Patterns

## Chapter 1: File System Operations 📂

Let's understand how we handle files safely:

```python
# BAD: Files might not close properly
def process_file(file_path):
    content = open(file_path).read()
    return analyze_content(content)

# GOOD: Context manager ensures cleanup
def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return analyze_content(content)
```

Real World Use Cases:
1. Reading source code files
2. Processing large codebases
3. Handling multiple file types

Example:
```python
from pathlib import Path

def analyze_directory(directory: Path):
    """Safely analyze directory contents."""
    try:
        # Use pathlib for modern path handling
        for file_path in directory.rglob('*.py'):
            with file_path.open() as f:
                content = f.read()
                yield analyze_content(content)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
```

## Chapter 2: Async Programming ⚡

Understanding async operations in analysis:

```python
# BAD: Blocking operations
def analyze_files(files):
    for file in files:
        result = analyze_file(file)
        save_result(result)

# GOOD: Async operations
async def analyze_files(files):
    tasks = [analyze_file(file) for file in files]
    results = await asyncio.gather(*tasks)
    await save_results(results)
```

Real World Use Cases:
1. Analyzing multiple files concurrently
2. Making API calls efficiently
3. Handling long-running operations

Example:
```python
async def analyze_with_progress():
    """Analyze files with progress tracking."""
    async with aiofiles.open('large_file.py') as f:
        content = await f.read()
        
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(analyze_chunk(chunk))
            for chunk in split_content(content)
        ]
    
    return [task.result() for task in tasks]
```

## Chapter 3: Resource Management 🔧

Managing system resources effectively:

```python
# BAD: Resource leaks possible
class Analyzer:
    def __init__(self):
        self.file = open('analysis.log', 'w')
        
    def analyze(self):
        self.file.write('Starting analysis...')

# GOOD: Proper resource management
class Analyzer:
    def __init__(self):
        self._file = None
        
    async def __aenter__(self):
        self._file = await aiofiles.open('analysis.log', 'w')
        return self
        
    async def __aexit__(self, exc_type, exc, tb):
        await self._file.close()
```

Real World Use Cases:
1. Managing file handles
2. Database connections
3. Network resources

## Chapter 4: Error Handling 🚨

Robust error handling patterns:

```python
# BAD: Generic error handling
try:
    analyze_code()
except Exception as e:
    print(f"Error: {e}")

# GOOD: Specific error handling
try:
    analyze_code()
except SyntaxError as e:
    logger.error(f"Syntax error in code: {e}")
except MemoryError as e:
    logger.critical(f"Out of memory: {e}")
except Exception as e:
    logger.exception("Unexpected error during analysis")
finally:
    cleanup_resources()
```

## Chapter 5: Logging Best Practices 📝

Professional logging patterns:

```python
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Structured logging
logger.info("Analysis started", extra={
    'files_count': len(files),
    'start_time': time.time(),
    'analyzer_version': '1.0.0'
})
```

## Chapter 6: Code Analysis Patterns 🔍

Common analysis patterns:

```python
# Pattern 1: Visitor Pattern
class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        
    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

# Pattern 2: Builder Pattern
class AnalysisBuilder:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self._analysis = Analysis()
        
    def add_metrics(self, metrics):
        self._analysis.metrics = metrics
        return self
        
    def add_suggestions(self, suggestions):
        self._analysis.suggestions = suggestions
        return self
```

## Exercises 🏋️‍♂️

1. File Handling:
```python
# Exercise: Implement safe file reading
def read_files_safely(directory: Path) -> List[str]:
    """
    Read all Python files in directory safely.
    Return list of file contents.
    """
    # Your code here
    pass
```

2. Async Analysis:
```python
# Exercise: Implement concurrent file analysis
async def analyze_files_concurrently(
    files: List[Path],
    max_concurrent: int = 5
) -> List[Dict]:
    """
    Analyze multiple files concurrently with limit.
    Return analysis results.
    """
    # Your code here
    pass
```

## Additional Resources 📚
1. Python AST Module Documentation
2. asyncio Documentation
3. pathlib Tutorial
4. Python Design Patterns
5. Logging Cookbook

Would you like to:
1. Try the exercises?
2. Learn more about specific topics?
3. See more real-world examples? 